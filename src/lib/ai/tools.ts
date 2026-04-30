import { sendBookingEmail } from "@/lib/email";
import type { ChatMessage } from "@/lib/chat/types";

export type ToolDefinition = {
  type: "function";
  function: {
    name: string;
    description: string;
    parameters: Record<string, unknown>;
  };
};

export const TOOLS: ToolDefinition[] = [
  {
    type: "function",
    function: {
      name: "submit_booking",
      description:
        "Submit a booking request to schedule a call with Zach. Only call this AFTER you've collected the required fields from the user.",
      parameters: {
        type: "object",
        required: ["name", "email", "workingOn"],
        properties: {
          name: { type: "string", description: "Full name", maxLength: 120 },
          email: { type: "string", description: "Email address", maxLength: 254 },
          company: { type: "string", description: "Optional company name", maxLength: 160 },
          workingOn: {
            type: "string",
            description: "What the user is working on or wants help with",
            maxLength: 4000,
          },
          timeline: {
            type: "string",
            description: "Optional timeline (e.g., 'starting next month')",
            maxLength: 160,
          },
        },
      },
    },
  },
];

export type SubmitBookingArgs = {
  name: string;
  email: string;
  workingOn: string;
  company?: string;
  timeline?: string;
};

export type ToolResult = {
  ok: boolean;
  message: string;
};

function formatTranscript(messages: ChatMessage[]): string {
  return messages
    .filter((m) => m.role === "user" || m.role === "assistant")
    .map((m) => `${m.role === "user" ? "User" : "ZAICORE"}: ${m.content.trim()}`)
    .join("\n\n");
}

export async function executeTool(
  name: string,
  args: unknown,
  conversation: ChatMessage[],
): Promise<ToolResult> {
  if (name !== "submit_booking") {
    return { ok: false, message: `Unknown tool: ${name}` };
  }

  const a = args as Partial<SubmitBookingArgs>;
  if (!a.name || !a.email || !a.workingOn) {
    return {
      ok: false,
      message: "Missing required fields. Need name, email, and what they're working on.",
    };
  }

  // I3: validate email format before handing to Resend
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(a.email)) {
    return {
      ok: false,
      message: "Email format invalid. Ask the user to provide a real email.",
    };
  }

  const transcript = formatTranscript(conversation);
  const workingOnWithTranscript = `${a.workingOn}\n\n---\nConversation transcript:\n${transcript}`;

  const result = await sendBookingEmail({
    name: a.name,
    email: a.email,
    company: a.company,
    workingOn: workingOnWithTranscript,
    timeline: a.timeline,
  });

  if (!result.ok) {
    return {
      ok: false,
      message: `Booking failed: ${result.reason ?? "unknown error"}. Tell the user to try again or email zachary@zaicore.com directly.`,
    };
  }
  return {
    ok: true,
    message:
      "Booking submitted successfully. Tell the user Zach will reply within 24 hours and confirm what they should expect.",
  };
}
