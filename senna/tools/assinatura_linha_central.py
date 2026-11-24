"""Gera SIG {vb, ink, d[]} no formato do Plazza a partir da assinatura ampliada 4x.

ink = contorno real da tinta (espessura variável); d = trajeto da caneta (linha central),
encadeado em poucos gestos contínuos para a escrita fluir. Uso: python3 assinatura_linha_central.py sig_x4.png saida.json
"""
import json, math, sys
import numpy as np
from PIL import Image, ImageFilter
from skimage.morphology import skeletonize, remove_small_objects

SRC, OUT = sys.argv[1], sys.argv[2]
K = 4
im = Image.open(SRC).convert("L").filter(ImageFilter.GaussianBlur(1.3))  # recorte da assinatura já 4x (super_resolucao.py)
a = np.asarray(im).astype(float)
ink = a < 150
ink = remove_small_objects(ink, max_size=200)
sk = skeletonize(ink)
H, W = sk.shape
N8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def nb(p):
    y, x = p
    for dy, dx in N8:
        yy, xx = y + dy, x + dx
        if 0 <= yy < H and 0 <= xx < W and sk[yy, xx]:
            yield (yy, xx)

pix = set(map(tuple, np.argwhere(sk)))
deg = {p: sum(1 for _ in nb(p)) for p in pix}
nodes = {p for p in pix if deg[p] != 2}

# cluster junction pixels
clusters, cid = [], {}
for p in nodes:
    if p in cid:
        continue
    stack, c = [p], []
    cid[p] = len(clusters)
    while stack:
        q = stack.pop(); c.append(q)
        for r in nb(q):
            if r in nodes and r not in cid:
                cid[r] = len(clusters); stack.append(r)
    clusters.append(c)

# trace edges between clusters
edges, seen = [], set()
for ci, c in enumerate(clusters):
    for p in c:
        for q in nb(p):
            if q in nodes:
                continue
            key = (p, q)
            if key in seen:
                continue
            path, prev, cur = [p, q], p, q
            while cur not in nodes:
                nxt = [r for r in nb(cur) if r != prev and r not in path[-3:]]
                if not nxt:
                    break
                prev, cur = cur, nxt[0]
                path.append(cur)
            seen.add((path[1], path[0])); seen.add((path[-2], path[-1]) if len(path) > 1 else key)
            seen.add(key)
            end = cid.get(path[-1], -1)
            edges.append({"a": ci, "b": end, "pts": path})
# deduplicate (each edge traced from both ends)
uniq, sig = [], set()
for e in edges:
    k = (min(tuple(e["pts"][0]), tuple(e["pts"][-1])), max(tuple(e["pts"][0]), tuple(e["pts"][-1])), len(e["pts"]))
    if k in sig:
        continue
    sig.add(k); uniq.append(e)
edges = uniq

def L(e):
    return len(e["pts"])

# prune short spurs (endpoint-to-junction)
def cdeg(ci):
    return sum((e["a"] == ci) + (e["b"] == ci) for e in edges)
changed = True
while changed:
    changed = False
    for e in list(edges):
        ea, eb = e["a"], e["b"]
        if L(e) < 14 and (len(clusters[ea]) == 1 and deg[clusters[ea][0]] == 1 or len(clusters[eb]) == 1 and deg[clusters[eb][0]] == 1) and cdeg(ea) + cdeg(eb) > 2:
            edges.remove(e); changed = True

def direction(pts, at_start):
    seg = pts[:12] if at_start else pts[::-1][:12]
    (y0, x0), (y1, x1) = seg[0], seg[-1]
    v = (x1 - x0, y1 - y0)  # pointing away from node
    n = math.hypot(*v) or 1
    return (v[0] / n, v[1] / n)

# at each cluster, pair edges by straightest continuation
inc = {}
for i, e in enumerate(edges):
    inc.setdefault(e["a"], []).append((i, True))
    inc.setdefault(e["b"], []).append((i, False))
link = {}
for ci, lst in inc.items():
    if len(lst) < 2:
        continue
    ds = [(i, s, direction(edges[i]["pts"], s)) for i, s in lst]
    pairs = []
    for x in range(len(ds)):
        for y in range(x + 1, len(ds)):
            if ds[x][0] == ds[y][0]:
                continue
            d1, d2 = ds[x][2], ds[y][2]
            pairs.append((d1[0] * d2[0] + d1[1] * d2[1], x, y))  # -1 = straight
    pairs.sort()
    used = set()
    for score, x, y in pairs:
        if x in used or y in used or score > -0.2:
            continue
        used |= {x, y}
        link[(ds[x][0], ds[x][1])] = (ds[y][0], ds[y][1])
        link[(ds[y][0], ds[y][1])] = (ds[x][0], ds[x][1])

done, strokes = set(), []
def walk(i, start_at_a):
    pts = []
    while True:
        done.add(i)
        p = edges[i]["pts"] if start_at_a else edges[i]["pts"][::-1]
        pts += p if not pts else p[1:]
        end = (i, not start_at_a)  # far end
        nx = link.get(end)
        if not nx or nx[0] in done:
            return pts
        i, start_at_a = nx[0], nx[1]

