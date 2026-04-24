"""Composite the reference robot into the engineering scene still.

Input: section_engineering.png (fox alone at wood panel) + robot_tinkerer.png
Output: engineering_with_robot.png — fox at panel + reference robot hovering to
the LEFT of the fox, holding a small brass gear in its pincer. Matches the
rest of the scene lighting/style.
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

SCENE = to_data_uri(MASCOTS / "section_engineering.png")
ROBOT = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Take the first image (the engineering scene: fox in safety goggles behind a tall wood workbench panel, soldering iron in paw with a thin smoke wisp, warm off-white studio background, 1024x1024 frame) and add the helper robot from the second image into it.

Place the robot to the LEFT of the fox, hovering in the empty space above the wood panel's top edge, around x=300 across the 1024 frame (so roughly 30% across). Vertical center around 45% from top. Match the robot's design to the second reference image EXACTLY: single large amber camera-lens eye, cream-white rounded body with gold accent band, two pincer arms, soft blue thruster glow beneath. Same scale relative to the fox — the robot's body is about the height of the fox's head.

The robot holds a small brass gear in its right pincer, extended slightly toward the fox as if offering it. The robot is clearly airborne — blue thruster glow visible under its body.

Keep EVERYTHING ELSE from the first image identical: same fox pose, same wood panel (extending from the LEFT edge of the frame all the way across to its right-end corner at ~65% across), same smoke wisp, same warm off-white background, same lighting and depth of field. 1024x1024 square frame. Premium Pixar 3D feature-film render."""

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

print("compositing reference robot into engineering scene…", flush=True)
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
out_path = MASCOTS / "engineering_with_robot.png"
out_path.write_bytes(png)
(OUT / "engineering_with_robot.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {out_path}", flush=True)
