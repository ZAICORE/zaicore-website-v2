import Link from "next/link";
import { site, footer } from "@/content/site";

function isExternal(href: string): boolean {
  return href.startsWith("http://") || href.startsWith("https://") || href.startsWith("mailto:");
}

export function Footer() {
  return (
    <footer className="relative w-full border-t border-hairline bg-[color:var(--cream-soft)]">
      <div className="mx-auto w-full max-w-[1280px] px-6 py-16 md:px-10 lg:px-14">
        <div className="grid grid-cols-1 gap-12 md:grid-cols-[1.3fr_1fr_1fr_1fr]">
          <div>
            <p className="font-serif text-2xl italic leading-[1.1] text-ink md:text-3xl">
              {site.tagline}
            </p>
            <p className="mt-4 max-w-sm text-sm text-muted">{site.description}</p>
          </div>
          {footer.columns.map((col) => (
            <div key={col.title}>
              <p className="eyebrow mb-4">{col.title}</p>
              <ul className="space-y-2">
                {col.links.map((l) =>
                  isExternal(l.href) ? (
                    <li key={l.href}>
                      <a
                        href={l.href}
                        className="text-sm text-ink-soft transition-colors hover:text-ink"
                        {...(l.href.startsWith("http")
                          ? { target: "_blank", rel: "noopener noreferrer" }
                          : {})}
                      >
                        {l.label}
                      </a>
                    </li>
                  ) : (
                    <li key={l.href}>
                      <Link
                        href={l.href}
                        className="text-sm text-ink-soft transition-colors hover:text-ink"
                      >
                        {l.label}
                      </Link>
                    </li>
                  ),
                )}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-16 flex flex-col items-start justify-between gap-4 border-t border-hairline pt-8 md:flex-row md:items-center">
          <p className="text-xs text-muted">{footer.copyright}</p>
          <p className="text-xs text-muted">{site.legalName}</p>
        </div>
      </div>
    </footer>
  );
}
