"""Composite 3 reference robots onto the security conveyor.

Input: section_security.png (owl alone at glass console) + robot_tinkerer.png
Output: security_with_robots.png — 3 identical helper robots hovering in a
line on the right portion of the belt (positions ~55%, 65%, 75% across the
frame), at mid-height just above the glass console's top edge. All three
clean (amber eye, cream body, gold band, blue thruster). They've just
"arrived from the right" and are about to drift leftward past the owl.
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

SCENE = to_data_uri(MASCOTS / "section_security.png")
ROBOT = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Take the first image (security scene: snowy owl behind a brushed-glass conveyor belt spanning the full width, BOTTOM-STRIP composition with empty upper cream for copy) and add THREE IDENTICAL helper robots from the second image into it.

Place the three robots in a horizontal line hovering just above the conveyor belt's top edge, on the RIGHT side of the owl. Positions across the frame: first robot at ~50%, second robot at ~65%, third robot at ~80%. Vertical position: each robot's body centered just above the belt's top edge (so the robots occupy roughly the lower-middle band of the frame — NOT in the upper empty cream zone). They face LEFT (toward the owl, the direction they are about to drift on the conveyor).

All three robots are IDENTICAL and match the second reference image EXACTLY: single large amber camera-lens eye, cream-white rounded body with gold accent band, two pincer arms held neutrally at their sides (no objects in their pincers), soft blue thruster glow beneath each body. Same scale — each robot's body is about the height of the owl's head. Evenly spaced, all clearly hovering (blue thruster glow visible beneath each).

Keep EVERYTHING ELSE from the first image identical: same owl pose (head turned to his right watching the robots), same glass conveyor belt spanning full width with its blue under-glow flow-line, same uniform warm cream background (#faf8f7), same lighting, same depth of field, and critically the same EMPTY UPPER 55% of the frame (pure cream, no characters or objects in the upper half). Premium Pixar 3D feature-film render. 16:9 landscape, 1792 by 1024."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": SCENE}},
    {"type": "image_url", "image_url": {"url": ROBOT}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("compositing 3 reference robots onto security conveyor…", flush=True)
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
(OUT / "security_with_robots.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {out_path}", flush=True)
