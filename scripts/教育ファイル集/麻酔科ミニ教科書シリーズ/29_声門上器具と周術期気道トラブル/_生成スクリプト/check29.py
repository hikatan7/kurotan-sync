# -*- coding: utf-8 -*-
"""㉙ 図版の自動点検

二つを見る。
 ① キャンバスからの食み出し（枠・文字が W×H の外へ出ていないか）
 ② 枠の内側からの食み出し（文字の中心がある枠から、その文字が出ていないか）

使い方： python check29.py <出力先> <図版スクリプト...>
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib

BOXES = []      # (x0, y0, x1, y1)
TEXTS = []      # (x0, y0, x1, y1, s)
LIMIT = [1520, 1500]

_box = figlib.Canvas.box
_rect = figlib.Canvas.rect
_text = figlib.Canvas.text


def box(self, x, y, w, h, *a, **k):
    BOXES.append((x, y, x + w, y + h))
    LIMIT[0], LIMIT[1] = self.w, self.h
    return _box(self, x, y, w, h, *a, **k)


def rect(self, x, y, w, h, *a, **k):
    BOXES.append((x, y, x + w, y + h))
    return _rect(self, x, y, w, h, *a, **k)


def text(self, x, y, s, size=12, **k):
    t = _text(self, x, y, s, size=size, **k)
    try:
        bb = t.get_window_extent(self._r)
        TEXTS.append((bb.x0, self.h - bb.y1, bb.x1, self.h - bb.y0, str(s)))
    except Exception:
        pass
    return t


figlib.Canvas.box = box
figlib.Canvas.rect = rect
figlib.Canvas.text = text


def run(mod):
    m = __import__(mod)
    names = sorted(n for n in dir(m)
                   if n.startswith("f") and n[1:3].isdigit())
    bad = 0
    for n in names:
        del BOXES[:]
        del TEXTS[:]
        getattr(m, n)()
        Wc, Hc = LIMIT
        # ① キャンバス外
        for x0, y0, x1, y1, s in TEXTS:
            if x0 < -2 or y0 < -2 or x1 > Wc + 2 or y1 > Hc + 2:
                print("  [canvas] %s  %s  (%.0f,%.0f)-(%.0f,%.0f)"
                      % (n, s[:24], x0, y0, x1, y1))
                bad += 1
        for x0, y0, x1, y1 in BOXES:
            if x0 < -2 or y0 < -2 or x1 > Wc + 2 or y1 > Hc + 2:
                print("  [canvas] %s  枠  (%.0f,%.0f)-(%.0f,%.0f)"
                      % (n, x0, y0, x1, y1))
                bad += 1
        # ② 枠の内側から溢れた文字
        for tx0, ty0, tx1, ty1, s in TEXTS:
            cx, cy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
            host = None
            for bx0, by0, bx1, by1 in BOXES:
                if bx0 <= cx <= bx1 and by0 <= cy <= by1:
                    a = (bx1 - bx0) * (by1 - by0)
                    if host is None or a < host[4]:
                        host = (bx0, by0, bx1, by1, a)
            if host is None:
                continue
            bx0, by0, bx1, by1, _ = host
            over = max(bx0 - tx0, tx1 - bx1, by0 - ty0, ty1 - by1)
            if over > 3:
                print("  [box] %s  %s  はみ出し %.0f px" % (n, s[:24], over))
                bad += 1
    print("%s : %d 件" % (mod, bad))
    return bad


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    sys.argv = [sys.argv[0], out]
    total = 0
    for mod in ["fig29a", "fig29b", "fig29c"]:
        total += run(mod)
    print("合計 %d 件" % total)
