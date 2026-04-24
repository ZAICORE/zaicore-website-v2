import type { Metadata } from "next";
import { Nav } from "@/components/layout/Nav";
import { Footer } from "@/components/layout/Footer";
import { Reveal } from "@/components/motion/Reveal";
import { BookForm } from "@/components/book/BookForm";

export const metadata: Metadata = {
  title: "Book a call",
  description:
    "Tell us what you're building. We'll tell you straight whether we're the right team and how fast.",
};

export default function BookPage() {
  return (
    <>
      <Nav />
      <main className="relative w-full bg-[color:var(--cream)] pt-28 md:pt-36">
        <section className="mx-auto w-full max-w-[1280px] px-6 pb-24 md:px-10 md:pb-32 lg:px-14">
          <div className="grid grid-cols-1 gap-16 md:grid-cols-[1fr_1.1fr] md:gap-20 lg:gap-24">
            {/* Left — copy */}
            <Reveal className="md:sticky md:top-32 md:self-start">
              <p className="eyebrow">Book a call</p>
              <h1 className="display mt-5 text-[clamp(2.2rem,4.8vw,3.6rem)] text-ink">
                Tell us what{" "}
                <span className="serif-italic text-[color:var(--lapis-glow)]">
                  you&apos;re building.
                </span>
              </h1>
              <p className="mt-6 max-w-md text-[1rem] leading-[1.6] text-muted">
                Short form, straight reply. We&apos;ll tell you whether we&apos;re the right team,
                what we&apos;d ship first, and how fast.
              </p>

              <ul className="mt-10 space-y-5 text-[0.95rem] text-ink">
                <Expect
                  label="24-hour reply"
                  body="From Zach directly. If we&apos;re not the right fit we&apos;ll tell you who is."
                />
                <Expect
                  label="30-minute first call"
                  body="We talk shape, constraints, and whether AI is even the right answer."
                />
                <Expect
                  label="No decks"
                  body="We&apos;ll send back a plan, not a pitch."
                />
              </ul>

              <div className="mt-14 hidden max-w-sm rounded-[16px] border border-hairline bg-[color:var(--cream-soft)] px-5 py-4 md:block">
                <p className="text-[0.8rem] font-medium tracking-[-0.01em] text-ink">
                  Not sure yet?
                </p>
                <p className="mt-1.5 text-[0.85rem] leading-[1.55] text-muted">
                  Just email{" "}
                  <a
                    href="mailto:hello@zaicore.com"
                    className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
                  >
                    hello@zaicore.com
                  </a>
                  . Skip the form.
                </p>
              </div>
            </Reveal>

            {/* Right — form */}
            <Reveal delay={0.1}>
              <div className="rounded-[28px] border border-hairline bg-[color:var(--cream-soft)] p-6 md:p-10">
                <BookForm />
              </div>
            </Reveal>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}

function Expect({ label, body }: { label: string; body: string }) {
  return (
    <li className="flex items-start gap-4">
      <span className="mt-[9px] h-[6px] w-[6px] flex-shrink-0 rounded-full bg-[color:var(--lapis-glow)]" />
      <div>
        <p className="font-medium tracking-[-0.01em] text-ink">{label}</p>
        <p className="mt-1 text-[0.9rem] leading-[1.5] text-muted">{body}</p>
      </div>
    </li>
  );
}
