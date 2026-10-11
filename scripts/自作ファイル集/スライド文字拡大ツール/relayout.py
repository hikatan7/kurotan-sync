# -*- coding: utf-8 -*-
"""行ごとに下へ伸ばして文字を大きくする（横幅は変えない）。PowerPoint COM で実測。
python relayout.py in.pptx out.pptx slide番号[,slide番号...] [fmax]
対象：タイトルより下、最下段の帯（キーメッセージ・出典行）より上の図形。"""
import os, sys
from win32com.client import gencache

GAP = 4.0


def runs(sh):
    rr = sh.TextFrame2.TextRange.Runs
    return [rr.Item(k) for k in range(1, rr.Count + 1)]


def is_text(sh):
    return sh.HasTextFrame and sh.TextFrame2.HasText


def nlines(sh):
    tr = sh.TextFrame.TextRange
    for k in range(1, 100):
        try:
            if tr.Lines(k, 1).Length == 0: return k - 1
        except Exception:
            return k - 1
    return 100


def need_h(sh):
    tf = sh.TextFrame2
    return tf.TextRange.BoundHeight + tf.MarginTop + tf.MarginBottom + 1.0


def zone(sl, H):
    """作業範囲：タイトル下端〜最下段の帯の上端"""
    shs = [sl.Shapes.Item(i) for i in range(1, sl.Shapes.Count + 1)]
    title_bottom = 0
    for s in shs:
        if is_text(s) and s.Top < H * 0.2:
            mx = max((r.Font.Size for r in runs(s)), default=0)
            if mx >= 18:
                title_bottom = max(title_bottom, s.Top + s.Height)
    # 下の帯：KEY MESSAGE の帯・出典・頁番号など、H*0.8 より下に始まる図形
    bottoms = [s.Top for s in shs if s.Top > H * 0.80]
    limit = min(bottoms) - 6 if bottoms else H - 14
    content = [s for s in shs if s.Top >= title_bottom - 2 and s.Top < limit and s.Top + s.Height <= limit + 2
               and not (is_text(s) and s.Top < H * 0.2 and max((r.Font.Size for r in runs(s)), default=0) >= 18)]
    return content, limit


def bands_of(content, zone_h):
    """背景の大枠（作業範囲の半分以上の高さ）を除いて、縦に重なる図形を行にまとめる"""
    big = [s for s in content if s.Height > zone_h * 0.5 and not s.HasTable]
    rest = sorted([s for s in content if s not in big], key=lambda s: s.Top)
    bands = []
    for s in rest:
        a, b = s.Top, s.Top + s.Height
        if bands and (min(b, bands[-1]["b"]) - a) > min(b - a, bands[-1]["b"] - bands[-1]["a"]) * 0.5:
            bands[-1]["b"] = max(bands[-1]["b"], b); bands[-1]["s"].append(s)
        else:
            bands.append({"a": a, "b": b, "s": [s]})
    return bands, big


