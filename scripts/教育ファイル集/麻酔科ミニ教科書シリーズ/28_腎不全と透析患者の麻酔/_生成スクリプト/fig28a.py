# -*- coding: utf-8 -*-
"""㉘ 図版 f01〜f07"""
import os

from fig28common import (Canvas, LH, textbox, cap, msg, fitlines, card, band,
                         stat, tick_axis, outpath, save, W, TEAL, FC,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)

OUT = outpath()


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f01
def f01():
    """腎臓の六つの仕事 → 手術室で見える顔"""
    ROWS = [
        ("① 溶質を捨てる", "尿毒素・リンが溜まる",
         "出血傾向・意識・創傷治癒", PURPLE),
        ("② 水と電解質の量", "体液過剰／高カリウム",
         "肺うっ血・低血圧・不整脈", BLUE),
        ("③ 酸塩基を調える", "代謝性アシドーシス",
         "換気の要求・昇圧薬の効き", GREEN),
        ("④ 血圧と体液量の調節", "高血圧と透析後の低血圧",
         "血圧の振れ幅が大きい", ORANGE),
        ("⑤ ホルモンを出す", "EPO・活性型ビタミンD低下",
         "貧血・血管石灰化", RED),
        ("⑥ 薬を体から出す", "腎排泄薬と活性代謝産物の蓄積",
         "効きすぎる・覚めない", NAVY),
    ]
    RH, GAP, TOP = 104, 14, 140
    cv = Canvas(W, 1500)
    cap(cv, 46, "腎臓の六つの仕事と、手術室で見える六つの顔")

    L, CW1, CW2, CW3 = 52, 330, 430, 560
    X2 = L + CW1 + 44
    X3 = X2 + CW2 + 44
    for x, w, t in ((L, CW1, "腎臓の仕事"), (X2, CW2, "抜けると起きること"),
                    (X3, CW3, "手術室で見える顔")):
        cv.text(x + w / 2, TOP - 26, t, size=11.5, color=GREY, weight="bold")

    for i, (job, lose, face, color) in enumerate(ROWS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, CW1, RH, fc=color, ec=color, lw=0, radius=8)
        s, ln = fitlines(cv, [job], CW1 - 34, 12.4, weight="bold", floor=9.4)
        cv.block(L, y + (RH - LH(s, 1.45) * len(ln)) / 2, CW1, ln, s,
                 color="white", weight="bold")

        cv.arrow((L + CW1 + 8, y + RH / 2), (X2 - 10, y + RH / 2),
                 color=color, lw=2.2, head=11)
        cv.box(X2, y, CW2, RH, fc=FC[color], ec=color, lw=1.7, radius=8)
        s, ln = fitlines(cv, [lose], CW2 - 36, 11.2)
        cv.block(X2, y + (RH - LH(s, 1.55) * len(ln)) / 2, CW2, ln, s)

        cv.arrow((X2 + CW2 + 8, y + RH / 2), (X3 - 10, y + RH / 2),
                 color=color, lw=2.2, head=11)
        cv.box(X3, y, CW3, RH, fc="white", ec=color, lw=2.0, radius=8)
        s, ln = fitlines(cv, [face], CW3 - 36, 11.8, weight="bold")
        cv.block(X3, y + (RH - LH(s, 1.55) * len(ln)) / 2, CW3, ln, s,
                 color=color, weight="bold")

    y = TOP + len(ROWS) * (RH + GAP) + 10
    msg(cv, y, "透析が代行するのは①②③まで。⑤は代行されない。⑥は麻酔科医の仕事そのもの")
    save(cv, P("f01_six_jobs.png"))


