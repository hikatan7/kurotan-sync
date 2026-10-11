# -*- coding: utf-8 -*-
"""㉙ 図版 f01〜f08（総論・解剖・置き方）"""
import os

from fig29common import (Canvas, LH, textbox, cap, msg, fitlines, card, band,
                         stat, tick_axis, outpath, save, W, TEAL, FC,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)

OUT = outpath()


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f01
def f01():
    """三つの機能 ── 声門上器具を製品名で覚えない"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "声門上器具を製品名ではなく「三つの機能」で分ける")

    CW, GAP, X0, Y0 = 460, 40, 52, 130
    COLS = [
        ("① 周囲シール", BLUE,
         ["喉頭入口部の周囲を囲み、", "声門へ気流を導く", "",
          "気管内をカフで隔離する", "のではない"]),
        ("② 胃ドレーン", GREEN,
         ["食道入口部へ向かう経路。", "胃管挿入・胃内ガス排出・",
          "逆流の認識を助ける", "", "気道隔離ではない"]),
        ("③ 挿管導管", PURPLE,
         ["柔軟性気管支鏡などを併用し、", "気管挿管への橋渡しになる",
          "", "器具ごとの適合性は", "添付文書で確認する"]),
    ]
    for i, (head, color, lines) in enumerate(COLS):
        x = X0 + i * (CW + GAP)
        card(cv, x, Y0, CW, head, lines, color, head_size=14.0,
             body_size=11.4, lh=1.75)

    YB = Y0 + 440
    cv.text(X0, YB, "この三つは、それぞれ別の期待に応える。", size=12.0,
            color=GREY, ha="left")

    Y1 = YB + 40
    band(cv, X0, Y1, W - 104, 112, "第1世代",
         ["呼吸管腔だけをもち、胃内容を導く専用の経路がない"],
         ORANGE, label_w=250)
    band(cv, X0, Y1 + 130, W - 104, 138, "第2世代",
         ["胃ドレーンチャネル、より高い咽頭リーク圧、",
          "バイトブロックなどを備える"],
         BLUE, label_w=250)
    band(cv, X0, Y1 + 288, W - 104, 138, "第3世代",
         ["カメラを内蔵し、留置を目で見て確かめられる。",
          "第2世代の機能に「視認」が加わったもの"],
         GREEN, label_w=250)

    msg(cv, Y1 + 454,
        "世代は「安全 対 危険」の二分法ではない。第2世代でも気管チューブが要る場面はある")
    save(cv, P("f01_three_functions.png"))


# ---------------------------------------------------------------- f02
def f02():
    """器具の来歴 ── 40年の年表"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "声門上器具の四十年 ── 何を足してきたのか")

    ITEMS = [
        ("1980年代", "試作と発表",
         ["咽頭にカフを置き", "声門の周囲を囲む"], BLUE),
        ("1990年代", "普及と検証",
         ["誤嚥の頻度が数字で", "語られはじめる"], GREEN),
        ("2000年代", "胃ドレーンの追加",
         ["第2世代 ── 逆流を", "「逃がす」構造"], ORANGE),
        ("2010年代", "救済器具として",
         ["難気道指針の", "Plan B に定着"], PURPLE),
        ("2020年代", "視認の追加",
         ["第3世代 ── カメラで", "留置を目で見る"], RED),
    ]
    CW, GAP, X0 = 272, 20, 60
    AY = 264
    cv.arrow((X0 - 14, AY), (X0 + 5 * CW + 4 * GAP + 14, AY),
             color=GREY, lw=2.4, head=12)
    for i, (era, head, body, color) in enumerate(ITEMS):
        x = X0 + i * (CW + GAP)
        cx = x + CW / 2
        cv.text(cx, AY + 34, era, size=11.4, color=GREY, weight="bold")
        cv.ax.plot([cx, cx], [AY - 9, AY + 9], color=GREY, lw=2.0, zorder=4)
        cv.arrow((cx, AY - 14), (cx, AY - 40), color=color, lw=2.2, head=10)
        hs, hl = fitlines(cv, [head], CW - 26, 11.8, weight="bold", floor=9.0)
        hh = 26 + LH(hs, 1.4) * len(hl)
        cv.box(x, AY - 46 - hh, CW, hh, fc=color, ec=color, lw=0, radius=8)
        cv.block(x, AY - 46 - hh + 13, CW, hl, hs, color="white",
                 weight="bold")
        bs, bl = fitlines(cv, body, CW - 34, 11.0, floor=8.8)
        bh = 30 + LH(bs, 1.6) * len(bl)
        cv.box(x, AY + 62, CW, bh, fc=FC[color], ec=color, lw=1.7, radius=8)
        cv.block(x, AY + 62 + 15, CW, bl, bs, lh=LH(bs, 1.6))

    Y2 = AY + 254
    cv.text(52, Y2, "足されてきたものを、一列に並べると", size=12.5,
            color=GREY, weight="bold", ha="left")
    STEPS = ["気流路をつくる", "胃の道を分ける", "リーク圧を上げる",
             "咬み込みを防ぐ", "挿管の橋渡し", "留置を目で見る"]
    SW, SG = 222, 18
    for i, s in enumerate(STEPS):
        x = 52 + i * (SW + SG)
        cv.box(x, Y2 + 34, SW, 92, fc="white", ec=NAVY, lw=1.8, radius=8)
        sz, ln = fitlines(cv, [s], SW - 30, 11.4, weight="bold", floor=8.8)
        cv.block(x, Y2 + 34 + (92 - LH(sz, 1.45) * len(ln)) / 2, SW, ln, sz,
                 color=NAVY, weight="bold")
        if i < len(STEPS) - 1:
            cv.arrow((x + SW + 2, Y2 + 80), (x + SW + SG - 2, Y2 + 80),
                     color=GREY, lw=2.0, head=10)

    msg(cv, Y2 + 156,
        "足されたのは機能であって、声門の内側に入る資格ではない")
    save(cv, P("f02_history.png"))


