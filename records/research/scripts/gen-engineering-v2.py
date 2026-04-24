"""Regen engineering section still with the workbench + lip composition.

Fox in medium shot behind a warm wood workbench, lip across lower frame hiding
the build. Fox's face + goggles + smoke wisp visible. Robots fly in from the
left side of frame handing parts to fox's paw. Right 60% of frame clean warm
off-white for body copy. Background matches hero's warm off-white (#faf8f7).
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

FOX_REF = to_data_uri(MASCOTS / "fox_soldering.png")
ROBOT_REF = to_data_uri(MASCOTS / "robot_tinkerer.png")

PROMPT = """The fox character must match the provided fox reference exactly — warm russet fur, clear protective safety goggles DOWN over its eyes (covering the eyes), focused expression. The helper robot must match the provided robot reference exactly — cream-white pill-shaped body with matte plastic finish, rounded dome head with a single glowing amber camera-lens eye, rounded arms ending in soft pincer hands, slim gold accent band, small round black rubber wheels. The robot HOVERS using small softly-glowing blue thrusters on its underside.

Style: premium 3D cartoon feature-film render quality, warm cinematic lighting, soft subsurface scattering on fur and plastic, shallow depth of field.

BACKGROUND: PERFECTLY FLAT UNIFORM WARM OFF-WHITE SEAMLESS STUDIO matching the exact color #faf8f7 (subtle warm tone — NOT pure bright white, NOT gray, a soft warm off-white that feels like natural diffuse daylight on a white wall). ABSOLUTELY UNIFORM across the entire empty space — NO noise, NO grain, NO gradient, NO darker corners or brighter center, NO subtle color variance anywhere. Just one single flat consistent warm off-white tone. Infinite background, NO walls visible, NO windows, NO architecture. Just the flat warm off-white void. No floor texture — just the same warm off-white on the ground.

Image dimensions: 1792 wide by 1024 tall (16:9 landscape).

COMPOSITION: strongly left-biased with significant negative space both ABOVE and to the RIGHT of the scene. The fox, his workbench, and the helper robot occupy roughly the LEFT 35% of the frame. The RIGHT 65% of the frame is clean empty flat warm off-white space (for body-copy overlay). CRITICAL: leave AT LEAST 40% of the frame height as EMPTY WARM OFF-WHITE SPACE above the fox's ears — the fox's highest point (ear tips) must be at about 45% from the top edge of the frame, NEVER higher. Characters must be SMALL relative to the frame — small enough that the fox's head-and-shoulders occupy maybe 20-25% of frame height total. Never clip any part of any character.

THE WORKBENCH: A beautiful warm wood workbench positioned in the LEFT portion of the frame. Its base sits near the bottom edge of the frame. The workbench extends from off the left edge of the frame and stops at approximately 50% of the way across the frame horizontally (further LEFT than the right edge) — it DOES NOT span the full width. At its right end, the bench has a CLEAN FINISHED ENDPOINT: a clear visible right-end corner where the front lip and top surface meet at a defined edge (showing the wood grain end-cap). The right 50% of the frame beyond the bench is clean empty warm off-white space. The workbench has a DEFINED FRONT LIP (the front edge of the bench, facing the viewer) that is visible across the bench's width. This lip HIDES whatever is being built on the work surface from the viewer — we cannot see what's on the workbench, only the front wood lip. The bench top sits at about 45% up from the bottom of the frame. The bench is made of warm wood with subtle grain, brass edge detail, and a small chamfered top corner at the right-end.

THE FOX (behind the workbench, medium shot, SMALL in frame): The fox sits at the workbench, visible from the CHEST UP above the bench lip. The fox's highest point (ear tips) reaches no higher than about 30% from the top of the frame — there must be AT LEAST 25% empty warm off-white space above his ears. His head and chest are clearly in view. He wears his clear safety goggles down over his eyes, focused expression. One russet paw is visible just above the lip — that paw holds a small chrome soldering iron, and a THIN WISP OF SMOKE curls upward from the soldering iron tip (the smoke rises into the empty upper frame area, clearly visible). The fox looks down at his work (the work itself is hidden behind the lip — we don't see the circuit board, only the tip of the iron and the smoke).

THE HELPER ROBOT (entering from left): A single helper robot HOVERS with a visible soft blue thruster glow beneath its body, positioned at bench-lip height on the LEFT side of the frame (near the left edge). The robot is SMALL (similar scale to the fox, not larger). It extends one pincer forward toward the fox's exposed paw, holding out a SMALL POLISHED BRASS COMPONENT (a tiny gear, small circuit element). The robot's top (eye-level) is at similar height to the fox's ears, well within the frame — never clipped at the top.

LIGHTING: Warm golden amber key light from upper left (casts soft highlights on the fox's fur and the wood bench). Cool fill from upper right (keeps the right 60% of frame clean and neutral). Subtle warm glow from the soldering iron tip. Shallow depth of field with the fox in sharpest focus.

CRITICAL CONSTRAINTS:
- Absolutely NO text, NO letters, NO numerals, NO writing anywhere.
- Fox's goggles must be DOWN over his eyes (worn, not pushed up).
- The bench LIP must be clearly visible and must HIDE whatever's on the work surface.
- We must see the fox's FACE + goggles + one paw holding the soldering iron + the smoke wisp.
- The right 60% of the frame is clean empty warm off-white space — no objects, no characters, no details.
- Background is warm off-white (#faf8f7) — not pure white, not gray.

Feeling: focused craftsmanship, serene + warm + cinematic, the expert at his bench with the AI quietly bringing him what he needs."""

content = [{"type": "text", "text": PROMPT}]
content.append({"type": "image_url", "image_url": {"url": FOX_REF}})
content.append({"type": "image_url", "image_url": {"url": ROBOT_REF}})

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print("regen engineering scene v2 — workbench + lip + medium shot…", flush=True)
t0 = time.time()
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
r = urllib.request.urlopen(req, timeout=420)
data = json.load(r)
if "error" in data:
    print(f"API_ERROR: {data['error']}", flush=True); exit(1)
images = data["choices"][0]["message"].get("images", [])
if not images:
    print("NO_IMAGE", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
(OUT / "section_engineering_v2.png").write_bytes(png)
(MASCOTS / "section_engineering.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
