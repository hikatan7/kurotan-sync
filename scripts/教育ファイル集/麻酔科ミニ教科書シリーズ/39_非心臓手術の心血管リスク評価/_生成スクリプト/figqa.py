# -*- coding: utf-8 -*-
"""図版の版面検査。

figlib.Canvas.save に割り込んで、保存の直前に次を機械的に調べる。
  A) 文字どうしの重なり
  B) 文字がキャンバスからはみ出していないか
  C) 文字が、自分の属さない枠（FancyBboxPatch）にかぶっていないか
目視では見落とす重なりを、座標で拾うための道具。
"""
import sys
import figlib

TOL = 2.0           # この画素数までの接触は重なりとみなさない
report = []


def _rect(bb):
    return (bb.x0, bb.y0, bb.x1, bb.y1)


def _ov(a, b, tol=TOL):
    """2つの矩形の重なり面積（tol だけ内側に縮めてから判定）"""
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    w = min(ax1, bx1) - max(ax0, bx0) - tol
    h = min(ay1, by1) - max(ay0, by0) - tol
    return w * h if (w > 0 and h > 0) else 0.0


def check(cv, name):
    fig = cv.fig
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    H = cv.h

    texts = []
    for t in cv.ax.texts:
        if not t.get_text().strip():
            continue
        if t.get_alpha() == 0:                 # measure() の捨てテキスト
            continue
        try:
            bb = t.get_window_extent(r)
        except Exception:
            continue
        texts.append((t.get_text().strip(), _rect(bb)))

    issues = []

    # A) 文字どうし
    # 幅の広い行は数 px かすっただけで面積が大きく出るので、
    # 「縦の重なりが文字高の 35% 以上」かつ「横に 6px 以上」を条件にする。
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            s1, (ax0, ay0, ax1, ay1) = texts[i]
            s2, (bx0, by0, bx1, by1) = texts[j]
            vo = min(ay1, by1) - max(ay0, by0)
            ho = min(ax1, bx1) - max(ax0, bx0)
            hmin = min(ay1 - ay0, by1 - by0)
            if vo <= 0 or ho <= 6 or hmin <= 0:
                continue
            if vo / hmin >= 0.35:
                issues.append("文字の重なり  「%s」×「%s」 "
                              "(縦 %.0f px＝文字高の %.0f%%)"
                              % (s1[:26], s2[:26], vo, 100 * vo / hmin))

    # C) 文字が枠の境界をまたいでいないか（枠の中に完全に収まるか、
    #    まったく触れないかのどちらかであるべき）
    import matplotlib.colors as mcolors
    from matplotlib.patches import FancyArrowPatch
    patches = []
    for pt in cv.ax.patches:
        if isinstance(pt, FancyArrowPatch):    # 矢印は枠ではない
            continue
        try:
            pb = pt.get_window_extent(r)
        except Exception:
            continue
        if pb.width < 8 or pb.height < 8:
            continue
        patches.append((_rect(pb), pt))

    for s_, tr in texts:
        tx0, ty0, tx1, ty1 = tr
        for pr, pt in patches:
            px0, py0, px1, py1 = pr
            inside = (tx0 >= px0 - TOL and tx1 <= px1 + TOL
                      and ty0 >= py0 - TOL and ty1 <= py1 + TOL)
            if inside:
                continue
            vo = min(ty1, py1) - max(ty0, py0)
            ho = min(tx1, px1) - max(tx0, px0)
            th = ty1 - ty0
            if vo > 0.35 * th and ho > 10:
                issues.append("文字が枠をまたぐ  「%s」" % s_[:30])
                break

    # D) 白い文字が明るい面に乗っていないか
    for t in cv.ax.texts:
        if not t.get_text().strip() or t.get_alpha() == 0:
            continue
        try:
            rgb = mcolors.to_rgb(t.get_color())
        except Exception:
            continue
        if min(rgb) < 0.85:                    # 白系の文字だけを見る
            continue
        try:
            tb = t.get_window_extent(r)
        except Exception:
            continue
        cx = (tb.x0 + tb.x1) / 2
        cy = (tb.y0 + tb.y1) / 2
        under = None
        for pr, pt in patches:                 # 後に描いたものほど上
            px0, py0, px1, py1 = pr
            if px0 <= cx <= px1 and py0 <= cy <= py1:
                under = pt
        lum = 1.0
        if under is not None:
            try:
                fc = mcolors.to_rgb(under.get_facecolor())
                lum = 0.299 * fc[0] + 0.587 * fc[1] + 0.114 * fc[2]
            except Exception:
                pass
        if lum > 0.68:      # figlib の amber(0.60)・grey(0.59) は実物で可読
            issues.append("白文字が明るい面の上  「%s」（下地の明度 %.2f）"
                          % (t.get_text().strip()[:30], lum))

    # B) キャンバス外
    for s, (x0, y0, x1, y1) in texts:
        if x0 < -TOL or x1 > cv.w + TOL or y0 < -TOL or y1 > H + TOL:
            issues.append("枠外へはみ出し  「%s」 x[%.0f,%.0f] y[%.0f,%.0f]"
                          % (s[:26], x0, x1, y0, y1))

    if issues:
        report.append((name, issues))
    return issues


_orig_save = figlib.Canvas.save


def _save(self, path):
    import os
    check(self, os.path.basename(path))
    return _orig_save(self, path)


figlib.Canvas.save = _save

if __name__ == "__main__":
    import fig22_a
    import fig22_b
    for mod in (fig22_a, fig22_b):
        for n in sorted(d for d in dir(mod) if d.startswith("f") and d[1:].isdigit()):
            getattr(mod, n)()
    print("\n" + "=" * 66)
    if not report:
        print("版面の問題は検出されなかった。")
    else:
        for name, issues in report:
            print("\n■ %s  （%d件）" % (name, len(issues)))
            for i in issues:
                print("   -", i)
        print("\n合計 %d図 / %d件" % (len(report), sum(len(i) for _, i in report)))
    sys.exit(1 if report else 0)
