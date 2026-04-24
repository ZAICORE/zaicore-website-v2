"""Security video v2 — owl behind belt, 3 robots face camera, new narrative.

Uses security_scene_start.png (the newly approved still) as BOTH first_frame
and last_frame to pixel-lock the loop close. owl_typing.png + robot_tinkerer.png
carry character identity via input_references.

Narrative (10s):
  0–2s  Wide shot. 3 robots hover stationary on the belt facing camera.
        Owl behind the belt scans them left-to-right.
  2–4s  RIGHTMOST robot's eye flashes red. Owl's head tilts, then owl's right
        wing extends forward, scoops the red-eyed robot with feathered wing
        (NOT talon, NOT beak). Owl flicks it backward over his shoulder — it
        spirals into the deep background and DETONATES in a stylized cream
        puff cloud (cartoon poof, not realistic fire).
  4–7s  Remaining 2 robots' thruster flames flare brighter. They lift off the
        belt and fly off the RIGHT edge of frame, one after another.
  7–10s Owl's head tracks them rightward as they exit, then turns back LEFT.
        Three fresh identical robots fly in from off-screen LEFT, bank around,
        and settle onto the belt in the ORIGINAL three positions facing camera.
        Frame 10s == frame 0s exactly (enforced by last_frame = first_frame).
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

START     = to_data_uri(MASCOTS / "security_scene_start.png")
OWL_REF   = to_data_uri(MASCOTS / "owl_typing.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Pixar 3D. Light warm studio background matching the first_frame. CAMERA IS ABSOLUTELY STATIC for all 10 seconds — no zoom, no pan, no dolly, no drift, no reframing, not a single pixel of camera movement. The chrome conveyor platform with the snowy owl behind it stays fixed in the bottom-left of the frame for every frame — never slides, bounces, scales, or shifts.

CRITICAL ROBOT COUNT RULES — enforce strictly across every frame:
- Frame 0 through 2.5s: exactly THREE robots on the platform.
- 2.5s through 4.5s: the owl is holding the red robot in its wing / throwing it / watching it explode. Exactly TWO robots remain on the platform (the two that were not grabbed). No new robot may appear on the platform.
- 4.5s through 7.5s: the TWO remaining robots fly off to the upper-right and exit the frame. DURING this window the ONLY moving robots are those exact TWO — no third robot spawns, no replacement fades in, no duplicate lands on the belt.
- 7.0s through 8.5s: the platform is COMPLETELY EMPTY — zero robots anywhere on or near the belt. The owl stands alone behind the empty platform.
- 8.5s through 10s: three fresh robots drift in from off-screen LEFT and settle into the exact same three positions as frame 0.

Beat-by-beat:

[0–2s] Three identical helper robots hover on the chrome conveyor in the bottom-left, all facing the camera. Each: single amber eye, cream-white body, gold band, thin pincer arms, soft blue thruster flame beneath. The conveyor belt's surface slowly drifts left-to-right. The snowy owl stands behind the platform, head and upper chest visible above the belt's front edge, scanning the three robots.

[2–2.7s] The RIGHTMOST robot's eye flashes RED and vibrates / shakes rapidly. Owl's expression shifts to SERIOUS — brow lowers, eyes narrow, face focused.

[2.7–3.5s] Owl raises his right wing and DELIBERATELY GRABS the red robot in the curve of his feathered wing (firm catch — not a talon grab, not a beak grab, not a flick). Owl winds up and THROWS it strongly backward over his shoulder like a pitcher, sending the robot tumbling comically into the deep background.

[3.5–4.5s] Owl turns his head to WATCH the thrown robot. It spirals and tumbles backward through the air, shrinking as it travels into the deep background, and then DETONATES in a stylized Pixar-style cream/white PUFF CLOUD (cartoon poof — no fire, no realism, no debris). The puff expands then dissipates. Throughout this beat, the TWO remaining robots on the platform stay still, waiting. No third robot is added.

[4.5–7s] The TWO remaining robots (only two — do not add any others) activate their thrusters more intensely. They drift the last stretch rightward along the belt; as each reaches the belt's right end, it drops off the edge, its blue thruster flame flares brightly, and it FLIES UP AND TO THE RIGHT, exiting the upper-right corner of the frame one after another. By 7.0s both are gone and the platform is completely empty. STRICTLY no extra robot appears during this window.

[7–8.5s] Platform EMPTY. Owl stands alone, head tracking where the last robot departed (upper right), then slowly turning back to face LEFT. The empty platform is clearly visible — chrome frame, empty belt surface, no robots anywhere.

[8.5–10s] Three fresh identical robots drift INTO the frame from off-screen LEFT along the conveyor, settling into the exact same three positions on the platform as frame 0 by 10.0s. Their thrusters return to the idle glow. Owl's head returns to its starting position, expression calm. Frame 10.0s matches frame 0.0s exactly — seamless loop close.

NEGATIVES — strict: NEVER spawn, materialize, or reveal a third / fourth / replacement robot during the 2.7–8.5s window. Between 4.5s and 8.5s the belt must trend from two → zero robots, NOT from two → three. No ghost robot, no duplicate, no phantom arrival. No second owl, no duplicated characters, no warping, no jitter, no camera motion, no platform drift. Nothing in the upper-right area except empty clean studio background and the briefly departing two robots."""

body = {
    "model": "bytedance/seedance-2.0",
    "prompt": PROMPT,
    "aspect_ratio": "16:9",
    "duration": 10,
    "resolution": "1080p",
    "generate_audio": False,
    "frame_images": [
        {"type": "image_url", "image_url": {"url": START}, "frame_type": "first_frame"},
    ],
    "input_references": [
        {"type": "image_url", "image_url": {"url": OWL_REF}},
        {"type": "image_url", "image_url": {"url": ROBOT_REF}},
    ],
}

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

print(f"submitting security video v2 (new narrative, approved still)… prompt={len(PROMPT)} chars", flush=True)
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
