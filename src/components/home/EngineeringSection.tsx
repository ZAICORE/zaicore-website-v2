import { engineering } from "@/content/engineering";
import { Section } from "@/components/ui/Section";
import { Reveal } from "@/components/motion/Reveal";
import { Stagger, StaggerItem } from "@/components/motion/Stagger";
import { MediaSlot } from "@/components/media/MediaSlot";

export function EngineeringSection() {
  return (
    <Section id="engineering" tone="cream" className="border-t border-hairline py-24 md:py-36 lg:py-44">
      {/* HEADER */}
      <div className="mx-auto max-w-4xl text-center">
        <Reveal>
          <p className="eyebrow">{engineering.eyebrow}</p>
          <h2 className="display mt-6 text-[clamp(2.2rem,5vw,4rem)] text-ink">
            {engineering.headline.lead}{" "}
            <span className="serif-italic text-[color:var(--lapis-glow)]">
              {engineering.headline.italic}
            </span>
          </h2>
          <p className="mx-auto mt-7 max-w-2xl text-[1.05rem] leading-[1.6] text-muted md:text-[1.12rem]">
            {engineering.intro}
          </p>
        </Reveal>
      </div>

      {/* SHOWREEL — Seedance slot for an engineering clip */}
      <Reveal delay={0.1} className="mx-auto mt-16 w-full max-w-[1100px] md:mt-20">
        <MediaSlot
          assetId={engineering.mediaId}
          aspect="aspect-[16/9]"
          rounded="rounded-[28px]"
          showStars
          className="shadow-[0_40px_120px_-20px_rgba(14,14,16,0.25)] ring-1 ring-inset ring-hairline"
          overlay={
            <div className="absolute inset-0 flex items-end p-6 md:p-10">
              <div className="flex items-center gap-2 rounded-full bg-black/30 px-3 py-1.5 text-[0.68rem] uppercase tracking-[0.18em] text-white/90 backdrop-blur-md">
                <span className="h-1.5 w-1.5 rounded-full bg-[color:var(--signal)]" />
                Showreel · engineering
              </div>
            </div>
          }
        />
      </Reveal>

      {/* VERTICALS GRID */}
      <Stagger className="mt-16 grid grid-cols-1 gap-5 md:mt-24 md:grid-cols-2 md:gap-6 lg:grid-cols-3" stagger={0.06}>
        {engineering.verticals.map((v) => {
          const Icon = v.icon;
          return (
            <StaggerItem key={v.id}>
              <article className="group relative h-full overflow-hidden rounded-[20px] border border-hairline bg-[color:var(--paper)] p-7 transition-all duration-500 ease-out hover:-translate-y-1 hover:border-hairline-strong hover:shadow-[0_30px_80px_-20px_rgba(14,14,16,0.15)]">
                <div className="mb-6 inline-flex h-11 w-11 items-center justify-center rounded-xl bg-[color:var(--lapis-mist)] text-[color:var(--lapis-glow)]">
                  <Icon className="h-5 w-5" strokeWidth={1.5} />
                </div>
                <h3 className="text-[1.15rem] font-medium tracking-[-0.015em] text-ink">
                  {v.title}
                </h3>
                <p className="mt-1.5 text-[0.9rem] text-muted">{v.summary}</p>
                <p className="mt-5 text-[0.93rem] leading-[1.6] text-ink-soft">
                  {v.description}
                </p>
                <div
                  aria-hidden
                  className="absolute -right-20 -top-20 h-52 w-52 rounded-full bg-[color:var(--lapis-mist)] opacity-0 blur-3xl transition-opacity duration-700 group-hover:opacity-100"
                />
              </article>
            </StaggerItem>
          );
        })}
      </Stagger>
    </Section>
  );
}
