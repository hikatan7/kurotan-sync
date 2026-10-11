# -*- coding: utf-8 -*-
"""㉙ 図版 f16〜f22（鑑別・合併症・危機・導管）"""
import os

from fig29common import (Canvas, LH, textbox, cap, msg, fitlines, card, band,
                         stat, tick_axis, outpath, save, W, TEAL, FC,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)
from fig29b import bullets

OUT = outpath()


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f16
def f16():
    """換気できないときの五つの候補"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "「空気が入らない」の五つの候補 ── 病態生理で見分ける")

    ROWS = [
        ("喉頭痙攣", "刺激の直後に急な吸気性閉塞。努力性呼吸があるのに波形が消える",
         "機能的な声門閉鎖", RED),
        ("舌根沈下・咽頭虚脱", "下顎挙上と体位で改善しやすい",
         "声門より上の解剖学的閉塞", ORANGE),
        ("器具の位置不良・咬み込み", "リークまたは高抵抗。胸郭運動が不良",
         "気流経路の機械的障害", BLUE),
        ("気管支痙攣", "呼気延長、両側性の笛声音、呼気相の波形変形",
         "末梢気道抵抗の増大", GREEN),
        ("肺コンプライアンス低下", "高い気道内圧と小さい一回換気量",
         "肺・胸壁側の力学的問題", PURPLE),
    ]
    L, C1, C2, GAP, TOP, RH = 52, 366, 630, 18, 190, 116
    C3 = W - 104 - C1 - C2 - 2 * GAP
    HEAD = [("候補", C1), ("示唆する所見", C2), ("病態生理の違い", C3)]
    x = L
    for h, w in HEAD:
        cv.box(x, TOP - 66, w, 54, fc=NAVY, ec=NAVY, lw=0, radius=8)
        cv.text(x + w / 2, TOP - 39, h, size=12.5, color="white",
                weight="bold")
        x += w + GAP

    for i, (name, sign, mech, color) in enumerate(ROWS):
        y = TOP + i * (RH + 12)
        cv.box(L, y, C1, RH, fc=color, ec=color, lw=0, radius=8)
        s, ln = fitlines(cv, [name], C1 - 30, 12.4, weight="bold", floor=9.4)
        cv.block(L, y + (RH - LH(s, 1.45) * len(ln)) / 2, C1, ln, s,
                 color="white", weight="bold")
        x2 = L + C1 + GAP
        cv.box(x2, y, C2, RH, fc=FC[color], ec=color, lw=1.7, radius=8)
        s2, ln2 = fitlines(cv, [sign], C2 - 44, 11.4, floor=9.2)
        cv.block(x2 + 22, y + (RH - LH(s2, 1.6) * len(ln2)) / 2, C2 - 44, ln2,
                 s2, ha="left")
        x3 = x2 + C2 + GAP
        cv.box(x3, y, C3, RH, fc="white", ec=color, lw=1.8, radius=8)
        s3, ln3 = fitlines(cv, [mech], C3 - 36, 11.6, weight="bold",
                           floor=9.0)
        cv.block(x3, y + (RH - LH(s3, 1.5) * len(ln3)) / 2, C3, ln3, s3,
                 color=color, weight="bold")

    y = TOP + len(ROWS) * (RH + 12) + 18
    cv.box(L, y, W - 104, 140, fc=FC[NAVY], ec=NAVY, lw=2.0, radius=8)
    cv.text(W / 2, y + 44, "見分けの三つの手がかり", size=14.0, color=NAVY,
            weight="bold")
    cv.text(W / 2, y + 96,
            "①吸気性か呼気性か　②聴診で何が聞こえるか　③何の直後に始まったか",
            size=12.2, color=INK)

    msg(cv, y + 168,
        "胸とお腹は動いているのに空気が入らない ── これは声門そのものが閉じている",
        fc="#fceeec", ec=RED, tc=RED)
    save(cv, P("f16_differential.png"))


# ---------------------------------------------------------------- f17
def f17():
    """陰圧性肺水腫の成り立ち"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "解除できても終わりではない ── 陰圧性肺水腫")

    CHAIN = [
        ("閉じた声門に向かって強く吸う", RED),
        ("胸腔内圧が大きく陰圧になる", RED),
        ("静脈還流が増え、左室後負荷も増える", ORANGE),
        ("肺毛細血管の内外で圧の差が開く", ORANGE),
        ("水が間質へ、そして肺胞へ移動する", BLUE),
        ("非心原性の肺水腫", NAVY),
    ]
    BW, BH, GAP, X0, Y0 = 820, 96, 24, 60, 140
    for i, (t, color) in enumerate(CHAIN):
        y = Y0 + i * (BH + GAP)
        cv.box(X0, y, BW, BH, fc=FC[color], ec=color, lw=1.9, radius=8)
        s, ln = fitlines(cv, [t], BW - 44, 12.6, weight="bold", floor=9.6)
        cv.block(X0, y + (BH - LH(s, 1.5) * len(ln)) / 2, BW, ln, s,
                 color=color, weight="bold")
        if i < len(CHAIN) - 1:
            cv.arrow((X0 + BW / 2, y + BH + 3),
                     (X0 + BW / 2, y + BH + GAP - 3),
                     color=GREY, lw=2.4, head=12)

    XR, RW = X0 + BW + 56, W - (X0 + BW + 56) - 56
    SIGNS = ["酸素化が改善しない", "湿性ラ音が出てくる", "泡沫状・淡血性の痰",
             "胸部画像の新しい浸潤影", "肺コンプライアンスの低下"]
    s, ln = bullets(cv, SIGNS, RW - 48, 11.4)
    h1 = 92 + LH(s, 1.95) * len(ln)
    cv.box(XR, Y0, RW, h1, fc="white", ec=RED, lw=2.0, radius=8)
    cv.text(XR + RW / 2, Y0 + 40, "閉塞解除のあとに探すもの", size=13.0,
            color=RED, weight="bold")
    cv.block(XR + 24, Y0 + 62, RW - 48, ln, s, ha="left", lh=LH(s, 1.95))

    Y2 = Y0 + h1 + 30
    ACTS = ["酸素を上げ、PEEP または CPAP をかける",
            "誤嚥・無気肺・気管支痙攣と並行して評価する",
            "改善しなければ気管挿管を含む呼吸管理へ",
            "多くは 12〜24 時間で軽快するが、観察の体制を決める"]
    s2, ln2 = bullets(cv, ACTS, RW - 48, 11.4)
    h2 = 92 + LH(s2, 1.95) * len(ln2)
    cv.box(XR, Y2, RW, h2, fc=FC[GREEN], ec=GREEN, lw=2.0, radius=8)
    cv.text(XR + RW / 2, Y2 + 40, "すること", size=13.0, color=GREEN,
            weight="bold")
    cv.block(XR + 24, Y2 + 62, RW - 48, ln2, s2, ha="left", lh=LH(s2, 1.95))

    msg(cv, max(Y0 + 6 * (BH + GAP) + 10, Y2 + h2 + 30),
        "閉塞が解けた瞬間は、観察の終わりではなく始まりである")
    save(cv, P("f17_nppe.png"))


