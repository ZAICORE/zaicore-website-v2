import type { LucideIcon } from "lucide-react";
import { Flag, UserX, Radar, Mail } from "lucide-react";

export type SecurityPillar = {
  id: string;
  title: string;
  summary: string;
  icon: LucideIcon;
};

export const security = {
  eyebrow: "Security",
  headline: {
    lead: "An AI security team,",
    italic: "watching 24/7.",
  },
  summary:
    "An always-on team protecting you, your family, and the systems your team relies on. Data-broker removal, breach intelligence, and managed email defense. Plus invisible canary traps most platforms don't run.",
  pillars: [
    {
      id: "canary",
      title: "Canary traps",
      summary:
        "Invisible tripwires intruders hit the moment they probe, before they know it exists.",
      icon: Flag,
    },
    {
      id: "broker",
      title: "Data-broker removal",
      summary:
        "764+ data brokers scrubbed of your personal information, re-checked every week.",
      icon: UserX,
    },
    {
      id: "breach",
      title: "Breach & credential monitoring",
      summary:
        "19B+ leaked credentials and 850+ dark web sources watched for anything tied to you.",
      icon: Radar,
    },
    {
      id: "email",
      title: "Managed email defense",
      summary:
        "Phishing, impersonation, and exec BEC flagged in real time on Gmail. M365 for enterprise.",
      icon: Mail,
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
