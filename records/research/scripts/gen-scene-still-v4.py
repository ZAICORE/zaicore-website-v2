"""Regen scene_still with ZAICORE wordmark on the back wall.

Uses zaicore_wordmark.png as input_reference alongside fox + owl.
Fox far left, owl far right, huge empty middle, ZAICORE wordmark clean
and legible on the seamless white back wall behind them.
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
LOGO_REF = to_data_uri(MASCOTS / "zaicore_wordmark.png")

PROMPT = """Wide cinematic composition in classic 3D animated film style, 16:9 landscape aspect ratio. Pure white seamless studio — white floor, white background — with soft floor shadows.

BACK WALL SIGNAGE: The word ZAICORE appears LARGE and CLEANLY on the back wall of the seamless studio, centered horizontally, positioned in the upper center of the frame. The wordmark matches the provided logo reference EXACTLY — bold geometric sans-serif letters, high contrast, crisp edges, confident proportions. Render it as CLEAN DARK CHARCOAL PAINTED LETTERING on the white wall, sharp and unambiguous (not etched, not 3D extruded — just bold flat lettering painted cleanly onto the wall). The lettering is large enough to be easily legible — roughly 12 percent of the total image height.

COMPOSITION:
- FAR LEFT 20 PERCENT: the fox character sits here. Left edge of fox body is ~5% from the left edge of frame. Fox occupies the left 20% of frame width.
- FAR RIGHT 20 PERCENT: the owl character stands here. Right edge of owl body is ~5% from the right edge of frame. Owl occupies the right 20% of frame width.
- MIDDLE 60 PERCENT: empty white space. The ZAICORE wordmark is visible on the back wall here.

SCALE: fox and owl each occupy roughly the BOTTOM HALF of the frame vertically. Characters are small-scale relative to the frame — each roughly 40-45% of frame height. Plenty of empty space above each character's head.

LEFT CHARACTER — the fox (match provided fox reference exactly):
- Young fox with warm russet fur, clear protective safety goggles DOWN OVER ITS EYES.
- Sits cross-legged on the white floor, body facing three-quarters toward the right.
- One paw holds a small chrome soldering iron with a thin wisp of curling smoke.
- Other paw rests on a small green circuit board in its lap.
- Focused, looking down at work.
- Positioned in the LEFT 20% of the frame.

RIGHT CHARACTER — the snowy owl (match provided owl reference exactly):
- Snowy owl with pristine white feathers and warm yellow eyes, standing directly on the white floor.
- In front of the owl: a small open silver aluminum laptop — brushed metal, COMPLETELY UNBRANDED (no logos, no markings). Back lid faces viewer (plain silver), screen faces the owl.
- Owl bends slightly forward, one talon tapping a key, other talon on floor.
- Focused, head tilted down toward screen, body facing three-quarters toward the left.
- Positioned in the RIGHT 20% of the frame.

LIGHTING: Warm key light from upper right, cool fill from upper left. Soft grounded floor shadows under each character. The back wall is evenly lit so the ZAICORE wordmark reads clearly.

CAMERA: Locked static eye-level wide shot. Characters are small subjects with massive negative space (and the wordmark) between them.

STYLE: Premium 3D animated feature-film quality. Soft subsurface scattering on fur and feathers. Warm cinematic palette. Pure white seamless studio — no gradients, no textures beyond the wordmark on back wall.

Image dimensions: 1792 wide by 1024 tall.

CRITICAL:
- The ONLY text anywhere in the image is the word ZAICORE on the back wall. No other text, no labels, no numerals, no words anywhere.
- The laptop has NO logo, NO brand mark, NO symbols — plain silver metal.
- Fox stays strictly in the LEFT 20% of frame width. Owl stays strictly in the RIGHT 20% of frame width.
- ZAICORE wordmark must be LEGIBLE and crisp — matching the geometric sans style of the provided logo reference.
- No other characters, no robot visible in this scene — just fox and owl and the ZAICORE back-wall signage."""

content = [{"type": "text", "text": PROMPT}]
content.append({"type": "image_url", "image_url": {"url": LOGO_REF}})
content.append({"type": "image_url", "image_url": {"url": FOX_REF}})
content.append({"type": "image_url", "image_url": {"url": OWL_REF}})

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("regen scene_still v4 — fox + owl + ZAICORE wordmark on back wall…", flush=True)
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
(OUT / "scene_still_v4.png").write_bytes(png)
(MASCOTS / "scene_still.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to {MASCOTS / 'scene_still.png'}", flush=True)
