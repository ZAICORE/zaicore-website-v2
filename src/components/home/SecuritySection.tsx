import { Check } from "lucide-react";
import { security } from "@/content/security";
import { Section } from "@/components/ui/Section";
import { Reveal } from "@/components/motion/Reveal";
import { MediaSlot } from "@/components/media/MediaSlot";
import { Button } from "@/components/ui/Button";

export function SecuritySection() {
  return (
    <Section id="security" tone="ink" className="py-28 md:py-36">
      <div className="grid grid-cols-1 items-center gap-12 md:grid-cols-12 md:gap-14">
        <div className="md:col-span-6">
          <Reveal>
            <p className="eyebrow text-[color:var(--muted-soft)]">{security.eyebrow}</p>
            <h2 className="display mt-5 text-[clamp(2rem,4.4vw,3.6rem)] text-cream">
              {security.headline.lead}{" "}
              <span className="serif-italic text-[color:var(--signal)]">
                {security.headline.italic}
              </span>
            </h2>
            <p className="mt-6 max-w-lg text-[1.05rem] leading-[1.6] text-[color:var(--cream-soft)]/80">
              {security.summary}
            </p>
            <ul className="mt-8 space-y-3">
              {security.bullets.map((b) => (
                <li key={b} className="flex items-start gap-3 text-[0.95rem] text-cream/90">
                  <span className="mt-1 inline-flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-[color:var(--signal)]/20 text-[color:var(--signal)]">
                    <Check className="h-3 w-3" strokeWidth={2.5} />
                  </span>
                  <span>{b}</span>
                </li>
              ))}
            </ul>
            <div className="mt-10">
              <Button
                href={security.cta.href}
                label={security.cta.label}
                variant="accent"
                external={security.cta.external}
              />
            </div>
          </Reveal>
        </div>

        <div className="md:col-span-6">
          <Reveal delay={0.15}>
            <div className="relative">
              <MediaSlot
                assetId={security.mediaId}
                aspect="aspect-[4/5]"
                rounded="rounded-[28px]"
                showStars
                className="shadow-[0_30px_80px_rgba(0,0,0,0.4)]"
                overlay={<SecurityOverlay />}
              />
              <div
                aria-hidden
                className="absolute -inset-6 -z-10 rounded-[36px] bg-[color:var(--signal)] opacity-[0.05] blur-3xl"
              />
            </div>
          </Reveal>
        </div>
      </div>
    </Section>
  );
}

function SecurityOverlay() {
  return (
    <div className="absolute inset-0 flex items-end p-6 md:p-8">
      <div className="w-full rounded-2xl bg-black/40 p-4 backdrop-blur-md">
        <div className="mb-2 flex items-center justify-between text-[0.65rem] uppercase tracking-[0.18em] text-white/60">
          <span>Sunday briefing · preview</span>
          <span className="inline-flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-[color:var(--signal)]" />
            Protected
          </span>
        </div>
        <p className="font-serif text-lg italic leading-snug text-white">
          Four actions this week. Two broker takedowns confirmed. None urgent.
        </p>
      </div>
    </div>
  );
}
