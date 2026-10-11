# -*- coding: utf-8 -*-
"""第14巻 f02 上肢の短軸超音波解剖（模式）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Circle, Rectangle
from figlib import Canvas, LH, NAVY, INK

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1520, 620
cv = Canvas(W, H)
ax = cv.ax
ART, VEIN, NERVE = "#c0392b", "#2e6da4", "#c8a415"
TENDON, BONE, SKIN = "#cfd6de", "#e6dfd3", "#f3ddd0"

cv.title(W / 2, 44, "上肢の短軸像 —— 針を進める前に「隣に何があるか」を見る",
         size=12.5, ha="center")

PANELS = [
    ("上腕",
     [("上腕動脈", ART, (10, -6), 28), ("正中神経", NERVE, (62, 12), 19),
      ("尺側皮静脈", VEIN, (-62, 20), 31)],
     "動脈のすぐ内側に正中神経が並走する"),
    ("前腕近位",
     [("橈骨動脈", ART, (6, 2), 23), ("橈骨神経浅枝", NERVE, (52, -8), 15),
      ("橈側皮静脈", VEIN, (-60, 22), 26)],
     "橈骨神経の浅枝が伴走する"),
    ("手関節（橈側）",
     [("橈骨動脈", ART, (-16, 0), 23), ("橈側手根屈筋腱", TENDON, (42, 6), 24),
      ("橈骨", BONE, (-6, 40), 34)],
     "正中神経は手根管の中にあり、動脈から離れている"),
    ("手関節（尺側）",
     [("尺骨動脈", ART, (-16, 0), 22), ("尺骨神経", NERVE, (30, 6), 18),
      ("尺骨", BONE, (2, 40), 34)],
     "神経が動脈に接し、損傷のリスクが高い"),
]

L = 44
GAPX = 20
PW = (W - L * 2 - GAPX * 3) / 4.0
PTOP = 88
USH = 168
LEG_X = 34          # 凡例の○の中心（パネル左端からの距離）
LEG_TX = LEG_X + 16  # 凡例の文字開始位置
# 凡例の文字がパネル内に収まるサイズを実測から決める
LEG_SZ = min(cv.fit_size([n for p in PANELS for (n, _, _, _) in p[1]],
                         PW - LEG_TX - 22, 9.4), 9.4)
LEGH = LH(LEG_SZ, 1.75)
PH = 34 + USH + 22 + LEGH * 3 + 14

for i, (title, items, caption) in enumerate(PANELS):
    px = L + i * (PW + GAPX)
    cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    cv.text(px + PW / 2, PTOP + 30, title, size=11.2, color=NAVY, weight="bold")
    ux, uy, uw = px + 28, PTOP + 50, PW - 56
    ax.add_patch(Rectangle((ux, uy), uw, USH, facecolor="#2b2f36",
                           edgecolor="none", zorder=2))
    ax.add_patch(Rectangle((ux, uy), uw, 22, facecolor=SKIN,
                           edgecolor="none", zorder=3))
    cx, cy = px + PW / 2, uy + 92
    for name, col, (dx, dy), rr in items:
        ax.add_patch(Circle((cx + dx, cy + dy), rr, facecolor=col,
                            edgecolor="white", lw=1.6, zorder=5))
    ly = uy + USH + 26
    for j, (name, col, _, _) in enumerate(items):
        yy = ly + LEGH * j
        ax.add_patch(Circle((px + LEG_X, yy), 7, facecolor=col,
                            edgecolor="#9aa4b0", lw=1.0, zorder=5))
        cv.text(px + LEG_TX, yy, name, size=LEG_SZ, color=INK, ha="left")
    for j, ln in enumerate(cv.wrap(caption, PW - 16, 9.4)):
        cv.text(px + PW / 2, PTOP + PH + 30 + LH(9.4, 1.4) * j, ln,
                size=9.4, color=INK)

NOTE = ("※ 模式図であり、位置関係の個体差は大きい。触れる一点だけで決めず、"
        "走査して最も条件のよい区間を選ぶ。")
for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
    cv.text(W / 2, PTOP + PH + 118 + LH(9.8, 1.45) * i, ln, size=9.8,
            color="#5d6875")
cv.save(os.path.join(OUT, "f02_us_anatomy.png"))
print("ok f02")
