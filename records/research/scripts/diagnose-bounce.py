"""Measure frame-to-frame pixel deltas in security_scene.APPROVED.mp4
to find the actual bounce location.

Also computes optimal loop trim points — the pair (early, late) that
minimizes the loop-seam jump.
"""
import numpy as np
import subprocess
import tempfile
import pathlib
from PIL import Image

VIDEO = pathlib.Path("/Users/zacharyferguson/zaicore-engineering/public/mascots/security_scene.APPROVED.mp4")
tmp = tempfile.mkdtemp()

print("extracting 241 frames at 192x108…", flush=True)
subprocess.run([
    "ffmpeg", "-i", str(VIDEO), "-vf", "scale=192:108",
    "-frames:v", "241", f"{tmp}/f_%04d.png",
    "-loglevel", "error", "-y"
], check=True)

frames = []
for i in range(1, 242):
    img = np.array(Image.open(f"{tmp}/f_{i:04d}.png").convert("RGB"), dtype=np.float32)
    frames.append(img)

# consecutive deltas
deltas = []
for i in range(240):
    d = float(np.mean((frames[i] - frames[i+1]) ** 2))
    deltas.append(d)

# loop seam (frame 240 back to frame 0)
loop_delta = float(np.mean((frames[240] - frames[0]) ** 2))

avg = sum(deltas) / len(deltas)
print(f"\nmean consecutive delta:  {avg:7.1f}")
print(f"median consecutive delta: {sorted(deltas)[120]:7.1f}")
print(f"max consecutive delta:   {max(deltas):7.1f} at frame {deltas.index(max(deltas))}→{deltas.index(max(deltas))+1}")
print(f"loop seam delta (240→0): {loop_delta:7.1f}  [{loop_delta/avg:.1f}x mean]")

print("\ntop 10 biggest consecutive deltas:")
top = sorted(enumerate(deltas), key=lambda x: -x[1])[:10]
for idx, d in top:
    print(f"  frame {idx:3d}→{idx+1:3d}: {d:7.1f}  [{d/avg:.1f}x mean]")

# Find best loop trim: minimize MSE between some early frame (0..20) and some late frame (220..240)
print("\nsearching best loop trim (early 0-20, late 220-240)…")
best = (1e18, 0, 240)
for e in range(0, 21):
    for l in range(220, 241):
        d = float(np.mean((frames[e] - frames[l]) ** 2))
        if d < best[0]:
            best = (d, e, l)

d, e, l = best
kept = l - e + 1
print(f"\nbest pair: frame {e} ↔ frame {l}  (delta={d:.1f}, {d/avg:.2f}x mean)")
print(f"→ trim: drop first {e} frames, drop last {240-l} frames, keep {kept} frames ({kept/24:.2f}s)")
print(f"→ ffmpeg: -ss {e/24:.3f} -t {kept/24:.3f} or filter_complex trim=start_frame={e}:end_frame={l+1}")

# Also report: where is frame 0 most similar within 220-240?
print(f"\nbest end for frame 0: ", end="")
best_for_0 = min(range(220, 241), key=lambda i: float(np.mean((frames[0] - frames[i]) ** 2)))
d0 = float(np.mean((frames[0] - frames[best_for_0]) ** 2))
print(f"frame {best_for_0} (delta={d0:.1f}, {d0/avg:.2f}x mean)")
