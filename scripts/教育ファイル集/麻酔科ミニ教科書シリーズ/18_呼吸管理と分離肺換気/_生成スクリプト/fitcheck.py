# -*- coding: utf-8 -*-
"""図版がキャンバスの外へはみ出していないかを機械的に確認する。

figlib.Canvas.save を差し替え、描画済みのテキストと図形の座標を
キャンバス矩形と突き合わせて報告する。
使い方: python fitcheck.py <出力先> fig18_a.py fig18_b.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import figlib

REPORT = []
MARGIN = 2.0


def _install():
    C = figlib.Canvas
    _text, _box, _rect, _save = C.text, C.box, C.rect, C.save

    def text(self, x, y, s, *a, **k):
        t = _text(self, x, y, s, *a, **k)
        self._items = getattr(self, "_items", [])
        self._items.append(("text", t, s))
        return t

    def box(self, x, y, w, h, *a, **k):
        self._shapes = getattr(self, "_shapes", [])
        self._shapes.append((x, y, x + w, y + h))
        return _box(self, x, y, w, h, *a, **k)

    def rect(self, x, y, w, h, *a, **k):
        self._shapes = getattr(self, "_shapes", [])
        self._shapes.append((x, y, x + w, y + h))
        return _rect(self, x, y, w, h, *a, **k)

    def save(self, path, *a, **k):
        r = self.fig.canvas.get_renderer()
        inv = self.ax.transData.inverted()
        name = os.path.basename(path)
        for kind, t, s in getattr(self, "_items", []):
            bb = t.get_window_extent(renderer=r)
            (x0, y0) = inv.transform((bb.x0, bb.y0))
            (x1, y1) = inv.transform((bb.x1, bb.y1))
            tx0, tx1 = min(x0, x1), max(x0, x1)
            ty0, ty1 = min(y0, y1), max(y0, y1)
            over = max(-tx0, tx1 - self.w, -ty0, ty1 - self.h)
            if over > MARGIN:
                side = {"左": -tx0, "右": tx1 - self.w,
                        "上": -ty0, "下": ty1 - self.h}
                REPORT.append((name, "文字", max(side, key=lambda q: side[q]),
                               round(float(over), 1), s[:30]))
        for (bx0, by0, bx1, by1) in getattr(self, "_shapes", []):
            over = max(-bx0, bx1 - self.w, -by0, by1 - self.h)
            if over > MARGIN:
                side = {"左": -bx0, "右": bx1 - self.w,
                        "上": -by0, "下": by1 - self.h}
                REPORT.append((name, "枠", max(side, key=lambda q: side[q]),
                               round(float(over), 1), ""))
        return _save(self, path, *a, **k)

    C.text, C.box, C.rect, C.save = text, box, rect, save


_install()

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
for mod in sys.argv[2:]:
    path = mod if os.path.isabs(mod) else os.path.join(HERE, mod)
    sys.argv = [path, OUT]
    src = open(path, encoding="utf-8").read()
    exec(compile(src, path, "exec"), {"__name__": "__main__", "__file__": path})

if not REPORT:
    print("はみ出し 0 件")
else:
    print("はみ出し %d 件" % len(REPORT))
    for name, kind, side, over, s in REPORT:
        print("  %-30s %s %s へ %6.1f px  %s" % (name, kind, side, over, s))
