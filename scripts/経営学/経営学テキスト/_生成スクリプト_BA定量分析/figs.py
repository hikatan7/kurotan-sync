# -*- coding: utf-8 -*-
"""定量分析の入口 図版 f01〜f08（数値はすべて架空）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP, DPI)

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False

W = 1520
LIGHT = "#b8c0c9"


def P(n):
    return os.path.join(OUT, n)


def cbox(cv, x, y, w, h, style):
    """中身を後から置く枠。中心を返す。"""
    cv.box(x, y, w, h, style=style)
    return x + w / 2, y + h / 2


# ---------------------------------------------------------------- f01
def f01():
    H = 760
    cv = Canvas(W, H)
    cw = 440
    cards = [
        ("時系列", "過去と比べる", "先月は 450 件 → 38 件減った", "blue", 50, 40),
        ("計画・目標", "あるべき姿と比べる", "目標 430 件 → 18 件不足", "green", 540, 40),
        ("セグメント", "内部で分けて比べる", "外科系 −30 件、内科系 −8 件", "amber", 1030, 40),
        ("外部", "他施設と比べる", "同規模病院の平均は 380 件", "purple", 250, 540),
        ("関係", "別の数字と並べる", "麻酔科医の出勤数と連動している", "red", 830, 540),
    ]
    # 中央
    cx, cy, cwid, chei = W / 2 - 230, 300, 460, 150
    cv.box(cx, cy, cwid, chei, style="navy", lw=2.2)
    cv.text(W / 2, cy + 48, "今月の手術件数", size=12.5, color=NAVY, weight="bold")
    cv.text(W / 2, cy + 102, "412 件", size=22, color=NAVY, weight="bold")
    for head, sub, ex, st, x, y in cards:
        h = textbox(cv, x, y, cw, [sub, ex], 10.6, style=st, title=head,
                    title_size=12.5, min_h=170)
        # 中央の枠の縁から、カードの縁へ
        tx, ty = x + cw / 2, (y + h if y < cy else y)
        sx = min(max(tx, cx + 40), cx + cwid - 40)
        sy = cy if y < cy else cy + chei
        cv.arrow((sx, sy), (tx, ty), color=GREY, lw=1.8)
    cv.save(P("f01_hikaku.png"))


# ---------------------------------------------------------------- f02
def f02():
    H = 470
    cv = Canvas(W, H)
    steps = [
        ("What", "何が問題か", ["あるべき姿と現状の差", "目標と実績を比べる", "KPI を分解する"], "navy"),
        ("Where", "どこに問題があるか", ["層別で場所を絞る", "寄与の大きい順に並べる", "切り口を掛け合わせる"], "blue"),
        ("Why", "なぜ起きているか", ["仮説を複数立てる", "予言を先に書いて確かめる", "工程に分解する"], "amber"),
        ("How", "どうするか", ["選択肢を複数出す", "効果・費用・実現性", "副作用を比べる"], "green"),
    ]
    w, gap, x0, y = 330, 50, 45, 40
    hs = []
    for i, (en, jp, lines, st) in enumerate(steps):
        x = x0 + i * (w + gap)
        h = textbox(cv, x, y, w, [jp, ""] + lines, 10.8, style=st, title=en,
                    title_size=16, min_h=300)
        hs.append(h)
        if i < 3:
            cv.arrow((x + w + 6, y + h / 2), (x + w + gap - 6, y + h / 2),
                     color=GREY, lw=2.4, head=14)
    yb = y + max(hs) + 30
    cv.box(x0, yb, 4 * w + 3 * gap, 70, style="grey")
    cv.text(W / 2, yb + 35, "いまどの段階の問いに答えているかを見失わなければ、行きつ戻りつしてよい",
            size=11.2, color=INK)
    cv.save(P("f02_steps.png"))


# ---------------------------------------------------------------- f03
def f03():
    H = 700
    cv = Canvas(W, H)
    bw, bh = 300, 76

    def node(x, yc, s, st):
        cv.box(x, yc - bh / 2, bw, bh, style=st)
        sz = cv.fit_size([s], bw - 24, 11.5)
        cv.text(x + bw / 2, yc, s, size=sz, color=INK, weight="bold")
        return (x, yc)

    def link(a, b, op=None):
        (x1, y1), (x2, y2) = a, b
        mx = x1 + bw + 36
        cv.ax.plot([x1 + bw, mx, mx, x2], [y1, y1, y2, y2], color=GREY, lw=1.6, zorder=2)
        if op:
            cv.text(mx - 16, (y1 + y2) / 2 if False else y2 - 26, op, size=11, color=GREY)

    X = [40, 420, 800, 1180]
    r = node(X[0], 350, "手術室の収益", "navy")
    n = node(X[1], 190, "件数", "blue")
    u = node(X[1], 520, "1 件あたり単価", "green")
    link(r, n); link(r, u, "×")
    a1 = node(X[2], 70, "稼働室数", "blue")
    a2 = node(X[2], 190, "稼働日数", "blue")
    a3 = node(X[2], 310, "1 室 1 日あたり件数", "blue")
    for t, op in ((a1, None), (a2, "×"), (a3, "×")):
        link(n, t, op)
    b1 = node(X[2], 470, "術式の構成", "green")
    b2 = node(X[2], 590, "加算の算定", "green")
    link(u, b1); link(u, b2, "＋")
    c1 = node(X[3], 250, "枠の利用率", "amber")
    c2 = node(X[3], 370, "入替時間", "amber")
    link(a3, c1); link(a3, c2)
    cv.text(X[3] + bw / 2, 436, "↑ 麻酔科・看護部・外科の", size=10, color=GREY)
    cv.text(X[3] + bw / 2, 464, "連携で動く", size=10, color=GREY)
    cv.text(X[3] + bw / 2, 530, "← 医事課と診療科で動く", size=10, color=GREY)
    cv.save(P("f03_kpitree.png"))


# ---------------------------------------------------------------- charts
def chart(figsize=(7.6, 3.6)):
    fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(LIGHT)
    ax.spines["bottom"].set_color(LIGHT)
    ax.tick_params(colors=INK, labelsize=9.5)
    ax.yaxis.grid(True, color="#e6e9ed", lw=0.8)
    ax.set_axisbelow(True)
    return fig, ax


def save(fig, name):
    fig.tight_layout()
    fig.savefig(P(name), dpi=DPI, facecolor="white")
    plt.close(fig)


DAYS = ["月", "火", "水", "木", "金"]
DEM = np.array([175, 125, 115, 120, 165])
CAP = 36.0


def f04():
    fig, ax = chart()
    u = DEM * 0.2 / CAP * 100
    cols = [RED if v >= 90 else LIGHT for v in u]
    bars = ax.bar(DAYS, u, color=cols, width=0.62)
    for b, v in zip(bars, u):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, "%d%%" % round(v),
                ha="center", va="bottom", fontsize=10, color=INK)
    ax.axhline(78, color=NAVY, ls="--", lw=1.4)
    ax.text(2, 79.5, "週平均 78%", color=NAVY, fontsize=9.5, ha="center", va="bottom")
    ax.axhline(100, color=GREY, lw=1.0)
    ax.text(2, 101.5, "処理能力の上限（100%）", color=GREY, fontsize=9, ha="center", va="bottom")
    ax.set_ylim(0, 115)
    ax.set_ylabel("稼働率（%）", fontsize=10, color=INK)
    save(fig, "f04_peak.png")


def f05():
    fig, ax = chart((7.6, 3.9))
    r = np.linspace(0.3, 0.965, 300)
    base = r / (1 - r)
    for v, c, lab in ((0.5, GREEN, "ばらつき小（因子 0.5）"),
                      (1.0, BLUE, "ばらつき中（因子 1）"),
                      (2.0, RED, "ばらつき大（因子 2）")):
        ax.plot(r * 100, base * v, color=c, lw=2.2, label=lab)
    for x in (80, 90):
        ax.axvline(x, color=LIGHT, lw=1, ls=":")
        ax.text(x, 41, "%d%%" % x, ha="center", va="bottom", fontsize=9, color=GREY)
    ax.set_xlim(30, 100)
    ax.set_ylim(0, 40)
    ax.set_xlabel("稼働率（%）", fontsize=10, color=INK)
    ax.set_ylabel("平均待ち時間\n（平均処理時間の何倍か）", fontsize=9.5, color=INK)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    save(fig, "f05_kingman.png")


def f06():
    fig, ax = chart((7.6, 3.6))
    groups = ["合計", "高リスク患者", "低リスク患者"]
    X = [8.0, 11.0, 3.5]
    Y = [6.0, 13.0, 4.25]
    n = [("40/500", "30/500"), ("33/300", "13/100"), ("7/200", "17/400")]
    xi = np.arange(3)
    w = 0.34
    bx = ax.bar(xi - w / 2, X, w, color=NAVY, label="チーム X")
    by = ax.bar(xi + w / 2, Y, w, color=LIGHT, label="チーム Y")
    for bars, vals, k in ((bx, X, 0), (by, Y, 1)):
        for b, v, nn in zip(bars, vals, n):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.25,
                    "%s%%\n(%s)" % (("%.2f" % v).rstrip("0").rstrip("."), nn[k]),
                    ha="center", va="bottom", fontsize=8.6, color=INK, linespacing=1.2)
    ax.set_xticks(xi)
    ax.set_xticklabels(groups, fontsize=10)
    ax.set_ylim(0, 16.5)
    ax.set_ylabel("合併症率（%）", fontsize=10, color=INK)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    save(fig, "f06_simpson.png")


def f07():
    fig, ax = chart((7.6, 3.5))
    ax.yaxis.grid(False)
    ax.xaxis.grid(True, color="#e6e9ed", lw=0.8)
    items = [("整形外科", -280), ("外科", -10), ("脳神経外科", -10),
             ("その他", 10), ("循環器内科", 20), ("内科", 30), ("合計", -240)]
    items = items[::-1]
    labs = [a for a, _ in items]
    vals = [b for _, b in items]
    cols = [NAVY if a == "合計" else (RED if a == "整形外科" else LIGHT) for a in labs]
    bars = ax.barh(labs, vals, color=cols, height=0.62)
    for b, v in zip(bars, vals):
        ax.text(v + (6 if v >= 0 else -6), b.get_y() + b.get_height() / 2,
                ("+%d" % v) if v > 0 else ("−%d" % -v),
                ha="left" if v >= 0 else "right", va="center", fontsize=9.5, color=INK)
    ax.axvline(0, color=GREY, lw=1)
    ax.set_xlim(-340, 80)
    ax.set_xlabel("紹介患者数の増減（件、前年度比）", fontsize=10, color=INK)
    save(fig, "f07_ex1.png")


def f08():
    fig, ax = chart((7.6, 3.6))
    now = DEM * 0.2 / CAP * 100
    c = np.array([145, 145, 135, 140, 135]) * 0.2 / CAP * 100
    xi = np.arange(5)
    w = 0.36
    b1 = ax.bar(xi - w / 2, now, w, color=LIGHT, label="現状")
    b2 = ax.bar(xi + w / 2, c, w, color=GREEN, label="C 案（予定検査を火〜木へ）")
    for bars, vals in ((b1, now), (b2, c)):
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 1.5, "%d" % round(v),
                    ha="center", va="bottom", fontsize=9, color=INK)
    ax.axhline(90, color=RED, ls="--", lw=1.2)
    ax.text(4.5, 91, "90%", color=RED, fontsize=9, ha="right", va="bottom")
    ax.set_xticks(xi)
    ax.set_xticklabels(DAYS, fontsize=10)
    ax.set_ylim(0, 118)
    ax.set_ylabel("稼働率（%）", fontsize=10, color=INK)
    ax.legend(frameon=False, fontsize=9, loc="upper center", ncol=2)
    save(fig, "f08_ex2.png")


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08):
        fn()
        print("ok", fn.__name__)
