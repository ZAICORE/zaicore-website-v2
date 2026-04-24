"""Engineering-page hero still — fox tinkering on the helper robot.

9:16 vertical. Nano Banana Pro (google/gemini-3-pro-image-preview) at 2K.
Fox in safety goggles (over eyes, not forehead), seated on workshop floor,
helper robot (matching robot_tinkerer.png — thruster, no legs) resting in
his lap / on a small surface in front of him, open panel exposed, fox
working on it with a small tool. Warm cream studio bg. Bottom-heavy
character composition with empty cream upper third.

Output is the first_frame AND last_frame for the Seedance 2.0 loop.
"""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT_STILLS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))
OUT_STILLS.mkdir(parents=True, exist_ok=True)

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

FOX   = to_data_uri(MASCOTS / "fox_soldering.png")
ROBOT = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Render a Pixar 3D feature-film quality scene, 16:9 LANDSCAPE frame (wider than tall), clean white studio background with a SUBTLE natural rendered gradient (near-white, very light warm tint, soft ambient depth — NOT flat pure RGB 255,255,255 white, but reads as white to the eye). The composition is heavily weighted to the BOTTOM-RIGHT corner — the upper-left two-thirds of the frame is empty white studio space for copy overlay.

TWO reference images:
IMAGE 1 — the FOX: identity reference (fur pattern, snout, ear shape, paw shape). Use his identity EXACTLY.
IMAGE 2 — the ROBOT: identity reference (single amber camera-lens eye, cream-white body, gold band, two pincer arms, blue thruster). Use this design.

SCENE — small cluster tucked into the BOTTOM-RIGHT CORNER, ONLY THE BOTTOM HALF OF THE FRAME:
- The fox + robot cluster is SMALL — fits ENTIRELY within the bottom-right quadrant. The TOP of the fox's head/ears sits at or below the vertical midline of the frame (the cluster does NOT extend above the 50% height mark). Width-wise it occupies roughly the right ~22% of the frame.
- The ENTIRE upper half of the frame (above the vertical midline) is empty white studio space — no characters, no fox ears poking up, nothing.
- The cluster anchors to the bottom edge and the right edge of the frame.
- The fox sits on a simple wooden workshop stool. His body is slightly angled toward camera-left, head and shoulders oriented toward the camera.
- Protective clear SAFETY GOGGLES are WORN OVER HIS EYES (clear lenses covering the eyes, visible reflection on the lens surface — NOT pushed up on his forehead). Goggles DOWN, on his face.
- The helper robot (matching IMAGE 2) sits in the fox's lap, face angled slightly up toward the fox. The robot's thruster is OFF / idle (no flame — sitting at rest). A small rectangular access panel on the robot's side is open, revealing a hint of circuit board / gold contacts inside.
- The fox holds a tiny PRECISION TOOL (small screwdriver or tweezers) in his paw, tip extended into the open panel, mid-work. His other paw steadies the robot.
- Fox's expression is focused — eyes behind goggles concentrated on the panel.

UPPER-LEFT ~78% of the frame: completely empty white studio background with the same subtle gradient — no objects, no characters, no shadows, nothing. Pure clean copy space. The cluster does NOT spread leftward — it stays tucked in the bottom-right corner.

HARD NEGATIVES:
- Goggles DOWN over the eyes — never pushed up on forehead.
- No second fox, no ghost characters, no duplicated elements.
- The upper-left and central area of the frame is completely empty — no floating objects, no tools, no decorative elements.
- Background is NOT flat RGB(255,255,255) — render it with a subtle natural gradient so it has depth, but it should read visually as a clean white studio.
- No wooden floor texture spread across the frame — only a small grounding surface (the stool) under the fox, and even that should be minimal.

Premium Pixar 3D render, 16:9 LANDSCAPE."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": FOX}},
    {"type": "image_url", "image_url": {"url": ROBOT}},
]

body = {
    "model": "google/gemini-3-pro-image-preview",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
    "image_config": {
        "aspect_ratio": "16:9",
        "image_size": "2K",
    },
}

print("Nano Banana Pro — engineering page hero still (9:16 vertical)…", flush=True)
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

msg = data["choices"][0]["message"]
images = msg.get("images", [])
if not images:
    print(f"NO_IMAGE; msg: {json.dumps(msg)[:800]}", flush=True); exit(1)

png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
out_path = MASCOTS / "engineering_page_start.png"
out_path.write_bytes(png)
(OUT_STILLS / "engineering_page_start.png").write_bytes(png)

from PIL import Image
import io
img = Image.open(io.BytesIO(png))
print(f"output: {img.size[0]}x{img.size[1]}")
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost})", flush=True)
print(f"saved to: {out_path}", flush=True)
