"""Regenerate robot without the WALL-E trigger. Describe the aesthetic only."""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT_STILLS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))

PROMPT = (
    "A small, endearing worker robot character in classic Pixar-animation style, fitting "
    "alongside a Pixar fox and owl in the same storybook cast. The robot is built from a "
    "weathered cube-shaped metal body with warm rust-and-mustard painted panels, visibly "
    "aged and dented like a beloved old tool. Two large expressive binocular-style eyes "
    "mounted on a short articulated neck stalk, giving a curious searching look. Two "
    "retractable rectangular metal arms ending in small three-fingered grippers. Below the "
    "boxy body, small caterpillar-track treads instead of legs or wheels — visible rubber "
    "tread pattern. A small tool (tiny brass wrench) held gently in one gripper, the other "
    "hand reaching slightly forward in a curious gesture. "
    "Color palette: warm earthy mustard yellow with rust-orange accents, chrome glints on "
    "the eye lenses, visible patina on the metal. "
    "Friendly, approachable, gentle — not intimidating, not military, not threatening. "
    "The feeling of an old helpful workshop companion. "
    "Standing calmly on a pure white seamless studio background, soft floor shadow. "
    "Full body visible head to treads, centered. "
    "Same Pixar feature-film render quality as the companion fox and owl characters: "
    "soft subsurface scattering on the metal, rich dimensional lighting, warm cinematic "
    "key-plus-fill lighting. "
    "Image dimensions: 1024 wide by 1536 tall (2:3 vertical portrait)."
)

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": [{"type": "text", "text": PROMPT}]}],
    "modalities": ["image", "text"],
}
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
t0 = time.time()
print("generating robot (safe prompt)...", flush=True)
r = urllib.request.urlopen(req, timeout=300)
data = json.load(r)
if "error" in data:
    print(f"ERROR: {data['error']}", flush=True); exit(1)
images = data["choices"][0]["message"].get("images", [])
if not images:
    print("no image", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
(OUT_STILLS / "robot_tinkerer.png").write_bytes(png)
(MASCOTS / "robot_tinkerer.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"DONE ({len(png)//1024} KB, {time.time()-t0:.0f}s, ${cost:.3f})", flush=True)
