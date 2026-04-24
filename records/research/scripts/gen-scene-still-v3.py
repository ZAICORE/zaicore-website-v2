"""Regen scene_still.png — fox FAR LEFT, owl FAR RIGHT, HUGE empty middle.

Problem with v2: characters too close together, no room for ZAICORE text + robot between them.

v3: characters pushed to the OUTER EDGES (~15% margins each side), SMALLER in frame
(take up bottom half only), leaving a tall empty middle column of ~70% width for:
  - ZAICORE wordmark overlay (center-vertical)
  - Robot rising from bottom center to touch the text
"""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))
OUT.mkdir(parents=True, exist_ok=True)

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

FOX_REF = to_data_uri(MASCOTS / "fox_soldering.png")
OWL_REF = to_data_uri(MASCOTS / "owl_typing.png")

PROMPT = """Wide cinematic composition in classic 3D animated film style, 16:9 landscape aspect ratio. Pure white seamless studio — white floor, white background — with soft floor shadows.

COMPOSITION (critical — characters must be pushed to the outer edges):
- Horizontal layout: the image is divided into three zones.
- FAR LEFT 20 PERCENT: the fox character sits here. Left edge of fox body touches the 5% margin from the left edge of frame. Fox occupies roughly the LEFT 20% of frame width.
- FAR RIGHT 20 PERCENT: the owl character stands here. Right edge of owl body touches the 5% margin from the right edge of frame. Owl occupies roughly the RIGHT 20% of frame width.
- MIDDLE 60 PERCENT: COMPLETELY EMPTY WHITE SPACE. No characters, no objects, no text. This is a vast empty center zone.

SCALE (critical — characters must be small, occupying only the bottom half):
- Fox and owl each occupy roughly the BOTTOM HALF of the frame vertically. The top half of the frame is empty white space above them.
- Characters are small relative to the frame — each roughly 40-45% of the frame height. Plenty of empty space above each character's head.

LEFT CHARACTER — the fox (match the provided fox reference exactly):
- Young fox with warm russet fur, wearing clear protective safety goggles DOWN OVER ITS EYES (actively worn, covering the eyes).
- Sits cross-legged on the white floor, body facing three-quarters toward the right (toward the empty center).
- One paw holds a small chrome soldering iron with a thin wisp of curling smoke.
- Other paw rests on a small green circuit board in its lap.
- Focused, looking down at work.
- Positioned in the LEFT 20% of the frame.

RIGHT CHARACTER — the snowy owl (match the provided owl reference exactly):
- Snowy owl with pristine white feathers and warm yellow eyes, standing directly on the white floor (no perch).
- In front of the owl sits a small open silver aluminum laptop — smooth brushed metal, COMPLETELY UNBRANDED with no logos, no markings, no symbols on any surface. The laptop back lid (plain silver metal, no logo) faces the viewer; the screen faces the owl.
- Owl bends slightly forward, one talon lifted and tapping a key on the keyboard, other talon on the floor.
- Focused, head tilted down toward the screen, body facing three-quarters toward the left (toward the empty center).
- Positioned in the RIGHT 20% of the frame.

LIGHTING: Warm key light from upper right, cool fill from upper left. Soft grounded floor shadows under each character. Shallow depth of field, film-grade.

CAMERA: Locked static eye-level wide shot. The characters are small subjects with massive negative space between them.

STYLE: Premium 3D animated feature-film quality. Soft subsurface scattering on fur and feathers. Warm cinematic palette. Pure white seamless studio — no gradients, no textures on background or floor.

Image dimensions: 1792 wide by 1024 tall (close to 16:9 landscape — wide horizontal).

CRITICAL CONSTRAINTS:
- The middle 60% of the frame is PURE EMPTY WHITE SPACE. No text, no objects, no shadows beyond the characters' own floor shadows.
- Fox stays strictly in the LEFT 20% of frame width. Owl stays strictly in the RIGHT 20% of frame width.
- Characters are SMALL — they must not dominate the frame. Plenty of empty white above each character's head.
- Laptop has NO logo, NO brand mark, NO symbols. Plain silver metal on every surface.
- No other characters, no robot visible in this scene. Just fox and owl."""

content = [{"type": "text", "text": PROMPT}]
content.append({"type": "image_url", "image_url": {"url": FOX_REF}})
content.append({"type": "image_url", "image_url": {"url": OWL_REF}})

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("regen scene_still v3 — wider spacing, smaller characters, huge empty middle…", flush=True)
t0 = time.time()
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
r = urllib.request.urlopen(req, timeout=300)
data = json.load(r)
if "error" in data:
    print(f"API_ERROR: {data['error']}", flush=True); exit(1)
images = data["choices"][0]["message"].get("images", [])
if not images:
    print("NO_IMAGE returned", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
(OUT / "scene_still_v3.png").write_bytes(png)
(MASCOTS / "scene_still.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to {MASCOTS / 'scene_still.png'}", flush=True)
