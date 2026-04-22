import { cn } from "@/lib/cn";

type SectionProps = {
  id?: string;
  className?: string;
  children: React.ReactNode;
  tone?: "cream" | "paper" | "ink";
};

const tones = {
  cream: "bg-[color:var(--cream)] text-ink",
  paper: "bg-[color:var(--paper)] text-ink",
  ink: "bg-[color:var(--ink)] text-cream",
};

export function Section({ id, className, children, tone = "cream" }: SectionProps) {
  return (
    <section id={id} className={cn("relative w-full overflow-hidden", tones[tone], className)}>
      <div className="mx-auto w-full max-w-[1280px] px-6 md:px-10 lg:px-14">{children}</div>
    </section>
  );
}
