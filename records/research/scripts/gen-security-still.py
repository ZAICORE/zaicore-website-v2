"""Security section still — owl alone at brushed-glass console.

Mirror of the engineering scene: same warm off-white studio, thin glass console
(mirror of the wood panel) spans the lower portion, owl at ~44% across, empty
upper-right for copy overlay, empty right portion of the belt where robots
will be composited in next.
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

OWL_REF = to_data_uri(MASCOTS / "owl_typing.png")

PROMPT = """Match the provided owl character EXACTLY — same snowy owl with pristine white feathers, same face, same body proportions. Premium Pixar 3D feature-film render. 16:9 landscape, 1792 by 1024.

Setting: uniformly flat warm off-white studio background (#faf8f7, RGB approx 250/248/247). No walls, no floor, no other objects. Background color is PERFECTLY UNIFORM across the ENTIRE frame — no gradient, no warmer patches, no tonal shifts.

COMPOSITION — this is a BOTTOM-STRIP layout: all characters and furniture sit in the LOWER 35% of the frame. The UPPER 65% of the frame is empty pure cream background (for body copy to sit later).

A thin brushed-glass conveyor belt extends horizontally ACROSS THE ENTIRE FULL WIDTH of the frame (from off the left edge to off the right edge). The belt is a clean horizontal surface with a subtle pale-blue directional flow-line glowing faintly BENEATH the glass surface (security/processing-layer indicator). The belt's top edge is a flat horizontal line positioned at about 65% down from the top of the frame. Below that edge is the belt itself, visible down to the bottom of the frame.

The owl stands behind the conveyor belt, visible only from his chest up above the belt's top edge. He is positioned at about 28% across the frame (center-left). He is SMALL — the top of his head reaches ONLY about 45% down from the top of the frame (so his head sits in the middle band of the frame, near the top of the bottom strip). His posture is alert and watchful: head turned slightly to HIS RIGHT (camera's right) as if tracking something approaching from that direction. Eyes wide and intent. Wings folded neatly at his sides.

The owl is ALONE — no robots, no other figures. To the RIGHT of the owl, along the full horizontal extent of the belt (roughly 40% to 95% across the frame), above the belt's top edge, is open empty warm cream space — clear room where helper robots will later hover.

The UPPER 55% of the frame (from the top of the frame down to about 55% from the top) is completely empty uniform cream. No objects, no detail, just clean breathing room for text to sit. This upper empty cream zone spans the full width of the frame.

Warm key light from the upper left, a cool pale-blue under-light catching the glass belt from below. Shallow depth of field on the owl."""

content = [{"type": "text", "text": PROMPT}]
content.append({"type": "image_url", "image_url": {"url": OWL_REF}})

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("gen security still — owl alone at glass console…", flush=True)
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
(OUT / "section_security.png").write_bytes(png)
(MASCOTS / "section_security.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {MASCOTS / 'section_security.png'}", flush=True)