# ---------------------------------------------------------------- f02
def f02():
    """腎臓の言葉の地図"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "腎臓の言葉の地図 ── 時間軸で分ける")

    X0, X1, AY = 120, 1400, 240
    tick_axis(cv, X0, X1, AY,
              [(0.0, "発症"), (0.18, "7 日"), (0.52, "90 日"), (1.0, "以降")])

    SPANS = [(0.0, 0.18, "AKI\n急性腎障害", RED),
             (0.18, 0.52, "AKD\n急性腎障害後期", ORANGE),
             (0.52, 1.0, "CKD\n慢性腎臓病", BLUE)]
    for a, b, lab, color in SPANS:
        xa, xb = X0 + (X1 - X0) * a, X0 + (X1 - X0) * b
        cv.box(xa + 6, AY - 150, xb - xa - 12, 128, fc=FC[color], ec=color,
               lw=1.8, radius=8)
        cv.text((xa + xb) / 2, AY - 86, lab, size=13.0, color=color,
                weight="bold", linespacing=1.5)

    cv.text(X0, AY + 96, "CKD の内訳 ── GFR 区分", size=11.5, color=GREY,
            weight="bold", ha="left")
    G = [("G1", "90 以上", GREY), ("G2", "60〜89", GREY),
         ("G3a", "45〜59", BLUE), ("G3b", "30〜44", BLUE),
         ("G4", "15〜29", ORANGE), ("G5", "15 未満", RED)]
    CW, GAP, GY = 196, 14, AY + 126
    for i, (g, v, color) in enumerate(G):
        x = X0 + i * (CW + GAP)
        cv.box(x, GY, CW, 104, fc=FC[color], ec=color, lw=1.7, radius=8)
        cv.text(x + CW / 2, GY + 34, g, size=14.5, color=color, weight="bold")
        s = cv.fit_size([v], CW - 26, 10.6)
        cv.text(x + CW / 2, GY + 76, v, size=s, color=INK)

    SY = GY + 134
    SUF = [("G5D", "透析を受けている", RED),
           ("G5T", "腎移植を受けている", GREEN),
           ("AKI on CKD", "CKD に急性増悪が重なった", PURPLE)]
    SW = 420
    for i, (t, d, color) in enumerate(SUF):
        x = X0 + i * (SW + 20)
        cv.box(x, SY, SW, 100, fc="white", ec=color, lw=2.0, radius=8)
        cv.text(x + 20, SY + 32, t, size=13.0, color=color, weight="bold",
                ha="left")
        s, ln = fitlines(cv, [d], SW - 40, 10.6)
        cv.block(x + 20, SY + 54, SW - 40, ln, s, ha="left")

    msg(cv, SY + 124,
        "「CKD G5」と書いてあっても、透析をしているかどうかは別に確かめる")
    save(cv, P("f02_terms.png"))


# ---------------------------------------------------------------- f03
def f03():
    """日本の透析人口"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "日本の透析人口（2024年12月31日現在・日本透析医学会統計）")

    L = 52
    SW, SG = 348, 16
    STATS = [("337,414 人", "慢性透析患者数", NAVY),
             ("70.27 歳", "平均年齢", BLUE),
             ("36,404 人", "年間の新規導入", ORANGE),
             ("10,774 人", "腹膜透析患者数", GREEN)]
    for i, (v, l, c) in enumerate(STATS):
        stat(cv, L + i * (SW + SG), 100, SW, 136, v, l, color=c)

    STATS2 = [("2,725.4 人", "人口百万対", GREY),
              ("71.69 歳", "導入時の平均年齢", GREY),
              ("38,348 人", "年間死亡患者数", GREY),
              ("約 3%", "腹膜透析の占める割合", GREY)]
    for i, (v, l, c) in enumerate(STATS2):
        stat(cv, L + i * (SW + SG), 252, SW, 118, v, l, color=c, vs=19.0)

    BY = 428
    cv.text(L, BY - 20, "原疾患（維持透析患者）", size=11.8, color=GREY,
            weight="bold", ha="left")
    BARS = [("糖尿病性腎症", 39.2, RED), ("慢性糸球体腎炎", 23.0, BLUE),
            ("腎硬化症", 14.5, ORANGE), ("その他・不明", 23.3, GREY)]
    BX, BW, BH = 300, 980, 46
    for i, (name, pct, color) in enumerate(BARS):
        y = BY + 14 + i * (BH + 12)
        cv.text(BX - 18, y + BH / 2, name, size=11.4, color=INK, ha="right")
        cv.rect(BX, y, BW, BH, fc="#eef1f4")
        cv.rect(BX, y, BW * pct / 45.0, BH, fc=color)
        cv.text(BX + BW * pct / 45.0 + 16, y + BH / 2, "%.1f%%" % pct,
                size=11.6, color=color, weight="bold", ha="left")

    msg(cv, BY + 14 + 4 * (BH + 12) + 18,
        "四割が糖尿病性腎症 ── 自律神経障害・無痛性虚血・胃内容停滞がついてくる")
    save(cv, P("f03_jp_dialysis.png"))


