"use client";

import { motion } from "motion/react";
import { hero } from "@/content/hero";
import { Button } from "@/components/ui/Button";
import { MediaSlot } from "@/components/media/MediaSlot";

/**
 * Minimal hero — Kyle Skelly / Sculpt pattern.
 * Big centered title. Tiny subtitle. Two CTAs. Two characters flanking.
 * Everything else (engineering depth, security depth) lives in scroll sections.
 */
export function Hero() {
  return (
    <section className="relative w-full overflow-hidden bg-[color:var(--cream)] pt-28 md:pt-32">
      <div className="relative mx-auto flex w-full max-w-[1600px] flex-col items-center px-6 pb-20 md:px-10 md:pb-28 lg:px-14">
        <div className="grid w-full grid-cols-[minmax(0,1.1fr)_minmax(0,auto)_minmax(0,1.1fr)] items-end gap-2 md:gap-6 lg:gap-10">
          <MascotSlot side="left" id={hero.mascots.left.id} delay={0.35} />

          <div className="flex min-w-0 flex-col items-center justify-end pb-10 md:pb-16">
            <motion.h1
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1], delay: 0.25 }}
              className="display max-w-[760px] text-center text-[clamp(2.2rem,6vw,5.6rem)] text-ink"
            >
              {hero.headline.lead}
              <br />
              <span className="serif-italic text-[color:var(--lapis-glow)]">
                {hero.headline.italic}
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.5 }}
              className="mt-6 max-w-xl text-center text-[0.95rem] leading-[1.55] text-muted md:text-[1rem]"
            >
              {hero.subline}
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.65 }}
              className="mt-7 flex flex-wrap items-center justify-center gap-3"
            >
              {hero.ctas.map((cta) => (
                <Button
                  key={cta.label}
                  href={cta.href}
                  label={cta.label}
                  variant={cta.variant}
                  external={cta.external}
                />
              ))}
            </motion.div>
          </div>

          <MascotSlot side="right" id={hero.mascots.right.id} delay={0.45} />
        </div>
      </div>
    </section>
  );
}

function MascotSlot({ side, id, delay }: { side: "left" | "right"; id: string; delay: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1, ease: [0.22, 1, 0.36, 1], delay }}
      className={`relative flex items-end ${side === "left" ? "justify-start pl-0" : "justify-end pr-0"}`}
    >
      <MediaSlot
        assetId={id}
        aspect="aspect-[3/4]"
        rounded="rounded-none"
        showGrain={false}
        className="w-full max-w-[320px] md:max-w-[400px] lg:max-w-[480px] bg-transparent"
      />
    </motion.div>
  );
}
