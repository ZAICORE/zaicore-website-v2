"""Fix the top edge of the wood bench — make it perfectly level and crisp.

Takes the current 16:9 padded composite as input and asks gpt-image-2 to
clean up the bench top edge without changing anything else.
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

CURRENT = to_data_uri(MASCOTS / "engineering_with_robot_16x9.png")

PROMPT = """Edit this image. Preserve the 16:9 landscape aspect ratio (wider than tall — DO NOT crop to square). Keep the fox, the helper robot, their positions, their sizes, the lighting, the warm cream background, and the overall composition EXACTLY the same.

The ONLY change: fix the top edge of the wood workbench panel. Currently the top edge looks slightly rough, wavy, and uneven. Redraw the top edge so it is a PERFECTLY STRAIGHT, LEVEL, CRISP horizontal line running from the LEFT edge of the frame all the way to the panel's right-end corner. The panel must look like a professionally crafted flat wood workbench — clean 90-degree corner at the right end, razor-straight top, no lumpiness, no dips, no waviness. The wood grain of the panel stays the same. The panel's height (its top edge y-position) stays approximately the same.

Everything else stays identical. No other changes."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": CURRENT}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("fixing bench top edge…", flush=True)
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
out_path = MASCOTS / "engineering_with_robot_16x9.png"
out_path.write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {out_path}", flush=True)
