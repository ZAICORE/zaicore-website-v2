"""Regen security video via fal Seedance 2.0 reference-to-video.
- @Image1 = the composite still (anchor for first/last frame, exact pixels).
- @Video1 = the approved clip (motion + narrative reference).
- Prompt: camera welded in place, no settle, no bounce, first frame =
  composite pixels exactly, loop back to that pose cleanly.
"""
import os, pathlib, time
import fal_client

for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('FAL_KEY='):
        os.environ['FAL_KEY'] = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
REF_IMAGE = MASCOTS / "security_with_robots.png"
REF_VIDEO = MASCOTS / "security_scene.APPROVED.mp4"

PROMPT = """Generate a 10-second cinematic Pixar 3D video.

FRAME 0 MUST BE PIXEL-EXACT TO @Image1. No adjustment, no zoom-in, no fade-in, no settle-in, no framing correction on the first frame. The very first rendered frame is @Image1 exactly.

THE CAMERA IS ABSOLUTELY WELDED IN PLACE. Zero pan, zero tilt, zero zoom, zero dolly, zero shake, zero bounce, zero framing adjustment for the entire 10 seconds. No camera movement whatsoever. Think of the camera as bolted to a concrete wall pointed at the scene. The framing at frame 0 is IDENTICAL to the framing at every frame through frame 240. Especially: no subtle "come-in" or settling effect on the opening frames.

USE @Video1 as the exact motion reference for the narrative and character action: the middle robot's eye turns red, the owl snatches it with a wing, flings it spiraling into the background, the remaining two robots continue rightward and fly off the right edge of the glass conveyor belt, and three fresh robots slide in from the left to close the loop. Preserve the scene (lower-left composition, cream background, flat glass conveyor, owl behind, robots on it).

THE FINAL FRAME MUST BE PIXEL-EXACT TO @Image1 again so the loop is seamless.

Output: 10 seconds, 16:9, 1080p, no audio, pristine h264, camera perfectly still throughout."""

print(f"uploading reference image ({REF_IMAGE.stat().st_size // 1024} KB)…", flush=True)
img_url = fal_client.upload_file(str(REF_IMAGE))
print(f"image: {img_url}", flush=True)

print(f"uploading reference video ({REF_VIDEO.stat().st_size // 1024} KB)…", flush=True)
vid_url = fal_client.upload_file(str(REF_VIDEO))
print(f"video: {vid_url}", flush=True)

t0 = time.time()
print("submitting to fal seedance-2.0 reference-to-video…", flush=True)

def on_queue_update(update):
    if hasattr(update, "logs"):
        for log in update.logs or []:
            print(f"  [{time.time() - t0:5.0f}s] {log.get('message', log)}", flush=True)

result = fal_client.subscribe(
    "bytedance/seedance-2.0/reference-to-video",
    arguments={
        "prompt": PROMPT,
        "image_urls": [img_url],
        "video_urls": [vid_url],
        "resolution": "1080p",
        "duration": "10",
        "aspect_ratio": "16:9",
        "generate_audio": False,
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)

elapsed = time.time() - t0
video_info = result.get("video") or {}
video_url = video_info.get("url") if isinstance(video_info, dict) else None

if not video_url:
    print(f"NO_VIDEO_URL, full result: {result}", flush=True)
    raise SystemExit(1)

print(f"\ndownloading: {video_url}", flush=True)
import urllib.request
out_path = MASCOTS / "security_scene.FAL_LOCK.mp4"
urllib.request.urlretrieve(video_url, str(out_path))
size_kb = out_path.stat().st_size // 1024
print(f"DONE ({size_kb} KB, {elapsed:.0f}s)", flush=True)
print(f"saved to: {out_path}", flush=True)
