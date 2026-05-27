"use client";

import { useState, useEffect } from "react";
import { QrCode, X, Share2 } from "lucide-react";

/**
 * QR + native share button for a Person card.
 *
 * Renders one action button. Tapping opens a fullscreen overlay with
 * the giant QR (so another phone can focus + scan it easily). On
 * devices that support the Web Share API (iOS Safari, Android), the
 * native share sheet is offered alongside.
 *
 * The SVG is server-generated and passed in as a string — no
 * client-side QR encoding needed.
 */
export function ShareQR({
  url,
  qrSvg,
  name,
}: {
  url: string;
  qrSvg: string;
  name: string;
}) {
  const [open, setOpen] = useState(false);
  const [canShare, setCanShare] = useState(false);

  useEffect(() => {
    setCanShare(typeof navigator !== "undefined" && typeof navigator.share === "function");
  }, []);

  // Lock body scroll while overlay is open.
  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [open]);

  // Esc to close.
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  async function handleNativeShare() {
    if (typeof navigator === "undefined" || !navigator.share) return;
    try {
      await navigator.share({
        title: `${name} — ZAICORE`,
        text: `${name} · ZAICORE`,
        url,
      });
    } catch {
      // user cancelled — no-op
    }
  }

  const cardClasses =
    "group relative flex w-full items-center justify-between gap-4 rounded-2xl border border-hairline-strong bg-[rgba(250,248,247,0.82)] px-5 py-4 text-left backdrop-blur-[10px] transition-all duration-300 ease-out hover:-translate-y-0.5 hover:border-ink hover:shadow-[0_14px_28px_rgba(14,14,16,0.10)]";

  return (
    <>
      <button type="button" onClick={() => setOpen(true)} className={cardClasses}>
        <span className="flex flex-1 items-center gap-4 min-w-0">
          <span className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-[color:var(--lapis-mist)] text-[color:var(--lapis-glow)]">
            <QrCode className="h-4 w-4" strokeWidth={1.75} />
          </span>
          <span className="flex flex-1 flex-col text-left min-w-0">
            <span className="text-[1rem] font-medium leading-[1.1] tracking-[-0.01em] text-ink">
              Show QR
            </span>
            <span className="mt-[0.15rem] truncate text-[0.82rem] leading-[1.35] text-muted">
              Hold up to another phone to share
            </span>
          </span>
        </span>
        <span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full border border-hairline-strong text-ink transition-all duration-300">
          <QrCode className="h-3.5 w-3.5" strokeWidth={1.75} />
        </span>
      </button>

      {open && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label="QR code to share this profile"
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-[color:var(--cream)] px-6"
        >
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setOpen(false);
            }}
            aria-label="Close"
            className="absolute right-5 top-5 flex h-11 w-11 items-center justify-center rounded-full border border-hairline-strong bg-[rgba(250,248,247,0.9)] text-ink backdrop-blur-md transition-colors hover:border-ink"
          >
            <X className="h-5 w-5" strokeWidth={1.75} />
          </button>

          <div onClick={(e) => e.stopPropagation()} className="flex flex-col items-center gap-6">
            <p className="text-[0.7rem] uppercase tracking-[0.32em] text-muted">
              Scan to save my card
            </p>
            <div
              className="rounded-2xl border border-hairline-strong bg-paper p-6 shadow-[0_30px_60px_rgba(14,14,16,0.10)]"
              style={{ width: "min(78vw, 420px)", height: "min(78vw, 420px)" }}
              // SVG is server-generated; safe inline.
              dangerouslySetInnerHTML={{ __html: qrSvg }}
            />
            <p className="serif-italic text-center text-[1.1rem] leading-[1.4] text-ink/80">
              {name}
            </p>
            {canShare && (
              <button
                type="button"
                onClick={handleNativeShare}
                className="inline-flex items-center gap-2 rounded-full bg-ink px-5 py-3 text-[0.9rem] font-medium text-cream transition-transform hover:-translate-y-0.5"
              >
                <Share2 className="h-4 w-4" strokeWidth={1.75} />
                Share via…
              </button>
            )}
            <p className="text-[0.72rem] uppercase tracking-[0.28em] text-muted-soft">
              Tap anywhere to close
            </p>
          </div>
        </div>
      )}
    </>
  );
}
