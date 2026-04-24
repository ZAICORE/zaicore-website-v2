"""Generate security composite mirroring engineering's LEFT-HEAVY layout.

Belt extends from off the LEFT edge to a visible right-end corner at ~55%.
Robots on the belt (where they can drift right and fly off the end).
Owl on the far left behind the belt.
Right half of frame is pure empty cream for copy overlay.

Uses rule-of-thirds/percentage-split prompting from image-gen research.
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

OWL_REF = to_data_uri(MASCOTS / "owl_typing.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """1024x1024. Pixar 3D render. Uniformly warm cream/white background (#faf8f7), PURE FLAT CREAM — no gradient, no secondary characters, no reflections, no duplicate characters, no faint silhouettes, no ghost images. ONLY ONE OWL AND THREE ROBOTS in the entire image. Nothing else. The right 55% of the frame is PURE FLAT CREAM with absolutely nothing in it. Matches the aesthetic of a Pixar workshop scene where a character stands behind a front-facing bench/counter panel.

CRITICAL — ALL ELEMENTS FACE THE CAMERA DIRECTLY, LIKE A PIXAR WORKBENCH SCENE:
- The METAL CONVEYOR BENCH is shown as a VERTICAL FRONT-FACE PANEL along the bottom of the frame — we see ONLY the flat front face (like looking at the front of a workbench), NOT the top surface. Brushed-aluminum texture with visible panel seams and subtle industrial details. The panel runs horizontally across the bottom of the frame.
- The OWL stands BEHIND the panel, facing the camera head-on. Only his chest and head visible above the panel's top edge.
- The ROBOTS sit/hover at the TOP EDGE of the panel (their thrusters firing downward with blue glow, visible right at the panel's top edge), each facing the camera directly.

COMPOSITION:
- Content occupies only the LOWER-LEFT QUADRANT of the frame.
- Upper 50% of frame is PURE EMPTY CREAM (no objects).
- Right 55% of frame is PURE EMPTY CREAM (no objects).

Metal bench panel: vertical front-face of a brushed-aluminum workbench, occupying the bottom ~22% of the frame as a horizontal strip. Extends from the LEFT edge of the frame to about 45% across, with a CLEAN RIGHT-END vertical edge (the bench visibly ends on the right). Panel BOTTOM is flush with the frame bottom. Panel TOP edge at about 78% down from top of frame.

Snowy owl (matching first reference), FRONT-FACING, stands BEHIND the panel. Only chest-up visible above the panel's top edge. Positioned at about 10% across the frame. Owl head at about 58% down from top — QUITE SMALL.

THREE IDENTICAL helper robots MATCHING THE SECOND REFERENCE IMAGE EXACTLY — including their two small articulated ARMS at each side of their body (important: arms must be present and visible). ONE MODIFICATION ONLY: replace the robot's legs with small BLUE-GLOWING THRUSTERS on the underside of the body (two small circular thruster ports emitting soft bright blue light downward). Each robot is FRONT-FACING (amber eye looking at camera, ARMS VISIBLE at sides), hovering with thrusters just at the TOP EDGE of the bench panel. Arranged in a line at 15%, 25%, 35% across the frame. Each robot body about 9% of frame height — QUITE SMALL.

Shallow DOF, soft warm key light from upper left."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": OWL_REF}},
    {"type": "image_url", "image_url": {"url": ROBOT_REF}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("generating LEFT-heavy security composite…", flush=True)
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
