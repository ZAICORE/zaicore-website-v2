"""Generate the v2 hero video — animated white-studio bottom-band scene.

Uses scene_hero.png as first_frame and last_frame for seamless loop.
Uses robot_tinkerer.png as input_reference for character consistency.
10s at 1080p, subtle ambient motion + one hovering robot crossing.
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

SCENE_STILL = to_data_uri(MASCOTS / "scene_hero.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Single wide static shot, 16:9 aspect ratio, 10 seconds total. Pure white seamless studio throughout — infinite white background, no walls, no architecture, no furniture, just white.

CAMERA: Locked eye-level shot. Completely static — no pan, no zoom, no dolly, no tilt. The camera does not move for any reason throughout the entire 10 seconds.

THE SCENE (matches the provided first_frame/last_frame exactly): A team of cream-and-gold helper robots distributed across the BOTTOM THIRD of the frame in a horizontal band. Each robot is at its own floating holographic workstation showing abstract glowing wireframe geometry and data curves. Two robots hover with soft blue thruster glows beneath their bodies. All robots match the provided reference image — cream pill bodies, single amber eye, gold accent band, round black wheels.

STYLE: ZAICORE animation style — original 3D cartoon characters with soft subsurface scattering on plastic, warm cinematic lighting, shallow depth of field, premium render quality. Pure white seamless studio — absolutely no architecture visible. Grounded soft floor shadows under each robot.

TIMELINE (three beats, seamless loop — the end frame must match the start frame exactly):

First, from 0 to 4 seconds: The robots are at their workstations along the bottom band, each doing subtle idle work — small natural motions. The robot at the leftmost floating panel makes tiny pincer gestures toward a glowing curve on its hologram. The two robots at the center-left station (one holding a translucent glowing panel between them) gesture slightly, as if discussing what's on the panel. The center pair of robots with a larger hologram between them both tilt their heads slightly. The rightmost robots at their panel make tiny gestures. Two robots hover near the middle of the frame using their blue thrusters — one at mid-upper-center carrying a small floating hologram, moving very slowly to the right across the scene; one at mid-upper-right carrying a floating item, moving very slowly to the left. They are tracing slow graceful arcs across the upper portion of the scene. The floating holographic panels pulse gently with their warm amber glow, never flickering — always smooth and continuous.

Then, from 4 to 7 seconds: The two hovering robots cross at the center-top of the scene, gently passing each other (never touching), each one now on the opposite side of where they started. The grounded robots continue their subtle station work — small head turns, tiny pincer gestures toward their holograms. One robot in the middle group slowly points at a detail on its shared floating hologram with a pincer. Everything remains calm and graceful. No character looks at the camera. The pulses of amber holographic light continue their gentle rhythm.

Finally, from 7 to 10 seconds: The two hovering robots continue their slow arcs and return exactly to their starting positions and starting orientations. The grounded robots settle back to their exact starting poses. By 10 seconds, every robot is in the EXACT same position and pose as at 0 seconds — producing a perfectly seamless invisible loop. The holograms continue their smooth warm pulse.

CONSTRAINTS: No text anywhere on screen — no letters, no numerals, no labels, no words, no signage of any kind, no readable content on any hologram. Holograms show only abstract glowing wireframe geometry and luminous curves. No speech, no dialogue, no audio. Camera is absolutely locked and static. Only the robots specified in the scene — no additional figures. The background is pure infinite white — no walls, no architecture, no furniture ever appears. The top two-thirds of the frame stays clean and empty throughout the entire video. Loop-match the starting and ending poses exactly — seamless invisible loop."""

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
        {"type": "image_url", "image_url": {"url": ROBOT_REF}},
    ],
}

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

print("submitting hero v2 video (bottom-band scene, 1080p)...", flush=True)
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
        out_path = OUT_VIDEOS / "hero_scene.mp4"
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
