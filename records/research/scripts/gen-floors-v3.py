"""v3 scene stills — fixes from v2 feedback:
- Hero: modern cubicle/office environment (not pure white void), robots at workstations
- Engineering: real modern server rack (not steampunk circuit-board tower)
- Security: robots watching a floating network visualization (not tower-being-tested)
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
    "round black rubber wheels. Some robots HOVER in the air using small softly-glowing "
    "blue thrusters on the underside of their bodies (wheels tucked in slightly when "
    "hovering, soft blue ion-glow visible beneath). Same character family across all. "
    "\n\nSTYLE: premium Pixar 3D animation feature-film render quality. Soft subsurface "
    "scattering on plastic, rich dimensional lighting, shallow depth of field, warm "
    "cinematic color grading. "
    "\n\nCRITICAL: Absolutely NO text, NO letters, NO numerals, NO signage, NO labels, "
    "NO readable words on screens, NO brand marks, NO writing of any kind anywhere. "
    "Screens and holographic panels show only ABSTRACT glowing wireframe geometry, "
    "luminous curves, waveforms, network diagrams, and particle flows — never text. "
    "\n\nImage dimensions: 1792 wide by 1024 tall (16:9 landscape)."
)

SPECS = [
    {
        "name": "scene_hero",
        "prompt": (
            "HERO SCENE — the ZAICORE main office floor. A bright modern open-plan AI "
            "company workspace, minimalist and clean. "
            "\n\nENVIRONMENT: Mostly bright white with light wood floor, very minimal "
            "so the scene still feels airy. A few low frosted-glass cubicle partitions "
            "(waist-height) define workstation clusters without cluttering the scene. "
            "Small modern desks with floating holographic monitors above them (the "
            "monitors show abstract glowing wireframe data visualizations and curves — "
            "NO text). A few wall-mounted brass accent lights add warmth. Very subtle "
            "hint of a large window with soft diffuse daylight on one side. NOT a "
            "detailed architectural scene — the space feels like a clean backdrop to "
            "the robots, not a competing subject. "
            "\n\nCAST: 10-12 cream-and-gold helper robots (matching reference) across "
            "the floor in natural working poses. "
            "- 3 robots seated-equivalent at desks behind low glass partitions, each "
            "interacting with a floating holographic display above their desk. "
            "- 2 robots gathered around a single desk in the center-middle, one "
            "pointing at a floating hologram, the other watching. "
            "- 2 robots HOVERING with blue thrusters above the scene, moving between "
            "cubicles, carrying small floating holographic documents. "
            "- 2 robots walking calmly on their wheels between stations on the floor. "
            "- 1 robot at a larger collaborative display on the right, pointing out "
            "something on a floating wireframe project. "
            "\n\nCOMPOSITION: All robots anchored in the bottom two-thirds of the "
            "frame. The top third stays fairly clean (soft daylight, minimal content) "
            "so a wordmark overlay sits cleanly above. Shallow depth of field on two "
            "or three foreground robots. Warm key light with cool fill. "
            "\n\nFeel: calm, alive, productive — the ZAICORE AI workforce at work."
        ),
    },
    {
        "name": "scene_engineering",
        "prompt": (
            "ENGINEERING SCENE — a team of cream-and-gold helper robots building a "
            "tall modern server rack. Pure white seamless studio background, simple and "
            "clean. "
            "\n\nTHE OBJECT (left-biased — occupying the left 35% of the frame): A "
            "tall modern server rack / compute tower rising from the floor to about "
            "75% of frame height. Sleek brushed-aluminum and dark-anodized chassis. "
            "Stacked horizontal server blades with small LED indicator lights (amber "
            "and cool-white, no text on them). Subtle cable management visible on one "
            "side (tidy bundles of colored fiber and copper cables). Cooling fin "
            "details. A few blades are still being installed, so the rack looks "
            "partially assembled — authentically mid-build. Recognizably MODERN DATA "
            "CENTER HARDWARE, not sci-fi circuitry. "
            "\n\nCAST (6 robots, varied heights around the rack): "
            "- 2 robots on the floor at the base, on wheels, one handing a server "
            "blade up to another who is sliding it into the rack. "
            "- 2 robots HOVERING with blue thrusters at mid-height, working on "
            "middle bays — one connecting cables, one securing a blade. "
            "- 1 robot HOVERING near the top of the rack, installing the topmost "
            "blade. "
            "- 1 robot on the floor to the right of the rack, on wheels, holding a "
            "translucent floating holographic blueprint showing abstract wireframe "
            "diagrams (NO text), consulting it. "
            "\n\nCOMPOSITION: The right 60% of the frame is clean empty white space "
            "(for body-copy overlay). Soft amber key light with cool fill. Warm glow "
            "from the LED indicators radiates onto the white floor near the rack. "
            "Shallow depth of field on the working robots. "
            "\n\nFeel: focused modern engineering, real hardware, real work."
        ),
    },
    {
        "name": "scene_security",
        "prompt": (
            "SECURITY SCENE — a team of cream-and-gold helper robots overseeing a "
            "floating network visualization. Pure white seamless studio background. "
            "\n\nTHE SUBJECT (right-biased — occupying the right 40% of the frame): A "
            "large FLOATING NETWORK VISUALIZATION hovering in the air about 1 meter "
            "off the ground. It is a luminous three-dimensional constellation of "
            "glowing nodes connected by thin streams of light — some nodes pulse warm "
            "amber, some pulse cool-white, and the connecting data-streams flow in "
            "visible particle-light trails between them. The network is roughly "
            "sphere-shaped, about 2 meters across, made entirely of light — it has no "
            "solid body, only points of light and connections. Some nodes are brighter "
            "than others, hinting at active traffic. NO text, NO labels on any node — "
            "just luminous geometry. "
            "\n\nCAST (6 robots, varied heights around the network): "
            "- 2 robots on the floor in front of the network, on wheels, watching it "
            "attentively — one with a pincer hand slightly raised as if tracing a "
            "data flow in the air. "
            "- 2 robots HOVERING with blue thrusters around the network at "
            "mid-height, on opposite sides — one reaching into the network with a "
            "pincer, examining a specific node closely, the other pointing at a node "
            "further along a data-stream. "
            "- 1 robot HOVERING above the top of the network, looking down through "
            "the full constellation. "
            "- 1 robot on the floor at the far left of the scene, on wheels, at a "
            "small floating holographic console with abstract glowing waveform "
            "signal curves (NO text). "
            "\n\nCOMPOSITION: The left 50% of the frame is clean empty white space "
            "(for body-copy overlay). Cool-neutral key light for a slightly cooler "
            "palette than the engineering scene, balanced by the warm amber pulses "
            "from the network visualization itself. Soft cool-blue accent glow from "
            "the holographic console. The network's luminance bathes the immediate "
            "floor in a soft mixed amber-and-cool glow. Shallow depth of field on "
            "the two nearest robots. "
            "\n\nFeel: vigilant, focused, watchful — overseeing the living system."
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
    (OUT / f"{name}_v3.png").write_bytes(png)
    (MASCOTS / f"{name}.png").write_bytes(png)
    cost = data.get("usage", {}).get("cost", 0.0)
    return name, f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s)", cost

print("generating 3 ZAICORE scene stills v3 — cubicles, server rack, network viz…", flush=True)
t0 = time.time(); total = 0.0
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(generate_one, s): s["name"] for s in SPECS}
    for fut in as_completed(futures):
        name, status, cost = fut.result(); total += cost
        print(f"[{name}] {status}  cost=${cost:.3f}", flush=True)
print(f"\nDONE in {time.time()-t0:.0f}s. total ${total:.3f}", flush=True)
print(f"saved to {MASCOTS}/", flush=True)
