import { NextResponse } from "next/server";
import { sendBookingEmail } from "@/lib/email";

export const runtime = "nodejs";

const buckets = new Map<string, { count: number; resetAt: number }>();
const WINDOW_MS = 60_000;
const MAX_PER_WINDOW = 5;

function rateLimited(ip: string): boolean {
  const now = Date.now();
  const bucket = buckets.get(ip);
  if (!bucket || bucket.resetAt < now) {
    buckets.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return false;
  }
  bucket.count += 1;
  return bucket.count > MAX_PER_WINDOW;
}

function str(v: unknown, max = 2000): string | null {
  if (typeof v !== "string") return null;
  const t = v.trim();
  if (!t) return null;
  if (t.length > max) return t.slice(0, max);
  return t;
}

function isEmail(s: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s) && s.length <= 254;
}

export async function POST(req: Request) {
  const ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ?? "unknown";
  if (rateLimited(ip)) {
    return NextResponse.json({ error: "Too many requests" }, { status: 429 });
  }

  let payload: Record<string, unknown>;
  try {
    payload = (await req.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  if (str(payload.website, 1)) {
    return NextResponse.json({ ok: true });
  }

  const name = str(payload.name, 120);
  const email = str(payload.email, 254);
  const workingOn = str(payload.workingOn, 4000);
  const company = str(payload.company, 160) ?? undefined;
  const timeline = str(payload.timeline, 160) ?? undefined;

  if (!name || !email || !workingOn) {
    return NextResponse.json(
      { error: "Name, email, and a short note are required." },
      { status: 400 },
    );
  }
  if (!isEmail(email)) {
    return NextResponse.json({ error: "That email doesn't look right." }, { status: 400 });
  }

  const result = await sendBookingEmail({ name, email, company, workingOn, timeline });
  if (!result.ok) {
    return NextResponse.json({ error: "Couldn't send. Try again in a moment." }, { status: 502 });
  }
  return NextResponse.json({ ok: true });
}
