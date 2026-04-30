/**
 * Asset registry. Swap URIs here to change media anywhere in the site.
 * `src` can be a local path (starts with /) or a remote URL.
 * `fallback` renders if `src` is empty or fails. A gradient type or poster image.
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
    src: "/mascots/hero_scene.mp4",
    poster: "/mascots/scene_still.png",
    alt: "ZAICORE hero scene: fox soldering, owl at laptop, helper robot",
    fallback: "cream",
  },
  engineeringShowreel: {
    id: "engineeringShowreel",
    kind: "video",
    src: "/mascots/engineering_scene.mp4",
    poster: "/mascots/engineering_with_robot_16x9.png",
    alt: "Fox at workbench soldering, helper robots bringing parts",
    fallback: "cream",
  },
  securityProduct: {
    id: "securityProduct",
    kind: "image",
    src: "",
    alt: "ZAICORE Security briefing preview",
    fallback: "signal",
  },
  securityShowreel: {
    id: "securityShowreel",
    kind: "video",
    src: "/mascots/security_scene.mp4",
    poster: "/mascots/security_scene_start.png",
    alt: "Owl monitoring a conveyor of helper robots, catches the infected one",
    fallback: "cream",
  },
  mascotEngineer: {
    id: "mascotEngineer",
    kind: "image",
    src: "/mascots/fox.png",
    alt: "ZAICORE engineering mascot",
    fallback: "cream",
  },
  mascotSentinel: {
    id: "mascotSentinel",
    kind: "image",
    src: "/mascots/owl.png",
    alt: "ZAICORE security mascot",
    fallback: "cream",
  },
};
