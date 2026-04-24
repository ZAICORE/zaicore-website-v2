"""Security video — owl monitoring conveyor of helper robots.

Uses the composite still (owl + 3 reference robots on the conveyor) as BOTH
first_frame and last_frame — this pixel-locks the starting state AND the
ending state, so Seedance pulls the 3 "new" robots arriving at the end of
the cycle into matching the reference design.

Narrative: belt drifts right-to-left. Middle robot glitches as it approaches
the owl. Owl's talon snaps out, grabs the bad robot, flicks it up and out.
Remaining 2 continue drifting left and exit off the left edge. Belt empty
briefly. 3 new clean robots enter from the right edge and settle into the
starting positions — matches first_frame, loop closes.
"""
import os, json, base64, urllib.request, urllib.error, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT_VIDEOS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

COMPOSITE = to_data_uri(MASCOTS / "security_approved_frame0.png")
OWL_REF   = to_data_uri(MASCOTS / "owl_typing.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Pixar 3D. Cream background. Camera is static — no pan, no zoom, no movement of any kind.

A GLASS CONVEYOR BELT runs along the bottom-left of the frame and is VISIBLE IN EVERY FRAME OF THE VIDEO — it never disappears, never fades, it anchors the bottom of the scene throughout the full 10 seconds.

[0s] Wide shot. Bipedal snowy owl stands behind the glass belt, watching. Three helper robots stand on the belt, drifting slowly rightward along it.

[2s] The leading robot (closest to the belt's right-end) has its eye turn red. Owl cocks his head curiously and studies it. He then extends his FEATHERED WING over the belt, scoops the red robot up in the curve of his wing feathers (wing grab — not talon, not beak, not hand), and tosses it away with a flick of the wing — it spirals backward into the deep distance, shrinking to a speck.

[5s] The remaining two robots keep drifting rightward along the belt. When each reaches the belt's right-end, it lifts off the glass and flies off the right edge of the frame — one after another, conveyor rhythm.

[8s] Owl watches them fly off, then turns his head left as three fresh robots slide in from off-screen-left back onto the belt. Frame 10s matches the start frame exactly — seamless loop."""

body = {
    "model": "bytedance/seedance-2.0",
    "prompt": PROMPT,
    "aspect_ratio": "16:9",
    "duration": 10,
    "resolution": "1080p",
    "generate_audio": False,
    "frame_images": [
        {"type": "image_url", "image_url": {"url": COMPOSITE}, "frame_type": "first_frame"},
        {"type": "image_url", "image_url": {"url": COMPOSITE}, "frame_type": "last_frame"},
    ],
    "input_references": [
        {"type": "image_url", "image_url": {"url": OWL_REF}},
        {"type": "image_url", "image_url": {"url": ROBOT_REF}},
    ],
}

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

print(f"submitting security video (3-robot conveyor + glitch-catch-toss cycle)… prompt={len(PROMPT)} chars", flush=True)
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/videos",
    data=json.dumps(body).encode(),
    headers=HEADERS,
)
try:
    r = urllib.request.urlopen(req, timeout=60)
    initial = json.load(r)
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:800]}", flush=True); exit(1)

print(f"submitted. id={initial.get('id')}", flush=True)
polling_url = initial.get("polling_url")
if not polling_url:
    print(f"no polling_url; full response: {json.dumps(initial, indent=2)[:800]}", flush=True); exit(1)
print(f"polling: {polling_url}", flush=True)

t0 = time.time()
last_status = None
while True:
    req = urllib.request.Request(polling_url, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        p = json.load(r)
    except urllib.error.HTTPError as e:
        print(f"poll HTTP {e.code}: {e.read().decode()[:300]}", flush=True)
        time.sleep(10); continue
    status = p.get("status")
    elapsed = time.time() - t0
    if status != last_status:
        print(f"  [{elapsed:5.0f}s] status={status}", flush=True)
        last_status = status
    if status in ("completed", "succeeded"):
        urls = p.get("unsigned_urls") or p.get("output") or []
        if isinstance(urls, str): urls = [urls]
        if not urls:
            print(f"  no urls in success response: {json.dumps(p, indent=2)[:600]}", flush=True); exit(1)
        video_url = urls[0]
        print(f"  downloading from {video_url[:80]}...", flush=True)
        dl_req = urllib.request.Request(video_url, headers={"Authorization": f"Bearer {KEY}"})
        out_path = OUT_VIDEOS / "security_scene.mp4"
        with urllib.request.urlopen(dl_req, timeout=180) as resp, open(out_path, "wb") as f:
            f.write(resp.read())
        size_kb = out_path.stat().st_size // 1024
        cost = (p.get("usage") or {}).get("cost", "unknown")
        print(f"\nDONE ({size_kb} KB, {elapsed:.0f}s total, cost=${cost})", flush=True)
        print(f"saved to: {out_path}", flush=True)
        break
    if status in ("failed", "cancelled", "expired"):
        print(f"  FAILED: {p.get('error') or json.dumps(p)[:500]}", flush=True); exit(1)
    time.sleep(8)
