"""Fresh lean prompt for the engineering scene still. No constraint piling —
positive description only. One soldering iron, one smoke wisp, done.
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
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Match the provided fox character exactly. Premium Pixar 3D feature-film render. 1024x1024 square frame.

Setting: uniformly flat warm off-white studio (#faf8f7, RGB approximately 250/248/247). No walls, no floor, no other objects. Background color is PERFECTLY UNIFORM — no gradient, no warmer patches.

COMPOSITION — this image will be padded horizontally to a wider 16:9 canvas by adding cream on the RIGHT only. Therefore the panel MUST extend all the way from the LEFT edge of THIS 1024 image to about 65% across (x=665 of 1024), and the fox should be positioned at about 49% across THIS image (x=500 of 1024). That way when padded, the panel will reach the far left of the final canvas.

A tall solid wood panel (like a craftsman's workbench front wall, not a table with a visible top) extends horizontally across the lower portion of the frame. It rises from the bottom of the frame up to about 65% down from the top of the frame — a vertical wood panel, not a flat surface. The panel extends from the LEFT edge of this 1024 frame (reaching x=0, continuing off-screen to the left) all the way to about 65% across (x=665), where it has a clean finished right-end corner. The top horizontal edge of the panel is flat and clearly visible. Behind this panel (entirely hidden from the camera's view) is the fox's work surface — anything placed behind the panel's top edge is completely invisible to the viewer.

The fox stands or sits behind this wood panel, visible only from his chest up above the top edge of the panel. He is positioned at about 49% across this frame (center, around x=500 of 1024). He is SMALL in frame — the top of his ears reaches about 55% down from the top of the frame, leaving roughly half the frame empty warm off-white above him. He wears safety goggles over his eyes. One of his paws is visible just above the top edge of the panel, holding a slim chrome pencil-grip soldering iron angled downward (the tip of the iron descends behind the panel, hidden). A single thin wisp of smoke rises upward from just behind the panel's top edge into the empty space above. The fox looks down, focused on hidden work.

The fox is ALONE — no robot, no other figures. To the LEFT of the fox, along the top edge of the panel (roughly x=100 to x=420 across the 1024 frame), is open empty warm cream space above the panel — clear visible space where a robot could later fly in and hover at bench height.

The RIGHT 35% of this frame (from about x=670 to x=1024) is completely empty uniform cream — no panel, no objects, just clean cream.

The upper half of the frame is also mostly empty cream (above the fox's head).

Warm key light from the upper left. Shallow depth of field on the fox."""

content = [{"type": "text", "text": PROMPT}]
content.append({"type": "image_url", "image_url": {"url": FOX_REF}})

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("regen engineering still — lean prompt…", flush=True)
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
(OUT / "section_engineering_lean.png").write_bytes(png)
(MASCOTS / "section_engineering.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
