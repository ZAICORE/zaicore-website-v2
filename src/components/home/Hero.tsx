"use client";

import { motion } from "motion/react";
import { hero } from "@/content/hero";
import { Button } from "@/components/ui/Button";
import { MediaSlot } from "@/components/media/MediaSlot";

export function Hero() {
  return (
    <section className="relative w-full overflow-hidden bg-[color:var(--cream)] pt-28 md:pt-32">
      {/* Ambient grid + radial vignette — Kyle-Skelly style, very subtle */}
      <BackgroundGrid />

      <div className="relative mx-auto flex w-full max-w-[1400px] flex-col items-center px-6 pb-24 md:px-10 md:pb-32 lg:px-14">
        {/* Eyebrow */}
        <motion.p
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1], delay: 0.15 }}
          className="eyebrow text-center"
        >
          {hero.eyebrow}
        </motion.p>

        {/* Title row — LEFT MASCOT · CENTER COLUMN · RIGHT MASCOT */}
        <div className="mt-8 grid w-full grid-cols-[minmax(0,1fr)_minmax(0,auto)_minmax(0,1fr)] items-end gap-4 md:mt-6 md:gap-6 lg:gap-8">
          <MascotSlot side="left" id={hero.mascots.left.id} delay={0.4} />

          <div className="flex flex-col items-center justify-end pb-6 md:pb-10">
            <motion.h1
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
              className="display max-w-[720px] text-center text-[clamp(2rem,5.8vw,5rem)] text-ink"
            >
              {hero.headline.lead}
              <br />
              <span className="serif-italic text-[color:var(--lapis-glow)]">
                {hero.headline.italic}
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.55 }}
              className="mt-8 max-w-2xl text-center text-[1.05rem] leading-[1.6] text-muted md:text-[1.12rem]"
            >
              {hero.subline}
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.7 }}
              className="mt-8 flex flex-wrap items-center justify-center gap-3"
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

          <MascotSlot side="right" id={hero.mascots.right.id} delay={0.5} />
        </div>

        {/* Live dot */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1 }}
          className="mt-8 flex items-center gap-3 text-[0.8rem] text-muted"
        >
          <span className="relative flex h-2 w-2">
            <span className="absolute inset-0 animate-ping rounded-full bg-[color:var(--signal)] opacity-70" />
            <span className="relative h-2 w-2 rounded-full bg-[color:var(--signal)]" />
          </span>
          <span>Currently building. Open for select engagements.</span>
        </motion.div>
      </div>
    </section>
  );
}

/**
 * Free-standing mascot slot — no frame, no container, no label. Character (when
 * present) sits directly on the hero background just like Kyle Skelly's
 * characters on the Sculpt site.
 */
function MascotSlot({ side, id, delay }: { side: "left" | "right"; id: string; delay: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1, ease: [0.22, 1, 0.36, 1], delay }}
      className={`relative flex items-end ${side === "left" ? "justify-end" : "justify-start"}`}
    >
      <MediaSlot
        assetId={id}
        aspect="aspect-[3/4]"
        rounded="rounded-none"
        showGrain={false}
        className="w-full max-w-[340px] md:max-w-[420px] lg:max-w-[500px] bg-transparent"
      />
    </motion.div>
  );
}

function BackgroundGrid() {
  return (
    <div
      aria-hidden
      className="pointer-events-none absolute inset-0 -z-10"
      style={{
        backgroundImage:
          "linear-gradient(to right, rgba(14,14,16,0.035) 1px, transparent 1px), linear-gradient(to bottom, rgba(14,14,16,0.035) 1px, transparent 1px)",
        backgroundSize: "64px 64px",
        maskImage:
          "radial-gradient(ellipse 85% 70% at 50% 45%, #000 30%, transparent 75%)",
        WebkitMaskImage:
          "radial-gradient(ellipse 85% 70% at 50% 45%, #000 30%, transparent 75%)",
      }}
    />
  );
}
