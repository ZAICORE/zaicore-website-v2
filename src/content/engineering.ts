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
    "The software off-the-shelf can't build. Agents, custom models, and the infrastructure that makes AI actually work in production.",
  verticals: [
    {
      id: "agentic",
      title: "Agentic systems",
      summary: "Tool-using, multi-step, MCP-native. Agents that finish the task — not chatbots.",
      icon: Bot,
    },
    {
      id: "models",
      title: "Custom models",
      summary: "Post-training, fine-tunes, distillation. A model shaped to your domain.",
      icon: Atom,
    },
    {
      id: "evals",
      title: "Evals & observability",
      summary: "Traces, ground truth, regression catches. The layer that makes AI shippable.",
      icon: LineChart,
    },
  ] satisfies Vertical[],
  cta: { label: "Explore engineering", href: "/engineering" },
  mediaId: "engineeringShowreel",
};
