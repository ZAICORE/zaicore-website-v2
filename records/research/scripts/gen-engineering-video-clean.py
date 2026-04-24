"""Fresh lean engineering video prompt.

Narrative: receive part → place it below the lip → solder it → robot exits →
next robot comes from the other side with a different part → repeat.

Uses the new clean engineering still as first_frame + last_frame.
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

PROMPT = """16:9 static shot, locked camera, 10 seconds. Flat warm off-white studio throughout. Premium Pixar 3D feature-film render.

The scene matches the provided first-frame still: a long wood workbench extending off the left edge across most of the frame, a fox behind it (chest-up, goggles on, pencil-grip soldering iron in one paw, single thin smoke wisp from the iron tip). The fox is ALONE — no robots anywhere in the first frame. The upper half and right portion of the frame are empty warm off-white.

Loop beats:

0–1.5s: Fox alone at the bench, soldering quietly, single smoke wisp rising from his iron (matches first frame).

1.5–3s: A helper robot (cream body, single amber camera-lens eye, gold accent band, blue thruster glow) flies INTO the frame from the LEFT edge, carrying a small brass gear in its pincer. It hovers to the LEFT of the fox at bench-lip height.

3–4s: The fox reaches out with his free paw (which rises ABOVE the top edge of the wood panel) and takes the brass gear from the robot's pincer. He then LOWERS his paw carrying the gear DOWN behind the top edge of the wood panel. CRITICAL: once the gear descends below the panel's top edge, it is COMPLETELY HIDDEN from view (the solid wood panel blocks the camera's view of anything behind and below its top edge). The gear disappears from view as it goes behind the panel and never reappears above the panel. The fox's empty paw comes back up above the panel edge, and he resumes soldering.

4–5s: The left robot drifts back and flies OUT off the LEFT edge of the frame, completely leaving the scene.

5–6s: Fox alone again, soldering, smoke wisp rising.

6–7.5s: A different helper robot (same character family) flies INTO the frame from the RIGHT edge, carrying a small green circuit board in its pincer. It hovers to the RIGHT of the fox at bench-lip height.

7.5–8.5s: The fox reaches out with his free paw (rising above the panel top edge), takes the circuit board from the robot's pincer, and LOWERS his paw carrying the circuit board DOWN behind the panel's top edge. The circuit board disappears from view as soon as it descends below the panel edge and never reappears above the panel. His empty paw comes back up and he resumes soldering.

8.5–10s: The right robot drifts back and flies OUT off the RIGHT edge of the frame, completely leaving the scene. By 10.0s the fox is ALONE at his bench, soldering with his single smoke wisp — matching the first frame exactly for a seamless loop.

Throughout: one soldering iron, one thin smoke wisp from its tip. The fox's goggles stay on. The tall wood panel at the front of the workbench is solid — anything that goes behind the panel's top edge (the gear, the circuit board, the soldering iron tip) is completely hidden from the camera's view. Nothing placed behind the panel reappears above it. Robots always visibly fly in from an edge and visibly fly out to an edge — never fade or pop. Never more than one robot visible at a time. At the end (10.0s) the scene is EXACTLY the starting pose: fox alone, no robots anywhere, no parts visible above the panel edge."""

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

print("submitting engineering video (clean lean prompt)…", flush=True)
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
