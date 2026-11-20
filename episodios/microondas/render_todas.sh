#!/usr/bin/env bash
# Renderiza todas as cenas do episódio em 2 filas paralelas. Uso: episodios/microondas/render_todas.sh [--hq]
cd "$(dirname "$0")"
PY="${BLENDER_PY:-python3}"
( for s in s0 s2 s4; do $PY render.py -- $s seq "$@" 2>&1 | grep DONE; done ) &
( for s in s1 s3 s5; do $PY render.py -- $s seq "$@" 2>&1 | grep DONE; done ) &
wait
