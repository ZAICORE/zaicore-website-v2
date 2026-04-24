"""Send approved 1024x1024 square to Nano Banana Pro — RESIZE ONLY.

DO NOT redraw. DO NOT regenerate. DO NOT modify any existing content.
Only extend the background to the right to turn the square into a 16:9
landscape frame. Match the existing background tone exactly — continue
the natural studio gradient the source already has.
"""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

STILLS_BACKUP = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))
MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

SRC = to_data_uri(STILLS_BACKUP / "security_scene_start.png")

PROMPT = """This is an approved final image. Your ONLY task is to change its aspect ratio from 1:1 square to 16:9 landscape by extending the background to the right.

STRICT PRESERVATION RULES — these are NON-NEGOTIABLE:
1. DO NOT redraw the owl. Keep the owl pixel-for-pixel identical to the input.
2. DO NOT redraw the three robots. Keep them pixel-for-pixel identical.
3. DO NOT redraw the chrome conveyor belt / platform. Keep it pixel-for-pixel identical.
4. DO NOT move, resize, shift, or reposition any existing element.
5. DO NOT change the lighting, color grading, or style of any existing pixel.
6. The entire existing 1:1 image appears UNCHANGED on the LEFT side of the new 16:9 frame.

WHAT YOU ARE ADDING — the RIGHT SIDE of the new wider frame:
- Extend the existing subtle warm-white studio background seamlessly rightward.
- The added area is EMPTY studio space — NO new objects, NO characters, NO shadows, NO text, NO details, NO secondary owl, NO ghost faces, nothing at all.
- The added area continues the gentle ambient gradient the source image already has in its upper-right corner — same color, same tone, same soft lighting falloff. It must look like a natural continuation of the same studio environment.
- The added area must NOT be flat pure RGB(255,255,255). It should have the same subtle rendered gradient the source background has.

Output: a 16:9 landscape frame. The source square becomes the LEFT portion of the output. The RIGHT portion is empty studio background matching the source."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": SRC}},
]

body = {
    "model": "google/gemini-3-pro-image-preview",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
    "image_config": {
        "aspect_ratio": "16:9",
        "image_size": "2K",
    },
}

print("Nano Banana Pro — resize only, preserve everything…", flush=True)
t0 = time.time()
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
r = urllib.request.urlopen(req, timeout=420)
data = json.load(r)
if "error" in data:
    print(f"ERROR: {data['error']}", flush=True); exit(1)

msg = data["choices"][0]["message"]
images = msg.get("images", [])
if not images:
    print(f"NO_IMAGE; msg: {json.dumps(msg)[:800]}", flush=True); exit(1)

png_data_uri = images[0].get("image_url", {}).get("url", "")
png = base64.b64decode(png_data_uri.split(",", 1)[1])
out_path = MASCOTS / "security_scene_start.png"
out_path.write_bytes(png)
(STILLS_BACKUP / "security_scene_start_16x9.png").write_bytes(png)

from PIL import Image
import io
img = Image.open(io.BytesIO(png))
print(f"output: {img.size[0]}x{img.size[1]}")
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost})", flush=True)
print(f"saved to: {out_path}", flush=True)
