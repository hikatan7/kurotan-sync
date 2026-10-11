# -*- coding: utf-8 -*-
"""㊸ 図版共通の道具。

figlib の Canvas（ピクセル座標・y は下向き）の上に、
波形パネルと凡例を描くための薄い層を足す。
"""
import os
import figlib
from figlib import (Canvas, LH, NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE,
                    PURPLE, textbox)

W = 1800                     # 図版の標準幅（px）
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "図版")

# 波形の色（全図で統一する）
C_PRES = "#2e6da4"           # 圧
C_FLOW = "#2e7d52"           # 流量
C_VOL = "#6b4fa0"            # 量
C_NOTE = "#c0392b"           # 注記


def ensure_dir():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)


def path(name):
    ensure_dir()
    return os.path.join(OUT, name)


def head(cv, title, sub=None):
    """図の左上に見出しを置き、本文を始める y を返す。"""
    cv.title(56, 52, title, size=20)
    y = 96
    if sub:
        for ln in cv.wrap(sub, cv.w - 120, 13):
            cv.text(56, y + 16, ln, size=13, color=GREY, ha="left")
            y += LH(13, 1.35)
        y += 8
    return y + 46


class Panel(object):
    """波形を描くパネル。t は 0..1、v は 0（下端）..1（上端）で渡す。"""

    def __init__(self, cv, x, y, w, h, label, color=INK, base=0.0,
                 label_size=13):
        self.cv, self.x, self.y, self.w, self.h = cv, x, y, w, h
        self.color = color
        self.base = base
        cv.rect(x, y, w, h, fc="#fbfcfd", ec="#c9d2dc", lw=1.2)
        # ラベルは枠の外（上）に置く。枠の中に置くと注記と重なる。
        cv.text(x, y - 12, label, size=label_size, color=color,
                weight="bold", ha="left", va="bottom")
        # 基線
        by = self.py(base)
        cv.ax.plot([x, x + w], [by, by], color="#c9d2dc", lw=1.2,
                   linestyle=(0, (5, 4)), zorder=2)

    def px(self, t):
        return self.x + self.w * t

    def py(self, v):
        return self.y + self.h - self.h * v

    def plot(self, pts, color=None, lw=2.6, z=4, ls="-"):
        xs = [self.px(t) for t, _ in pts]
        ys = [self.py(v) for _, v in pts]
        self.cv.ax.plot(xs, ys, color=color or self.color, lw=lw, zorder=z,
                        linestyle=ls, solid_joinstyle="round")

    def vline(self, t, color=GREY, lw=1.2, ls=(0, (4, 4))):
        self.cv.ax.plot([self.px(t), self.px(t)], [self.y + 4, self.y + self.h - 4],
                        color=color, lw=lw, linestyle=ls, zorder=3)

    def hline(self, v, color=GREY, lw=1.2, ls=(0, (4, 4)), t0=0.0, t1=1.0):
        self.cv.ax.plot([self.px(t0), self.px(t1)], [self.py(v), self.py(v)],
                        color=color, lw=lw, linestyle=ls, zorder=3)

    def note(self, t, v, s, color=C_NOTE, size=12, ha="center", va="center"):
        self.cv.text(self.px(t), self.py(v), s, size=size, color=color,
                     ha=ha, va=va, weight="bold")

    def caption(self, s, color=None, size=12.5, ha="right"):
        """パネルの見出し行（枠の外・上）の右端に注記を置く。"""
        x = self.x + self.w if ha == "right" else self.x
        self.cv.text(x, self.y - 12, s, size=size, color=color or GREY,
                     ha=ha, va="bottom", weight="bold")

    def toplabel(self, t, s, color=None, size=12.5, ha="center"):
        """枠の外・上の任意の位置に注記を置く（縦線の頭など）。"""
        self.cv.text(self.px(t), self.y - 12, s, size=size,
                     color=color or GREY, ha=ha, va="bottom", weight="bold")

    def label_left(self, v, s, size=11.5, color=GREY):
        self.cv.text(self.x - 12, self.py(v), s, size=size, color=color,
                     ha="right", va="center")


def legend(cv, x, y, items, size=12, gap=26):
    """items: [(色, 文字列), ...] を横一列に置く。返り値は消費した高さ。"""
    cx = x
    for color, s in items:
        cv.ax.plot([cx, cx + 34], [y, y], color=color, lw=3.2, zorder=5)
        cv.text(cx + 44, y, s, size=size, color=INK, ha="left", va="center")
        cx += 44 + cv.width(s, size) + gap
    return LH(size, 1.6)


def steps(n, hi=0.78, lo=0.06, duty=0.35, rise=0.02):
    """矩形に近い圧波形を n 周期ぶん返す（t は 0..1）。"""
    pts = []
    for i in range(n):
        t0 = i / float(n)
        t1 = t0 + duty / n
        t2 = (i + 1) / float(n)
        pts += [(t0, lo), (t0 + rise, hi), (t1, hi), (t1 + rise, lo), (t2 - 0.001, lo)]
    return pts


def decay(t0, t1, v0, v1, n=24, k=3.2):
    """指数的に減衰する区間の点列。"""
    import math
    out = []
    for i in range(n + 1):
        f = i / float(n)
        v = v1 + (v0 - v1) * math.exp(-k * f)
        out.append((t0 + (t1 - t0) * f, v))
    return out


def ramp(t0, t1, v0, v1, n=2):
    return [(t0, v0), (t1, v1)]
