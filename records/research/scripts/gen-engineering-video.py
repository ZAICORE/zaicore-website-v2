"""Generate the engineering section video — fox at workbench, robots handing
parts from both sides, steady smoke wisp from soldering iron.

Uses section_engineering.png as first_frame + last_frame for seamless loop.
References: fox_soldering, robot_tinkerer.
10 seconds, 1080p.

Loop cycle:
0-2s:  Start pose (left robot hovering with part extended, fox reaching from
       behind bench lip with second paw).
2-3s:  Fox takes part. Left robot releases, flies back out off the left edge.
3-5s:  Fox solders with new part — smoke rises clearly.
5-7s:  Right robot flies in from right side of frame with another part,
       approaches the bench, extends pincer toward fox.
7-8s:  Fox takes the right-side part. Right robot releases, flies back out
       off the right edge.
8-10s: Left robot flies back in from left edge with a new part. By 10s it
       reaches the exact start pose — seamless loop.
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

SCENE_STILL = to_data_uri(MASCOTS / "section_engineering.png")
FOX_REF     = to_data_uri(MASCOTS / "fox_soldering.png")
ROBOT_REF   = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Single wide static shot, 16:9 aspect ratio, 10 seconds total. FLAT UNIFORM warm off-white seamless studio (approximately #faf8f7) throughout — not pure bright white, not gray — a consistent clean warm off-white with NO noise, NO grain, NO gradient, NO color variance anywhere.

CAMERA: Locked eye-level shot framed on a warm wood workbench in the left 45% of the frame. Completely static — no pan, no zoom, no dolly, no tilt. The camera does not move for any reason throughout the entire 10 seconds.

SUBJECTS (must match the provided reference images exactly):
- The fox character (match fox reference exactly) — warm russet fur, clear safety goggles DOWN over his eyes (worn, covering the eyes), visible from chest up above a warm wood workbench lip. SMALL in frame — the fox's ear tips are at about 45% from the top of the frame with plenty of clean empty space above him. He holds a chrome soldering iron in one visible paw above the bench lip; EXACTLY ONE single thin steady wisp of smoke curls continuously upward from the soldering iron tip only. CRITICAL: never two wisps, never a duplicate, never split, never separate trails — ONE wisp from ONE iron tip, unambiguously singular.
- Helper robots (match robot reference exactly) — cream-white pill-shaped bodies, rounded dome heads with a single glowing amber camera-lens eye, pincer hands, gold accent band. Each robot HOVERS using small softly-glowing blue thrusters under its body (visible blue glow). Robots are similar size to the fox, never larger.

THE WORKBENCH: Beautiful warm wood workbench in the LEFT 45% of the frame with a clean finished right-end corner. A defined front wood lip hides whatever is on the work surface. The RIGHT 55% of the frame is flat clean empty warm off-white space.

TIMELINE — STRICT SEAMLESS LOOP where end frame EXACTLY matches start frame:

0.0 to 1.0s — START POSE: ONE helper robot hovers on the LEFT (with visible blue thruster glow) at bench-lip height, extending one pincer forward holding out a small polished brass GEAR toward the fox. The fox leans slightly toward the robot, soldering iron in one paw (with its steady smoke wisp), his OTHER paw raised from behind the lip reaching for the gear. This pose MATCHES the provided first-frame still exactly.

1.0 to 2.0s — HANDOFF: Fox's reaching paw gently takes the gear from the robot's pincer. The robot releases, begins drifting backward.

2.0 to 3.5s — LEFT EXIT: The left robot flies VISIBLY LEFT with its blue thruster glow and completely EXITS off the LEFT edge of the frame. By 3.5s, no robot is visible anywhere in the frame. Fox has lowered his paw behind the lip with the gear and is back to solo soldering (smoke wisp continues).

3.5 to 5.0s — SOLO BEAT: Fox solders alone behind the workbench, no robots visible anywhere in the frame. Smoke wisp continues steadily.

5.0 to 6.0s — RIGHT ENTRY: A different helper robot flies INTO the frame from the RIGHT edge with visible blue thruster glow, approaching at bench-lip height. It carries a small green CIRCUIT BOARD in its pincer (clearly different from a gear — flat rectangular shape with tiny components visible).

6.0 to 7.0s — RIGHT HANDOFF: The right robot hovers just to the fox's right, extends pincer with the circuit board. Fox turns slightly, raises his paw from behind the lip, and gently takes the circuit board. Robot releases.

7.0 to 8.5s — RIGHT EXIT: The right robot flies VISIBLY RIGHT with blue thruster glow and completely EXITS off the RIGHT edge of the frame. By 8.5s, NO ROBOT IS VISIBLE anywhere in the frame. The fox has lowered his paw with the circuit board and is back to solo soldering.

8.5 to 9.0s — SOLO BEAT: Fox alone, smoke rising. NO robots visible anywhere.

9.0 to 10.0s — LEFT RE-ENTRY (to close loop): A helper robot flies INTO the frame from the LEFT edge with blue thruster glow, carrying a small brass GEAR in its pincer. It flies quickly to its START POSE on the left side of the fox and settles into position by 10.0s — pincer extended with gear, fox's paw rising from behind the lip reaching for it. By exactly 10.0s, the scene MATCHES the START POSE exactly (identical to frame 0). Seamless invisible loop.

CRITICAL LOOP RULES:
- Between 2.5s and 5.0s: NO ROBOT IS VISIBLE anywhere in the frame.
- Between 7.5s and 9.0s: NO ROBOT IS VISIBLE anywhere in the frame.
- Every robot that enters must VISIBLY FLY IN FROM AN EDGE (not appear, not fade in).
- Every robot that exits must VISIBLY FLY OUT PAST AN EDGE (not fade, not teleport).
- At exactly 10.0s the scene must match the 0.0s start pose exactly so the loop is invisible.
- NEVER have two robots on screen at the same time.
- The parts alternate: gear (first handoff, matches start), circuit board (second handoff), gear (third handoff / new loop start) — visually distinct shapes.

Throughout all 10 seconds:
- EXACTLY ONE thin steady wisp of smoke rises continuously from the SINGLE soldering iron tip. Never two wisps, never a duplicated trail, never a second smoke source. Only ONE unambiguous wisp exists in the scene at any moment.
- Background is flat uniform warm off-white (#faf8f7) with NO noise/grain/variance.
- The workbench, fox's goggled face, and warm wood lip remain stable and consistent.
- Fox's goggles stay DOWN over his eyes throughout.

STYLE: ZAICORE animation style — original 3D cartoon characters with warm cinematic lighting, soft subsurface scattering on fur and plastic, shallow depth of field. Flat uniform warm off-white seamless studio background.

CONSTRAINTS: No text anywhere on screen — no letters, no numerals, no labels, no writing. No speech, no dialogue, no audio. Camera absolutely locked and static. Only the fox and helper robots described appear — no additional figures."""

body = {
    "model": "bytedance/seedance-2.0",
    "prompt": PROMPT,
    "aspect_ratio": "16:9",
    "duration": 10,
    "resolution": "1080p",
    "generate_audio": False,
    "frame_images": [
        {"type": "image_url", "image_url": {"url": SCENE_STILL}, "frame_type": "first_frame"},
        {"type": "image_url", "image_url": {"url": SCENE_STILL}, "frame_type": "last_frame"},
    ],
    "input_references": [
        {"type": "image_url", "image_url": {"url": FOX_REF}},
        {"type": "image_url", "image_url": {"url": ROBOT_REF}},
    ],
}

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

print("submitting engineering section video, 1080p...", flush=True)
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
        out_path = OUT_VIDEOS / "engineering_scene.mp4"
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
