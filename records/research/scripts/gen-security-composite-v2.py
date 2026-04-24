"""Fix the security composite — owl's head turned right to watch the robots,
pure site-cream background (#faf8f7) so there's no color seam when embedded.

Takes the current composite as the primary input and tells gpt-image to edit
it: rotate the owl's head to the right, match the background to the site.
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

CURRENT = to_data_uri(MASCOTS / "security_with_robots.png")
OWL_REF = to_data_uri(MASCOTS / "owl_typing.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Edit the first image (current security scene: snowy owl standing behind a brushed-glass console, three identical helper robots hovering in a line on the right side of the belt). Make TWO precise changes:

1. TURN THE OWL'S HEAD TO FACE THE ROBOTS. The owl's head should rotate to his right (camera-left of his body → camera-right in frame) so his eyes are clearly locked onto the three robots. His body stays in the same position and pose; only his head and gaze rotate. He should look alert, intent, watchful — visibly tracking the robots. Match the owl reference (second image) for character fidelity.

2. CHANGE THE BACKGROUND to pure site cream (#faf8f7 — a warm off-white, RGB approximately 250/248/247). The background above and around the console must be UNIFORMLY this cream — no gradient, no warmer patches, no tonal shifts. The glass console keeps its subtle pale-blue under-glow flow-line. Everything else stays identical.

Keep the three robots EXACTLY as they are — same positions, same design (single large amber camera-lens eye, cream body, gold accent band, pincer arms at sides, soft blue thruster glow beneath each), all matching the third reference image. Don't change their count, spacing, or poses.

Keep the same owl character design, same glass console with blue under-glow, same framing, same lighting, same shallow depth of field. Premium Pixar 3D feature-film render. 16:9 landscape-ish."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": CURRENT}},
    {"type": "image_url", "image_url": {"url": OWL_REF}},
    {"type": "image_url", "image_url": {"url": ROBOT_REF}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("regen security composite — fix owl gaze + background…", flush=True)
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
(OUT / "security_with_robots_v2.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {out_path}", flush=True)
