# -*- coding: utf-8 -*-
"""第13巻 気道管理 図版 f01〜f06"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(name):
    return os.path.join(OUT, name)


# ---------------------------------------------------------------- f01
def f01():
    W, H = 1520, 820
    cv = Canvas(W, H)
    cv.title(W / 2, 46, "気道確保は「段」で考える —— 目的は挿管ではなく酸素化の維持",
             size=12.5, ha="center")
    STEPS = [
        ("① 体位と用手気道確保", "頭部後屈・下顎挙上／スニッフィング位・ランプ位",
         "#eaf4ee", "#1f6b47"),
        ("② 気道補助具", "経口・経鼻エアウェイ　舌根沈下を機械的に外す",
         "#e9f0fa", "#2e6da4"),
        ("③ フェイスマスク換気", "2人法・両手下顎挙上　気道内圧は 15 cmH₂O 以下を目安",
         "#eaf1f8", "#2e6da4"),
        ("④ 声門上器具（SGA）", "第2世代を第一に。挿管失敗時の救済換気の主役",
         "#fdf1e0", "#b8760f"),
        ("⑤ 気管挿管", "ビデオ喉頭鏡／ブジー／気管支鏡　試行は原則3回まで",
         "#fdf1e0", "#b8760f"),
        ("⑥ 緊急前頸部気道（eFONA）", "CICO 宣言後　メス・ブジー・チューブ法",
         "#fbeeee", "#c0392b"),
    ]
    L, R = 60, W - 60
    TOP, RH, GAP = 104, 96, 14
    for i, (head, body, fc, ec) in enumerate(STEPS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc=fc, ec=ec, lw=1.8, radius=8)
        cv.text(L + 30, y + RH / 2 - LH(11) * 0.42, head, size=11,
                color=ec, weight="bold", ha="left")
        cv.text(L + 30, y + RH / 2 + LH(10) * 0.48, body, size=9.6,
                color=INK, ha="left")
        if i < len(STEPS) - 1:
            cv.arrow((W / 2, y + RH + 1), (W / 2, y + RH + GAP - 1),
                     color="#8d97a3", lw=2.0, head=9)
    NOTE = ("※ 上の段が失敗したら同じ手を繰り返さず、次の段へ移る。"
            "どの段に居ても、酸素化の維持が最優先である。")
    cv.text(W / 2, TOP + 6 * (RH + GAP) + 26,
            NOTE, size=cv.fit_size([NOTE], R - L, 9.6), color="#5d6875")
    cv.save(P("f01_hierarchy.png"))


# ---------------------------------------------------------------- f02
def f02():
    W, H = 1520, 800
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "意識消失で上気道が閉じる —— 詰まる場所は3つある",
             size=12.5, ha="center")
    PANELS = [
        (70, "覚醒時", "#eaf4ee", "#1f6b47",
         ["咽頭拡張筋が持続的に働き", "咽頭腔（virtual space）が開く"]),
        (530, "意識消失", "#fdf1e0", "#b8760f",
         ["筋緊張が落ち、軟口蓋・舌根・", "喉頭蓋が後方へ倒れる"]),
        (990, "用手気道確保", "#eaf1f8", "#2e6da4",
         ["頭部後屈＋下顎挙上で", "3か所を同時に前方へ引き出す"]),
    ]
    PW, PTOP, PH = 460, 92, 400
    for x, title, fc, ec, lines in PANELS:
        cv.box(x, PTOP, PW, PH, fc="white", ec=ec, lw=1.8, radius=8)
        cv.text(x + PW / 2, PTOP + 34, title, size=11.5, color=ec, weight="bold")
        # 咽頭の模式
        ax = cv.ax
        base_y = PTOP + 250
        ax.plot([x + 60, x + PW - 60], [base_y + 96, base_y + 96],
                color="#c3ccd6", lw=3, zorder=2)
        ax.add_patch(Polygon([[x + 60, base_y + 96], [x + 140, base_y - 60],
                              [x + 200, base_y + 96]],
                             closed=True, facecolor="#f0d7c9",
                             edgecolor="#b98f78", lw=1.4, zorder=3))
        collapse = {"覚醒時": 0, "意識消失": 52, "用手気道確保": 8}[title]
        ax.add_patch(Ellipse((x + 250, base_y + 40 + collapse * 0.4), 190, 92,
                             facecolor="#f2c9b8", edgecolor="#b98f78",
                             lw=1.4, zorder=3))          # 舌根
        ax.add_patch(Ellipse((x + 168, base_y - 46 + collapse * 0.5), 120, 54,
                             facecolor="#f0d7c9", edgecolor="#b98f78",
                             lw=1.4, zorder=3))          # 軟口蓋
        ax.add_patch(Polygon([[x + 336, base_y - 24 + collapse * 0.7],
                              [x + 388, base_y - 66 + collapse * 0.7],
                              [x + 372, base_y + 6 + collapse * 0.7]],
                             closed=True, facecolor="#f2c9b8",
                             edgecolor="#b98f78", lw=1.4, zorder=3))  # 喉頭蓋
        gap = 78 - collapse
        ax.add_patch(FancyBboxPatch((x + 150, base_y - 4),
                                    230, max(gap, 6),
                                    boxstyle="round,pad=2",
                                    facecolor="#cfe6ea" if gap > 20 else "#f6c6c2",
                                    edgecolor="none", zorder=2))
        for i, ln in enumerate(lines):
            cv.text(x + PW / 2, PTOP + PH + 34 + LH(10, 1.4) * i, ln,
                    size=10, color=INK)
    LAB = [("軟口蓋", 240, 380), ("舌　根", 320, 470), ("喉頭蓋", 445, 400)]
    for txt, lx, ly in LAB:
        cv.text(lx, ly, txt, size=9.4, color="#8d5a3c")
    NOTE = ("※ 「舌が落ちる」だけではない。軟口蓋・舌根・喉頭蓋のどれが主因かで、"
            "エアウェイの種類も、下顎挙上の効き方も変わる。")
    cv.text(W / 2, H - 44, NOTE,
            size=cv.fit_size([NOTE], W - 120, 9.6), color="#5d6875")
    cv.save(P("f02_upper_airway.png"))


# ---------------------------------------------------------------- f03
def f03():
    W, H, DPI = 1520, 820, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0.095, 0.175, 0.855, 0.665])
    d = np.linspace(2.0, 8.0, 400)
    lam = (8.0 / d) ** 4
    turb = (8.0 / d) ** 5
    ax.plot(d, lam, color="#2e6da4", lw=3.4, label="層流：抵抗 ∝ 1/r⁴")
    ax.plot(d, turb, color="#c0392b", lw=3.2, ls=(0, (8, 5)),
            label="乱流：抵抗 ∝ 1/r⁵")
    for dd, col in ((8.0, "#2e7d52"), (6.0, "#d98e2b"), (4.0, "#c0392b")):
        ax.plot([dd], [(8.0 / dd) ** 4], marker="o", ms=12, color=col, zorder=5)
    ax.annotate("成人気管 8 mm\n（基準 = 1）", xy=(8.0, 1.0), xytext=(6.55, 6.2),
                fontsize=11, color="#2e7d52", ha="left", va="top",
                linespacing=1.6,
                arrowprops=dict(arrowstyle="->", color="#2e7d52", lw=1.6))
    ax.annotate("1 mm の浮腫で 6 mm\n→ 層流でも 3.2 倍", xy=(6.0, 3.16),
                xytext=(4.15, 14.5), fontsize=11, color="#b8760f",
                ha="left", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="->", color="#b8760f", lw=1.6))
    ax.annotate("2 mm の浮腫で 4 mm\n→ 16 倍、乱流なら 32 倍", xy=(4.0, 16.0),
                xytext=(4.35, 27.5), fontsize=11, color="#c0392b",
                ha="left", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.6))
    ax.set_xlim(2.0, 8.6)
    ax.set_ylim(0, 33)
    ax.set_xlabel("気道の内径（mm）", fontsize=12, color=INK, labelpad=10)
    ax.set_ylabel("気流抵抗（内径 8 mm を 1 とした相対値）", fontsize=12,
                  color=INK, labelpad=10)
    ax.set_title("1 mm の浮腫が、なぜ致命的になりうるか", fontsize=13,
                 color="#0A1830", weight="bold", pad=16)
    ax.legend(fontsize=11, loc="upper right", frameon=True, framealpha=1.0,
              edgecolor="#c3ccd6")
    ax.grid(color="#eceff2", lw=1.0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11, colors=INK)
    for s in ax.spines.values():
        s.set_color("#7c8894")
    fig.text(0.5, 0.05,
             "※ 小児では基準となる内径が小さいため、同じ 1 mm の浮腫が成人よりはるかに大きな抵抗上昇を生む。",
             fontsize=10, color="#8d97a3", ha="center", va="center")
    fig.savefig(P("f03_resistance.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f04
def f04():
    W, H, DPI = 1520, 920, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0.115, 0.235, 0.845, 0.60])
    t = np.linspace(0, 12, 600)

    def curve(t_start_fall, t_to_80):
        y = np.full_like(t, 99.0)
        m = t > t_start_fall
        z = (t[m] - t_start_fall) / t_to_80
        y[m] = 99 - 19 * z ** 1.9
        return np.clip(y, 40, 100)

    SERIES = [
        ("健常成人（前酸素化十分）", curve(6.0, 2.6), "#2e6da4", "-"),
        ("高度肥満 BMI 40", curve(1.3, 0.9), "#c0392b", (0, (8, 5))),
        ("妊婦（末期）", curve(1.7, 1.1), "#7b52a8", (0, (2, 2.4))),
        ("小児（乳児）", curve(1.0, 0.7), "#b8760f", (0, (6, 3, 1.5, 3))),
    ]
    for lab, y, col, ls in SERIES:
        ax.plot(t, y, color=col, lw=3.2, ls=ls, label=lab)
    ax.axhline(90, color="#8d97a3", lw=1.8, ls=":")
    ax.text(11.8, 91.0, "SpO₂ 90%", fontsize=10.5, color="#6b7785",
            ha="right", va="bottom")
    ax.set_xlim(0, 12)
    ax.set_ylim(60, 102)
    ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel("無呼吸開始からの時間（分）", fontsize=12, color=INK, labelpad=10)
    ax.set_ylabel("SpO₂（%）", fontsize=12, color=INK, labelpad=10)
    ax.set_title("同じ前酸素化でも、無呼吸に耐えられる時間はまったく違う",
                 fontsize=13, color="#0A1830", weight="bold", pad=16)
    ax.legend(fontsize=11, loc="lower left", frameon=True, framealpha=1.0,
              edgecolor="#c3ccd6")
    ax.grid(color="#eceff2", lw=1.0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11, colors=INK)
    for s in ax.spines.values():
        s.set_color("#7c8894")
    for i, ln in enumerate([
            "※ 概念図。機能的残気量（FRC）が小さく酸素消費量が大きいほど、脱飽和は早い。",
            "　 「まだ 5 分ある」は健常成人にしか成り立たない。"]):
        fig.text(0.5, 0.075 - i * 0.038, ln, fontsize=9.8, color="#8d97a3",
                 ha="center", va="center")
    fig.savefig(P("f04_desaturation.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f05
def f05():
    W, H, DPI = 1520, 840, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0.105, 0.205, 0.775, 0.625])
    ax2 = ax.twinx()
    t = np.linspace(0, 25, 500)
    spo2 = np.where(t < 18, 99.5, 99.5 - 0.55 * (t - 18) ** 1.6)
    paco2 = 40 + 3.0 * t
    l1, = ax.plot(t, np.clip(spo2, 80, 100), color="#2e6da4", lw=3.6,
                  label="SpO₂（酸素化）")
    l2, = ax2.plot(t, paco2, color="#c0392b", lw=3.4, ls=(0, (8, 5)),
                   label="PaCO₂（換気）")
    ax2.axhline(100, color="#c0392b", lw=1.4, ls=":")
    ax2.text(24.6, 103, "PaCO₂ 100 mmHg", fontsize=10.5, color="#c0392b",
             ha="right", va="bottom")
    ax.set_xlim(0, 25)
    ax.set_ylim(80, 102)
    ax2.set_ylim(30, 125)
    ax.set_xlabel("無呼吸酸素化（HFNO）の経過時間（分）", fontsize=12,
                  color=INK, labelpad=10)
    ax.set_ylabel("SpO₂（%）", fontsize=12, color="#2e6da4", labelpad=10)
    ax2.set_ylabel("PaCO₂（mmHg）", fontsize=12, color="#c0392b", labelpad=12)
    ax.set_title("酸素化が保たれていることは、換気が保たれていることではない",
                 fontsize=13, color="#0A1830", weight="bold", pad=16)
    ax.legend(handles=[l1, l2], fontsize=11, loc="lower left", frameon=True,
              framealpha=1.0, edgecolor="#c3ccd6")
    ax.grid(color="#eceff2", lw=1.0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11, colors=INK)
    ax2.tick_params(labelsize=11, colors=INK)
    for s in list(ax.spines.values()) + list(ax2.spines.values()):
        s.set_color("#7c8894")
    for i, ln in enumerate([
            "※ PaCO₂ の上昇はおおむね直線的で、報告される速度は毎分およそ 3 mmHg 前後。",
            "　 SpO₂ を根拠に無呼吸時間を無制限に延ばしてはならない。"]):
        fig.text(0.5, 0.072 - i * 0.040, ln, fontsize=9.8, color="#8d97a3",
                 ha="center", va="center")
    fig.savefig(P("f05_apnoeic_ox.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f06
def f06():
    W, H, DPI = 1520, 840, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0.245, 0.195, 0.70, 0.665])
    ROWS = [
        ("Mallampati III/IV", 0.42, 0.86),
        ("甲状オトガイ間距離", 0.24, 0.94),
        ("開口量（切歯間距離）", 0.27, 0.90),
        ("頸部可動域", 0.31, 0.93),
        ("上唇咬合試験", 0.67, 0.92),
        ("複合スコア", 0.60, 0.90),
    ]
    y = np.arange(len(ROWS))[::-1]
    h = 0.34
    ax.barh(y + h / 2, [r[1] for r in ROWS], h, color="#1f4e88", label="感度")
    ax.barh(y - h / 2, [r[2] for r in ROWS], h, color="#0f5c3f", label="特異度")
    for yy, r in zip(y, ROWS):
        ax.text(r[1] + 0.012, yy + h / 2, f"{r[1]:.2f}", fontsize=10.5,
                color="#1f4e88", va="center", weight="bold")
        ax.text(r[2] + 0.012, yy - h / 2, f"{r[2]:.2f}", fontsize=10.5,
                color="#0f5c3f", va="center", weight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in ROWS], fontsize=11.5, color=INK)
    ax.set_xlim(0, 1.09)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("感度・特異度（代表的なメタ解析の概数）", fontsize=12,
                  color=INK, labelpad=10)
    ax.set_title("ベッドサイドの所見は、どれも単独では困難気道を拾いきれない",
                 fontsize=13, color="#0A1830", weight="bold", pad=16)
    ax.legend(fontsize=11, loc="lower right", frameon=True, framealpha=1.0,
              edgecolor="#c3ccd6")
    ax.grid(axis="x", color="#eceff2", lw=1.0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11, colors=INK)
    for s in ax.spines.values():
        s.set_color("#7c8894")
    for i, ln in enumerate([
            "※ 特異度は高く感度は低い。つまり「所見あり」は準備の根拠になるが、",
            "　 「所見なし」は困難でないことの保証にならない。"]):
        fig.text(0.5, 0.068 - i * 0.040, ln, fontsize=9.8, color="#8d97a3",
                 ha="center", va="center")
    fig.savefig(P("f06_bedside_tests.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


for fn in (f04,):
    fn()
    print("ok", fn.__name__)
