"""Security scene — fresh 16:9 still generated from scratch.

Uses gpt-image-2 (openai/gpt-5.4-image-2) with owl + robot PNGs as IDENTITY
references only. Prompt describes the ENTIRE scene from scratch: bottom-left
conveyor belt, 3 identical robots hovering (thruster flames, NO legs), snowy
owl standing behind the belt, upper-right cream copy zone.

NOT a composite onto an existing base — the prior compositor runs kept
turning the thruster into tripod legs because it was reinterpreting an
already-broken starting scene. Pure fresh generation avoids that drift.

Output: public/mascots/security_scene_start.png (becomes the Seedance
first_frame + last_frame for the next step).
"""
import os, json, base64, urllib.request, pathlib, time

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

MASCOTS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/public/mascots'))
OUT_STILLS = pathlib.Path(os.path.expanduser('~/zaicore-engineering/records/research/stills'))
OUT_STILLS.mkdir(parents=True, exist_ok=True)

def to_data_uri(p: pathlib.Path) -> str:
    return f"data:image/png;base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"

OWL   = to_data_uri(MASCOTS / "owl_typing.png")
ROBOT = to_data_uri(MASCOTS / "robot_tinkerer.png")
COMP  = to_data_uri(MASCOTS / "security_approved_frame0.png")

PROMPT = """Render a Pixar 3D feature-film scene. Warm uniform cream background (#faf8f7). You are given THREE reference images:

IMAGE 1 (owl): identity reference for the owl — snowy owl with this exact feather pattern, yellow eyes, and beak. Identity only. Ignore the laptop — it must NOT appear in the output scene.

IMAGE 2 (robot): identity reference for the helper robot design — single large amber camera-lens eye, cream-white rounded body with gold accent band, two thin pincer arms at sides, soft blue thruster glow beneath the body. Use this exact character design for ALL THREE robots in the scene.

IMAGE 3 (composition reference): shows the exact layout I want — snowy owl standing directly behind a chrome industrial platform, with three small helper robots lined up in front of the owl on top of the platform, all four subjects grouped tightly together in the bottom-LEFT corner of a wide frame. USE THIS COMPOSITION EXACTLY. The belt height, the owl's position behind it, the spacing and size of the three robots, the cluster size — all match image 3. The ONLY difference: raise the platform/belt slightly so that MORE of the owl's body is obscured behind the belt (the belt's front face should hide the owl from the mid-chest down, leaving only head + shoulders + folded wingtops visible above the belt's top edge). Also swap the robot design to match image 2 (with blue thruster glow beneath each body).

Compose it as a 1792 wide by 1024 tall LANDSCAPE frame (wider than tall). The owl + belt + robot cluster occupies ONLY the bottom-left ~35% of this wider frame. The upper-right ~65% is PURE EMPTY WARM CREAM — nothing in it at all.

HARD NEGATIVES — things that MUST NOT appear anywhere in the output:
- DO NOT duplicate the owl. There is EXACTLY ONE owl in the scene. Do NOT paint a second owl, a ghost owl face, a faded owl silhouette, or any owl-like shape anywhere in the cream upper-right area.
- DO NOT add any laptop, computer, screen, or desk object.
- DO NOT add extra characters beyond the one owl and three robots.
- DO NOT spread the cluster across the full width — stays tight in the bottom-left corner.
- The upper-right 65% of the frame stays completely empty cream — no objects, no atmospheric elements, no floating shapes, nothing.

Premium Pixar 3D feature-film render, 1792x1024 LANDSCAPE, warm clean studio lighting matching the ZAICORE engineering and hero scenes."""

content = [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": OWL}},
    {"type": "image_url", "image_url": {"url": ROBOT}},
    {"type": "image_url", "image_url": {"url": COMP}},
]

body = {
    "model": "openai/gpt-5.4-image-2",
    "messages": [{"role": "user", "content": content}],
    "modalities": ["image", "text"],
}

print(f"generating security scene still (fresh 16:9, no composite base)…", flush=True)
print(f"  prompt chars: {len(PROMPT)}", flush=True)
t0 = time.time()
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
)
r = urllib.request.urlopen(req, timeout=420)
data = json.load(r)
if "error" in data:
    print(f"ERROR: {data['error']}", flush=True); exit(1)
images = data["choices"][0]["message"].get("images", [])
if not images:
    print(f"NO_IMAGE; full response: {json.dumps(data)[:600]}", flush=True); exit(1)
png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
out_path = MASCOTS / "security_scene_start.png"
out_path.write_bytes(png)
(OUT_STILLS / "security_scene_start.png").write_bytes(png)
cost = data.get("usage", {}).get("cost", 0.0)
print(f"OK ({len(png)//1024} KB, {time.time()-t0:.0f}s, cost=${cost:.3f})", flush=True)
print(f"saved to: {out_path}", flush=True)
