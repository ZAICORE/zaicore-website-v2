"""Generate the v3 hero video — wordmark falls, robots restore it.

Uses scene_still.png (fox + owl + wordmark on wall) as both first_frame and
last_frame so the loop closes seamlessly.
References: fox_soldering, owl_typing, robot_tinkerer, zaicore_wordmark.
10 seconds, 1080p. Full narrative fits in 10s: wordmark falls → animals
shrug and return to work → robots fly in with wordmark → robots place it
back → robots leave → loop.
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
LOGO_REF    = to_data_uri(MASCOTS / "zaicore_wordmark.png")

PROMPT = """Single wide static shot, 16:9 aspect ratio, 10 seconds total. Pure white seamless studio throughout.

CAMERA: Locked eye-level wide shot. Completely static — no pan, no zoom, no dolly, no tilt. The camera does not move for any reason throughout the entire 10 seconds.

SUBJECTS (must match the provided reference images exactly):
- A young 3D cartoon fox wearing clear safety goggles DOWN over its eyes, sitting cross-legged on the left third of the floor, holding a chrome soldering iron in one paw and a small green circuit board in its lap. Warm russet fur.
- A 3D cartoon snowy owl with pristine white feathers, standing on the right third of the floor next to a small open silver aluminum laptop. The laptop is completely UNBRANDED (no logos). Its back lid (plain silver) faces the viewer; the screen faces the owl.
- THREE small 3D cartoon helper robots (matching the robot reference): cream-white pill-shaped bodies, matte plastic finish, rounded dome heads with a single large glowing amber camera-lens eye, rounded arms with pincer hands, slim gold accent band, rolling on small round black wheels. Each robot has soft glowing blue thrusters on its underside for hovering flight.
- The word ZAICORE appears on the back wall of the studio as clean bold dark charcoal painted lettering (matching the provided logo reference exactly — bold geometric sans-serif, crisp edges). The wordmark is centered horizontally, positioned in the upper-center of the frame.

TIMELINE (seamless loop — the end frame must match the start frame exactly):

First, from 0 to 1.5 seconds: The ZAICORE wordmark is fully in place on the back wall. The fox is soldering the circuit board in its lap (a thin wisp of smoke curls from the iron tip). The owl taps a key on the unbranded silver laptop keyboard. Both are focused on their own work. The center of the frame is empty white space. No robots are visible.

Then, from 1.5 to 3 seconds: The ZAICORE wordmark on the back wall loses its grip and FALLS — the whole word tilts and slides down off the wall, tumbling through the air in the center of the frame, then landing softly on the white floor between the fox and owl. The letters stay joined together as one unit as they fall. The fox pauses soldering, lifts its head, pushes its safety goggles up onto its forehead with one paw, and looks with wide-eyed surprise at the fallen wordmark. The owl lifts its talon off the keyboard, turns its head, and looks at the fallen wordmark.

Then, from 3 to 4.5 seconds: The fox and owl turn their heads toward each other briefly, then each performs a CLEAR SHOULDER SHRUG — a classic "dunno, not my problem" gesture done ENTIRELY with shoulders/upper body, NOT with limbs. Critical details: the FOX keeps both paws in its lap with the soldering iron still held, paws do NOT lift up or out (do not raise paws above shoulder height, do not show palms). The fox just lifts its SHOULDERS briefly toward its ears with head tilted slightly, a pure shoulder-shrug silhouette. The OWL keeps both wings fully FOLDED against its body, wings do NOT spread out or lift up (do not make wing gestures of any kind). The owl just lifts its SHOULDER-AREA toward its head briefly, feathers on shoulders puffing up slightly, a pure shoulder-shrug silhouette. Both characters keep their existing limbs exactly where they were — the shrug is ONLY the shoulders rising, nothing else moves. The gesture reads as "dismissive / not-my-problem" through the shoulder lift and head tilt alone. Then the fox immediately pulls the goggles back down over its eyes, picks up the soldering iron, and turns its body and gaze back down to its circuit board, resuming work. The owl immediately turns its body and gaze back to the silver laptop and resumes tapping the keyboard. They are POINTEDLY IGNORING the fallen wordmark — it's not their job to fix it.

