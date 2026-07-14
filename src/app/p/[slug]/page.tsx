import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { notFound } from "next/navigation";
import { ArrowUpRight, ArrowDownToLine, Mail, Phone, Globe } from "lucide-react";
import QRCode from "qrcode";
import { Nav } from "@/components/layout/Nav";
import { Footer } from "@/components/layout/Footer";
import { people, type Person } from "@/content/people";
import { site } from "@/content/site";
import { ShareQR } from "./ShareQR";

// Brand icons (lucide-react dropped trademarked logos; inline so the
// LinkedIn / X / GitHub buttons keep their familiar marks).
function Linkedin({ className, strokeWidth = 0 }: { className?: string; strokeWidth?: number }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" strokeWidth={strokeWidth} aria-hidden>
      <path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.95v5.66H9.36V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z" />
    </svg>
  );
}
function Twitter({ className, strokeWidth = 0 }: { className?: string; strokeWidth?: number }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" strokeWidth={strokeWidth} aria-hidden>
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
    </svg>
  );
}
function Github({ className, strokeWidth = 0 }: { className?: string; strokeWidth?: number }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" strokeWidth={strokeWidth} aria-hidden>
      <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.4 3-.405 1.02.005 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
    </svg>
  );
}
interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const p = people[slug];
  if (!p) return { title: "Profile not found" };
  return {
    title: `${p.name} · ${p.title}, ${p.company}`,
    description: p.bio,
    robots: { index: false, follow: false },
    openGraph: {
      title: `${p.name} — ${p.title} at ${p.company}`,
      description: p.bio,
      type: "profile",
    },
  };
}

export default async function PersonPage({ params }: Props) {
  const { slug } = await params;
  const person = people[slug];
  if (!person) notFound();

  const profileUrl = `${site.url}/p/${person.slug}`;
  const qrSvg = await QRCode.toString(profileUrl, {
    type: "svg",
    errorCorrectionLevel: "M",
    margin: 1,
    color: { dark: "#0E0E10", light: "#FAF8F7" },
  });

  return (
    <>
      <Nav />
      <main className="relative w-full bg-[color:var(--cream)] pt-28 pb-24 md:pt-36 md:pb-32">
        <div className="mx-auto w-full max-w-[680px] px-6 md:px-10">
          <Card person={person} profileUrl={profileUrl} qrSvg={qrSvg} />
        </div>
      </main>
      <Footer />
    </>
  );
}

function Card({ person, profileUrl, qrSvg }: { person: Person; profileUrl: string; qrSvg: string }) {
  const initials = (
    person.initials ?? `${person.givenName[0] ?? ""}${person.familyName[0] ?? ""}`
  ).toUpperCase();

  const actions: Array<{
    label: string;
    sublabel: string;
    href: string;
    icon: React.ComponentType<{ className?: string; strokeWidth?: number }>;
    external?: boolean;
    download?: boolean;
  }> = [];

  actions.push({
    label: "Save Contact",
    sublabel: "Adds to your phone",
    href: `/api/p/${person.slug}/vcard`,
    icon: ArrowDownToLine,
    download: true,
  });

  if (person.linkedin) {
    actions.push({
      label: "LinkedIn",
      sublabel: linkedinHandle(person.linkedin),
      href: person.linkedin,
      icon: Linkedin,
      external: true,
    });
  }
  if (person.email) {
    actions.push({
      label: "Email",
      sublabel: person.email,
      href: `mailto:${person.email}`,
      icon: Mail,
    });
  }
  if (person.phone) {
    actions.push({
      label: "Call",
      sublabel: person.phone,
      href: `tel:${person.phone.replace(/[^+\d]/g, "")}`,
      icon: Phone,
    });
  }
  if (person.twitter) {
    actions.push({
      label: "X / Twitter",
      sublabel: twitterHandle(person.twitter),
      href: person.twitter,
      icon: Twitter,
      external: true,
    });
  }
  if (person.github) {
    actions.push({
      label: "GitHub",
      sublabel: githubHandle(person.github),
      href: person.github,
      icon: Github,
      external: true,
    });
  }
  if (person.website && person.website !== person.companyUrl) {
    actions.push({
      label: "Website",
      sublabel: stripScheme(person.website),
      href: person.website,
      icon: Globe,
      external: true,
    });
  }
  if (person.companyUrl) {
    actions.push({
      label: person.company,
      sublabel: stripScheme(person.companyUrl),
      href: person.companyUrl,
      icon: Globe,
      external: true,
    });
  }

  return (
    <article className="flex flex-col items-center text-center">
      {/* Avatar */}
      <div className="relative h-32 w-32 overflow-hidden rounded-full bg-[color:var(--lapis-mist)] ring-1 ring-hairline-strong md:h-36 md:w-36">
        {person.photo ? (
          <Image
            src={person.photo}
            alt={person.name}
            fill
            sizes="(min-width: 768px) 144px, 128px"
            className="object-cover"
            priority
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-[2rem] font-medium text-[color:var(--lapis-glow)] tracking-tight md:text-[2.4rem]">
            {initials}
          </div>
        )}
      </div>

      {/* Name + title */}
      <h1 className="mt-7 text-[clamp(2rem,5vw,2.75rem)] font-medium leading-[1.05] tracking-[-0.02em] text-ink">
        {person.name}
      </h1>
      <p className="mt-3 text-[0.78rem] uppercase tracking-[0.32em] text-muted">
        {person.title}
        <span className="mx-2 text-muted-soft">·</span>
        <span className="text-[color:var(--lapis-glow)]">{person.company}</span>
      </p>

      {/* Bio */}
      <p className="serif-italic mt-7 max-w-[420px] text-[1.1rem] leading-[1.45] text-ink/85">
        {person.bio}
      </p>
      {person.city && (
        <p className="mt-3 text-[0.78rem] uppercase tracking-[0.28em] text-muted-soft">
          {person.city}
        </p>
      )}

      {/* Divider */}
      <div className="mt-10 flex w-full items-center justify-center gap-3">
        <span className="h-px flex-1 max-w-[120px] bg-gradient-to-r from-transparent via-hairline-strong to-transparent" />
        <span className="block h-1.5 w-1.5 rotate-45 bg-[color:var(--lapis-glow)]" aria-hidden />
        <span className="h-px flex-1 max-w-[120px] bg-gradient-to-r from-transparent via-hairline-strong to-transparent" />
      </div>

      {/* Action cards — Show QR is first so the owner can pull it up and share fast */}
      <div className="mt-10 grid w-full grid-cols-1 gap-3">
        <ShareQR url={profileUrl} qrSvg={qrSvg} name={person.name} />
        {actions.map((a) => (
          <ActionCard key={a.label} {...a} />
        ))}
      </div>
    </article>
  );
}

