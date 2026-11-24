"""Real-ESRGAN em NumPy puro, sem PyTorch: x4plus (RRDBNet) ou general-x4v3 (compacto, ~14x mais rápido).

Uso: python3 super_resolucao.py PESOS.pth entrada.png saida.png [largura_final]
Pesos: https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
       https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth
A imagem é processada em faixas com sobreposição, então fotos grandes cabem na memória.
"""
import pickle, sys, time, zipfile
import numpy as np
from PIL import Image


def load_pth(path):
    zf = zipfile.ZipFile(path)
    root = zf.namelist()[0].split("/")[0]
    storages = {}

    def storage(key):
        if key not in storages:
            storages[key] = np.frombuffer(zf.read(f"{root}/data/{key}"), dtype=np.float32)
        return storages[key]

    def rebuild(st, offset, size, stride, *a):
        if not size:
            return st[offset:offset + 1].reshape(())
        return np.lib.stride_tricks.as_strided(st[offset:], shape=size, strides=[s * 4 for s in stride]).copy()

    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if name == "_rebuild_tensor_v2":
                return rebuild
            if mod == "collections" and name == "OrderedDict":
                import collections
                return collections.OrderedDict
            if mod.startswith("torch"):
                return lambda *a, **k: None
            return super().find_class(mod, name)

        def persistent_load(self, pid):
            return storage(pid[2])

    sd = U(zf.open(f"{root}/data.pkl")).load()
    return sd.get("params_ema", sd.get("params", sd))


W = {}


def conv(x, name, act=False):
    w, b = W[name + ".weight"], W[name + ".bias"]  # (out,in,3,3)
    H, Wd, C = x.shape
    p = np.pad(x, ((1, 1), (1, 1), (0, 0)))
    cols = np.concatenate([p[dy:dy + H, dx:dx + Wd] for dy in range(3) for dx in range(3)], axis=2)
    k = w.transpose(2, 3, 1, 0).reshape(9 * C, -1)
    y = (cols.reshape(-1, 9 * C) @ k).reshape(H, Wd, -1) + b
    if act:
        np.maximum(y, 0.2 * y, out=y)
    return y


def rdb(x, n):
    x1 = conv(x, n + ".conv1", 1)
    x2 = conv(np.concatenate([x, x1], 2), n + ".conv2", 1)
    x3 = conv(np.concatenate([x, x1, x2], 2), n + ".conv3", 1)
    x4 = conv(np.concatenate([x, x1, x2, x3], 2), n + ".conv4", 1)
    x5 = conv(np.concatenate([x, x1, x2, x3, x4], 2), n + ".conv5")
    return x5 * 0.2 + x


def up2(x):
    return x.repeat(2, 0).repeat(2, 1)


def run(img):
    feat = conv(img, "conv_first")
    body = feat
    for i in range(23):
        t = time.time()
        o = rdb(rdb(rdb(body, f"body.{i}.rdb1"), f"body.{i}.rdb2"), f"body.{i}.rdb3")
        body = o * 0.2 + body
    feat = feat + conv(body, "conv_body")
    feat = conv(up2(feat), "conv_up1", 1)
    feat = conv(up2(feat), "conv_up2", 1)
    return conv(conv(feat, "conv_hr", 1), "conv_last")


def run_compact(img):
    x = img
    n = max(int(k.split(".")[1]) for k in W if k.startswith("body."))
    for i in range(n + 1):
        k = f"body.{i}"
        if k + ".bias" in W:
            x = conv(x, k)
        else:  # PReLU
            a = W[k + ".weight"]
            x = np.maximum(x, 0) + a * np.minimum(x, 0)
    H, Wd, _ = x.shape
    x = x.reshape(H, Wd, 3, 4, 4).transpose(0, 3, 1, 4, 2).reshape(H * 4, Wd * 4, 3)
    return x + img.repeat(4, 0).repeat(4, 1)


def tiled(img, fn, band=128, pad=40):
    H = img.shape[0]
    out = np.zeros((H * 4, img.shape[1] * 4, 3), np.float32)
    for y in range(0, H, band):
        a, b = max(0, y - pad), min(H, y + band + pad)
        t = time.time()
        r = fn(img[a:b])
        out[y * 4:min(H, y + band) * 4] = r[(y - a) * 4:(y - a + min(band, H - y)) * 4]
        print(f"faixa {y}/{H} {time.time() - t:.1f}s", flush=True)
    return out


if __name__ == "__main__":
    W.update({k: v.astype(np.float32) for k, v in load_pth(sys.argv[1]).items()})
    im = np.asarray(Image.open(sys.argv[2]).convert("RGB")).astype(np.float32) / 255
    fn = run if "conv_first.weight" in W else run_compact
    out = np.clip(tiled(im, fn), 0, 1)
    res = Image.fromarray((out * 255 + 0.5).astype(np.uint8))
    if len(sys.argv) > 4:
        w = int(sys.argv[4])
        res = res.resize((w, round(res.height * w / res.width)), Image.LANCZOS)
    res.save(sys.argv[3])
    print("ok", res.size)
