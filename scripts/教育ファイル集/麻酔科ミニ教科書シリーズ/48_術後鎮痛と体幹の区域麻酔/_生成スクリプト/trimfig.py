# -*- coding: utf-8 -*-
"""図版の下端に残る余白を切り落とす。

figlib の Canvas は高さを先に決めるため、枠の実高が見積りより小さいと
下に白が残る。左右・上は版面設計どおりなので、下だけを詰める。
"""
import os
import sys
import numpy as np
from PIL import Image

PAD = 44


def trim_bottom(path, pad=PAD):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    nonwhite = (a < 250).any(axis=2).any(axis=1)   # 行ごとに白以外があるか
    idx = np.nonzero(nonwhite)[0]
    if len(idx) == 0:
        return None
    last = int(idx[-1])
    new_h = min(a.shape[0], last + 1 + pad)
    if new_h >= a.shape[0] - 4:
        return None
    im.crop((0, 0, a.shape[1], new_h)).save(path)
    return a.shape[0], new_h


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "図版")
    for f in sorted(os.listdir(d)):
        if not f.endswith(".png"):
            continue
        r = trim_bottom(os.path.join(d, f))
        print("  %-26s %s" % (f, ("%d → %d" % r) if r else "変更なし"))
