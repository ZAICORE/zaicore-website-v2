import { Check } from "lucide-react";
import { security } from "@/content/security";
import { Section } from "@/components/ui/Section";
import { Reveal } from "@/components/motion/Reveal";
import { MediaSlot } from "@/components/media/MediaSlot";
import { Button } from "@/components/ui/Button";

export function SecuritySection() {
  return (
    <Section id="security" tone="ink" className="py-28 md:py-40 lg:py-48">
      {/* HEADER */}
      <div className="mx-auto max-w-5xl text-center">
        <Reveal>
          <p className="eyebrow text-[color:var(--muted-soft)]">{security.eyebrow}</p>
          <h2 className="display mt-6 text-[clamp(2.4rem,5.6vw,4.6rem)] text-cream">
            {security.headline.lead}{" "}
            <span className="serif-italic text-[color:var(--signal)]">
              {security.headline.italic}
            </span>
          </h2>
          <p className="mx-auto mt-7 max-w-3xl text-[1.05rem] leading-[1.65] text-[color:var(--cream-soft)]/75 md:text-[1.15rem]">
            {security.summary}
          </p>
        </Reveal>
      </div>

      {/* PRODUCT PREVIEW + BULLETS */}
      <div className="mt-16 grid grid-cols-1 items-center gap-12 md:mt-24 md:grid-cols-12 md:gap-16">
        <div className="md:col-span-7">
          <Reveal>
            <div className="relative">
              <MediaSlot
                assetId={security.mediaId}
                aspect="aspect-[16/10]"
                rounded="rounded-[28px]"
                showStars
                className="shadow-[0_50px_140px_-30px_rgba(0,0,0,0.6)] ring-1 ring-white/10"
                overlay={<BriefingOverlay />}
              />
              <div
                aria-hidden
                className="absolute -inset-10 -z-10 rounded-[40px] bg-[color:var(--signal)] opacity-[0.06] blur-3xl"
              />
            </div>
          </Reveal>
        </div>

        <div className="md:col-span-5">
          <Reveal delay={0.15}>
            <ul className="space-y-4">
              {security.bullets.map((b) => (
                <li key={b} className="flex items-start gap-3 text-[0.98rem] leading-[1.5] text-cream/90">
                  <span className="mt-[3px] inline-flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-[color:var(--signal)]/20 text-[color:var(--signal)]">
                    <Check className="h-3 w-3" strokeWidth={2.5} />
                  </span>
                  <span>{b}</span>
                </li>
              ))}
            </ul>
            <div className="mt-10 flex flex-wrap items-center gap-3">
              <Button
                href={security.cta.href}
                label={security.cta.label}
                variant="accent"
                external={security.cta.external}
              />
              <a
                href={security.secondaryCta.href}
                className="text-[0.9rem] text-cream/60 underline-offset-4 transition-colors hover:text-cream hover:underline"
              >
                {security.secondaryCta.label} →
              </a>
            </div>
          </Reveal>
        </div>
      </div>

      {/* PAGE-END CLOSER — folds the old FinalCTA into Security */}
      <Reveal delay={0.2} className="mx-auto mt-28 max-w-3xl text-center md:mt-40">
        <p className="eyebrow text-[color:var(--muted-soft)]">Start a conversation</p>
        <h3 className="display mt-5 text-[clamp(1.8rem,3.8vw,3rem)] text-cream">
          Build something{" "}
          <span className="serif-italic text-[color:var(--signal)]">worth trusting.</span>
        </h3>
        <p className="mx-auto mt-5 max-w-xl text-[1rem] leading-[1.6] text-cream/60">
          Tell us the problem. We&apos;ll tell you whether we&apos;re the right team to solve it, and how fast.
        </p>
        <div className="mt-8 flex items-center justify-center gap-3">
          <Button href="#contact" label="Book a call" variant="primary" className="bg-cream text-ink hover:bg-cream/90" />
        </div>
      </Reveal>
    </Section>
  );
}

function BriefingOverlay() {
  return (
    <div className="absolute inset-0 flex items-end p-6 md:p-10">
      <div className="w-full max-w-md rounded-2xl bg-black/45 p-5 backdrop-blur-md">
        <div className="mb-2 flex items-center justify-between text-[0.62rem] uppercase tracking-[0.2em] text-white/60">
          <span>Sunday briefing · preview</span>
          <span className="inline-flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-[color:var(--signal)]" />
            Protected
          </span>
        </div>
        <p className="font-serif text-[1.15rem] italic leading-[1.35] text-white">
          Four actions this week. Two broker takedowns confirmed. None urgent.
        </p>
      </div>
    </div>
  );
}
