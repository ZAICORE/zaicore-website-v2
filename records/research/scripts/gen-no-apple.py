"""Regen owl_typing.png and scene_still.png without the Apple logo — generic silver laptop only."""
import os, json, base64, urllib.request, pathlib, time
from concurrent.futures import ThreadPoolExecutor, as_completed

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

OWL_BASE = "owl_reference"  # we'll use existing owl.png (no laptop in it) as reference, then compose

SPECS = [
    {
        "name": "owl_typing",
        "refs": [MASCOTS / "owl.png"],
        "ref_note": "Match this owl character exactly.",
        "prompt": (
            "A watchful snowy owl (matching the provided reference exactly) standing directly "
            "on a seamless white studio floor, no perch. In front of the owl is a small open "
            "silver aluminum laptop — generic minimalist design, smooth brushed metal finish, "
            "completely UNBRANDED with no logos, no markings, no symbols on any surface. "
            "The laptop is positioned so the owl looks at its screen: the BACK of the lid "
            "faces the viewer, with completely plain silver metal on the back — no logo, no "
            "text, no engraving, just smooth silver metal. The owl bends slightly forward, "
            "one talon lifted and tapping a key on the visible keyboard. Other talon grips the "
            "floor. Focused watchful expression, head tilted down to the screen. Wings folded. "
            "Pure white seamless studio background, soft floor shadow. Full body visible, "
            "centered. Classic 3D animated film render, soft subsurface scattering, warm "
            "cinematic lighting, film-grade quality. "
            "Image dimensions: 1024 wide by 1536 tall (2:3 vertical portrait). "
            "IMPORTANT: absolutely no brand logos of any kind on the laptop."
        ),
    },
    {
        "name": "scene_still",
        "refs": [MASCOTS / "fox_soldering.png"],  # owl ref will be regenerated in parallel
        "ref_note": "Match the fox character exactly (reference provided). For the owl, generate a snowy owl consistent with a Pixar-style cast.",
        "prompt": (
            "Wide cinematic composition in classic 3D animated film style, landscape aspect "
            "ratio (3:2 landscape approximation of 16:9). Pure white seamless studio — white "
            "floor, white background — with soft floor shadows.\n\n"
            "LEFT THIRD: A curious young fox (match the provided reference exactly, warm "
            "russet fur). Sits cross-legged on the white floor, wearing clear protective "
            "safety goggles DOWN OVER ITS EYES (actively worn). One paw holds a small chrome "
            "soldering iron with thin wisp of smoke. Other paw rests on small green circuit "
            "board in its lap. Focused, looking down at work. Faces slightly toward right.\n\n"
            "RIGHT THIRD: A snowy owl with pristine white feathers and yellow eyes, standing "
            "directly on the white floor (no perch). In front of the owl is a small open "
            "generic silver laptop — smooth brushed aluminum, COMPLETELY UNBRANDED, no logos "
            "or markings of any kind on any surface. The laptop's back lid (plain silver, "
            "NO LOGO) faces the viewer, screen faces the owl. Owl bends forward, one talon "
            "tapping the keyboard, other talon on floor. Focused, head tilted down. Faces "
            "slightly toward left.\n\n"
            "MIDDLE THIRD: EMPTY white space spanning about 40 percent of frame width. No "
            "objects, no text, no figures. Characters stay strictly in outer thirds.\n\n"
            "LIGHTING: Warm key from upper right, cool fill from upper left. Soft floor "
            "shadows. CAMERA: static eye-level wide shot. STYLE: classic 3D animated film "
            "quality, soft subsurface scattering, warm cinematic palette.\n\n"
            "Image dimensions: 1536 wide by 1024 tall (3:2 landscape — wide horizontal). "
            "CRITICAL: the laptop has NO logo, NO brand mark, NO symbols. Plain silver metal."
        ),
    },
]

def generate_one(spec):
    name = spec["name"]; t0 = time.time()
    content = [{"type": "text", "text": spec["ref_note"] + "\n\n" + spec["prompt"]}]
    for ref in spec["refs"]:
        content.append({"type": "image_url", "image_url": {"url": to_data_uri(ref)}})
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
        return name, f"FAILED: {e}", 0.0
    if "error" in data:
        return name, f"API_ERROR: {data['error']}", 0.0
    images = data["choices"][0]["message"].get("images", [])
    if not images:
        return name, "NO_IMAGE", 0.0
    png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
    (OUT / f"{name}.png").write_bytes(png)
    (MASCOTS / f"{name}.png").write_bytes(png)
    cost = data.get("usage", {}).get("cost", 0.0)
    return name, f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s)", cost

print("regen owl_typing + scene_still in parallel (no Apple/brand references)…", flush=True)
t0 = time.time(); total = 0.0
with ThreadPoolExecutor(max_workers=2) as pool:
    futures = {pool.submit(generate_one, s): s["name"] for s in SPECS}
    for fut in as_completed(futures):
        name, status, cost = fut.result(); total += cost
        print(f"[{name}] {status}  cost=${cost:.3f}", flush=True)
print(f"\nDONE in {time.time()-t0:.0f}s. total ${total:.3f}", flush=True)
