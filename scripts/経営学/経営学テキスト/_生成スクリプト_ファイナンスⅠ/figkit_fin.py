# -*- coding: utf-8 -*-
"""ファイナンスⅠの図版。figkit の4型（cards/flow/matrix/bars）に、数値の図を足す。

lines    … 折れ線（NPVプロファイル、資本コストと負債比率など）
tornado  … 感度分析のトルネード図
tree     … 待つオプションの決定木
stack    … DCF の現在価値の内訳（積み上げ棒）
数値はすべて calc.py から渡す。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figkit import *          # noqa: F401,F403  cards / flow / matrix / bars
from figkit import W, plt
from figlib import Canvas, textbox, NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE, DPI

COL = {"blue": BLUE, "red": RED, "green": GREEN, "orange": ORANGE, "grey": GREY,
       "purple": PURPLE, "navy": NAVY}


def _finish(fig, ax, title, note, path):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title(title, fontsize=12.5, color=NAVY, weight="bold")
    if note:
        fig.text(0.99, 0.01, note, ha="right", fontsize=8.5, color=GREY)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)


def lines(path, title, series, xlabel, ylabel, marks=(), hline=None, note=None, h=3.6,
          xfmt="%g", legend_loc="best"):
    """series: [(凡例, xs, ys, 色名, 線種)]  marks: [(x, y, ラベル, dx, dy)]"""
    fig, ax = plt.subplots(figsize=(W / DPI, h), dpi=DPI)
    for lab, xs, ys, c, ls in series:
        ax.plot(xs, ys, color=COL.get(c, c), lw=2.4, ls=ls, label=lab)
    if hline is not None:
        ax.axhline(hline, color=GREY, lw=1.0)
    for x, y, lab, dx, dy in marks:
        ax.plot([x], [y], "o", color=INK, ms=5)
        ax.annotate(lab, (x, y), xytext=(x + dx, y + dy), fontsize=9.5, color=INK,
                    arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8))
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.tick_params(labelsize=9.5)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: xfmt % v))
    ax.legend(frameon=False, fontsize=9.5, loc=legend_loc)
    _finish(fig, ax, title, note, path)


def tornado(path, title, rows, base, xlabel, note=None):
    """rows: [(項目, 悪い側の値, 良い側の値)]（振れ幅の大きい順）"""
    fig, ax = plt.subplots(figsize=(W / DPI, 0.55 * len(rows) + 1.3), dpi=DPI)
    for i, (lab, lo, hi) in enumerate(rows):
        ax.barh(i, lo - base, left=base, color=RED, height=0.6)
        ax.barh(i, hi - base, left=base, color=BLUE, height=0.6)
        ax.text(lo, i, "%s " % format(round(lo), ","), ha="right", va="center", fontsize=9, color=INK)
        ax.text(hi, i, " %s" % format(round(hi), ","), ha="left", va="center", fontsize=9, color=INK)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=9.8)
    ax.invert_yaxis()
    ax.axvline(base, color=INK, lw=1.2)
    ax.axvline(0, color=GREY, lw=1.0, ls="--")
    lo = min(r[1] for r in rows)
    hi = max(r[2] for r in rows)
    pad = (hi - lo) * 0.16
    ax.set_xlim(lo - pad, hi + pad)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.tick_params(axis="x", labelsize=9.5)
    _finish(fig, ax, title, note, path)


def stack(path, title, labels, vals, colors, ylabel, total_label, note=None):
    """左に各年の現在価値、右端に合計（＝事業価値）を積み上げで示す"""
    import numpy as np
    fig, ax = plt.subplots(figsize=(W / DPI, 3.5), dpi=DPI)
    xs = np.arange(len(labels) + 1)
    for x, v, c in zip(xs, vals, colors):
        b = ax.bar(x, v, color=COL.get(c, c), width=0.62)
        ax.text(x, v, format(round(v), ","), ha="center", va="bottom", fontsize=9, color=INK)
    bottom = 0.0
    for v, c in zip(vals, colors):
        ax.bar(xs[-1], v, bottom=bottom, color=COL.get(c, c), width=0.62, edgecolor="white", lw=0.8)
        bottom += v
    ax.text(xs[-1], bottom, format(round(bottom), ","), ha="center", va="bottom", fontsize=9.5,
            color=NAVY, weight="bold")
    ax.set_xticks(xs, list(labels) + [total_label], fontsize=9.5)
    ax.set_ylabel(ylabel, fontsize=10)
    _finish(fig, ax, title, note, path)


def tree(path, title, root, branches, wait, note=None):
    """root: 今すぐ投資の期待NPV表示, branches: [(確率ラベル, 結果, NPV文字列, 色)],
    wait: [(確率ラベル, 行動, NPV文字列, 色)]、各2本"""
    H = 640
    cv = Canvas(W, H)
    cv.title(W / 2, 40, title, size=15, ha="center")
    bw, gap = 300, 50

    def group(y0, head, rows, sty):
        h = textbox(cv, 40, y0 + 40, bw, head[1], 10.6, title=head[0], title_size=12, style=sty)
        cy = y0 + 40 + h / 2
        ys = []
        for i, (pl, what, val, s) in enumerate(rows):
            y = y0 + i * 125
            x1 = 40 + bw + 220
            hh = textbox(cv, x1, y, 520, [what], 10.4, style=s, min_h=64)
            textbox(cv, x1 + 540, y, 400, [val], 10.4, style=s, min_h=64)
            cv.arrow((40 + bw + 6, cy), (x1 - 6, y + hh / 2), color=GREY, lw=2.0, head=12)
            my = (cy + y + hh / 2) / 2
            cv.text(40 + bw + 60, my - 34 if i == 0 else my + 16, pl, size=10.5, color=NAVY, weight="bold")
        return h

    group(80, root, branches, "amber")
    group(350, wait[0], wait[1], "blue")
    if note:
        textbox(cv, 40, 590 - 30, W - 80, [note], 10.0, style="grey")
    cv.save(path)
