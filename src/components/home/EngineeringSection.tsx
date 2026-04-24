"use client";

import { motion } from "motion/react";
import { engineering } from "@/content/engineering";
import { Reveal } from "@/components/motion/Reveal";
import { MediaSlot } from "@/components/media/MediaSlot";
import { Button } from "@/components/ui/Button";

export function EngineeringSection() {
  return (
    <section
      id="engineering"
      className="relative w-full overflow-hidden border-t border-hairline bg-[color:var(--cream)]"
    >
      {/* Desktop: video on the left, text column on the right */}
      <div className="relative mx-auto hidden w-full max-w-[1680px] md:block">
        <div className="relative">
          <MediaSlot
            assetId="engineeringShowreel"
            aspect="aspect-[16/9]"
            rounded="rounded-none"
            showGrain={false}
            transparentContainer
            fit="contain"
            className="w-full bg-transparent"
          />

          {/* Text column anchored to the right half of the video */}
          <div className="pointer-events-none absolute inset-y-0 right-0 flex w-[48%] items-center pr-[3%] lg:w-[44%] lg:pr-[4%]">
            <div className="w-full max-w-[560px]">
              <motion.p
                initial={{ opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-120px" }}
                transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
                className="eyebrow"
              >
                {engineering.eyebrow}
              </motion.p>
              <motion.h2
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-120px" }}
                transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.1 }}
                className="display mt-3 text-[clamp(1.5rem,2.4vw,2.4rem)] leading-[1.05] tracking-[-0.03em] text-ink"
              >
                {engineering.headline.lead}{" "}
                <span className="serif-italic text-[color:var(--lapis-glow)]">
                  {engineering.headline.italic}
                </span>
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-120px" }}
                transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.2 }}
                className="mt-3 max-w-md text-[clamp(0.85rem,1vw,0.95rem)] leading-[1.5] text-muted"
              >
                {engineering.intro}
              </motion.p>

              <motion.ul
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-120px" }}
                transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
                className="mt-5 space-y-3"
              >
                {engineering.verticals.map((v) => {
                  const Icon = v.icon;
                  return (
                    <li key={v.id} className="flex items-start gap-3">
                      <span className="mt-[2px] inline-flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-[color:var(--lapis-mist)] text-[color:var(--lapis-glow)]">
                        <Icon className="h-3.5 w-3.5" strokeWidth={1.5} />
                      </span>
                      <div>
                        <p className="text-[clamp(0.82rem,0.95vw,0.92rem)] font-medium tracking-[-0.01em] text-ink">
                          {v.title}
                        </p>
                        <p className="text-[clamp(0.76rem,0.88vw,0.86rem)] leading-[1.45] text-muted">
                          {v.summary}
                        </p>
                      </div>
                    </li>
                  );
                })}
              </motion.ul>

              <motion.div
                initial={{ opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-120px" }}
                transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1], delay: 0.4 }}
                className="pointer-events-auto mt-6"
              >
                <Button
                  href={engineering.cta.href}
                  label={engineering.cta.label}
                  variant="primary"
                />
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile: stacked */}
      <div className="md:hidden">
        <MediaSlot
          assetId="engineeringShowreel"
          aspect="aspect-[16/9]"
          rounded="rounded-none"
          showGrain={false}
          transparentContainer
          fit="contain"
          className="w-full bg-transparent"
        />
        <div className="mx-auto max-w-3xl px-6 py-12 text-center">
          <Reveal>
            <p className="eyebrow">{engineering.eyebrow}</p>
            <h2 className="display mt-4 text-[clamp(1.9rem,6vw,2.4rem)] text-ink">
              {engineering.headline.lead}{" "}
              <span className="serif-italic text-[color:var(--lapis-glow)]">
                {engineering.headline.italic}
              </span>
            </h2>
            <p className="mt-5 text-[1rem] leading-[1.55] text-muted">{engineering.intro}</p>
          </Reveal>
          <Reveal delay={0.1} className="mt-8 space-y-5 text-left">
            {engineering.verticals.map((v) => {
              const Icon = v.icon;
              return (
                <div key={v.id} className="flex items-start gap-3">
                  <span className="mt-[2px] inline-flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-[color:var(--lapis-mist)] text-[color:var(--lapis-glow)]">
                    <Icon className="h-4 w-4" strokeWidth={1.5} />
                  </span>
                  <div>
                    <p className="text-[0.95rem] font-medium text-ink">{v.title}</p>
                    <p className="text-[0.88rem] leading-[1.5] text-muted">{v.summary}</p>
                  </div>
                </div>
              );
            })}
          </Reveal>
          <Reveal delay={0.2} className="mt-8">
            <Button href={engineering.cta.href} label={engineering.cta.label} variant="primary" />
          </Reveal>
        </div>
      </div>
    </section>
  );
}
