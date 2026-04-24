"""Fix the security video camera-bounce at the loop end using fal's
Seedance 2.0 reference-to-video endpoint.

Feeds the APPROVED clip as reference. Prompt tells the model to recreate
the exact same scene/motion/characters but with a rock-steady camera —
no bounce, no jolt, no snap-to-last-frame correction at the end.
"""
import os, pathlib, time
import fal_client

for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('FAL_KEY='):
        os.environ['FAL_KEY'] = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
REF_VIDEO = MASCOTS / "security_scene.APPROVED.mp4"

PROMPT = """Recreate the EXACT scene, narrative, and character motion shown in @Video1 with zero changes to: the owl's identity and appearance, the three robots' identity and appearance, the glass conveyor belt, the composition (content in lower-left quadrant, right 55% empty cream, upper 50% empty cream), the camera framing, the wing-snatch action, the robot spiraling into the background, the two remaining robots flying off the right edge, and the three fresh robots sliding in from the left to close the loop.

THE ONLY CHANGE: camera is absolutely locked — zero pan, zero tilt, zero zoom, zero dolly, zero bounce, zero shake, zero framing adjustment. Crucially: no snap, no jolt, no zoom-correction at the END of the clip. Framing at frame 0 is identical to framing at the final frame. Think locked-off tripod for the entire 10 seconds. The end state settles naturally without any camera adjustment and loops back cleanly to the starting frame."""

print(f"uploading reference video ({REF_VIDEO.stat().st_size // 1024} KB)…", flush=True)
ref_url = fal_client.upload_file(str(REF_VIDEO))
print(f"uploaded: {ref_url}", flush=True)

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
        "video_urls": [ref_url],
        "resolution": "1080p",
        "duration": "10",
        "aspect_ratio": "16:9",
        "generate_audio": False,
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
out_path = MASCOTS / "security_scene.FAL.mp4"
urllib.request.urlretrieve(video_url, str(out_path))
size_kb = out_path.stat().st_size // 1024
print(f"\nDONE ({size_kb} KB, {elapsed:.0f}s total)", flush=True)
print(f"saved to: {out_path}", flush=True)
