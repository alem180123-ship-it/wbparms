"""Per-frame loudness envelope and onsets -> work/energy.json (drives audio-reactive effects)."""
import json

import numpy as np
import soundfile as sf

a, sr = sf.read("work/audio16k.wav", dtype="float32")
fps = 30
hop = sr // fps
n = len(a) // hop
rms = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
db = 20 * np.log10(rms + 1e-6)
s = np.convolve(db, np.ones(5) / 5, "same")
lo, hi = np.percentile(s, 10), np.percentile(s, 98)
e = np.clip((s - lo) / (hi - lo), 0, 1)
on = np.clip(np.diff(db, prepend=db[0]), 0, None)
on = np.clip(on / np.percentile(on, 99), 0, 1)
json.dump({"fps": fps, "energy": [round(float(x), 3) for x in e], "onset": [round(float(x), 3) for x in on]},
          open("work/energy.json", "w"))
