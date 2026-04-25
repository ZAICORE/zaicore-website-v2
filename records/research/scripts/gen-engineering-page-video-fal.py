"""Engineering page video via fal.ai Seedance 2.0 image-to-video.

OpenRouter's Seedance queue is jammed (4 jobs stuck at pending for >1h).
fal.ai routes directly to ByteDance — different infrastructure, should
process normally.

Same narrative: fox works on robot panel → looks up at camera → back to work.
first frame and last frame both = engineering_page_start.png for loop close.
"""
import os, pathlib, sys, urllib.request
import fal_client

# Load FAL_KEY
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('FAL_KEY='):
        os.environ['FAL_KEY'] = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
START = MASCOTS / "engineering_page_start.png"
OUT   = MASCOTS / "engineering_page_scene.mp4"

print("uploading start frame to fal storage…", flush=True)
start_url = fal_client.upload_file(str(START))
print(f"  start_url: {start_url[:80]}", flush=True)

PROMPT = """STATIC LOCKED-OFF SHOT. The camera is bolted to a tripod and CANNOT MOVE. NO ZOOM, NO PAN, NO DOLLY, NO TILT, NO PUSH-IN, NO PULL-OUT, NO REFRAMING, NO RECOMPOSITION. The framing of frame 0 is IDENTICAL to the framing of every single subsequent frame, all the way to frame 6.0. This is a still character study with subtle internal animation — like a Pixar character idle loop captured by a security camera bolted to a wall. The fox + helper robot cluster stays in the EXACT same pixels in the bottom-right corner for every frame. The empty white studio space in the upper-left stays the EXACT same proportion of the frame for every frame.

Pixar 3D feature-film render. White studio background matching the input frame.

ONLY THESE THINGS MOVE — internal character animation only, never the camera:

[0–2.5s] The fox sits on the wooden stool, helper robot in his lap. Head tilted down, focused on the open access panel. Small careful paw movements — micro-adjustments inside the panel with his precision tool. Robot stays still.

[2.5–4s] Fox PAUSES the tool. Lifts his head, makes brief eye contact with the camera through his safety goggles, and gives a small ACKNOWLEDGING NOD — one clean head dip down then back up, like a "what's up" greeting nod. Warm, friendly expression during the nod. Robot stays still throughout.

[4–6s] Fox lowers his gaze back to the panel and resumes the tool work. Pose at frame 6.0 matches frame 0.0 EXACTLY — seamless loop.

ABSOLUTE NEGATIVES — these are deal-breakers:
- The camera does NOT move. Not even a tiny breath of motion. The video is locked-off.
- The framing does NOT change between any two frames. The scene fits in the frame the same way at all times.
- No zoom-in or zoom-out, even subtle. No dolly. No pan. No crane. No focus pulls.
- The cluster does NOT shrink or grow in apparent size. The empty white studio space in the upper-left stays exactly the same size.
- Fox's safety goggles stay DOWN over his eyes — they NEVER slide to his forehead.
- Robot stays still in fox's lap — does not animate, fly, or change pose.
- No additional characters appear.
- No audio, no soundtrack, no music."""

print("submitting fal seedance 2.0 image-to-video…", flush=True)

def on_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs or []:
            print(f"  [fal] {log.get('message','')}", flush=True)

result = fal_client.subscribe(
    "bytedance/seedance-2.0/image-to-video",
    arguments={
        "prompt": PROMPT,
        "image_url": start_url,
        "end_image_url": start_url,
        "resolution": "1080p",
        "duration": 6,
        "aspect_ratio": "16:9",
        "generate_audio": False,
    },
    with_logs=True,
    on_queue_update=on_update,
)

print(f"\nresult: {result}", flush=True)

video = result.get("video") or {}
video_url = video.get("url") if isinstance(video, dict) else result.get("video_url")
if not video_url:
    print("NO VIDEO URL in response; full result above.", flush=True)
    sys.exit(1)

print(f"downloading video from {video_url[:80]}…", flush=True)
urllib.request.urlretrieve(video_url, str(OUT))
size_mb = OUT.stat().st_size / 1024 / 1024
print(f"DONE — {size_mb:.1f} MB at {OUT}", flush=True)
