"""Try to get gpt-image-2 (via OpenRouter) to output 1536x1024 landscape.

Testing if the size parameter forwards through OpenRouter's chat completions
endpoint for gpt-image-2. Uses rule-of-thirds + percentage-split composition
prompting per image-generation research.

Also passes owl + robot refs so character identity stays locked.
"""
import os, json, base64, urllib.request, pathlib, time, io

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

PROMPT = """Wide landscape composition, 1536x1024. Premium Pixar 3D feature-film render. Warm cream background (#faf8f7), uniform flat cinematic infinity sweep — no walls, no gradient.

COMPOSITION — rule of thirds, landscape frame:

Anchoring environment: a brushed-glass conveyor belt spans the LOWER QUARTER of the frame, CONTINUOUS from the LEFT edge all the way to the RIGHT edge — the belt must be FULL WIDTH with no breaks, no gaps, no cream showing beside it at the bottom. Subtle pale-blue directional flow-line glows beneath the glass across the full width.

LEFT THIRD of frame (0-33% across): a snowy owl with pristine white feathers (matching the first reference image exactly) stands behind the belt, chest-up above the belt's top edge. Head turned slightly to his right, eyes tracking something to his right. Owl head positioned at about 45% down from the top of the frame.

RIGHT TWO-THIRDS of frame (33-100% across): three IDENTICAL helper robots (matching the second reference image exactly) hovering in a line above the belt at approximately 50%, 65%, and 80% across the frame. Each robot: single large amber camera-lens eye, cream-white rounded body, gold accent band, two pincer arms at sides, soft blue thruster glow beneath.

UPPER HALF of the frame is EMPTY CREAM NEGATIVE SPACE — no characters, no objects. Pure breathing room for copy overlay.

All characters are SMALL in frame — they occupy only the lower-middle band. Shallow depth of field on characters, warm key light from upper left."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": OWL_REF}},
    {"type": "image_url", "image_url": {"url": ROBOT_REF}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
    # TESTING: does OpenRouter forward this to gpt-image-2?
    "size": "1536x1024",
}

print("testing: gpt-image-2 with size=1536x1024…", flush=True)
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

from PIL import Image
img = Image.open(io.BytesIO(png))
print(f"OUTPUT DIMENSIONS: {img.size}")

out_path = MASCOTS / "security_with_robots_image2_test.png"
out_path.write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {out_path}", flush=True)
