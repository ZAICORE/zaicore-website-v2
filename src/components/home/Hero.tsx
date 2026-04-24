"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { hero } from "@/content/hero";
import { MediaSlot } from "@/components/media/MediaSlot";

export function Hero() {
  return (
    <section className="relative w-full overflow-hidden bg-[color:var(--cream)] pt-20 md:pt-24">
      <div className="relative mx-auto w-full max-w-[1680px] px-4 md:px-8">
        <div className="relative">
          <MediaSlot
            assetId="heroMedia"
            aspect="aspect-[16/9]"
            rounded="rounded-none"
            showGrain={false}
            transparentContainer
            fit="contain"
            className="w-full bg-transparent"
          />

          {/* Tagline — anchored near the top of the scene */}
          <div className="pointer-events-none absolute left-1/2 top-[22%] flex w-[min(38%,520px)] -translate-x-1/2 justify-center hero-tagline-wrap">
            <motion.p
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, ease: [0.22, 1, 0.36, 1], delay: 0.4 }}
              className="serif-italic text-center text-[clamp(1rem,3.2vw,3rem)] font-medium leading-[1.08] text-ink"
              style={{ letterSpacing: "-0.02em" }}
            >
              AI engineering and{" "}
              <span className="text-[color:var(--lapis-glow)]">cyber security.</span>
            </motion.p>
          </div>

          {/* CTAs — overlaid on the video, vertical stack, glass cards */}
          <div className="pointer-events-none absolute inset-x-0 top-[52%] flex justify-center hero-ctas-wrap">
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, ease: [0.22, 1, 0.36, 1], delay: 0.65 }}
              className="pointer-events-auto grid w-[min(34%,360px)] grid-cols-1 gap-3 hero-cta-grid"
            >
              {hero.ctas.map((cta) => {
                const Arrow = cta.external ? ArrowUpRight : ArrowRight;
                const kind = cta.external ? "Product" : "Discipline";
                const body = (
                  <>
                    <span className="flex flex-col items-center text-center">
                      <span className="text-[0.6rem] font-medium uppercase tracking-[0.18em] text-muted transition-colors duration-300 group-hover:text-muted">
                        {kind}
                      </span>
                      <span className="mt-[0.2rem] text-[1.05rem] font-medium leading-[1.1] tracking-[-0.02em] text-ink transition-colors duration-300">
                        {cta.label}
                      </span>
                      <span className="mt-[0.15rem] text-[0.78rem] leading-[1.35] text-muted transition-colors duration-300">
                        {cta.sublabel}
                      </span>
                    </span>
                    <span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full border border-hairline-strong text-ink transition-all duration-300">
                      <Arrow className="h-3.5 w-3.5" strokeWidth={1.75} />
                    </span>
                  </>
                );
                const classes =
                  "group relative flex w-full items-center justify-center gap-4 rounded-2xl border border-hairline-strong bg-[rgba(250,248,247,0.82)] px-4 py-3.5 backdrop-blur-[10px] transition-all duration-300 ease-out hover:-translate-y-0.5 hover:border-ink hover:shadow-[0_14px_28px_rgba(14,14,16,0.10)]";
                return cta.external ? (
                  <a
                    key={cta.label}
                    href={cta.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={classes}
                  >
                    {body}
                  </a>
                ) : (
                  <Link key={cta.label} href={cta.href} className={classes}>
                    {body}
                  </Link>
                );
              })}
            </motion.div>
          </div>
        </div>
      </div>

      {/* Mobile fallback: CTAs flow below the video (overlay collapses via CSS) */}
      <style>{`
        @media (max-width: 900px) {
          .hero-ctas-wrap {
            position: static !important;
            inset: auto !important;
            margin: 2rem auto 4rem !important;
            padding: 0 1.5rem !important;
          }
          .hero-ctas-wrap .hero-cta-grid {
            width: 100% !important;
            max-width: 640px !important;
            gap: 1rem !important;
          }
        }
      `}</style>
    </section>
  );
}
