import type { LucideIcon } from "lucide-react";
import {
  Flag,
  ShieldAlert,
  Laptop,
  Mail,
  Globe,
  Newspaper,
} from "lucide-react";

export type SecurityPillar = {
  id: string;
  title: string;
  summary: string;
  icon: LucideIcon;
};

export const security = {
  eyebrow: "Security",
  headline: {
    lead: "An AI security agent,",
    italic: "watching 24/7.",
  },
  summary:
    "One always-on agent protecting you, your family, and the systems your team relies on. Identity cleanup, breach intelligence, endpoint and email defense — plus invisible canary traps most platforms don't run.",
  pillars: [
    {
      id: "canary",
      title: "Canary traps",
      summary:
        "Invisible tripwires intruders hit the moment they probe — before they know it exists.",
      icon: Flag,
    },
    {
      id: "intel",
      title: "Identity & breach intel",
      summary:
        "764+ data brokers scrubbed. 19B+ leaked credentials and 850+ dark web sources watched.",
      icon: ShieldAlert,
    },
    {
      id: "endpoint",
      title: "Endpoint scanner",
      summary:
        "Zero-config agent for macOS, Windows, Linux. Catches persistence, infostealers, malware.",
      icon: Laptop,
    },
    {
      id: "email",
      title: "Managed email defense",
      summary:
        "Phishing, impersonation, exec BEC — triaged on M365 and Google Workspace with human handoff.",
      icon: Mail,
    },
    {
      id: "browser",
      title: "Browser protection",
      summary:
        "Phishing sites blocked in-session. Form autofill watched. Signed feeds verified on-device.",
      icon: Globe,
    },
    {
      id: "briefing",
      title: "Weekly AI briefing",
      summary:
        "Plain-English recap in your inbox: what we caught, what you should do, nothing more.",
      icon: Newspaper,
    },
  ] satisfies SecurityPillar[],
  cta: {
    label: "Visit security.zaicore.com",
    href: "https://security.zaicore.com",
    external: true,
  },
  mediaId: "securityShowreel",
  mascotId: "mascotSentinel",
};
