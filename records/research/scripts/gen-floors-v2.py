"""Generate v2 of ZAICORE scene stills — white studio, NOT architectural.

Revisions after v1 feedback:
- Back to pure white seamless studio (architecture was too much)
- Hero: horizontal, robots anchored along bottom, some hovering, clean space above for wordmark
- Engineering: vertical tall object on LEFT side of frame, robots at multiple heights
- Security: vertical tall object on RIGHT side of frame (same object, now testing)
- Some robots hover with small blue thrusters to reach upper parts
- Clean empty white space for wordmark/body copy overlay
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

ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

REF_NOTE = (
    "The helper robots in this scene must match the provided reference image exactly — "
    "cream-white pill-shaped bodies with matte plastic finish, rounded dome heads with a "
    "single large glowing amber camera-lens eye (not binocular), rounded arms ending in "
    "soft pincer hands, slim gold accent band around the middle, rolling on two small "
    "round black rubber wheels. Some robots in this scene HOVER in the air using small "
    "softly-glowing blue thrusters on the underside of their bodies (the wheels tuck in "
    "slightly when hovering, and a soft blue ion-glow is visible beneath the hovering "
    "robots). Same character family, same render style across all robots. "
    "\n\nBACKGROUND: Pure white seamless studio — infinite white, no walls, no windows, "
    "no architecture, no objects beyond what's specified. Soft grounded floor shadows "
    "under each robot. "
    "\n\nSTYLE: premium Pixar 3D animation feature-film render quality. Soft subsurface "
    "scattering on plastic and materials, rich dimensional lighting, shallow depth of "
    "field, warm cinematic color grading. "
    "\n\nCRITICAL: Absolutely NO text, NO letters, NO numerals, NO signage, NO labels, "
    "NO readable words on screens or blueprints, NO brand marks, NO writing of any kind "
    "anywhere. Screens and blueprints show only ABSTRACT glowing wireframe geometry, "
    "luminous curves, waveforms, and particle flows — never text. "
    "\n\nImage dimensions: 1792 wide by 1024 tall (16:9 landscape)."
)

SPECS = [
    {
        "name": "scene_hero",
        "prompt": (
            "HERO SCENE — the management / overview moment. Pure white seamless studio. "
            "A team of 10 cream-and-gold helper robots working together, anchored ALONG "
            "THE BOTTOM THIRD of the frame. "
            "\n\nCOMPOSITION: All robots stay in the bottom third of the frame. The top "
            "two-thirds of the frame is clean empty white space (reserved for a wordmark "
            "overlay). "
            "\n\nACTION: Across the bottom third, from left to right: "
            "- 2 robots on the left, on their wheels, operating a small floating "
            "holographic panel at hip height showing abstract glowing wireframe "
            "geometry. "
            "- 2 robots in the center-bottom gathered around a small floating "
            "holographic project — a luminous rotating wireframe shape — with one robot "
            "pointing, one robot watching thoughtfully. "
            "- 2 robots HOVERING above the center group using glowing blue thrusters "
            "under their bodies, at about mid-frame height, examining the project from "
            "above. "
            "- 2 robots on the right, on their wheels, at another small floating "
            "holographic display with abstract glowing data curves. "
            "- 2 robots walking calmly across the scene between stations. "
            "\n\nLIGHTING: Soft warm key light from upper right, cool fill from upper "
            "left. Subtle amber glows from the floating holographic displays. Grounded "
            "floor shadows. Shallow depth of field on the center robots. "
            "\n\nThis scene should feel calm, intelligent, collaborative — the AI "
            "collective at work."
        ),
    },
    {
        "name": "scene_engineering",
        "prompt": (
            "ENGINEERING SCENE — the build moment. Pure white seamless studio. A team "
            "of 6 cream-and-gold helper robots building a TALL precision object on the "
            "LEFT SIDE of the frame. "
            "\n\nCOMPOSITION: The subject is LEFT-BIASED — the tall object stands on "
            "the left side of the frame (occupying roughly the left 35% of the frame "
            "width). The RIGHT SIDE of the frame (roughly 60% of the width) is clean "
            "empty white space (reserved for body-copy overlay). "
            "\n\nTHE OBJECT: A tall vertical precision structure rising from the floor "
            "to about 75% of the frame height. Recognizably a sophisticated piece of "
            "technology: stacked circuit-board panels with glowing amber traces, brass "
            "gears and linkages connecting the levels, small glowing orb components, "
            "delicate copper wire bundles running vertically, visible structural "
            "scaffold details — like a miniature beautiful tech tower under "
            "construction, partially assembled. The object sits on the white floor. "
            "\n\nACTION: 6 robots building at varied heights: "
            "- 2 robots on the floor at the base, on their wheels, leaning in with "
            "small soldering irons (thin wisps of smoke curling from the tips), "
            "soldering delicate connections at the bottom levels. "
            "- 2 robots HOVERING with soft blue thrusters at mid-height, reaching in "
            "with small pincer tools to assemble middle sections of the object. "
            "- 1 robot HOVERING near the top of the object, both hands placing a small "
            "component into the top structure. "
            "- 1 robot on the floor to the right of the object, on its wheels, holding "
            "up a translucent floating blueprint showing abstract glowing wireframe "
            "schematics (NO text), looking from the blueprint to the object. "
            "\n\nLIGHTING: Warm amber accent light radiating from the object's glowing "
            "components casts a subtle warm gradient onto the white floor around it. "
            "Soft cool fill from upper right. Grounded shadows. Shallow depth of field "
            "on two of the working robots. "
            "\n\nFeeling: focused craftsmanship, teamwork, precision."
        ),
    },
    {
        "name": "scene_security",
        "prompt": (
            "SECURITY SCENE — the testing and hardening moment. Pure white seamless "
            "studio. A team of 6 cream-and-gold helper robots inspecting and testing "
            "the SAME tall precision object from engineering, now complete and being "
            "verified. The object is on the RIGHT SIDE of the frame. "
            "\n\nCOMPOSITION: The subject is RIGHT-BIASED — the tall object stands on "
            "the right side of the frame (occupying roughly the right 35% of the frame "
            "width). The LEFT SIDE of the frame (roughly 60% of the width) is clean "
            "empty white space (reserved for body-copy overlay). "
            "\n\nTHE OBJECT: The same tall vertical precision structure from the "
            "engineering scene — stacked circuit-board panels with glowing amber "
            "traces, brass gears and linkages, copper wire bundles, delicate "
            "components — now COMPLETE and sitting on a minimal polished brushed-metal "
            "inspection pedestal. The object is pristine, glowing softly, rising about "
            "75% of frame height. "
            "\n\nACTION: 6 robots testing at varied heights: "
            "- 2 robots on the floor at the base of the pedestal, on their wheels, "
            "leaning in with slender brass probes examining seams at the bottom "
            "levels of the object. "
            "- 2 robots HOVERING with soft blue thrusters at mid-height, casting "
            "warm amber scanning-beams across the middle sections of the object. "
            "- 1 robot HOVERING near the top of the object, examining the uppermost "
            "components with a brass probe. "
            "- 1 robot on the floor to the left of the object, on its wheels, at a "
            "small floating holographic console showing abstract glowing waveform "
            "visualizations and signal curves (NO text, only luminous curves). "
            "\n\nLIGHTING: Cool-neutral key light from upper left creates a slightly "
            "cooler palette than the engineering scene, balanced by the warm amber "
            "scanning-beams from the hovering robots and the object's own glowing "
            "components. Subtle cool-blue accent glow from the monitoring console. "
            "Grounded shadows. Shallow depth of field on the testing robots. "
            "\n\nFeeling: watchful, methodical, careful — hardening the work."
        ),
    },
]

def generate_one(spec):
    name = spec["name"]; t0 = time.time()
    content = [{"type": "text", "text": REF_NOTE + "\n\n" + spec["prompt"]}]
    content.append({"type": "image_url", "image_url": {"url": ROBOT_REF}})
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

print("generating 3 ZAICORE scene stills v2 — white studio, cleaner layouts…", flush=True)
t0 = time.time(); total = 0.0
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(generate_one, s): s["name"] for s in SPECS}
    for fut in as_completed(futures):
        name, status, cost = fut.result(); total += cost
        print(f"[{name}] {status}  cost=${cost:.3f}", flush=True)
print(f"\nDONE in {time.time()-t0:.0f}s. total ${total:.3f}", flush=True)
print(f"saved to {MASCOTS}/", flush=True)
