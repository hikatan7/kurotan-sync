# -*- coding: utf-8 -*-
"""第13巻 f13 Cormack-Lehane と POGO"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Ellipse, Polygon, Rectangle
from figlib import Canvas, LH, NAVY, INK

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1520, 634
cv = Canvas(W, H)
ax = cv.ax
cv.title(W / 2, 44, "Cormack-Lehane 分類と POGO —— 何が見えているかを言葉にする",
         size=12, ha="center")

GRADES = [
    ("Grade 1", "声門が全部見える", 0.02, "POGO 100%"),
    ("Grade 2", "声門の後方だけ見える", 0.58, "POGO 20〜50%"),
    ("Grade 3", "喉頭蓋しか見えない", 1.05, "POGO 0%"),
    ("Grade 4", "喉頭蓋も見えない", 1.75, "POGO 0%"),
]
PW, PTOP, PH = 340, 86, 274
RW, RH_ = 190, 176

for i, (name, desc, occ, pogo) in enumerate(GRADES):
    px = 42 + i * (PW + 22)
    cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    cx, cy = px + PW / 2, PTOP + 166
    cv.text(cx, PTOP + 38, name, size=12, color=NAVY, weight="bold", z=9)

    ax.add_patch(Ellipse((cx, cy), RW, RH_, facecolor="#f3d9cd",
                         edgecolor="none", zorder=2))
    clip = Ellipse((cx, cy), RW, RH_, transform=ax.transData)

    # 声門（前方が上）
    glo = Polygon([[cx, cy - 60], [cx - 28, cy + 54], [cx + 28, cy + 54]],
                  closed=True, facecolor="#33383f", edgecolor="none", zorder=4)
    ax.add_patch(glo)
    glo.set_clip_path(clip)
    for sgn in (-1, 1):
        band = Polygon([[cx + sgn * 3, cy - 60],
                        [cx + sgn * 31, cy + 54],
                        [cx + sgn * 52, cy + 54],
                        [cx + sgn * 11, cy - 60]], closed=True,
                       facecolor="#f4ece8", edgecolor="#cbb7ad", lw=1.2,
                       zorder=5)
        ax.add_patch(band)
        band.set_clip_path(clip)

    # 喉頭蓋（上から降りてきて覆う）
    low = cy - 96 + occ * 175
    body = Rectangle((cx - RW / 2 - 6, cy - RH_ / 2 - 6), RW + 12,
                     (low - (cy - RH_ / 2 - 6)), facecolor="#f2c4ae",
                     edgecolor="none", zorder=6)
    ax.add_patch(body)
    body.set_clip_path(clip)
    lip = Ellipse((cx, low), RW + 12, 58, facecolor="#f2c4ae",
                  edgecolor="#c08d72", lw=1.8, zorder=7)
    ax.add_patch(lip)
    lip.set_clip_path(clip)

    ax.add_patch(Ellipse((cx, cy), RW, RH_, facecolor="none",
                         edgecolor="#b98f78", lw=2.4, zorder=9))
    cv.text(cx, PTOP + PH + 28, desc, size=9.8, color=INK)
    cv.text(cx, PTOP + PH + 28 + LH(9.8, 1.5), pogo, size=9.8,
            color="#2e6da4", weight="bold")

NOTE = ("※ Cormack-Lehane は直接喉頭鏡の視野の分類である。ビデオ喉頭鏡の画面所見に"
        "同じ Grade を当てると難易度を過小評価するため、記録には器具名を併記する。")
for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
    cv.text(W / 2, H - 86 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
cv.save(os.path.join(OUT, "f13_cl_pogo.png"))
print("ok f13")
