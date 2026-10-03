#!/usr/bin/env bash
# usage: ./make.sh source.mp4 [out.mp4]
# Images referenced in build_data.py must be in img/.
set -euo pipefail
cd "$(dirname "$0")"
SRC=$(realpath "$1"); OUT=${2:-out/final.mp4}
cp "$SRC" work/src.mp4
ffmpeg -v error -y -i work/src.mp4 -vn -ac 1 -ar 16000 work/audio16k.wav
python3 energy.py
python3 transcribe_sherpa.py           # -> work/segments.json (proofread it!)
python3 align.py                       # -> work/words.json, applies corrections.json
python3 build_data.py                  # -> work/data.json (scenes + subtitle lines)
node render.mjs work/video_only.mp4    # white stage, cards, subtitles
ffmpeg -v error -y -i work/video_only.mp4 -i work/src.mp4 -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart "$OUT"
echo "done: $OUT"
