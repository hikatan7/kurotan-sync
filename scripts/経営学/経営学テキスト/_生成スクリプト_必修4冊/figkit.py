# -*- coding: utf-8 -*-
"""必修4冊の図版。文字を測ってから枠を決める figlib を土台に、よく使う型を4つ用意する。

cards  … 見出しつきの枠を格子に並べる（概念の並列）
flow   … 左から右へ矢印でつなぐ（手順・因果）
matrix … 2×2 の象限（二軸での分類）
bars   … 棒グラフ（数値はすべて架空）
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import Canvas, textbox, LH, NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE, JP, DPI, FILL

plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False
W = 1520
STYLES = ["blue", "green", "amber", "purple", "red", "navy"]


def _title(cv, s):
    cv.title(W / 2, 44, s, size=15, ha="center")
    return 90


def cards(path, title, items, cols=3, body=10.6, head=12.5):
    """items: [(見出し, [行, …])]"""
    gap = 36
    cw = (W - 80 - gap * (cols - 1)) / cols
    # 高さを先に測る（同じ段は同じ高さに揃える）
    probe = Canvas(W, 400)
    hs = []
    for hd, lines in items:
        hs.append(textbox(probe, 0, 0, cw, lines, body, title=hd, title_size=head))
    plt.close(probe.fig)
    rows = [hs[i:i + cols] for i in range(0, len(hs), cols)]
    rh = [max(r) for r in rows]
    H = int(90 + sum(rh) + gap * (len(rows) - 1) + 40)
    cv = Canvas(W, H)
    y = _title(cv, title)
    for r, h in enumerate(rh):
        row = items[r * cols:(r + 1) * cols]
        x0 = (W - (len(row) * cw + gap * (len(row) - 1))) / 2
        for c, (hd, lines) in enumerate(row):
            textbox(cv, x0 + c * (cw + gap), y, cw, lines, body, title=hd,
                    title_size=head, style=STYLES[(r * cols + c) % len(STYLES)], min_h=h)
        y += h + gap
    cv.save(path)


def flow(path, title, steps, body=10.4, head=12.5, note=None):
    """steps: [(見出し, [行, …])] を横一列に矢印でつなぐ"""
    n = len(steps)
    gap = 54
    cw = (W - 80 - gap * (n - 1)) / n
    probe = Canvas(W, 400)
    h = max(textbox(probe, 0, 0, cw, l, body, title=t, title_size=head) for t, l in steps)
    plt.close(probe.fig)
    nh = 0
    if note:
        nh = 110
    H = int(90 + h + 40 + nh)
    cv = Canvas(W, H)
    y = _title(cv, title)
    for i, (t, l) in enumerate(steps):
        x = 40 + i * (cw + gap)
        textbox(cv, x, y, cw, l, body, title=t, title_size=head,
                style=STYLES[i % len(STYLES)], min_h=h)
        if i < n - 1:
            cv.arrow((x + cw + 6, y + h / 2), (x + cw + gap - 6, y + h / 2), color=GREY, lw=2.4, head=14)
    if note:
        textbox(cv, 40, y + h + 26, W - 80, [note], 10.2, style="grey")
    cv.save(path)


def matrix(path, title, xlab, ylab, quads, body=10.4, head=12.5):
    """quads: [左上, 右上, 左下, 右下]、各 (見出し, [行])。xlab=(左, 右), ylab=(下, 上)"""
    ox, oy = 170, 110
    cw = (W - ox - 60 - 30) / 2
    probe = Canvas(W, 400)
    h = max(textbox(probe, 0, 0, cw, l, body, title=t, title_size=head) for t, l in quads)
    plt.close(probe.fig)
    H = int(oy + h * 2 + 30 + 110)
    cv = Canvas(W, H)
    _title(cv, title)
    pos = [(ox, oy), (ox + cw + 30, oy), (ox, oy + h + 30), (ox + cw + 30, oy + h + 30)]
    sty = ["amber", "green", "grey", "blue"]
    for (x, y), (t, l), s in zip(pos, quads, sty):
        textbox(cv, x, y, cw, l, body, title=t, title_size=head, style=s, min_h=h)
    yb = oy + 2 * h + 30 + 40
    cv.arrow((ox, yb), (W - 60, yb), color=NAVY, lw=2.2, head=14)
    cv.text(ox + cw / 2, yb + 30, xlab[0], size=11, color=NAVY, weight="bold")
    cv.text(ox + cw * 1.5 + 30, yb + 30, xlab[1], size=11, color=NAVY, weight="bold")
    cv.arrow((ox - 40, oy + 2 * h + 30), (ox - 40, oy), color=NAVY, lw=2.2, head=14)
    cv.text(ox - 95, oy + h / 2, ylab[1], size=11, color=NAVY, weight="bold")
    cv.text(ox - 95, oy + h * 1.5 + 30, ylab[0], size=11, color=NAVY, weight="bold")
    cv.save(path)


def bars(path, title, labels, series, ylabel="", note=None, horizontal=False):
    """series: [(凡例, [値…], 色名)]"""
    col = {"blue": BLUE, "red": RED, "green": GREEN, "orange": ORANGE, "grey": GREY, "purple": PURPLE}
    fig, ax = plt.subplots(figsize=(W / DPI, 3.4), dpi=DPI)
    n = len(series)
    wid = 0.8 / n
    import numpy as np
    xs = np.arange(len(labels))
    for i, (lab, vals, c) in enumerate(series):
        off = xs - 0.4 + wid * (i + 0.5)
        if horizontal:
            bs = ax.barh(off, vals, height=wid, color=col.get(c, c), label=lab)
        else:
            bs = ax.bar(off, vals, width=wid, color=col.get(c, c), label=lab)
        for b, v in zip(bs, vals):
            if horizontal:
                ax.text(b.get_width(), b.get_y() + b.get_height() / 2, " %g" % v, va="center", fontsize=8.5, color=INK)
            else:
                ax.text(b.get_x() + b.get_width() / 2, b.get_height(), "%g" % v, ha="center", va="bottom", fontsize=8.5, color=INK)
    if horizontal:
        ax.set_yticks(xs, labels, fontsize=9.5)
        ax.invert_yaxis()
        ax.set_xlabel(ylabel, fontsize=9.5)
    else:
        ax.set_xticks(xs, labels, fontsize=9.5)
        ax.set_ylabel(ylabel, fontsize=9.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title(title, fontsize=12, color=NAVY, weight="bold")
    if n > 1:
        ax.legend(frameon=False, fontsize=9)
    if note:
        fig.text(0.99, 0.01, note, ha="right", fontsize=8, color=GREY)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