CRITICAL ANATOMY CONSTRAINT: The fox has exactly 4 legs and NO hands — its front paws function as both hands and front legs. Do NOT draw the fox with raised hands in addition to its legs. The owl has exactly 2 wings and 2 legs — wings serve as arms. Do NOT draw the owl with both wings raised AND legs visible as if it had 4 limbs. Each character always shows the correct number of limbs for its anatomy.

Then, from 4.5 to 6.5 seconds: EXACTLY THREE small cream helper robots (never two, never four, never five — ALWAYS exactly three identical robots matching the provided reference) fly into the frame from the BOTTOM EDGE at three spread-out positions: ROBOT ONE enters flying low from the bottom-left, landing on the white floor near the LEFT END of the fallen wordmark; ROBOT TWO enters flying low from the bottom-center (staying LOW near the floor — never rising toward the wall), landing on the white floor in front of the MIDDLE of the fallen wordmark; ROBOT THREE enters flying low from the bottom-right, landing on the white floor near the RIGHT END of the fallen wordmark. Each robot has a soft blue thruster glow visible under its body. Every robot must VISIBLY enter the frame from off-screen on camera — no robot ever pops into existence in the middle of the frame, and NO ROBOT EVER PASSES BEHIND THE ZAICORE WORDMARK at any point. After landing, the three robots lift the wordmark together in front of them (Robot 1 on the left end, Robot 2 in the middle underneath, Robot 3 on the right end) and fly upward together as a group IN FRONT OF the back wall (never behind it), carrying the wordmark toward its original position. Throughout this action there must be EXACTLY THREE ROBOTS VISIBLE AT ALL TIMES — never a fourth robot, never two, never five, never any robot behind the wall or behind the wordmark.

Then, from 6.5 to 7.5 seconds: The same three robots (exactly three, always three) press the ZAICORE wordmark back into place on the back wall at its original position. The wordmark settles cleanly on the wall, crisp and legible, exactly matching its starting position.

Then, from 7.5 to 9 seconds: THE WORDMARK IS RESTORED AND SITS PROUDLY ON THE WALL, clean and crisp. This is the payoff beat — the wordmark is beautifully in place and the camera lets it sit for a full moment. The three robots drift back a short distance from the wall and hover in the center of the frame, their pincer hands lowered (they've finished their job). The fox glances up briefly from its soldering, the owl glances up briefly from its laptop — both see the wordmark is restored. The three hovering robots do a small unified "all good" head nod together. Still exactly three robots. The ZAICORE wordmark remains perfectly visible and stable throughout this whole beat.

Finally, from 9 to 10 seconds: The same three robots (still exactly three, never more) fly VISIBLY OUT OF FRAME — ROBOT ONE drops straight down below the bottom edge of the frame, ROBOT TWO flies diagonally out the bottom-left corner, ROBOT THREE flies diagonally out the bottom-right corner. Every robot must be visibly flying toward and off the edge of the frame — no robot is allowed to simply disappear or fade in place. The fox resettles into its exact starting pose (goggles down, head tilted to circuit board, soldering iron in paw). The owl resettles into its exact starting pose (head tilted to laptop, one talon tapping keyboard). By 10 seconds the scene EXACTLY matches the start pose: ZAICORE wordmark clean on the back wall, fox soldering on the left, owl typing on the right, empty middle with NO ROBOTS VISIBLE. Seamless invisible loop.

STYLE: ZAICORE animation style — original 3D cartoon characters rendered with warm cinematic lighting, soft subsurface scattering on fur and feathers and plastic, shallow depth of field. Pure white seamless studio background and floor. Soft realistic floor shadows beneath each character.

CONSTRAINTS: No text anywhere on screen OTHER than the ZAICORE wordmark (which matches the provided logo reference exactly). No additional labels, no numerals, no captions, no writing on the laptop or anywhere else. No speech, no dialogue, no audio. Camera is absolutely locked and static — zero camera movement. Only the specified fox, owl, and three robots appear — no additional figures. Loop-match the starting and ending poses exactly. The ZAICORE wordmark must remain legible and stable whenever it is on the wall (not shimmering or warping)."""

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
        {"type": "image_url", "image_url": {"url": LOGO_REF}},
    ],
}

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

print("submitting hero v3 video — fall + robot restore narrative, 1080p...", flush=True)
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
