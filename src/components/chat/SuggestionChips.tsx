"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";

const POOL = [
  "What does ZAICORE build?",
  "Tell me about ZAICORE Security",
  "Book a call with Zach",
  "Who's the CEO?",
  "What engineering work do you do?",
  "How does ZAICORE Security work?",
];

const VISIBLE_COUNT = 3;
const ROTATION_MS = 6000;

type Props = {
  onPick: (q: string) => void;
};

function pickThree(offset: number): string[] {
  return Array.from({ length: VISIBLE_COUNT }, (_, i) => POOL[(offset + i) % POOL.length]);
}

export function SuggestionChips({ onPick }: Props) {
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    const id = window.setInterval(() => {
      setOffset((o) => (o + VISIBLE_COUNT) % POOL.length);
    }, ROTATION_MS);
    return () => window.clearInterval(id);
  }, []);

  const chips = pickThree(offset);

  return (
    <div className="flex flex-wrap gap-1.5 justify-end">
      <AnimatePresence mode="popLayout">
        {chips.map((q, i) => (
          <motion.button
            key={q}
            initial={{ opacity: 0, y: 6, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -5, scale: 0.97 }}
            transition={{
              duration: 0.38,
              ease: [0.22, 1, 0.36, 1],
              delay: i * 0.04,
            }}
            onClick={() => onPick(q)}
            className="rounded-full border border-white/52 bg-white/46 px-3 py-1.5 text-[0.76rem] font-medium text-ink/80 backdrop-blur-md hover:bg-white/68 hover:text-ink hover:border-white/70 transition-colors duration-200 cursor-pointer select-none"
            type="button"
          >
            {q}
          </motion.button>
        ))}
      </AnimatePresence>
    </div>
  );
}
