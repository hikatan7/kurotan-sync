# -*- coding: utf-8 -*-
"""第13巻 f02 上気道閉塞の3か所"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import Canvas, LH, INK

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1520, 606
cv = Canvas(W, H)
FLESH, FLESH_E = "#f0d3c4", "#c08d72"
OPEN_C, SHUT_C = "#cfe6ea", "#f4bdb7"

cv.title(W / 2, 44, "意識消失で上気道が閉じる —— 詰まる場所は3つある",
         size=12.5, ha="center")

PW, PH, PTOP = 452, 300, 90
PANELS = [
    (56, "覚醒時", "#1f6b47", (0.10, 0.12, 0.08), OPEN_C,
     ["咽頭拡張筋が持続的に働き", "咽頭腔（virtual space）が開いている"]),
    (534, "意識消失", "#b8760f", (0.92, 1.02, 0.72), SHUT_C,
     ["筋緊張が落ち、軟口蓋・舌根・", "喉頭蓋が後方へ倒れて塞ぐ"]),
    (1012, "用手気道確保", "#2e6da4", (0.24, 0.22, 0.14), OPEN_C,
     ["頭部後屈＋下顎挙上で", "3か所を同時に前へ引き出す"]),
]

X0, X1 = 72, PW - 72
TOPW, BOTW = 118, 246          # 気道の上下壁（パネル内 y）
BAND = 44                      # 粘膜・軟部組織の厚み
SPAN = BOTW - TOPW


def bump(x, c, w, d):
    return d * np.exp(-((x - c) ** 2) / (2 * (w / 2.2) ** 2))


for px, title, col, (d_soft, d_tongue, d_epi), lum, caption in PANELS:
    cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
    cv.text(px + PW / 2, PTOP + 32, title, size=11.5, color=col, weight="bold")
    ax = cv.ax
    x = np.linspace(X0, X1, 700)
    top = TOPW + bump(x, X0 + 96, 86, d_soft * SPAN * 0.50) \
        + bump(x, X0 + 250, 66, d_epi * SPAN * 0.46)
    bot = BOTW - bump(x, X0 + 172, 118, d_tongue * SPAN * 0.52)
    bot = np.maximum(bot, top + 4)
    ax.fill_between(px + x, PTOP + top, PTOP + bot, color=lum, zorder=2)
    ax.fill_between(px + x, PTOP + TOPW - BAND, PTOP + top,
                    color=FLESH, zorder=3)
    ax.fill_between(px + x, PTOP + bot, PTOP + BOTW + BAND,
                    color=FLESH, zorder=3)
    ax.plot(px + x, PTOP + top, color=FLESH_E, lw=1.8, zorder=4)
    ax.plot(px + x, PTOP + bot, color=FLESH_E, lw=1.8, zorder=4)
    for yy in (TOPW - BAND, BOTW + BAND):
        ax.plot([px + X0, px + X1], [PTOP + yy] * 2, color="#b9c2cc",
                lw=2.2, zorder=5)
    cv.arrow((px + X0 - 26, PTOP + (TOPW + BOTW) / 2),
             (px + X0 - 4, PTOP + (TOPW + BOTW) / 2),
             color="#9aa4b0", lw=1.8, head=8)
    for i, ln in enumerate(caption):
        cv.text(px + PW / 2, PTOP + PH + 32 + LH(10, 1.42) * i, ln,
                size=10, color=INK)

px = PANELS[0][0]
for lx, ly, txt in ((X0 + 96, TOPW - BAND / 2 - 2, "① 軟口蓋"),
                    (X0 + 250, TOPW - BAND / 2 - 2, "③ 喉頭蓋"),
                    (X0 + 172, BOTW + BAND / 2 + 2, "② 舌　根")):
    cv.text(px + lx, PTOP + ly, txt, size=9.4, color="#8a4f28", weight="bold")

NOTE = ("※ 「舌が落ちる」だけではない。軟口蓋・舌根・喉頭蓋のどれが主因かで、"
        "エアウェイの選択も、下顎挙上の効き方も変わる。")
cv.text(W / 2, H - 40, NOTE, size=cv.fit_size([NOTE], W - 140, 9.8),
        color="#5d6875")
cv.save(os.path.join(OUT, "f02_upper_airway.png"))
print("ok f02")
