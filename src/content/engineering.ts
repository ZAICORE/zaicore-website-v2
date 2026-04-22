import type { LucideIcon } from "lucide-react";
import { Cpu, Workflow, Eye, ShieldCheck, Waves, Network } from "lucide-react";

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
    lead: "Custom AI, shipped",
    italic: "into real production.",
  },
  intro:
    "We build AI systems that teams actually use. Agents, pipelines, tooling, evals. The kind of work that shows up in the metrics the week after it ships.",
  verticals: [
    {
      id: "agents",
      title: "Agents & copilots",
      summary: "Custom agents wired to your workflows.",
      description:
        "Claude, GPT, or whichever frontier model the job needs. Tool-using agents, streaming UIs, evals that keep them honest.",
      icon: Cpu,
    },
    {
      id: "pipelines",
      title: "Data & retrieval",
      summary: "RAG, ingest, observability.",
      description:
        "Indexing pipelines, vector stores, retrieval that answers real questions. Instrumented so you can see why it gave the answer it gave.",
      icon: Network,
    },
    {
      id: "voice",
      title: "Voice & realtime",
      summary: "Streamed audio and video interfaces.",
      description:
        "Speech-to-speech, interruption handling, low-latency pipelines. The kind of work that feels magic when it lands.",
      icon: Waves,
    },
    {
      id: "vision",
      title: "Vision & multimodal",
      summary: "Images, video, structured understanding.",
      description:
        "Document parsing, scene understanding, visual agents. What the model sees becomes what the product knows.",
      icon: Eye,
    },
    {
      id: "ops",
      title: "Infra & ops",
      summary: "The scaffolding under the AI.",
      description:
        "Railway, Vercel, Cloudflare. Typed APIs, CI gates, tests that actually catch regressions. Bet-your-launch-on-it infrastructure.",
      icon: Workflow,
    },
    {
      id: "security",
      title: "Secure by construction",
      summary: "Guardrails, audits, shipped safely.",
      description:
        "Prompt injection defense, secrets hygiene, SOC 2 trajectory. The security product informs every other engagement.",
      icon: ShieldCheck,
    },
  ] satisfies Vertical[],
  mediaId: "engineeringShowreel",
};
