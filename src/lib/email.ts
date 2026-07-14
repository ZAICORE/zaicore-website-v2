import { Resend } from "resend";

function getClient(): Resend | null {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.warn("[email] RESEND_API_KEY not configured, falling back to log-only");
    return null;
  }
  return new Resend(apiKey);
}

export type BookingEmailParams = {
  name: string;
  email: string;
  company?: string;
  workingOn: string;
  timeline?: string;
};

const NOTIFY_FROM = process.env.BOOK_NOTIFY_FROM ?? "ZAICORE Booking <booking@zaicore.com>";
const NOTIFY_TO = process.env.BOOK_NOTIFY_TO ?? "zachary@zaicore.com";

function renderBody(p: BookingEmailParams) {
  const escape = (s: string) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return `<!doctype html><html><body style="font-family:system-ui,-apple-system,sans-serif;line-height:1.55;color:#0e0e10;max-width:600px;margin:0 auto;padding:32px 24px;">
  <h2 style="font-weight:500;letter-spacing:-0.02em;margin:0 0 24px;">New booking request</h2>
  <table style="border-collapse:collapse;width:100%;font-size:14px;">
    <tr><td style="padding:8px 0;color:#6b6b72;width:140px;">Name</td><td style="padding:8px 0;">${escape(p.name)}</td></tr>
    <tr><td style="padding:8px 0;color:#6b6b72;">Email</td><td style="padding:8px 0;"><a href="mailto:${escape(p.email)}" style="color:#2e4f8c;">${escape(p.email)}</a></td></tr>
    ${p.company ? `<tr><td style="padding:8px 0;color:#6b6b72;">Company</td><td style="padding:8px 0;">${escape(p.company)}</td></tr>` : ""}
    ${p.timeline ? `<tr><td style="padding:8px 0;color:#6b6b72;">Timeline</td><td style="padding:8px 0;">${escape(p.timeline)}</td></tr>` : ""}
  </table>
  <div style="margin-top:24px;padding:20px;background:#f4f1ee;border-radius:12px;">
    <p style="margin:0 0 8px;font-size:12px;color:#6b6b72;text-transform:uppercase;letter-spacing:0.14em;">What they're working on</p>
    <p style="margin:0;white-space:pre-wrap;">${escape(p.workingOn)}</p>
  </div>
  <p style="margin-top:32px;font-size:12px;color:#9a9aa1;">Reply directly to reach ${escape(p.name)}.</p>
</body></html>`;
}

const ALERT_FROM = process.env.ALERT_FROM ?? "ZAICORE Alerts <alerts@zaicore.com>";
const ALERT_TO = process.env.ALERT_TO ?? "zachary@zaicore.com";

export type AlertEmailParams = {
  subject: string;
  headline: string;
  problems: string[];
  detail?: string;
};

export async function sendAlertEmail(p: AlertEmailParams): Promise<{ ok: boolean; reason?: string }> {
  const client = getClient();
  if (!client) {
    console.error("[alert] NOT SENT (no Resend key):", p.subject, p.problems);
    return { ok: false, reason: "no-resend-key" };
  }

  const escape = (s: string) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  const html = `<!doctype html><html><body style="font-family:system-ui,-apple-system,sans-serif;line-height:1.55;color:#0e0e10;max-width:600px;margin:0 auto;padding:32px 24px;">
  <h2 style="font-weight:500;letter-spacing:-0.02em;margin:0 0 8px;">${escape(p.headline)}</h2>
  <p style="margin:0 0 24px;font-size:13px;color:#6b6b72;">zaicore.com · chat dock health check</p>
  <ul style="margin:0;padding-left:18px;font-size:14px;">
    ${p.problems.map((x) => `<li style="margin-bottom:8px;">${escape(x)}</li>`).join("")}
  </ul>
  ${
    p.detail
      ? `<pre style="margin-top:24px;padding:16px;background:#f4f1ee;border-radius:12px;font-size:12px;white-space:pre-wrap;overflow-x:auto;">${escape(p.detail)}</pre>`
      : ""
  }
  <p style="margin-top:32px;font-size:12px;color:#9a9aa1;">Models are configured in <code>src/lib/ai/openrouter.ts</code>.</p>
</body></html>`;

  try {
    const { error } = await client.emails.send({
      from: ALERT_FROM,
      to: ALERT_TO,
      subject: p.subject,
      html,
    });
    if (error) {
      console.error("[alert] Resend returned error:", error);
      return { ok: false, reason: error.message };
    }
    return { ok: true };
  } catch (err) {
    console.error("[alert] send failed:", err);
    return { ok: false, reason: err instanceof Error ? err.message : "unknown" };
  }
}

export async function sendBookingEmail(params: BookingEmailParams): Promise<{ ok: boolean; reason?: string }> {
  const client = getClient();
  if (!client) {
    console.log("[email] Booking received (no Resend key):", params);
    return { ok: true, reason: "logged-only" };
  }

  try {
    const { error } = await client.emails.send({
      from: NOTIFY_FROM,
      to: NOTIFY_TO,
      subject: `New booking from ${params.name}${params.company ? ` (${params.company})` : ""}`,
      replyTo: params.email,
      html: renderBody(params),
    });
    if (error) {
      console.error("[email] Resend returned error:", error);
      return { ok: false, reason: error.message };
    }
    return { ok: true };
  } catch (err) {
    console.error("[email] send failed:", err);
    return { ok: false, reason: err instanceof Error ? err.message : "unknown" };
  }
}
