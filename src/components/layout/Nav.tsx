"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { cn } from "@/lib/cn";
import { nav, site } from "@/content/site";

export function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <motion.header
      initial={{ y: -16, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
      className={cn(
        "fixed left-0 right-0 top-0 z-50 transition-[background,backdrop-filter,border-color] duration-500",
        scrolled
          ? "border-b border-hairline bg-[color:var(--cream)]/80 backdrop-blur-xl"
          : "border-b border-transparent bg-transparent",
      )}
    >
      <nav className="mx-auto flex w-full max-w-[1280px] items-center justify-between px-6 py-4 md:px-10 md:py-5 lg:px-14">
        <Link href="/" className="flex items-center">
          <span className="text-[1.05rem] font-bold uppercase tracking-[-0.04em] text-ink">{site.name}</span>
        </Link>

        <div className="hidden items-center gap-1 md:flex">
          {nav.primary.map((item) =>
            item.external ? (
              <a
                key={item.href}
                href={item.href}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full px-4 py-2 text-sm text-ink-soft transition-colors hover:text-ink"
              >
                {item.label}
              </a>
            ) : (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-full px-4 py-2 text-sm text-ink-soft transition-colors hover:text-ink"
              >
                {item.label}
              </Link>
            ),
          )}
        </div>

        <Link
          href={nav.cta.href}
          className="hidden rounded-full bg-ink px-4 py-2 text-sm font-medium text-cream transition-transform duration-300 hover:-translate-y-0.5 md:inline-block"
        >
          {nav.cta.label}
        </Link>
      </nav>
    </motion.header>
  );
}
