# -*- coding: utf-8 -*-
"""㉙ 図版 f09〜f15（維持・抜去・トラブルの読み方）"""
import os

from fig29common import (Canvas, LH, textbox, cap, msg, fitlines, card, band,
                         stat, tick_axis, outpath, save, W, TEAL, FC,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)

OUT = outpath()


def P(n):
    return os.path.join(OUT, n)


def bullets(cv, items, w, size, floor=8.8):
    """「・」つきの箇条書きを、折り返しても崩れない行の並びにして返す。

    fitlines に生の項目を渡して結果へ一律に「・」を足すと、折り返された
    2行目にも「・」が付いて項目数が水増しされる。先に1項目ずつ折り返す。
    """
    s = max(cv.fit_size(items, w, size, min_size=floor), size * 0.92)   # 縮めすぎず、長い項目は折り返す
    out = []
    for it in items:
        ln = cv.wrap("・" + it, w, s)
        out.append(ln[0])
        out.extend("　" + x for x in ln[1:])
    return s, out


# ---------------------------------------------------------------- f09
def f09():
    """気腹と頭低位が何を動かすか"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "気腹と頭低位 ── シールに何が起きているのか")

    CHAIN = [
        ("気腹・頭低位", NAVY),
        ("横隔膜が頭側へ押し上がる", BLUE),
        ("胸腹部のコンプライアンス低下", BLUE),
        ("同じ一回換気量に、より高い圧が要る", ORANGE),
        ("必要換気圧が咽頭リーク圧に近づく", ORANGE),
        ("咽頭からの漏れ・食道へのガス流入", RED),
        ("胃膨満 → さらに横隔膜が上がる", RED),
    ]
    BW, BH, GAP, X0, Y0 = 880, 96, 26, 60, 140
    for i, (t, color) in enumerate(CHAIN):
        y = Y0 + i * (BH + GAP)
        fc = FC[color]
        cv.box(X0, y, BW, BH, fc=fc, ec=color, lw=1.9, radius=8)
        s, ln = fitlines(cv, [t], BW - 44, 12.6, weight="bold", floor=9.6)
        cv.block(X0, y + (BH - LH(s, 1.5) * len(ln)) / 2, BW, ln, s,
                 color=color, weight="bold")
        if i < len(CHAIN) - 1:
            cv.arrow((X0 + BW / 2, y + BH + 3),
                     (X0 + BW / 2, y + BH + GAP - 3),
                     color=GREY, lw=2.4, head=12)

    # 最後の行から2行目へ戻る「悪循環」の矢印
    ytop = Y0 + 3 * (BH + GAP) + BH / 2
    ybot = Y0 + 6 * (BH + GAP) + BH / 2
    cv.ax.plot([X0 + BW + 26, X0 + BW + 80, X0 + BW + 80, X0 + BW + 26],
               [ybot, ybot, ytop, ytop], color=RED, lw=2.4, zorder=3)
    cv.arrow((X0 + BW + 40, ytop), (X0 + BW + 22, ytop), color=RED, lw=2.4,
             head=12)
    cv.text(X0 + BW + 96, (ytop + ybot) / 2, "悪循環", size=12.5, color=RED,
            weight="bold", ha="left")

    XR, RW = X0 + BW + 210, 340
    CH = ["気腹圧はいくつか", "手術台は何度傾いたか",
          "傾けた時刻とリークの時刻", "筋弛緩は足りているか",
          "胃ドレーンは引けているか"]
    s, ln = bullets(cv, CH, RW - 44, 11.0)
    rh = 76 + LH(s, 1.9) * len(ln)
    cv.box(XR, Y0, RW, rh, fc="white", ec=GREEN, lw=2.0, radius=8)
    cv.text(XR + RW / 2, Y0 + 40, "先に確かめる", size=13.5, color=GREEN,
            weight="bold")
    cv.block(XR + 22, Y0 + 62, RW - 44, ln, s, ha="left", lh=LH(s, 1.9))

    msg(cv, Y0 + 7 * (BH + GAP) + 6,
        "リークが出たとき、器具は何も変わっていない。変わったのは患者の力学である")
    save(cv, P("f09_pneumoperitoneum.png"))


# ---------------------------------------------------------------- f10
def f10():
    """2025-JSA 覚醒・抜管の四つの MUST"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "覚醒・抜去の四つの MUST（2025-JSA ガイドライン）")

    MUST = [
        ("① 筋収縮回復", "筋弛緩モニタで確認する", BLUE),
        ("② 自発呼吸回復", "呼吸指示なしで呼吸している", GREEN),
        ("③ 従命可能", "開口維持・挺舌・離握手で確かめる", ORANGE),
        ("④ 抜去後の上気道維持", "抜いた直後に閉塞がないか見る", PURPLE),
    ]
    CW, GAP, X0, Y0 = 344, 18, 52, 136
    for i, (head, body, color) in enumerate(MUST):
        x = X0 + i * (CW + GAP)
        card(cv, x, Y0, CW, head, [body], color, head_size=12.6,
             body_size=10.8, lh=1.7, body_h=104)

    Y1 = Y0 + 230
    cv.text(52, Y1, "達成できていないときの分かれ道", size=13.0, color=NAVY,
            weight="bold", ha="left")

    BR = [
        ("浅麻酔で体動・気道反射", "器具を抜かずに再鎮静する", RED),
        ("深麻酔で抜きたい", "声門上器具を活用する（推奨）", GREEN),
        ("上気道浮腫が疑わしい", "カフリークテストで評価する", ORANGE),
        ("手術室で四項目が揃わない", "抜去せず退室し、体制を整えて抜く", PURPLE),
    ]
    BW, BH, BG, Y2 = W - 104, 104, 16, Y1 + 34
    for i, (cond, act, color) in enumerate(BR):
        y = Y2 + i * (BH + BG)
        cv.box(52, y, BW, BH, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.rect(58, y + 6, 470, BH - 12, fc=color, ec="none")
        s, ln = fitlines(cv, [cond], 440, 12.0, weight="bold", floor=9.4)
        cv.block(58, y + (BH - LH(s, 1.45) * len(ln)) / 2, 470, ln, s,
                 color="white", weight="bold")
        cv.arrow((540, y + BH / 2), (586, y + BH / 2), color=color, lw=2.4,
                 head=12)
        s2, ln2 = fitlines(cv, [act], BW - 570, 12.4, weight="bold",
                           floor=9.6)
        cv.block(600, y + (BH - LH(s2, 1.45) * len(ln2)) / 2, BW - 570, ln2,
                 s2, color=color, weight="bold", ha="left")

    Y3 = Y2 + 4 * (BH + BG) + 14
    cv.box(52, Y3, W - 104, 150, fc="white", ec=NAVY, lw=2.2, radius=8)
    cv.text(W / 2, Y3 + 44, "抜去は「終わったあとの作業」ではない", size=14.5,
            color=NAVY, weight="bold")
    cv.text(W / 2, Y3 + 96,
            "浅い麻酔深度での抜去操作は、それ自体が喉頭への刺激になる",
            size=11.8, color=GREY)

    msg(cv, Y3 + 180,
        "覚醒後抜管が原則。深麻酔で抜くと決めたなら、声門上器具を残す道が用意されている")
    save(cv, P("f10_four_musts.png"))


# ---------------------------------------------------------------- f11
def f11():
    """所見 → 原因 → 確認 → 行動"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "順番を守る ── 所見から入り、行動で出る")

    STEPS = [
        ("所見", "いま手に入っているもの",
         ["リークの音", "気道内圧", "一回換気量",
          "カプノグラムの形", "胸郭の動き"], BLUE),
        ("原因の候補", "まだ決めていないもの",
         ["器具の位置", "サイズ・カフ", "必要換気圧の上昇",
          "機能的閉塞", "回路と肺"], ORANGE),
        ("確認", "候補をふるいにかけるもの",
         ["口腔内を見る", "聴診する", "時間関係を追う",
          "回路を遡る", "胃ドレーンを引く"], GREEN),
        ("行動", "はじめて手を動かすもの",
         ["酸素化を保つ", "位置を直す", "設定を変える",
          "応援を呼ぶ", "次の気道戦略へ"], PURPLE),
    ]
    CW, GAP, X0, Y0 = 330, 38, 52, 150
    for i, (head, sub, lines, color) in enumerate(STEPS):
        x = X0 + i * (CW + GAP)
        cv.box(x, Y0, CW, 66, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + CW / 2, Y0 + 33, head, size=15.0, color="white",
                weight="bold")
        s, ln = fitlines(cv, [sub], CW - 20, 10.6, floor=8.8)
        cv.block(x, Y0 + 76, CW, ln, s, color=GREY)
        s2, ln2 = bullets(cv, lines, CW - 56, 11.2, floor=9.2)
        bh = 44 + LH(s2, 1.85) * len(ln2)
        cv.box(x, Y0 + 112, CW, bh, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.block(x + 28, Y0 + 134, CW - 56, ln2, s2,
                 ha="left", lh=LH(s2, 1.85))
        if i < 3:
            cv.arrow((x + CW + 6, Y0 + 33), (x + CW + GAP - 6, Y0 + 33),
                     color=GREY, lw=2.6, head=13)

    Y1 = Y0 + 112 + 44 + LH(11.2, 1.85) * 5 + 52
    cv.box(52, Y1, W - 104, 128, fc="#fceeec", ec=RED, lw=2.0, radius=8)
    cv.text(W / 2, Y1 + 42, "行動から入ると、何が起きるか", size=13.5,
            color=RED, weight="bold")
    cv.text(W / 2, Y1 + 88,
            "確かめていない原因を、すでに決めたことにしてしまう",
            size=12.0, color=INK)

    msg(cv, Y1 + 158,
        "「SAD 不良」と名づけた瞬間に、回路も肺も視野から消える",
        fc="#fceeec", ec=RED, tc=RED)
    save(cv, P("f11_finding_to_action.png"))


# ---------------------------------------------------------------- f12
def f12():
    """リークをどう読むか"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "大きなリークを、二つの側に振り分ける")

    TOP_W, X0, Y0 = 800, 360, 130
    cv.box(X0, Y0, TOP_W, 92, fc=NAVY, ec=NAVY, lw=0, radius=8)
    t = "リークが大きい／一回換気量が入らない"
    ts = cv.fit_size([t], TOP_W - 60, 14.5, weight="bold")
    cv.text(X0 + TOP_W / 2, Y0 + 46, t, size=ts, color="white",
            weight="bold")

    YQ = Y0 + 130
    cv.box(330, YQ, 860, 80, fc="white", ec=GREY, lw=2.0, radius=8)
    cv.text(760, YQ + 40, "いつから？　何をした直後から？", size=13.0,
            color=INK, weight="bold")

    YB = YQ + 130
    CW = 690
    LX, RX = 60, 60 + CW + 50
    cv.arrow((760, YQ + 84), (LX + CW / 2, YB - 8), color=BLUE, lw=2.4,
             head=12)
    cv.arrow((760, YQ + 84), (RX + CW / 2, YB - 8), color=ORANGE, lw=2.4,
             head=12)

    LEFT = ("器具の側が変わった", BLUE,
            ["挿入直後から漏れている", "カフ量・カフ圧が足りない",
             "サイズが合っていない", "浅い・深い・回っている",
             "頭頸部の位置が変わった", "分泌物・血液が付着した"])
    RIGHT = ("患者の側が変わった", ORANGE,
             ["気腹を開始した", "頭低位・体位を変えた",
              "気管支痙攣が起きた", "筋弛緩が切れてきた",
              "肺コンプライアンスが落ちた", "一回換気量の設定を上げた"])
    for x, (head, color, lines) in ((LX, LEFT), (RX, RIGHT)):
        cv.box(x, YB, CW, 74, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + CW / 2, YB + 37, head, size=14.0, color="white",
                weight="bold")
        s, ln = bullets(cv, lines, CW - 80, 11.6, floor=9.4)
        bh = 42 + LH(s, 1.9) * len(ln)
        cv.box(x, YB + 84, CW, bh, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.block(x + 40, YB + 106, CW - 80, ln, s,
                 ha="left", lh=LH(s, 1.9))

    Y2 = YB + 84 + 42 + LH(11.6, 1.9) * 6 + 36
    cv.box(60, Y2, W - 120, 132, fc="white", ec=GREEN, lw=2.2, radius=8)
    cv.text(W / 2, Y2 + 44, "どちらでも、最初にすることは同じ", size=14.0,
            color=GREEN, weight="bold")
    cv.text(W / 2, Y2 + 92,
            "酸素化を保つ → 回路を確認 → 頭頸部の位置と下顎挙上 → 位置とカフの最適化",
            size=12.0, color=INK)

    msg(cv, Y2 + 162,
        "反射的にカフを足すのは、原因を「シール不足」と決めてしまったということ")
    save(cv, P("f12_reading_leak.png"))


# ---------------------------------------------------------------- f13
def f13():
    """気道内圧が高いときの分岐"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "気道内圧が高い ── 三つの場所に分けて考える")

    COLS = [
        ("機械的な閉塞", RED,
         ["咬み込み", "器具内腔の折れ曲がり", "分泌物・血液による閉塞",
          "喉頭蓋の巻き込み", "回路側のバルブ閉塞"],
         "口腔内を見る・器具を吸引する"),
        ("機能的な閉塞", ORANGE,
         ["喉頭痙攣", "気管支痙攣", "声門上の軟部組織の虚脱",
          "麻酔深度が浅い", "筋弛緩が不十分"],
         "吸気性か呼気性か・喘鳴・時間関係"),
        ("肺と胸壁の問題", BLUE,
         ["肺コンプライアンス低下", "気胸・大量胸水", "無気肺",
          "高度肥満・気腹・体位", "腹腔内圧の上昇"],
         "気道内圧と換気量の関係・聴診"),
    ]
    CW, GAP, X0, Y0 = 460, 40, 52, 140
    for i, (head, color, lines, check) in enumerate(COLS):
        x = X0 + i * (CW + GAP)
        cv.box(x, Y0, CW, 74, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + CW / 2, Y0 + 37, head, size=14.5, color="white",
                weight="bold")
        s, ln = bullets(cv, lines, CW - 70, 11.2, floor=9.0)
        bh = 40 + LH(s, 1.9) * len(ln)
        cv.box(x, Y0 + 84, CW, bh, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.block(x + 34, Y0 + 104, CW - 70, ln, s,
                 ha="left", lh=LH(s, 1.9))
        cv.box(x, Y0 + 84 + bh + 16, CW, 96, fc="white", ec=color, lw=1.8,
               radius=8)
        cv.text(x + CW / 2, Y0 + 84 + bh + 42, "確かめ方", size=10.6,
                color=GREY, weight="bold")
        s2, ln2 = fitlines(cv, [check], CW - 40, 11.2, weight="bold",
                           floor=9.0)
        cv.block(x, Y0 + 84 + bh + 54, CW, ln2, s2, color=color,
                 weight="bold")

    Y2 = Y0 + 84 + (40 + LH(11.2, 1.9) * 5) + 16 + 96 + 40
    cv.box(52, Y2, W - 104, 150, fc=FC[NAVY], ec=NAVY, lw=2.0, radius=8)
    cv.text(W / 2, Y2 + 48, "同じ「押す手が重い」でも、直し方は三つとも違う",
            size=14.5, color=NAVY, weight="bold")
    cv.text(W / 2, Y2 + 100,
            "機械的なら取り除く。機能的なら反射を断つ。肺胸壁なら設定と病態を扱う",
            size=11.8, color=INK)

    msg(cv, Y2 + 180,
        "分類は、酸素化に余裕があるあいだの作業である。余裕が無ければ次の段階へ",
        fc="#fceeec", ec=RED, tc=RED)
    save(cv, P("f13_high_pressure.png"))


# ---------------------------------------------------------------- f14
def f14():
    """カプノグラムの読み分け"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "カプノグラムを四つの形で読む")

    import numpy as np

    def wave(x0, y0, w, h, kind, color):
        """箱の中に波形を描く"""
        t = np.linspace(0, 3.0, 900)
        v = np.zeros_like(t)
        for k in range(3):
            ph = t - k
            m = (ph >= 0.05) & (ph < 0.55)
            if kind == "normal":
                v[m] = np.clip((ph[m] - 0.05) / 0.06, 0, 1) * 0.92 + \
                    (ph[m] - 0.05) * 0.10
            elif kind == "small":
                v[m] = (np.clip((ph[m] - 0.05) / 0.06, 0, 1) * 0.92 +
                        (ph[m] - 0.05) * 0.10) * 0.45
            elif kind == "shark":
                v[m] = (1 - np.exp(-(ph[m] - 0.05) * 3.0)) * 1.00
            elif kind == "flat":
                v[m] = 0.0
        cv.ax.plot(x0 + t / 3.0 * w, y0 + h - v * h * 0.86,
                   color=color, lw=2.6, zorder=5)
        cv.ax.plot([x0, x0 + w], [y0 + h, y0 + h], color="#c8ced6", lw=1.4,
                   zorder=3)

    ITEMS = [
        ("安定した矩形波", "normal", GREEN,
         "換気は届いている。位置の確認は、ここから始める"),
        ("小さいが形は保つ", "small", ORANGE,
         "一回換気量が足りない。リーク・位置不良・設定を疑う"),
        ("立ち上がりが斜めになる", "shark", BLUE,
         "呼出が遅れている。気管支痙攣・器具内腔の狭窄"),
        ("波形が消える", "flat", RED,
         "回路離断・完全閉塞・重症の喉頭痙攣・心拍出量の低下"),
    ]
    CW, RH, GAP, X0, Y0 = 712, 250, 28, 52, 136
    for i, (name, kind, color, note) in enumerate(ITEMS):
        col, row = i % 2, i // 2
        x = X0 + col * (CW + GAP)
        y = Y0 + row * (RH + GAP)
        cv.box(x, y, CW, RH, fc="white", ec=color, lw=2.0, radius=8)
        cv.rect(x + 6, y + 6, CW - 12, 54, fc=color, ec="none")
        s, ln = fitlines(cv, [name], CW - 60, 13.0, weight="bold", floor=10.0)
        cv.block(x + 6, y + 6 + (54 - LH(s, 1.4) * len(ln)) / 2, CW - 12, ln,
                 s, color="white", weight="bold")
        wave(x + 40, y + 78, CW - 80, 100, kind, color)
        s2, ln2 = fitlines(cv, [note], CW - 56, 11.2, floor=9.0)
        cv.block(x + 28, y + 190, CW - 56, ln2, s2, ha="left",
                 lh=LH(s2, 1.55))

    Y2 = Y0 + 2 * (RH + GAP) + 24
    cv.box(52, Y2, W - 104, 172, fc=FC[NAVY], ec=NAVY, lw=2.0, radius=8)
    cv.text(W / 2, Y2 + 46, "波形は「器具の成績表」ではない", size=14.5,
            color=NAVY, weight="bold")
    cv.text(W / 2, Y2 + 96,
            "肺へガスが届き、そこから戻ってきたことだけを示している。",
            size=11.8, color=INK)
    cv.text(W / 2, Y2 + 132,
            "だから、消えたときに疑うべき場所は器具だけではない。",
            size=11.8, color=INK)

    msg(cv, Y2 + 200,
        "波形の消失は、緊急評価の起点であって、診断名ではない")
    save(cv, P("f14_capnogram.png"))


# ---------------------------------------------------------------- f15
def f15():
    """喉頭痙攣の反射弓と四つの介入"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "喉頭痙攣の反射弓と、断ち切る四か所")

    ARC = [
        ("刺激", ["血液・分泌物・逆流物", "吸引・咽頭操作",
                "浅麻酔下の器具操作"], RED),
        ("求心路", ["上喉頭神経内枝", "（迷走神経）"], ORANGE),
        ("脳幹", ["反射の統合"], PURPLE),
        ("遠心路", ["反回神経", "（迷走神経）"], BLUE),
        ("声門閉鎖", ["内喉頭筋の内転", "外側輪状披裂筋ほか"], NAVY),
    ]
    AW, AG, X0, Y0 = 268, 20, 60, 140
    fitted = [fitlines(cv, ln, AW - 30, 10.4, floor=8.6)
              for _, ln, _ in ARC]
    AH = max(58 + LH(s, 1.6) * len(ln) + 18 for s, ln in fitted)
    for i, (head, lines, color) in enumerate(ARC):
        x = X0 + i * (AW + AG)
        s, ln = fitted[i]
        cv.box(x, Y0, AW, AH, fc=FC[color], ec=color, lw=1.9, radius=8)
        cv.text(x + AW / 2, Y0 + 36, head, size=13.5, color=color,
                weight="bold")
        cv.block(x + 15, Y0 + 58, AW - 30, ln, s, lh=LH(s, 1.6))
        if i < 4:
            cv.arrow((x + AW + 3, Y0 + AH / 2), (x + AW + AG - 3, Y0 + AH / 2),
                     color=GREY, lw=2.4, head=11)

    Y1 = Y0 + AH + 50
    ACTS = [
        ("①", "刺激を止める",
         "手術操作・吸引・器具操作を止め、応援を呼び、100% 酸素",
         "求心路への入力を断つ", RED),
        ("②", "上気道を開ける",
         "口腔内を確認し下顎挙上。密着マスクで穏やかな CPAP",
         "声門上の閉塞成分を減らす", ORANGE),
        ("③", "麻酔を深くする",
         "静脈麻酔薬を少量ずつ追加する（用量は施設の手順書に従う）",
         "反射の閾値を上げる", PURPLE),
        ("④", "筋弛緩薬",
         "低酸素・徐脈が進むなら、速効性筋弛緩薬をためらわない",
         "遠心路の出力を断つ", BLUE),
    ]
    BH, BG = 118, 16
    for i, (no, head, body, why, color) in enumerate(ACTS):
        y = Y1 + i * (BH + BG)
        cv.box(60, y, W - 120, BH, fc=FC[color], ec=color, lw=1.9, radius=8)
        cv.rect(66, y + 6, 74, BH - 12, fc=color, ec="none")
        cv.text(66 + 37, y + BH / 2, no, size=20.0, color="white",
                weight="bold")
        s, ln = fitlines(cv, [head], 300, 13.5, weight="bold", floor=10.4)
        cv.block(156, y + (BH - LH(s, 1.45) * len(ln)) / 2, 300, ln, s,
                 color=color, weight="bold", ha="left")
        s2, ln2 = fitlines(cv, [body], 640, 11.4, floor=9.2)
        cv.block(478, y + (BH - LH(s2, 1.55) * len(ln2)) / 2, 640, ln2, s2,
                 ha="left")
        s3, ln3 = fitlines(cv, [why], 300, 11.0, weight="bold", floor=9.0)
        cv.block(1140, y + (BH - LH(s3, 1.5) * len(ln3)) / 2, 300, ln3, s3,
                 color=GREY, weight="bold", ha="left")

    Y2 = Y1 + 4 * (BH + BG) + 14
    cv.box(60, Y2, W - 120, 164, fc="white", ec=NAVY, lw=2.2, radius=8)
    cv.text(W / 2, Y2 + 44, "二重の閉塞が起きている", size=14.0, color=NAVY,
            weight="bold")
    cv.text(W / 2, Y2 + 94,
            "声門が閉じるだけでなく、強い吸気努力が喉頭内を陰圧にして、",
            size=11.6, color=INK)
    cv.text(W / 2, Y2 + 128,
            "声門上の軟部組織を内側へ引き込む。だから②に生理学的な意味がある。",
            size=11.6, color=INK)

    msg(cv, Y2 + 192,
        "順番は覚えるものではない。反射のどこを断っているかで決まっている")
    save(cv, P("f15_reflex_arc.png"))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f09, f10, f11, f12, f13, f14, f15):
        fn()
        print("ok", fn.__name__)
