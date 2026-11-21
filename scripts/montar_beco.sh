#!/usr/bin/env bash
# Junta os quadros do beco (renders/beco/frames) no vídeo final 1080x1920, 24fps, sem áudio.
# Uso: scripts/montar_beco.sh [--hq]
set -e
cd "$(dirname "$0")/.."
DIR=renders/beco/frames; [ "$1" = "--hq" ] && DIR=renders/beco/frames_hq
N=$(ls "$DIR"/*.png | wc -l)
[ "$N" -lt 720 ] && echo "Aviso: só $N de 720 quadros prontos."
ffmpeg -v error -y -framerate 24 -i "$DIR/%05d.png" \
  -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,format=yuv420p" \
  -c:v libx264 -preset slow -crf 18 -movflags +faststart renders/beco-30s-3D.mp4
echo "OK: renders/beco-30s-3D.mp4"
