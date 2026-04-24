"use client";

import { useState, type FormEvent } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Check } from "lucide-react";

type Status = "idle" | "sending" | "sent" | "error";

export function BookForm() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (status === "sending") return;
    setStatus("sending");
    setError(null);

    const form = new FormData(e.currentTarget);
    const payload = {
      name: form.get("name"),
      email: form.get("email"),
      company: form.get("company"),
      workingOn: form.get("workingOn"),
      timeline: form.get("timeline"),
      website: form.get("website"),
    };

    try {
      const res = await fetch("/api/book", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = (await res.json()) as { ok?: boolean; error?: string };
      if (!res.ok || !data.ok) {
        setError(data.error ?? "Something went wrong.");
        setStatus("error");
        return;
      }
      setStatus("sent");
      (e.target as HTMLFormElement).reset();
    } catch {
      setError("Network hiccup. Try again?");
      setStatus("error");
    }
  }

  return (
    <div className="relative">
      <AnimatePresence mode="wait">
        {status === "sent" ? (
          <motion.div
            key="success"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
            className="rounded-[24px] border border-hairline bg-[color:var(--paper)] p-10 text-center"
          >
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-[color:var(--lapis-mist)] text-[color:var(--lapis-glow)]">
              <Check className="h-6 w-6" strokeWidth={1.5} />
            </div>
            <h3 className="display mt-6 text-[clamp(1.6rem,2.4vw,2rem)] text-ink">
              Got it.{" "}
              <span className="serif-italic text-[color:var(--lapis-glow)]">
                Zach will reply within 24 hours.
              </span>
            </h3>
            <p className="mx-auto mt-4 max-w-md text-[0.95rem] text-muted">
              If it&apos;s urgent, just email{" "}
              <a
                href="mailto:zachary@zaicore.com"
                className="text-ink underline decoration-hairline-strong underline-offset-4 hover:decoration-ink"
              >
                zachary@zaicore.com
              </a>
              .
            </p>
          </motion.div>
        ) : (
          <motion.form
            key="form"
            onSubmit={onSubmit}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="space-y-5"
            noValidate
          >
            <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
              <Field label="Name" name="name" required autoComplete="name" />
              <Field label="Email" name="email" type="email" required autoComplete="email" />
            </div>
            <Field label="Company (optional)" name="company" autoComplete="organization" />
            <Textarea
              label="What are you working on?"
              name="workingOn"
              required
              placeholder="Give us the shape of the problem. We'll tell you straight whether we're the right team."
              rows={5}
            />
            <Field
              label="Timeline (optional)"
              name="timeline"
              placeholder="e.g. starting next month, flexible, exploring"
            />

            {/* honeypot — hidden from humans, attractive to bots */}
            <input
              type="text"
              name="website"
              tabIndex={-1}
              autoComplete="off"
              aria-hidden="true"
              className="absolute left-[-9999px] h-0 w-0 opacity-0"
            />

            {error && (
              <p className="text-[0.9rem] text-[color:#b84b4b]" role="alert">
                {error}
              </p>
            )}

            <div className="flex items-center justify-between gap-4 pt-2">
              <p className="text-[0.8rem] text-muted">
                We&apos;ll never spam, sell, or forward your info.
              </p>
              <button
                type="submit"
                disabled={status === "sending"}
                className="group relative inline-flex items-center gap-2 rounded-full bg-ink px-6 py-3 text-[0.95rem] font-medium text-cream transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_10px_30px_rgba(14,14,16,0.2)] disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:translate-y-0 disabled:hover:shadow-none"
              >
                {status === "sending" ? "Sending…" : "Send message"}
              </button>
            </div>
          </motion.form>
        )}
      </AnimatePresence>
    </div>
  );
}

type FieldProps = {
  label: string;
  name: string;
  type?: string;
  required?: boolean;
  placeholder?: string;
  autoComplete?: string;
};

function Field({ label, name, type = "text", required, placeholder, autoComplete }: FieldProps) {
  return (
    <label className="block">
      <span className="block text-[0.8rem] font-medium tracking-[-0.01em] text-ink">
        {label}
        {required && <span className="ml-1 text-[color:var(--lapis-glow)]">*</span>}
      </span>
      <input
        name={name}
        type={type}
        required={required}
        placeholder={placeholder}
        autoComplete={autoComplete}
        className="mt-2 w-full rounded-[12px] border border-hairline bg-[color:var(--paper)] px-4 py-3 text-[0.95rem] text-ink outline-none transition-all duration-200 placeholder:text-muted-soft focus:border-[color:var(--lapis-glow)] focus:ring-4 focus:ring-[color:var(--lapis-mist)]"
      />
    </label>
  );
}

type TextareaProps = {
  label: string;
  name: string;
  required?: boolean;
  placeholder?: string;
  rows?: number;
};

function Textarea({ label, name, required, placeholder, rows = 4 }: TextareaProps) {
  return (
    <label className="block">
      <span className="block text-[0.8rem] font-medium tracking-[-0.01em] text-ink">
        {label}
        {required && <span className="ml-1 text-[color:var(--lapis-glow)]">*</span>}
      </span>
      <textarea
        name={name}
        required={required}
        rows={rows}
        placeholder={placeholder}
        className="mt-2 w-full resize-y rounded-[12px] border border-hairline bg-[color:var(--paper)] px-4 py-3 text-[0.95rem] text-ink outline-none transition-all duration-200 placeholder:text-muted-soft focus:border-[color:var(--lapis-glow)] focus:ring-4 focus:ring-[color:var(--lapis-mist)]"
      />
    </label>
  );
}
