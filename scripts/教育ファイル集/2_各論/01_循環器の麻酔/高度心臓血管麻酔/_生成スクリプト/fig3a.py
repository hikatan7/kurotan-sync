# -*- coding: utf-8 -*-
"""第Ⅲ章 脊髄保護　図版 h01〜h07"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)
from fig1a import cap, msg, fitlines, card, W, TEAL
from figcrop import crop_bottom

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- h01
def h01():
    """脊髄の血流支配"""
    cv = Canvas(W, 1060)
    cap(cv, 44, "脊髄は、一本の動脈で養われているのではない")

    # 左：脊髄と分節動脈
    LX, LY, LW, LH_ = 70, 130, 620, 700
    cv.box(LX, LY, LW, LH_, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(LX + LW / 2, LY + 34, "大動脈から脊髄へ", size=12.2, color=NAVY,
            weight="bold")

    # 大動脈（縦）
    cv.rect(LX + 100, LY + 80, 56, 500, fc="#f0e3e3", ec="#c9a2a2", lw=1.4)
    cv.text(LX + 126, LY + 66, "大動脈", size=10.0, color=GREY)
    # 脊髄（縦）
    cv.rect(LX + 430, LY + 80, 56, 500, fc="#eef1f5", ec="#b9c2cc", lw=1.4)
    cv.text(LX + 458, LY + 66, "脊髄", size=10.0, color=GREY)
    cv.text(LX + LW / 2, LY + 616, "前脊髄動脈は細く、単独では支えきれない",
            size=9.4, color=GREY)

    LEV = [("T4", 120), ("T6", 190), ("T8", 260), ("T9-T12", 330),
           ("L1", 400), ("L2", 470)]
    for lab, dy in LEV:
        y = LY + dy
        cv.arrow((LX + 158, y), (LX + 426, y), color=BLUE, lw=2.0, head=9)
        cv.text(LX + 292, y - 16, "分節動脈", size=8.8, color=BLUE)
        cv.text(LX + 86, y, lab, size=9.4, color=GREY, ha="right")

    # 右：三層の説明
    RX = LX + LW + 30
    RW = W - 70 - RX
    ITEMS = [("① 分節動脈（肋間・腰動脈）", BLUE, "#eaf1f8",
              ["大動脈から左右に分かれて出る",
               "手術やステントで何本かが失われる"]),
             ("② 側副血行網", GREEN, "#eaf5ee",
              ["椎体周囲・傍脊柱筋・硬膜外の網目",
               "鎖骨下動脈と腸骨動脈からも流入する"]),
             ("③ 前脊髄動脈", PURPLE, "#f1ecf8",
              ["脊髄の前 2/3 を養う",
               "Adamkiewicz 動脈が最大の供給枝"])]
    y = LY + 10
    for t, col, fc, lines in ITEMS:
        h = card(cv, RX, y, RW, t, lines, col, fc, body_size=10.2, lh=1.8)
        y += h + 26

    msg(cv, LY + LH_ + 30,
        "「Adamkiewicz 動脈を温存すれば守れる」という理解は、もう古い")
    cv.save(P("h01_blood_supply.png"))
    crop_bottom(P("h01_blood_supply.png"))


# ---------------------------------------------------------------- h02
def h02():
    """側副血行網の圧と再構築"""
    cv = Canvas(W, 900)
    cap(cv, 44, "分節動脈を一度に切ると、側副血行網の圧が落ちる")

    x0, y0 = 110, 180
    pw, ph = W - 260, 330
    cv.rect(x0, y0, pw, ph, fc="#fbfcfd", ec="#dde3ea", lw=1.4)
    for v, lab in ((0.05, "100"), (0.30, "75"), (0.55, "50"), (0.80, "25")):
        yy = y0 + ph * v
        cv.ax.plot([x0, x0 + pw], [yy, yy], color="#e8ecf0", lw=1.0, zorder=1)
        cv.text(x0 - 16, yy, lab, size=9.2, color=GREY, ha="right")
    cv.text(x0 + pw, y0 - 24, "側副血行網の圧（ベースラインに対する %）",
            size=9.4, color=GREY, ha="right")

    # 一度に切った場合
    PTS = [("ベース", 0.05, 100), ("全分節動脈を結紮", 0.28, 27),
           ("24 時間後", 0.55, 40), ("120 時間後", 0.86, 90)]
    xs = [x0 + pw * p for _, p, _ in PTS]
    ys = [y0 + ph * (1.0 - v / 100.0) * 0.95 + ph * 0.02 for _, _, v in PTS]
    cv.ax.plot(xs, ys, color=RED, lw=2.8, marker="o", markersize=6, zorder=4)
    for (lab, p, v), xx, yy in zip(PTS, xs, ys):
        cv.text(xx, y0 + ph + 26, lab, size=9.6, color=INK)
        cv.text(xx, yy - 24, "%d%%" % v, size=10.4, color=RED, weight="bold")

    # 2段階
    cv.ax.plot([xs[0], xs[1]], [ys[0], y0 + ph * 0.38], color=GREEN, lw=2.8,
               marker="o", markersize=6, zorder=4, linestyle="--")
    cv.text(xs[1] + 20, y0 + ph * 0.34, "2 回に分ければ 50〜70% で済む",
            size=10.2, color=GREEN, weight="bold", ha="left")

    textbox(cv, 70, y0 + ph + 70, W - 140,
            ["ブタの実験では、側副血行網の圧はもともと大動脈圧の 75% であった。",
             "全分節動脈を一度に結紮すると 27% まで落ち、"
             "24 時間で 40%、120 時間で 90% まで回復した。",
             "このとき約半数に脊髄障害が生じたが、"
             "1 週間あけて 2 段階で結紮した場合は 50〜70% の低下にとどまり、障害は減った。"],
            10.5, style="green", title="段階的に切るという発想の出どころ",
            title_color=GREEN, pad_y=16)
    cv.save(P("h02_collateral_pressure.png"))
    crop_bottom(P("h02_collateral_pressure.png"))


# ---------------------------------------------------------------- h03
def h03():
    """SCPP の式"""
    cv = Canvas(W, 1000)
    cap(cv, 44, "脊髄灌流圧は、引き算で決まる")

    cx = W / 2
    # 式
    FW = W - 140
    cv.box(cx - FW / 2, 120, FW, 110, fc="#e8edf5", ec=NAVY, lw=2.0, radius=12)
    eq = "脊髄灌流圧（SCPP）＝ 平均動脈圧（MAP）－ 髄液圧（CSF 圧）"
    cv.text(cx, 175, eq,
            size=cv.fit_size([eq], FW - 70, 15, weight="bold"),
            color=NAVY, weight="bold")

    CASE = [("よくある状況", "MAP 80", "CSF 15", 65, GREY, "#f2f4f6"),
            ("MAP を上げる", "MAP 90", "CSF 15", 75, BLUE, "#eaf1f8"),
            ("髄液を抜く", "MAP 80", "CSF 10", 70, GREEN, "#eaf5ee"),
            ("両方やる", "MAP 90", "CSF 10", 80, RED, "#fceeec")]
    w = (W - 140 - 90) / 4
    for i, (t, m, c, s, col, fc) in enumerate(CASE):
        x = 70 + (w + 30) * i
        cv.box(x, 280, w, 300, fc="#ffffff", ec=col, lw=1.8, radius=10)
        cv.box(x, 280, w, 52, fc=col, ec=col, lw=0, radius=10)
        ts = cv.fit_size([t], w - 30, 11.4, weight="bold")
        cv.text(x + w / 2, 306, t, size=ts, color="white", weight="bold")
        cv.text(x + w / 2, 372, m, size=12.6, color=INK)
        cv.text(x + w / 2, 410, "－", size=12, color=GREY)
        cv.text(x + w / 2, 444, c, size=12.6, color=INK)
        cv.ax.plot([x + 40, x + w - 40], [478, 478], color=col, lw=1.6)
        vtxt = "%d mmHg" % s
        cv.text(x + w / 2, 524, vtxt,
                size=cv.fit_size([vtxt], w - 46, 20, weight="bold"),
                color=col, weight="bold")
        cv.rect(x + 30, 556, (w - 60) * s / 100.0, 12, fc=fc)

    th = textbox(cv, 70, 620, W - 140,
                 ["MAP を 10 上げても、CSF 圧を 5 下げても、SCPP は上がる。",
                  "つまり脊髄保護には、循環側と髄液側の二つの入口がある。",
                  "そして髄液圧は、体位・咳・吸引・ドレーンの高さで簡単に変わる。"],
                 10.8, style="navy", pad_y=16)

    msg(cv, 620 + th + 28,
        "「血圧を上げる」と「髄液を抜く」は、同じ引き算の両側である")
    cv.save(P("h03_scpp.png"))
    crop_bottom(P("h03_scpp.png"))


# ---------------------------------------------------------------- h04
def h04():
    """遠位灌流の限界"""
    cv = Canvas(W, 900)
    cap(cv, 44, "遠位大動脈灌流は、脊髄の下の方にしか届かない")

    # 脊髄の縦断
    x0, y0, bw, bh = 250, 150, 120, 520
    cv.rect(x0, y0, bw, bh, fc="#eef1f5", ec="#b9c2cc", lw=1.4)
    SEG = [("C1〜Th7", 0.0, 0.42, "5%", RED, "#fceeec"),
           ("Th8〜L2", 0.42, 0.30, "24%", ORANGE, "#fdf3e3"),
           ("遠位（腰仙部）", 0.72, 0.28, "480%", GREEN, "#eaf5ee")]
    for lab, p, hp, val, col, fc in SEG:
        yy = y0 + bh * p
        hh = bh * hp
        cv.rect(x0, yy, bw, hh, fc=fc, ec=col, lw=1.6)
        cv.text(x0 - 20, yy + hh / 2, lab, size=10.4, color=INK, ha="right")
        cv.box(x0 + bw + 60, yy + hh / 2 - 34, 260, 68, fc="#ffffff", ec=col,
               lw=1.8, radius=8)
        cv.text(x0 + bw + 190, yy + hh / 2 - 12, val, size=16, color=col,
                weight="bold")
        sub = "ベースライン比の血流"
        cv.text(x0 + bw + 190, yy + hh / 2 + 18, sub,
                size=cv.fit_size([sub], 230, 8.8), color=GREY)
        cv.arrow((x0 + bw + 4, yy + hh / 2), (x0 + bw + 56, yy + hh / 2),
                 color=col, lw=2.0, head=9)

    textbox(cv, x0 + bw + 360, 190, W - 70 - (x0 + bw + 360),
            ["遠位大動脈灌流を行うと、",
             "腰仙部はベースラインの約 480% まで過灌流になる一方、",
             "上位胸髄（C1〜Th7）にはわずか 5%、",
             "中位（Th8〜L2）にも 24% しか届かなかった。",
             "",
             "さらに、髄液圧を上げる実験を加えても、",
             "遠位灌流はその影響を打ち消せなかった。"],
            10.5, style="red", title="ブタ実験が示したこと",
            title_color=RED, pad_y=16)

    msg(cv, 720,
        "遠位灌流があるから安心、ではない。上位胸髄は別の手段で守るしかない",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("h04_distal_perfusion.png"))
    crop_bottom(P("h04_distal_perfusion.png"))


# ---------------------------------------------------------------- h05
def h05():
    """脊髄保護バンドル"""
    cv = Canvas(W, 960)
    cap(cv, 44, "脊髄保護は、一つの手技ではなく束である")

    cx = W / 2
    HW = 620
    cv.box(cx - HW / 2, 120, HW, 80, fc="#0f6d78", ec="#0f6d78", lw=0,
           radius=10)
    ht = "脊髄灌流圧を保ち、酸素を届ける"
    cv.text(cx, 160, ht,
            size=cv.fit_size([ht], HW - 60, 13.4, weight="bold"),
            color="white", weight="bold")

    B = [("MAP を上げる", BLUE, "#eaf1f8",
          ["昇圧薬・輸液・心拍出量", "目標は術式と施設基準で決める"]),
         ("CSF 圧を下げる", GREEN, "#eaf5ee",
          ["髄液ドレナージ", "過剰排液は合併症になる"]),
         ("酸素を運ぶ", PURPLE, "#f1ecf8",
          ["Hb と SpO2", "貧血は SCI の危険因子"]),
         ("血流路を残す", ORANGE, "#fdf3e3",
          ["分節動脈の再建", "左鎖骨下動脈の再建"]),
         ("遠位へ灌流する", TEAL, "#e4f2f4",
          ["左心バイパス・遠位灌流", "ただし上位胸髄には届きにくい"]),
         ("段階に分ける", RED, "#fceeec",
          ["staged repair・MIS2ACE", "側副血行網の再構築を待つ"])]

    w = (W - 140 - 60) / 3
    y = 250
    for i, (t, col, fc, lines) in enumerate(B):
        r, c = divmod(i, 3)
        x = 70 + (w + 30) * c
        yy = y + r * 240
        if r == 0:
            cv.arrow((cx, 204), (x + w / 2, yy - 8), color="#b9c2cc", lw=1.6,
                     head=8)
        card(cv, x, yy, w, t, lines, col, fc, body_size=10.2, lh=1.8)

    textbox(cv, 70, 740, W - 140,
            ["この六つは、どれか一つで足りるものではない。",
             "そしてどれも、単独では確かなエビデンスを持たない。",
             "束として運用し、施設のプロトコルに落とすことが、"
             "実際に発生率を下げている。"],
            10.8, style="navy", pad_y=16)
    cv.save(P("h05_bundle.png"))
    crop_bottom(P("h05_bundle.png"))


# ---------------------------------------------------------------- h06
def h06():
    """術式別の SCI 発生率"""
    cv = Canvas(W, 960)
    cap(cv, 44, "脊髄虚血の頻度は、術式と範囲で桁が変わる")

    ROWS = [("TEVAR・複雑 EVAR（VQI 3,406 件）", 2.3, BLUE,
             "2014 年 4.55% → 2018 年 1.43% へ低下"),
            ("開胸 DTA/TAAA（428 例）", 13.5, RED,
             "早期 2.9% ＋ 遅発性 10.6%"),
            ("分枝・開窓型 EVAR（1,681 例）", 7.1, ORANGE,
             "一過性 3.0% ＋ 永続 4.1%"),
            ("血管内 TAAA 修復（27 研究 2,333 例）", 11.0, PURPLE,
             "extent I・II・III・V は 13%、extent IV は 6%"),
            ("FET（35 研究 3,154 例）", 4.7, GREEN,
             "ステント 15 cm 以上・T8 以遠で増える")]

    y = 140
    bx = 520
    full = (W - 260) - bx
    for lab, val, col, note in ROWS:
        cv.box(70, y, W - 140, 132, fc="#ffffff", ec=col, lw=1.6, radius=10)
        ls = cv.fit_size([lab], 400, 11.0, weight="bold")
        cv.text(94, y + 40, lab, size=ls, color=col, weight="bold", ha="left")
        ns = cv.fit_size([note], 400, 9.6)
        cv.text(94, y + 88, note, size=ns, color=GREY, ha="left")
        cv.rect(bx, y + 48, full, 36, fc="#eef1f5")
        cv.rect(bx, y + 48, full * val / 16.0, 36, fc=col)
        cv.text(W - 100, y + 66, "%.1f%%" % val, size=15, color=col,
                ha="right", weight="bold")
        y += 148

    msg(cv, y + 10,
        "「脊髄虚血は数%」という言い方は、どの手術の話かを決めないと意味がない")
    cv.save(P("h06_sci_rates.png"))
    crop_bottom(P("h06_sci_rates.png"))


# ---------------------------------------------------------------- h07
def h07():
    """遅発性対麻痺のタイムライン"""
    cv = Canvas(W, 960)
    cap(cv, 44, "対麻痺は、手術室を出てから起こることのほうが多い")

    x0, y0 = 110, 180
    pw = W - 220
    cv.ax.plot([x0, x0 + pw], [y0 + 60, y0 + 60], color="#b9c2cc", lw=3)
    MARK = [("手術終了", 0.0, NAVY), ("6 時間", 0.16, ORANGE),
            ("24 時間", 0.42, RED), ("48 時間", 0.62, RED),
            ("110 時間", 0.94, GREY)]
    for lab, p, col in MARK:
        xx = x0 + pw * p
        cv.ax.plot([xx, xx], [y0 + 44, y0 + 76], color=col, lw=3)
        cv.text(xx, y0 + 104, lab, size=10.0, color=col)
    cv.rect(x0 + pw * 0.16, y0 + 20, pw * 0.78, 22, fc="#fceeec")
    cv.text(x0 + pw * 0.55, y0, "遅発性対麻痺が起こりうる時間帯", size=11.0,
            color=RED, weight="bold")
    cv.text(x0 + pw * 0.42, y0 + 140, "中央値 21.6 時間", size=10.4,
            color=RED, weight="bold")

    C = [("発症したときの数字", RED, "#fceeec",
          ["平均 MAP 74 mmHg", "平均 CSF 圧 14 mmHg",
           "つまり SCPP は 60 mmHg 前後"]),
         ("予後（胸腹部大動脈修復）", PURPLE, "#f1ecf8",
          ["30 日死亡 38%（対照 13%）", "5 年生存 28%（対照 75%）",
           "遅発性対麻痺は予後を変える"]),
         ("救済できる可能性", GREEN, "#eaf5ee",
          ["血管内修復 69 例中 12 例が発症", "8 例は回復、永続は 4 例（5.8%）",
           "早く気づけば戻せることがある"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 400, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    textbox(cv, 70, 700, W - 140,
            ["発症時の MAP 74 mmHg は、多くの病棟で「許容範囲」とされる血圧である。",
             "つまり遅発性対麻痺は、"
             "「明らかな低血圧」がなくても起こりうる。",
             "だからこそ、術後も SCPP を意識した目標値が要る。"],
            10.8, style="amber", title="この数字の意味",
            title_color="#9a6510", pad_y=16)
    cv.save(P("h07_delayed_paraplegia.png"))
    crop_bottom(P("h07_delayed_paraplegia.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (h01, h02, h03, h04, h05, h06, h07):
        fn()
        print("ok", fn.__name__)
