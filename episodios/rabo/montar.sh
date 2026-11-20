#!/usr/bin/env bash
# Junta os quadros do Blender e renderiza o vídeo final (legendas + folhas de calendário + card de escolha).
# Uso: episodios/rabo/montar.sh [--hq]
set -e
cd "$(dirname "$0")"
python3 roteiro.py > /dev/null
if [ "$1" = "--hq" ]; then DIR=renders/frames_hq; else DIR=renders/frames; fi
LIST=$(mktemp)
for s in $(python3 -c "import roteiro; print(' '.join(x['id'] for x in roteiro.SCENES))"); do
  for f in "$DIR/$s"/[0-9][0-9][0-9][0-9][0-9].jpg; do echo "file '$PWD/$f'"; echo "duration 0.0333333"; done
done > "$LIST"
TOTAL=$(python3 -c "import roteiro; print(roteiro.TOTAL)")
mkdir -p hyperframes/assets/video
ffmpeg -v error -y -f concat -safe 0 -i "$LIST" -vf "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 18 -t "$TOTAL" hyperframes/assets/video/blender.mp4
cd hyperframes && npx --yes hyperframes@0.9.70 render --quality delivery -o ../E-se-voce-tivesse-rabo.mp4
