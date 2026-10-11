# -*- coding: utf-8 -*-
"""図版の文字の重なりを、描画時の実測で洗い出す。

Canvas.save の直前に、その図に置かれた文字の外接矩形を全部とり、
互いに食い込んでいる組を報告する。目視では見落とす重なりを拾う。
"""
import os, sys, importlib
import figlib

HITS = []
_orig_save = figlib.Canvas.save


def _boxes(cv):
    out = []
    for t in cv.ax.texts:
        s = t.get_text().strip()
        if not s:
            continue
        bb = t.get_window_extent(cv._r)
        out.append((s, bb.x0, bb.y0, bb.x1, bb.y1))
    return out


def _check(cv, path):
    bs = _boxes(cv)
    name = os.path.basename(path)
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            s1, a0, b0, a1, b1 = bs[i]
            s2, c0, d0, c1, d1 = bs[j]
            # 外接矩形は文字より少し大きい。1 割ずつ縮めて判定する。
            mw1, mh1 = (a1 - a0) * .10, (b1 - b0) * .10
            mw2, mh2 = (c1 - c0) * .10, (d1 - d0) * .10
            ix = min(a1 - mw1, c1 - mw2) - max(a0 + mw1, c0 + mw2)
            iy = min(b1 - mh1, d1 - mh2) - max(b0 + mh1, d0 + mh2)
            if ix <= 0 or iy <= 0:
                continue
            area = ix * iy
            small = min((a1 - a0) * (b1 - b0), (c1 - c0) * (d1 - d0))
            if small > 0 and area / small > 0.12:
                HITS.append((name, round(area / small, 2),
                             s1[:26].replace("\n", "/"), s2[:26].replace("\n", "/")))


def save(self, path):
    _check(self, path)
    return _orig_save(self, path)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    figlib.Canvas.save = save
    for n in range(1, 9):
        for part in ("a", "b"):
            mod = importlib.import_module("fig%d%s" % (n, part))
            if hasattr(mod, "main"):
                mod.main()
            else:
                for nm in dir(mod):
                    f = getattr(mod, nm)
                    if callable(f) and nm[0] in "fghmnqrs" and nm[1:].isdigit():
                        f()
    print("=== 文字の重なり %d 件 ===" % len(HITS))
    for h in sorted(HITS):
        print("  %-34s %.2f  「%s」×「%s」" % h)


if __name__ == "__main__":
    main()
