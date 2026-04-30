import { NextResponse } from "next/server";
import {
  streamChat,
  parseSSE,
  PRIMARY_MODEL,
  FALLBACK_MODEL,
  type ORMessage,
} from "@/lib/ai/openrouter";
import { TOOLS, executeTool } from "@/lib/ai/tools";
import { buildSystemPrompt } from "@/lib/ai/system-prompt";
import type { ChatMessage, SSEEvent } from "@/lib/chat/types";

export const runtime = "nodejs";

// In-memory rate limit bucket -- resets on server restart (acceptable for this use case)
const buckets = new Map<string, { count: number; resetAt: number }>();
const WINDOW_MS = 60 * 60 * 1000; // 1 hour
const MAX_PER_WINDOW = 60;
const MAX_INPUT_LEN = 4000;
const MAX_TOOL_ITERATIONS = 3;

function rateLimited(ip: string): boolean {
  const now = Date.now();
  const b = buckets.get(ip);
  if (!b || b.resetAt < now) {
    buckets.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return false;
  }
  b.count += 1;
  return b.count > MAX_PER_WINDOW;
}

function clientToOR(messages: ChatMessage[]): ORMessage[] {
  return messages.map((m): ORMessage => {
    if (m.role === "tool") {
      return {
        role: "tool",
        content: m.content,
        tool_call_id: m.toolCallId ?? "",
      };
    }
    if (m.role === "assistant" && m.toolCalls?.length) {
      return {
        role: "assistant",
        content: m.content,
        tool_calls: m.toolCalls.map((t) => ({
          id: t.id,
          type: "function" as const,
          function: { name: t.name, arguments: JSON.stringify(t.arguments) },
        })),
      };
    }
    if (m.role === "user" || m.role === "assistant") {
      return { role: m.role, content: m.content };
    }
    // system messages from client are dropped -- server injects its own
    return { role: "user", content: m.content };
  });
}

function encodeSSE(event: SSEEvent): string {
  return `data: ${JSON.stringify(event)}\n\n`;
}

export async function POST(req: Request) {
  const ip =
    req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ?? "unknown";

  // Parse and validate BEFORE consuming quota -- only count requests that will be processed
  let payload: { messages?: ChatMessage[] };
  try {
    payload = (await req.json()) as { messages?: ChatMessage[] };
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const messages = payload.messages;
  if (!Array.isArray(messages) || messages.length === 0) {
    return NextResponse.json({ error: "messages required" }, { status: 400 });
  }

  const last = messages[messages.length - 1];
  if (
    !last ||
    last.role !== "user" ||
    !last.content ||
    last.content.length > MAX_INPUT_LEN
  ) {
    return NextResponse.json(
      { error: "Last message must be a user message under 4000 chars" },
      { status: 400 },
    );
  }

  // Validation passed -- now charge the rate limit bucket
  if (rateLimited(ip)) {
    return NextResponse.json(
      { error: "Slow down -- try again in an hour." },
      { status: 429 },
    );
  }

  const orMessages: ORMessage[] = [
    { role: "system", content: buildSystemPrompt() },
    ...clientToOR(messages),
  ];

  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      const send = (event: SSEEvent) => {
        // I1: guard enqueue -- client may have disconnected, making this throw
        try {
          controller.enqueue(encoder.encode(encodeSSE(event)));
        } catch {
          // client gone -- swallow; the abort signal will unwind the loop
        }
      };

      try {
        let iteration = 0;
        let model = PRIMARY_MODEL;
        let sentDone = false; // B1: track whether we already sent the done event

        while (iteration < MAX_TOOL_ITERATIONS) {
          iteration++;

          // Primary model with one fallback retry on initial connection failure
          let res: Response;
          try {
            res = await streamChat({ messages: orMessages, tools: TOOLS, model, signal: req.signal });
          } catch (err) {
            if (model === PRIMARY_MODEL) {
              model = FALLBACK_MODEL;
              res = await streamChat({
                messages: orMessages,
                tools: TOOLS,
                model,
                signal: req.signal,
              });
            } else {
              throw err;
            }
          }

          let assistantContent = "";
          // Map<chunkIndex, accumulated tool call state>
          const toolCallsAcc = new Map<
            number,
            { id: string; name: string; argString: string }
          >();
          let finishReason: string | null = null;

          for await (const chunk of parseSSE(res.body!)) {
            const choice = chunk.choices?.[0];
            const delta = choice?.delta;

            if (delta?.content) {
              assistantContent += delta.content;
              send({ type: "token", content: delta.content });
            }

            // Accumulate streamed tool_calls -- arguments arrive in fragments
            if (delta?.tool_calls) {
              for (const tc of delta.tool_calls) {
                const idx = tc.index;
                const existing = toolCallsAcc.get(idx) ?? {
                  id: "",
                  name: "",
                  argString: "",
                };
                if (tc.id) existing.id = tc.id;
                if (tc.function?.name) existing.name = tc.function.name;
                if (tc.function?.arguments)
                  existing.argString += tc.function.arguments;
                toolCallsAcc.set(idx, existing);
              }
            }

            if (choice?.finish_reason) {
              finishReason = choice.finish_reason;
            }
          }

          // No tool calls -- stream is complete
          if (toolCallsAcc.size === 0) {
            sentDone = true; // B1: mark so the trailing guard below doesn't double-emit
            send({ type: "done" });
            break;
          }

          // Persist assistant turn with tool_calls before executing them
          const toolCalls = [...toolCallsAcc.values()];
          orMessages.push({
            role: "assistant",
            content: assistantContent,
            tool_calls: toolCalls.map((t) => ({
              id: t.id,
              type: "function",
              function: { name: t.name, arguments: t.argString },
            })),
          });

          // Execute each tool and feed result back into orMessages
          for (const tc of toolCalls) {
            let parsedArgs: unknown = {};
            try {
              parsedArgs = JSON.parse(tc.argString || "{}");
            } catch {
              // empty args -- executeTool will return a validation error
            }

            send({
              type: "tool_call",
              toolName: tc.name,
              toolArgs: parsedArgs as Record<string, unknown>,
            });

            const result = await executeTool(tc.name, parsedArgs, messages);

            send({
              type: "tool_result",
              toolName: tc.name,
              ok: result.ok,
              message: result.message,
            });

            orMessages.push({
              role: "tool",
              content: JSON.stringify(result),
              tool_call_id: tc.id,
            });
          }

          // If the model signaled it's done after tool results, stop
          if (finishReason !== "tool_calls") break;
          // Otherwise loop -- model will process tool results and continue
        }

        // If we exhausted iterations without a done event, close cleanly
        // B1: only emit if the natural-finish branch hasn't already sent one
        if (!sentDone) {
          send({ type: "done" });
        }
      } catch (err) {
        const msg = err instanceof Error ? err.message : "stream error";
        controller.enqueue(encoder.encode(encodeSSE({ type: "error", message: msg })));
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}