# ---------------------------------------------------------------- f04
def f04():
    """透析からの経過時間"""
    LW, L, R = 190, 60, 1466
    COLS = [("0〜6 時間", "透析直後", RED),
            ("6〜24 時間", "翌日まで", GREEN),
            ("24〜48 時間", "中一日", ORANGE),
            ("48〜72 時間", "中二日明け", PURPLE)]
    ROWS = [("体液量", ["最も少ない", "適正に近い", "増えてくる", "多い"], BLUE),
            ("カリウム", ["最も低い", "低め", "上がってくる", "高い"], RED),
            ("凝固", ["ヘパリンが残存", "ほぼ回復", "正常", "正常"], GREEN),
            ("麻酔の注意",
             ["導入時の低血圧", "待機手術に最適", "おおむね許容",
              "高カリウムと体液過剰"], NAVY)]
    HY, HH, RY, RH, GAP = 110, 84, 214, 92, 12
    H = RY + len(ROWS) * (RH + GAP) + 110
    cv = Canvas(W, max(H, 1500))
    cap(cv, 46, "前回透析からの経過時間で、何が変わるか")

    X0 = L + LW
    CW = (R - X0 - 3 * 16) / 4
    for i, (t, sub, color) in enumerate(COLS):
        x = X0 + i * (CW + 16)
        cv.box(x, HY, CW, HH, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + CW / 2, HY + 30, t, size=13.5, color="white", weight="bold")
        cv.text(x + CW / 2, HY + 60, sub, size=10.6, color="white")

    for r, (label, cells, color) in enumerate(ROWS):
        y = RY + r * (RH + GAP)
        cv.box(L, y, LW - 16, RH, fc=FC[color], ec=color, lw=1.7, radius=8)
        s, ln = fitlines(cv, [label], LW - 50, 11.8, weight="bold", floor=9.2)
        cv.block(L, y + (RH - LH(s, 1.45) * len(ln)) / 2, LW - 16, ln, s,
                 color=color, weight="bold")
        for i, c in enumerate(cells):
            x = X0 + i * (CW + 16)
            cv.box(x, y, CW, RH, fc=FC[COLS[i][2]], ec=COLS[i][2], lw=1.5,
                   radius=8)
            s2, ln2 = fitlines(cv, [c], CW - 34, 11.4)
            cv.block(x, y + (RH - LH(s2, 1.55) * len(ln2)) / 2, CW, ln2, s2)

    msg(cv, RY + len(ROWS) * (RH + GAP) + 16,
        "検査値は「いつ引いたか」とセットでなければ読めない")
    save(cv, P("f04_timeline.png"))


# ---------------------------------------------------------------- f05
def f05():
    """術前評価の七つの窓"""
    ITEMS = [
        ("① 透析の型と条件",
         ["血液透析か腹膜透析か", "曜日・時間・除水量", "回路の抗凝固薬"], NAVY),
        ("② 前回透析からの経過",
         ["最後に透析したのはいつか", "検査値を引いた時刻", "次の透析の予定"], NAVY),
        ("③ 体液量",
         ["ドライウェイトと当日体重", "浮腫・頸静脈・肺野", "透析中の血圧経過"], BLUE),
        ("④ 心臓",
         ["左室肥大と拡張能", "弁の石灰化・心膜液", "虚血・不整脈"], RED),
        ("⑤ 血液",
         ["ヘモグロビン・血小板数", "出血の病歴", "輸血と同種抗体"], PURPLE),
        ("⑥ アクセス",
         ["シャントの位置と種類", "スリルの有無", "腹膜カテーテル"], GREEN),
        ("⑦ 薬",
         ["降圧薬・抗血栓薬", "SGLT2 阻害薬・GLP-1", "免疫抑制薬・吸着薬"], ORANGE),
    ]
    L, CW, GAP, TOP = 52, 348, 16, 112
    CH = 69 + 9 + 28 + 3 * LH(10.8, 1.85)
    H = TOP + 2 * CH + 34 + 110
    cv = Canvas(W, max(H, 1500))
    cap(cv, 46, "術前評価の七つの窓 ── ①②を先に決めないと、③以降が読めない")

    for i, (head, lines, color) in enumerate(ITEMS[:4]):
        card(cv, L + i * (CW + GAP), TOP, CW, head, lines, color,
             head_size=12.2, body_size=10.8, lh=1.85)
    Y2 = TOP + CH + 24
    L2 = L + (CW + GAP) / 2
    for i, (head, lines, color) in enumerate(ITEMS[4:]):
        card(cv, L2 + i * (CW + GAP), Y2, CW, head, lines, color,
             head_size=12.2, body_size=10.8, lh=1.85)

    msg(cv, Y2 + CH + 18,
        "最初に聞くのは検査値ではなく「最後に透析をしたのはいつですか」")
    save(cv, P("f05_seven_windows.png"))


