"""Regenerate stills with user feedback:
  - Fox: safety GOGGLES not glasses
  - Owl: on a MacBook-style laptop, no perch
  - Robot: WALL-E style, not brass tinkerer
"""
import os, json, base64, urllib.request, pathlib, time
from concurrent.futures import ThreadPoolExecutor, as_completed

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT_STILLS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))

def to_data_uri(path: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"

BASE = (
    "Classic Disney-Pixar 3D character render, Pixar feature-film quality. "
    "Soft subsurface scattering, rich dimensional lighting, warm key light with cool fill, "
    "shallow depth of field, cinematic quality. Large expressive eyes with genuine personality. "
    "Pure white seamless studio background, soft floor shadow. Full body visible head to feet, "
    "character takes up most of the vertical frame, centered. "
    "Image dimensions: 1024 wide by 1536 tall (2:3 vertical portrait). Film-grade Pixar render."
)

SPECS = [
    {
        "name": "fox_soldering",
        "ref_path": MASCOTS / "fox.png",
        "ref_note": "Match this fox character exactly — same fur color, face, proportions, expression style.",
        "prompt": (
            "A curious young fox (matching the provided reference character exactly) sitting "
            "cross-legged on a seamless white studio floor. The fox is wearing protective SAFETY "
            "GOGGLES — clear lenses, rubber strap around its head, visible and distinctly worn "
            "for workshop work. In its right paw it holds a small chrome soldering iron with a "
            "thin wisp of smoke curling upward from the tip. In its lap rests a small green "
            "circuit board it is carefully working on. Focused, thoughtful expression, looking "
            "down at its work, slight gentle smile. The goggles should be prominent and clearly "
            "visible — this is a maker who takes safety seriously. "
            + BASE
        ),
    },
    {
        "name": "owl_typing",
        "ref_path": MASCOTS / "owl.png",
        "ref_note": "Match this owl character exactly — same feathers, eyes, proportions, style.",
        "prompt": (
            "A watchful snowy owl (matching the provided reference character exactly) standing "
            "on a seamless white studio floor. In front of the owl is a small open laptop — "
            "silver brushed-aluminum MacBook-style, lid open, screen glowing softly with a "
            "dark security dashboard interface (subtle cyan accents). The owl is bent forward "
            "slightly, one talon lifted and delicately tapping a key on the laptop keyboard. "
            "The other talon is on the floor. Focused, watchful expression, head tilted down "
            "to look at the glowing screen. Wings folded neatly. No perch — the owl is standing "
            "directly on the floor. The laptop is small enough to fit comfortably in front of "
            "the owl. "
            + BASE
        ),
    },
    {
        "name": "robot_tinkerer",
        "ref_path": None,
        "ref_note": None,
        "prompt": (
            "A small friendly robot character in the style of WALL-E from Pixar — cube-shaped "
            "weathered body with warm rust-and-yellow painted metal showing age and dents, "
            "two large expressive binocular-style eyes on an articulated stalk/neck mechanism, "
            "rectangular retractable arms with three-fingered grippers, small caterpillar "
            "treads for feet (not wheels), a small curious and kind expression in the eyes. "
            "Warm earthy color palette — muted yellows, rust orange, metal patina. Holding a "
            "small tool (tiny wrench or spark-gauge) in one gripper. Standing calmly, full "
            "body visible, centered on pure white seamless studio background, soft floor "
            "shadow. Endearing, helpful, not intimidating — directly evoking WALL-E's warmth "
            "and curiosity. Same storybook Pixar cast aesthetic as a fox and owl. "
            "Image dimensions: 1024 wide by 1536 tall (2:3 vertical portrait). "
            "Film-grade Pixar render quality, subsurface lighting, cinematic."
        ),
    },
]

def generate_one(spec):
    name = spec["name"]; t0 = time.time()
    content = [{"type": "text", "text": spec["prompt"]}]
    if spec["ref_path"] is not None:
        content[0]["text"] = spec["ref_note"] + "\n\n" + content[0]["text"]
        content.append({"type": "image_url", "image_url": {"url": to_data_uri(spec["ref_path"])}})
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
    try:
        r = urllib.request.urlopen(req, timeout=300); data = json.load(r)
    except Exception as e:
        return name, f"REQUEST_FAILED: {e}", 0.0
    if "error" in data:
        return name, f"API_ERROR: {data['error']}", 0.0
    images = data["choices"][0]["message"].get("images", [])
    if not images:
        return name, "NO_IMAGE", 0.0
    png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
    (OUT_STILLS / f"{name}.png").write_bytes(png)
    (MASCOTS / f"{name}.png").write_bytes(png)
    cost = data.get("usage", {}).get("cost", 0.0)
    return name, f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s)", cost

print("firing 3 requests in parallel…", flush=True)
t0 = time.time(); total = 0.0
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(generate_one, s): s["name"] for s in SPECS}
    for fut in as_completed(futures):
        name, status, cost = fut.result(); total += cost
        print(f"[{name}] {status}  cost=${cost:.3f}", flush=True)
print(f"\nDONE in {time.time()-t0:.0f}s. total ${total:.3f}", flush=True)
