import { engineering } from "@/content/engineering";
import { Section } from "@/components/ui/Section";
import { Reveal } from "@/components/motion/Reveal";
import { Stagger, StaggerItem } from "@/components/motion/Stagger";

export function EngineeringSection() {
  return (
    <Section id="engineering" tone="cream" className="py-28 md:py-36">
      <div className="grid grid-cols-1 gap-12 md:grid-cols-12 md:gap-10">
        <div className="md:col-span-5">
          <Reveal>
            <p className="eyebrow">{engineering.eyebrow}</p>
            <h2 className="display mt-5 text-[clamp(2rem,4.2vw,3.4rem)] text-ink">
              {engineering.headline.lead}{" "}
              <span className="serif-italic text-[color:var(--lapis-glow)]">
                {engineering.headline.italic}
              </span>
            </h2>
            <p className="mt-6 max-w-md text-[1rem] leading-[1.6] text-muted md:text-[1.05rem]">
              {engineering.intro}
            </p>
          </Reveal>
        </div>

        <div className="md:col-span-7">
          <Stagger
            className="grid grid-cols-1 gap-4 sm:grid-cols-2"
            stagger={0.06}
          >
            {engineering.verticals.map((v) => {
              const Icon = v.icon;
              return (
                <StaggerItem key={v.id}>
                  <article className="group relative h-full overflow-hidden rounded-2xl border border-hairline bg-[color:var(--paper)] p-6 transition-all duration-500 ease-out hover:-translate-y-0.5 hover:border-hairline-strong hover:shadow-[0_20px_60px_rgba(14,14,16,0.08)]">
                    <div className="mb-5 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-[color:var(--lapis-mist)] text-[color:var(--lapis-glow)]">
                      <Icon className="h-5 w-5" strokeWidth={1.5} />
                    </div>
                    <h3 className="text-[1.05rem] font-medium tracking-[-0.01em] text-ink">
                      {v.title}
                    </h3>
                    <p className="mt-1 text-[0.88rem] text-muted">{v.summary}</p>
                    <p className="mt-4 text-[0.9rem] leading-[1.55] text-ink-soft">
                      {v.description}
                    </p>
                    <div
                      aria-hidden
                      className="absolute -right-16 -top-16 h-40 w-40 rounded-full bg-[color:var(--lapis-mist)] opacity-0 blur-3xl transition-opacity duration-700 group-hover:opacity-100"
                    />
                  </article>
                </StaggerItem>
              );
            })}
          </Stagger>
        </div>
      </div>
    </Section>
  );
}
