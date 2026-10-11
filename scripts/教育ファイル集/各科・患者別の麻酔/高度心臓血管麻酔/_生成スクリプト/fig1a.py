# -*- coding: utf-8 -*-
"""第Ⅰ章 CIED　図版 f01〜f07"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False

W = 1520
TEAL = "#0f6d78"


def P(n):
    return os.path.join(OUT, n)


def cap(cv, y, s, color=NAVY, size=12.5):
    sz = cv.fit_size([s], W - 90, size, weight="bold")
    cv.title(W / 2, y, s, size=sz, ha="center", color=color)


def msg(cv, y, s, fc="#e4f2f4", ec=TEAL, tc=TEAL, size=13.0, x=44, w=None):
    w = w or (W - 88)
    sz = cv.fit_size([s], w - 56, size, weight="bold")
    h = 30 + LH(sz, 1.5)
    cv.box(x, y, w, h, fc=fc, ec=ec, lw=2.0, radius=8)
    cv.text(x + w / 2, y + h / 2, s, size=sz, color=tc, weight="bold")
    return h


def fitlines(cv, lines, w, size, weight="normal", floor=8.4):
    s = cv.fit_size(lines, w, size, min_size=floor, weight=weight)
    if all(cv.width(l, s, weight) <= w for l in lines):
        return s, list(lines)
    out = []
    for l in lines:
        out.extend(cv.wrap(l, w, s, weight))
    return s, out


def card(cv, x, y, w, head, lines, color, fc, head_h=50, body_h=None,
         head_size=11.6, body_size=10.2, lh=1.6):
    hs, hl = fitlines(cv, [head], w - 30, head_size, weight="bold", floor=8.8)
    head_h = max(head_h, 18 + LH(hs, 1.45) * len(hl))
    cv.box(x, y, w, head_h, fc=color, ec=color, lw=0, radius=8)
    cv.block(x, y + (head_h - LH(hs, 1.45) * len(hl)) / 2, w, hl, hs,
             color="white", weight="bold")
    s, bl = fitlines(cv, lines, w - 36, body_size)
    bh = body_h or (26 + LH(s, lh) * len(bl))
    cv.box(x, y + head_h + 9, w, bh, fc=fc, ec=color, lw=1.7, radius=8)
    for j, ln in enumerate(bl):
        cv.text(x + w / 2, y + head_h + 9 + 13 + LH(s, lh) * (j + 0.5), ln,
                size=s, color=INK)
    return head_h + 9 + bh


# ---------------------------------------------------------------- f01
def f01():
    """CIED患者に対する8つの問い"""
    cv = Canvas(W, 900)
    cap(cv, 44, "CIED を「機械」ではなく「患者＋デバイス」として読む")

    cx, cy = W / 2, 470
    BW = 380
    cv.box(cx - BW / 2, cy - 62, BW, 124, fc="#0f6d78", ec="#0f6d78",
           lw=0, radius=10)
    cl = ["CIED が入っている患者が", "手術に来た"]
    cs = cv.fit_size(cl, BW - 46, 13.5, weight="bold")
    cv.block(cx - BW / 2, cy - LH(cs, 1.5), BW, cl, cs, color="white",
             weight="bold", lh=LH(cs, 1.5))

    Q = [("① 何のデバイスか", ["PM / ICD / CRT-P / CRT-D", "S-ICD / leadless / EV-ICD"], BLUE),
         ("② なぜ入っているか", ["房室ブロック・洞不全", "VT/VF・低心機能"], BLUE),
         ("③ ペーシング依存か", ["自己調律はあるか", "止まると何が起こるか"], RED),
         ("④ 電池と最終チェック", ["残量・最終interrogation", "遠隔モニタリングの有無"], GREEN),
         ("⑤ magnet で何が起きるか", ["機種で違う", "止まるのは頻拍治療だけか"], RED),
         ("⑥ 手術部位はどこか", ["generator との距離", "電流の通り道"], ORANGE),
         ("⑦ EMI は起きそうか", ["モノポーラか", "対極板はどこか"], ORANGE),
         ("⑧ 術後に誰が戻すか", ["interrogation の予約", "戻すまでの監視"], PURPLE)]

    xs = [60, 60, 60, 60, W - 60 - 330, W - 60 - 330, W - 60 - 330,
          W - 60 - 330]
    ys = [130, 320, 510, 700, 130, 320, 510, 700]
    for (t, lines, col), x, y in zip(Q, xs, ys):
        textbox(cv, x, y, 330, lines, 10.0, title=t, title_size=11.4,
                title_color=col, fc="#ffffff", ec=col, lw=1.8, pad_y=12)
        p0 = (x + 330, y + 60) if x < W / 2 else (x, y + 60)
        p1 = (cx - BW / 2 - 4, cy) if x < W / 2 else (cx + BW / 2 + 4, cy)
        cv.arrow(p0, p1, color="#b9c2cc", lw=1.5, head=8)

    cv.save(P("f01_eight_questions.png"))


# ---------------------------------------------------------------- f02
def f02():
    """PM と ICD の機能の違い"""
    cv = Canvas(W, 850)
    cap(cv, 44, "ペースメーカーと ICD は別の機械である")

    rows = [("徐脈を感知してペーシングする", "○", "○"),
            ("VT/VF を検出する", "×", "○"),
            ("抗頻拍ペーシング（ATP）を行う", "×", "○"),
            ("ショックを与える", "×", "○"),
            ("magnet を置くと", "多くは非同期ペーシング", "頻拍治療の停止のみ"),
            ("ペーシング依存なら", "非同期化で守れる", "magnet では守れない")]

    x0, y0 = 80, 150
    wl, wc = 560, 380
    hh = 60
    cv.box(x0, y0, wl, hh, fc="#eef1f5", ec="#c9d2dc", lw=1.4, radius=6)
    cv.text(x0 + wl / 2, y0 + hh / 2, "機能", size=12, color=NAVY,
            weight="bold")
    cv.box(x0 + wl, y0, wc, hh, fc="#eaf1f8", ec=BLUE, lw=1.6, radius=6)
    cv.text(x0 + wl + wc / 2, y0 + hh / 2, "ペースメーカー", size=12,
            color=BLUE, weight="bold")
    cv.box(x0 + wl + wc, y0, wc, hh, fc="#fceeec", ec=RED, lw=1.6, radius=6)
    cv.text(x0 + wl + wc * 1.5, y0 + hh / 2, "ICD", size=12, color=RED,
            weight="bold")

    y = y0 + hh + 10
    for i, (lab, a, b) in enumerate(rows):
        h = 78
        bg = "#ffffff" if i % 2 == 0 else "#fafbfc"
        cv.box(x0, y, wl, h, fc=bg, ec="#dde3ea", lw=1.2, radius=6)
        s = cv.fit_size([lab], wl - 36, 11.0)
        cv.text(x0 + wl / 2, y + h / 2, lab, size=s, color=INK)
        for j, (txt, col, fc) in enumerate([(a, BLUE, "#f7fafd"),
                                            (b, RED, "#fdf6f5")]):
            cv.box(x0 + wl + wc * j, y, wc, h, fc=fc, ec="#dde3ea", lw=1.2,
                   radius=6)
            big = txt in ("○", "×")
            s2 = 20 if big else cv.fit_size([txt], wc - 30, 10.6)
            cv.text(x0 + wl + wc * j + wc / 2, y + h / 2, txt, size=s2,
                    color=col if big else INK,
                    weight="bold" if big else "normal")
        y += h + 8

    msg(cv, y + 14, "「ICD に magnet を置けばペースメーカーが非同期になる」は誤り",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("f02_pm_vs_icd.png"))


# ---------------------------------------------------------------- f03
def f03():
    """CRT-P と CRT-D のリード配置"""
    cv = Canvas(W, 860)
    cap(cv, 44, "リードが何本あり、どこに入っているか")

    PW, PX0, PY = 680, 70, 130
    PH = 596

    def panel(x, title, color, has_shock, note):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.text(x + PW / 2, PY + 34, title, size=12.4, color=color,
                weight="bold")
        # 本体
        gx, gy = x + 40, PY + 146
        cv.box(gx, gy, 158, 104, fc="#dbe4ee", ec=NAVY, lw=1.8, radius=8)
        cv.block(gx, gy + 52 - LH(10.0, 1.45), 158, ["本体", "（鎖骨下）"], 10.0,
                 color=NAVY, weight="bold")
        if has_shock:
            cv.text(gx + 79, gy + 126, "ショック機能あり", size=9.4, color=RED,
                    weight="bold")
        # 3つの部屋
        CH = [("右房リード（RA）", "右房", BLUE, 0),
              ("右室リード（RV）", "右室", GREEN, 1),
              ("左室リード（LV）※冠静脈洞経由", "左室", PURPLE, 2)]
        bx = x + 330
        for lab, room, col, i in CH:
            by = PY + 92 + 108 * i
            cv.box(bx, by, 260, 74, fc="#f4f6f9", ec=col, lw=1.6, radius=8)
            cv.text(bx + 130, by + 26, room, size=11.0, color=col,
                    weight="bold")
            ls = cv.fit_size([lab], 244, 9.2)
            cv.text(bx + 130, by + 54, lab, size=ls, color=GREY)
            cv.arrow((gx + 132, gy + 46), (bx - 6, by + 37), color=col,
                     lw=2.0, head=9)
        s2, bl = fitlines(cv, note, PW - 60, 10.4)
        for j, ln in enumerate(bl):
            cv.text(x + PW / 2, PY + 432 + LH(s2, 1.62) * (j + 0.5), ln,
                    size=s2, color=INK)

    panel(PX0, "CRT-P（両室ペーシング）", BLUE, False,
          ["徐脈ペーシングと両室同期のみを行う",
           "ショック機能はない",
           "magnet 応答はペースメーカーに準じる"])
    panel(W - PX0 - PW, "CRT-D（除細動機能つき）", RED, True,
          ["両室ペーシングに加えて VT/VF を治療する",
           "magnet で止まるのは頻拍治療だけである",
           "ペーシング依存なら再プログラミングを考える"])

    msg(cv, PY + PH + 30,
        "見た目は同じ3本リードでも、magnet を置いたときに起こることはまったく違う")
    cv.save(P("f03_crt.png"))


# ---------------------------------------------------------------- f04
def f04():
    """右室心尖部ペーシングと伝導系ペーシング"""
    cv = Canvas(W, 860)
    cap(cv, 44, "どこを刺激しているかで、心室の動き方が変わる")

    PW, PY, PH = 640, 130, 560

    def panel(x, title, color, lines, mode):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        ts = cv.fit_size([title], PW - 50, 12.2, weight="bold")
        cv.text(x + PW / 2, PY + 34, title, size=ts, color=color,
                weight="bold")
        cx, cy = x + PW / 2, PY + 210
        cv.box(cx - 150, cy - 120, 300, 250, fc="#f4f6f9", ec="#c9d2dc",
               lw=1.4, radius=36)
        cv.text(cx, cy - 138, "心室", size=9.6, color=GREY)
        if mode == "apex":
            sx, sy = cx - 34, cy + 92
            cv.text(sx, sy + 24, "右室心尖部", size=9.6, color=color,
                    weight="bold")
            for dx, dy in ((-96, -64), (-52, -118), (18, -140), (86, -104),
                           (110, -46)):
                cv.arrow((sx, sy), (sx + dx, sy + dy), color="#b9c2cc",
                         lw=1.6, head=8)
            cv.text(cx + 72, cy - 96, "順に伝わる", size=9.2, color=GREY)
        else:
            sx, sy = cx - 16, cy - 10
            cv.text(sx - 6, sy - 34, "中隔・左脚領域", size=9.6, color=color,
                    weight="bold")
            for dx, dy in ((-108, 46), (-86, 96), (0, 116), (92, 96),
                           (112, 42)):
                cv.arrow((sx, sy), (sx + dx, sy + dy), color="#b9c2cc",
                         lw=1.6, head=8)
            cv.text(cx + 80, cy + 104, "ほぼ同時", size=9.2, color=GREY)
        cv.rect(sx - 7, sy - 7, 14, 14, fc=color)
        s2, bl = fitlines(cv, lines, PW - 56, 10.4)
        for j, ln in enumerate(bl):
            cv.text(x + PW / 2, PY + 392 + LH(s2, 1.66) * (j + 0.5), ln,
                    size=s2, color=INK)

    panel(70, "従来の右室心尖部ペーシング", GREEN,
          ["刺激は心筋の中をじわじわ伝わって広がる",
           "左脚ブロック型の幅の広い QRS になる",
           "長期には心機能低下をきたすことがある"], "apex")
    panel(W - 70 - PW, "伝導系ペーシング（His 束・左脚領域）", PURPLE,
          ["本来の伝導系に乗せて刺激を広げる",
           "QRS 幅が保たれる",
           "MELOS 研究 2533 例での成功率は徐脈適応 92.4%"], "csp")

    textbox(cv, 70, PY + PH + 26, W - 140,
            ["麻酔科にとっての意味は「どちらが優れているか」ではない。",
             "植込み様式が何であれ、止まったときに何が起こるかを先に決めておくことである。"],
            10.6, style="navy", pad_y=14)
    cv.save(P("f04_csp.png"))


# ---------------------------------------------------------------- f05
def f05():
    """経静脈リードを持たないデバイス"""
    cv = Canvas(W, 900)
    cap(cv, 44, "経静脈リードを持たない三つのデバイス")

    D = [("leadless ペースメーカー", GREEN, "#eaf5ee",
          ["右室内に留置する本体一体型", "経静脈リードがない",
           "magnet に反応しない機種がある", "＝ magnet では守れないことがある"]),
         ("S-ICD（皮下植込み型 ICD）", BLUE, "#eaf1f8",
          ["リードは胸骨左縁の皮下", "心臓内に電極がない",
           "徐脈ペーシングはできない", "magnet で頻拍治療を止められる"]),
         ("EV-ICD（血管外 ICD）", PURPLE, "#f1ecf8",
          ["リードを胸骨下に留置する", "ATP と間欠的ペーシングが可能",
           "除細動成功率 98.7%（pivotal 試験）", "血管内リードの合併症を避ける"])]

    w = 430
    gap = (W - 140 - w * 3) / 2
    for i, (t, col, fc, lines) in enumerate(D):
        x = 70 + (w + gap) * i
        card(cv, x, 130, w, t, lines, col, fc, body_size=10.4, lh=1.75)

    th = textbox(cv, 70, 500, W - 140,
            ["これらは「新しいから難しい」のではなく、",
             "従来の前提（magnet を置けば非同期になる・ペーシングができる）が",
             "そのまま通用しないから難しい。",
             "術前に機種を特定できなければ、magnet を当てにした計画は立てられない。"],
            10.8, style="amber", pad_y=16)

    msg(cv, 500 + th + 28,
        "S-ICD と leadless PM は、外部除細動と体外ペーシングの準備を先に決める",
        fc="#fdf3e3", ec=ORANGE, tc="#9a6510")
    cv.save(P("f05_nontransvenous.png"))


# ---------------------------------------------------------------- f06
def f06():
    """EMI の電流経路"""
    cv = Canvas(W, 980)
    cap(cv, 44, "電気メスの電流は、どこを通って帰るのか")

    # 患者の輪郭
    cv.box(230, 150, W - 460, 420, fc="#f7f9fb", ec="#c9d2dc", lw=1.6,
           radius=26)
    cv.text(258, 176, "患者", size=11.0, color=GREY, ha="left")

    # generator と lead
    cv.box(330, 250, 130, 70, fc="#dbe4ee", ec=NAVY, lw=1.8, radius=8)
    cv.text(395, 285, "本体", size=10.4, color=NAVY, weight="bold")
    cv.box(620, 300, 190, 150, fc="#fceeec", ec=RED, lw=1.8, radius=30)
    cv.text(715, 375, "心臓", size=11.0, color=RED, weight="bold")
    cv.arrow((460, 285), (628, 336), color=NAVY, lw=2.2, head=9, style="-")
    cv.text(544, 276, "リード", size=9.6, color=NAVY)

    # active electrode → 対極板
    cv.box(880, 190, 210, 62, fc="#fdf3e3", ec=ORANGE, lw=1.8, radius=8)
    cv.text(985, 221, "電気メス先端", size=10.6, color="#9a6510", weight="bold")
    cv.box(880, 480, 210, 62, fc="#fdf3e3", ec=ORANGE, lw=1.8, radius=8)
    cv.text(985, 511, "対極板", size=10.6, color="#9a6510", weight="bold")
    cv.arrow((985, 254), (985, 476), color=ORANGE, lw=3.0, head=13)
    cv.text(1105, 365, "本来の電流路", size=10.4, color="#9a6510",
            weight="bold")

    # 望ましくない経路
    cv.arrow((944, 258), (802, 332), color=RED, lw=2.4, head=11)
    cv.arrow((626, 392), (470, 314), color=RED, lw=2.4, head=11)
    cv.text(560, 206, "避けたい経路（本体・リードを横切る）", size=10.6,
            color=RED, weight="bold")

    textbox(cv, 70, 630, (W - 160) / 2,
            ["電流路が本体とリードを横切ると", "EMI が起きる",
             "＝ 手術部位そのものより、", "電流の通り道で決まる"],
            10.8, style="red", title="何がリスクを決めるのか",
            title_color=RED, pad_y=14)
    textbox(cv, 90 + (W - 160) / 2, 630, (W - 160) / 2,
            ["対極板を術野の反対側に置き、", "本体・リードを結ぶ線から外す",
             "モノポーラをバイポーラに替える", "凝固よりも短い通電にする"],
            10.8, style="green", title="できる対策", title_color=GREEN,
            pad_y=14)
    cv.save(P("f06_emi_path.png"))


# ---------------------------------------------------------------- f07
def f07():
    """手術部位別の EMI 発生率"""
    cv = Canvas(W, 900)
    cap(cv, 44, "「臍より上か下か」は目安であって、境界線ではない")

    # 左：Schulman 2019（ICD、実測）
    x0, y0 = 70, 140
    w = (W - 170) / 2
    PH = 520
    cv.box(x0, y0, w, PH, fc="#ffffff", ec=BLUE, lw=1.8, radius=10)
    t1 = ["ICD 患者で実測した EMI", "（Schulman 2019, Anesthesiology）"]
    s1 = cv.fit_size(t1, w - 50, 11.4, weight="bold")
    cv.block(x0, y0 + 16, w, t1, s1, color=BLUE, weight="bold")
    BARS = [("臍より上の手術（n=70）", 20.0, 7),
            ("臍より下の手術（n=40）", 2.5, 0),
            ("心臓手術（n=34）", 68.0, 29)]
    by = y0 + 142
    full = w - 48
    for lab, a, b in BARS:
        cv.text(x0 + 24, by, lab, size=10.2, color=INK, ha="left")
        cv.rect(x0 + 24, by + 18, full, 28, fc="#eef1f5")
        cv.rect(x0 + 24, by + 18, full * a / 100.0, 28, fc="#9fc0e0")
        cv.rect(x0 + 24, by + 18, full * b / 100.0, 28, fc=BLUE)
        cl2 = "EMI %.1f%%　／　うち臨床的に問題となったもの %d%%" % (a, b)
        cv.text(x0 + 24, by + 64, cl2,
                size=cv.fit_size([cl2], full, 9.6), color=GREY, ha="left")
        by += 118
    fn = "淡い帯＝EMI 全体　　濃い帯＝臨床的に問題となったもの"
    cv.text(x0 + 24, y0 + PH - 30, fn,
            size=cv.fit_size([fn], full, 9.2), color=GREY, ha="left")

    # 右：ICD-ON レジストリ
    x1 = x0 + w + 30
    cv.box(x1, y0, w, PH, fc="#ffffff", ec=GREEN, lw=1.8, radius=10)
    t2 = ["術野別の EMI 発生", "（ICD-ON レジストリ 331 例）"]
    s2 = cv.fit_size(t2, w - 50, 11.4, weight="bold")
    cv.block(x1, y0 + 16, w, t2, s2, color=GREEN, weight="bold")
    B2 = [("胸部", 45), ("頭頸部", 35), ("上肢", 15), ("腸骨稜より上の腹部", 3)]
    lw2 = max(cv.width(l, 10.2) for l, _ in B2) + 34
    by = y0 + 116
    for lab, a in B2:
        cv.text(x1 + 24, by + 14, lab, size=10.2, color=INK, ha="left")
        bx = x1 + 24 + lw2
        bw = w - 48 - lw2 - 80
        cv.rect(bx, by, bw, 28, fc="#eef1f5")
        cv.rect(bx, by, bw * a / 100.0, 28, fc=GREEN)
        cv.text(x1 + w - 28, by + 14, "%d%%" % a, size=10.4, color=GREEN,
                ha="right", weight="bold")
        by += 86

    textbox(cv, 70, y0 + PH + 26, W - 140,
            ["頭頸部で 35%、上肢で 15% に EMI が出ている。",
             "「臍より上ならとりあえず magnet」という言い方は、この数字を説明できない。",
             "見るべきは部位ではなく、本体・リードと電流路の位置関係である。"],
            10.8, style="navy", pad_y=14)
    cv.save(P("f07_emi_by_site.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f01, f02, f03, f04, f05, f06, f07):
        fn()
        print("ok", fn.__name__)
