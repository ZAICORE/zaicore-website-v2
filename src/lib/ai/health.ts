/**
 * Health check for the chat dock's models.
 *
 * Two independent failure modes, both of which have already bitten us:
 *
 *   1. A model stops responding (404, auth, outage).
 *   2. A model is *deprecated* — still answering today, gone tomorrow.
 *
 * On 2026-07-14 both PRIMARY and FALLBACK were deprecated in the same
 * window and the dock went down silently. So we check the live catalogue
 * as well as making a real call: the catalogue check is the one that warns
 * us *before* an outage rather than after.
 */

import { PRIMARY_MODEL, FALLBACK_MODEL } from "./openrouter";

const MODELS_URL = "https://openrouter.ai/api/v1/models";
const COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions";

export type ModelHealth = {
  model: string;
  role: "primary" | "fallback";
  /** Present in OpenRouter's live catalogue. False ⇒ deprecated or removed. */
  listed: boolean;
  /** Answered a real completion request. */
  responds: boolean;
  latencyMs?: number;
  error?: string;
};

export type ChatHealth = {
  status: "healthy" | "degraded" | "down";
  checkedAt: string;
  models: ModelHealth[];
  /** Human-readable problems, safe to drop straight into an alert email. */
  problems: string[];
};

async function listedModels(apiKey: string): Promise<Set<string> | null> {
  try {
    const res = await fetch(MODELS_URL, {
      headers: { Authorization: `Bearer ${apiKey}` },
      signal: AbortSignal.timeout(15_000),
    });
    if (!res.ok) return null;
    const body = (await res.json()) as { data?: Array<{ id?: string }> };
    return new Set((body.data ?? []).map((m) => m.id).filter((id): id is string => !!id));
  } catch {
    // Catalogue unreachable — don't infer deprecation from it.
    return null;
  }
}

async function probe(model: string, apiKey: string): Promise<{ ok: boolean; ms: number; error?: string }> {
  const started = performance.now();
  try {
    const res = await fetch(COMPLETIONS_URL, {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
      // max_tokens is deliberately generous: reasoning models (mimo-v2.5)
      // spend completion tokens thinking before they emit any content, and a
      // tight cap makes a healthy model look broken.
      body: JSON.stringify({
        model,
        messages: [{ role: "user", content: "ping" }],
        max_tokens: 64,
      }),
      signal: AbortSignal.timeout(30_000),
    });
    const ms = Math.round(performance.now() - started);
    if (!res.ok) {
      const text = (await res.text()).slice(0, 300);
      return { ok: false, ms, error: `HTTP ${res.status}: ${text}` };
    }
    // A 200 can still carry an error envelope.
    const body = (await res.json()) as { error?: { message?: string } };
    if (body.error) return { ok: false, ms, error: body.error.message ?? "unknown error" };
    return { ok: true, ms };
  } catch (err) {
    return {
      ok: false,
      ms: Math.round(performance.now() - started),
      error: err instanceof Error ? err.message : "unknown error",
    };
  }
}

export async function checkChatHealth(): Promise<ChatHealth> {
  const checkedAt = new Date().toISOString();
  const apiKey = process.env.OPENROUTER_API_KEY;

  if (!apiKey) {
    return {
      status: "down",
      checkedAt,
      models: [],
      problems: ["OPENROUTER_API_KEY is not set — the chat dock cannot make any request."],
    };
  }

  const catalogue = await listedModels(apiKey);

  const targets: Array<{ model: string; role: "primary" | "fallback" }> = [
    { model: PRIMARY_MODEL, role: "primary" },
    { model: FALLBACK_MODEL, role: "fallback" },
  ];

  const models: ModelHealth[] = await Promise.all(
    targets.map(async ({ model, role }) => {
      const r = await probe(model, apiKey);
      return {
        model,
        role,
        // If the catalogue is unreachable we can't judge listing; assume listed
        // so a transient OpenRouter blip doesn't page us with a false deprecation.
        listed: catalogue ? catalogue.has(model) : true,
        responds: r.ok,
        latencyMs: r.ms,
        error: r.error,
      };
    }),
  );

  const problems: string[] = [];
  for (const m of models) {
    if (!m.responds) {
      problems.push(`${m.role} model ${m.model} is NOT responding — ${m.error ?? "unknown error"}`);
    }
    if (!m.listed) {
      problems.push(
        `${m.role} model ${m.model} is no longer in OpenRouter's catalogue — it has been deprecated and will stop working. Migrate it now.`,
      );
    }
  }

  const primary = models.find((m) => m.role === "primary");
  const fallback = models.find((m) => m.role === "fallback");
  const anyResponds = Boolean(primary?.responds || fallback?.responds);

  const status: ChatHealth["status"] = !anyResponds
    ? "down" // no model answers ⇒ the dock is broken for every visitor
    : problems.length > 0
      ? "degraded" // still serving, but something is failing or on death row
      : "healthy";

  return { status, checkedAt, models, problems };
}
