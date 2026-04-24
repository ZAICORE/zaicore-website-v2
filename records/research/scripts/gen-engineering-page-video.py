"""Engineering page hero video — fox working on robot, looks up at viewer, back to work.

Uses engineering_page_start.png (the approved 16:9 still with cluster tucked in
bottom-right) as both first_frame AND last_frame to enforce loop close.
fox_soldering.png + robot_tinkerer.png carry character identity.

Narrative (~6s):
  0–2.5s   Fox quietly works on the robot's open panel — small precise tool
           movements, head tilted down to focus.
  2.5–4s   Fox pauses. Lifts his head, looks directly at the camera. Slight
           acknowledgment — eyes meet camera, soft moment, maybe a tiny
           eyebrow raise behind goggles. Robot stays still in his lap.
  4–6s     Fox returns gaze to the panel and resumes working.
           Frame 6.0 == Frame 0.0 exactly — seamless loop.
"""
import os, json, base64, urllib.request, urllib.error, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT_VIDEOS = MASCOTS

def to_data_uri(p): return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

START = to_data_uri(MASCOTS / "engineering_page_start.png")
FOX_REF   = to_data_uri(MASCOTS / "fox_soldering.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Pixar 3D feature-film render. White studio background matching the first_frame. CAMERA IS ABSOLUTELY STATIC for the entire 6 seconds — no zoom, no pan, no dolly, no drift, no shake, not a single pixel of camera motion. The fox + helper robot cluster stays FIXED in the bottom-right of the frame for every single frame — never slides, scales, drifts, or repositions. The upper-left ~78% of the frame remains empty white studio space throughout.

Loop beats — gentle, intimate, character-driven:

[0–2.5s] The fox sits on the wooden stool in the bottom-right corner, helper robot resting in his lap. Fox's head is tilted down, focused on the open access panel. He works the tiny precision tool with small, careful paw movements — micro-adjustments inside the panel. The robot is still and patient, looking slightly up. Subtle, quiet activity.

[2.5–4s] Fox PAUSES the tool. He slowly LIFTS his head and looks directly at the camera — soft eye contact through the safety goggles, a small recognition that we're there. His expression is warm, briefly attentive — maybe a tiny eyebrow lift or a soft "hi" beat. The robot stays still in his lap. Tool stays in his paw, paused mid-air.

[4–6s] Fox lowers his gaze back to the open panel and resumes the precise tool work — same head tilt, same paw movements as the opening beat. By frame 6.0 the pose, expression, and composition match frame 0.0 EXACTLY for a seamless loop.

NEGATIVES: the cluster must NOT slide, scale, or leave the bottom-right corner. The camera must NOT move. No jitter, no temporal flicker, no warping. The fox's safety goggles stay ON over his eyes the entire video — they do NOT slide up to his forehead. The robot stays still in his lap — it does not animate, fly, or change pose. No additional characters, no second fox, no ghost figures. The upper-left empty studio space stays empty throughout."""

body = {
    "model": "bytedance/seedance-2.0",
    "prompt": PROMPT,
    "aspect_ratio": "16:9",
    "duration": 6,
    "resolution": "1080p",
    "generate_audio": False,
    "frame_images": [
        {"type": "image_url", "image_url": {"url": START}, "frame_type": "first_frame"},
        {"type": "image_url", "image_url": {"url": START}, "frame_type": "last_frame"},
    ],
    "input_references": [
        {"type": "image_url", "image_url": {"url": FOX_REF}},
        {"type": "image_url", "image_url": {"url": ROBOT_REF}},
    ],
}

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

print(f"submitting engineering page video… prompt={len(PROMPT)} chars", flush=True)
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
        out_path = OUT_VIDEOS / "engineering_page_scene.mp4"
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
