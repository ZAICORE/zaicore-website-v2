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
}: Props) {
  const asset = assets[assetId];
  const [mediaReady, setMediaReady] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    const onCanPlay = () => setMediaReady(true);
    v.addEventListener("canplay", onCanPlay);
    return () => v.removeEventListener("canplay", onCanPlay);
  }, []);

  if (!asset) {
    return (
      <div className={cn("fallback-cream", rounded, aspect, className)} aria-hidden />
    );
  }

  const hasSrc = asset.src && asset.src.length > 0;
  const fallback = asset.fallback ?? "cream";

  return (
    <div
      className={cn(
        "relative isolate overflow-hidden",
        fallbackClass[fallback],
        rounded,
        aspect,
        showGrain && "grain",
        showStars && "stars",
        className,
      )}
    >
      {hasSrc && asset.kind === "video" && (
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
            "absolute inset-0 h-full w-full object-cover transition-opacity duration-700",
            mediaReady ? "opacity-100" : "opacity-0",
          )}
        />
      )}
      {hasSrc && asset.kind === "image" && (
        <Image
          src={asset.src}
          alt={asset.alt ?? ""}
          fill
          priority
          className="object-cover"
          sizes="(max-width: 1024px) 100vw, 65vw"
        />
      )}
      {overlay && <div className="pointer-events-none absolute inset-0 z-10">{overlay}</div>}
    </div>
  );
}
