import type { LucideIcon } from "lucide-react";
import { Bot, Atom, LineChart } from "lucide-react";

export type Vertical = {
  id: string;
  title: string;
  summary: string;
  icon: LucideIcon;
};

export const engineering = {
  eyebrow: "Engineering",
  headline: {
    lead: "AI-first engineering,",
    italic: "shipped to production.",
  },
  intro:
    "The software off-the-shelf can't build. We ship AI that takes action, fits how your business actually works, and keeps working in production.",
  verticals: [
    {
      id: "agentic",
      title: "AI that actually does the work",
      summary:
        "Agents wired into your real tools. They book, process, escalate, close the loop. Not chatbots that suggest. Software that finishes.",
      icon: Bot,
    },
    {
      id: "models",
      title: "Models built for your business",
      summary:
        "Off-the-shelf AI was trained on everything except your domain. We build systems on your data, your language, your edge cases, so the AI sounds like you and knows what matters.",
      icon: Atom,
    },
    {
      id: "evals",
      title: "AI you can bet the business on",
      summary:
        "The reason most AI dies in production: nobody built the layer that catches it when it drifts. We do. Testing, monitoring, the ground truth your team can stand behind.",
      icon: LineChart,
    },
  ] satisfies Vertical[],
  cta: { label: "Explore engineering", href: "/engineering" },
  mediaId: "engineeringShowreel",
};
