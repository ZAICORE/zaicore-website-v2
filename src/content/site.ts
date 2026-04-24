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

export type NavItem = {
  label: string;
  href: string;
  external?: boolean;
};

export const nav = {
  primary: [
    { label: "Engineering", href: "/engineering" },
    { label: "Security", href: "https://security.zaicore.com", external: true },
  ] satisfies readonly NavItem[],
  cta: { label: "Book a call", href: "/book" },
} as const;

export const footer = {
  columns: [
    {
      title: "Work",
      links: [
        { label: "Engineering", href: "/engineering" },
        { label: "ZAICORE Security", href: "https://security.zaicore.com" },
        { label: "Book a call", href: "/book" },
      ],
    },
    {
      title: "Contact",
      links: [
        { label: "hello@zaicore.com", href: "mailto:hello@zaicore.com" },
        { label: "zachary@zaicore.com", href: "mailto:zachary@zaicore.com" },
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
