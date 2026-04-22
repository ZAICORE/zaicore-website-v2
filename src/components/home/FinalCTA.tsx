import { Section } from "@/components/ui/Section";
import { Button } from "@/components/ui/Button";
import { Reveal } from "@/components/motion/Reveal";
import { nav } from "@/content/site";

export function FinalCTA() {
  return (
    <Section id="contact" tone="cream" className="py-28 md:py-36">
      <Reveal className="mx-auto max-w-3xl text-center">
        <p className="eyebrow">Start a conversation</p>
        <h2 className="display mt-5 text-[clamp(2.2rem,5vw,4rem)] text-ink">
          Build something{" "}
          <span className="serif-italic text-[color:var(--lapis-glow)]">worth trusting.</span>
        </h2>
        <p className="mx-auto mt-6 max-w-xl text-[1.05rem] leading-[1.6] text-muted">
          Tell us the problem. We&apos;ll tell you whether we&apos;re the right team to solve it, and how fast.
        </p>
        <div className="mt-10 flex items-center justify-center gap-3">
          <Button href={nav.cta.href} label={nav.cta.label} variant="primary" />
          <Button
            href="https://security.zaicore.com"
            label="Or try ZAICORE Security"
            variant="ghost"
            external
          />
        </div>
      </Reveal>
    </Section>
  );
}
