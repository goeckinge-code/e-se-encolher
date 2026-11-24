"""Traçados dos circuitos para a seção "Nas pistas".

Fonte: bacinger/f1-circuits (GeoJSON, licença MIT, (c) Tomislav Bacinger)
https://raw.githubusercontent.com/bacinger/f1-circuits/master/f1-circuits.geojson
Uso: python3 pistas.py f1-circuits.geojson ../assets/js/pistas.js
Projeta lon/lat num plano (equirretangular local), simplifica e encaixa cada pista
numa caixa 1000x1000, salvando como caminhos SVG.
"""
import json, math, sys

IDS = {"monaco": "mc-1929", "estoril": "pt-1972", "suzuka": "jp-1962", "spa": "be-1925", "interlagos": "br-1940"}
src, dst = sys.argv[1], sys.argv[2]
feats = {f["properties"]["id"]: f for f in json.load(open(src))["features"]}


def rdp(P, eps):
    if len(P) < 3:
        return P
    (ax, ay), (bx, by) = P[0], P[-1]
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy) or 1e-9
    d = [abs(dx * (y - ay) - dy * (x - ax)) / n for x, y in P]
    i = max(range(len(P)), key=d.__getitem__)
    if d[i] > eps:
        return rdp(P[:i + 1], eps)[:-1] + rdp(P[i:], eps)
    return [P[0], P[-1]]


out = {}
for key, fid in IDS.items():
    f = feats[fid]
    g = f["geometry"]
    co = g["coordinates"] if g["type"] == "LineString" else g["coordinates"][0]
    lat0 = sum(c[1] for c in co) / len(co)
    pts = [(c[0] * math.cos(math.radians(lat0)) * 111320, -c[1] * 110540) for c in co]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    s = 860 / max(w, h)
    ox, oy = (1000 - w * s) / 2 - min(xs) * s, (1000 - h * s) / 2 - min(ys) * s
    P = [(x * s + ox, y * s + oy) for x, y in pts]
    k = max(range(len(P)), key=lambda i: math.hypot(P[i][0] - P[0][0], P[i][1] - P[0][1]))
    P = rdp(P[:k + 1], 1.2)[:-1] + rdp(P[k:], 1.2)  # circuito fechado: divide no ponto mais distante
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in P) + "Z"
    out[key] = {"d": d, "len_m": f["properties"].get("length"), "nome": f["properties"]["Name"]}
    print(key, len(co), "->", len(P), "pontos")

open(dst, "w").write("/* Traçados: bacinger/f1-circuits (MIT, (c) Tomislav Bacinger). Gerado por tools/pistas.py */\nconst PISTAS=" + json.dumps(out, ensure_ascii=False) + ";\n")
