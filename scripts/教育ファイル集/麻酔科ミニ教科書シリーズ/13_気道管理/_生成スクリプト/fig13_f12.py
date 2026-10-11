# -*- coding: utf-8 -*-
"""第13巻 f12 見える線と通す線"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Ellipse, Circle
from figlib import Canvas, LH, INK

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1520, 740
cv = Canvas(W, H)
ax = cv.ax
BLUE, RED, GREEN, AMBER = "#2e6da4", "#c0392b", "#1f6b47", "#d98e2b"

cv.title(W / 2, 44, "「見える線」と「チューブを通す線」は別物である",
         size=12.5, ha="center")

PW, PTOP, PH = 690, 86, 366
PANELS = [
    (56, "直接喉頭鏡", BLUE, "dl",
     ["術者の目から声門まで一直線に見通せて初めて挿管できる",
      "見えた＝同じ線でチューブも入る"]),
    (774, "ビデオ喉頭鏡（強湾曲）", RED, "vl",
     ["先端のカメラが曲がった先を映すので、見通しは要らない",
      "見えていても、チューブの通り道は別に作らねばならない"]),
]

for px, title, col, mode, caption in PANELS:
    cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
    cv.text(px + PW / 2, PTOP + 34, title, size=11.5, color=col, weight="bold")

    tt = np.linspace(0, 1, 400)
    chx = px + 108 + 448 * tt
    chy = PTOP + 128 + 176 * tt ** 2.3
    ax.fill_between(chx, chy - 44, chy + 44, color="#f7e4da", zorder=2)
    ax.plot(chx, chy - 44, color="#c08d72", lw=2.6, zorder=3)
    ax.plot(chx, chy + 44, color="#c08d72", lw=2.6, zorder=3)
    gl = (chx[-1] + 18, chy[-1])
    ax.add_patch(Ellipse(gl, 40, 64, facecolor="#8f4a4a", edgecolor="#5d2f2f",
                         lw=1.6, zorder=6))
    cv.text(gl[0] + 32, gl[1], "声門", size=9.4, color="#8f4a4a", ha="left", z=7)

    if mode == "dl":
        eye = (px + 76, PTOP + 116)
        ax.add_patch(Circle(eye, 15, facecolor=BLUE, edgecolor="none", zorder=7))
        cv.text(eye[0], eye[1] - 30, "術者の目", size=9.2, color=BLUE, z=7)
        ax.plot([eye[0], gl[0]], [eye[1], gl[1]], color=BLUE, lw=3.0, zorder=7)
        lx, ly = px + 300, PTOP + PH - 44
        cv.text(lx, ly, "見える線 ＝ 通す線", size=10.5, color=BLUE,
                weight="bold", z=8)
        ax.plot([lx, px + 340], [ly - 18, PTOP + 246], color=BLUE, lw=1.2,
                ls=":", zorder=8)
    else:
        cam = (chx[300], chy[300])
        ax.add_patch(Circle(cam, 13, facecolor=GREEN, edgecolor="none", zorder=8))
        ax.plot([cam[0], gl[0]], [cam[1], gl[1]], color=GREEN, lw=3.0,
                ls=(0, (4, 3)), zorder=8)
        ax.plot(chx, chy, color=AMBER, lw=3.4, zorder=7)
        cv.text(px + 430, PTOP + 92, "見える線（先端カメラ）", size=10.5,
                color=GREEN, weight="bold", z=9)
        ax.plot([px + 470, cam[0]], [PTOP + 106, cam[1] - 14], color=GREEN,
                lw=1.2, ls=":", zorder=9)
        lx, ly = px + 250, PTOP + PH - 44
        cv.text(lx, ly, "通す線（チューブ）", size=10.5, color="#b8760f",
                weight="bold", z=9)
        ax.plot([lx, px + 300], [ly - 18, PTOP + 208], color=AMBER, lw=1.2,
                ls=":", zorder=9)

    for i, ln in enumerate(caption):
        cv.text(px + PW / 2, PTOP + PH + 34 + LH(10, 1.42) * i, ln,
                size=min(cv.fit_size([ln], PW - 30, 10), 10), color=INK)

NOTE = ("※ 画面いっぱいに声門が映っていてもチューブが進まないのは、"
        "術者の腕でも器具の不良でもなく、この2本の線の食い違いによる。"
        "専用スタイレットで形を作り、必要なら角度の浅いブレードに替えて見え方を犠牲にする。")
for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
    cv.text(W / 2, H - 76 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
cv.save(os.path.join(OUT, "f12_laryngoscope.png"))
print("ok f12")
