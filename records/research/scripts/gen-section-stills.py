"""Generate the engineering and security section stills in parallel.

Engineering: fox on LEFT at a larger workbench, 2-3 helper robots assisting.
Right 60% of frame clean for body copy.

Security: owl on RIGHT at a larger monitoring setup with floating screens,
2-3 helper robots assisting. Left 60% of frame clean for body copy.

Same warm off-white seamless studio as the hero so the scroll feels continuous.
"""
import os, json, base64, urllib.request, pathlib, time
from concurrent.futures import ThreadPoolExecutor, as_completed

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))
OUT.mkdir(parents=True, exist_ok=True)

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

FOX_REF = to_data_uri(MASCOTS / "fox_soldering.png")
OWL_REF = to_data_uri(MASCOTS / "owl_typing.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

SHARED_NOTE = (
    "Style: premium 3D cartoon feature-film render quality, warm cinematic lighting, "
    "soft subsurface scattering on fur, feathers, and plastic, shallow depth of field. "
    "\n\nBackground: warm off-white seamless studio (approximately #faf8f7 — subtle warm "
    "tone, NOT pure stark white). Infinite background, NO walls, NO windows, NO "
    "architecture, NO furniture beyond what is specified. Soft grounded floor shadows "
    "under each character. "
    "\n\nThe helper robots must match the provided robot reference exactly — cream-white "
    "pill-shaped bodies, matte plastic, rounded dome heads with a single glowing amber "
    "camera-lens eye, rounded arms ending in pincer hands, slim gold accent band, two "
    "small round black rubber wheels. Some robots HOVER using small softly-glowing blue "
    "thrusters on the underside of their bodies. "
    "\n\nCRITICAL: Absolutely NO text, NO letters, NO numerals, NO signage, NO labels, "
    "NO readable words on any screen or hologram, NO writing of any kind anywhere. All "
    "holograms and displays show only ABSTRACT glowing wireframe geometry, luminous "
    "curves, network diagrams, and particle flows. "
    "\n\nImage dimensions: 1792 wide by 1024 tall (16:9 landscape)."
)

SPECS = [
    {
        "name": "section_engineering",
        "refs": [FOX_REF, ROBOT_REF],
        "ref_note": "Match the provided fox character exactly (first reference). Helper robots match the provided robot reference exactly (second reference).",
        "prompt": (
            "ENGINEERING SECTION — the fox at work with AI helpers assisting. "
            "\n\nCOMPOSITION: left-biased. The fox and its workspace occupy the left 40% "
            "of the frame. The RIGHT 60% of the frame is clean empty warm off-white "
            "space (reserved for body copy overlay). "
            "\n\nMAIN SUBJECT (left side): The fox character (match reference exactly — "
            "warm russet fur, clear safety goggles DOWN over its eyes). The fox sits "
            "cross-legged on the warm off-white floor at a slightly larger workbench "
            "scene. In the fox's lap and in front of it: a more elaborate mid-build "
            "project — a complex but elegant circuit assembly with brass-edged panels, "
            "glowing amber traces, small polished components, and delicate copper "
            "linkages. The fox holds a chrome soldering iron in one paw, a thin wisp of "
            "smoke curling from the tip, and rests its other paw near a small green "
            "circuit board in its lap. Focused expression, looking down at work. "
            "\n\nHELPER ROBOTS (between fox and center, still within left 40%): TWO "
            "helper robots assisting the fox. "
            "- ROBOT ONE: HOVERING at mid-height with a visible soft blue thruster glow "
            "beneath it, positioned just above and to the right of the fox. It holds a "
            "small polished brass component in one pincer and extends it toward the fox "
            "as if offering it. "
            "- ROBOT TWO: on its wheels on the floor to the right of the fox, facing "
            "the fox, working on a small sub-assembly in its own pincer hands — "
            "contributing a piece to the larger build. "
            "\n\nLIGHTING: Warm golden-amber key light from upper left, cool fill from "
            "upper right. Subtle warm amber glow from the project's glowing components "
            "casts a soft warm wash on the floor near the fox. Shallow depth of field "
            "with the fox in sharpest focus. "
            "\n\nFeeling: focused craft, expert-plus-assistant collaboration."
        ),
    },
    {
        "name": "section_security",
        "refs": [OWL_REF, ROBOT_REF],
        "ref_note": "Match the provided owl character exactly (first reference). Helper robots match the provided robot reference exactly (second reference).",
        "prompt": (
            "SECURITY SECTION — the owl at her monitoring station with AI helpers assisting. "
            "\n\nCOMPOSITION: right-biased. The owl and her monitoring setup occupy the "
            "right 40% of the frame. The LEFT 60% of the frame is clean empty warm "
            "off-white space (reserved for body copy overlay). "
            "\n\nMAIN SUBJECT (right side): The owl character (match reference exactly — "
            "snowy owl, pristine white feathers, warm yellow eyes). The owl stands "
            "directly on the warm off-white floor in front of an elegant open silver "
            "aluminum laptop (completely UNBRANDED — no logos, plain silver back lid "
            "faces the viewer, screen faces the owl). Arrayed in the air around the "
            "owl at varied heights: 2-3 floating holographic display panels showing "
            "abstract luminous data visualizations — one with glowing waveform signal "
            "curves, one with a small glowing network-diagram of connected nodes, one "
            "with flowing luminous data streams (NO TEXT, NO numbers, NO readable "
            "content — only abstract glowing geometry). The owl's head is tilted "
            "alertly toward one of the floating holograms, one talon lifted slightly "
            "as if pointing to a detail. Focused, watchful, intelligent expression. "
            "\n\nHELPER ROBOTS (between owl and center, still within right 40%): TWO "
            "helper robots assisting the owl. "
            "- ROBOT ONE: HOVERING at mid-height with a visible soft blue thruster "
            "glow, positioned just to the left of the owl near one of the floating "
            "holograms. A pincer hand is extended toward the hologram as if tracing a "
            "data flow. "
            "- ROBOT TWO: on its wheels on the floor to the left of the owl, facing "
            "slightly toward the owl and her setup, with a small polished brass probe "
            "in one pincer hand raised as if examining something in the air. "
            "\n\nLIGHTING: Cooler-neutral key light from upper right, soft warm fill "
            "from upper left. Subtle cool-blue accent glow from the floating "
            "holograms balanced by a warm amber glow from the owl's laptop screen. "
            "Shallow depth of field with the owl in sharpest focus. The palette is "
            "slightly cooler than the engineering section but still warm and premium, "
            "never cold. "
            "\n\nFeeling: vigilant, watchful, expert-plus-assistant collaboration."
        ),
    },
]

def generate_one(spec):
    name = spec["name"]; t0 = time.time()
    content = [{"type": "text", "text": spec["ref_note"] + "\n\n" + SHARED_NOTE + "\n\n" + spec["prompt"]}]
    for ref in spec["refs"]:
        content.append({"type": "image_url", "image_url": {"url": ref}})
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
        r = urllib.request.urlopen(req, timeout=420); data = json.load(r)
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

print("generating engineering + security section stills in parallel...", flush=True)
t0 = time.time(); total = 0.0
with ThreadPoolExecutor(max_workers=2) as pool:
    futures = {pool.submit(generate_one, s): s["name"] for s in SPECS}
    for fut in as_completed(futures):
        name, status, cost = fut.result(); total += cost
        print(f"[{name}] {status}  cost=${cost:.3f}", flush=True)
print(f"\nDONE in {time.time()-t0:.0f}s. total ${total:.3f}", flush=True)
print(f"saved to {MASCOTS}/", flush=True)
