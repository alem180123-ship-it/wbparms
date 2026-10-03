"""VAD-segmented Whisper (sherpa-onnx) transcription -> work/segments.json.

Hugging Face is blocked in this environment, so faster-whisper can't fetch its
model; sherpa-onnx models come from GitHub releases instead.
"""
import json
import sys

import numpy as np
import sherpa_onnx
import soundfile as sf

M = "models/sherpa-onnx-whisper-turbo"
audio, sr = sf.read("work/audio16k.wav", dtype="float32")
assert sr == 16000

vad_cfg = sherpa_onnx.VadModelConfig()
vad_cfg.silero_vad.model = "models/silero_vad.onnx"
vad_cfg.silero_vad.min_silence_duration = float(sys.argv[1]) if len(sys.argv) > 1 else 0.25
vad_cfg.silero_vad.min_speech_duration = 0.2
vad_cfg.silero_vad.max_speech_duration = 8.0
vad_cfg.silero_vad.threshold = 0.4
vad_cfg.sample_rate = 16000
vad = sherpa_onnx.VoiceActivityDetector(vad_cfg, buffer_size_in_seconds=120)

rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{M}/turbo-encoder.int8.onnx",
    decoder=f"{M}/turbo-decoder.int8.onnx",
    tokens=f"{M}/turbo-tokens.txt",
    language="ru",
    task="transcribe",
    num_threads=4,
)

win = vad_cfg.silero_vad.window_size
segs = []
for i in range(0, len(audio), win):
    vad.accept_waveform(audio[i:i + win])
    while not vad.empty():
        segs.append((vad.front.start, np.array(vad.front.samples)))
        vad.pop()
vad.flush()
while not vad.empty():
    segs.append((vad.front.start, np.array(vad.front.samples)))
    vad.pop()

out = []
for start, samples in segs:
    s = rec.create_stream()
    s.accept_waveform(16000, samples)
    rec.decode_stream(s)
    r = s.result
    t0 = start / 16000
    item = {"start": round(t0, 3), "end": round(t0 + len(samples) / 16000, 3), "text": r.text.strip()}
    ts = list(getattr(r, "timestamps", []) or [])
    if ts:
        item["tokens"] = list(r.tokens)
        item["timestamps"] = [round(t0 + t, 3) for t in ts]
    out.append(item)
    print(f"{item['start']:6.2f}-{item['end']:6.2f} {item['text']}", flush=True)

json.dump(out, open("work/segments.json", "w"), ensure_ascii=False, indent=1)
