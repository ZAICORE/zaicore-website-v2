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

export type DisciplineGroup = {
  id: string;
  label: string;
  blurb: string;
  items: Discipline[];
};

export const disciplines = {
  eyebrow: "Engineering",
  headline: {
    lead: "Everything we build,",
    italic: "built to ship.",
  },
  intro:
    "The full range of what we build, from AI down to the infrastructure underneath it. One team, one bar, people who have shipped this before.",
  groups: [
    {
      id: "ai",
      label: "AI systems",
      blurb: "AI that takes real work off your team and holds up once it is live.",
      items: [
        {
          id: "agents",
          title: "Agents that take action",
          summary:
            "Software that completes multi-step tasks across your tools. It books, processes, and escalates, instead of just replying.",
          icon: Bot,
        },
        {
          id: "context",
          title: "Grounded in your data",
          summary:
            "We feed the model the right information at the right moment, so answers come from your business, not a guess.",
          icon: Layers,
        },
        {
          id: "models",
          title: "Models tuned to you",
          summary:
            "Off-the-shelf AI knows everything except your domain. We shape models to your data, your language, and your budget.",
          icon: Atom,
        },
        {
          id: "evals",
          title: "Tested and monitored",
          summary:
            "Tracing, regression checks, and ground truth that catch the AI when it drifts. The layer that makes it safe to ship.",
          icon: LineChart,
        },
      ],
    },
    {
      id: "platform",
      label: "Product and platform",
      blurb: "The software and infrastructure your business actually runs on.",
      items: [
        {
          id: "product",
          title: "Full-stack product",
          summary:
            "Web, mobile, and APIs. Typed end to end, tested where it counts, built to last.",
          icon: Globe2,
        },
        {
          id: "cloud",
          title: "Cloud and infrastructure",
          summary:
            "Multi-region infrastructure defined in code, built for real-world load and easy to run.",
          icon: CloudCog,
        },
        {
          id: "platform",
          title: "Internal platforms",
          summary:
            "Self-service tooling so your teams ship fast without rebuilding the same stack every time.",
          icon: ServerCog,
        },
        {
          id: "design",
          title: "Design and frontend",
          summary:
            "Interfaces and component systems that scale across products without slowing the team down.",
          icon: Palette,
        },
        {
          id: "devtools",
          title: "Developer tooling",
          summary:
            "CLIs, SDKs, and integrations your engineers actually reach for, because someone built them right.",
          icon: Terminal,
        },
        {
          id: "perf",
          title: "Performance and scale",
          summary:
            "Speed, throughput, and cost tuned so the system holds up as you grow, not just on launch day.",
          icon: Gauge,
        },
      ],
    },
    {
      id: "trust",
      label: "Data, security and trust",
      blurb: "The parts that keep everything safe, grounded, and compliant.",
      items: [
        {
          id: "data",
          title: "Data engineering",
          summary:
            "Clean pipelines that keep models grounded and reporting honest. Good data in, reliable answers out.",
          icon: Database,
        },
        {
          id: "security",
          title: "Security engineering",
          summary:
            "Threat modeling, secure identity, and trust boundaries built for systems that can take action on their own.",
          icon: ShieldCheck,
        },
        {
          id: "governance",
          title: "Governance and compliance",
          summary:
            "Audit logs, data lineage, and controls that keep you ready for rules like the EU AI Act.",
          icon: ScrollText,
        },
      ],
    },
  ] satisfies DisciplineGroup[],
};