# ---------------------------------------------------------------- f03
def f03():
    """世代の機能マトリクス"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "世代でできること・できないこと")

    ROWS = [
        ("声門へ気流を導く", "○", "○", "○", GREEN),
        ("咽頭リーク圧", "低め", "高め", "高め", BLUE),
        ("胃ドレーンチャネル", "×", "○", "○", ORANGE),
        ("バイトブロック構造", "製品による", "多くは内蔵", "多くは内蔵", PURPLE),
        ("留置を目で確認", "×（盲目的）", "×（盲目的）", "○（内蔵カメラ）", RED),
        ("気管挿管の導管", "製品による", "製品による", "製品による", GREY),
        ("声門より遠位の隔離", "×", "×", "×", NAVY),
    ]
    L, C1, CW, GAP, TOP, RH = 52, 470, 300, 18, 176, 96
    HEADS = ["第1世代", "第2世代", "第3世代"]
    cv.text(L + C1 / 2, TOP - 34, "機能", size=12.0, color=GREY, weight="bold")
    for j, h in enumerate(HEADS):
        x = L + C1 + GAP + j * (CW + GAP)
        cv.box(x, TOP - 66, CW, 54, fc=NAVY, ec=NAVY, lw=0, radius=8)
        cv.text(x + CW / 2, TOP - 39, h, size=12.5, color="white",
                weight="bold")

    for i, (name, a, b, c, color) in enumerate(ROWS):
        y = TOP + i * (RH + 12)
        cv.box(L, y, C1, RH, fc=FC[color], ec=color, lw=1.7, radius=8)
        s, ln = fitlines(cv, [name], C1 - 34, 11.8, weight="bold", floor=9.2)
        cv.block(L, y + (RH - LH(s, 1.45) * len(ln)) / 2, C1, ln, s,
                 color=color, weight="bold")
        for j, v in enumerate((a, b, c)):
            x = L + C1 + GAP + j * (CW + GAP)
            fc = "#fdecea" if v.startswith("×") else "white"
            cv.box(x, y, CW, RH, fc=fc, ec=color, lw=1.6, radius=8)
            s2, ln2 = fitlines(cv, [v], CW - 26, 11.6, weight="bold",
                               floor=9.0)
            cv.block(x, y + (RH - LH(s2, 1.45) * len(ln2)) / 2, CW, ln2, s2,
                     color=RED if v.startswith("×") else INK, weight="bold")

    y = TOP + len(ROWS) * (RH + 12) + 16
    msg(cv, y,
        "最下段だけは、どの世代でも「×」のままである。これが本書を貫く一行になる",
        fc="#fceeec", ec=RED, tc=RED)
    save(cv, P("f03_generations.png"))


# ---------------------------------------------------------------- f04
def f04():
    """二本の道 ── 気流路と消化管路"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "声門上器具が関わる二本の道")

    CW, X0, Y0 = 690, 60, 140
    X1 = X0 + CW + 60

    cv.box(X0, Y0, CW, 68, fc=BLUE, ec=BLUE, lw=0, radius=8)
    cv.text(X0 + CW / 2, Y0 + 34, "① 気流路 ── 器具が「作る」道", size=14.0,
            color="white", weight="bold")
    cv.box(X1, Y0, CW, 68, fc=ORANGE, ec=ORANGE, lw=0, radius=8)
    cv.text(X1 + CW / 2, Y0 + 34, "② 消化管路 ── 器具は「見張る」だけ",
            size=14.0, color="white", weight="bold")

    AIR = ["口腔・舌根", "口咽頭", "器具のカフ／ゲル状シール",
           "喉頭入口部（喉頭蓋・披裂部）", "声門（仮声帯・真声帯）", "気管 → 肺"]
    GUT = ["器具の先端は食道入口部へ向く", "第2世代の胃ドレーン",
           "上部食道", "胃", "胃送気・逆流", "誤嚥のリスク"]
    BH, BG, YS = 96, 26, Y0 + 106
    for i in range(6):
        y = YS + i * (BH + BG)
        cv.box(X0, y, CW, BH, fc=FC[BLUE], ec=BLUE, lw=1.8, radius=8)
        s, ln = fitlines(cv, [AIR[i]], CW - 40, 12.0, floor=9.4)
        cv.block(X0, y + (BH - LH(s, 1.5) * len(ln)) / 2, CW, ln, s,
                 color=INK)
        fc = "#fdecea" if i >= 4 else FC[ORANGE]
        ec = RED if i >= 4 else ORANGE
        cv.box(X1, y, CW, BH, fc=fc, ec=ec, lw=1.8, radius=8)
        s, ln = fitlines(cv, [GUT[i]], CW - 40, 12.0, floor=9.4)
        cv.block(X1, y + (BH - LH(s, 1.5) * len(ln)) / 2, CW, ln, s,
                 color=RED if i >= 4 else INK)
        if i < 5:
            cv.arrow((X0 + CW / 2, y + BH + 3), (X0 + CW / 2, y + BH + BG - 3),
                     color=BLUE, lw=2.4, head=11)
            cv.arrow((X1 + CW / 2, y + BH + 3), (X1 + CW / 2, y + BH + BG - 3),
                     color=ORANGE, lw=2.4, head=11)

    y = YS + 6 * (BH + BG) + 10
    msg(cv, y,
        "①の道は、位置が浅い・深い・回ると簡単に細くなる。②の道は、細くも太くもならない")
    save(cv, P("f04_two_paths.png"))


