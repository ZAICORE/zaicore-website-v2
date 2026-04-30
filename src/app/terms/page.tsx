import type { Metadata } from "next";
import { LegalPage, LegalSection } from "@/components/legal/LegalPage";

export const metadata: Metadata = {
  title: "Terms",
  description:
    "The baseline terms that govern use of the ZAICORE marketing site and booking form.",
};

export default function TermsPage() {
  return (
    <LegalPage
      eyebrow="Terms"
      title={
        <>
          The rules of the road,{" "}
          <span className="serif-italic text-[color:var(--lapis-glow)]">kept short.</span>
        </>
      }
      updated="April 24, 2026"
    >
      <LegalSection heading="Scope">
        <p>
          These terms govern use of <strong>zaicore.com</strong>, the marketing site and booking
          form. They do not govern ZAICORE Security, which has its own product terms of service.
        </p>
      </LegalSection>

      <LegalSection heading="Using the site">
        <p>You agree not to:</p>
        <ul className="list-disc space-y-2 pl-5">
          <li>Scrape, spider, or otherwise automate the site at a rate that looks abusive.</li>
          <li>
            Submit false information or someone else&apos;s contact info to the booking form.
          </li>
          <li>
            Attempt to breach, probe, or interfere with the site or its infrastructure. If you do
            so with authorization, email{" "}
            <a
              href="mailto:security@zaicore.com"
              className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
            >
              security@zaicore.com
            </a>{" "}
            first.
          </li>
        </ul>
      </LegalSection>

      <LegalSection heading="Content">
        <p>
          All text, code, marks, and assets on this site are owned by Zaicore Software Solutions
          Inc. or used with permission. Don&apos;t republish without asking.
        </p>
      </LegalSection>

      <LegalSection heading="Bookings are not contracts">
        <p>
          Submitting the booking form opens a conversation. It does not create a binding
          engagement. A formal engagement only exists once both parties sign a dedicated
          agreement.
        </p>
      </LegalSection>

      <LegalSection heading="No warranties">
        <p>
          The site is provided as-is. We make no guarantees about uptime, accuracy, or fitness for
          any particular purpose.
        </p>
      </LegalSection>

      <LegalSection heading="Liability">
        <p>
          To the maximum extent permitted by law, Zaicore Software Solutions Inc. is not liable for
          indirect, incidental, or consequential damages arising from your use of the site.
        </p>
      </LegalSection>

      <LegalSection heading="Changes">
        <p>
          We may update these terms. The date at the top reflects the current version. Continued
          use after changes means you accept them.
        </p>
      </LegalSection>

      <LegalSection heading="Governing law">
        <p>
          These terms are governed by the laws of the State of Delaware, United States, without
          regard to conflict-of-laws principles.
        </p>
      </LegalSection>

      <LegalSection heading="Contact">
        <p>
          Email{" "}
          <a
            href="mailto:zachary@zaicore.com"
            className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
          >
            zachary@zaicore.com
          </a>{" "}
          for anything here.
        </p>
      </LegalSection>
    </LegalPage>
  );
}
