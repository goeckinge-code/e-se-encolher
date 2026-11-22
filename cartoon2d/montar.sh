#!/usr/bin/env bash
# Renderiza (se preciso) e junta os quadros no MP4 final, sem áudio.
set -e
cd "$(dirname "$0")"
[ -d node_modules ] || npm i
[ "$(ls out/frames 2>/dev/null | wc -l)" -ge 900 ] || node render.js seq 30
ffmpeg -v error -y -framerate 30 -i out/frames/%05d.jpg -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -movflags +faststart ../renders/reclamacao-custa-1-real.mp4
echo "OK: renders/reclamacao-custa-1-real.mp4"
