/**
 * Mascot registry. Two characters, same artistic rules:
 * quiet, Pixar-adjacent, cream palette, thoughtful more than cute.
 * Each is a Seedance loop with a transparent (blend-mode: darken) background.
 *
 * Swap mediaId in assets.ts to change the actual video once generated.
 */
export type Mascot = {
  id: string;
  name: string;
  role: string;
  mediaId: string;
  description: string;
};

export const mascots: Record<string, Mascot> = {
  engineer: {
    id: "engineer",
    name: "Eli",
    role: "Engineering mascot",
    mediaId: "mascotEngineer",
    description:
      "A small figure in a cream jumper with a builder's apron, soldering iron in hand, tinkering at a workbench. Pixar-adjacent, warm, patient.",
  },
  sentinel: {
    id: "sentinel",
    name: "Vela",
    role: "Security mascot",
    mediaId: "mascotSentinel",
    description:
      "A lighthouse keeper in a deep blue coat, calmly scanning the horizon with a small brass telescope. Pixar-adjacent, watchful, unhurried.",
  },
};
