#!/usr/bin/env bash
# Renderiza (se preciso) e junta os quadros de um episódio no MP4 final, sem áudio.
# Uso: ./montar.sh ep02-mentira    (padrão: ep01-reclamacao)
set -e
cd "$(dirname "$0")"
EP=${1:-ep01-reclamacao}
[ -d node_modules ] || npm i
node render.js seq 30 --ep "$EP"   # só renderiza os quadros que faltam (REFAZ=1 refaz todos)
OUT=../renders/$EP.mp4; [ "$EP" = ep01-reclamacao ] && OUT=../renders/reclamacao-custa-1-real.mp4
ffmpeg -v error -y -framerate 30 -i out/$EP/frames/%05d.jpg -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -movflags +faststart "$OUT"
echo "OK: ${OUT#../}"
