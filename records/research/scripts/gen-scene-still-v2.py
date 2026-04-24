"""Regenerate scene still — flip MacBook so the owl faces the screen, viewer sees back."""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

PROMPT = (
    "Create a wide cinematic composition in classic Pixar feature-film 3D animation style, "
    "16:9 horizontal landscape aspect ratio. Pure white seamless studio — white floor, white "
    "background — with soft natural floor shadows beneath each character.\n\n"
    "COMPOSITION (three equal thirds, more breathing room in the middle):\n\n"
    "LEFT THIRD — A curious young fox (match first reference image exactly, warm russet fur). "
    "Sits cross-legged on the white floor, wearing clear protective safety goggles positioned "
    "down over its eyes (not on forehead — the goggles are actively being worn in the correct "
    "working position). One paw holds a small chrome soldering iron with a thin wisp of smoke. "
    "The other paw rests on a small green circuit board in its lap. Focused expression, "
    "looking DOWN at its work. Fox faces slightly toward the right (toward the middle of "
    "the frame).\n\n"
    "RIGHT THIRD — A watchful snowy owl (match second reference image exactly). Stands "
    "directly on the white floor. In front of the owl is a small open MacBook-style laptop.\n\n"
    "CRITICAL LAPTOP ORIENTATION: The laptop is oriented so the OWL can see its screen. "
    "The screen faces AWAY from the viewer, toward the owl. The viewer's perspective looks "
    "at the BACK OF THE LAPTOP LID — meaning the Apple logo on the back of the lid is "
    "visible to the viewer. The owl is behind the laptop from the viewer's perspective, "
    "bent slightly forward to look at the screen (which the viewer cannot see because the "
    "screen faces the owl). One talon reaches down toward the keyboard, the other grips the "
    "floor. Focused watchful expression, head tilted down to the screen. Owl faces slightly "
    "toward the left (toward the middle of the frame).\n\n"
    "MIDDLE THIRD — INTENTIONALLY EMPTY SPACE spanning roughly 40% of the frame width. "
    "No objects, no text, no figures, no decoration. Just the clean seamless white floor "
    "and background. Both characters must stay inside their outer thirds — do not let them "
    "creep into this middle space.\n\n"
    "LIGHTING: Warm key from upper right, soft cool fill from upper left. Shallow depth of "
    "field. Realistic floor shadows beneath each character.\n\n"
    "CAMERA: Static eye-level wide shot. Framing: both characters fully in frame, feet "
    "touching lower third, heads in upper two-thirds.\n\n"
    "STYLE: Pixar feature-film render quality, soft subsurface scattering, rich dimensional "
    "lighting. Image dimensions: 1536 wide by 1024 tall (3:2 landscape approximation of "
    "16:9) — wide horizontal composition.\n\n"
    "The three thirds must read clearly: fox on left, empty white center, owl+laptop on "
    "right with laptop's back-of-lid (Apple logo side) facing the viewer."
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
print("regenerating scene still (laptop flipped, more middle breathing room)...", flush=True)
r = urllib.request.urlopen(req, timeout=300); data = json.load(r)
if "error" in data:
    print(f"ERROR: {data['error']}", flush=True); exit(1)
images = data["choices"][0]["message"].get("images", [])
if not images:
    print("no image", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
(OUT / "scene_still.png").write_bytes(png)
(MASCOTS / "scene_still.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"DONE ({len(png)//1024} KB, {time.time()-t0:.0f}s, ${cost:.3f})", flush=True)
