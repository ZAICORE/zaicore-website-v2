"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";

export function Stagger({
  children,
  delay = 0,
  stagger = 0.08,
  className,
}: {
  children: ReactNode;
  delay?: number;
  stagger?: number;
  className?: string;
}) {
  return (
    <motion.div
      initial="hidden"
      whileInView="shown"
      viewport={{ once: true, margin: "-80px" }}
      variants={{
        hidden: {},
        shown: { transition: { delayChildren: delay, staggerChildren: stagger } },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

export function StaggerItem({
  children,
  y = 16,
  duration = 0.7,
  className,
}: {
  children: ReactNode;
  y?: number;
  duration?: number;
  className?: string;
}) {
  return (
    <motion.div
      variants={{
        hidden: { opacity: 0, y },
        shown: { opacity: 1, y: 0, transition: { duration, ease: [0.22, 1, 0.36, 1] } },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
