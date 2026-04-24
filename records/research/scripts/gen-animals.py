"""Generate claymation-style animal mascot variants for ZAICORE.
Fox · Owl · Elephant · Dolphin, 2 variations each.
"""
import os, json, base64, urllib.request, pathlib

KEY = None
for line in pathlib.Path(os.path.expanduser('~/PersonalWebsite/.env.local')).read_text().split('\n'):
    if line.startswith('OPENROUTER_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break
assert KEY, "no key"

BASE_STYLE = (
    "Claymation stop-motion character, Wallace and Gromit / Aardman Animation style. "
    "Visible fingerprint marks and subtle imperfections on plasticine clay surfaces, "
    "handcrafted tactile feel, warm studio lighting, soft shadow on the floor. "
    "Pure white seamless background, full body visible head to feet/base, "
    "character takes up most of the vertical frame, centered. Warm earthy palette. "
    "Tactile, charming, distinctly not digital. Image dimensions: 1024 wide by 1536 tall (2:3 vertical portrait)."
)

ANIMALS = {
    'fox_v1': (
        "A curious young fox, warm orange-russet fur with cream belly, big thoughtful eyes, "
        "sitting upright on its haunches with tail curled around its feet, holding a small glowing "
        "green circuit board in its paws like it's precious, faint smile, tilted head. "
        + BASE_STYLE
    ),
    'fox_v2': (
        "A clever fox standing on its hind legs, deep russet fur, big expressive eyes, "
        "holding a tiny brass wrench in one paw, other paw scratching its chin thoughtfully, "
        "alert attentive expression. "
        + BASE_STYLE
    ),
    'owl_v1': (
        "A wise barn-owl character, warm cream and tan feathers with darker markings, "
        "huge round thoughtful amber eyes, perched on a small wooden branch, "
        "holding a tiny brass spyglass/telescope in one talon, feathers slightly ruffled, "
        "calm watchful expression. "
        + BASE_STYLE
    ),
    'owl_v2': (
        "A vigilant snowy owl, soft white and grey feathers, intense yellow eyes, "
        "wings slightly open as if just landing, one talon holding a small brass compass, "
        "protective stance, alert expression. "
        + BASE_STYLE
    ),
    'elephant_v1': (
        "A gentle young baby elephant, soft grey-blue clay skin with visible thumbprints, "
        "big kind eyes with long lashes, small rounded ears, holding a tiny glowing "
        "blue orb carefully at the tip of its trunk, warm thoughtful expression. "
        + BASE_STYLE
    ),
    'elephant_v2': (
        "A wise adult elephant standing calmly, warm grey clay skin, large expressive eyes, "
        "tusks small and gentle, trunk curled upward holding a small brass lantern that glows softly, "
        "wise patient expression. "
        + BASE_STYLE
    ),
    'dolphin_v1': (
        "A playful dolphin character in a graceful mid-leap arc, smooth blue-grey clay body with "
        "cream underside, big expressive eyes, slight smile, body curved upward mid-jump "
        "as if suspended in air, small droplets of clay suggesting water. "
        + BASE_STYLE
    ),
    'dolphin_v2': (
        "A clever dolphin standing vertically balanced on its tail on a small clay wave, "
        "smooth blue-grey clay skin, inquisitive eyes, slight curious smile, "
        "small hologram-like glowing symbol floating above its rostrum. "
        + BASE_STYLE
    ),
}

OUT_DIR = pathlib.Path("/Users/zacharyferguson/zaicore-engineering/records/research/animals")
OUT_DIR.mkdir(parents=True, exist_ok=True)

total = 0.0
for name, prompt in ANIMALS.items():
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
    out = OUT_DIR / f"{name}.png"
    out.write_bytes(png)
    cost = data.get("usage", {}).get("cost", 0)
    total += cost
    print(f"  saved {out.name} ({len(png)//1024} KB, ${cost:.3f})", flush=True)

print(f"\nDONE. total ${total:.3f}", flush=True)
