/**
 * Portability layer: swap this file to adapt the chat dock to another site.
 * system-prompt.ts imports exclusively from here -- never from content/ directly.
 */

import { engineering } from "@/content/engineering";
import { security } from "@/content/security";
import { disciplines } from "@/content/disciplines";
import { site } from "@/content/site";

export type KnowledgeVertical = {
  title: string;
  summary: string;
};

export type KnowledgeDiscipline = {
  title: string;
  summary: string;
};

export type KnowledgePillar = {
  title: string;
  summary: string;
};

export type Knowledge = {
  siteDescription: string;
  siteUrl: string;
  securityUrl: string;
  securityHeadline: string;
  securitySummary: string;
  engineeringVerticals: KnowledgeVertical[];
  disciplines: KnowledgeDiscipline[];
  securityPillars: KnowledgePillar[];
  ceoBio: string;
};

export const KNOWLEDGE: Knowledge = {
  siteDescription: site.description,
  siteUrl: site.url,
  securityUrl: site.securityUrl,
  securityHeadline: `${security.headline.lead} ${security.headline.italic}`,
  securitySummary: security.summary,
  engineeringVerticals: engineering.verticals.map((v) => ({
    title: v.title,
    summary: v.summary,
  })),
  disciplines: disciplines.items.map((d) => ({
    title: d.title,
    summary: d.summary,
  })),
  securityPillars: security.pillars.map((p) => ({
    title: p.title,
    summary: p.summary,
  })),
  ceoBio:
    "Zachary Ferguson is the founder and CEO of ZAICORE and ZAICORE Cyber Security. He's an Engineering Physics and Computer Engineering graduate who started both companies to build AI systems and applied cybersecurity from the ground up. Reach him at zachary@zaicore.com, or book a call at /book on this site.",
};
