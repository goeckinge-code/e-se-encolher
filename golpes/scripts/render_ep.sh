#!/usr/bin/env bash
# Renderiza todos os planos de um episódio (retoma de onde parou).
# Uso: golpes/scripts/render_ep.sh ep01-piramide [s01 s02 ...]
# PY = Python com o módulo bpy (pip install bpy) ou: PY="blender -b -P" (Blender instalado)
set -e
cd "$(dirname "$0")/../.."
EP="$1"; shift
PY="${PY:-python3}"
SHOTS="$@"
[ -z "$SHOTS" ] && SHOTS=$(python3 -c "import sys; sys.path.insert(0,'golpes/$EP'); import roteiro; print(' '.join(s['id'] for s in roteiro.SHOTS))")
for s in $SHOTS; do
  $PY golpes/blender/render.py -- "$EP" "$s" seq 2>&1 | grep -E "DONE|Error|Traceback" || true
done