# ---------------------------------------------------------------- f18
def f18():
    """危ない瞬間は予測できる"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "喉頭痙攣が起きやすい瞬間は、あらかじめ分かっている")

    X0, X1, AY = 120, 1400, 320
    cv.arrow((X0 - 20, AY), (X1 + 30, AY), color=GREY, lw=3.0, head=14)
    cv.text(X0 - 40, AY + 44, "麻酔の経過", size=11.5, color=GREY, ha="left")

    EVENTS = [
        (0.03, "導入直後", "意識は落ちたが\n反射はまだ残る", RED),
        (0.24, "器具の挿入", "咽頭を直接\n刺激している", ORANGE),
        (0.44, "体位変換・吸引", "器具が動き、\n分泌物が流れる", PURPLE),
        (0.64, "手術操作の開始", "痛み刺激に対して\n麻酔が浅い", BLUE),
        (0.85, "抜去の前後", "麻酔が浅く、\n口腔内に血液", RED),
    ]
    CW = 252
    for frac, head, body, color in EVENTS:
        px = X0 + (X1 - X0) * frac
        x = min(max(px - CW / 2, 40), W - CW - 40)
        cv.ax.plot([px, px], [AY - 10, AY + 10], color=color, lw=3.0, zorder=5)
        cv.arrow((px, AY - 16), (px, AY - 44), color=color, lw=2.2, head=10)
        hs, hl = fitlines(cv, [head], CW - 26, 12.4, weight="bold", floor=9.4)
        hh = 26 + LH(hs, 1.4) * len(hl)
        cv.box(x, AY - 50 - hh, CW, hh, fc=color, ec=color, lw=0, radius=8)
        cv.block(x, AY - 50 - hh + 13, CW, hl, hs, color="white",
                 weight="bold")
        cv.box(x, AY + 70, CW, 116, fc=FC[color], ec=color, lw=1.7, radius=8)
        cv.text(x + CW / 2, AY + 128, body, size=10.8, color=INK,
                linespacing=1.75)

    Y2 = AY + 230
    cv.text(52, Y2, "共通しているのは、この二つが重なる瞬間である", size=13.0,
            color=NAVY, weight="bold", ha="left")
    TWO = [("麻酔が浅い", "反射の閾値が下がっている", ORANGE),
           ("喉頭が刺激される", "血液・分泌物・器具・手術操作", RED)]
    CW2, GAP2 = 716, 18
    for i, (head, body, color) in enumerate(TWO):
        x = 52 + i * (CW2 + GAP2)
        cv.box(x, Y2 + 32, CW2, 116, fc=FC[color], ec=color, lw=2.0, radius=8)
        cv.text(x + CW2 / 2, Y2 + 68, head, size=14.5, color=color,
                weight="bold")
        s, ln = fitlines(cv, [body], CW2 - 40, 11.6, floor=9.2)
        cv.block(x, Y2 + 96, CW2, ln, s)
    cv.text(W / 2, Y2 + 176, "＋", size=22.0, color=GREY, weight="bold")

    Y3 = Y2 + 200
    cv.box(52, Y3, W - 104, 128, fc="white", ec=GREEN, lw=2.2, radius=8)
    cv.text(W / 2, Y3 + 44, "だから、予防は手技ではなく段取りになる", size=14.0,
            color=GREEN, weight="bold")
    cv.text(W / 2, Y3 + 90,
            "その瞬間の前に、口腔内を確認し、麻酔深度を確かめ、誰が何をするかを決めておく",
            size=11.8, color=INK)

    msg(cv, Y3 + 156,
        "危ない瞬間が分かっているなら、驚く必要はない。備えておけばよい")
    save(cv, P("f18_risky_moments.png"))


# ---------------------------------------------------------------- f19
def f19():
    """誤嚥を三段階に分ける"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "誤嚥を三段階に分ける ── 器具が関われるのはどこか")

    STAGES = [
        ("① 逆流", "胃内容が食道を上がってくる",
         ["胃内圧が上がる", "下部食道括約筋の機能低下",
          "胃送気で胃が張る"],
         "器具は関われない", RED),
        ("② 咽頭への到達", "逆流物が下咽頭に現れる",
         ["第2世代の胃ドレーンが逃がす", "ここで気づけることがある",
          "器具の外側を回ることもある"],
         "器具が「関われる」唯一の段", ORANGE),
        ("③ 誤嚥", "声門を越えて下気道へ入る",
         ["声門は器具の外側にある", "確実な隔離はできない",
          "気管チューブとの差はここ"],
         "器具は関われない", NAVY),
    ]
    CW, GAP, X0, Y0 = 460, 40, 52, 136
    bottom = Y0
    for i, (head, sub, lines, foot, color) in enumerate(STAGES):
        x = X0 + i * (CW + GAP)
        cv.box(x, Y0, CW, 74, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + CW / 2, Y0 + 37, head, size=15.0, color="white",
                weight="bold")
        s0, ln0 = fitlines(cv, [sub], CW - 30, 11.4, weight="bold", floor=9.2)
        cv.block(x, Y0 + 84, CW, ln0, s0, color=color, weight="bold")
        s, ln = bullets(cv, lines, CW - 64, 11.0)
        bh = 36 + LH(s, 1.9) * len(ln)
        cv.box(x, Y0 + 124, CW, bh, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.block(x + 32, Y0 + 142, CW - 64, ln, s, ha="left", lh=LH(s, 1.9))
        fc = "#eaf5ee" if i == 1 else "#fdecea"
        ec = GREEN if i == 1 else RED
        cv.box(x, Y0 + 124 + bh + 16, CW, 82, fc=fc, ec=ec, lw=1.9, radius=8)
        s2, ln2 = fitlines(cv, [foot], CW - 34, 11.6, weight="bold",
                           floor=9.0)
        cv.block(x, Y0 + 124 + bh + 16 + (82 - LH(s2, 1.45) * len(ln2)) / 2,
                 CW, ln2, s2, color=ec, weight="bold")
        bottom = max(bottom, Y0 + 124 + bh + 16 + 82)
        if i < 2:
            cv.arrow((x + CW + 6, Y0 + 37), (x + CW + GAP - 6, Y0 + 37),
                     color=GREY, lw=2.6, head=13)

    Y2 = bottom + 48
    NUM = [("約 2/10,000", "喉頭マスクでの誤嚥の頻度として\n古典的なメタ解析が示した値",
            BLUE),
           ("14 例 対 8 例", "英国の全国調査で報告された誤嚥 ──\n声門上器具と気管チューブ",
            ORANGE),
           ("37%", "英国の別の全国調査で、気道合併症の\n最多を占めた喉頭痙攣の割合",
            RED)]
    NW, NG, NH = 460, 40, 196
    for i, (v, lab, color) in enumerate(NUM):
        x = 52 + i * (NW + NG)
        cv.box(x, Y2, NW, NH, fc=FC[color], ec=color, lw=2.0, radius=8)
        vs = cv.fit_size([v], NW - 44, 25.0, weight="bold")
        cv.text(x + NW / 2, Y2 + 52, v, size=vs, color=color, weight="bold")
        ls, ll = fitlines(cv, [lab], NW - 52, 10.4, floor=8.6)
        cv.block(x + 26, Y2 + 92, NW - 52, ll, ls, color=GREY,
                 lh=LH(ls, 1.7))

    msg(cv, Y2 + NH + 26,
        "低い頻度は「起きない」ではない。しかも、その数字は待機手術のものである",
        fc="#fceeec", ec=RED, tc=RED)
    save(cv, P("f19_aspiration_stages.png"))


# ---------------------------------------------------------------- f20
def f20():
    """試行回数の階段"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "反復しないことも、ひとつの手技である")

    X0, BASE = 110, 700
    STEPS = [("1 回目", 0.22, GREEN, "見えている粘膜は無傷"),
             ("2 回目", 0.45, ORANGE, "発赤・軽い出血が出る"),
             ("3 回目", 0.70, RED, "浮腫が加わりはじめる"),
             ("4 回目以降", 1.00, NAVY, "マスク換気も挿管も難しくなる")]
    SW, SG = 320, 18
    for i, (lab, frac, color, note) in enumerate(STEPS):
        x = X0 + i * (SW + SG)
        h = 120 + (BASE - 240) * frac
        cv.box(x, BASE - h, SW, h, fc=FC[color], ec=color, lw=2.0, radius=8)
        cv.text(x + SW / 2, BASE - h + 46, lab, size=15.5, color=color,
                weight="bold")
        s, ln = fitlines(cv, [note], SW - 40, 11.2, floor=9.0)
        cv.block(x + 20, BASE - h + 76, SW - 40, ln, s, lh=LH(s, 1.6))

    cv.arrow((X0 - 40, BASE), (X0 - 40, 180), color=GREY, lw=2.4, head=12)
    cv.text(X0 - 36, 160, "その後の\n難しさ", size=11.2, color=GREY,
            ha="center", linespacing=1.6)
    cv.ax.plot([X0 - 40, X0 + 4 * SW + 3 * SG + 20], [BASE, BASE],
               color=GREY, lw=2.4, zorder=3)

    Y1 = BASE + 56
    cv.text(52, Y1, "器具ではなく、この四つを見る", size=13.5, color=NAVY,
            weight="bold", ha="left")
    FOUR = [("酸素化", "SpO₂ の値と、下がり方の速さ", BLUE),
            ("時間", "いつから換気できていないか", ORANGE),
            ("試行回数", "誰が、何回、何で試したか", PURPLE),
            ("次の一手", "覚醒か、挿管か、前頸部気道確保か", RED)]
    CW, GAP = 344, 18
    for i, (head, body, color) in enumerate(FOUR):
        x = 52 + i * (CW + GAP)
        card(cv, x, Y1 + 32, CW, head, [body], color, head_size=13.0,
             body_size=10.6, lh=1.7, body_h=100)

    Y2 = Y1 + 32 + 220
    cv.box(52, Y2, W - 104, 136, fc="white", ec=GREEN, lw=2.2, radius=8)
    cv.text(W / 2, Y2 + 44, "増やすべきなのは、試行回数ではなく人手である",
            size=14.5, color=GREEN, weight="bold")
    cv.text(W / 2, Y2 + 94,
            "早く呼んで何もなかったときのコストは、ほとんどゼロである",
            size=12.0, color=INK)

    msg(cv, Y2 + 164,
        "試行の累積は出血・浮腫・外傷を増やし、その後の換気をさらに困難にする",
        fc="#fceeec", ec=RED, tc=RED)
    save(cv, P("f20_attempts.png"))


# ---------------------------------------------------------------- f21
def f21():
    """三つの難気道アルゴリズムの中での位置"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "難気道の道筋のなかで、声門上器具はどこに置かれているか")

    COLS = [
        ("英国 DAS 2025", BLUE,
         ["Plan A ── 気管挿管", "Plan B ── 声門上器具で換気",
          "Plan C ── フェイスマスク換気", "Plan D ── 緊急前頸部気道確保"],
         "酸素を絶やさないこと、初回で成功させることを前面に置いた"),
        ("米国 ASA 2022", GREEN,
         ["換気できるかで道が分かれる", "声門上器具は救済換気の柱",
          "覚醒に戻す道を常に持つ", "意識下気道確保を考慮する条件を示す"],
         "誤嚥リスクが高い・無呼吸に耐えられない患者を名指しした"),
        ("日本 JSA-AMA", ORANGE,
         ["緑 ── 換気できている", "黄 ── 換気が怪しい",
          "赤 ── 換気できない", "赤では速やかに前頸部気道確保へ"],
         "換気の状態を色で示し、宣言する言葉を決めた"),
    ]
    CW, GAP, X0, Y0 = 460, 40, 52, 140
    bottom = Y0
    for i, (head, color, lines, note) in enumerate(COLS):
        x = X0 + i * (CW + GAP)
        cv.box(x, Y0, CW, 76, fc=color, ec=color, lw=0, radius=8)
        s0, ln0 = fitlines(cv, [head], CW - 30, 14.5, weight="bold",
                           floor=11.0)
        cv.block(x, Y0 + (76 - LH(s0, 1.4) * len(ln0)) / 2, CW, ln0, s0,
                 color="white", weight="bold")
        s, ln = bullets(cv, lines, CW - 64, 11.4)
        bh = 40 + LH(s, 2.0) * len(ln)
        cv.box(x, Y0 + 90, CW, bh, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.block(x + 32, Y0 + 110, CW - 64, ln, s, ha="left", lh=LH(s, 2.0))
        s2, ln2 = fitlines(cv, [note], CW - 44, 10.8, floor=8.8)
        nh = 34 + LH(s2, 1.65) * len(ln2)
        cv.box(x, Y0 + 90 + bh + 16, CW, nh, fc="white", ec=color, lw=1.8,
               radius=8)
        cv.block(x + 22, Y0 + 90 + bh + 16 + 17, CW - 44, ln2, s2, ha="left",
                 lh=LH(s2, 1.65))
        bottom = max(bottom, Y0 + 90 + bh + 16 + nh)

    Y2 = bottom + 46
    COMMON = ["声門上器具は「挿管できないときの妥協」ではなく、酸素化を取り戻す手段である",
              "試行回数に上限を置き、上限に達したら次へ進むと決めてある",
              "波形カプノグラフィで換気を確かめる",
              "換気できないと分かった時点で、声に出して宣言する"]
    s, ln = bullets(cv, COMMON, W - 200, 11.4)
    ch = 72 + LH(s, 1.85) * len(ln) + 20
    cv.box(52, Y2, W - 104, ch, fc=FC[NAVY], ec=NAVY, lw=2.0, radius=8)
    cv.text(W / 2, Y2 + 46, "三つに共通していること", size=14.5, color=NAVY,
            weight="bold")
    cv.block(100, Y2 + 72, W - 200, ln, s, ha="left", lh=LH(s, 1.85))

    msg(cv, Y2 + ch + 28,
        "どの指針でも、器具を正すことより酸素化を保って次へ移ることが優先される")
    save(cv, P("f21_algorithms.png"))


# ---------------------------------------------------------------- f22
def f22():
    """挿管導管として使う"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "導管として使う ── 四つのやり方と、その順位")

    WAYS = [
        ("① 盲目的に押し込む", RED,
         ["器具の内腔から気管チューブを送る", "成功率は器具によって大きく違う",
          "外傷と時間の浪費になりやすい"],
         "推奨されない"),
        ("② 柔軟性気管支鏡を通す", GREEN,
         ["鏡で声門を見ながらチューブを進める", "内径と長さの適合を先に確かめる",
          "換気を続けたまま行える利点がある"],
         "第一に考える"),
        ("③ 交換用カテーテル", BLUE,
         ["気管支鏡でカテーテルを気管へ置く", "器具を抜いてチューブをかぶせる",
          "細いチューブしか通らない器具で有効"],
         "内腔が細いとき"),
        ("④ 内蔵カメラで見る", PURPLE,
         ["第3世代の器具で声門を直接見る", "留置の修正も同じ視野で行える",
          "配備と訓練が前提になる"],
         "使える施設なら"),
    ]
    CW, GAP, X0, Y0 = 344, 18, 52, 136
    bottom = Y0
    for i, (head, color, lines, verdict) in enumerate(WAYS):
        x = X0 + i * (CW + GAP)
        s0, ln0 = fitlines(cv, [head], CW - 26, 12.6, weight="bold",
                           floor=9.6)
        hh = max(76, 26 + LH(s0, 1.4) * len(ln0))
        cv.box(x, Y0, CW, hh, fc=color, ec=color, lw=0, radius=8)
        cv.block(x, Y0 + (hh - LH(s0, 1.4) * len(ln0)) / 2, CW, ln0, s0,
                 color="white", weight="bold")
        s, ln = bullets(cv, lines, CW - 52, 10.6)
        bh = 36 + LH(s, 1.85) * len(ln)
        cv.box(x, Y0 + 90, CW, bh, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.block(x + 26, Y0 + 108, CW - 52, ln, s, ha="left", lh=LH(s, 1.85))
        cv.box(x, Y0 + 90 + bh + 16, CW, 72, fc="white", ec=color, lw=2.0,
               radius=8)
        s2, ln2 = fitlines(cv, [verdict], CW - 30, 12.4, weight="bold",
                           floor=9.6)
        cv.block(x, Y0 + 90 + bh + 16 + (72 - LH(s2, 1.45) * len(ln2)) / 2,
                 CW, ln2, s2, color=color, weight="bold")
        bottom = max(bottom, Y0 + 90 + bh + 16 + 72)

    Y1 = bottom + 48
    cv.text(52, Y1, "始める前に決めておく四つ", size=13.5, color=NAVY,
            weight="bold", ha="left")
    PRE = [("何のために挿管するのか", "換気ができているなら、急ぐ理由は何か", BLUE),
           ("どのチューブが通るのか", "内径・外径・長さを器具ごとに確かめてある", GREEN),
           ("抜くときどうするのか", "器具を残すのか抜くのか、手順を共有してある",
            ORANGE),
           ("うまくいかなかったら", "何回で止めて、次に何をするか決めてある", RED)]
    BH, BG, Y2 = 100, 14, Y1 + 32
    for i, (head, body, color) in enumerate(PRE):
        y = Y2 + i * (BH + BG)
        cv.box(52, y, W - 104, BH, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.rect(58, y + 6, 470, BH - 12, fc=color, ec="none")
        s, ln = fitlines(cv, [head], 440, 12.2, weight="bold", floor=9.4)
        cv.block(58, y + (BH - LH(s, 1.45) * len(ln)) / 2, 470, ln, s,
                 color="white", weight="bold")
        s2, ln2 = fitlines(cv, [body], W - 104 - 520, 11.8, floor=9.4)
        cv.block(556, y + (BH - LH(s2, 1.5) * len(ln2)) / 2, W - 104 - 520,
                 ln2, s2, ha="left")

    msg(cv, Y2 + 4 * (BH + BG) + 14,
        "換気が保てているなら、導管としての挿管は「急ぐ手技」ではなくなる")
    save(cv, P("f22_conduit.png"))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f16, f17, f18, f19, f20, f21, f22):
        fn()
        print("ok", fn.__name__)
