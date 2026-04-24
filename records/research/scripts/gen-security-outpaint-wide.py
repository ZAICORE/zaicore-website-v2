"""Outpaint the security composite to a wider 16:9 aspect ratio.
Continue the belt naturally on both sides so there's no stretching.
"""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

CURRENT = to_data_uri(MASCOTS / "security_with_robots.png")

PROMPT = """Extend this image horizontally into a WIDER 16:9 LANDSCAPE aspect ratio (wider than tall). The output MUST be landscape, not square — approximately 1792 wide by 1024 tall.

Add more image content on the LEFT and RIGHT sides: extend the brushed-glass conveyor belt (with its pale-blue under-glow flow-line) so it spans the ENTIRE WIDTH of the new wider frame — continuing seamlessly off both the LEFT and RIGHT edges. The added side sections must match the existing belt's glass material, color, and under-glow exactly. Cream background above the belt must match the existing warm cream and be uniform across the full width.

Keep the owl, the three helper robots, and all their sizes and positions EXACTLY as they are in the original — do not resize or move them. The goal is simply: make the scene wider with the belt continuing across."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": CURRENT}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("outpainting security composite to 16:9…", flush=True)
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
images = data["choices"][0]["message"].get("images", [])
if not images:
    print("NO_IMAGE", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
# Save directly as 16x9 — even if it came back square, we'll see
out_path = MASCOTS / "security_with_robots_16x9.png"
out_path.write_bytes(png)
# Check dimensions
from PIL import Image
import io
img = Image.open(io.BytesIO(png))
print(f"output dimensions: {img.size}")
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {out_path}", flush=True)
