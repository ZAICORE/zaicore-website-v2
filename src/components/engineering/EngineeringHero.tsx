"use client";

import { motion } from "motion/react";
import { Button } from "@/components/ui/Button";

type Props = {
  eyebrow: string;
  headline: { lead: string; italic: string };
  intro: string;
};

export function EngineeringHero({ eyebrow, headline, intro }: Props) {
  return (
    <section className="relative w-full overflow-hidden pt-20 md:pt-24">
      {/* Desktop: full-width video with copy overlaid LEFT (fox sits bottom-right of video) */}
      <div className="relative mx-auto hidden w-full max-w-[1680px] md:block">
        <div className="relative">
          <video
            src="/mascots/engineering_page_scene.mp4"
            poster="/mascots/engineering_page_start.png"
            autoPlay
            muted
            loop
            playsInline
            preload="auto"
            className="aspect-[16/9] w-full bg-transparent object-contain"
          />

          <div className="pointer-events-none absolute inset-y-0 left-0 flex w-[52%] items-center pl-[3%] lg:w-[48%] lg:pl-[4%]">
            <div className="w-full max-w-[640px]">
              <motion.p
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
                className="eyebrow"
              >
                {eyebrow}
              </motion.p>
              <motion.h1
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.1 }}
                className="display mt-4 text-[clamp(1.8rem,3.4vw,3.4rem)] leading-[1.02] text-ink"
              >
                {headline.lead}{" "}
                <span className="serif-italic text-[color:var(--lapis-glow)]">
                  {headline.italic}
                </span>
              </motion.h1>
              <motion.p
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.2 }}
                className="mt-5 max-w-lg text-[clamp(0.92rem,1.05vw,1.05rem)] leading-[1.55] text-muted"
              >
                {intro}
              </motion.p>
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
                className="pointer-events-auto mt-7 flex flex-wrap items-center gap-3"
              >
                <Button href="/book" label="Book a call" variant="primary" />
                <Button
                  href="https://security.zaicore.com"
                  label="See ZAICORE Security"
                  variant="ghost"
                  external
                />
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile: video on top, copy stacked below */}
      <div className="md:hidden">
        <video
          src="/mascots/engineering_page_scene.mp4"
          poster="/mascots/engineering_page_start.png"
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
          className="aspect-[16/9] w-full bg-transparent object-contain"
        />
        <div className="mx-auto max-w-3xl px-6 py-12 text-center">
          <p className="eyebrow">{eyebrow}</p>
          <h1 className="display mt-4 text-[clamp(2rem,6vw,2.6rem)] leading-[1.05] text-ink">
            {headline.lead}{" "}
            <span className="serif-italic text-[color:var(--lapis-glow)]">
              {headline.italic}
            </span>
          </h1>
          <p className="mt-5 text-[1rem] leading-[1.55] text-muted">{intro}</p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Button href="/book" label="Book a call" variant="primary" />
            <Button
              href="https://security.zaicore.com"
              label="See ZAICORE Security"
              variant="ghost"
              external
            />
          </div>
        </div>
      </div>
    </section>
  );
}
