"""Pixar-style A/B test: fox v1 concept and owl v2 concept, in Pixar 3D."""
import os, json, base64, urllib.request, pathlib

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

BASE = (
    "Classic Disney-Pixar 3D character render, Pixar feature-film quality, similar to characters "
    "from Zootopia, Up, or Wall-E. Soft subsurface scattering on fur/feathers, rich dimensional "
    "lighting, warm key light with cool fill, shallow depth of field, rendered at cinematic quality. "
    "Large expressive eyes with genuine personality, detailed character design. "
    "Pure white seamless studio background, soft floor shadow. Full body visible head to feet, "
    "character takes up most of the vertical frame, centered. "
    "Image dimensions: 1024 wide by 1536 tall (2:3 vertical portrait). "
    "NOT claymation. NOT a figurine. NOT AI-generic. Film-grade Pixar render."
)

PROMPTS = {
    'pixar_fox': (
        "A curious young fox character, rich warm orange-russet fur with detailed texture showing "
        "individual hairs, cream fluffy belly, big expressive brown eyes with specular highlights, "
        "sitting upright on its haunches with bushy tail curled around its feet, "
        "holding a small glowing green circuit board in its paws like it's precious, "
        "faint thoughtful smile, tilted head showing curiosity. "
        + BASE
    ),
    'pixar_owl': (
        "A watchful snowy owl character, pristine white feathers with detailed texture and subtle "
        "grey markings, huge piercing yellow eyes with intelligent expression, "
        "wings slightly spread as if just landing, one talon delicately holding a small brass "
        "compass, protective stance, calm alert expression with slight eyebrow raise. "
        + BASE
    ),
}

OUT = pathlib.Path("/Users/zacharyferguson/zaicore-engineering/records/research/animals")
OUT.mkdir(parents=True, exist_ok=True)

total = 0.0
for name, prompt in PROMPTS.items():
    print(f"[{name}] generating...", flush=True)
    body = {
        "model": "openai/gpt-5.4-image-2",
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    try:
        r = urllib.request.urlopen(req, timeout=180)
        data = json.load(r)
    except Exception as e:
        print(f"  failed: {e}", flush=True)
        continue
    if "error" in data:
        print(f"  api error: {data['error']}", flush=True)
        continue
    images = data["choices"][0]["message"].get("images", [])
    if not images:
        print(f"  no image", flush=True)
        continue
    url = images[0]["image_url"]["url"]
    png = base64.b64decode(url.split(",", 1)[1])
    (OUT / f"{name}.png").write_bytes(png)
    cost = data.get("usage", {}).get("cost", 0)
    total += cost
    print(f"  saved ({len(png)//1024} KB, ${cost:.3f})", flush=True)

print(f"\nDONE. total ${total:.3f}", flush=True)
