# -*- coding: utf-8 -*-
"""第13巻 f17 輪状甲状膜の同定"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matplotlib.patches import Rectangle, Polygon
from figlib import Canvas, LH, NAVY, INK

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
W, H = 1520, 674
cv = Canvas(W, H)
ax = cv.ax
cv.title(W / 2, 44, "輪状甲状膜をどう見つけるか —— 触れないなら超音波で線を引く",
         size=12, ha="center")

LX, LY, LW, LHT = 56, 84, 600, 476
cv.box(LX, LY, LW, LHT, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
cv.text(LX + LW / 2, LY + 34, "前頸部の正中構造", size=11.4, color=NAVY,
        weight="bold")

cxx = LX + 300
y0 = LY + 78
HALF = 58


def lab(y, text, col, bold=False):
    cv.text(cxx - HALF - 26, y, text, size=9.6, color=col, ha="right",
            weight="bold" if bold else "normal", z=6)
    ax.plot([cxx - HALF - 20, cxx - HALF - 4], [y, y], color=col, lw=1.2,
            ls=":", zorder=6)


ax.add_patch(Polygon([[cxx - HALF, y0 + 80], [cxx - HALF, y0 + 20],
                      [cxx, y0], [cxx + HALF, y0 + 20], [cxx + HALF, y0 + 80]],
                     closed=True, facecolor="#e6d4c8", edgecolor="#b98f78",
                     lw=1.8, zorder=3))
lab(y0 + 50, "甲状軟骨", "#8a5a3c")
ax.add_patch(Rectangle((cxx - HALF, y0 + 84), HALF * 2, 34,
                       facecolor="#fbe3d6", edgecolor="#c0392b", lw=2.4,
                       zorder=3))
lab(y0 + 101, "輪状甲状膜", "#c0392b", bold=True)
ax.add_patch(Rectangle((cxx - HALF, y0 + 122), HALF * 2, 46,
                       facecolor="#e6d4c8", edgecolor="#b98f78", lw=1.8,
                       zorder=3))
lab(y0 + 145, "輪状軟骨", "#8a5a3c")
for k in range(4):
    ax.add_patch(Rectangle((cxx - 44, y0 + 178 + k * 32), 88, 24,
                           facecolor="#eef1f5", edgecolor="#9aa4b0", lw=1.4,
                           zorder=3))
lab(y0 + 240, "気管軟骨", "#6b7785")

ax.annotate("", xy=(cxx + HALF + 26, y0 + 84),
            xytext=(cxx + HALF + 26, y0 + 118),
            arrowprops=dict(arrowstyle="<|-|>", color="#c0392b", lw=1.7))
cv.text(cxx + HALF + 38, y0 + 101, "約 9 mm", size=9.6, color="#c0392b",
        ha="left", z=6)
_cap = "成人では高さ 約 9 mm・幅 約 30 mm。切開は横向きに置く"
cv.text(LX + LW / 2, LY + LHT - 34, _cap,
        size=min(cv.fit_size([_cap], LW - 50, 9.6), 9.6), color="#5d6875")

RX = LX + LW + 30
RW_ = W - 56 - RX
ITEMS = [
    ("① 触知（laryngeal handshake）", "#1f6b47",
     ["母指と中指で甲状軟骨の両側を挟んで喉頭を安定させ、",
      "示指を尾側へ滑らせて陥凹を探す"]),
    ("② 触れないときがある", "#b8760f",
     ["高度肥満・浮腫・血腫・頸部手術後・放射線後では、",
      "触知だけで正しい高さを当てられる確率は大きく落ちる"]),
    ("③ 超音波で線を引く", "#2e6da4",
     ["高周波リニアプローブで正中を縦走査し、",
      "気管輪と輪状軟骨を数えて位置を同定する"]),
    ("④ 印は「導入前」に付ける", "#c0392b",
     ["困難が予想される症例では、麻酔導入の前に",
      "皮膚マーキングまで済ませておく"]),
]
IY, IH, IG = LY, 110, 12
for i, (head, col, lines) in enumerate(ITEMS):
    y = IY + i * (IH + IG)
    cv.box(RX, y, RW_, IH, fc="white", ec=col, lw=1.7, radius=8)
    cv.text(RX + 24, y + 30, head, size=10.6, color=col, weight="bold",
            ha="left")
    for j, ln in enumerate(lines):
        cv.text(RX + 24, y + 58 + LH(9.4, 1.35) * j, ln,
                size=min(cv.fit_size([ln], RW_ - 48, 9.4), 9.4),
                color=INK, ha="left")

NOTE = ("※ 「だいたいこの辺」で切ると、甲状腺や大血管に入る。"
        "触知が確実でないなら、事前に超音波で線を引いておくことが最大の準備になる。")
for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
    cv.text(W / 2, H - 86 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
cv.save(os.path.join(OUT, "f17_cricothyroid.png"))
print("ok f17")
