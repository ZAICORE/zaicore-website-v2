"""Generate 2 Seedance 2.0 hero idle loops via Replicate.

Key trick for seamless loops: pass the same still as BOTH `image` (first frame)
and `last_frame_image` (last frame). Seedance then creates a clip that starts
AND ends at the identical pose — the loop seam is invisible.
"""
import os, json, time, pathlib, urllib.request, urllib.error, base64

TOKEN = None
for line in pathlib.Path(os.path.expanduser('~/cyber-crime/apps/marketing/.env.local')).read_text().split('\n'):
    if line.startswith('REPLICATE_API_TOKEN='):
        TOKEN = line.split('=', 1)[1].strip().strip('"').strip("'")
        break
assert TOKEN, "no replicate token"

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT = MASCOTS

def upload_file_as_data_uri(path: pathlib.Path) -> str:
    """Return a data: URI — Replicate accepts these as image inputs."""
    b = path.read_bytes()
    b64 = base64.b64encode(b).decode('ascii')
    return f"data:image/png;base64,{b64}"

SPECS = [
    {
        "name": "fox_idle",
        "image_path": MASCOTS / "fox.png",
        "prompt": (
            "The fox breathes gently in and out. Eyes blink twice slowly. "
            "Head tilts slightly to the right, the fox glances briefly toward the right side of "
            "the frame as if looking at something, then settles back to the exact starting pose. "
            "Subtle ear twitch. Completely static camera, no panning, no zoom. "
            "Pure white studio background, soft even lighting. Calm, peaceful motion. "
            "End pose must match start pose exactly for a seamless loop."
        ),
    },
    {
        "name": "owl_idle",
        "image_path": MASCOTS / "owl.png",
        "prompt": (
            "The owl breathes gently. Eyes blink slowly twice. Head tilts slightly to the left, "
            "the owl looks briefly toward the left side of the frame, wing feathers ruffle softly, "
            "then settles back to the exact starting pose. "
            "Completely static camera, no panning, no zoom. "
            "Pure white studio background, soft even lighting. Calm, watchful motion. "
            "End pose must match start pose exactly for a seamless loop."
        ),
    },
]

HEADERS = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}
# Seedance 2.0 latest version (from /v1/models/bytedance/seedance-2.0)
MODEL = "bytedance/seedance-2.0"

def create_prediction(prompt: str, image_data_uri: str) -> dict:
    body = {
        "input": {
            "prompt": prompt,
            "image": image_data_uri,
            "last_frame_image": image_data_uri,  # the loop trick
            "duration": 5,
            "resolution": "720p",
            "aspect_ratio": "3:4",
            "generate_audio": False,
        }
    }
    req = urllib.request.Request(
        f"https://api.replicate.com/v1/models/{MODEL}/predictions",
        data=json.dumps(body).encode(),
        headers=HEADERS,
    )
    try:
        r = urllib.request.urlopen(req, timeout=60)
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:300]}", flush=True)
        raise
    return json.load(r)

def poll(pred_id: str) -> dict:
    url = f"https://api.replicate.com/v1/predictions/{pred_id}"
    while True:
        req = urllib.request.Request(url, headers=HEADERS)
        p = json.load(urllib.request.urlopen(req, timeout=30))
        status = p.get("status")
        if status in ("succeeded", "failed", "canceled"):
            return p
        print(f"    status={status}", flush=True)
        time.sleep(8)

def download(url: str, out_path: pathlib.Path):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as r, open(out_path, "wb") as f:
        f.write(r.read())

total_time = 0.0
for spec in SPECS:
    print(f"[{spec['name']}] uploading still...", flush=True)
    img_uri = upload_file_as_data_uri(spec["image_path"])
    print(f"[{spec['name']}] submitting Seedance job (first+last frame locked to still)...", flush=True)
    t0 = time.time()
    pred = create_prediction(spec["prompt"], img_uri)
    pid = pred["id"]
    print(f"  prediction id: {pid}", flush=True)
    result = poll(pid)
    elapsed = time.time() - t0
    total_time += elapsed
    if result["status"] != "succeeded":
        print(f"  FAILED: {result.get('error')}", flush=True)
        continue
    out = result["output"]
    # output is either a string (url) or a list
    video_url = out if isinstance(out, str) else out[0]
    out_path = OUT / f"{spec['name']}.mp4"
    print(f"  downloading → {out_path.name}", flush=True)
    download(video_url, out_path)
    size_kb = out_path.stat().st_size // 1024
    print(f"  saved {out_path.name} ({size_kb} KB, {elapsed:.0f}s)", flush=True)

print(f"\nDONE. total render time {total_time:.0f}s", flush=True)
