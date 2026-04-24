import type { Metadata } from "next";
import { Nav } from "@/components/layout/Nav";
import { Footer } from "@/components/layout/Footer";
import { Reveal } from "@/components/motion/Reveal";
import { Button } from "@/components/ui/Button";
import { EngineeringHero } from "@/components/engineering/EngineeringHero";
import { disciplines } from "@/content/disciplines";

export const metadata: Metadata = {
  title: "Engineering",
  description:
    "Thirteen disciplines, one team, one bar. Agentic systems, context engineering, platform, security, compliance — shipped.",
};

export default function EngineeringPage() {
  return (
    <>
      <Nav />
      <main className="relative w-full bg-[color:var(--cream)]">
        <EngineeringHero
          eyebrow={disciplines.eyebrow}
          headline={disciplines.headline}
          intro={disciplines.intro}
        />

        {/* Disciplines grid */}
        <section className="relative w-full border-t border-hairline bg-[color:var(--cream-soft)] py-20 md:py-28">
          <div className="mx-auto w-full max-w-[1280px] px-6 md:px-10 lg:px-14">
            <Reveal className="max-w-2xl">
              <p className="eyebrow">Coverage</p>
              <h2 className="display mt-4 text-[clamp(1.6rem,2.6vw,2.2rem)] leading-[1.1] text-ink">
                The disciplines we actually{" "}
                <span className="serif-italic text-[color:var(--lapis-glow)]">ship against.</span>
              </h2>
              <p className="mt-5 text-[0.95rem] leading-[1.6] text-muted">
                Not a menu. A commitment: these are the surfaces we&apos;ll go deep on when you hand us a problem.
              </p>
            </Reveal>

            <div className="mt-14 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {disciplines.items.map((d, i) => {
                const Icon = d.icon;
                return (
                  <Reveal key={d.id} delay={Math.min(i * 0.04, 0.25)}>
                    <div className="group h-full rounded-[20px] border border-hairline bg-[color:var(--paper)] p-6 transition-all duration-300 hover:-translate-y-0.5 hover:border-hairline-strong hover:shadow-[0_14px_34px_rgba(14,14,16,0.06)]">
                      <span className="inline-flex h-9 w-9 items-center justify-center rounded-lg bg-[color:var(--lapis-mist)] text-[color:var(--lapis-glow)]">
                        <Icon className="h-4 w-4" strokeWidth={1.5} />
                      </span>
                      <h3 className="mt-5 text-[1rem] font-medium tracking-[-0.01em] text-ink">
                        {d.title}
                      </h3>
                      <p className="mt-2 text-[0.88rem] leading-[1.55] text-muted">{d.summary}</p>
                    </div>
                  </Reveal>
                );
              })}
            </div>
          </div>
        </section>

        {/* Closing CTA */}
        <section className="w-full py-28 md:py-36">
          <Reveal className="mx-auto max-w-3xl px-6 text-center">
            <p className="eyebrow">Start a conversation</p>
            <h2 className="display mt-5 text-[clamp(2rem,4.4vw,3.4rem)] text-ink">
              Tell us the problem.{" "}
              <span className="serif-italic text-[color:var(--lapis-glow)]">
                We&apos;ll tell you how fast.
              </span>
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-[1rem] leading-[1.6] text-muted">
              Short form. 24-hour reply. No decks.
            </p>
            <div className="mt-10 flex items-center justify-center gap-3">
              <Button href="/book" label="Book a call" variant="primary" />
              <Button
                href="https://security.zaicore.com"
                label="Try ZAICORE Security"
                variant="ghost"
                external
              />
            </div>
          </Reveal>
        </section>
      </main>
      <Footer />
    </>
  );
}
