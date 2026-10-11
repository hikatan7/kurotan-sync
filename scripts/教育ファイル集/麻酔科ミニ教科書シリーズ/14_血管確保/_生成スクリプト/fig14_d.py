# -*- coding: utf-8 -*-
"""第14巻 血管確保 図版 f19・f20"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f19
def f19():
    W, H = 1520, 440
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "画面が見えないとき、触るのはこの4つ ── 所要時間10秒",
             size=12.5, ha="center")
    COLS = [
        ("① 深度", "#2e6da4", "depth",
         ["目標血管が画面の上から", "1/3〜1/2 に来るまで浅くする",
          "深いままだと血管が小さく映り", "針先も見えない"]),
        ("② ゲイン", "#1f6b47", "gain",
         ["全体の明るさ", "上げすぎると内腔にノイズが乗り",
          "血栓や壁と区別がつかない", "内腔が真っ黒に見える程度に"]),
        ("③ フォーカス", "#7b52a8", "focus",
         ["ビームが最も細く絞られる深さ", "目標血管の深さに合わせる",
          "その位置の分解能が上がる", "―"]),
        ("④ プリセット", "#b8760f", "preset",
         ["「血管」「小部位」などの初期設定", "ゼロから調整するより速い",
          "施設で設定を共有しておくと", "再現性がある"]),
    ]
    L, R = 44, W - 44
    GAP = 16
    CW = (R - L - GAP * 3) / 4
    HTOP, HH = 96, 72
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size([l for c in COLS for l in c[3]], CW - 40, 9.8), 9.8)
    BH = 34 + LH(sz, 2.0) * 4
    for i, (head, col, eng, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + 26, head, size=11.4, color="white",
                weight="bold")
        cv.text(x + CW / 2, HTOP + 54, eng, size=8.6, color="#e3e9ef")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            if ln == "―":
                continue
            cv.text(x + CW / 2, BTOP + 34 + LH(sz, 2.0) * j, ln, size=sz,
                    color=INK)
    NOTE = ("※ 血管確保に使うのは高周波リニアプローブ（おおむね 5〜15 MHz）。"
            "狙う深さは 0.3〜2 cm 程度である。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, BTOP + BH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f19_us_settings.png"))


# ---------------------------------------------------------------- f20
def f20():
    W, H = 1520, 700
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "骨髄路 ── 骨髄腔は虚脱しないので、ショックでも使える",
             size=12.5, ha="center")
    BONE, MARROW, MARK = "#e6dfd3", "#d9b8a4", "#c0392b"
    PANELS = [
        ("脛骨近位内側", "第一選択", "top",
         "脛骨粗面の内側やや下方。平坦で目標が取りやすく、胸骨圧迫の妨げにならない",
         0.30),
        ("脛骨遠位内側", "代替", "bottom",
         "内果の上方。近位脛骨が使えないときに選ぶ", 0.74),
        ("上腕骨近位", "代替", "top",
         "大結節。薬剤の到達は速いが、体動で逸脱しやすい", 0.22),
    ]
    L = 60
    PW, PTOP = 452, 88
    CSZ = 9.6
    nline = max(len(cv.wrap(p[3], PW - 52, CSZ)) for p in PANELS)
    CAPTOP = 100 + 236 + 26
    PH = CAPTOP + LH(CSZ, 1.5) * nline + 22
    for i, (title, tag, flare, caption, frac) in enumerate(PANELS):
        px = L + i * (PW + 22)
        cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
        cv.text(px + PW / 2, PTOP + 28, title, size=11.6, color=NAVY,
                weight="bold")
        tw = cv.measure(tag, 9.2, weight="bold")[0] + 26
        tc = "#1f6b47" if tag == "第一選択" else "#5d6875"
        cv.box(px + PW / 2 - tw / 2, PTOP + 52, tw, 34, fc=tc, ec=tc, lw=0,
               radius=6)
        cv.text(px + PW / 2, PTOP + 69, tag, size=9.0, color="white",
                weight="bold")
        bx, by, bw, bh = px + PW / 2 - 46, PTOP + 100, 92, 236
        ax.add_patch(Rectangle((bx, by), bw, bh, facecolor=BONE,
                               edgecolor="#b8ac99", lw=1.6, zorder=3))
        ax.add_patch(Rectangle((bx + 22, by + 10), bw - 44, bh - 20,
                               facecolor=MARROW, edgecolor="none", zorder=4))
        if flare == "top":
            pts = [(bx - 22, by), (bx + bw + 22, by),
                   (bx + bw, by + 34), (bx, by + 34)]
        else:
            pts = [(bx - 22, by + bh), (bx + bw + 22, by + bh),
                   (bx + bw, by + bh - 34), (bx, by + bh - 34)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=BONE,
                             edgecolor="#b8ac99", lw=1.6, zorder=3))
        my = by + bh * frac
        ax.add_patch(Circle((bx + 4, my), 9, facecolor=MARK,
                            edgecolor="white", lw=1.6, zorder=6))
        cv.arrow((bx - 84, my - 26), (bx - 6, my - 4), color=MARK, lw=2.2,
                 head=9, z=6)
        cv.text(bx - 88, my - 34, "穿刺点", size=9.4, color=MARK, ha="right",
                weight="bold")
        cv.text(bx + bw + 16, by + bh * 0.5, "骨髄腔", size=9.4,
                color="#7a6a55", ha="left")
        for j, ln in enumerate(cv.wrap(caption, PW - 52, CSZ)):
            cv.text(px + PW / 2, PTOP + CAPTOP + LH(CSZ, 1.5) * j, ln,
                    size=CSZ, color=INK)
    NOTE = ("※ 禁忌 ── 同一骨の骨折・24時間以内の穿刺歴、穿刺部の感染・熱傷、"
            "同側の主要血管損傷、骨の脆弱性がある疾患、人工関節や当該骨の手術歴。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, PTOP + PH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f20_io_sites.png"))


for fn in (f19, f20):
    fn()
    print("ok", fn.__name__)
