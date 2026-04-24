# Owl Security Scene — Design Spec

**Date:** 2026-04-24
**Status:** approved, pre-implementation
**Target:** `/mascots/security_scene.mp4` (replaces current broken version)

## Problem

Previous attempts at the security scene video failed because the compositor (`gpt-image-2`) kept rendering the helper robot with tripod legs standing on a glass table — ignoring the thruster-only design in `robot_tinkerer.png`. The "conveyor belt" also rendered as a featureless glass slab with no visible belt surface, leaving Seedance 2.0 nothing to lock onto and causing it to invent random geometry in frames away from first/last.

## Pipeline

Two steps. No composite hybrids, no PIL tricks.

1. **`gpt-image-2`** (OpenRouter `openai/gpt-5.4-image-2`) generates the start still — one prompt, one call, full scene with owl + 3 robots + conveyor belt. Native output 1792×1024 (16:9).
2. **Seedance 2.0** (OpenRouter `bytedance/seedance-2.0`) animates it. Same still passed as both `first_frame` and `last_frame` to enforce the loop close. `input_references` carries `owl_typing.png` + `robot_tinkerer.png` for identity consistency.

If the start still has too much dead cream on top and Seedance can't "see" the whole belt clearly, crop the top band before handoff to Seedance.

## Start still composition

**Mirrors the engineering scene composition** (`engineering_with_robot_16x9.png`): bottom-left character cluster, upper-right cream copy space.

- 16:9 aspect, 1792×1024.
- **Conveyor belt**: runs LEFT-to-RIGHT across the bottom-LEFT ~55% of the frame. Slight downward camera angle so the belt's top surface is visible (matching how the engineering bench's top is visible). Brushed chrome sides, glass/transparent top with visible belt-surface texture (rubber conveyor lines running along its length), thin blue under-light bar glowing beneath — clearly a working industrial conveyor, not a flat table. The belt itself does not appear to be moving (stationary inspection platform); the blue glow is ambient, not directional flow.
- **Three identical robots**: hovering on the belt, evenly spaced, all facing the camera directly (big amber camera-lens eyes looking at viewer). Exact clones of `robot_tinkerer.png` — single amber eye, cream-white body with gold accent band, two pincer arms at sides, **blue thruster flame visible below each body, NO legs, NO feet**. Each robot ~same height as the owl's chest-to-head span.
- **Owl**: snowy owl, bipedal Pixar-style, standing behind the belt, slightly left-of-center behind the trio of robots. Head + upper body clearly visible above and behind the robots. Watching over them like a security guard behind a lineup. Identity matches `owl_typing.png` (no laptop in frame).
- **Background**: uniform warm cream (#faf8f7). No secondary objects, no ghost faces, no second characters. Pure cream in the upper-right 40–45% of the frame for copy overlay.
- **Render style**: Pixar 3D feature-film quality, matching the hero and engineering scenes. Soft key light from upper-front, subtle ambient.

**Hard negatives** (in prompt): robots have NO legs, NO feet, NO articulated limbs below the body. Body is suspended in mid-air by a single blue thruster flame only. The belt is a conveyor, not a table.

## Video narrative (10s, Seedance prompt)

Camera is static — no pan, zoom, or dolly. Belt stays in-frame every single frame.

- **0–2s**: Three robots hover stationary on the belt, facing camera. Owl behind, head scanning left-to-right over them.
- **2–4s**: **Rightmost** robot's eye flashes red (malfunction/compromise signal). Owl's head tilts curiously. Owl's right wing extends forward over the belt, scoops the red-eyed robot up in the curve of the wing feathers (wing grab — not talon, not beak), and flicks it backward over his shoulder. It spirals into the deep background and detonates in a stylized cream puff cloud (not fire).
- **4–7s**: The remaining two robots' thrusters flare brighter. They lift off the belt and fly off the **right edge** of the frame, one after another.
- **7–10s**: Owl's head tracks them rightward as they exit, then turns back LEFT. Three fresh identical robots fly in from off-screen LEFT, bank around, and settle onto the belt in the original positions facing camera. Frame 10s = frame 0s exactly.

## Sizing and loop

- `gpt-image-2` native output: 1792×1024 (16:9).
- Seedance 2.0 request: `aspect_ratio: "16:9"`, `resolution: "1080p"`, `duration: 10`.
- Same still as `first_frame` AND `last_frame` — pixel-locks start and end state.
- `input_references`: `owl_typing.png` (identity only — laptop will not appear because the scene prompt does not include it), `robot_tinkerer.png` (identity + thruster design).
- Generate with `loop: true` at the MediaSlot level as usual.

## Reference assets used

- `public/mascots/owl_typing.png` — owl identity reference (laptop ignored by prompt)
- `public/mascots/robot_tinkerer.png` — robot identity reference (thruster, no legs)

## Outputs

- **New still**: `public/mascots/security_scene_start.png` (becomes the new 16:9 poster + Seedance first/last frame)
- **New video**: `public/mascots/security_scene.mp4` (overwrites current, used by `securityShowreel` asset)

No other files change. `src/content/assets.ts` already points `securityShowreel` → `/mascots/security_scene.mp4`.

## Success criteria

- Robots have **no legs**. Thruster flame visible under each. Hovering, not standing.
- Conveyor belt is visibly a conveyor, not a table or glass slab.
- Owl clearly stands behind the belt, visible above the robots.
- Loop closes seamlessly — frame 10s identical to frame 0s.
- Three-beat narrative (scan → catch bad one → clear the rest → new wave) reads clearly in one viewing.
- Scene matches engineering scene's visual language (bottom-left composition, cream upper-right, Pixar 3D).

## Out of scope

- No redesign of the SecuritySection layout. Current copy-overlay-on-cream-upper remains.
- No new character references. `owl_typing.png` and `robot_tinkerer.png` are used as-is.
- No PIL/compositing, no inpainting, no mask work. One image call, one video call.
