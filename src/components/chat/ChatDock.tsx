"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { GlassBar } from "./GlassBar";
import { MessageColumn } from "./MessageColumn";
import {
  loadConversation,
  saveConversation,
  newConversation,
  appendMessage,
  updateLastAssistantMessage,
} from "@/lib/chat/storage";
import type { ChatMessage, SSEEvent, StoredConversation } from "@/lib/chat/types";

function uid(): string {
  return crypto.randomUUID();
}

export function ChatDock() {
  const [conv, setConv] = useState<StoredConversation | null>(null);
  const [expanded, setExpanded] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  // Hydrate from localStorage after mount (avoids SSR mismatch).
  // localStorage is not available server-side, so we must read it in a client-only
  // mount effect and set state once. Always start collapsed -- user must click
  // to open, even if there's prior conversation history.
  useEffect(() => {
    const stored = loadConversation();
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setConv(stored ?? newConversation());
  }, []);

  // Persist on every conv change
  useEffect(() => {
    if (conv) saveConversation(conv);
  }, [conv]);

  // Escape collapses (when not streaming)
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape" && expanded && !streaming) {
        setExpanded(false);
      }
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [expanded, streaming]);

  const send = useCallback(
    async (text: string) => {
      if (!conv || streaming || !text.trim()) return;

      setError(null);
      setExpanded(true);
      setInputValue("");

      const userMsg: ChatMessage = {
        id: uid(),
        role: "user",
        content: text.trim(),
        timestamp: Date.now(),
      };
      const assistantMsg: ChatMessage = {
        id: uid(),
        role: "assistant",
        content: "",
        timestamp: Date.now(),
      };

      // Build the conversation snapshot to send (user messages before the new assistant stub)
      const withUser = appendMessage(conv, userMsg);
      const withBoth = appendMessage(withUser, assistantMsg);
      setConv(withBoth);
      setStreaming(true);

      const ctrl = new AbortController();
      abortRef.current = ctrl;

      try {
        const res = await fetch("/api/chat/stream", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          // Send all messages except the trailing empty assistant stub
          body: JSON.stringify({ messages: withUser.messages }),
          signal: ctrl.signal,
        });

        if (!res.ok || !res.body) {
          const data = await res.json().catch(() => ({})) as { error?: string };
          throw new Error(data.error ?? `Request failed (${res.status})`);
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let assistantContent = "";

        // Coalesce token updates into one render per animation frame instead of
        // one per token. mimo-flash emits 30-50 tokens/sec; rendering each one
        // causes visible jitter. rAF batching gives smooth ~60fps reveals.
        let pendingFrame: number | null = null;
        const flushContent = () => {
          pendingFrame = null;
          const snapshot = assistantContent;
          setConv((prev) =>
            prev
              ? updateLastAssistantMessage(prev, (m) => ({ ...m, content: snapshot }))
              : prev,
          );
        };
        const scheduleFlush = () => {
          if (pendingFrame === null) {
            pendingFrame = requestAnimationFrame(flushContent);
          }
        };

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
            if (!payload) continue;

            let event: SSEEvent;
            try {
              event = JSON.parse(payload) as SSEEvent;
            } catch {
              continue;
            }

            if (event.type === "token") {
              assistantContent += event.content;
              scheduleFlush();
            } else if (event.type === "error") {
              throw new Error(event.message);
            }
            // tool_call / tool_result / done -- no visible UI action needed
          }
        }

        // Flush any tail content before exiting the streaming state
        if (pendingFrame !== null) {
          cancelAnimationFrame(pendingFrame);
        }
        flushContent();
      } catch (err) {
        if (err instanceof Error && err.name === "AbortError") return;
        const msg = err instanceof Error ? err.message : "Something went wrong.";
        setError(msg);
      } finally {
        setStreaming(false);
        abortRef.current = null;
      }
    },
    [conv, streaming],
  );

  // Hydration guard -- don't render until client state is ready
  if (!conv) return null;

  const visibleMessages = conv.messages.filter(
    (m) => m.role === "user" || m.role === "assistant",
  );
  const hasMessages = visibleMessages.length > 0;

  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-0 z-50 flex justify-center px-3 pb-7 sm:px-4 sm:pb-10">
      <div className="pointer-events-auto flex w-full max-w-[400px] flex-col gap-2 sm:max-w-[420px]">

        {/* Message column (expanded + has content) */}
        <AnimatePresence>
          {expanded && hasMessages && (
            <motion.div
              key="messages"
              initial={{ opacity: 0, y: 14, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 10, scale: 0.98 }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
              className="rounded-[20px] border border-white/55 bg-white/46 backdrop-blur-2xl shadow-[0_20px_52px_-12px_rgba(14,14,16,0.18),0_3px_8px_-2px_rgba(14,14,16,0.08)] p-3"
            >
              <MessageColumn messages={conv.messages} streaming={streaming} />
              <AnimatePresence>
                {error && (
                  <motion.p
                    key="error"
                    initial={{ opacity: 0, y: 4 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="mt-2 text-[0.78rem] text-[color:#b84b4b]"
                    role="alert"
                  >
                    {error}
                  </motion.p>
                )}
              </AnimatePresence>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Input bar -- always visible */}
        <GlassBar
          expanded={expanded}
          disabled={streaming}
          value={inputValue}
          onChange={setInputValue}
          onSubmit={() => void send(inputValue)}
          onCollapse={() => setExpanded(false)}
          onFocus={() => setExpanded(true)}
        />
      </div>
    </div>
  );
}
