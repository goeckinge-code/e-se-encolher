#!/usr/bin/env bash
# Junta os quadros do Blender em hyperframes/assets/video/blender.mp4 e renderiza o vídeo final
# com legendas, folhas de calendário e o card de escolha (HyperFrames).
# Uso: scripts/montar.sh [--hq]
set -e
cd "$(dirname "$0")/.."
if [ "$1" = "--hq" ]; then DIR=renders/frames_hq; DUR=0.0333333; else DIR=renders/frames; DUR=0.0666667; fi
LIST=$(mktemp)
for s in s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10; do
  for f in "$DIR/$s"/*.jpg; do echo "file '$PWD/$f'"; echo "duration $DUR"; done
done > "$LIST"
TOTAL=$(python3 -c "import sys; sys.path.insert(0,'hyperframes/build'); import build; print(build.TOTAL)")
ffmpeg -v error -y -f concat -safe 0 -i "$LIST" -vf "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 18 -t "$TOTAL" hyperframes/assets/video/blender.mp4
cd hyperframes && npx hyperframes render --quality delivery -o ../renders/E-se-voce-encolhesse-final.mp4
