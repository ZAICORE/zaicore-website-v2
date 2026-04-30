"use client";

import { useRef, type FormEvent, type KeyboardEvent } from "react";
import { ArrowUp, ChevronDown } from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import styles from "./glass.module.css";

type Props = {
  expanded: boolean;
  disabled: boolean;
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
  onCollapse: () => void;
  onFocus: () => void;
};

export function GlassBar({
  expanded,
  disabled,
  value,
  onChange,
  onSubmit,
  onCollapse,
  onFocus,
}: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!value.trim() || disabled) return;
    onSubmit();
  }

  function handleKey(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Escape" && expanded) {
      onCollapse();
      inputRef.current?.blur();
    }
  }

  const canSend = value.trim().length > 0 && !disabled;

  return (
    <form
      onSubmit={handleSubmit}
      className={`${styles.glass} flex items-center gap-1.5 px-2.5 py-2`}
    >
      <AnimatePresence>
        {expanded && (
          <motion.button
            key="collapse"
            type="button"
            onClick={onCollapse}
            aria-label="Collapse chat"
            initial={{ opacity: 0, scale: 0.8, width: 0 }}
            animate={{ opacity: 1, scale: 1, width: 32 }}
            exit={{ opacity: 0, scale: 0.8, width: 0 }}
            transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
            className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full text-muted hover:text-ink hover:bg-black/06 transition-colors duration-150"
          >
            <ChevronDown className="h-4 w-4" strokeWidth={2} />
          </motion.button>
        )}
      </AnimatePresence>

      <input
        ref={inputRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={onFocus}
        onKeyDown={handleKey}
        placeholder="Ask ZAICORE anything..."
        disabled={disabled}
        maxLength={4000}
        autoComplete="off"
        spellCheck={false}
        className="flex-1 min-w-0 bg-transparent text-[0.93rem] text-ink placeholder:text-ink/36 outline-none px-1.5 py-1 disabled:opacity-50"
      />

      <motion.button
        type="submit"
        disabled={!canSend}
        aria-label="Send"
        whileHover={canSend ? { scale: 1.06, y: -1 } : {}}
        whileTap={canSend ? { scale: 0.94 } : {}}
        transition={{ duration: 0.15, ease: [0.22, 1, 0.36, 1] }}
        className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-ink text-cream transition-opacity duration-200 disabled:opacity-30 cursor-pointer disabled:cursor-default"
      >
        <ArrowUp className="h-3.5 w-3.5" strokeWidth={2.3} />
      </motion.button>
    </form>
  );
}
