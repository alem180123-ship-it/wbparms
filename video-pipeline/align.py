"""Give Whisper's text word-level timings borrowed from the Russian zipformer.

Whisper (sherpa-onnx) has the better text but no timestamps; the zipformer
transducer has token timestamps. Words are matched on a normalized stem and the
unmatched ones are interpolated by character length.
"""
import difflib
import json
import re

import sherpa_onnx
import soundfile as sf

Z = "models/sherpa-onnx-zipformer-ru-2024-09-18"
audio, sr = sf.read("work/audio16k.wav", dtype="float32")
segs = json.load(open("work/segments.json"))
corr = json.load(open("corrections.json"))

rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=f"{Z}/encoder.int8.onnx", decoder=f"{Z}/decoder.int8.onnx",
    joiner=f"{Z}/joiner.int8.onnx", tokens=f"{Z}/tokens.txt", num_threads=4,
    decoding_method="greedy_search")


def key(w):
    w = re.sub(r"[^a-zа-яё]", "", w.lower()).replace("ё", "е")
    return w[:5]


all_words = []
for seg in segs:
    a, b = int(seg["start"] * sr), int(seg["end"] * sr)
    s = rec.create_stream()
    s.accept_waveform(sr, audio[a:b])
    rec.decode_stream(s)
    r = s.result
    zw = []  # [text, start]
    for tok, ts in zip(r.tokens, r.timestamps):
        t = seg["start"] + ts
        if tok[:1] in ("▁", " ") or not zw:
            zw.append([tok.lstrip("▁ "), t])
        else:
            zw[-1][0] += tok
    zw = [w for w in zw if w[0]]
    text = seg["text"]
    for bad, good in corr.items():
        text = text.replace(bad, good)
    ww = text.split()
    sm = difflib.SequenceMatcher(None, [key(w) for w in ww], [key(w[0]) for w in zw], autojunk=False)
    times = [None] * len(ww)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = zw[blk.b + k][1]
    # anchors at segment edges, then interpolate by char length
    first_speech = zw[0][1] if zw else seg["start"]
    if times[0] is None:
        times[0] = first_speech
    ends = [None] * len(ww)
    i = 0
    while i < len(ww):
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < len(ww) and times[j] is None:
            j += 1
        t0 = times[i - 1]
        t1 = times[j] if j < len(ww) else seg["end"] - 0.15
        lens = [len(ww[k]) + 2 for k in range(i - 1, j)]
        tot = sum(lens)
        acc = 0
        for k in range(i, j):
            acc += lens[k - i]
            times[k] = t0 + (t1 - t0) * acc / tot
        i = j
    # enforce monotonic
    for k in range(1, len(times)):
        times[k] = max(times[k], times[k - 1] + 0.06)
    for k in range(len(ww)):
        nxt = times[k + 1] if k + 1 < len(ww) else seg["end"]
        ends[k] = min(nxt, times[k] + 0.9)
    matched = sum(1 for blk in sm.get_matching_blocks() for _ in range(blk.size))
    print(f"{seg['start']:6.2f} matched {matched}/{len(ww)}  zip: {' '.join(w[0] for w in zw)[:110]}")
    for w, s0, e0 in zip(ww, times, ends):
        all_words.append({"w": w, "s": round(s0, 3), "e": round(e0, 3)})

json.dump(all_words, open("work/words.json", "w"), ensure_ascii=False, indent=0)
print(len(all_words), "words")
