# -*- coding: utf-8 -*-
"""図版の「枠から文字がはみ出す」を機械的に検出する。

figlib.Canvas.box / rect / text を差し替えて描画座標を記録し、
save() の時点で「ある枠と交差しているのに、その枠に収まっていない文字」を報告する。
"""
import sys
import os
import io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import figlib

PAD = 1.5          # 枠線の内側にこれだけ食い込むのは許容（px）
REPORT = []


def _install():
    C = figlib.Canvas
    _box, _rect, _text, _save = C.box, C.rect, C.text, C.save

    def box(self, x, y, w, h, *a, **k):
        self._boxes = getattr(self, "_boxes", [])
        self._boxes.append((x, y, x + w, y + h))
        return _box(self, x, y, w, h, *a, **k)

    def rect(self, x, y, w, h, *a, **k):
        self._boxes = getattr(self, "_boxes", [])
        self._boxes.append((x, y, x + w, y + h))
        return _rect(self, x, y, w, h, *a, **k)

    def text(self, x, y, s, *a, **k):
        t = _text(self, x, y, s, *a, **k)
        self._texts = getattr(self, "_texts", [])
        self._texts.append(t)
        return t

    def save(self, path, *a, **k):
        r = self.fig.canvas.get_renderer()
        boxes = getattr(self, "_boxes", [])
        for t in getattr(self, "_texts", []):
            bb = t.get_window_extent(renderer=r)
            inv = self.ax.transData.inverted()
            (x0, y0) = inv.transform((bb.x0, bb.y0))
            (x1, y1) = inv.transform((bb.x1, bb.y1))
            tx0, tx1 = min(x0, x1), max(x0, x1)
            ty0, ty1 = min(y0, y1), max(y0, y1)
            for (bx0, by0, bx1, by1) in boxes:
                # 枠と文字が「部分的に」重なっていたら、枠をまたいでいる
                ix = max(0.0, min(tx1, bx1) - max(tx0, bx0))
                iy = max(0.0, min(ty1, by1) - max(ty0, by0))
                area = max((tx1 - tx0) * (ty1 - ty0), 1e-6)
                frac = (ix * iy) / area
                if not (0.06 < frac < 0.94):
                    continue
                over = max(bx0 - tx0, tx1 - bx1, by0 - ty0, ty1 - by1)
                if over > PAD:
                    d = {"L": bx0 - tx0, "R": tx1 - bx1,
                         "T": by0 - ty0, "B": ty1 - by1}
                    dr = max(d, key=lambda k: d[k])
                    REPORT.append((os.path.basename(path),
                                   t.get_text()[:26],
                                   round(float(over), 1),
                                   "%s %d%%内 box=(%d,%d)-(%d,%d)"
                                   % (dr, round(frac * 100), bx0, by0, bx1, by1)))
                    break
        return _save(self, path, *a, **k)

    C.box, C.rect, C.text, C.save = box, rect, text, save


_install()

OUT = sys.argv[1]
for mod in sys.argv[2:]:
    sys.argv = [mod, OUT]
    src = open(mod, encoding="utf-8").read()
    exec(compile(src, mod, "exec"), {"__name__": "__main__", "__file__": mod})

with io.open("qa14/overflow.txt", "w", encoding="utf-8") as fh:
    fh.write("はみ出し %d 件" % len(REPORT) + chr(10))
    for f, s, o, dr in REPORT:
        fh.write("  %-26s %5.1f px  %-26s %s" % (f, o, dr, s) + chr(10))
print("report ->", len(REPORT))
