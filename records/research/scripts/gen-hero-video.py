"""Generate the hero Seedance 2.0 video on OpenRouter.

Uses scene_still.png as both first_frame and last_frame (for seamless loop).
Uses fox_soldering.png + owl_typing.png + robot_tinkerer.png as input_references.
Timeline-structured prompt: 3 beats across 10 seconds.
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

SCENE_STILL = to_data_uri(MASCOTS / "scene_still.png")
FOX_REF     = to_data_uri(MASCOTS / "fox_soldering.png")
OWL_REF     = to_data_uri(MASCOTS / "owl_typing.png")
ROBOT_REF   = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Single wide static shot, 16:9 aspect ratio, 10 seconds total. Pure white seamless studio background and floor throughout.

CAMERA: Locked eye-level wide shot. Completely static — no pan, no zoom, no dolly, no tilt. The camera does not move for any reason throughout the entire 10 seconds.

SUBJECTS (three characters, must match the provided reference images exactly):
- A young 3D cartoon fox character wearing clear safety goggles, sitting cross-legged on the left third of the floor, holding a chrome soldering iron in one paw and a small green circuit board in its lap. Warm russet fur.
- A 3D cartoon snowy owl with pristine white feathers, standing on the right third of the floor next to a small open silver aluminum laptop. The laptop is completely UNBRANDED (no logos, no markings). Its back lid (plain silver metal) faces the viewer; the screen faces the owl.
- A small 3D cartoon helper robot character: rounded cream-white pill-shaped body with smooth matte finish, a single large glowing amber camera-lens eye centered on a rounded dome head (not binocular, not stalk-mounted), two simple rounded arms ending in pincer hands (one holding a small brass wrench), a slim gold accent band around the middle of the body, rolling on two small round black rubber wheels.

TIMELINE (three beats, seamless loop — the end frame must match the start frame exactly):

First, from 0 to 4 seconds: The fox solders the circuit board in its lap, a thin wisp of smoke curls upward from the soldering iron tip. The owl taps one key on the unbranded silver laptop keyboard with one talon, head tilted down toward the screen. Both characters are focused on their own work, neither looks up. The center of the frame is empty white space. No robot is visible.

Then, from 4 to 7 seconds: The worker robot rises upward from below the bottom center of the frame, rolling up on its treads until it is positioned in the empty center of the frame, facing the camera. The robot extends its arm and small brass wrench UPWARD toward the upper-center area of the frame (as if reaching up to fix something above it — the robot's wrench hand reaches up past the midline of the frame, close to where the top center of the frame is). As the robot appears, the fox pauses its soldering, lifts its head, looks toward the robot with curious surprise, and gently pushes its safety goggles up onto its forehead with one paw. The owl pauses its typing, lifts its talon off the keyboard, turns its head to look toward the robot. The fox and owl exchange a brief glance toward each other and each give a small bemused shoulder shrug. The robot's raised wrench hovers near the top center of the frame as if tightening something invisible.

Finally, from 7 to 10 seconds: The robot lowers itself back down out of the bottom center of the frame, disappearing below. The fox pulls its safety goggles back down over its eyes with one paw, picks up the soldering iron again, and returns to soldering the circuit board. The owl turns back toward its silver laptop, talon lowers to the keyboard and resumes tapping. By 10 seconds, both characters are in the EXACT same pose as at 0 seconds — producing a perfectly seamless invisible loop.

STYLE: ZAICORE animation style — original 3D cartoon characters rendered with warm cinematic lighting, soft subsurface scattering on fur and feathers and metal, shallow depth of field. Pure white seamless studio background and floor. Soft realistic floor shadows beneath each character.

CONSTRAINTS: No text anywhere on screen. No speech, no dialogue, no audio of any kind. Camera is locked and static — absolutely no camera movement. Only the three specified characters in the scene — no additional figures. The middle-center area of the frame must remain empty white space except during the 4-to-7-second beat when the robot is visible. Loop-match the starting and ending poses exactly."""

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
        {"type": "image_url", "image_url": {"url": OWL_REF}},
        {"type": "image_url", "image_url": {"url": ROBOT_REF}},
    ],
}

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

print("submitting hero video generation to OpenRouter Seedance 2.0...", flush=True)
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
print(f"status: {initial.get('status')}", flush=True)
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
        # OpenRouter's content URLs require the same Bearer token
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
