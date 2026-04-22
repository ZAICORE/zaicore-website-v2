export const site = {
  name: "ZAICORE",
  legalName: "Zaicore Software Solutions Inc.",
  tagline: "AI engineering and applied security.",
  description:
    "ZAICORE builds AI systems and ships ZAICORE Security — a cybersecurity product for people who want a plan, not notifications.",
  url: "https://zaicore.com",
  securityUrl: "https://security.zaicore.com",
  email: "hello@zaicore.com",
  social: {
    x: "https://x.com/zaicore",
    linkedin: "https://www.linkedin.com/company/zaicore",
    github: "https://github.com/ZAICORE",
  },
} as const;

export const nav = {
  primary: [
    { label: "Engineering", href: "#engineering" },
    { label: "ZAICORE Security", href: "#security", accent: true },
    { label: "About", href: "#about" },
    { label: "Contact", href: "#contact" },
  ],
  cta: { label: "Book a call", href: "#contact" },
} as const;

export const footer = {
  columns: [
    {
      title: "Company",
      links: [
        { label: "About", href: "#about" },
        { label: "Contact", href: "#contact" },
        { label: "Careers", href: "/careers" },
      ],
    },
    {
      title: "Products",
      links: [
        { label: "ZAICORE Security", href: "https://security.zaicore.com" },
        { label: "Engineering Services", href: "#engineering" },
      ],
    },
    {
      title: "Legal",
      links: [
        { label: "Privacy", href: "/privacy" },
        { label: "Terms", href: "/terms" },
      ],
    },
  ],
  copyright: `© ${new Date().getFullYear()} Zaicore Software Solutions Inc.`,
} as const;
