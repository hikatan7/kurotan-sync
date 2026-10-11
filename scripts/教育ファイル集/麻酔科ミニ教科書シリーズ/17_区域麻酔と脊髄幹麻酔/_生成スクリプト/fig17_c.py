# -*- coding: utf-8 -*-
"""第17巻 図版 f19（デルマトームと必要な麻酔高位）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figlib import Canvas, LH, NAVY, INK, JP
from figkit import note, banner

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP


def P(n):
    return os.path.join(OUT, n)


def f19():
    W, H = 1520, 880
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "どの高さまで効かせるか —— 目印になるデルマトーム",
             size=12.5, ha="center")
    ROWS = [
        ("C8・T1", "#7b52a8", "小指", "上肢の手術"),
        ("T4", "#c0392b", "乳頭", "上腹部の手術。これ以上は循環変動が大きい"),
        ("T6", "#d2762b", "剣状突起", "上腹部の手術"),
        ("T10", "#b8760f", "臍", "経尿道的手術、下肢の手術、帝王切開の下限"),
        ("T12", "#2e6da4", "鼠径部", "―"),
        ("L1", "#1f6b47", "鼠径靱帯", "―"),
        ("S2〜S5", "#5d6875", "会陰部", "肛門・会陰の手術（サドルブロック）"),
    ]
    L, R = 56, W - 56
    LEV_SZ = 11.2
    LEVW = max(cv.measure(r[0], LEV_SZ, weight="bold")[0] for r in ROWS) + 46
    MARK_SZ = 11.0
    MARKW = max(cv.measure(r[2], MARK_SZ, weight="bold")[0] for r in ROWS) + 44
    TOP, GAP = 96, 14
    bsz = min(cv.fit_size([r[3] for r in ROWS],
                          R - L - LEVW - MARKW - 90, 10.0), 10.0)
    RH = 30 + LH(bsz, 1.0) * 0.5 + 26
    for i, (lev, col, mark, use) in enumerate(ROWS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L, y, LEVW, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(L + LEVW / 2, y + RH / 2, lev, size=LEV_SZ, color="white",
                weight="bold")
        cv.box(L + LEVW + 20, y + (RH - 46) / 2, MARKW, 46, fc="#f2f5f8",
               ec=col, lw=1.4, radius=6)
        cv.text(L + LEVW + 20 + MARKW / 2, y + RH / 2, mark, size=MARK_SZ,
                color=col, weight="bold")
        if use != "―":
            cv.text(L + LEVW + MARKW + 46, y + RH / 2, use, size=bsz,
                    color=INK, ha="left")
    y = banner(cv, W, TOP + 7 * (RH + GAP) + 10,
               "T4 を超えると心臓交感神経（T1〜T4）まで遮断され、"
               "徐脈と血圧低下が強く出る")
    note(cv, W, y + 30,
         "※ デルマトームには個体差と重なりがあり、境界は明瞭ではない。"
         "麻酔域の確認は、冷覚・痛覚・触覚のどれで見たかを記録に添える"
         "（この三つは止まる高さが違う）。")
    cv.save(P("f19_dermatome.png"))


if __name__ == "__main__":
    f19()
    print("ok f19")
