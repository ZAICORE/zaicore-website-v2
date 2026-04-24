import type { ReactNode } from "react";
import { Nav } from "@/components/layout/Nav";
import { Footer } from "@/components/layout/Footer";
import { Reveal } from "@/components/motion/Reveal";

type LegalPageProps = {
  eyebrow: string;
  title: ReactNode;
  updated: string;
  children: ReactNode;
};

export function LegalPage({ eyebrow, title, updated, children }: LegalPageProps) {
  return (
    <>
      <Nav />
      <main className="relative w-full bg-[color:var(--cream)] pt-28 md:pt-36">
        <section className="mx-auto w-full max-w-[780px] px-6 pb-32 md:px-10">
          <Reveal>
            <p className="eyebrow">{eyebrow}</p>
            <h1 className="display mt-5 text-[clamp(2.2rem,4.8vw,3.4rem)] leading-[1.02] text-ink">
              {title}
            </h1>
            <p className="mt-4 text-[0.85rem] text-muted">Last updated: {updated}</p>
          </Reveal>
          <Reveal delay={0.08} className="mt-14 space-y-10 text-[1rem] leading-[1.7] text-ink-soft">
            {children}
          </Reveal>
        </section>
      </main>
      <Footer />
    </>
  );
}

type SectionProps = { heading: string; children: ReactNode };
export function LegalSection({ heading, children }: SectionProps) {
  return (
    <section className="scroll-mt-32">
      <h2 className="text-[1.15rem] font-medium tracking-[-0.01em] text-ink">{heading}</h2>
      <div className="mt-3 space-y-4 text-muted">{children}</div>
    </section>
  );
}
