"""v4 hero scene only — strict white void, robots in horizontal band along bottom.

Fix from v3: kill the office architecture entirely. No walls, no floor patterning,
no windows, no furniture, no wood — pure white seamless studio. Robots work in a
2D-ish horizontal band along the bottom third. Each robot has its own floating
holographic workstation at hip height. Some walk between stations, some hover
briefly above.
"""
import os, json, base64, urllib.request, pathlib, time

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

PROMPT = (
    "The helper robots must match the provided reference image exactly — cream-white "
    "pill-shaped bodies with matte plastic finish, rounded dome heads with a single "
    "large glowing amber camera-lens eye, rounded arms ending in soft pincer hands, "
    "slim gold accent band around the middle, rolling on two small round black rubber "
    "wheels. Some robots HOVER in the air using small softly-glowing blue thrusters on "
    "the underside of their bodies. Same character family across all. "
    "\n\nSTYLE: premium Pixar 3D animation feature-film render quality. Soft subsurface "
    "scattering, shallow depth of field, warm cinematic lighting. "
    "\n\nBACKGROUND: ABSOLUTELY PURE WHITE SEAMLESS STUDIO — infinite white, NO walls, "
    "NO windows, NO architecture, NO wooden floor, NO furniture, NO desks, NO cubicle "
    "partitions, NO wall art, NO plants, NO objects in the background of ANY kind. Just "
    "pure white. Soft grounded floor shadows under each robot is the only indication "
    "of a floor. "
    "\n\nNO TEXT, NO letters, NO numerals, NO signage, NO labels, NO readable words on "
    "screens or holograms, NO writing of any kind anywhere. All floating holograms show "
    "only ABSTRACT luminous wireframe geometry, glowing curves, and particle flows. "
    "\n\nImage dimensions: 1792 wide by 1024 tall (16:9 landscape). "
    "\n\nCOMPOSITION: Strict 2D-ish horizontal band along the BOTTOM THIRD of the "
    "frame. ALL robots must be positioned within the bottom third vertically. The top "
    "TWO-THIRDS of the frame is pure empty white space (reserved for a wordmark "
    "overlay). Think of it as a frieze or a horizontal strip of activity along the "
    "bottom of an otherwise empty canvas. "
    "\n\nSCENE — the ZAICORE AI workforce at work, distributed across the bottom band, "
    "each at their own workstation or moving between: "
    "\n\n"
    "LEFT SIDE OF BAND (left third): "
    "- 1 robot on its wheels facing forward, in front of a floating holographic "
    "control panel at hip-height showing abstract glowing wireframe geometry. "
    "- 1 robot on its wheels next to it, slightly further left, at another floating "
    "holographic panel with glowing data curves. "
    "- 1 robot walking on its wheels past them, moving toward the center, carrying a "
    "small floating holographic document. "
    "\n\n"
    "CENTER OF BAND (center third): "
    "- 2 robots on their wheels standing together in front of a slightly larger "
    "floating holographic display showing an abstract rotating wireframe object — one "
    "pointing at the hologram, the other watching thoughtfully. "
    "- 1 robot HOVERING with a soft blue thruster glow, positioned ABOVE the center "
    "robots but still within the lower half of the frame, crossing the scene from "
    "left to right, carrying a small floating holographic item. "
    "\n\n"
    "RIGHT SIDE OF BAND (right third): "
    "- 1 robot on its wheels in front of a floating holographic panel with abstract "
    "glowing network-diagram shapes. "
    "- 1 robot on its wheels next to it, leaning toward the same panel as if "
    "discussing what's on it. "
    "- 1 robot HOVERING with a soft blue thruster glow, in the lower-right, carrying "
    "a small floating holographic shape, moving across. "
    "\n\n"
    "Every floating holographic panel is waist-height to its robot, unsupported "
    "(floats in air), with soft warm amber glow emission. "
    "\n\nLIGHTING: Soft warm key light from upper right, cool fill from upper left. "
    "Subtle amber glows from the floating holograms cast a faint warm wash on the "
    "white floor near each station. Grounded shadows. Shallow depth of field with "
    "two or three center-foreground robots in sharpest focus. "
    "\n\nFeel: calm, alive, productive — the AI workforce in action, each at their "
    "station, some moving through, like watching a quiet hive of intelligent "
    "activity."
)

content = [{"type": "text", "text": PROMPT}]
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

print("generating hero v4 — strict white void, bottom-third band…", flush=True)
t0 = time.time()
r = urllib.request.urlopen(req, timeout=420)
data = json.load(r)
if "error" in data:
    print(f"API_ERROR: {data['error']}", flush=True); exit(1)
images = data["choices"][0]["message"].get("images", [])
if not images:
    print("NO_IMAGE", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
(OUT / "scene_hero_v4.png").write_bytes(png)
(MASCOTS / "scene_hero.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"DONE ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to {MASCOTS / 'scene_hero.png'}", flush=True)