def apply(sl, f, H, commit):
    content, limit = zone(sl, H)
    if not content:
        return None
    z0 = min(s.Top for s in content); z1 = max(s.Top + s.Height for s in content)
    bands, big = bands_of(content, z1 - z0)
    saved = []
    one = {}
    tsaved = []
    for s in content:
        if s.HasTable:
            t = s.Table; cells = []; rows = []
            for ri in range(1, t.Rows.Count + 1):
                rows.append((t.Rows(ri), t.Rows(ri).Height))
                for ci in range(1, t.Columns.Count + 1):
                    sh2 = t.Cell(ri, ci).Shape
                    if sh2.HasTextFrame and sh2.TextFrame2.HasText:
                        cells.append((ri, sh2, [(r, r.Font.Size) for r in runs(sh2)]))
            tsaved.append((s, s.Height, rows, cells))
        rs = [(r, r.Font.Size) for r in runs(s)] if is_text(s) else []
        saved.append((s, s.Top, s.Height, rs))
        if is_text(s):
            one[id(s)] = nlines(s) <= 1 and len(s.TextFrame2.TextRange.Text.strip()) <= 16
        if is_text(s):
            try:
                s.TextFrame2.AutoSize = 0
            except Exception:
                pass
            for r, sz in rs:
                if sz < 18:
                    r.Font.Size = round(sz * f * 2) / 2
    tgrow = {}
    for s, h0, rows, cells in tsaved:
        for ri, sh2, rs in cells:
            for r, sz in rs: r.Font.Size = round(sz * f * 2) / 2
        tot = 0.0
        for ri, (row, rh) in enumerate(rows, 1):
            need = rh
            for rj, sh2, rs in cells:
                if rj == ri:
                    tf = sh2.TextFrame2
                    need = max(need, tf.TextRange.BoundHeight + tf.MarginTop + tf.MarginBottom + 1)
            row.Height = need; tot += need
        tgrow[id(s)] = tot - sum(rh for _, rh in rows)
    # もともと1行の文字は1行に戻す（同じ列・同じ元サイズでそろえる）
    grp = {}
    for s, t, h, rs in saved:
        if rs and one.get(id(s)) and nlines(s) > 1:
            k = 1.0
            while k > 0.55 and nlines(s) > 1:
                k -= 0.05
                for r, sz in rs:
                    if sz < 18: r.Font.Size = max(sz, round(sz * f * k * 2) / 2)
            key = (round(max(sz for _, sz in rs), 1), round(s.Left / 10))
            grp[key] = min(grp.get(key, 1.0), k)
    for s, t, h, rs in saved:
        if rs and one.get(id(s)):
            key = (round(max(sz for _, sz in rs), 1), round(s.Left / 10))
            if key in grp:
                for r, sz in rs:
                    if sz < 18: r.Font.Size = max(sz, round(sz * f * grp[key] * 2) / 2)
    # 行ごとの伸び
    shift = 0.0; plan = []
    for bd in bands:
        grow = 0.0
        for s in bd["s"]:
            if is_text(s):
                grow = max(grow, need_h(s) - s.Height)
            if id(s) in tgrow:
                grow = max(grow, tgrow[id(s)])
        grow = max(grow, 0.0)
        plan.append((bd, shift, grow))
        shift += grow
    total = shift
    ok = z1 + total <= limit
    if commit and ok:
        for bd, sh0, grow in plan:
            bh = bd["b"] - bd["a"]
            for s in bd["s"]:
                top0, h0 = s.Top, s.Height
                s.Top = top0 + sh0
                full = h0 >= bh - 3  # 行いっぱいの図形（背景の四角など）は行と一緒に伸ばす
                if s.HasTable:
                    pass
                elif is_text(s):
                    s.Height = max(h0 + (grow if full else 0), need_h(s))
                elif full:
                    s.Height = h0 + grow
                else:
                    # 行の中の小さな飾り：行の中で同じ割合の位置へ
                    s.Top = top0 + sh0 + (top0 - bd["a"]) / max(bh, 1) * grow
        for s in big:
            # 大枠：覆う範囲の行の伸びを合計
            a, b = s.Top, s.Top + s.Height
            before = sum(g for bd, sh0, g in plan if bd["b"] <= a + 1)
            inside = sum(g for bd, sh0, g in plan if bd["a"] >= a - 1 and bd["b"] <= b + 1)
            s.Top = a + before; s.Height = s.Height + inside
    else:
        for s, h0, rows, cells in tsaved:
            for ri, sh2, rs in cells:
                for r, sz in rs: r.Font.Size = sz
            for row, rh in rows: row.Height = rh
        for s, t, h, rs in saved:
            for r, sz in rs:
                r.Font.Size = sz
            s.Top = t; s.Height = h
    return ok, round(z1 + total - limit, 1)


def main(src, dst, slides, fmax=1.8):
    import shutil
    shutil.copyfile(src, dst)
    app = gencache.EnsureDispatch("PowerPoint.Application")
    pr = app.Presentations.Open(os.path.abspath(dst), False, False, False)
    H = pr.PageSetup.SlideHeight
    out = []
    for n in slides:
        sl = pr.Slides(n)
        best = 1.0; f = 1.0
        while f + 0.05 <= fmax + 1e-9:
            f2 = round(f + 0.05, 2)
            r = apply(sl, f2, H, commit=False)
            if r and r[0]:
                best = f2; f = f2
            else:
                break
        if best > 1.0:
            apply(sl, best, H, commit=True)
        out.append((n, best))
    pr.Save(); pr.Close()
    return out


if __name__ == "__main__":
    sl = [int(x) for x in sys.argv[3].split(",")]
    print(main(sys.argv[1], sys.argv[2], sl, float(sys.argv[4]) if len(sys.argv) > 4 else 1.8))
