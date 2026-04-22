"use client";

import { motion } from "motion/react";
import { hero } from "@/content/hero";
import { Button } from "@/components/ui/Button";
import { MediaSlot } from "@/components/media/MediaSlot";

export function Hero() {
  return (
    <section className="relative min-h-[92vh] w-full overflow-hidden bg-[color:var(--cream)] pt-28 md:pt-32">
      <div className="mx-auto grid w-full max-w-[1280px] grid-cols-1 gap-10 px-6 pb-24 md:grid-cols-12 md:gap-12 md:px-10 md:pb-32 lg:px-14 lg:pt-16">
        {/* LEFT — text column (5 cols) */}
        <div className="relative z-10 md:col-span-5 md:pt-4">
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1], delay: 0.15 }}
            className="eyebrow"
          >
            {hero.eyebrow}
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1], delay: 0.25 }}
            className="display mt-5 text-[clamp(2.6rem,5.6vw,4.8rem)] text-ink"
          >
            {hero.headline.lead}{" "}
            <span className="serif-italic text-[color:var(--lapis-glow)]">
              {hero.headline.italic}
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.45 }}
            className="mt-6 max-w-md text-[1.05rem] leading-[1.55] text-muted md:text-[1.1rem]"
          >
            {hero.subline}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.6 }}
            className="mt-8 flex flex-wrap items-center gap-3"
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

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 0.9 }}
            className="mt-10 flex items-center gap-3 text-[0.82rem] text-muted"
          >
            <span className="relative flex h-2 w-2">
              <span className="absolute inset-0 animate-ping rounded-full bg-[color:var(--signal)] opacity-70" />
              <span className="relative h-2 w-2 rounded-full bg-[color:var(--signal)]" />
            </span>
            <span>Currently building. Open for select engagements.</span>
          </motion.div>
        </div>

        {/* RIGHT — media column (7 cols) */}
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.1, ease: [0.22, 1, 0.36, 1], delay: 0.2 }}
          className="relative md:col-span-7"
        >
          <MediaSlot
            assetId={hero.mediaId}
            aspect="aspect-[4/5] md:aspect-[5/6]"
            rounded="rounded-[32px]"
            showStars
            overlay={<HeroOverlay />}
            className="shadow-[0_30px_80px_rgba(14,14,16,0.18)]"
          />
          <SpecBadge />
        </motion.div>
      </div>
    </section>
  );
}

function HeroOverlay() {
  return (
    <div className="absolute inset-0 flex items-end justify-between p-6 md:p-8">
      <div className="flex items-center gap-2 rounded-full bg-black/30 px-3 py-1.5 text-[0.68rem] uppercase tracking-[0.18em] text-white/90 backdrop-blur-md">
        <span className="h-1.5 w-1.5 rounded-full bg-[color:var(--signal)]" />
        Live · ZAICORE signal
      </div>
      <div className="hidden items-center gap-2 rounded-full bg-black/30 px-3 py-1.5 text-[0.68rem] uppercase tracking-[0.18em] text-white/90 backdrop-blur-md md:flex">
        <span>4K · 16:9</span>
      </div>
    </div>
  );
}

function SpecBadge() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1, delay: 1.1, ease: [0.22, 1, 0.36, 1] }}
      className="absolute -bottom-6 left-6 hidden max-w-[280px] rounded-2xl border border-hairline bg-[color:var(--paper)]/95 p-4 shadow-[0_20px_60px_rgba(14,14,16,0.08)] backdrop-blur md:block"
    >
      <p className="eyebrow mb-1">Recent</p>
      <p className="text-sm leading-snug text-ink">
        Shipped a real-time voice agent running on Claude Sonnet 4.6 with 110ms first-token latency.
      </p>
    </motion.div>
  );
}
