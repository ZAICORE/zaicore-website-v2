"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/cn";
import { assets, type MediaAsset } from "@/content/assets";

type Props = {
  assetId: string;
  className?: string;
  rounded?: string;
  aspect?: string;
  loop?: boolean;
  showStars?: boolean;
  showGrain?: boolean;
  /** Cover the slot with children overlay (for text over video). */
  overlay?: React.ReactNode;
  /**
   * When true, renders NOTHING (empty space) if the asset has no src.
   * Used for mascot slots, we don't want an ugly gradient block when
   * the real character image hasn't dropped in yet.
   */
  invisibleWhenEmpty?: boolean;
  /**
   * How the media fills its container. `cover` (default) crops to fill;
   * `contain` preserves the full subject. Use `contain` for mascots
   * standing in their own slot.
   */
  fit?: "cover" | "contain";
  /**
   * When true, skips the background fallback class so the media sits
   * directly on the parent background. Use for PNGs with baked-white backgrounds.
   */
  transparentContainer?: boolean;
  /**
   * CSS object-position for the media. "top" crops the bottom when the
   * container aspect is shorter than the media's native aspect.
   */
  objectPosition?: "top" | "center" | "bottom" | "left" | "right";
  /**
   * Render two stacked video elements staggered by half the duration so
   * one is always mid-playback while the other resets. Masks the
   * browser's subtle render artifact at loop restart.
   */
  seamlessLoop?: boolean;
};

const fallbackClass: Record<NonNullable<MediaAsset["fallback"]>, string> = {
  aurora: "fallback-aurora",
  lapis: "fallback-lapis",
  cream: "fallback-cream",
  signal: "fallback-signal",
};

export function MediaSlot({
  assetId,
  className,
  rounded = "rounded-[28px]",
  aspect = "aspect-[4/5]",
  loop = true,
  showStars = false,
  showGrain = true,
  overlay,
  invisibleWhenEmpty = false,
  fit = "cover",
  transparentContainer = false,
  objectPosition,
  seamlessLoop = false,
}: Props) {
  const objectPosClass = objectPosition ? `object-${objectPosition}` : "";
  const asset = assets[assetId];
  const [mediaReady, setMediaReady] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const videoRefB = useRef<HTMLVideoElement | null>(null);
  const [activeIdx, setActiveIdx] = useState(0);

  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    const onCanPlay = () => setMediaReady(true);
    v.addEventListener("canplay", onCanPlay);
    return () => v.removeEventListener("canplay", onCanPlay);
  }, []);

  // Seamless loop: stagger two videos. When primary hits duration-0.4s, start
  // secondary from 0 and fade it in; when primary ends, swap roles.
  useEffect(() => {
    if (!seamlessLoop) return;
    const a = videoRef.current;
    const b = videoRefB.current;
    if (!a || !b) return;
    const CROSSFADE = 0.12;
    let rafId: number;
    const tick = () => {
      const active = activeIdx === 0 ? a : b;
      const other = activeIdx === 0 ? b : a;
      if (active.duration && active.currentTime >= active.duration - CROSSFADE) {
        if (other.paused) {
          other.currentTime = 0;
          void other.play();
          setActiveIdx((i) => 1 - i);
        }
      }
      rafId = requestAnimationFrame(tick);
    };
    rafId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafId);
  }, [seamlessLoop, activeIdx]);

  if (!asset) {
    return (
      <div className={cn("fallback-cream", rounded, aspect, className)} aria-hidden />
    );
  }

  const hasSrc = asset.src && asset.src.length > 0;
  const fallback = asset.fallback ?? "cream";

  // If the asset has no src and we're asked to be invisible when empty, render
  // a space-holding but visually transparent div. Keeps layout stable.
  if (!hasSrc && invisibleWhenEmpty) {
    return <div className={cn(rounded, aspect, className)} aria-hidden />;
  }

  return (
    <div
      className={cn(
        "relative isolate overflow-hidden",
        !transparentContainer && fallbackClass[fallback],
        rounded,
        aspect,
        showGrain && "grain",
        showStars && "stars",
        className,
      )}
    >
      {hasSrc && asset.kind === "video" && !seamlessLoop && (
        <video
          ref={videoRef}
          src={asset.src}
          poster={asset.poster}
          autoPlay
          muted
          loop={loop}
          playsInline
          preload="auto"
          className={cn(
            "absolute inset-0 h-full w-full transition-opacity duration-700",
            fit === "cover" ? "object-cover" : "object-contain",
            objectPosClass,
            mediaReady ? "opacity-100" : "opacity-0",
          )}
        />
      )}
      {hasSrc && asset.kind === "video" && seamlessLoop && (
        <>
          <video
            ref={videoRef}
            src={asset.src}
            poster={asset.poster}
            autoPlay
            muted
            playsInline
            preload="auto"
            className={cn(
              "absolute inset-0 h-full w-full transition-opacity duration-[120ms] ease-linear",
              fit === "cover" ? "object-cover" : "object-contain",
              objectPosClass,
              !mediaReady ? "opacity-0" : activeIdx === 0 ? "opacity-100" : "opacity-0",
            )}
          />
          <video
            ref={videoRefB}
            src={asset.src}
            poster={asset.poster}
            muted
            playsInline
            preload="auto"
            className={cn(
              "absolute inset-0 h-full w-full transition-opacity duration-[120ms] ease-linear",
              fit === "cover" ? "object-cover" : "object-contain",
              objectPosClass,
              !mediaReady ? "opacity-0" : activeIdx === 1 ? "opacity-100" : "opacity-0",
            )}
          />
        </>
      )}
      {hasSrc && asset.kind === "image" && (
        <Image
          src={asset.src}
          alt={asset.alt ?? ""}
          fill
          priority
          className={cn(fit === "cover" ? "object-cover" : "object-contain", objectPosClass)}
          sizes="(max-width: 1024px) 100vw, 65vw"
        />
      )}
      {overlay && <div className="pointer-events-none absolute inset-0 z-10">{overlay}</div>}
    </div>
  );
}
