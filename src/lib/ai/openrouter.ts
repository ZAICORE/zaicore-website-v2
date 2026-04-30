import type { ToolDefinition } from "./tools";

const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";

export const PRIMARY_MODEL = "xiaomi/mimo-v2-flash";
export const FALLBACK_MODEL = "x-ai/grok-4.1-fast";

export type ORMessage = {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  tool_calls?: Array<{
    id: string;
    type: "function";
    function: { name: string; arguments: string };
  }>;
  tool_call_id?: string;
  name?: string;
};

export type ORStreamChunk = {
  id?: string;
  choices?: Array<{
    delta?: {
      content?: string;
      // reasoning tokens (mimo-v2-flash emits these -- ignored by our consumer)
      reasoning?: string;
      tool_calls?: Array<{
        index: number;
        id?: string;
        type?: "function";
        function?: { name?: string; arguments?: string };
      }>;
    };
    finish_reason?: string | null;
  }>;
};

export type ORRequest = {
  messages: ORMessage[];
  tools?: ToolDefinition[];
  model?: string;
  temperature?: number;
  max_tokens?: number;
  signal?: AbortSignal;
};

function getApiKey(): string {
  const k = process.env.OPENROUTER_API_KEY;
  if (!k) throw new Error("Missing OPENROUTER_API_KEY");
  return k;
}

export async function streamChat(req: ORRequest): Promise<Response> {
  const body = {
    model: req.model ?? PRIMARY_MODEL,
    messages: req.messages,
    stream: true,
    temperature: req.temperature ?? 0.4,
    max_tokens: req.max_tokens ?? 1024,
    tools: req.tools,
    tool_choice: req.tools ? "auto" : undefined,
  };

  const res = await fetch(OPENROUTER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getApiKey()}`,
      "HTTP-Referer": "https://zaicore.com",
      "X-Title": "ZAICORE Chat Dock",
    },
    body: JSON.stringify(body),
    signal: req.signal,
  });

  if (!res.ok || !res.body) {
    const text = await res.text().catch(() => "");
    throw new Error(`OpenRouter error ${res.status}: ${text}`);
  }
  return res;
}

export async function* parseSSE(
  stream: ReadableStream<Uint8Array>,
): AsyncGenerator<ORStreamChunk> {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed.startsWith("data:")) continue;
        const payload = trimmed.slice(5).trim();
        if (payload === "[DONE]") return;
        if (!payload) continue;
        try {
          yield JSON.parse(payload) as ORStreamChunk;
        } catch {
          // skip malformed SSE line
        }
      }
    }
  } finally {
    await reader.cancel().catch(() => {});
  }
}