# ---------------------------------------------------------------- f05
def f05():
    """シールの天秤 ── 換気圧とリーク圧"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "換気が成り立つ条件 ── 二つの圧のあいだで")

    BX, BY, BW, BH = 60, 140, 700, 420
    cv.box(BX, BY, BW, 70, fc=BLUE, ec=BLUE, lw=0, radius=8)
    cv.text(BX + BW / 2, BY + 35, "必要換気圧（上がる側）", size=13.5,
            color="white", weight="bold")
    UP = ["気腹・頭低位", "肥満・胸壁コンプライアンス低下", "気管支痙攣",
          "肺水腫・無気肺", "腹腔内圧の上昇", "一回換気量を増やす設定"]
    for i, t in enumerate(UP):
        y = BY + 84 + i * 54
        cv.box(BX, y, BW, 46, fc=FC[BLUE], ec=BLUE, lw=1.5, radius=7)
        s, ln = fitlines(cv, [t], BW - 34, 11.4, floor=9.2)
        cv.block(BX, y + (46 - LH(s, 1.4) * len(ln)) / 2, BW, ln, s)

    CX = BX + BW + 60
    cv.box(CX, BY, BW, 70, fc=GREEN, ec=GREEN, lw=0, radius=8)
    cv.text(CX + BW / 2, BY + 35, "シールが耐える圧（限界側）", size=13.5,
            color="white", weight="bold")
    DN = ["器具の種類と設計", "サイズの適合", "挿入の深さと回旋",
          "カフ量とカフ圧", "頭頸部の位置（屈曲・伸展）", "咽頭の解剖と粘膜の状態"]
    for i, t in enumerate(DN):
        y = BY + 84 + i * 54
        cv.box(CX, y, BW, 46, fc=FC[GREEN], ec=GREEN, lw=1.5, radius=7)
        s, ln = fitlines(cv, [t], BW - 34, 11.4, floor=9.2)
        cv.block(CX, y + (46 - LH(s, 1.4) * len(ln)) / 2, BW, ln, s)

    Y2 = BY + BH + 40
    cv.box(60, Y2, W - 120, 110, fc="white", ec=NAVY, lw=2.0, radius=8)
    cv.text(W / 2, Y2 + 40,
            "必要換気圧  ＜  咽頭リーク圧　であるあいだ、換気は成り立つ",
            size=15.0, color=NAVY, weight="bold")
    cv.text(W / 2, Y2 + 78,
            "この不等号が崩れると、ガスは咽頭から漏れ、食道へ向かう",
            size=11.6, color=GREY)

    msg(cv, Y2 + 138,
        "リークが出たとき、崩れたのが左辺なのか右辺なのかを先に決める")
    save(cv, P("f05_seal_balance.png"))


# ---------------------------------------------------------------- f06
def f06():
    """カフ圧の階段"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "カフ圧 ── 「最大注入量」は最適シールではない")

    X0, X1, AY = 160, 1380, 620
    cv.arrow((X0, AY), (X0, 180), color=GREY, lw=2.4, head=12)
    cv.text(X0 - 24, 200, "カフ内圧", size=11.5, color=GREY, ha="right")
    cv.arrow((X0, AY), (X1 + 20, AY), color=GREY, lw=2.4, head=12)

    ZONES = [
        (0.00, 0.34, "低すぎる", "リーク・胃送気・換気量不足", ORANGE, 0.72),
        (0.34, 0.68, "添付文書の範囲内で\n最小有効圧", "シールは足り、粘膜は生きる",
         GREEN, 0.34),
        (0.68, 1.00, "高すぎる", "粘膜虚血・神経障害・咽頭痛", RED, 0.14),
    ]
    for a, b, lab, note, color, ytop in ZONES:
        xa, xb = X0 + (X1 - X0) * a, X0 + (X1 - X0) * b
        ya = 180 + (AY - 180) * ytop
        cv.box(xa + 6, ya, xb - xa - 12, AY - ya - 6, fc=FC[color], ec=color,
               lw=1.8, radius=8)
        cv.text((xa + xb) / 2, ya + 52, lab, size=13.0, color=color,
                weight="bold", linespacing=1.5)
        s, ln = fitlines(cv, [note], xb - xa - 44, 11.0, floor=9.0)
        cv.block(xa + 22, AY - 20 - LH(s, 1.5) * len(ln), xb - xa - 44, ln, s,
                 color=INK)

    Y2 = AY + 60
    CARDS = [
        ("測る", ["マノメーターで測る。", "注入量では圧はわからない"], BLUE),
        ("上限を決めておく", ["添付文書の範囲を超えない。", "多くは60 cmH₂O が上限"],
         GREEN),
        ("途中で測り直す", ["笑気はカフ圧を上げる。", "長時間症例では再評価する"],
         ORANGE),
        ("ゲル型でも油断しない", ["体温で軟化し位置が動く。", "リークとカプノグラムで追う"],
         PURPLE),
    ]
    CW, GAP = 344, 18
    for i, (head, lines, color) in enumerate(CARDS):
        x = 52 + i * (CW + GAP)
        card(cv, x, Y2, CW, head, lines, color, head_size=12.0,
             body_size=10.4, lh=1.7)

    msg(cv, Y2 + 268,
        "咽頭粘膜の灌流は低い圧で止まる。シールを買うために粘膜を売ってはならない",
        fc="#fceeec", ec=RED, tc=RED)
    save(cv, P("f06_cuff_pressure.png"))


