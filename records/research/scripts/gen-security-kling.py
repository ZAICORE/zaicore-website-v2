"""Security video regen via fal Kling 3.0 Pro image-to-video.
Same thruster composite anchors both start and end frame for loop.
Same tight timeline prompt that's working well for Seedance.
"""
import os, pathlib, time
import fal_client

for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('FAL_KEY='):
        os.environ['FAL_KEY'] = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
COMPOSITE = MASCOTS / "security_with_robots.png"

PROMPT = """Pixar 3D. Cream background. Camera is static — no pan, no zoom, no movement of any kind.

[0s] Wide shot. Horizontal glass conveyor belt in the lower-left of the frame. Bipedal snowy owl stands behind the belt, watching. Three helper robots with blue-glowing thrusters hover just above the belt, drifting slowly rightward.

[2s] The leading robot (closest to the belt's right-end) has its eye turn red. Owl cocks his head curiously, studies it for a beat, then extends a wing and gently grabs the red robot. He throws it — it spirals backward into the deep distance, shrinking to a speck.

[5s] The remaining two robots drift onward toward the belt's end. Each falls briefly off the edge, thrusters flare bright blue, and flies off the right edge of the frame one after another.

[8s] Owl watches them go, then turns his head left as three fresh robots hover-drift in from off-screen-left back onto the belt. Frame 10s matches the start frame exactly — seamless loop."""

print(f"uploading composite ({COMPOSITE.stat().st_size // 1024} KB)…", flush=True)
img_url = fal_client.upload_file(str(COMPOSITE))
print(f"uploaded: {img_url}", flush=True)

t0 = time.time()
print("submitting to fal Kling 3.0 Pro image-to-video…", flush=True)

def on_queue_update(update):
    if hasattr(update, "logs"):
        for log in update.logs or []:
            print(f"  [{time.time() - t0:5.0f}s] {log.get('message', log)}", flush=True)

result = fal_client.subscribe(
    "fal-ai/kling-video/v3/pro/image-to-video",
    arguments={
        "prompt": PROMPT,
        "start_image_url": img_url,
        "end_image_url": img_url,
        "duration": "10",
        "aspect_ratio": "16:9",
        "audio": False,
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)

elapsed = time.time() - t0
print(f"\nresult keys: {list(result.keys())}", flush=True)

video_info = result.get("video") or {}
video_url = video_info.get("url") if isinstance(video_info, dict) else None

if not video_url:
    print(f"NO_VIDEO_URL, full result: {result}", flush=True)
    raise SystemExit(1)

print(f"downloading: {video_url}", flush=True)
import urllib.request
out_path = MASCOTS / "security_scene.KLING.mp4"
urllib.request.urlretrieve(video_url, str(out_path))
size_kb = out_path.stat().st_size // 1024
print(f"DONE ({size_kb} KB, {elapsed:.0f}s)", flush=True)
print(f"saved to: {out_path}", flush=True)
