"""Generate the 16:9 scene still that anchors the Seedance loop.
Fox soldering on left, owl at MacBook on right, empty middle for ZAICORE text overlay.
Uses fox.png and owl.png as multimodal reference images for character identity.
"""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT_STILLS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))

def to_data_uri(path: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"

PROMPT = (
    "Create a wide cinematic composition in classic Pixar feature-film 3D animation style, "
    "16:9 horizontal landscape aspect ratio. The scene is a pure white seamless studio — "
    "white floor, white background — with characters standing on it, soft natural floor "
    "shadows beneath each character.\n\n"
    "COMPOSITION (three equal thirds):\n"
    "LEFT THIRD — A curious young fox character (match the first provided reference image "
    "exactly — same fur color, face, proportions, warm russet tones). The fox sits "
    "cross-legged on the white floor, wearing clear protective safety goggles with a rubber "
    "strap around its head. One paw holds a small chrome soldering iron with a thin wisp "
    "of smoke curling upward. The other paw rests on a small green circuit board in its "
    "lap. Focused expression, looking down at its work, slight gentle smile. Positioned "
    "with the fox centered in the left third of the frame, facing toward the right (toward "
    "the middle of the frame).\n\n"
    "RIGHT THIRD — A watchful snowy owl character (match the second provided reference "
    "image exactly — same feathers, eyes, proportions, pristine white with subtle grey "
    "markings). The owl stands directly on the white floor (no perch). In front of the owl "
    "sits a small open laptop — silver brushed-aluminum MacBook style, lid open, screen "
    "glowing softly with a dark-themed security dashboard interface (subtle cyan accents). "
    "The owl bends slightly forward, one talon lifted and tapping a key. The other talon "
    "rests on the floor. Focused watchful expression, head tilted down to the screen. "
    "Positioned centered in the right third of the frame, facing toward the left (toward "
    "the middle of the frame).\n\n"
    "MIDDLE THIRD — INTENTIONALLY EMPTY SPACE between the two characters. No objects, "
    "no text, no figures, no decoration. Just the clean seamless white floor and white "
    "background. This negative space will be filled with title text as a post-production "
    "overlay. The characters on left and right do NOT extend into this middle space.\n\n"
    "LIGHTING: Warm key light from upper right, soft cool fill from upper left, shallow "
    "depth of field. Both characters fully visible head to floor. Soft realistic floor "
    "shadow under each character.\n\n"
    "CAMERA: Static eye-level wide shot, no pan or zoom. Framing: both characters fully "
    "in frame, their feet touching the bottom third of the frame, their heads in the top "
    "two-thirds.\n\n"
    "STYLE: Pixar feature-film render quality, soft subsurface scattering on fur and "
    "feathers, rich dimensional lighting, warm cinematic palette.\n\n"
    "Image dimensions: 1536 wide by 1024 tall (3:2 landscape) OR 1792 wide by 1024 tall "
    "if 16:9 is supported. Seamless white studio background throughout."
)

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": to_data_uri(MASCOTS / "fox_soldering.png")}},
    {"type": "image_url", "image_url": {"url": to_data_uri(MASCOTS / "owl_typing.png")}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
t0 = time.time()
print("generating scene still (16:9, fox left + owl right + empty middle)...", flush=True)
r = urllib.request.urlopen(req, timeout=300)
data = json.load(r)
if "error" in data:
    print(f"ERROR: {data['error']}", flush=True); exit(1)
images = data["choices"][0]["message"].get("images", [])
if not images:
    print(f"no image; content preview: {data['choices'][0]['message'].get('content','')[:200]}", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
(OUT_STILLS / "scene_still.png").write_bytes(png)
(MASCOTS / "scene_still.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"DONE ({len(png)//1024} KB, {time.time()-t0:.0f}s, ${cost:.3f})", flush=True)
