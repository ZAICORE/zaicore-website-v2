"""Take current security composite and rescale EVERYTHING smaller via gpt-image-2.

Input: security_with_robots.png (1024x1024 — the composite source).
Output: same file, but with owl + robots + belt all scaled down with more
cream breathing room around the composition.
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

PROMPT = """Edit this image. Keep the composition IDENTICAL: same owl, same three identical robots in a line on the brushed-glass conveyor, same cream background, same lighting. ONE change: make EVERYTHING (owl + all three robots + conveyor) proportionally SMALLER in the frame — about 70% of its current size — so there is MORE empty cream space around and above the characters. The owl and robots must keep identical proportions to each other; shrink as a group uniformly. Keep the cream background color the same. Same 1024x1024 frame size. Premium Pixar 3D render."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": CURRENT}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("shrinking security composite via gpt-image…", flush=True)
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
out_path = MASCOTS / "security_with_robots.png"
out_path.write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {out_path}", flush=True)
