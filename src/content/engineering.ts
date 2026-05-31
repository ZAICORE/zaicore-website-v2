import type { LucideIcon } from "lucide-react";
import { Bot, Layers, ShieldCheck } from "lucide-react";

export type Vertical = {
  id: string;
  title: string;
  summary: string;
  icon: LucideIcon;
};

export const engineering = {
  eyebrow: "Engineering",
  headline: {
    lead: "AI and software,",
    italic: "built to ship.",
  },
  intro:
    "We build AI and software that becomes your competitive edge. It fits how your business already works, ships to production, and you own it.",
  verticals: [
    {
      id: "ai",
      title: "AI that does the busywork",
      summary:
        "Plugs into the tools you already run, kills the repetitive work, and handles the workflows your team does by hand today.",
      icon: Bot,
    },
    {
      id: "software",
      title: "The hard software underneath",
      summary:
        "Full-stack product, cloud, data, the infrastructure your business runs on. Typed end to end, built to outlast whoever wrote it. You own the IP.",
      icon: Layers,
    },
    {
      id: "reliability",
      title: "Built to bet the business on",
      summary:
        "The eval layer, monitoring, and security that keep AI and software reliable in production, where most of it quietly dies. The part nobody else bothers to build.",
      icon: ShieldCheck,
    },
  ] satisfies Vertical[],
  cta: { label: "Explore engineering", href: "/engineering" },
  mediaId: "engineeringShowreel",
};
