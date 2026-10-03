#!/usr/bin/env bash
# One-time setup: Python deps, speech models (GitHub releases; Hugging Face may be blocked), Cyrillic fonts (npm).
set -euo pipefail
cd "$(dirname "$0")"
pip install -q sherpa-onnx soundfile numpy
mkdir -p models fonts work out img
R=https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models
[ -d models/sherpa-onnx-whisper-turbo ] || curl -sSL "$R/sherpa-onnx-whisper-turbo.tar.bz2" | tar xj -C models
[ -d models/sherpa-onnx-zipformer-ru-2024-09-18 ] || curl -sSL "$R/sherpa-onnx-zipformer-ru-2024-09-18.tar.bz2" | tar xj -C models
[ -f models/silero_vad.onnx ] || curl -sSL -o models/silero_vad.onnx "$R/silero_vad.onnx"
for f in cormorant-garamond unbounded; do
  [ -d "fonts/$f" ] && continue
  (cd fonts && npm pack -q "@fontsource/$f" >/dev/null && tar xzf fontsource-$f-*.tgz && mv package "$f" && rm fontsource-$f-*.tgz)
done
echo "setup ok"
