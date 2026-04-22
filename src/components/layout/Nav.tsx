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
        <Link href="/" className="flex items-center gap-2">
          <LogoMark />
          <span className="text-[0.95rem] font-medium tracking-[-0.01em]">{site.name}</span>
        </Link>

        <div className="hidden items-center gap-1 md:flex">
          {nav.primary.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "relative rounded-full px-4 py-2 text-sm transition-colors",
                "hover:bg-[color:var(--hairline)]/60",
                "accent" in item && item.accent && "text-ink",
              )}
            >
              {"accent" in item && item.accent && (
                <span
                  aria-hidden
                  className="absolute left-3 top-1/2 h-1.5 w-1.5 -translate-y-1/2 rounded-full bg-[color:var(--signal)] shadow-[0_0_12px_rgba(44,221,233,0.7)]"
                />
              )}
              <span className={"accent" in item && item.accent ? "pl-4" : ""}>{item.label}</span>
            </Link>
          ))}
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

function LogoMark() {
  return (
    <span
      aria-hidden
      className="relative inline-flex h-7 w-7 items-center justify-center"
    >
      <span className="absolute inset-0 rounded-[9px] bg-gradient-to-br from-[color:var(--lapis-glow)] via-[color:var(--lapis)] to-[color:var(--ink)]" />
      <span className="relative h-2 w-2 rounded-full bg-[color:var(--signal)] shadow-[0_0_10px_rgba(44,221,233,0.9)]" />
    </span>
  );
}
