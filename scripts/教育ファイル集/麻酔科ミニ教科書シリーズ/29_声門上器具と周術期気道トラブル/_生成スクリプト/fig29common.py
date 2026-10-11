# -*- coding: utf-8 -*-
"""㉘ 図版の共通部品"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)

plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False

W = 1520
TEAL = "#0f6d78"

FC = {
    RED: "#fceeec",
    BLUE: "#eaf1f8",
    GREEN: "#eaf5ee",
    ORANGE: "#fdf3e3",
    PURPLE: "#f1ecf8",
    NAVY: "#e8edf5",
    TEAL: "#e4f2f4",
    GREY: "#f2f4f6",
}


def cap(cv, y, s, color=NAVY, size=12.5, w=None):
    w = w or (W - 90)
    sz = cv.fit_size([s], w, size, weight="bold")
    cv.title(W / 2, y, s, size=sz, ha="center", color=color)


def msg(cv, y, s, fc="#e4f2f4", ec=TEAL, tc=TEAL, size=13.0, x=44, w=None):
    w = w or (W - 88)
    sz = cv.fit_size([s], w - 56, size, weight="bold")
    h = 30 + LH(sz, 1.5)
    cv.box(x, y, w, h, fc=fc, ec=ec, lw=2.0, radius=8)
    cv.text(x + w / 2, y + h / 2, s, size=sz, color=tc, weight="bold")
    return h


def fitlines(cv, lines, w, size, weight="normal", floor=8.6):
    s = cv.fit_size(lines, w, size, min_size=floor, weight=weight)
    if all(cv.width(l, s, weight) <= w for l in lines):
        return s, list(lines)
    out = []
    for l in lines:
        out.extend(cv.wrap(l, w, s, weight))
    return s, out


def card(cv, x, y, w, head, lines, color, fc=None, head_h=54, body_h=None,
         head_size=12.0, body_size=10.4, lh=1.65):
    fc = fc or FC.get(color, "#f2f4f6")
    hs, hl = fitlines(cv, [head], w - 32, head_size, weight="bold", floor=8.8)
    head_h = max(head_h, 20 + LH(hs, 1.45) * len(hl))
    cv.box(x, y, w, head_h, fc=color, ec=color, lw=0, radius=8)
    cv.block(x, y + (head_h - LH(hs, 1.45) * len(hl)) / 2, w, hl, hs,
             color="white", weight="bold")
    s, bl = fitlines(cv, lines, w - 36, body_size)
    bh = body_h or (28 + LH(s, lh) * len(bl))
    cv.box(x, y + head_h + 9, w, bh, fc=fc, ec=color, lw=1.7, radius=8)
    for j, ln in enumerate(bl):
        cv.text(x + w / 2, y + head_h + 9 + 14 + LH(s, lh) * (j + 0.5), ln,
                size=s, color=INK)
    return head_h + 9 + bh


def band(cv, x, y, w, h, label, lines, color, fc=None, label_w=260,
         label_size=11.5, body_size=10.4):
    """左に見出し帯、右に本文の横長ブロック"""
    fc = fc or FC.get(color, "#f2f4f6")
    cv.box(x, y, w, h, fc=fc, ec=color, lw=1.7, radius=8)
    cv.rect(x + 6, y + 6, label_w, h - 12, fc=color, ec="none")
    ls, ll = fitlines(cv, [label], label_w - 26, label_size, weight="bold",
                      floor=9.0)
    cv.block(x + 6, y + (h - LH(ls, 1.4) * len(ll)) / 2, label_w, ll, ls,
             color="white", weight="bold")
    inner = w - label_w - 40
    s, bl = fitlines(cv, lines, inner, body_size)
    cv.block(x + label_w + 22, y + (h - LH(s, 1.65) * len(bl)) / 2, inner,
             bl, s, ha="left")
    return h


def stat(cv, x, y, w, h, value, label, color=NAVY, fc=None, vs=25.0, ls=10.6):
    fc = fc or FC.get(color, "#f2f4f6")
    cv.box(x, y, w, h, fc=fc, ec=color, lw=1.8, radius=8)
    v = cv.fit_size([value], w - 36, vs, weight="bold")
    l, ll = fitlines(cv, [label], w - 36, ls, floor=8.0)
    lh = LH(l, 1.45)
    block_h = lh * len(ll)
    cv.text(x + w / 2, y + (h - block_h) / 2 - 4, value, size=v, color=color,
            weight="bold")
    cv.block(x + 18, y + h - 14 - block_h, w - 36, ll, l, color=GREY)
    return h


def tick_axis(cv, x0, x1, y, labels, color=GREY, size=10.0):
    """横軸を引いて、(比率, ラベル) の目盛を打つ"""
    cv.arrow((x0, y), (x1 + 26, y), color=color, lw=2.0, head=11)
    for frac, lab in labels:
        px = x0 + (x1 - x0) * frac
        cv.ax.plot([px, px], [y - 9, y + 9], color=color, lw=2.0, zorder=4)
        cv.text(px, y + 30, lab, size=size, color=color)


def outpath(default="fig"):
    out = sys.argv[1] if len(sys.argv) > 1 else default
    os.makedirs(out, exist_ok=True)
    return out


def save(cv, path, pad=30):
    """余白を実測して切り詰めて保存する。高さを事前に計算しなくてよくなる。"""
    from PIL import Image, ImageChops
    cv.save(path)
    im = Image.open(path).convert('RGB')
    bg = Image.new('RGB', im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, bg).getbbox()
    if not bbox:
        return
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad); y1 = min(im.height, y1 + pad)
    im.crop((x0, y0, x1, y1)).save(path)
