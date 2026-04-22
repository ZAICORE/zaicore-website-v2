import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/cn";

type Variant = "primary" | "accent" | "ghost";

type ButtonProps = {
  href: string;
  label: string;
  variant?: Variant;
  external?: boolean;
  className?: string;
};

const base =
  "group relative inline-flex items-center gap-2 rounded-full px-5 py-3 text-[0.95rem] font-medium transition-all duration-300 ease-out will-change-transform";

const variants: Record<Variant, string> = {
  primary:
    "bg-ink text-cream hover:bg-ink-soft hover:-translate-y-0.5 hover:shadow-[0_10px_30px_rgba(14,14,16,0.2)]",
  accent:
    "bg-[color:var(--signal-soft)] text-ink ring-1 ring-inset ring-[color:var(--signal)]/40 hover:ring-[color:var(--signal)]/80 hover:-translate-y-0.5",
  ghost:
    "text-ink ring-1 ring-inset ring-hairline-strong hover:ring-ink hover:-translate-y-0.5",
};

export function Button({ href, label, variant = "primary", external, className }: ButtonProps) {
  const content = (
    <>
      <span>{label}</span>
      {external && (
        <ArrowUpRight className="h-4 w-4 opacity-70 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
      )}
    </>
  );
  const classes = cn(base, variants[variant], className);
  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={classes}>
        {content}
      </a>
    );
  }
  return (
    <Link href={href} className={classes}>
      {content}
    </Link>
  );
}
