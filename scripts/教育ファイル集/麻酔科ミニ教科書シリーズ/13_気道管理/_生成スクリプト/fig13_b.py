# -*- coding: utf-8 -*-
"""第13巻 気道管理 図版 f07〜f11"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle, Rectangle
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f07
def f07():
    W, H = 1520, 700
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "Mallampati 分類 —— 座位・最大開口・舌を最大に出させ、発声はさせない",
             size=12, ha="center")
    CLASSES = [
        ("Class I", "軟口蓋・口蓋垂・口蓋弓が見える", 0.00),
        ("Class II", "軟口蓋と口蓋垂は見えるが口蓋弓は隠れる", 0.30),
        ("Class III", "軟口蓋と口蓋垂の基部のみ", 0.62),
        ("Class IV", "軟口蓋が見えない", 0.90),
    ]
    PW, PTOP, PH = 340, 92, 316
    for i, (name, desc, occ) in enumerate(CLASSES):
        px = 42 + i * (PW + 22)
        cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
        cx, cy = px + PW / 2, PTOP + 176
        ax.add_patch(Ellipse((cx, cy), 210, 268, facecolor="#f3d9cd",
                             edgecolor="#b98f78", lw=2.0, zorder=2))
        ax.add_patch(Ellipse((cx, cy), 168, 224, facecolor="#8f4a4a",
                             edgecolor="none", zorder=3))
        # 口蓋弓（左右の柱）
        for sgn in (-1, 1):
            ax.add_patch(Ellipse((cx + sgn * 56, cy - 6), 26, 168,
                                 facecolor="#e8b6a6", edgecolor="none",
                                 zorder=4))
        # 軟口蓋
        ax.add_patch(Ellipse((cx, cy - 92), 150, 62, facecolor="#f0c7b6",
                             edgecolor="none", zorder=5))
        # 口蓋垂
        ax.add_patch(Polygon([[cx - 13, cy - 78], [cx + 13, cy - 78],
                              [cx, cy - 6]], closed=True,
                             facecolor="#e0a191", edgecolor="none", zorder=6))
        # 舌（下からせり上がって隠す）
        rise = occ * 232
        ax.add_patch(Ellipse((cx, cy + 132 - rise + 116), 210, 300,
                             facecolor="#f2c4ae", edgecolor="#c08d72",
                             lw=1.8, zorder=7))
        ax.add_patch(Ellipse((cx, cy), 214, 272, facecolor="none",
                             edgecolor="#b98f78", lw=2.2, zorder=8))
        cv.text(cx, PTOP + 44, name, size=12, color=NAVY, weight="bold", z=9)
        for j, ln in enumerate(cv.wrap(desc, PW - 40, 9.6)):
            cv.text(cx, PTOP + PH + 30 + LH(9.6, 1.4) * j, ln, size=9.6,
                    color=INK)
    NOTE = ("※ 発声させると軟口蓋が挙上して見かけ上よく見え、過小評価になる。"
            "臥位での評価も同じ理由で信頼できない。単独では感度が低く、"
            "他の所見と組み合わせて初めて意味を持つ。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, H - 68 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f07_mallampati.png"))


# ---------------------------------------------------------------- f08
def f08():
    W, H = 1520, 672
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "評価は「点数」ではなく「3つの層のどこか」に変換する",
             size=12.5, ha="center")
    COLS = [
        ("通常導入", "#eaf4ee", "#1f6b47",
         ["所見が揃って良好", "既往の困難なし", "肥満・OSA なし"],
         ["通常の導入と喉頭展開", "ただしバックアップ器具は", "同じ室内に置く"]),
        ("準備を厚くして導入", "#fdf1e0", "#b8760f",
         ["小顎・短頸・高度肥満", "OSA 高リスク", "所見が1つ以上不良"],
         ["ビデオ喉頭鏡を第一に", "第2世代 SGA とブジーを開封", "上級者が入室してから導入"]),
        ("覚醒下挿管を選ぶ", "#fbeeee", "#c0392b",
         ["高度開口障害", "気道の狭窄・偏位・腫瘤", "換気困難が予想される"],
         ["表面麻酔を十分に効かせる", "自発呼吸と気道反射を保つ", "外科的気道の担当者を確保"]),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 100, 56
    BTOP = HTOP + HH + 8
    crit_sz = min(cv.fit_size([l for c in COLS for l in c[3]], CW - 40, 10.4), 10.4)
    plan_sz = min(cv.fit_size([l for c in COLS for l in c[4]], CW - 40, 10.4), 10.4)
    BH = 34 + LH(crit_sz, 1.5) * 3 + 30 + 26 + LH(plan_sz, 1.5) * 3 + 30
    for i, (head, fc, ec, crit, plan) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=ec, ec=ec, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.5, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc=fc, ec=ec, lw=1.8, radius=8)
        cy = BTOP + 28
        cv.text(x + CW / 2, cy, "こう見えたら", size=9.6, color=ec, weight="bold")
        cy += 22
        for j, ln in enumerate(crit):
            cv.text(x + CW / 2, cy + LH(crit_sz, 1.5) * (j + 0.5), ln,
                    size=crit_sz, color=INK)
        cy += LH(crit_sz, 1.5) * 3 + 22
        cv.ax.plot([x + 34, x + CW - 34], [cy, cy], color=ec, lw=1.2,
                   ls=":", zorder=4)
        cy += 24
        cv.text(x + CW / 2, cy, "こう計画する", size=9.6, color=ec, weight="bold")
        cy += 22
        for j, ln in enumerate(plan):
            cv.text(x + CW / 2, cy + LH(plan_sz, 1.5) * (j + 0.5), ln,
                    size=plan_sz, color=INK)
    NOTE = ("※ どの層でも、Plan A が失敗したときの Plan B・C・D と、"
            "撤退の条件（何分・何回で止めるか）を導入前に言葉にしておく。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 140, 9.8)):
        cv.text(W / 2, BTOP + BH + 40 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f08_stratify.png"))


# ---------------------------------------------------------------- f09
def f09():
    W, H = 1520, 700
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "体位 —— 外耳孔と胸骨切痕を水平に揃える",
             size=12.5, ha="center")
    PANELS = [
        (60, "平坦なベッド（不適）", "#c0392b", -46, 0,
         ["外耳孔が胸骨切痕より低い", "軸が揃わず視野が open しない"]),
        (534, "スニッフィング位", "#2e6da4", 4, 46,
         ["下位頸椎を屈曲、上位頸椎を伸展", "枕の高さは 7〜9 cm が目安"]),
        (1008, "ランプ位（肥満）", "#1f6b47", 6, 132,
         ["上半身ごと挙上する", "外耳孔と胸骨切痕を水平に"]),
    ]
    PW, PTOP, PH = 452, 92, 312
    for px, title, col, ear_dy, ramp, caption in PANELS:
        cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
        cv.text(px + PW / 2, PTOP + 34, title, size=11.2, color=col,
                weight="bold")
        bed = PTOP + 250
        ax.plot([px + 40, px + PW - 40], [bed, bed], color="#b9c2cc", lw=4,
                zorder=2)
        # 体幹（ランプで傾く）
        torso = Polygon([[px + 60, bed], [px + 300, bed],
                         [px + 300, bed - 56 - ramp * 0.42],
                         [px + 60, bed - 34]],
                        closed=True, facecolor="#dfe6ee",
                        edgecolor="#9aa4b0", lw=1.6, zorder=3)
        ax.add_patch(torso)
        # 頭部
        hx, hy = px + 348, bed - 92 - ramp * 0.42 + ear_dy * -0.55
        ax.add_patch(Circle((hx, hy), 44, facecolor="#f2d5c6",
                            edgecolor="#c08d72", lw=1.8, zorder=4))
        # 外耳孔と胸骨切痕
        ear = (hx - 6, hy + 6)
        stern = (px + 300, bed - 56 - ramp * 0.42)
        for pt, c in ((ear, "#c0392b"), (stern, "#2e6da4")):
            ax.add_patch(Circle(pt, 7, facecolor=c, edgecolor="none", zorder=6))
        ax.plot([stern[0], ear[0]], [stern[1], ear[1]], color="#6b7785",
                lw=1.8, ls=(0, (5, 4)), zorder=5)
        ax.plot([stern[0] - 30, ear[0] + 40], [stern[1], stern[1]],
                color="#c3ccd6", lw=1.2, ls=":", zorder=5)
        cv.text(px + PW - 46, PTOP + 76, "外耳孔", size=9.0, color="#c0392b",
                ha="right")
        cv.text(px + 62, PTOP + 76, "胸骨切痕", size=9.0, color="#2e6da4",
                ha="left")
        for i, ln in enumerate(caption):
            cv.text(px + PW / 2, PTOP + PH + 32 + LH(10, 1.42) * i, ln,
                    size=10, color=INK)
    NOTE = ("※ 「枕を外して首を反らす」のはスニッフィング位ではない。"
            "肥満では頭だけを高くすると頸部が前屈し、かえって展開できなくなる。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 140, 9.8)):
        cv.text(W / 2, H - 70 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f09_position.png"))


# ---------------------------------------------------------------- f10
def f10():
    W, H = 1520, 648
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "マスク換気は「できる／できない」ではなく段階で記録する",
             size=12.5, ha="center")
    ROWS = [
        ("Grade 1", "片手法で問題なく換気できる", "#eaf4ee", "#1f6b47",
         "そのまま進む"),
        ("Grade 2", "経口／経鼻エアウェイや両手法を要する", "#e9f0fa", "#2e6da4",
         "エアウェイを入れ、下顎挙上を強める"),
        ("Grade 3", "2人法でも換気が不安定・不十分", "#fdf1e0", "#b8760f",
         "十分な筋弛緩を得る／SGA へ移る／応援を呼ぶ"),
        ("Grade 4", "どうやっても換気できない", "#fbeeee", "#c0392b",
         "SGA を試み、無効なら CICO を宣言する"),
    ]
    L, R = 52, W - 52
    LABW, ACTX = 168, 800
    TOP, RH, GAP = 108, 92, 14
    desc_sz = min(cv.fit_size([r[1] for r in ROWS], ACTX - L - LABW - 60, 10.6), 10.6)
    act_sz = min(cv.fit_size([r[4] for r in ROWS], R - ACTX - 40, 10.6), 10.6)
    for i, (g, desc, fc, ec, act) in enumerate(ROWS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc=fc, ec=ec, lw=1.8, radius=8)
        cv.box(L + 14, y + 16, LABW, RH - 32, fc=ec, ec=ec, lw=0, radius=6)
        cv.text(L + 14 + LABW / 2, y + RH / 2, g, size=11, color="white",
                weight="bold")
        cv.text(L + LABW + 42, y + RH / 2, desc, size=desc_sz, color=INK,
                ha="left")
        cv.ax.plot([ACTX - 24, ACTX - 24], [y + 18, y + RH - 18],
                   color=ec, lw=1.2, ls=":", zorder=4)
        cv.text(ACTX, y + RH / 2, act, size=act_sz, color=ec, ha="left",
                weight="bold")
    NOTE = ("※ 胸郭が動いて見えても、それが胃の膨満であることがある。"
            "換気の成否は呼気カプノグラムの持続する波形で判断する。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 140, 9.8)):
        cv.text(W / 2, TOP + 4 * (RH + GAP) + 30 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f10_mask.png"))


# ---------------------------------------------------------------- f11
def f11():
    W, H = 1520, 760
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "第1世代と第2世代の声門上器具 —— 違いは「胃への出口」がある",
             size=12, ha="center")
    PANELS = [
        (96, "第1世代", "#b8760f", False,
         ["咽頭を塞ぐカフのみ", "リーク圧はおおむね 20 cmH₂O 前後",
          "胃内容の逆流に対して無防備"]),
        (790, "第2世代", "#1f6b47", True,
         ["胃管ドレナージ路を内蔵", "リーク圧はおおむね 30 cmH₂O 前後",
          "逆流物を口腔外へ逃がす設計"]),
    ]
    PW, PTOP, PH = 632, 92, 330
    for px, title, col, gen2, lines in PANELS:
        cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
        cv.text(px + PW / 2, PTOP + 36, title, size=12, color=col, weight="bold")
        cy = PTOP + 196
        # 気道チューブ
        ax.add_patch(Rectangle((px + 74, cy - 16), 300, 32,
                               facecolor="#cfe0ef", edgecolor="#5b7fa6",
                               lw=1.6, zorder=3))
        # カフ
        ax.add_patch(Ellipse((px + 432, cy), 190, 122, facecolor="#e8eef5",
                             edgecolor="#5b7fa6", lw=2.0, zorder=3))
        ax.add_patch(Ellipse((px + 432, cy), 118, 66, facecolor="#ffffff",
                             edgecolor="#9aa4b0", lw=1.4, zorder=4))
        cv.text(px + 432, cy, "声門へ", size=9.0, color="#6b7785", z=5)
        if gen2:
            ax.add_patch(Rectangle((px + 74, cy + 34), 300, 20,
                                   facecolor="#dcefe2", edgecolor="#2e7d52",
                                   lw=1.6, zorder=3))
            ax.plot([px + 374, px + 470], [cy + 44, cy + 66],
                    color="#2e7d52", lw=4, solid_capstyle="round", zorder=4)
            cv.text(px + 224, cy + 78, "胃管ドレナージ路（食道へ）", size=9.4,
                    color="#1f6b47", ha="left")
        cv.text(px + 224, cy - 40, "換気路（声門へ）", size=9.4,
                color="#2e6da4", ha="left")
        for i, ln in enumerate(lines):
            cv.text(px + PW / 2, PTOP + PH + 34 + LH(10, 1.42) * i, ln,
                    size=10, color=INK)
    NOTE = ("※ ドレナージ路があっても気管カフのような遮断ではない。"
            "活動性の逆流や高い気道内圧の下では誤嚥を完全には防げない。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 140, 9.8)):
        cv.text(W / 2, H - 74 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f11_sga.png"))


for fn in (f08, f10, f11):
    fn()
    print("ok", fn.__name__)
