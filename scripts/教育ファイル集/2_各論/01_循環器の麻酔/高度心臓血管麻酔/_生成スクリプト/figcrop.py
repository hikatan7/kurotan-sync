# -*- coding: utf-8 -*-
"""縦長の図（アルゴリズム）は、余白を実測して切り詰める。

Canvas の高さを先に決めると、枠が伸びたときに下端が切れる。
そこで十分に高いキャンバスで描き、描画後に下の余白を落とす。
"""
from PIL import Image
import numpy as np


def crop_bottom(path, margin=46, top_margin=None):
    im = Image.open(path).convert("L")
    a = np.asarray(im)
    rows = np.where((a < 248).any(axis=1))[0]
    if len(rows) == 0:
        return
    bottom = min(a.shape[0], int(rows[-1]) + margin)
    top = 0
    if top_margin is not None:
        top = max(0, int(rows[0]) - top_margin)
    Image.open(path).crop((0, top, a.shape[1], bottom)).save(path)
    return bottom - top
