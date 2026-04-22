"""Generate 5 style-reference images for ZAICORE mascot direction."""
import os, json, base64, urllib.request, pathlib

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break
assert KEY, "no key"

STYLES = {
    'style1_cinematic': (
        "Photorealistic cinematic photograph, A24 film still aesthetic, shot on 35mm film, shallow depth of field, warm natural window light, film grain. "
        "Real adult human (not illustration, not cartoon, not 3D render). Engineer, early 30s, kind thoughtful expression, cream cable-knit sweater, dark navy shirt underneath, dark work pants. "
        "Standing calmly, holding a small glowing circuit board cupped in both hands. Full body head-to-mid-calf, facing slightly right. Soft off-white seamless studio background."
    ),
    'style2_editorial': (
        "Editorial magazine illustration, New Yorker feature-art style, flat or semi-flat with confident clean lines and subtle textured fills. Warm muted palette: cream, ochre, deep navy, rust, soft black. "
        "Adult engineer early 30s, thoughtful expression, cream cable-knit sweater over navy shirt, dark work pants. Standing, holding a small glowing circuit board in both hands. Full body, facing slightly right. "
        "Off-white background with subtle paper texture. Conceptual, adult, print-magazine aesthetic. Absolutely NOT a 3D render, NOT Pixar, NOT photorealistic."
    ),
    'style3_claymation': (
        "Claymation stop-motion animation, Wallace and Gromit Aardman Animation style. Visible fingerprint marks and subtle imperfections on plasticine clay surfaces. Handcrafted tactile feel. "
        "Adult engineer early 30s, big round eyes, kind warm expression, cream knit sweater with clearly handcrafted ribbing, navy shirt, work pants. Standing, holding a small glowing circuit board. Full body, facing slightly right. "
        "Soft warm studio lighting. Off-white seamless background. Stop-motion aesthetic, distinctly not digital."
    ),
    'style4_arcane': (
        "Stylized painterly 3D animation, Netflix Arcane series aesthetic. Semi-realistic character features with visible brushstroke texture on hair, skin, and fabric. Cinematic dramatic rim lighting, warm-cool color contrast. "
        "Adult engineer early 30s, thoughtful intense expression, dark messy hair, cream cable-knit sweater, navy shirt, dark work pants. Standing, holding a small glowing circuit board. Full body, facing slightly right. "
        "Warm rim light, cool shadow side. Off-white background with subtle atmospheric haze. Adult animated film quality, refined and cinematic."
    ),
    'style5_pixar': (
        "Pixar-style 3D character render, similar to characters from Up or Wall-E. Soft rounded features, large expressive eyes, bright family-friendly studio lighting. "
        "Adult engineer early 30s, warm smile, dark messy hair, cream cable-knit sweater, navy shirt, dark work pants. Standing, holding a small glowing circuit board. Full body, facing slightly right. "
        "Off-white seamless background. Classic Disney-Pixar render quality."
    ),
}

OUT_DIR = pathlib.Path("/Users/zacharyferguson/zaicore-engineering/records/research/styles")
OUT_DIR.mkdir(parents=True, exist_ok=True)

total_cost = 0.0
for name, style in STYLES.items():
    print(f"[{name}] generating...", flush=True)
    prompt = (
        style
        + "\n\nImage dimensions: 1024 wide by 1536 tall (vertical 2:3 portrait). "
        "Single character, full body from head to mid-calf, centered vertically. Transparent or near-white background."
    )
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
        print(f"  request failed: {e}", flush=True)
        continue
    if "error" in data:
        print(f"  api error: {data['error']}", flush=True)
        continue
    msg = data["choices"][0]["message"]
    images = msg.get("images", [])
    if not images:
        print(f"  no image returned. content: {msg.get('content','')[:200]}", flush=True)
        continue
    url = images[0]["image_url"]["url"]
    b64 = url.split(",", 1)[1]
    png = base64.b64decode(b64)
    out = OUT_DIR / f"{name}.png"
    out.write_bytes(png)
    cost = data.get("usage", {}).get("cost", 0)
    total_cost += cost
    print(f"  saved {out.name} ({len(png)//1024} KB, ${cost:.3f})", flush=True)

print(f"\nALL DONE. total cost ${total_cost:.3f}", flush=True)
