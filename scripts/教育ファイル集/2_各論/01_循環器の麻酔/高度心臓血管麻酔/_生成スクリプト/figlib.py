# -*- coding: utf-8 -*-
"""麻酔科ミニ教科書 図版 再作図ライブラリ

原図と同じ 200dpi / Yu Gothic + DejaVu Sans で、
「文字を測ってから枠を決める」ことで枠外はみ出しを構造的に防ぐ。

座標系はすべてピクセル（左上原点、y は下向き）。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib.transforms import Bbox

DPI = 200
JP = ["DejaVu Sans", "Yu Gothic"]          # 本文（原図と同じ組み合わせ）
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False

# 原図の配色
NAVY = "#1b2a49"
INK = "#22303f"
GREY = "#6b7785"
RED = "#c0392b"
BLUE = "#2e6da4"
GREEN = "#2e7d52"
ORANGE = "#d98e2b"
PURPLE = "#6b4fa0"

FILL = {
    "blue":  ("#eaf1f8", "#2e6da4"),
    "red":   ("#fceeec", "#c0392b"),
    "green": ("#eaf5ee", "#2e7d52"),
    "amber": ("#fdf3e3", "#d98e2b"),
    "grey":  ("#f2f4f6", "#8d97a3"),
    "purple": ("#f1ecf8", "#6b4fa0"),
    "navy":  ("#e8edf5", "#1b2a49"),
}


def LH(size, k=1.45):
    """フォントサイズ(pt) から行送り(px) を返す。200dpi なので 1pt = 2.78px。"""
    return size * DPI / 72.0 * k


class Canvas:
    """ピクセル座標で描く薄いラッパ"""

    def __init__(self, w, h, facecolor="white", family=None):
        self.w, self.h = w, h
        self.family = family or JP
        self.fig = plt.figure(figsize=(w / DPI, h / DPI), dpi=DPI,
                              facecolor=facecolor)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(h, 0)
        self.ax.axis("off")
        self.ax.set_facecolor(facecolor)
        self.fig.canvas.draw()
        self._r = self.fig.canvas.get_renderer()

    # ---------- 計測 ----------
    def measure(self, s, size, weight="normal", family=None):
        """文字列を描かずに (幅, 高さ) ピクセルで返す"""
        t = self.ax.text(0, 0, s, fontsize=size, weight=weight,
                         family=family or self.family, alpha=0)
        bb = t.get_window_extent(self._r)
        t.remove()
        return bb.width, bb.height

    def width(self, s, size, weight="normal"):
        return self.measure(s, size, weight)[0]

    def fit_size(self, lines, max_w, size, min_size=6.0, weight="normal"):
        """全行が max_w に収まる最大の字送りを返す（size から 0.25 刻みで縮小）"""
        s = size
        while s > min_size:
            if all(self.width(l, s, weight) <= max_w for l in lines):
                return s
            s -= 0.25
        return min_size

    # ---------- 折り返し ----------
    # 行頭禁則（この文字で行を始めない）
    _NO_START = "、。，．・）」』】〕〉》’”ぁぃぅぇぉっゃゅょゎヵヶァィゥェォッャュョ！？：；/％%）"
    # 行末禁則（この文字で行を終えない）
    _NO_END = "（「『【〔〈《‘“"

    def wrap(self, text, max_w, size, weight="normal"):
        """日本語混じり文を max_w 幅で折り返す。
        半角英数字・単位（例 150 mg/dL）の途中では絶対に切らない。"""
        toks = self._tokenize(text)
        lines, cur = [], ""
        for t in toks:
            trial = cur + t
            if cur and self.width(trial.rstrip(), size, weight) > max_w:
                lines.append(cur.rstrip())
                cur = t.lstrip() if t.strip() else ""
            else:
                cur = trial
        if cur.strip():
            lines.append(cur.rstrip())
        return self._apply_kinsoku(lines)

    @staticmethod
    def _tokenize(text):
        """英数字・記号のかたまりは1トークン、和文は1文字ずつ"""
        out, buf = [], ""
        ascii_run = "0123456789.,%/-+±≧≦<>=~×÷abcdefghijklmnopqrstuvwxyz" \
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for ch in text:
            if ch in ascii_run:
                buf += ch
            elif ch == " ":
                if buf:
                    buf += ch          # 単位前の空白は語に含める（150 mg を割らない）
                else:
                    out.append(ch)
            else:
                if buf:
                    out.append(buf)
                    buf = ""
                out.append(ch)
        if buf:
            out.append(buf)
        # 「数字＋空白」で終わるトークンは次と結合（150 + mg/dL → 150 mg/dL）
        merged, i = [], 0
        while i < len(out):
            t = out[i]
            while t.endswith(" ") and i + 1 < len(out) and out[i + 1].strip() \
                    and out[i + 1][0].isascii() and out[i + 1][0] not in "（「":
                t += out[i + 1]
                i += 1
            merged.append(t)
            i += 1
        return merged

    @classmethod
    def _apply_kinsoku(cls, lines):
        # 行頭禁則（、。）」など）は前の行へ追い込み、行末禁則（（「など）は次の行へ送る。
        # 最終行が 1 文字だけになったら、前の行から 1 文字もらって 2 文字にする（2026-09-28）
        out, carry = [], ""
        for ln in lines:
            ln = carry + ln
            carry = ""
            while out and ln and ln[0] in cls._NO_START:
                out[-1] += ln[0]
                ln = ln[1:]
            if ln and ln[-1] in cls._NO_END and len(ln) > 1:
                carry = ln[-1]
                ln = ln[:-1]
            if ln:
                out.append(ln)
        if carry:
            out.append(carry)
        if len(out) >= 2 and len(out[-1].strip()) == 1 and len(out[-2]) > 3                 and out[-2][-1] not in cls._NO_END:
            out[-1] = out[-2][-1] + out[-1]
            out[-2] = out[-2][:-1]
        return out or [""]

    # ---------- 描画 ----------
    def box(self, x, y, w, h, style="grey", lw=1.6, radius=8,
            fc=None, ec=None, z=1, alpha=1.0):
        f, e = FILL.get(style, FILL["grey"])
        p = FancyBboxPatch(
            (x + radius, y + radius), w - 2 * radius, h - 2 * radius,
            boxstyle=f"round,pad={radius}",
            facecolor=fc if fc is not None else f,
            edgecolor=ec if ec is not None else e,
            linewidth=lw, zorder=z, alpha=alpha, mutation_aspect=1)
        self.ax.add_patch(p)
        return p

    def rect(self, x, y, w, h, fc, ec="none", lw=0, z=1, alpha=1.0):
        p = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                      linewidth=lw, zorder=z, alpha=alpha)
        self.ax.add_patch(p)
        return p

    def text(self, x, y, s, size=12, color=INK, weight="normal",
             ha="center", va="center", z=5, family=None, linespacing=1.45):
        return self.ax.text(x, y, s, fontsize=size, color=color, weight=weight,
                            ha=ha, va=va, zorder=z, linespacing=linespacing,
                            family=family or self.family)

    def block(self, x, y, w, lines, size, color=INK, weight="normal",
              ha="center", lh=None, z=5):
        """複数行を上から積む。返り値は消費した高さ"""
        lh = lh or LH(size)
        cx = {"center": x + w / 2, "left": x, "right": x + w}[ha]
        for i, ln in enumerate(lines):
            self.text(cx, y + lh * (i + 0.5), ln, size=size, color=color,
                      weight=weight, ha=ha, va="center", z=z)
        return lh * len(lines)

    def arrow(self, p0, p1, color=GREY, lw=2.0, head=9, z=3, style="-|>"):
        a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=head,
                            color=color, linewidth=lw, zorder=z,
                            shrinkA=0, shrinkB=0)
        self.ax.add_patch(a)
        return a

    def title(self, x, y, s, size=17, color=NAVY, weight="bold", ha="left"):
        return self.text(x, y, s, size=size, color=color, weight=weight,
                         ha=ha, va="center")

    def save(self, path):
        self.fig.savefig(path, dpi=DPI, facecolor=self.fig.get_facecolor())
        plt.close(self.fig)


def textbox(cv, x, y, w, lines, size, style="grey", pad_x=14, pad_y=12,
            title=None, title_size=None, title_color=None, color=INK,
            weight="normal", title_weight="bold", lw=1.6, radius=8,
            min_h=None, lh_scale=1.45, fc=None, ec=None, dry=False):
    """行を収めきる高さの枠を描く。size は幅に収まるまで自動縮小。返り値は高さ。"""
    inner = w - 2 * pad_x
    all_lines = ([title] if title else []) + list(lines)
    ts = title_size or size
    # 幅に合わせて縮小。ただし 0.9 倍より小さくはせず、入らない行は折り返す（2026-09-28）
    s = cv.fit_size(list(lines), inner, size) if lines else size
    if lines and s < size * 0.9:
        s = size * 0.9
        wrapped = []
        for ln in lines:
            ws = cv.wrap(ln, inner, s, weight)
            # 開き括弧だけの行が出たら次の行とつなぐ
            k = 0
            while k < len(ws) - 1:
                if ws[k].strip() in ("（", "(", "「", "［"):
                    ws[k:k + 2] = [ws[k].strip() + ws[k + 1].lstrip()]
                k += 1
            wrapped.extend(ws)
        lines = wrapped
    tsz = cv.fit_size([title], inner, ts, weight=title_weight) if title else ts
    lh = LH(s, lh_scale)
    tlh = LH(tsz, lh_scale)
    h = pad_y * 2 + (tlh if title else 0) + lh * len(lines)
    if min_h:
        h = max(h, min_h)
    if dry:
        return h   # 描かずに高さだけ返す
    cv.box(x, y, w, h, style=style, lw=lw, radius=radius, fc=fc, ec=ec)
    cy = y + pad_y + (h - pad_y * 2 - (tlh if title else 0) - lh * len(lines)) / 2
    if title:
        cv.text(x + w / 2, cy + tlh / 2, title, size=tsz,
                color=title_color or FILL.get(style, FILL["grey"])[1],
                weight=title_weight)
        cy += tlh
    for i, ln in enumerate(lines):
        cv.text(x + w / 2, cy + lh * (i + 0.5), ln, size=s, color=color,
                weight=weight)
    return h


def duo(cv, cx, cy, a, b, size=24, col_a=None, col_b=None,
        lab_a=None, lab_b=None, lab_dy=44, lab_size=9.6,
        sep="対", sep_size=12, max_w=None, gap=30):
    """「14.4% 対 2.3%」のような二つの数字を、実測した幅で並べる。

    決め打ちのオフセットで置くと、桁数が増えたときに数字どうしが重なる。
    数字とラベルの実幅を測ってから配置し、枠に入らなければ文字を小さくする。
    """
    col_a = RED if col_a is None else col_a
    col_b = GREY if col_b is None else col_b
    s = float(size)
    while True:
        wa = cv.width(a, s, "bold")
        wb = cv.width(b, s, "bold")
        wt = cv.width(sep, sep_size)
        ca = max(wa, cv.width(lab_a, lab_size) if lab_a else 0.0)
        cb = max(wb, cv.width(lab_b, lab_size) if lab_b else 0.0)
        total = ca + cb + wt + gap * 2
        if max_w is None or total <= max_w or s <= 13.0:
            break
        s -= 1.0
    x0 = cx - total / 2
    xa = x0 + ca / 2
    xs = x0 + ca + gap + wt / 2
    xb = x0 + ca + gap + wt + gap + cb / 2
    cv.text(xa, cy, a, size=s, color=col_a, weight="bold")
    cv.text(xs, cy, sep, size=sep_size, color=GREY)
    cv.text(xb, cy, b, size=s, color=col_b, weight="bold")
    if lab_a:
        cv.text(xa, cy + lab_dy, lab_a, size=lab_size, color=col_a)
    if lab_b:
        cv.text(xb, cy + lab_dy, lab_b, size=lab_size, color=col_b)
    return total

def boxrow(cv, x0, y, bw, gap, items, size, title_size=None, min_h=None,
           pad_x=14, arrows=False, arrow_color="#8d97a3", **kw):
    """横に並ぶ同格の textbox を、いちばん背の高いものに高さを揃えて描く。
    items = [(title, [lines], style), ...]。長い行は字を縮めず折り返す。返り値は高さ。"""
    inner = bw - 2 * pad_x - 4
    allines = [l for it in items for l in it[1] if l]
    # まず 0.9 倍までは縮めて 1 行に収める。それでも入らない行だけ折り返す
    size = max(cv.fit_size(allines, inner, size), size * 0.9) if allines else size
    wl = []
    for ttl, lines, st in items:
        out = []
        for l in lines:
            out += cv.wrap(l, inner, size) if l else [""]
        wl.append(out)
    h = max(textbox(cv, 0, y, bw, ls, size, title=it[0], title_size=title_size,
                    pad_x=pad_x, dry=True, **kw) for it, ls in zip(items, wl))
    h = max(h, min_h or 0)
    for i, (it, ls) in enumerate(zip(items, wl)):
        x = x0 + i * (bw + gap)
        textbox(cv, x, y, bw, ls, size, style=it[2], title=it[0],
                title_size=title_size, pad_x=pad_x, min_h=h, **kw)
        if arrows and i < len(items) - 1:
            cv.arrow((x + bw + 6, y + h / 2), (x + bw + gap - 6, y + h / 2),
                     color=arrow_color, lw=2.2, head=13)
    return h
