# -*- coding: utf-8 -*-
"""表の列幅を、内容の量に応じて自動配分する。

これまでは autofit まかせで、結果として列が均等割りになり、
「段」のように数字しか入らない列と、長い文章が入る列が同じ幅になっていた。
"""
import io

p = "bookkit.py"
s = io.open(p, encoding="utf-8").read()

HELPERS = '''# 本文の版面幅（cm）。A4 21.0 − 左右余白 2.2×2。
TEXT_W = A4_W - MARGIN["left"] - MARGIN["right"]


def _em(ch):
    """1文字の幅。全角は 1.0、半角は 0.5 として数える。"""
    o = ord(ch)
    if o < 0x2000:
        return 0.5
    if 0x2000 <= o < 0x2100:
        return 0.55
    return 1.0


def _emw(s):
    return sum(_em(c) for c in str(s))


def auto_widths(header, rows, total=None, cap=26.0, floor_cm=1.1):
    """列ごとの必要量から幅（cm）を配分する。

    cap … 1セルの「自然な幅」の頭打ち。長文セルは折り返す前提なので、
           これがないと 1 列だけが表を占領してしまう。
    floor_cm … どの列もこれより狭くしない（見出しが潰れるのを防ぐ）。
    """
    total = total if total is not None else TEXT_W
    n = len(header)
    nat = []
    for i in range(n):
        head = _emw(header[i]) if header else 0.0
        body = max([_emw(r[i]) for r in rows], default=0.0)
        nat.append(max(head, min(body, cap), 2.0))
    ssum = sum(nat)
    w = [total * x / ssum for x in nat]
    # 下限を割った列を持ち上げ、その分を広い列から削る
    for _ in range(4):
        short = [i for i, x in enumerate(w) if x < floor_cm]
        if not short:
            break
        need = sum(floor_cm - w[i] for i in short)
        donors = [i for i in range(n) if w[i] > floor_cm]
        dsum = sum(w[i] - floor_cm for i in donors) or 1.0
        for i in short:
            w[i] = floor_cm
        for i in donors:
            w[i] -= need * (w[i] - floor_cm) / dsum
    # 丸め誤差を最後の列で吸収する
    w[-1] += total - sum(w)
    return w


def _fixed_layout(t):
    """列幅を固定する（これをしないと Word が勝手に割り直す）。"""
    tblPr = t._tbl.tblPr
    for tag in ("w:tblLayout",):
        old = tblPr.find(qn(tag))
        if old is not None:
            tblPr.remove(old)
    el = OxmlElement("w:tblLayout")
    el.set(qn("w:type"), "fixed")
    tblPr.append(el)


'''
assert "def table(doc, caption, header, rows" in s
s = s.replace("def table(doc, caption, header, rows", HELPERS + "def table(doc, caption, header, rows", 1)

# --- 幅の適用
OLD = '''    if widths:
        for row in t.rows:
            for i, wcm in enumerate(widths):
                row.cells[i].width = Cm(wcm)'''
NEW = '''    if widths is None:
        widths = auto_widths(header, rows)
    t.autofit = False
    _fixed_layout(t)
    for row in t.rows:
        for i, wcm in enumerate(widths):
            row.cells[i].width = Cm(wcm)'''
assert OLD in s
s = s.replace(OLD, NEW, 1)
s = s.replace("    t.style = \"Table Grid\"\n    t.autofit = True",
              "    t.style = \"Table Grid\"")

io.open(p, "w", encoding="utf-8").write(s)
print("bookkit: 列幅の自動配分を追加")
