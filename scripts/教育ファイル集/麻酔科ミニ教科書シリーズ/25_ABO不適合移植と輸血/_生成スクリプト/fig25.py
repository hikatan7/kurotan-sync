# -*- coding: utf-8 -*-
"""㉕ ABO不適合移植と輸血　図版 f01〜f15"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False

W = 1520
AG = "#b3541e"          # 抗原の色
AB = "#2e6da4"          # 抗体の色
OK = "#1f7f4f"
NG = "#b3261e"
SOFT = "#f2f4f6"


def P(n):
    return os.path.join(OUT, n)


def cap(cv, y, s, color=NAVY, size=12.5):
    """図の見出し（幅に収まるまで縮小）"""
    sz = cv.fit_size([s], W - 90, size, weight="bold")
    cv.title(W / 2, y, s, size=sz, ha="center", color=color)


def msg(cv, y, s, fc="#e4f2f4", ec="#0f6d78", tc="#0f6d78", size=11.5,
        x=44, w=None):
    w = w or (W - 88)
    sz = cv.fit_size([s], w - 56, size, weight="bold")
    h = 30 + LH(sz, 1.5)
    cv.box(x, y, w, h, fc=fc, ec=ec, lw=2.0, radius=8)
    cv.text(x + w / 2, y + h / 2, s, size=sz, color=tc, weight="bold")
    return h


# ---------------------------------------------------------------- f01
def f01():
    cv = Canvas(W, 700)
    cap(cv, 44, "「O 型」という一語は、二つの独立した事実を畳み込んでいる")

    L, BW, TOP = 470, 520, 126
    h1 = textbox(cv, L, TOP, BW,
                 ["赤血球膜に A 抗原も B 抗原もない",
                  "（未修飾の H 抗原が残っている）"],
                 11.2, fc="#fdf1ea", ec=AG, title="事実 ①　抗原について",
                 title_color=AG, lw=2.0)
    y2 = TOP + h1 + 20
    h2 = textbox(cv, L, y2, BW,
                 ["血漿中に抗 A と抗 B が存在する",
                  "（主体は IgM。補体を強力に起動する）"],
                 11.2, fc="#eaf1f8", ec=AB, title="事実 ②　抗体について",
                 title_color=AB, lw=2.0)
    BOT = y2 + h2

    cy = (TOP + BOT) / 2
    cv.box(60, cy - 100, 300, 200, fc="#eef1f6", ec=NAVY, lw=2.4, radius=10)
    cv.text(210, cy - 38, "O 型", size=34, color=NAVY, weight="bold")
    cv.text(210, cy + 22, "（血液型ラベル）", size=11, color=GREY)
    cv.text(210, cy + 58, "圧縮ファイル", size=11.5, color="#0f6d78",
            weight="bold")
    cv.arrow((372, cy), (452, TOP + h1 / 2), color=GREY, lw=2.4, head=13)
    cv.arrow((372, cy), (452, y2 + h2 / 2), color=GREY, lw=2.4, head=13)

    RX, RW = 1026, 434
    inner = RW - 48
    A = ["ランドシュタイナーの法則", "── 自分が持たない抗原に",
         "　　対する抗体を必ず持つ"]
    B = ["この対応があるから、", "一文字で両方を言い表せる"]
    sa = cv.fit_size(A + B, inner, 10.6)
    st = cv.fit_size(["二つを結んでいるもの"], inner, 11.5, weight="bold")
    lh, tlh = LH(sa, 1.5), LH(st, 1.5)
    rh = 24 + tlh + lh * len(A) + 34 + lh * len(B) + 24
    cv.box(RX, TOP, RW, max(rh, BOT - TOP), fc="white", ec=GREY, lw=1.6,
           radius=8)
    y = TOP + 24 + (max(rh, BOT - TOP) - rh) / 2
    cv.text(RX + RW / 2, y + tlh / 2, "二つを結んでいるもの", size=st,
            color=NAVY, weight="bold")
    y += tlh
    for i, ln in enumerate(A):
        cv.text(RX + RW / 2, y + lh * (i + 0.5), ln, size=sa, color=INK)
    y += lh * len(A) + 17
    cv.ax.plot([RX + 40, RX + RW - 40], [y, y], color=GREY, lw=1.2, ls=":")
    y += 17
    for i, ln in enumerate(B):
        cv.text(RX + RW / 2, y + lh * (i + 0.5), ln, size=sa, color="#0f6d78")

    m1 = msg(cv, BOT + 34,
             "展開の前提 ── 体内にある「ABO 抗原を持つ領域」は、"
             "患者自身の赤血球ただ一つである")
    msg(cv, BOT + 34 + m1 + 16,
        "ABO 不適合移植は、この前提を壊す ── "
        "グラフト内皮という第二の抗原領域が加わる",
        fc="#fceeec", ec=NG, tc=NG)
    cv.save(P("f01_label_compression.png"))


# ---------------------------------------------------------------- f02
def f02():
    cv = Canvas(W, 600)
    cap(cv, 44, "ABO 遺伝子が作るのは抗原ではなく酵素である")

    def chain(cx, y, label, sub, color, fc, ec):
        cv.box(cx - 145, y - 90, 290, 180, fc=fc, ec=ec, lw=1.8, radius=8)
        cv.text(cx, y - 48, label, size=11.6, color=ec, weight="bold")
        x0 = cx - 30
        for i in range(3):
            cv.ax.add_patch(Circle((x0 + i * 30, y), 12,
                                   facecolor="#dfe5ec", edgecolor=GREY,
                                   lw=1.2, zorder=4))
        cv.ax.add_patch(Circle((x0 + 60, y), 14, facecolor=color,
                               edgecolor=color, lw=1.2, zorder=5))
        s = cv.fit_size([sub], 250, 9.8)
        cv.text(cx, y + 54, sub, size=s, color=GREY)

    chain(175, 200, "前駆糖鎖", "末端にフコースなし", "#dfe5ec",
          SOFT, GREY)
    GAP0, GAP1 = 330, 480
    cv.arrow((GAP0, 200), (GAP1, 200), color=GREY, lw=2.4, head=13)
    gw = GAP1 - GAP0 - 8
    gc = (GAP0 + GAP1) / 2
    cv.text(gc, 168, "FUT1", size=cv.fit_size(["FUT1"], gw, 10.6,
                                              weight="bold"),
            color=PURPLE, weight="bold")
    cv.text(gc, 234, "（H 遺伝子）",
            size=cv.fit_size(["（H 遺伝子）"], gw, 9.4), color=GREY)
    chain(630, 200, "H 抗原", "末端にフコースが付く", PURPLE,
          "#f6f1fa", PURPLE)

    BX, BW = 980, 460
    for cy, enzyme, out, note, color, fc in (
        (190, "A 型の酵素が GalNAc を付加", "A 抗原", "血漿には抗 B がある",
         AG, "#fdf1ea"),
        (330, "B 型の酵素がガラクトースを付加", "B 抗原",
         "血漿には抗 A がある", GREEN, "#eaf5ee"),
        (470, "機能する酵素がなく、何も付かない", "H 抗原のまま（O 型）",
         "血漿には抗 A と抗 B がある", GREY, SOFT),
    ):
        cv.arrow((781, 200), (964, cy), color=GREY, lw=2.2, head=12)
        cv.box(BX, cy - 56, BW, 112, fc=fc, ec=color, lw=1.9, radius=8)
        s = cv.fit_size([enzyme, note], BW - 56, 10.2)
        cv.text(BX + BW / 2, cy - 30, enzyme, size=s, color=GREY)
        so = cv.fit_size([out], BW - 56, 14.5, weight="bold")
        cv.text(BX + BW / 2, cy + 4, out, size=so, color=color, weight="bold")
        cv.text(BX + BW / 2, cy + 36, note, size=s, color=INK)

    cv.save(P("f02_abo_biosynthesis.png"))


# ---------------------------------------------------------------- f03
def f03():
    cv = Canvas(W, 790)
    cap(cv, 44, "抗原がどこに出ているか ── ABO と RhD を並べる")

    ROWS = [
        ("赤血球", True, True, "どちらも発現する"),
        ("血管内皮", True, False, "ここが移植の成否を分ける"),
        ("消化管・尿路上皮", True, False, "─"),
        ("外分泌腺・分泌液", True, False, "分泌型では可溶性抗原になる"),
        ("腎実質・肝実質", True, False, "─"),
    ]
    X0, XA, XB, XN = 70, 470, 660, 850
    cv.box(60, 96, W - 120, 56, fc="#eef1f6", ec=NAVY, lw=0, radius=7)
    cv.text(X0 + 150, 124, "抗原が発現している場所", size=11.2, color=NAVY,
            weight="bold")
    cv.text(XA + 60, 124, "ABO", size=11.8, color=AG, weight="bold")
    cv.text(XB + 60, 124, "RhD", size=11.8, color=BLUE, weight="bold")
    cv.text(XN + 280, 124, "備考", size=11.2, color=NAVY, weight="bold")

    for i, (name, a, b, note) in enumerate(ROWS):
        y = 176 + i * 62
        if i % 2 == 0:
            cv.rect(60, y - 24, W - 120, 56, fc="#fafbfc")
        cv.text(X0, y + 4, name, size=11.0, color=INK, ha="left")
        for x, on, c in ((XA + 60, a, AG), (XB + 60, b, BLUE)):
            if on:
                cv.ax.add_patch(Circle((x, y + 4), 13, facecolor=c,
                                       edgecolor=c, zorder=5))
                cv.text(x, y + 4, "●", size=0.1, color=c)
            else:
                cv.ax.add_patch(Circle((x, y + 4), 13, facecolor="white",
                                       edgecolor="#c3cad3", lw=1.8, zorder=5))
                cv.text(x, y + 5, "―", size=11, color="#9aa4b0")
        cv.text(XN, y + 4, note, size=10.2, color=GREY, ha="left")

    y = 176 + len(ROWS) * 62 + 6
    ha = textbox(cv, 60, y, 690,
                 ["糖転移酵素の産物なので、",
                  "酵素が働く細胞すべてに出る"],
                 11.0, fc="#fdf1ea", ec=AG,
                 title="ABO ── 全身の細胞にある糖鎖",
                 title_color=AG, lw=2.0)
    hb = textbox(cv, 770, y, 690,
                 ["赤血球系列に限局する膜貫通蛋白。",
                  "内皮には出ない"],
                 11.0, fc="#eaf1f8", ec=BLUE, title="RhD ── 赤血球だけの蛋白",
                 title_color=BLUE, lw=2.0)

    msg(cv, y + max(ha, hb) + 28,
        "移植の壁になるかどうかは、抗体の強さではなく、抗原がどこに発現しているかで決まる")
    cv.save(P("f03_antigen_distribution.png"))


# ---------------------------------------------------------------- f04
def f04():
    cv = Canvas(W, 760)
    cap(cv, 44, "抗原曝露の時間軸 ── 終わりがあるか、ないか")

    PH = 240

    def panel(y, title, color, fc):
        cv.box(60, y, W - 120, PH, fc=fc, ec=color, lw=1.8, radius=9)
        cv.text(88, y + 34, title, size=11.8, color=color, weight="bold",
                ha="left")
        ax0, ax1, base = 330, 1300, y + PH - 58
        cv.ax.plot([ax0, ax1], [base, base], color=GREY, lw=1.6)
        cv.ax.plot([ax0, ax0], [y + 74, base], color=GREY, lw=1.6)
        cv.text(ax0 + 6, base + 26, "移植・輸血", size=9.4, color=GREY,
                ha="left")
        cv.text(ax1, base + 26, "時間", size=9.6, color=GREY)
        cv.text(190, (y + 74 + base) / 2, "体内の\n不適合抗原量", size=9.8,
                color=GREY)
        return ax0, ax1, base

    TOP1 = 110
    ax0, ax1, base = panel(TOP1,
                           "不適合赤血球の輸血 ── 抗原は有限で、やがて消える",
                           BLUE, "#eaf1f8")
    xs = [ax0, ax0 + 30, ax0 + 90, ax0 + 190, ax0 + 320, ax0 + 470, ax0 + 620]
    ys = [base, base - 100, base - 88, base - 58, base - 28, base - 8, base]
    cv.ax.plot(xs, ys, color=BLUE, lw=3.0, zorder=5)
    cv.ax.fill_between(xs, ys, base, color=BLUE, alpha=0.16, zorder=4)
    cv.text(1140, base - 60, "数日〜数週で曝露は終わる", size=10.8,
            color=BLUE, weight="bold")

    TOP2 = TOP1 + PH + 30
    ax0, ax1, base = panel(TOP2,
                           "ABO 不適合移植 ── 抗原は生着している限り残る",
                           NG, "#fceeec")
    xs = [ax0, ax0 + 30, ax1 - 10]
    ys = [base, base - 92, base - 92]
    cv.ax.plot(xs, ys, color=NG, lw=3.0, zorder=5)
    cv.ax.fill_between(xs, ys, base, color=NG, alpha=0.14, zorder=4)
    cv.text(1000, base - 48, "洗い流すという選択肢が存在しない",
            size=10.8, color=NG, weight="bold")

    msg(cv, TOP2 + PH + 30, "移植とは、二度と洗い流せない輸血である",
        fc="#fceeec", ec=NG, tc=NG, size=13)
    cv.save(P("f04_irreversible.png"))


# ---------------------------------------------------------------- f05
def f05():
    cv = Canvas(W, 740)
    cap(cv, 44, "accommodation ── 危険な窓を通り抜ける")

    X0, X1, TOP, BASE = 200, 1400, 120, 470
    cv.rect(X0 + 150, TOP, 320, BASE - TOP, fc="#fdeceb", z=1)
    cv.text(X0 + 310, TOP + 26, "危険な窓（数週間〜1 か月）", size=10.8,
            color=NG, weight="bold", z=6)
    cv.ax.plot([X0, X1], [BASE, BASE], color=GREY, lw=1.6)
    cv.ax.plot([X0, X0], [TOP, BASE], color=GREY, lw=1.6)
    for x, lab in ((X0, "術前"), (X0 + 150, "移植"), (X0 + 470, "1 か月"),
                   (X0 + 800, "3 か月"), (X1 - 20, "以後")):
        cv.text(x, BASE + 26, lab, size=9.8, color=GREY)

    ax = cv.ax
    ab_x = [X0, X0 + 70, X0 + 150, X0 + 250, X0 + 400, X0 + 620, X0 + 900,
            X1 - 20]
    ab_y = [TOP + 40, TOP + 210, TOP + 280, TOP + 240, TOP + 160, TOP + 105,
            TOP + 80, TOP + 76]
    ax.plot(ab_x, ab_y, color=AB, lw=3.2, zorder=6)
    cv.text(X1, TOP + 34, "抗 A / 抗 B 抗体価　── 脱感作で下げ、やがて戻る",
            size=cv.fit_size(
                ["抗 A / 抗 B 抗体価　── 脱感作で下げ、やがて戻る"],
                620, 11, weight="bold"),
            color=AB, weight="bold", ha="right")

    rk_x = ab_x
    rk_y = [BASE - 6, BASE - 6, TOP + 60, TOP + 92, TOP + 170, TOP + 250,
            TOP + 300, TOP + 306]
    ax.plot(rk_x, rk_y, color=NG, lw=3.2, ls="--", zorder=6)
    cv.text(X0 + 560, TOP + 322, "グラフト傷害のリスク", size=11, color=NG,
            weight="bold", ha="left")

    cd_x = ab_x
    cd_y = [BASE - 4, BASE - 6, BASE - 20, BASE - 60, BASE - 120, BASE - 168,
            BASE - 190, BASE - 192]
    ax.plot(cd_x, cd_y, color=OK, lw=2.6, zorder=6)
    cv.text(X0 + 560, BASE - 214, "CD55・CD59 など内皮側の防御", size=10.6,
            color=OK, weight="bold", ha="left")

    textbox(cv, 60, 520, 690,
            ["抗体も抗原も消えていない。",
             "変わったのは抗原抗体反応の下流である"],
            11.0, fc="#eaf5ee", ec=OK, title="accommodation とは",
            title_color=OK, lw=2.0)
    textbox(cv, 770, 520, 690,
            ["抗体を根絶する治療ではなく、",
             "内皮が自分を守れるようになるまで時間を買う治療"],
            11.0, fc="#fdf3e3", ec=ORANGE, title="だから脱感作の目的は",
            title_color="#9a6410", lw=2.0)
    cv.save(P("f05_accommodation.png"))


# ---------------------------------------------------------------- f06
def f06():
    cv = Canvas(W, 820)
    cap(cv, 44, "A 型ドナー腎を持つ O 型患者 ── 同型輸血が最も危険になる")

    ROWS = [
        ("O 型 FFP", "抗 A と抗 B を含む",
         "抗 A が ② のグラフト内皮を直撃する", NG, "×　同型なのに危険"),
        ("A 型 FFP（ドナー型）", "抗 B のみを含む",
         "抗 B には体内に標的が一つもない", OK, "◎　最適解"),
        ("AB 型 FFP", "抗 A も抗 B も含まない",
         "どこにも結合しない", OK, "○　安全解"),
    ]
    RX, RW, RH, TOP = 480, 660, 132, 110
    for i, (name, has, effect, color, verdict) in enumerate(ROWS):
        y = TOP + i * (RH + 20)
        cv.box(RX, y, RW, RH, fc="white", ec=color, lw=2.0, radius=8)
        cv.text(RX + 24, y + 34, name, size=11.4, color=color, weight="bold",
                ha="left")
        cv.text(RX + 24, y + 74, has, size=10.2, color=GREY, ha="left")
        cv.text(RX + 24, y + 108, effect, size=10.4, color=INK, ha="left")
        cv.arrow((RX + RW + 10, y + RH / 2), (RX + RW + 56, y + RH / 2),
                 color=color, lw=2.2, head=12)
        vs = cv.fit_size([verdict], 290, 11.6, weight="bold")
        cv.text(1340, y + RH / 2, verdict, size=vs, color=color,
                weight="bold")
    RBOT = TOP + 3 * RH + 2 * 20

    cv.text(250, TOP + 36, "この患者の体内", size=11.6, color=NAVY,
            weight="bold")
    iy = TOP + 66
    ih1 = textbox(cv, 84, iy, 332, ["A 抗原も B 抗原もない"], 10.6,
                  fc="white", ec=GREY, title="① 患者の赤血球（O 型）",
                  title_color=GREY, lw=1.5)
    iy2 = iy + ih1 + 18
    ih2 = textbox(cv, 84, iy2, 332, ["A 抗原を発現している"], 10.6,
                  fc="#fdf1ea", ec=AG, title="② グラフト内皮（A 型）",
                  title_color=AG, lw=2.0)
    cv.box(60, TOP, 380, iy2 + ih2 + 24 - TOP, fc="#f7f9fb", ec=NAVY,
           lw=2.0, radius=9, z=0)

    m1 = msg(cv, RBOT + 36,
             "血液型ラベルの照合は「O 型患者に O 型 FFP」を正解と判定する ── "
             "ラベルはもうこの患者を記述していない",
             fc="#fceeec", ec=NG, tc=NG)
    msg(cv, RBOT + 36 + m1 + 16,
        "赤血球は患者を守るために選び、血漿はグラフトを守るために選ぶ")
    cv.save(P("f06_inversion.png"))


# ---------------------------------------------------------------- f07
def f07():
    cv = Canvas(W, 790)
    cap(cv, 44, "適合性の三本の軸 ── 同型輸血はこれを一文字に畳んだ近似解")

    LX, RX, BW, TOP, GAP = 90, 940, 490, 136, 34
    cv.text(LX + BW / 2, 104, "製剤が持ち込むもの", size=11.8, color=NAVY,
            weight="bold")
    cv.text(RX + BW / 2, 104, "体内に存在するもの", size=11.8, color=NAVY,
            weight="bold")

    hA = textbox(cv, LX, TOP, BW, ["赤血球・血小板の膜上"], 10.8,
                 fc="#fdf1ea", ec=AG, title="抗原", title_color=AG, lw=2.0)
    yB = TOP + hA + GAP
    hB = textbox(cv, LX, yB, BW, ["血漿・血小板製剤の浮遊液"], 10.8,
                 fc="#eaf1f8", ec=AB, title="抗体", title_color=AB, lw=2.0)

    h1 = textbox(cv, RX, TOP, BW, ["患者の血漿中の抗 A / 抗 B"], 10.8,
                 fc="#eaf1f8", ec=AB, title="① 患者の抗体", title_color=AB,
                 lw=2.0)
    y2 = TOP + h1 + GAP
    h2 = textbox(cv, RX, y2, BW, ["患者自身の赤血球膜上"], 10.8,
                 fc="#fdf1ea", ec=AG, title="② 患者の抗原", title_color=AG,
                 lw=2.0)
    y3 = y2 + h2 + GAP
    h3 = textbox(cv, RX, y3, BW, ["ドナー抗原を発現した血管内皮"], 10.8,
                 fc="#fdeceb", ec=NG, title="③ グラフトの抗原",
                 title_color=NG, lw=2.0)

    cv.arrow((LX + BW, TOP + hA / 2), (RX, TOP + h1 / 2), color=GREY,
             lw=2.2, head=13)
    cv.text((LX + BW + RX) / 2, TOP + hA / 2 - 26, "第 1 軸　赤血球輸血の軸",
            size=10.6, color=GREY, weight="bold")
    cv.arrow((LX + BW, yB + hB / 2), (RX, y2 + h2 / 2), color=GREY,
             lw=2.2, head=13)
    cv.text((LX + BW + RX) / 2, yB + hB / 2 - 26, "第 2 軸　血漿輸血の軸",
            size=10.6, color=GREY, weight="bold")

    ex, ey = LX + BW / 2, y3 + h3 / 2
    cv.ax.plot([ex, ex], [yB + hB, ey], color=NG, lw=3.0, zorder=3)
    cv.arrow((ex, ey), (RX, ey), color=NG, lw=3.0, head=15)
    cv.text((ex + RX) / 2, ey - 28, "第 3 軸　移植で初めて現れる",
            size=11.4, color=NG, weight="bold")

    yb = y3 + h3 + 34
    m1 = msg(cv, yb, "三本目の軸が、ABO 不適合移植の輸血学のすべてである",
             fc="#fceeec", ec=NG, tc=NG, size=13)
    msg(cv, yb + m1 + 16,
        "近似が成立する前提（体内の抗原領域が一つだけ）が崩れたら、元の三本に戻って数え直す")
    cv.save(P("f07_three_axes.png"))


# ---------------------------------------------------------------- f08
def f08():
    cv = Canvas(W, 940)
    cap(cv, 44, "血小板だけに生じるジレンマ ── 抗原と抗体が同じ袋に入っている")

    TOP = 100
    cv.text(760, TOP + 36, "血小板製剤という「袋」", size=11.6, color=NAVY,
            weight="bold")
    iy = TOP + 66
    h1 = textbox(cv, 584, iy, 352, ["膜に ABO 抗原を発現している"], 10.4,
                 fc="#fdf1ea", ec=AG, title="中身 ①　血小板（抗原）",
                 title_color=AG, lw=1.8)
    iy2 = iy + h1 + 16
    h2 = textbox(cv, 584, iy2, 352, ["抗 A / 抗 B を含む"], 10.4,
                 fc="#eaf1f8", ec=AB, title="中身 ②　ドナー血漿（抗体）",
                 title_color=AB, lw=1.8)
    OUTBOT = iy2 + h2 + 22
    cv.box(560, TOP, 400, OUTBOT - TOP, fc="#f7f9fb", ec=NAVY, lw=2.2,
           radius=10, z=0)

    SY = OUTBOT + 50
    cv.arrow((556, OUTBOT - 40), (400, SY - 12), color=GREY, lw=2.4, head=13)
    cv.arrow((964, OUTBOT - 40), (1120, SY - 12), color=GREY, lw=2.4,
             head=13)

    hL = textbox(cv, 80, SY, 560,
                 ["AB 型・ドナー型を選ぶ",
                  "血漿は無害 → グラフトは守れる",
                  "しかし血小板自身が抗原を持つため",
                  "患者の抗体に捕捉され、増加不良になる"],
                 10.8, fc="#eaf5ee", ec=OK, title="グラフト保護を優先すると",
                 title_color=OK, lw=2.0)
    hR = textbox(cv, 880, SY, 560,
                 ["O 型を選ぶ",
                  "血小板は抗原を持たない → よく上がる",
                  "しかし血漿の抗 A・抗 B が",
                  "グラフト内皮を攻撃する"],
                 10.8, fc="#fceeec", ec=NG, title="血小板数を優先すると",
                 title_color=NG, lw=2.0)

    BOT = SY + max(hL, hR)
    m1 = msg(cv, BOT + 34,
             "原則 ── 可逆な損失（血小板数）より、不可逆な損失（内皮の傷）を避ける")
    msg(cv, BOT + 34 + m1 + 16,
        "洗浄すれば袋の中身を分けられる ── "
        "第 1 軸だけを残して第 3 軸を消す（ただし受注製造。当日には間に合わない）",
        fc="#fdf3e3", ec=ORANGE, tc="#9a6410")
    cv.save(P("f08_platelet_dilemma.png"))


# ---------------------------------------------------------------- f09
def f09():
    cv = Canvas(W, 840)
    cap(cv, 44, "組み合わせ別の製剤選択 ── 三本の軸から機械的に導ける")

    ROWS = [
        ("A → O", "抗 A・抗 B", "O", "A　または　AB", "", "#fafbfc"),
        ("B → O", "抗 A・抗 B", "O", "B　または　AB", "", "white"),
        ("AB → O", "抗 A・抗 B", "O", "AB", "", "#fafbfc"),
        ("AB → A", "抗 B", "A（または O）", "AB", "", "white"),
        ("AB → B", "抗 A", "B（または O）", "AB", "", "#fafbfc"),
        ("A → B", "抗 A", "B（または O）", "AB のみ", "双方向", "#fdeceb"),
        ("B → A", "抗 B", "A（または O）", "AB のみ", "双方向", "#fdeceb"),
    ]
    X = [80, 430, 700, 950, 1310]
    cv.box(60, 96, W - 120, 58, fc="#eef1f6", ec=NAVY, lw=0, radius=7)
    for x, lab in zip(X, ["ドナー → レシピエント", "患者が持つ抗体",
                          "赤血球", "血漿・血小板", "備考"]):
        cv.text(x, 125, lab, size=11.0, color=NAVY, weight="bold", ha="left")

    for i, (combo, abo, rbc, pl, note, bg) in enumerate(ROWS):
        y = 160 + i * 66
        cv.rect(60, y, W - 120, 62, fc=bg)
        cv.text(X[0], y + 32, combo, size=12.0, color=NAVY, weight="bold",
                ha="left")
        cv.text(X[1], y + 32, abo, size=10.6, color=AB, ha="left")
        cv.text(X[2], y + 32, rbc, size=11.0, color=AG, weight="bold",
                ha="left")
        cv.text(X[3], y + 32, pl, size=11.0, color=OK, weight="bold",
                ha="left")
        if note:
            cv.text(X[4], y + 32, note, size=10.4, color=NG, weight="bold",
                    ha="left")

    y = 160 + len(ROWS) * 66 + 14
    textbox(cv, 60, y, 460,
            ["選べるならレシピエント型を優先。", "O 型を反射で選ばない"],
            10.6, fc="#fdf1ea", ec=AG, title="赤血球の列", title_color=AG,
            lw=1.8, min_h=118)
    textbox(cv, 540, y, 460,
            ["左が最適解（ドナー型）、", "右が安全解（AB 型）"],
            10.6, fc="#eaf5ee", ec=OK, title="血漿の列", title_color=OK,
            lw=1.8, min_h=118)
    textbox(cv, 1020, y, 440,
            ["患者の赤血球も守る必要があり、", "AB 型しか残らない"],
            10.6, fc="#fdeceb", ec=NG, title="双方向の 2 行", title_color=NG,
            lw=1.8, min_h=118)
    cv.save(P("f09_matrix.png"))


# ---------------------------------------------------------------- f10
def f10():
    cv = Canvas(W, 660)
    cap(cv, 44, "矢印を逆に向ける ── 抗体関連型拒絶と PLS")

    def panel(x, title, color, fc, combo, src, tgt, tim, organ):
        cv.box(x, 100, 690, 400, fc=fc, ec=color, lw=2.0, radius=9)
        cv.text(x + 345, 138, title, size=12.0, color=color, weight="bold")
        cv.text(x + 345, 172, combo, size=11.0, color=GREY)
        cv.box(x + 40, 208, 250, 86, fc="white", ec=color, lw=1.8, radius=7)
        cv.text(x + 165, 240, "抗体を作るのは", size=9.6, color=GREY)
        cv.text(x + 165, 270, src,
                size=cv.fit_size([src], 224, 11.2, weight="bold"),
                color=color, weight="bold")
        cv.arrow((x + 300, 251), (x + 396, 251), color=color, lw=3.0, head=16)
        cv.box(x + 406, 208, 250, 86, fc="white", ec=color, lw=1.8, radius=7)
        cv.text(x + 531, 240, "標的は", size=9.6, color=GREY)
        cv.text(x + 531, 270, tgt,
                size=cv.fit_size([tgt], 224, 11.2, weight="bold"),
                color=color, weight="bold")
        cv.ax.plot([x + 40, x + 650], [322, 322], color=color, lw=1.2, ls=":")
        cv.text(x + 345, 356, tim, size=10.6, color=INK)
        cv.text(x + 345, 392, organ, size=10.6, color=INK)
        cv.text(x + 345, 444, "検査", size=9.6, color=GREY)
        cv.text(x + 345, 470,
                "抗体価・C4d・生検" if "拒絶" in title
                else "直接クームス・LDH・ハプトグロビン",
                size=10.4, color=color, weight="bold")

    panel(60, "抗体関連型拒絶", NG, "#fceeec", "主不適合（例：A 型腎 → O 型患者）",
          "レシピエント", "グラフトの内皮",
          "移植直後〜1 か月", "腎で問題になる")
    panel(770, "Passenger lymphocyte syndrome", PURPLE, "#f4f0fa",
          "副不適合（例：O 型肝 → A 型患者）",
          "グラフト由来の B 細胞", "患者自身の赤血球",
          "移植後 1〜3 週", "肝・肺・小腸で多い")

    msg(cv, 536,
        "PLS では、赤血球は A 型なのに抗 A が存在する ── "
        "ランドシュタイナーの法則が破れ、ラベルが自己矛盾する",
        fc="#f4f0fa", ec=PURPLE, tc="#4a3477")
    cv.save(P("f10_pls.png"))


# ---------------------------------------------------------------- f11
def f11():
    cv = Canvas(W, 680)
    cap(cv, 44, "造血幹細胞移植 ── 血液型が時間の関数になる")

    X0, X1 = 190, 1440
    BAR_Y, BAR_H = 150, 76
    cv.text(60, BAR_Y + BAR_H / 2, "赤血球", size=10.6, color=GREY, ha="left")
    cv.rect(X0, BAR_Y, 380, BAR_H, fc="#f0d98b", ec="#c9a227", lw=1.6)
    cv.text(X0 + 190, BAR_Y + BAR_H / 2, "レシピエント型", size=10.6,
            color="#7a5f0a", weight="bold")
    for i in range(24):
        x = X0 + 380 + i * 15
        cv.rect(x, BAR_Y, 15, BAR_H,
                fc="#f0d98b" if i % 2 == 0 else "#bcd4ea", ec="none")
    cv.rect(X0 + 380, BAR_Y, 360, BAR_H, fc="none", ec=GREY, lw=1.6)
    cv.text(X0 + 560, BAR_Y + BAR_H / 2, "混在", size=10.8, color=INK,
            weight="bold")
    cv.rect(X0 + 740, BAR_Y, X1 - (X0 + 740), BAR_H, fc="#bcd4ea",
            ec="#2e6da4", lw=1.6)
    cv.text((X0 + 740 + X1) / 2, BAR_Y + BAR_H / 2, "ドナー型", size=10.6,
            color="#174682", weight="bold")

    cv.ax.plot([X0, X1], [270, 270], color=GREY, lw=1.6)
    for x, lab in ((X0, "移植前"), (X0 + 380, "移植"), (X0 + 740, "生着"),
                   (X1 - 10, "完全キメラ")):
        cv.ax.plot([x, x], [264, 276], color=GREY, lw=1.6)
        cv.text(x, 296, lab, size=9.8, color=GREY)

    bot = 0
    for x, w, t, lines, color, fc in (
        (60, 420, "移植前", ["レシピエント型で運用する"], GREY, SOFT),
        (500, 480, "移行期", ["赤血球は O 型", "血漿は AB 型",
                           "── 双方に無害な組み合わせへ逃がす"], NG, "#fceeec"),
        (1020, 440, "完全生着後", ["ドナー型で運用する"], BLUE, "#eaf1f8"),
    ):
        h = textbox(cv, x, 340, w, lines, 10.8, fc=fc, ec=color, title=t,
                    title_color=color, lw=2.0, min_h=150)
        bot = max(bot, 340 + h)

    msg(cv, bot + 28,
        "固形臓器移植では抗原領域が「増える」。HSCT では抗原領域が「入れ替わる」 ── "
        "ルールをそのまま持ち込んではならない")
    cv.save(P("f11_hsct_timeline.png"))


# ---------------------------------------------------------------- f12
def f12():
    cv = Canvas(W, 700)
    cap(cv, 44, "抗体価が上がった ── 患者が作ったのか、我々が入れたのか")

    X0, X1, BASE, TOP = 140, 640, 400, 150
    cv.ax.plot([X0, X1], [BASE, BASE], color=GREY, lw=1.6)
    cv.ax.plot([X0, X0], [TOP, BASE], color=GREY, lw=1.6)
    cv.text(X0 - 60, (TOP + BASE) / 2, "抗 A\n抗体価", size=10.0, color=GREY)
    xs = [X0 + 20, X0 + 120, X0 + 230, X0 + 340, X0 + 440]
    ys = [BASE - 60, BASE - 70, BASE - 130, BASE - 200, BASE - 216]
    cv.ax.plot(xs, ys, color=NAVY, lw=3.4, zorder=6)
    for x, y in zip(xs, ys):
        cv.ax.add_patch(Circle((x, y), 6, facecolor=NAVY, edgecolor="white",
                               lw=1.4, zorder=7))
    cv.text(X0 + 460, BASE - 246, "上がった", size=11.6, color=NAVY,
            weight="bold", ha="left")
    cv.text((X0 + X1) / 2, BASE + 28, "移植後の経過", size=9.8, color=GREY)

    h1 = textbox(cv, 800, 136, 640,
                 ["拒絶の始まりかもしれない。",
                  "グラフト機能と合わせて評価する"],
                 11.0, fc="#fceeec", ec=NG,
                 title="① 患者の免疫系が作った", title_color=NG, lw=2.0)
    y2 = 136 + h1 + 22
    h2 = textbox(cv, 800, y2, 640,
                 ["IVIG はプール血漿由来なので抗 A・抗 B を含む。",
                  "FFP の大量投与でも同じことが起こる"],
                 11.0, fc="#fdf3e3", ec=ORANGE,
                 title="② 我々が投与した製剤に入っていた",
                 title_color="#9a6410", lw=2.0)

    cv.arrow((700, 250), (790, 136 + h1 / 2), color=GREY, lw=2.4, head=13)
    cv.arrow((700, 250), (790, y2 + h2 / 2), color=GREY, lw=2.4, head=13)

    BOT = max(y2 + h2, 440)
    m1 = msg(cv, BOT + 32,
             "抗体価が測っているのは「体内の抗体分子の総量」であって、"
             "誰が作ったかは問わない",
             fc="#fdf3e3", ec=ORANGE, tc="#9a6410")
    msg(cv, BOT + 32 + m1 + 16,
        "検査値は「値」として読むのではなく、「その値がどう作られたか」とセットで読む")
    cv.save(P("f12_ivig.png"))


# ---------------------------------------------------------------- f13
def f13():
    cv = Canvas(W, 800)
    cap(cv, 44, "C5 を止めても、止まらない経路がある")

    CX = 420
    steps = [("抗体がグラフト内皮の抗原に結合", 120, NAVY, "#eef1f6"),
             ("C1q → 古典経路の起動", 210, NAVY, "#eef1f6"),
             ("C3 転換酵素 → C3b", 300, NAVY, "#eef1f6"),
             ("C5 転換酵素 → C5b", 420, NAVY, "#eef1f6"),
             ("C5b-9（膜侵襲複合体）", 520, GREY, "#f2f4f6")]
    for text, y, color, fc in steps:
        cv.box(CX - 250, y, 500, 62, fc=fc, ec=color, lw=1.8, radius=8)
        cv.text(CX, y + 31, text, size=11.0, color=color, weight="bold")
    for y0, y1 in ((182, 210), (272, 300), (362, 420), (482, 520)):
        cv.arrow((CX, y0), (CX, y1), color=GREY, lw=2.2, head=12)

    cv.ax.plot([CX - 120, CX + 120], [396, 372], color=NG, lw=5.0, zorder=8)
    cv.ax.plot([CX - 120, CX + 120], [372, 396], color=NG, lw=5.0, zorder=8)
    cv.text(CX + 190, 384, "C5 阻害薬", size=11.6, color=NG, weight="bold",
            ha="left")
    cv.text(CX, 614, "ここだけが止まる", size=11.0, color=GREY)

    RX, RW, ry = 870, 590, 150
    centers = []
    for title, lines in (
        ("オプソニン化（C3b / iC3b）",
         ["脾臓・肝臓のマクロファージが貪食する", "→ 血管外溶血・慢性の傷害"]),
        ("ADCC（Fcγ 受容体）",
         ["NK 細胞・マクロファージによる傷害", "→ 補体をまったく必要としない"]),
        ("内皮の活性化",
         ["Weibel-Palade 小体の放出、P-セレクチン表出",
          "→ 抗体結合そのものによる"]),
    ):
        h = textbox(cv, RX, ry, RW, lines, 10.4, fc="#eaf5ee", ec=OK,
                    title=title, title_color=OK, lw=2.0)
        centers.append(ry + h / 2)
        ry += h + 24

    cv.arrow((CX + 250, 331), (RX - 10, centers[0]), color=OK, lw=2.6,
             head=14)
    cv.arrow((CX + 250, 151), (RX - 10, centers[1]), color=OK, lw=2.6,
             head=14)
    cv.arrow((CX + 250, 151), (RX - 10, centers[2]), color=OK, lw=2.6,
             head=14)

    msg(cv, max(ry, 650) + 10,
        "経路をひとつ塞いでも病態は消えない。時間軸が伸び、現れる場所が変わるだけである",
        fc="#eaf5ee", ec=OK, tc="#14603c", size=12.5)
    cv.save(P("f13_complement.png"))


# ---------------------------------------------------------------- f14
def f14():
    cv = Canvas(W, 760)
    cap(cv, 44, "手術室で衝突する二つの時間軸")

    cv.box(60, 110, 660, 250, fc="#eaf1f8", ec=BLUE, lw=2.0, radius=9)
    cv.text(390, 148, "現在時制 ── 手術室の判断", size=12.0, color=BLUE,
            weight="bold")
    cv.block(84, 176, 612,
             ["酸素運搬能は足りているか", "止血は成立するか",
              "判断の地平線は数時間先まで"], 11.0, color=INK)
    cv.text(390, 322, "取り返しがつく損失を扱う", size=10.6, color=BLUE,
            weight="bold")

    cv.box(800, 110, 660, 250, fc="#fceeec", ec=NG, lw=2.0, radius=9)
    cv.text(1130, 148, "未来時制 ── 移植で加わる判断", size=12.0, color=NG,
            weight="bold")
    cv.block(824, 176, 612,
             ["この一単位の血漿が", "この患者の免疫学的な将来に何を残すか",
              "判断の地平線は数か月から数年"], 11.0, color=INK)
    cv.text(1130, 322, "取り返しがつかない損失を扱う", size=10.6, color=NG,
            weight="bold")

    cv.arrow((724, 235), (796, 235), color=GREY, lw=2.6, head=14,
             style="<|-|>")
    cv.text(760, 200, "衝突", size=11.0, color=NAVY, weight="bold")

    _h = textbox(cv, 60, 390, 1400,
            ["大量出血のさなかに「AB 型を待つか、O 型で止血するか」を迫られたら、"
             "現在時制が勝つ。患者が死ねばグラフトも死ぬ。",
             "だが本当に重要なのは、その二択が発生したこと自体が"
             "すでに一つの失敗だという認識のほうである。"],
            11.0, fc="white", ec=GREY, title="二択を迫られたとき",
            title_color=NAVY, lw=1.8)

    msg(cv, 390 + _h + 24,
        "プロトコルの価値は、正しい選択をさせることではなく、選ばなくて済むようにすること",
        size=12.5)
    cv.save(P("f14_two_timescales.png"))


# ---------------------------------------------------------------- f15
def f15():
    cv = Canvas(W, 620)
    cap(cv, 44, "暗記表の代わりに持ち帰る三つの問い")

    CARDS = [
        ("問い 一", "この患者の体内には、いま何種類の\n「抗原の領域」があるか",
         ["通常の患者：一つ（自分の赤血球）",
          "ABO 不適合移植：二つ（赤血球とグラフト内皮）",
          "HSCT の移行期：入れ替わっていく"], AG, "#fdf1ea"),
        ("問い 二", "いま入れようとしている製剤は、\n何を持ち込むのか",
         ["赤血球は抗原を持ち込む",
          "血漿は抗体を持ち込む",
          "血小板だけが両方を持ち込む"], AB, "#eaf1f8"),
        ("問い 三", "その抗体価は、\n誰が作ったのか",
         ["患者の免疫系か",
          "我々が投与した製剤（IVIG・FFP）か",
          "検査値は出所を教えてくれない"], PURPLE, "#f4f0fa"),
    ]
    GAP, L = 24, 60
    CW = (W - L * 2 - GAP * 2) / 3
    for i, (no, q, lines, color, fc) in enumerate(CARDS):
        x = L + i * (CW + GAP)
        cv.box(x, 100, CW, 60, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + CW / 2, 130, no, size=12.0, color="white", weight="bold")
        cv.box(x, 172, CW, 300, fc=fc, ec=color, lw=2.0, radius=8)
        sz = cv.fit_size(q.split("\n"), CW - 44, 11.8, weight="bold")
        cv.text(x + CW / 2, 228, q, size=sz, color=color, weight="bold")
        cv.ax.plot([x + 34, x + CW - 34], [284, 284], color=color, lw=1.2,
                   ls=":")
        s = cv.fit_size(lines, CW - 44, 10.4)
        for j, ln in enumerate(lines):
            cv.text(x + CW / 2, 322 + LH(s, 1.7) * j, ln, size=s, color=INK)

    msg(cv, 508,
        "血液型を合わせるのではない。抗原と抗体の地図を描くのである。", size=13.5)
    cv.save(P("f15_three_questions.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12,
               f13, f14, f15):
        fn()
        print("ok", fn.__name__)
