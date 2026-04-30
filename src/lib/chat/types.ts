export type ChatRole = "user" | "assistant" | "tool" | "system";

export type ToolCall = {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
};

export type ChatMessage = {
  id: string;
  role: ChatRole;
  content: string;
  toolCalls?: ToolCall[];
  toolCallId?: string;
  timestamp: number;
};

export type StoredConversation = {
  sessionId: string;
  startedAt: number;
  messages: ChatMessage[];
};

export type SSEEvent =
  | { type: "token"; content: string }
  | { type: "tool_call"; toolName: string; toolArgs: Record<string, unknown> }
  | { type: "tool_result"; toolName: string; ok: boolean; message: string }
  | { type: "done" }
  | { type: "error"; message: string };

export type ChatStatus = "idle" | "sending" | "streaming" | "error";
