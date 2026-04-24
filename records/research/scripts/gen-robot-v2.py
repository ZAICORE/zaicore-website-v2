"""Regenerate robot with an ORIGINAL ZAICORE design — not WALL-E-adjacent.

Problem: Seedance's copyright filter keeps tripping on the WALL-E-like worker robot
(cube body + binocular eye-stalk + treads + rust patina).

v2 design: modern rounded helper robot, cream body, single amber lens eye, small wheels,
clean matte finish. Feels like it belongs in Arc/Apple/A24 design world.
"""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT_STILLS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))

PROMPT = (
    "An original, endearing 3D cartoon helper robot character, designed to fit alongside a "
    "friendly 3D cartoon fox and snowy owl in the same warm storybook cast. "
    "\n\nBODY: Rounded capsule-shaped body with smooth matte cream-white plastic finish, "
    "clean and modern (no rust, no patina, no weathering, no dents — pristine and freshly "
    "made). Gentle soft curves throughout — no sharp edges, no cubic shapes, no boxy "
    "geometry. The body is roughly pill-shaped with a slight taper at top and bottom. "
    "\n\nHEAD: A rounded dome head that sits smoothly on top of the body with no neck. "
    "The head is the same cream-white matte plastic as the body. Across the front face, a "
    "single large circular camera-lens eye, glowing warm amber-gold, centered on the head "
    "like a friendly single eye (NOT binocular, NOT stalk-mounted, NOT two eyes). The lens "
    "has a subtle aperture detail, warm amber inner glow. "
    "\n\nARMS: Two simple rounded articulated arms that extend from the sides of the body, "
    "same cream-white matte plastic, ending in small soft rounded two-finger pincer hands. "
    "One hand gently grips a small polished brass wrench; the other arm extends slightly "
    "forward with palm open in a friendly gesture. "
    "\n\nBASE: Instead of legs or treads, the robot rolls on two small round black rubber "
    "wheels flush under the body (absolutely NO caterpillar treads, NO tank tracks). "
    "\n\nACCENT: A single slim band of warm signal-gold color wraps horizontally around the "
    "middle of the body like a decorative stripe — the only color accent. "
    "\n\nEXPRESSION: Friendly, curious, approachable, helpful. Not military, not "
    "intimidating, not industrial. The feeling of a brand-new helpful home companion. "
    "\n\nSETTING: Standing calmly on a pure white seamless studio background and floor, "
    "soft realistic floor shadow beneath the wheels. Full body visible head to wheels, "
    "centered in frame. "
    "\n\nSTYLE: ZAICORE animation style — original 3D cartoon character with soft "
    "subsurface scattering on the plastic, warm cinematic key-plus-fill lighting, rich "
    "dimensional shading, premium render quality. Same render style as the companion fox "
    "and owl characters. "
    "\n\nImage dimensions: 1024 wide by 1536 tall (2:3 vertical portrait). "
    "\n\nCRITICAL: This is an original character design. Do NOT make it cube-shaped. Do "
    "NOT give it binocular eyes or a stalk neck. Do NOT give it caterpillar treads. Do NOT "
    "weather or rust it. It must be smooth, rounded, cream-colored, single-lens-eyed, on "
    "round wheels."
)

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": [{"type": "text", "text": PROMPT}]}],
    "modalities": ["image", "text"],
}
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
t0 = time.time()
print("generating original ZAICORE helper robot...", flush=True)
r = urllib.request.urlopen(req, timeout=300)
data = json.load(r)
if "error" in data:
    print(f"ERROR: {data['error']}", flush=True); exit(1)
images = data["choices"][0]["message"].get("images", [])
if not images:
    print("no image", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
(OUT_STILLS / "robot_tinkerer_v2.png").write_bytes(png)
(MASCOTS / "robot_tinkerer.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"DONE ({len(png)//1024} KB, {time.time()-t0:.0f}s, ${cost:.3f})", flush=True)
print(f"saved to {MASCOTS / 'robot_tinkerer.png'}", flush=True)
