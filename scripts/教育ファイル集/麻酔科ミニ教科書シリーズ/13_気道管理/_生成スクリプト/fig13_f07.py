# -*- coding: utf-8 -*-
"""第13巻 f07 Mallampati 分類"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Ellipse, Polygon, Rectangle
from figlib import Canvas, LH, NAVY, INK

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1520, 664
cv = Canvas(W, H)
ax = cv.ax
cv.title(W / 2, 44, "Mallampati 分類 —— 座位・最大開口・舌を最大に出させ、発声はさせない",
         size=12, ha="center")

CLASSES = [
    ("Class I", ["軟口蓋・口蓋垂・口蓋弓が", "すべて見える"], 0.02),
    ("Class II", ["軟口蓋と口蓋垂は見えるが", "口蓋弓は隠れる"], 0.34),
    ("Class III", ["軟口蓋と口蓋垂の基部のみ", "見える"], 0.66),
    ("Class IV", ["軟口蓋が見えない", ""], 0.94),
]
PW, PTOP, PH = 340, 90, 300
MW, MH = 196, 250

for i, (name, desc, occ) in enumerate(CLASSES):
    px = 42 + i * (PW + 22)
    cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    cx, cy = px + PW / 2, PTOP + 178
    cv.text(cx, PTOP + 40, name, size=12, color=NAVY, weight="bold", z=9)

    mouth = Ellipse((cx, cy), MW, MH, facecolor="#f7e4da",
                    edgecolor="none", zorder=2)
    ax.add_patch(mouth)
    clip = Ellipse((cx, cy), MW, MH, transform=ax.transData)

    pharynx = Ellipse((cx, cy + 6), MW - 42, MH - 44, facecolor="#8f4a4a",
                      edgecolor="none", zorder=3)
    ax.add_patch(pharynx)
    pharynx.set_clip_path(clip)
    for sgn in (-1, 1):
        pil = Ellipse((cx + sgn * 52, cy + 2), 26, MH - 62,
                      facecolor="#e8b6a6", edgecolor="none", zorder=4)
        ax.add_patch(pil)
        pil.set_clip_path(clip)
    palate = Ellipse((cx, cy - 84), MW - 56, 58, facecolor="#f0c7b6",
                     edgecolor="none", zorder=5)
    ax.add_patch(palate)
    palate.set_clip_path(clip)
    uvula = Polygon([[cx - 12, cy - 72], [cx + 12, cy - 72], [cx, cy - 4]],
                    closed=True, facecolor="#dc9a89", edgecolor="none",
                    zorder=6)
    ax.add_patch(uvula)
    uvula.set_clip_path(clip)

    top_of_tongue = cy + MH / 2 - occ * MH
    tongue = Rectangle((cx - MW / 2 - 4, top_of_tongue), MW + 8,
                       MH, facecolor="#f2c4ae", edgecolor="none", zorder=7)
    ax.add_patch(tongue)
    tongue.set_clip_path(clip)
    if occ > 0.05:
        edge = Ellipse((cx, top_of_tongue + 22), MW - 6, 44,
                       facecolor="#f2c4ae", edgecolor="#c08d72", lw=1.6,
                       zorder=8)
        ax.add_patch(edge)
        edge.set_clip_path(clip)

    ax.add_patch(Ellipse((cx, cy), MW, MH, facecolor="none",
                         edgecolor="#b98f78", lw=2.4, zorder=9))
    for j, ln in enumerate(desc):
        if ln:
            cv.text(cx, PTOP + PH + 30 + LH(9.8, 1.42) * j, ln, size=9.8,
                    color=INK)

NOTE = ("※ 発声させると軟口蓋が挙上して見かけ上よく見え、過小評価になる。"
        "臥位での評価も同じ理由で信頼できない。単独では感度が低く、"
        "他の所見と組み合わせて初めて意味を持つ。")
for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
    cv.text(W / 2, H - 66 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
cv.save(os.path.join(OUT, "f07_mallampati.png"))
print("ok f07")
