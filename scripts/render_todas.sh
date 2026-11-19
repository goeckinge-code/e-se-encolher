#!/usr/bin/env bash
# Renderiza todas as cenas. Uso: scripts/render_todas.sh [--hq]
# BLENDER=caminho/do/blender (padrão: blender no PATH)
set -e
cd "$(dirname "$0")/.."
BL="${BLENDER:-blender}"
for s in s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10; do
  "$BL" -b -P blender/render.py -- "$s" seq "$@"
done
