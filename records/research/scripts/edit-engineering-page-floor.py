"""Edit engineering page still — replace wooden floor with cream studio floor."""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
STILLS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))

def to_data_uri(p): return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

SRC = to_data_uri(MASCOTS / "engineering_page_start.png")

PROMPT = """Edit this image. Keep EVERYTHING else pixel-identical:
- The fox stays exactly as he is — same pose, same goggles, same expression, same fur, same paw position.
- The helper robot stays exactly as it is — same panel, same open circuit board, same body, same color.
- The wooden stool the fox is sitting on stays exactly as it is.
- The fox's tail, paws, and body proportions remain unchanged.
- The screwdriver / tool in his paw stays exactly as it is.

ONLY CHANGE: at the very bottom of the frame, the strip of WOODEN FLOOR / WOODEN PLANKS visible under the stool should be REPLACED with the same warm cream studio background that fills the rest of the frame. The floor area should now blend seamlessly with the cream gradient background — no wooden grain, no plank lines, no floor texture. Just clean cream studio matching the upper portion of the frame.

The rest of the image is UNCHANGED."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": SRC}},
]

body = {
    "model": "google/gemini-3-pro-image-preview",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
    "image_config": {"aspect_ratio": "9:16", "image_size": "2K"},
}

print("Nano Banana Pro — floor edit…", flush=True)
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
    print(f"NO_IMAGE; msg: {json.dumps(msg)[:600]}", flush=True); exit(1)

png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
out_path = MASCOTS / "engineering_page_start.png"
out_path.write_bytes(png)
(STILLS / "engineering_page_start.png").write_bytes(png)

from PIL import Image
import io
img = Image.open(io.BytesIO(png))
print(f"output: {img.size[0]}x{img.size[1]}")
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost})", flush=True)