# ---------------------------------------------------------------- f06
def f06():
    """術前カリウムの帯"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "術前カリウムの帯 ── 数字は境界であって、スイッチではない")

    X0, X1, BY, BH = 130, 1360, 250, 76
    ZONES = [(4.0, 5.0, "日常の範囲", "#eaf5ee", GREEN),
             (5.0, 5.5, "様子を見る", "#f3f7ea", "#6d8a35"),
             (5.5, 6.0, "手を打つ", "#fdf3e3", ORANGE),
             (6.0, 7.0, "中止が増える", "#fceeec", RED)]
    LO, HI = 4.0, 7.0

    def px(v):
        return X0 + (X1 - X0) * (v - LO) / (HI - LO)

    for a, b, lab, fc, ec in ZONES:
        cv.rect(px(a), BY, px(b) - px(a), BH, fc=fc, ec=ec, lw=1.6)
        s = cv.fit_size([lab], px(b) - px(a) - 20, 12.0, min_size=8.2,
                        weight="bold")
        cv.text((px(a) + px(b)) / 2, BY + BH / 2, lab, size=s, color=ec,
                weight="bold")
    for v in (4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0):
        cv.ax.plot([px(v), px(v)], [BY + BH, BY + BH + 10], color=GREY, lw=1.8,
                   zorder=4)
        cv.text(px(v), BY + BH + 32, "%.1f" % v, size=11.2, color=GREY)
    cv.text(X1 + 52, BY + BH + 32, "mEq/L", size=10.6, color=GREY, ha="left")

    for v in (5.5, 6.0):
        cv.ax.plot([px(v), px(v)], [BY - 60, BY], color=NAVY, lw=2.4, zorder=5)
        cv.text(px(v), BY - 78, "%.1f" % v, size=15.0, color=NAVY,
                weight="bold")

    NOTES = [("5.5 を超える患者",
              "術中にカリウムを下げる処置を要する頻度が約 2 倍", ORANGE),
             ("24 時間以内に 6.0 以上",
              "手術が中止になる頻度が 2.40 倍。"
              "ただし実際に中止になったのは 5.5 以上の一割", RED)]
    NY = BY + BH + 76
    for i, (h, d, color) in enumerate(NOTES):
        band(cv, 130, NY + i * 96, X1 - 130 + 60, 84, h, [d], color,
             label_w=320, label_size=11.4, body_size=11.0)

    msg(cv, NY + 2 * 96 + 10,
        "どちらも患者の転帰ではなく、医師の行動を測った数字である")
    save(cv, P("f06_potassium.png"))


# ---------------------------------------------------------------- f07
def f07():
    """尿毒症性出血への手立てと時間軸"""
    ROWS = [("血液透析", 0.10, 0.60, "数時間で効き、次の透析まで", BLUE),
            ("デスモプレシン 0.3 µg/kg", 0.14, 0.34, "1 時間で効き 4〜8 時間",
             RED),
            ("クリオプレシピテート 10 単位", 0.14, 0.50,
             "1 時間で効き 4〜12 時間", PURPLE),
            ("赤血球輸血（Hct 30% 目安）", 0.20, 0.72, "貧血が続く限り", ORANGE),
            ("結合型エストロゲン 0.6 mg/kg/日×5 日", 0.30, 1.0,
             "6 時間で効き 14〜21 日", GREEN)]
    X0, X1, AY = 470, 1400, 172
    RY, RH, GAP = AY + 66, 78, 14
    H = RY + len(ROWS) * (RH + GAP) + 110
    cv = Canvas(W, max(H, 1500))
    cap(cv, 46, "尿毒症性出血への手立てと、その時間軸")

    tick_axis(cv, X0, X1, AY,
              [(0.0, "投与"), (0.14, "1 時間"), (0.30, "6 時間"),
               (0.50, "12 時間"), (0.72, "5 日"), (1.0, "21 日")])
    cv.text(X0 - 30, AY, "時間（対数的に圧縮）", size=10.4, color=GREY,
            ha="right")

    for i, (name, a, b, note, color) in enumerate(ROWS):
        y = RY + i * (RH + GAP)
        s, ln = fitlines(cv, [name], 380, 11.4, weight="bold", floor=9.0)
        cv.block(44, y + (RH - LH(s, 1.5) * len(ln)) / 2, 380, ln, s,
                 color=color, weight="bold", ha="left")
        xa, xb = X0 + (X1 - X0) * a, X0 + (X1 - X0) * b
        cv.box(xa, y + 12, xb - xa, RH - 24, fc=FC[color], ec=color, lw=1.8,
               radius=8)
        sz = cv.fit_size([note], xb - xa - 30, 10.8, min_size=9.6)
        if cv.width(note, sz, "bold") <= xb - xa - 30:
            cv.text((xa + xb) / 2, y + RH / 2, note, size=sz, color=color,
                    weight="bold")
        else:
            cv.text(xb + 16, y + RH / 2, note, size=10.4, color=color,
                    ha="left")

    msg(cv, RY + len(ROWS) * (RH + GAP) + 14,
        "選ぶ基準は「いつ手術か」── 今日ならデスモプレシン、数日後ならエストロゲン")
    save(cv, P("f07_uremic_bleeding.png"))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f01, f02, f03, f04, f05, f06, f07):
        fn()
        print("ok", fn.__name__)