# ---------------------------------------------------------------- f07
def f07():
    """誤嚥リスクの三軸"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "誤嚥リスクは三つの軸で見積もる ── 器具の世代は四つ目に来る")

    CW, GAP, X0, Y0 = 460, 40, 52, 132
    AX = [
        ("① 患者の側", RED,
         ["絶食が守られていない", "腸閉塞・胃内容の停滞",
          "妊娠後期", "高度肥満", "症候性の胃食道逆流",
          "食道の手術・狭窄の既往", "意識障害・球麻痺"]),
        ("② 手術と体位の側", ORANGE,
         ["緊急手術", "気腹・頭低位", "腹腔内圧が上がる操作",
          "腹臥位・側臥位", "長時間手術", "上腹部の操作",
          "手術台の傾きが変わる"]),
        ("③ 麻酔手技の側", BLUE,
         ["必要換気圧が高い設定", "深い鎮静で反射が落ちている",
          "位置不良のまま維持している", "胃送気が続いている",
          "抜去のタイミングが浅い", "吸引が届いていない",
          "人手が足りていない"]),
    ]
    for i, (head, color, lines) in enumerate(AX):
        x = X0 + i * (CW + GAP)
        card(cv, x, Y0, CW, head, lines, color, head_size=14.0,
             body_size=11.2, lh=1.8)

    Y2 = Y0 + 560
    cv.box(52, Y2, W - 104, 150, fc="white", ec=NAVY, lw=2.2, radius=8)
    cv.text(W / 2, Y2 + 46, "三つの軸を足してから、器具を選ぶ", size=15.0,
            color=NAVY, weight="bold")
    cv.text(W / 2, Y2 + 96,
            "第2世代を選ぶことは、リスクの見積もりを下げる理由にはならない",
            size=12.0, color=GREY)

    msg(cv, Y2 + 180,
        "「第2世代だから使える」ではなく「この三軸が軽いから使える」と言葉にする")
    save(cv, P("f07_aspiration_risk.png"))


# ---------------------------------------------------------------- f08
def f08():
    """位置確認は束で行う"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "位置の確認は、ひとつずつではなく束で行う")

    ITEMS = [
        ("換気抵抗", "低い", "押す手が軽いか", BLUE),
        ("カプノグラム", "安定した矩形波", "第Ⅲ相の平坦部があるか", GREEN),
        ("一回換気量", "設定どおり入る", "呼気側で測っているか", ORANGE),
        ("咽頭リーク圧", "十分に高い", "絶対値ではなくトレンド", PURPLE),
        ("聴診", "両側の呼吸音", "左右差と上腹部も聴く", TEAL),
        ("胃ドレーン", "胃管が容易に通る", "抵抗があれば押さない", RED),
    ]
    CW, RH, GAP, X0, Y0 = 696, 118, 24, 52, 140
    for i, (name, good, check, color) in enumerate(ITEMS):
        col, row = i % 2, i // 2
        x = X0 + col * (CW + GAP)
        y = Y0 + row * (RH + GAP)
        LW = 208
        cv.box(x, y, CW, RH, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.rect(x + 6, y + 6, LW, RH - 12, fc=color, ec="none")
        s, ln = fitlines(cv, [name], LW - 22, 11.6, weight="bold", floor=8.6)
        cv.block(x + 6, y + (RH - LH(s, 1.4) * len(ln)) / 2, LW, ln, s,
                 color="white", weight="bold")
        IW = CW - LW - 36
        s2, ln2 = fitlines(cv, [good], IW, 12.2, weight="bold", floor=9.4)
        cv.block(x + LW + 20, y + 22, IW, ln2, s2, color=color,
                 weight="bold", ha="left")
        s3, ln3 = fitlines(cv, [check], IW, 10.6, floor=8.8)
        cv.block(x + LW + 20, y + 22 + LH(s2, 1.45) * len(ln2) + 4, IW,
                 ln3, s3, color=GREY, ha="left")

    Y2 = Y0 + 3 * (RH + GAP) + 24
    cv.box(52, Y2, W - 104, 226, fc=FC[NAVY], ec=NAVY, lw=2.0, radius=8)
    cv.text(W / 2, Y2 + 44, "ファイバー所見（Brimacombe–Berry 分類）",
            size=13.5, color=NAVY, weight="bold")
    GR = [("Grade 1", "声帯が見えない"), ("Grade 2", "声帯と喉頭蓋前面"),
          ("Grade 3", "喉頭蓋後面が半分未満"),
          ("Grade 4", "声帯のみが見える")]
    GW, GG = 326, 16
    for i, (g, d) in enumerate(GR):
        x = 80 + i * (GW + GG)
        color = GREEN if i == 3 else GREY
        cv.box(x, Y2 + 74, GW, 116, fc="white", ec=color, lw=1.8, radius=8)
        cv.text(x + GW / 2, Y2 + 106, g, size=13.0, color=color,
                weight="bold")
        s, ln = fitlines(cv, [d], GW - 28, 10.6, floor=8.8)
        cv.block(x + 14, Y2 + 126, GW - 28, ln, s, color=INK)

    msg(cv, Y2 + 250,
        "Grade 4 は理想的な視野のひとつであって、安全の証明ではない",
        fc="#fceeec", ec=RED, tc=RED)
    save(cv, P("f08_confirm_bundle.png"))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08):
        fn()
        print("ok", fn.__name__)
