"""Generate a Pixar-style elephant for exploration."""
import os, json, base64, urllib.request, pathlib

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break

BASE = (
    "Classic Disney-Pixar 3D character render, Pixar feature-film quality. "
    "Soft subsurface scattering on skin, rich dimensional lighting, warm key light with cool fill, "
    "shallow depth of field, cinematic quality. Large expressive eyes with genuine personality. "
    "Pure white seamless studio background, soft floor shadow. Full body visible head to feet, "
    "character takes up most of the vertical frame, centered. "
    "Image dimensions: 1024 wide by 1536 tall (2:3 vertical portrait). Film-grade Pixar render."
)

PROMPTS = {
    'pixar_elephant_keeper': (
        "A wise, gentle elephant character in its middle years, warm grey-brown skin with detailed "
        "dimensional texture, kind amber eyes showing intelligence and warmth, small tusks, "
        "wearing a simple earth-toned linen robe tied at the waist. Trunk curled upward holding a "
        "small brass hurricane lantern with a soft warm glow. Standing calmly on all fours, "
        "patient protective expression, slight warm smile. "
        + BASE
    ),
}

OUT = pathlib.Path("/Users/zacharyferguson/zaicore-engineering/records/research/animals")

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
        print(f"  failed: {e}", flush=True); continue
    if "error" in data:
        print(f"  api error: {data['error']}", flush=True); continue
    images = data["choices"][0]["message"].get("images", [])
    if not images:
        print(f"  no image", flush=True); continue
    png = base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1])
    (OUT / f"{name}.png").write_bytes(png)
    cost = data.get("usage", {}).get("cost", 0)
    print(f"  saved ({len(png)//1024} KB, ${cost:.3f})", flush=True)
