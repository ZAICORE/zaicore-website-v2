"use client";

import type { StoredConversation, ChatMessage } from "./types";

const KEY = "zaicore_chat_v1";
const MAX_MESSAGES = 50;

export function loadConversation(): StoredConversation | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as StoredConversation;
    if (!parsed.sessionId || !Array.isArray(parsed.messages)) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function saveConversation(conv: StoredConversation): void {
  if (typeof window === "undefined") return;
  const trimmed: StoredConversation = {
    ...conv,
    messages: conv.messages.slice(-MAX_MESSAGES),
  };
  try {
    window.localStorage.setItem(KEY, JSON.stringify(trimmed));
  } catch {
    // quota exceeded or storage disabled -- fail silently
  }
}

export function clearConversation(): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.removeItem(KEY);
  } catch {
    // ignore
  }
}

export function newConversation(): StoredConversation {
  return {
    sessionId: crypto.randomUUID(),
    startedAt: Date.now(),
    messages: [],
  };
}

export function appendMessage(
  conv: StoredConversation,
  msg: ChatMessage,
): StoredConversation {
  return { ...conv, messages: [...conv.messages, msg] };
}

export function updateLastAssistantMessage(
  conv: StoredConversation,
  patch: (m: ChatMessage) => ChatMessage,
): StoredConversation {
  const idx = conv.messages.length - 1;
  if (idx < 0 || conv.messages[idx].role !== "assistant") return conv;
  const updated = [...conv.messages];
  updated[idx] = patch(updated[idx]!);
  return { ...conv, messages: updated };
}
