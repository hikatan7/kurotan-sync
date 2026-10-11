# -*- coding: utf-8 -*-
"""第13巻 f09 体位（外耳孔と胸骨切痕）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Circle, Polygon, Rectangle
from figlib import Canvas, LH, NAVY, INK

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1520, 660
cv = Canvas(W, H)
ax = cv.ax
cv.title(W / 2, 44, "体位 —— 外耳孔と胸骨切痕を水平に揃える", size=12.5,
         ha="center")

PW, PTOP, PH = 452, 88, 300
BED = 252
RED, BLUE, GREEN = "#c0392b", "#2e6da4", "#1f6b47"

PANELS = [
    (56, "平坦なベッド（不適）", RED, "flat", 34,
     ["外耳孔が胸骨切痕より低い", "軸が揃わず声門が見えにくい"]),
    (534, "スニッフィング位", BLUE, "pillow", -2,
     ["後頭部に高さ 7〜9 cm の枕", "下位頸椎を屈曲、上位頸椎を伸展"]),
    (1012, "ランプ位（肥満）", GREEN, "ramp", -2,
     ["上半身ごと挙上して外耳孔を持ち上げる", "頭だけを高くしてはいけない"]),
]

for px, title, col, kind, ear_dy, caption in PANELS:
    cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
    cv.text(px + PW / 2, PTOP + 34, title, size=11.2, color=col, weight="bold")
    ax.plot([px + 34, px + PW - 34], [PTOP + BED] * 2, color="#b9c2cc",
            lw=5, zorder=2, solid_capstyle="butt")

    if kind == "ramp":
        torso_top_head, torso_top_foot = 128, 196
        body = Polygon([[px + 44, PTOP + BED], [px + 290, PTOP + BED],
                        [px + 290, PTOP + torso_top_head],
                        [px + 44, PTOP + torso_top_foot]],
                       closed=True, facecolor="#dfe6ee", edgecolor="#9aa4b0",
                       lw=1.8, zorder=3)
        ax.add_patch(body)
        wedge = Polygon([[px + 60, PTOP + BED], [px + 290, PTOP + BED],
                         [px + 290, PTOP + BED - 52]],
                        closed=True, facecolor="#eef1f5",
                        edgecolor="#b9c2cc", lw=1.4, zorder=2)
        ax.add_patch(wedge)
        notch_y = torso_top_head
    else:
        torso_top = 184
        ax.add_patch(Rectangle((px + 44, PTOP + torso_top), 246,
                               BED - torso_top, facecolor="#dfe6ee",
                               edgecolor="#9aa4b0", lw=1.8, zorder=3))
        notch_y = torso_top
        if kind == "pillow":
            ax.add_patch(Rectangle((px + 296, PTOP + 146), 96, 38,
                                   facecolor="#cfe0ef", edgecolor="#5b7fa6",
                                   lw=1.6, zorder=3))
            cv.text(px + 344, PTOP + 165, "枕", size=9.2, color="#2e6da4", z=6)

    notch = (px + 290, PTOP + notch_y)
    ax.plot([notch[0] - 8, px + PW - 34], [notch[1]] * 2, color="#8d97a3",
            lw=1.6, ls=(0, (5, 4)), zorder=8)
    head_cy = PTOP + notch_y + ear_dy - 6
    head_cx = px + 344
    ax.add_patch(Circle((head_cx, head_cy), 44, facecolor="#f2d5c6",
                        edgecolor="#c08d72", lw=1.9, zorder=5))
    ear = (head_cx - 10, head_cy + 6)
    ax.add_patch(Circle(ear, 8, facecolor=RED, edgecolor="none", zorder=7))
    ax.add_patch(Circle(notch, 8, facecolor=BLUE, edgecolor="none", zorder=7))
    if ear_dy > 8:
        ax.plot([ear[0], ear[0]], [notch[1], ear[1]], color=RED, lw=1.6,
                ls=":", zorder=8)
        cv.arrow((px + PW - 44, notch[1] + 2), (px + PW - 44, ear[1] - 2),
                 color=RED, lw=1.8, head=9, style="<|-|>")
        cv.text(px + PW - 54, (notch[1] + ear[1]) / 2, "低い", size=9.2,
                color=RED, ha="right", z=9)
    cv.text(px + 62, PTOP + notch_y - 22, "胸骨切痕", size=9.2, color=BLUE,
            ha="left", z=8)
    cv.text(px + PW - 50, PTOP + 76, "外耳孔", size=9.2, color=RED,
            ha="right", z=8)
    for i, ln in enumerate(cv.wrap(" ".join(caption[:1]), PW - 40, 10)):
        pass
    for i, ln in enumerate(caption):
        cv.text(px + PW / 2, PTOP + PH + 32 + LH(10, 1.42) * i, ln,
                size=min(cv.fit_size([ln], PW - 24, 10), 10), color=INK)

NOTE = ("※ 「枕を外して首を反らす」のはスニッフィング位ではない。"
        "肥満で頭だけを高くすると頸部が前屈し、かえって展開できなくなる。")
for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
    cv.text(W / 2, H - 66 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
cv.save(os.path.join(OUT, "f09_position.png"))
print("ok f09")
