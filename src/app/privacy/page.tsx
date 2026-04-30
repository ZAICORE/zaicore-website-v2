import type { Metadata } from "next";
import Link from "next/link";
import { LegalPage, LegalSection } from "@/components/legal/LegalPage";

export const metadata: Metadata = {
  title: "Privacy",
  description: "How we handle information collected through the ZAICORE marketing site.",
};

export default function PrivacyPage() {
  return (
    <LegalPage
      eyebrow="Privacy"
      title={
        <>
          The short version:{" "}
          <span className="serif-italic text-[color:var(--lapis-glow)]">
            we collect the bare minimum.
          </span>
        </>
      }
      updated="April 24, 2026"
    >
      <LegalSection heading="What this covers">
        <p>
          This policy covers <strong>zaicore.com</strong>, our engineering marketing site and the
          booking form on this site. It does <em>not</em> cover{" "}
          <Link
            href="https://security.zaicore.com"
            className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
          >
            ZAICORE Security
          </Link>
          , which has its own product privacy policy because it handles much more sensitive data.
        </p>
      </LegalSection>

      <LegalSection heading="What we collect">
        <p>Only what you hand us. Specifically:</p>
        <ul className="list-disc space-y-2 pl-5">
          <li>
            <strong>Booking form submissions</strong>: your name, email, an optional company name,
            what you&apos;re working on, and an optional timeline. You submit this on purpose.
          </li>
          <li>
            <strong>Standard web server logs</strong>: IP address and request metadata, retained
            briefly for abuse prevention and basic analytics.
          </li>
        </ul>
        <p>
          We don&apos;t run third-party ad trackers. We don&apos;t sell or rent data to anyone.
          Ever.
        </p>
      </LegalSection>

      <LegalSection heading="How we use it">
        <p>
          Booking submissions go to one address:{" "}
          <a
            href="mailto:zachary@zaicore.com"
            className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
          >
            zachary@zaicore.com
          </a>
          . Zach reads them. Zach replies. That&apos;s the whole pipeline.
        </p>
        <p>
          Server logs are used to keep the site running and catch bots hitting the form endpoint.
        </p>
      </LegalSection>

      <LegalSection heading="Email delivery">
        <p>
          Booking notifications are delivered through{" "}
          <Link
            href="https://resend.com"
            className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
          >
            Resend
          </Link>
          , our transactional email provider. Resend processes the email in transit; we rely on
          their privacy and security practices for that hop.
        </p>
      </LegalSection>

      <LegalSection heading="Retention">
        <p>
          Inbound booking emails sit in Zach&apos;s inbox until handled. If you ask us to delete
          your message, email{" "}
          <a
            href="mailto:privacy@zaicore.com"
            className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
          >
            privacy@zaicore.com
          </a>{" "}
          and we will.
        </p>
        <p>Server logs are rotated routinely.</p>
      </LegalSection>

      <LegalSection heading="Your rights">
        <p>
          You can ask us to access, correct, or delete anything we have that identifies you. Email{" "}
          <a
            href="mailto:privacy@zaicore.com"
            className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
          >
            privacy@zaicore.com
          </a>
          . We&apos;ll act within 30 days.
        </p>
      </LegalSection>

      <LegalSection heading="Kids">
        <p>
          This site isn&apos;t for children under 13. We don&apos;t knowingly collect data from
          them.
        </p>
      </LegalSection>

      <LegalSection heading="Changes">
        <p>
          If we change this, we&apos;ll update the date at the top. Material changes get called out
          here for a while.
        </p>
      </LegalSection>

      <LegalSection heading="Contact">
        <p>
          Questions?{" "}
          <a
            href="mailto:privacy@zaicore.com"
            className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
          >
            privacy@zaicore.com
          </a>
          .
        </p>
      </LegalSection>
    </LegalPage>
  );
}
