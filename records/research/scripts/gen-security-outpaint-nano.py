"""Outpaint the approved 1024x1024 security still to native 16:9 using Nano Banana Pro.

Why: the previous PIL flat-paste extension created 84% pure white pixels in the
first_frame, which caused Seedance to drift/bounce the platform. Nano Banana
Pro extends the square with naturally rendered white/cream gradient — no flat
region for Seedance to misinterpret.

Input:  records/research/stills/security_scene_start.png  (clean 1024x1024 square)
Output: public/mascots/security_scene_start.png          (native 16:9, ~1792x1024)
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

PROMPT = """Take this 1024x1024 square image (a Pixar 3D scene with a snowy owl standing behind a chrome industrial platform, three small helper robots on top of the platform all facing the camera, white/cream background) and extend it into a WIDER 16:9 LANDSCAPE frame.

The existing content on the LEFT stays EXACTLY as it is — do NOT move, resize, or redraw the owl, the robots, the chrome platform, or anything on the left half of the image. Preserve every pixel of the existing scene. The owl + platform + robots cluster stays in the bottom-LEFT of the new wider frame.

Extend the image to the RIGHT by adding approximately 796 pixels of empty scene that continues the existing background naturally. Match the existing subtle warm-white lighting and gradient — the added area should look like a seamless continuation of the same studio environment, same color temperature, same ambient soft light. Do NOT introduce any new objects, characters, shadows, or details in the extended area. It should read as empty clean studio space — same background tone as the existing upper-right portion of the source image.

Critically: the added area must NOT be flat pure RGB(255,255,255) white. It should have the same natural rendered warm-white gradient with subtle ambient variation that the existing background has, so the final image reads as a single coherent studio render.

NEVER add a second owl, a ghost owl face, a secondary character, or any repeated elements in the extended area. Keep it empty."""

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

print("outpainting via Nano Banana Pro to native 16:9…", flush=True)
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
    print(f"NO_IMAGE in response; full message: {json.dumps(msg)[:800]}", flush=True); exit(1)

png_data_uri = images[0].get("image_url", {}).get("url", "")
if not png_data_uri.startswith("data:"):
    print(f"unexpected image_url format: {png_data_uri[:200]}", flush=True); exit(1)

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