function ActionCard({
  label,
  sublabel,
  href,
  icon: Icon,
  external,
  download,
}: {
  label: string;
  sublabel: string;
  href: string;
  icon: React.ComponentType<{ className?: string; strokeWidth?: number }>;
  external?: boolean;
  download?: boolean;
}) {
  const classes =
    "group relative flex w-full items-center justify-between gap-4 rounded-2xl border border-hairline-strong bg-[rgba(250,248,247,0.82)] px-5 py-4 text-left backdrop-blur-[10px] transition-all duration-300 ease-out hover:-translate-y-0.5 hover:border-ink hover:shadow-[0_14px_28px_rgba(14,14,16,0.10)]";

  const body = (
    <>
      <span className="flex flex-1 items-center gap-4 min-w-0">
        <span className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-[color:var(--lapis-mist)] text-[color:var(--lapis-glow)]">
          <Icon className="h-4 w-4" strokeWidth={1.75} />
        </span>
        <span className="flex flex-1 flex-col text-left min-w-0">
          <span className="text-[1rem] font-medium leading-[1.1] tracking-[-0.01em] text-ink">
            {label}
          </span>
          <span className="mt-[0.15rem] truncate text-[0.82rem] leading-[1.35] text-muted">
            {sublabel}
          </span>
        </span>
      </span>
      <span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full border border-hairline-strong text-ink transition-all duration-300">
        <ArrowUpRight className="h-3.5 w-3.5" strokeWidth={1.75} />
      </span>
    </>
  );

  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" className={classes}>
        {body}
      </a>
    );
  }
  if (download) {
    return (
      <a href={href} download className={classes}>
        {body}
      </a>
    );
  }
  return (
    <Link href={href} className={classes}>
      {body}
    </Link>
  );
}

function stripScheme(url: string): string {
  return url.replace(/^https?:\/\//, "").replace(/\/$/, "");
}
function linkedinHandle(url: string): string {
  const m = url.match(/linkedin\.com\/in\/([^/]+)/i);
  return m ? `linkedin.com/in/${m[1]}` : stripScheme(url);
}
function twitterHandle(url: string): string {
  const m = url.match(/(?:twitter|x)\.com\/([^/]+)/i);
  return m ? `@${m[1]}` : stripScheme(url);
}
function githubHandle(url: string): string {
  const m = url.match(/github\.com\/([^/]+)/i);
  return m ? `@${m[1]}` : stripScheme(url);
}
