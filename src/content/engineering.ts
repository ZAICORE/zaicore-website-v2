import type { LucideIcon } from "lucide-react";
import { Bot, Atom, Mic, Eye, LineChart, ShieldCheck } from "lucide-react";

export type Vertical = {
  id: string;
  title: string;
  summary: string;
  description: string;
  icon: LucideIcon;
};

export const engineering = {
  eyebrow: "Engineering",
  headline: {
    lead: "AI-first engineering,",
    italic: "shipped into real production.",
  },
  intro:
    "We build the software off-the-shelf can't. Agents, proprietary models, real-time systems — engineered to how your team actually operates, not bent around a vendor's roadmap.",
  verticals: [
    {
      id: "agentic",
      title: "Agentic systems",
      summary: "Agents that complete the task.",
      description:
        "Tool-using, computer-use, MCP-native. Multi-step autonomy with evals and safeguards that make the behavior reliable in production. Not chatbots.",
      icon: Bot,
    },
    {
      id: "models",
      title: "Custom models",
      summary: "When the frontier isn't enough.",
      description:
        "Post-training, fine-tunes, distillation, reward modeling on your data. A model shaped to your domain — yours, not a vendor's.",
      icon: Atom,
    },
    {
      id: "voice",
      title: "Voice & realtime",
      summary: "Speech-to-speech that feels human.",
      description:
        "Sub-200ms first-token latency, interruption handling, duplex audio. Built on frontier voice models and the infrastructure that keeps them snappy.",
      icon: Mic,
    },
    {
      id: "vision",
      title: "Vision & multimodal",
      summary: "What the system sees becomes what it knows.",
      description:
        "Document parsing, visual agents, video understanding. Multimodal pipelines that connect pixels to structured knowledge.",
      icon: Eye,
    },
    {
      id: "evals",
      title: "Evals & observability",
      summary: "The layer that makes AI shippable.",
      description:
        "Traces, ground truth, regression catches, dashboards. So \"it works on my machine\" becomes \"it works in production — and we can prove it.\"",
      icon: LineChart,
    },
    {
      id: "security",
      title: "Applied security",
      summary: "Prompt injection, guardrails, compliance.",
      description:
        "The cybersecurity discipline feeding back into how we build every other system. SOC 2 trajectory. ZAICORE Security is the same team.",
      icon: ShieldCheck,
    },
  ] satisfies Vertical[],
  mediaId: "engineeringShowreel",
};
