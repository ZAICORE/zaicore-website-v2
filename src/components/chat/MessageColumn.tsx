"use client";

import { useEffect, useRef } from "react";
import { motion } from "motion/react";
import type { ChatMessage } from "@/lib/chat/types";
import styles from "./glass.module.css";

type Props = {
  messages: ChatMessage[];
  streaming: boolean;
};

export function MessageColumn({ messages, streaming }: Props) {
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }, [messages, streaming]);

  const visible = messages.filter((m) => m.role === "user" || m.role === "assistant");
  if (visible.length === 0) return null;

  const lastIdx = visible.length - 1;

  return (
    <div
      ref={scrollRef}
      className={`overflow-y-auto ${styles.scrollArea}`}
      style={{ maxHeight: "56vh" }}
    >
      <div className="flex flex-col gap-2 py-1">
        {visible.map((m, idx) => {
          const isLastAssistant =
            idx === lastIdx && m.role === "assistant" && streaming;
          const isUser = m.role === "user";

          return (
            <motion.div
              key={m.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
              className={
                isUser
                  ? "self-end max-w-[86%] rounded-[18px] bg-ink/90 text-cream px-3.5 py-2 text-[0.9rem] leading-[1.48]"
                  : "self-start max-w-[94%] rounded-[18px] bg-white/58 backdrop-blur-md border border-white/52 px-3.5 py-2 text-[0.9rem] leading-[1.52] text-ink whitespace-pre-wrap"
              }
            >
              {m.content || (streaming && m.role === "assistant" ? "" : "")}
              {isLastAssistant && <span className={styles.streamCursor} aria-hidden="true" />}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
