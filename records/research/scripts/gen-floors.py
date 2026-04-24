"""Generate the 3 ZAICORE building floor reference stills in parallel.

Each floor feeds robot_tinkerer.png as an input_reference so the robot design
is consistent across floors. No text or lettering anywhere in any scene.
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
    "round black rubber wheels. Same character family, same render style. "
    "\n\nStyle: premium Pixar 3D animation feature-film render quality. Soft subsurface "
    "scattering on plastic and materials, rich dimensional lighting, shallow depth of "
    "field, warm cinematic color grading, film-grade craft. "
    "\n\nCRITICAL: Absolutely NO text, NO letters, NO numerals, NO signage, NO labels, "
    "NO readable words on screens, NO brand marks, NO writing of any kind anywhere in "
    "the scene. Every surface is pure material. Screens show only abstract glowing data "
    "visualizations or wireframe shapes, never text. "
    "\n\nImage dimensions: 1792 wide by 1024 tall (16:9 landscape)."
)

SPECS = [
    {
        "name": "floor_management",
        "prompt": (
            "Wide cinematic interior shot of the TOP FLOOR of a beautiful ZAICORE "
            "building — a command/management floor where the AI orchestrates the entire "
            "operation. "
            "\n\nARCHITECTURE: High ceilings, floor-to-ceiling windows along one wall "
            "letting in warm dawn light. Warm wood flooring, exposed warm wood ceiling "
            "beams, matte concrete accent walls, brass pendant lights hanging at "
            "varied heights, glass partition walls in places. Kengo Kuma meets Apple "
            "Park architectural language. "
            "\n\nCAST: Approximately 15-18 cream-and-gold helper robots (matching the "
            "reference exactly) distributed across the floor in natural working poses. "
            "Some groups of 3-4 robots at circular workstations arranged around the "
            "room — each workstation has several floating holographic panels in the air "
            "above it showing ABSTRACT glowing data visualizations (luminous curves, "
            "wireframe geometry, particle flows — NO text, NO numbers, NO writing of any "
            "kind). A central large holographic display at the middle of the room "
            "projects a slowly rotating abstract wireframe of a complex assembly — like "
            "a blueprint in light. Two or three robots gather thoughtfully around this "
            "central display. Other robots walk calmly between stations carrying tablets "
            "or small brass instruments (no text on tablets — just glowing abstract "
            "UI elements). "
            "\n\nKEY DETAIL: A wide open railing on one side of the floor reveals a "
            "partial view DOWN into the next floor below — a hint of warm workshop "
            "activity visible through the opening, establishing this as the top of a "
            "multi-floor building. "
            "\n\nLIGHTING: Warm golden dawn light from the windows, brass pendants add "
            "pools of warm fill light, subtle atmospheric haze catches the light rays. "
            "Shallow depth of field with the foreground robot sharp. "
            "\n\nThis floor feels like the bright, calm, intelligent brain of the whole "
            "ZAICORE operation."
        ),
    },
    {
        "name": "floor_engineering",
        "prompt": (
            "Wide cinematic interior shot of the ENGINEERING FLOOR of the ZAICORE "
            "building — a craftsman-style workshop where a team of helper robots is "
            "building one precision object together. "
            "\n\nARCHITECTURE: Warm wood workbench running across the center of the "
            "frame as the clear focal point. Brass pendant lights hanging directly above "
            "the workbench, pooling warm amber light onto the work surface. Exposed "
            "warm wood ceiling beams, wood shelving lined with precision tools (tiny "
            "brass wrenches, calipers, small screwdrivers, coiled copper wire — no "
            "labels on anything). Matte concrete walls. Warm amber afternoon sunlight "
            "pouring in from tall windows on the left side. "
            "\n\nCAST AND ACTION: SIX cream-and-gold helper robots (matching the "
            "reference exactly) gathered closely around the central workbench, all "
            "focused on ONE complex beautiful precision object in the middle of the "
            "bench — a mechanical-electronic assembly featuring brass gears, glowing "
            "amber circuit-board panels, delicate linkages, polished components. The "
            "object is the star of the scene. "
            "Robot 1: leaning in with a small soldering iron, a thin wisp of smoke "
            "curling from its tip, soldering a delicate connection. "
            "Robot 2: opposite Robot 1, also soldering a different connection on the "
            "same object. "
            "Robot 3: holding up a translucent vellum blueprint showing ABSTRACT "
            "technical schematic diagrams — wireframe geometry, flowing curves, nodes "
            "and lines (absolutely NO text, NO numbers, NO lettering — pure visual "
            "schematic only). "
            "Robot 4: next to Robot 3, pointing at a detail on the blueprint. "
            "Robot 5: measuring the object with small polished brass calipers. "
            "Robot 6: adjusting a small component on the object with a tiny brass "
            "wrench. "
            "All robots exhibit focused, absorbed body language (head tilted toward "
            "work, bodies leaned in). "
            "\n\nATMOSPHERE: A few fine wood shavings and tool detritus scattered on "
            "the workbench — lived-in, worked-in. Warm golden amber dominant palette. "
            "Shallow depth of field with the object and two nearest robots in sharpest "
            "focus. "
            "\n\nThis floor feels warm, dedicated, craftsmanlike — the hands of the "
            "ZAICORE operation."
        ),
    },
    {
        "name": "floor_security",
        "prompt": (
            "Wide cinematic interior shot of the SECURITY AND INSPECTION FLOOR of the "
            "ZAICORE building — where a team of helper robots tests and hardens what "
            "was built on the engineering floor above. "
            "\n\nARCHITECTURE: Same architectural DNA as the engineering floor (warm "
            "wood accents, brass fixtures, matte concrete walls) but the palette is "
            "noticeably cooler and cleaner here — polished metal inspection surfaces, "
            "glass panel enclosures, ceramic-tiled inspection bay floor. A large "
            "skylight overhead casts cool neutral-white daylight onto the inspection "
            "space. A central polished brushed-metal inspection pedestal is the clear "
            "focal point. "
            "\n\nCAST AND ACTION: SIX cream-and-gold helper robots (matching the "
            "reference exactly, same family as other floors) gathered around the "
            "central inspection pedestal, focused on testing ONE precision object (the "
            "same mechanical-electronic assembly with brass gears, glowing circuit-"
            "board panels, delicate linkages that was built on the engineering floor). "
            "The object sits proudly on the pedestal, being examined. "
            "Robot 1 and Robot 2: standing at a brass-and-chrome scanning array that "
            "casts a warm amber verification beam of light across the object, "
            "inspecting it. "
            "Robot 3: leaning in with a slender brass probe, examining a seam on the "
            "object closely. "
            "Robot 4: at a nearby monitoring console that has several floating "
            "holographic panels above it showing abstract glowing waveform "
            "visualizations and signal curves (ABSOLUTELY NO text, NO numbers — just "
            "pure luminous curves and waveforms). "
            "Robot 5 and Robot 6: partially visible inside a glass-panel enclosure on "
            "one side of the pedestal, their pincer hands gently placed on the object's "
            "surface, performing a sealing or pressure-testing action — their glass "
            "enclosure glows faintly cool-blue from its interior. "
            "All robots exhibit methodical, careful body language — slower, more "
            "deliberate than the engineering floor's urgency. "
            "\n\nLIGHTING: Cool neutral daylight from the skylight is the key light. "
            "Warm amber accents from the scanning beam cutting across the object. Cool "
            "blue accent glows from the monitoring console and the sealed glass "
            "enclosure. The palette balances cool (security) with warm amber accents "
            "(verification glow) so the floor still feels premium and human, not cold. "
            "Shallow depth of field on the central object. "
            "\n\nThis floor feels watchful, methodical, careful — the guardianship of "
            "the ZAICORE operation."
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

print("generating 3 ZAICORE floor reference stills in parallel...", flush=True)
t0 = time.time(); total = 0.0
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(generate_one, s): s["name"] for s in SPECS}
    for fut in as_completed(futures):
        name, status, cost = fut.result(); total += cost
        print(f"[{name}] {status}  cost=${cost:.3f}", flush=True)
print(f"\nDONE in {time.time()-t0:.0f}s. total ${total:.3f}", flush=True)
print(f"saved to {MASCOTS}/", flush=True)
