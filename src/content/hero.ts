export const hero = {
  /**
   * Minimal by design — Kyle Skelly's Sculpt reference: big title, tiny
   * subtitle, one or two CTAs. Everything else lives below the fold.
   */
  headline: {
    lead: "We build what",
    italic: "off-the-shelf can't.",
  },
  subline: "Proprietary software, AI systems, and real security — engineered to how your team actually operates.",
  ctas: [
    { label: "See the engineering", href: "#engineering", variant: "primary" as const },
    { label: "ZAICORE Security", href: "https://security.zaicore.com", variant: "ghost" as const, external: true },
  ],
  mascots: {
    left: { id: "mascotEngineer", label: "Engineering" },
    right: { id: "mascotSentinel", label: "Security" },
  },
};
