/**
 * Asset registry. Swap URIs here to change media anywhere in the site.
 * `src` can be a local path (starts with /) or a remote URL.
 * `fallback` renders if `src` is empty or fails — a gradient type or poster image.
 */
export type MediaAsset = {
  id: string;
  kind: "video" | "image";
  src: string;
  poster?: string;
  alt?: string;
  fallback?: "aurora" | "lapis" | "cream" | "signal";
};

export const assets: Record<string, MediaAsset> = {
  heroMedia: {
    id: "heroMedia",
    kind: "video",
    src: "",
    poster: "",
    alt: "ZAICORE hero",
    fallback: "aurora",
  },
  engineeringShowreel: {
    id: "engineeringShowreel",
    kind: "video",
    src: "",
    fallback: "lapis",
  },
  securityProduct: {
    id: "securityProduct",
    kind: "image",
    src: "",
    alt: "ZAICORE Security briefing preview",
    fallback: "signal",
  },
  mascotEngineer: {
    id: "mascotEngineer",
    kind: "image",
    src: "",
    alt: "Eli — engineering mascot",
    fallback: "cream",
  },
  mascotSentinel: {
    id: "mascotSentinel",
    kind: "image",
    src: "",
    alt: "Vela — security mascot",
    fallback: "lapis",
  },
};
