import type { LucideIcon } from "lucide-react";
import {
  Bot,
  Layers,
  Atom,
  LineChart,
  Globe2,
  ServerCog,
  CloudCog,
  ShieldCheck,
  ScrollText,
  Database,
  Palette,
  Terminal,
  Gauge,
} from "lucide-react";

export type Discipline = {
  id: string;
  title: string;
  summary: string;
  icon: LucideIcon;
};

export const disciplines = {
  eyebrow: "Engineering",
  headline: {
    lead: "Everything we build,",
    italic: "built to ship.",
  },
  intro:
    "Thirteen disciplines, one team, one bar. No framework tourism, no vendor lock-in fan fiction — an opinionated stack and people who've shipped it before.",
  items: [
    {
      id: "agents",
      title: "Agentic systems",
      summary:
        "Tool-using, multi-step agents. MCP-native architecture. They finish what they start.",
      icon: Bot,
    },
    {
      id: "context",
      title: "Context engineering",
      summary:
        "The context window as a first-class architecture surface — not an afterthought prompt.",
      icon: Layers,
    },
    {
      id: "models",
      title: "Model post-training",
      summary:
        "Fine-tuning, distillation, preference alignment. A model shaped to your domain and budget.",
      icon: Atom,
    },
    {
      id: "evals",
      title: "Evals & AI observability",
      summary:
        "Traces, ground-truth regression, coding-agent harnesses. The layer that makes AI shippable.",
      icon: LineChart,
    },
    {
      id: "product",
      title: "Full-stack product engineering",
      summary:
        "Web, mobile, APIs — opinionated stack choices. Typed end-to-end, tested where it matters.",
      icon: Globe2,
    },
    {
      id: "platform",
      title: "Platform engineering",
      summary:
        "Internal developer platforms and self-service infra so every team ships without rebuilding the stack.",
      icon: ServerCog,
    },
    {
      id: "cloud",
      title: "Cloud architecture & infrastructure",
      summary:
        "Multi-region, IaC-first. Designed for agent-speed workloads — not human-centric load patterns.",
      icon: CloudCog,
    },
    {
      id: "security",
      title: "Security engineering",
      summary:
        "AppSec, threat modeling, zero-trust identity. Trust boundaries built for agents that can act.",
      icon: ShieldCheck,
    },
    {
      id: "governance",
      title: "AI governance & compliance",
      summary:
        "Policy-as-code, data lineage, bias audits, audit logs. EU AI Act and Colorado-ready.",
      icon: ScrollText,
    },
    {
      id: "data",
      title: "Data engineering & pipelines",
      summary:
        "The plumbing that keeps models grounded — clean data in, reliable retrieval out.",
      icon: Database,
    },
    {
      id: "design",
      title: "Design systems & frontend craft",
      summary:
        "Component architectures that scale across products without becoming a design tax.",
      icon: Palette,
    },
    {
      id: "devtools",
      title: "Developer tooling",
      summary:
        "CLIs, SDKs, MCP servers. The tools engineers reach for because someone made them right.",
      icon: Terminal,
    },
    {
      id: "perf",
      title: "Performance & scaling",
      summary:
        "Latency budgets, throughput ceilings, cost floors. Cost-per-token is now a product dimension.",
      icon: Gauge,
    },
  ] satisfies Discipline[],
};
