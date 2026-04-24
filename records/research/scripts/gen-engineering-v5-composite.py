"""Engineering video v5 — use composite still (fox + reference robot) as
first_frame + last_frame. Robot identity is physically locked in the opening
pixels, so Seedance animates the CORRECT robot instead of inventing one.

Narrative: robot hands gear to fox, exits left. Robot enters from right with
circuit board, hands off, exits right. A fresh robot arrives from the left
with another gear at the end — matching the composite for a seamless loop.
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

COMPOSITE = to_data_uri(MASCOTS / "engineering_with_robot_16x9.png")
FOX_REF   = to_data_uri(MASCOTS / "fox_soldering.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """Pixar 3D. Fixed camera throughout.

[0s] Helper robot hovers on LEFT with brass gear. Fox at workbench soldering.

[1.5s] Fox takes the gear, lowers it behind the panel's top edge (disappears below the lip). Continues soldering. Robot exits LEFT.

[3.5s] Second robot enters from RIGHT with a small green computer part.

[5s] Fox takes it, lowers it behind the panel (disappears below the lip). Continues soldering. Second robot exits RIGHT.

[7s] Third robot descends from ABOVE and DUMPS a clunky pile of gears and computer parts onto the fox's head — parts bounce off and scatter.

[8s] Fox pauses, pushes safety goggles UP onto his forehead, rubs one eye slowly with his paw — tired, weary expression. No smile.

[9s] Fox pulls goggles back down, resumes soldering. Fresh robot enters from LEFT with new gear.

[10s] Matches starting pose. Seamless loop."""

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
        {"type": "image_url", "image_url": {"url": FOX_REF}},
        {"type": "image_url", "image_url": {"url": ROBOT_REF}},
    ],
}

HEADERS = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

print(f"submitting engineering v5 (composite first+last, reference-locked robot)… prompt={len(PROMPT)} chars", flush=True)
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