# start from ends that have no link
for i, e in enumerate(edges):
    if i in done:
        continue
    for s in (True, False):
        if (i, s) not in link:
            strokes.append(walk(i, s)); break
for i in range(len(edges)):
    if i not in done:
        strokes.append(walk(i, True))

def rdp(P, eps):
    if len(P) < 3:
        return P
    a, b = np.array(P[0], float), np.array(P[-1], float)
    ab = b - a; n = np.hypot(*ab)
    d = [abs(ab[0]*(p[1]-a[1])-ab[1]*(p[0]-a[0])) / n if n else np.hypot(*(np.array(p, float) - a)) for p in P]
    k = int(np.argmax(d))
    if d[k] > eps:
        return rdp(P[:k + 1], eps)[:-1] + rdp(P[k:], eps)
    return [P[0], P[-1]]

def smooth(P, it=2):
    P = np.array(P, float)
    for _ in range(it):
        Q = [P[0]]
        for i in range(len(P) - 1):
            Q += [0.75 * P[i] + 0.25 * P[i + 1], 0.25 * P[i] + 0.75 * P[i + 1]]
        Q.append(P[-1]); P = np.array(Q)
    return P

strokes = [s for s in strokes if len(s) > 10]
# orient each stroke left->right-ish and order by start x (writing order)
out = []
for s in strokes:
    xy = [(p[1], p[0]) for p in s]
    if sum(p[1] for p in xy) / len(xy) < H * 0.14:
        continue  # sombra no topo do recorte
    dx, dy = abs(xy[-1][0] - xy[0][0]), abs(xy[-1][1] - xy[0][1])
    if (dy > dx * 1.1 and xy[0][1] > xy[-1][1]) or (dy <= dx * 1.1 and xy[0][0] > xy[-1][0]):
        xy = xy[::-1]  # verticais de cima para baixo, horizontais da esquerda para a direita
    out.append(xy)
out.sort(key=lambda s: min(p[0] for p in s))

allp = np.array([p for s in out for p in s], float)
x0, y0 = allp.min(0) - 8 * K
x1, y1 = allp.max(0) + 8 * K
sc = 1000 / (x1 - x0)
Wd = x1 - x0

# encadeia os traços em gestos contínuos: a caneta segue para o traço mais próximo
def d2(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
rest = [list(map(tuple, s)) for s in out]
chains, cur = [], rest.pop(0)
while rest:
    end, s = cur[-1], rest[0]  # ordem de escrita: da esquerda para a direita
    dx, dy = abs(s[-1][0] - s[0][0]), abs(s[-1][1] - s[0][1])
    if dy > dx * 1.1:
        rev = s[0][1] > s[-1][1]  # verticais de cima para baixo
    else:
        rev = d2(end, s[-1]) < d2(end, s[0])  # começa pela ponta mais perto da caneta
    dd, j = d2(end, s[-1] if rev else s[0]), 0
    s = rest.pop(j)
    s = s[::-1] if rev else s
    if dd < Wd * 0.09:
        cur = cur + s  # a caneta "voa" até o próximo traço sem levantar o ritmo
    else:
        chains.append(cur); cur = s
chains.append(cur)

def path_d(P, closed=False):
    P = (np.array(P, float) - [x0, y0]) * sc
    d = f"M{P[0][0]:.1f} {P[0][1]:.1f}"
    for i in range(1, len(P) - 1):
        m = (P[i] + P[i + 1]) / 2
        d += f"Q{P[i][0]:.1f} {P[i][1]:.1f} {m[0]:.1f} {m[1]:.1f}"
    return d + ("Z" if closed else f"L{P[-1][0]:.1f} {P[-1][1]:.1f}")

D = [path_d(smooth(rdp(c, 2.2), 3)) for c in chains]

# contorno real da tinta (com os furos de a, e, y)
import cv2
mask = ((a < 112) * 255).astype(np.uint8)  # tinta: limiar mais fino que o do esqueleto
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
cs, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
INK = ""
for c in cs:
    if cv2.contourArea(c) < 12:
        continue
    if c[:, 0, 1].mean() < H * 0.14:
        continue  # sombra do topo do recorte
    pts = c[:, 0, :].astype(float)
    k = np.ones(5) / 5  # suaviza o contorno (circular)
    pts = np.stack([np.convolve(np.r_[pts[-2:, a], pts[:, a], pts[:2, a]], k, "valid") for a in (0, 1)], 1)
    pts = pts[::4]
    if len(pts) < 4:
        continue
    INK += path_d(list(pts) + [pts[0]], closed=True)

dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
thick = float(np.percentile(dist[sk > 0], 95)) * 2 * sc
sig = {"vb": [1000, float(round((y1 - y0) * sc, 1))], "w": round(thick * 1.9 + 3, 1), "ink": INK, "d": D}
json.dump(sig, open(OUT, "w"), separators=(",", ":"))
print(len(D), "gestos", sig["vb"], "espessura", round(thick, 1), "máscara", sig["w"], len(INK), "chars de tinta")
