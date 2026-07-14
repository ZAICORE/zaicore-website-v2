/**
 * Chat-dock health check, called on a schedule by
 * .github/workflows/chat-health.yml (every 15 minutes).
 *
 * Returns 200 when the dock can serve visitors, 503 when it cannot — the
 * workflow fails on a non-200, so GitHub emails Zachary even in the case
 * where this route (or the whole site) is too broken to send mail itself.
 *
 * Emails on "degraded" too, not just "down": a deprecated-but-still-working
 * model is the warning we want, since that is the state the dock sat in
 * before it broke.
 */

import { NextResponse } from "next/server";
import { checkChatHealth } from "@/lib/ai/health";
import { sendAlertEmail } from "@/lib/email";

/**
 * Best-effort alert throttle. At 15-minute checks, an unthrottled outage
 * would send ~96 emails a day. This is module scope, so it only holds for as
 * long as the serverless instance stays warm — it thins the flood rather than
 * guaranteeing exactly one email. Recovery is always announced.
 */
const ALERT_THROTTLE_MS = 60 * 60 * 1000;
let lastAlertAt = 0;
let lastStatus: string | null = null;

function unauthorized() {
  return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
}

export async function GET(request: Request) {
  const secret = process.env.CRON_SECRET;

  // Fail loudly rather than leaving an unauthenticated endpoint that spends
  // OpenRouter credits for anyone who finds it. The workflow surfaces this as
  // a failed run, which is itself the notification that setup is incomplete.
  if (!secret) {
    return NextResponse.json(
      { error: "CRON_SECRET is not configured on the server — health checks cannot run." },
      { status: 500 },
    );
  }

  const auth = request.headers.get("authorization");
  if (auth !== `Bearer ${secret}`) return unauthorized();

  // ?selftest=1 — proves the alert path actually delivers, without waiting for a
  // real outage to find out RESEND_API_KEY was never set in production.
  if (new URL(request.url).searchParams.get("selftest") === "1") {
    const res = await sendAlertEmail({
      subject: "🧪 ZAICORE chat-dock alert test",
      headline: "This is a test. Your alerting works.",
      problems: ["If you are reading this in your inbox, a real outage will reach you too."],
    });
    return NextResponse.json({ selftest: true, ...res }, { status: res.ok ? 200 : 503 });
  }

  const health = await checkChatHealth();

  const isBad = health.status !== "healthy";
  const recovered = health.status === "healthy" && lastStatus !== null && lastStatus !== "healthy";
  const throttled = Date.now() - lastAlertAt < ALERT_THROTTLE_MS;

  let emailed = false;
  let emailError: string | undefined;

  if (isBad && !throttled) {
    const down = health.status === "down";
    const res = await sendAlertEmail({
      subject: down
        ? "🔴 ZAICORE chat dock is DOWN"
        : "🟠 ZAICORE chat dock — degraded / model deprecated",
      headline: down
        ? "The chat dock is not answering visitors."
        : "The chat dock still works, but something needs attention.",
      problems: health.problems,
      detail: JSON.stringify(health.models, null, 2),
    });
    emailed = res.ok;
    emailError = res.reason;
    if (res.ok) lastAlertAt = Date.now();
  } else if (recovered) {
    const res = await sendAlertEmail({
      subject: "🟢 ZAICORE chat dock recovered",
      headline: "The chat dock is answering normally again.",
      problems: ["All configured models are responding and still listed on OpenRouter."],
    });
    emailed = res.ok;
    emailError = res.reason;
    lastAlertAt = 0;
  }

  lastStatus = health.status;

  // A problem we detected but could not report is itself a critical failure:
  // without this, a missing RESEND_API_KEY would mean a degraded dock returns
  // 200, the workflow passes, and nobody is ever told. Fail loudly instead so
  // GitHub's own failure email gets through.
  const alertUndeliverable = isBad && !throttled && !emailed;

  const httpStatus = health.status === "down" || alertUndeliverable ? 503 : 200;

  return NextResponse.json(
    {
      ...health,
      alert: {
        emailed,
        throttled: isBad && throttled,
        error: emailError,
        undeliverable: alertUndeliverable,
      },
    },
    { status: httpStatus },
  );
}
