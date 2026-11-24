"""Real-ESRGAN x4plus (RRDBNet) em NumPy puro, sem PyTorch.

Uso: python3 super_resolucao.py RealESRGAN_x4plus.pth entrada.png saida.png
Pesos: https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
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
        print(f"bloco {i + 1}/23 {time.time() - t:.1f}s", flush=True)
    feat = feat + conv(body, "conv_body")
    feat = conv(up2(feat), "conv_up1", 1)
    feat = conv(up2(feat), "conv_up2", 1)
    return conv(conv(feat, "conv_hr", 1), "conv_last")


if __name__ == "__main__":
    W.update({k: v.astype(np.float32) for k, v in load_pth(sys.argv[1]).items()})
    im = np.asarray(Image.open(sys.argv[2]).convert("RGB")).astype(np.float32) / 255
    out = np.clip(run(im), 0, 1)
    Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(sys.argv[3])
    print("ok", out.shape)
