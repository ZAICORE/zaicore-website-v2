"""Extend the engineering workbench leftward naturally via gpt-image-2.

Takes the current 16:9 composite and asks the model to continue the wood panel
seamlessly off the left edge of the frame, preserving everything else.
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

PROMPT = """Edit this 16:9 image. You MUST preserve the 16:9 aspect ratio (wider than tall — DO NOT output a square). DO NOT move or resize anything. Keep the fox, the robot, their sizes, and their positions EXACTLY where they are.

The ONLY change: in the empty cream area to the LEFT of the existing wood workbench panel (the strip of cream that sits on top of where the panel's flat bottom region continues), PAINT MORE WOOD PANEL. Continue the exact same wood grain pattern, color, knot texture, and warm side-lighting from the existing panel, extending leftward all the way to the LEFT edge of the frame (and off-screen). The goal: the wood workbench should now look like it extends seamlessly from off the left edge of the frame all the way across to its current finished right-end corner — with no visible left edge and no cream gap between the panel and the frame's left side.

The panel's TOP horizontal edge stays at the SAME vertical height. The panel bottom remains at the frame bottom. The empty cream above the panel's top edge stays cream (do not paint wood there). The right half of the frame stays empty cream for copy (do not paint wood there).

No stretching, no blur, no color shift at the join — the extension must be indistinguishable from the original panel."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": CURRENT}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("extending engineering workbench leftward via gpt-image…", flush=True)
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
