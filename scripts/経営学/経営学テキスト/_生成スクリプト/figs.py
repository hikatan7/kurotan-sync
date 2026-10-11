# -*- coding: utf-8 -*-
"""クリティカル・シンキング 図版 f01〜f08"""
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


def title(cv, y, s, color=NAVY, size=14.0):
    sz = cv.fit_size([s], W - 90, size, weight="bold")
    cv.title(W / 2, y, s, size=sz, ha="center", color=color)


def card(cv, x, y, w, head, lines, color, fill, head_size=12.0,
         body_size=10.4, pad=16, min_body=None):
    """見出し帯つきのカード。返り値は全体の高さ。"""
    hs = cv.fit_size([head], w - 2 * pad, head_size, weight="bold")
    hh = 20 + LH(hs, 1.4)
    body = []
    bs = body_size
    for ln in lines:
        body.extend(cv.wrap(ln, w - 2 * pad, bs))
    bh = max(min_body or 0, pad * 2 + LH(bs, 1.5) * len(body))
    cv.box(x, y, w, hh + bh, fc=fill, ec=color, lw=1.8, radius=10)
    cv.box(x, y, w, hh, fc=color, ec=color, lw=0, radius=10)
    cv.text(x + w / 2, y + hh / 2, head, size=hs, color="white", weight="bold")
    cy = y + hh + (bh - LH(bs, 1.5) * len(body)) / 2
    for i, ln in enumerate(body):
        cv.text(x + w / 2, cy + LH(bs, 1.5) * (i + 0.5), ln, size=bs, color=INK)
    return hh + bh


# ---------------------------------------------------------------- f01
def f01():
    cv = Canvas(W, 470)
    title(cv, 46, "図1　空・雨・傘 ── 意見の三段と、割れたときに見る場所")
    xs, w, gap = 83, 430, 32
    cols = [
        ("空（事実）", BLUE, "#eaf1f8",
         ["今月の定時終了率は 62%", "（前月 74%）"],
         "ここで割れたら：同じ数字を見ているか。定義と期間は同じか"),
        ("雨（解釈）", ORANGE, "#fdf3e3",
         ["遅れは特定の 3 室に", "偏っている"],
         "ここで割れたら：分解したうえでの解釈か。別の解釈は成り立たないか"),
        ("傘（行動）", GREEN, "#eaf5ee",
         ["その 3 室の枠設定を", "実測に合わせる"],
         "ここで割れたら：打ち手は解釈に対応しているか。副作用はどこに出るか"),
    ]
    y = 110
    for i, (head, col, fill, lines, foot) in enumerate(cols):
        x = xs + i * (w + gap)
        h = card(cv, x, y, w, head, lines, col, fill, min_body=110)
        fs = cv.fit_size([foot], w - 20, 9.6)
        fl = cv.wrap(foot, w - 20, fs)
        for j, ln in enumerate(fl):
            cv.text(x + w / 2, y + h + 26 + LH(fs, 1.5) * j, ln,
                    size=fs, color=GREY)
        if i < 2:
            cv.arrow((x + w + 2, y + h / 2), (x + w + gap - 2, y + h / 2),
                     color=GREY, lw=2.2)
    cv.text(W / 2, 428, "一段目で食い違っていることが最も多い",
            size=11.5, color=NAVY, weight="bold")
    cv.save(P("f01_kusoamekasa.png"))


# ---------------------------------------------------------------- f02
def f02():
    cv = Canvas(W, 820)
    title(cv, 46, "図2　ピラミッド・ストラクチャー ── 二方向の検査")
    kw = 760
    kx = (W - kw) / 2
    kh = textbox(cv, kx, 110, kw, ["時間外を減らす最も確実な一手は、",
                                   "手術枠の設定を実測に合わせることである"],
                 11.6, style="navy", title="キーメッセージ", title_size=11.0,
                 title_color=NAVY)
    ys = 110 + kh + 70
    bw, bgap = 380, 30
    bx0 = (W - (bw * 3 + bgap * 2)) / 2
    grounds = [["遅延は一部の室に", "偏っている"],
               ["その遅れは設定と", "実測の差で説明できる"],
               ["設定を変えても", "年間件数は維持できる"]]
    facts = [["不調 3 室 41%", "他 7 室 78%"],
             ["実測 22 分", "想定 15 分"],
             ["枠外実施分を", "枠内に戻す試算"]]
    bottom = ys
    for i in range(3):
        x = bx0 + i * (bw + bgap)
        h = textbox(cv, x, ys, bw, grounds[i], 10.8, style="blue",
                    title="根拠 %d" % (i + 1), title_size=10.2)
        cv.arrow((kx + kw / 2, 110 + kh + 6), (x + bw / 2, ys - 8),
                 color="#9aa6b4", lw=1.6)
        fy = ys + h + 48
        fh = textbox(cv, x + 45, fy, bw - 90, facts[i], 10.2, style="grey",
                     title="事実", title_size=9.6)
        cv.arrow((x + bw / 2, ys + h + 6), (x + bw / 2, fy - 8),
                 color="#9aa6b4", lw=1.6)
        bottom = fy + fh
    ax1, ax2 = 78, W - 78
    cv.arrow((ax1, 150), (ax1, bottom - 10), color=TEAL, lw=2.4)
    cv.text(ax1 + 14, bottom + 22, "Why so?", size=10.4, color=TEAL,
            weight="bold", ha="left")
    cv.text(ax1 + 14, bottom + 48, "なぜそう言えるのか", size=8.8, color=GREY,
            ha="left")
    cv.arrow((ax2, bottom - 10), (ax2, 150), color=PURPLE, lw=2.4)
    cv.text(ax2 - 14, bottom + 22, "So what?", size=10.4, color=PURPLE,
            weight="bold", ha="right")
    cv.text(ax2 - 14, bottom + 48, "だから何が言えるのか", size=8.8, color=GREY,
            ha="right")
    cv.text(W / 2, bottom + 92,
            "どちらの方向でも意味が通れば、構造は成立している",
            size=11.4, color=NAVY, weight="bold")
    cv.save(P("f02_pyramid.png"))


# ---------------------------------------------------------------- f03
def f03():
    cv = Canvas(W, 520)
    title(cv, 46, "図3　問題解決の四段 ── 各段で答える問いと、飛ばしたときに起きること")
    w, gap = 330, 30
    x0 = (W - (w * 4 + gap * 3)) / 2
    steps = [
        ("What", NAVY, "#e8edf5", ["何が問題か", "誰が困っているか"],
         "飛ばすと：打ち手から議論が始まる"),
        ("Where", BLUE, "#eaf1f8", ["全体か、一部か", "どこに偏っているか"],
         "飛ばすと：原因が全体論になる"),
        ("Why", ORANGE, "#fdf3e3", ["なぜそうなったか", "他ではなぜ起きないか"],
         "飛ばすと：思いつきの対策が付く"),
        ("How", GREEN, "#eaf5ee", ["どの案を選ぶか", "基準は何か"],
         "飛ばすと：案が一つで賛否になる"),
    ]
    y = 120
    for i, (head, col, fill, lines, foot) in enumerate(steps):
        x = x0 + i * (w + gap)
        h = card(cv, x, y, w, head, lines, col, fill, min_body=96)
        fs = cv.fit_size([foot], w - 16, 9.6)
        for j, ln in enumerate(cv.wrap(foot, w - 16, fs)):
            cv.text(x + w / 2, y + h + 26 + LH(fs, 1.5) * j, ln,
                    size=fs, color=RED)
        if i < 3:
            cv.arrow((x + w + 4, y + h / 2), (x + w + gap - 4, y + h / 2),
                     color=GREY, lw=2.4)
    cv.text(W / 2, 452, "この順序を書式にすると、経験による即答を止められる",
            size=11.5, color=NAVY, weight="bold")
    cv.save(P("f03_4steps.png"))


# ---------------------------------------------------------------- f04
def f04():
    cv = Canvas(W, 560)
    title(cv, 46, "図4　三つの分解パターン")
    w, gap = 450, 35
    x0 = (W - (w * 3 + gap * 2)) / 2
    y = 110
    # 層別
    x = x0
    textbox(cv, x, y, w, [], 10.0, style="blue", title="層別分解　属性で切る",
            title_size=11.4, min_h=54)
    bw = (w - 40) / 4
    for i, lab in enumerate(["A 科", "B 科", "C 科", "D 科"]):
        cv.box(x + 20 + i * bw, y + 70, bw - 8, 70, style="blue", lw=1.4)
        cv.text(x + 20 + i * bw + (bw - 8) / 2, y + 105, lab, size=10.2,
                color=INK)
    cv.text(x + w / 2, y + 175, "偏っているのはどこかを見る", size=10.0,
            color=GREY)
    # 変数
    x = x0 + w + gap
    textbox(cv, x, y, w, [], 10.0, style="amber",
            title="変数分解　掛け算に分ける", title_size=11.4, min_h=54)
    cv.box(x + 20, y + 70, w - 40, 70, style="amber", lw=1.4)
    cv.text(x + w / 2, y + 105, "手術収益 ＝ 件数 × 単価", size=11.0, color=INK)
    cv.text(x + w / 2, y + 175, "どの要素が効いているかを見る", size=10.0,
            color=GREY)
    # プロセス
    x = x0 + (w + gap) * 2
    textbox(cv, x, y, w, [], 10.0, style="green",
            title="プロセス分解　流れで切る", title_size=11.4, min_h=54)
    labs = ["入室", "導入", "執刀", "退室"]
    pw = (w - 40) / 4
    for i, lab in enumerate(labs):
        px = x + 20 + i * pw
        cv.box(px, y + 70, pw - 14, 70, style="green", lw=1.4)
        cv.text(px + (pw - 14) / 2, y + 105, lab, size=10.2, color=INK)
        if i < 3:
            cv.arrow((px + pw - 12, y + 105), (px + pw - 2, y + 105),
                     color=GREY, lw=1.6, head=7)
    cv.text(x + w / 2, y + 175, "どこで時間が落ちているかを見る", size=10.0,
            color=GREY)
    # 下段メッセージ
    textbox(cv, 200, 360, W - 400,
            ["どれを選ぶかの基準はひとつ ── その分解で、打ち手が変わるかどうか"],
            12.0, style="navy", min_h=90)
    cv.text(W / 2, 500, "森から木へ。構成比を確認してから深掘りする",
            size=11.0, color=GREY)
    cv.save(P("f04_decompose.png"))


# ---------------------------------------------------------------- f05
def f05():
    cv = Canvas(W, 640)
    title(cv, 46, "図5　速い判断と遅い判断 ── 止めるのは意識ではなく仕組み")
    w = 660
    x1, x2 = 60, 60 + w + 80
    y = 110
    h1 = card(cv, x1, y, w, "システム 1（速い）",
              ["自動的・努力を要さない・常に動いている",
               "経験を積むほど精度が上がる",
               "手術室で「様子がおかしい」と気づく力"],
              ORANGE, "#fdf3e3", min_body=130)
    h2 = card(cv, x2, y, w, "システム 2（遅い）",
              ["意識的・努力を要する・必要なときだけ動く",
               "書く、比べる、順序立てる",
               "呼び出さないかぎり動かない"],
              BLUE, "#eaf1f8", min_body=130)
    yy = y + max(h1, h2) + 50
    h3 = textbox(cv, 60, yy, W - 120,
                 ["時間を空ける　／　他人に説明する　／　書かせる　／　"
                  "順序を固定する　／　反対側を先に書く"],
                 12.2, style="navy", title="システム 2 を呼び出す五つの仕掛け",
                 title_size=11.6)
    cv.text(W / 2, yy + h3 + 46, "「気をつける」は仕掛けではない", size=11.0,
            color=RED, weight="bold")
    cv.save(P("f05_system12.png"))


# ---------------------------------------------------------------- f06
def f06():
    cv = Canvas(W, 960)
    title(cv, 46, "図6　トゥールミンの論証モデル ── 六つの要素")
    bw = 430
    # 限定（上）
    textbox(cv, (W - 620) / 2, 100, 620,
            ["緊急症例の割合が現在の水準にとどまる限り"],
            9.8, style="amber", title="限定（どこまで言えるか）",
            title_size=10.0, min_h=110)
    # データ → 主張
    dy = 250
    textbox(cv, 90, dy, bw,
            ["不調 3 室の入れ替え実測は 22 分", "（好調 7 室は 14 分）"],
            10.6, style="grey", title="データ（事実）", title_size=10.6,
            min_h=150)
    textbox(cv, W - 90 - bw, dy, bw,
            ["枠設定を実測に合わせて", "見直すべきである"],
            10.6, style="navy", title="主張", title_size=10.6, min_h=150)
    cv.arrow((90 + bw + 14, dy + 75), (W - 90 - bw - 14, dy + 75),
             color=NAVY, lw=2.6)
    cv.arrow((W / 2, 214), (W / 2, dy + 40), color=ORANGE, lw=1.8)
    # 論拠
    wy = 450
    textbox(cv, (W - 760) / 2, wy, 760,
            ["設定が実態より短ければ、遅延は構造的に発生する"],
            11.0, style="blue", title="論拠（データと主張をつなぐ規則）",
            title_size=10.6, min_h=110)
    cv.arrow((W / 2, wy - 10), (W / 2, dy + 158), color=BLUE, lw=2.2)
    # 裏付け
    by = wy + 150
    textbox(cv, (W - 760) / 2, by, 760,
            ["過去に設定を変更した際の実績、他院の運用報告"],
            10.4, style="grey", title="裏付け（論拠を支えるもの）",
            title_size=10.2, min_h=110)
    cv.arrow((W / 2, by - 10), (W / 2, wy + 118), color=GREY, lw=1.8)
    # 反証
    ry = by + 160
    textbox(cv, (W - 760) / 2, ry, 760,
            ["遅延の主因が人員配置にある場合は、設定変更では解決しない"],
            10.4, style="red", title="反証（成り立たない条件）",
            title_size=10.2, min_h=110)
    cv.text(W / 2, ry + 140,
            "限定と反証を先に書くほど、主張は通りやすくなる",
            size=11.4, color=NAVY, weight="bold")
    cv.save(P("f06_toulmin.png"))


# ---------------------------------------------------------------- f07
def f07():
    cv = Canvas(W, 540)
    title(cv, 46, "図7　Where ── 全体が一様に悪いのか、一部が極端に悪いのか")
    panel = 660
    base_y, bh = 330, 190
    for k, (x0, head, vals, col, note) in enumerate([
        (60, "全体が一様に悪い",
         [0.62, 0.61, 0.63, 0.62, 0.60, 0.62, 0.61, 0.63, 0.62, 0.64],
         BLUE, "原因は全室に共通するもの（始業、搬送、記録、清掃）"),
        (60 + panel + 80, "一部が極端に悪い",
         [0.78, 0.80, 0.25, 0.79, 0.77, 0.22, 0.81, 0.78, 0.20, 0.80],
         RED, "原因はその室に固有のもの（術式、チーム、機器）"),
    ]):
        cv.text(x0 + panel / 2, 106, head, size=12.4, color=col, weight="bold")
        bw = panel / 12
        for i, v in enumerate(vals):
            h = bh * v
            x = x0 + bw * (i + 0.6)
            c = col if v < 0.5 or col is BLUE else "#c8d3e0"
            cv.rect(x, base_y - h, bw * 0.72, h, fc=c)
        cv.arrow((x0 + 10, base_y), (x0 + panel - 10, base_y), color=GREY,
                 lw=1.4, style="-")
        cv.text(x0 + panel / 2, base_y + 26, "手術室 1〜10 室の定時終了率",
                size=9.6, color=GREY)
        for j, ln in enumerate(cv.wrap(note, panel - 20, 10.4)):
            cv.text(x0 + panel / 2, base_y + 64 + LH(10.4, 1.5) * j, ln,
                    size=10.4, color=INK)
    cv.text(W / 2, 500,
            "同じ「平均 62%」でも、打つべき手はまったく違う",
            size=11.5, color=NAVY, weight="bold")
    cv.save(P("f07_where.png"))


# ---------------------------------------------------------------- f08
def f08():
    cv = Canvas(W, 520)
    title(cv, 46, "図8　シングルループとダブルループ")
    boxes = [("前提・目標", PURPLE, "#f1ecf8"), ("やり方", BLUE, "#eaf1f8"),
             ("結果", GREEN, "#eaf5ee")]
    bw, gap = 360, 90
    x0 = (W - (bw * 3 + gap * 2)) / 2
    y = 150
    cxs = []
    for i, (lab, col, fill) in enumerate(boxes):
        x = x0 + i * (bw + gap)
        cv.box(x, y, bw, 96, fc=fill, ec=col, lw=2.0, radius=10)
        cv.text(x + bw / 2, y + 48, lab, size=13.0, color=col, weight="bold")
        cxs.append((x, x + bw))
        if i < 2:
            cv.arrow((x + bw + 8, y + 48), (x + bw + gap - 8, y + 48),
                     color=GREY, lw=2.4)
    # シングルループ（結果 → やり方）
    cv.arrow((cxs[2][0] + bw / 2, y + 104), (cxs[1][0] + bw / 2, y + 104),
             color=BLUE, lw=2.2)
    cv.text((cxs[1][0] + cxs[2][1]) / 2, y + 140,
            "シングルループ　やり方だけを直す", size=11.0, color=BLUE,
            weight="bold")
    # ダブルループ（結果 → 前提）
    cv.arrow((cxs[2][0] + bw / 2, y + 210), (cxs[0][0] + bw / 2, y + 210),
             color=PURPLE, lw=2.6)
    cv.text(W / 2, y + 246, "ダブルループ　前提そのものを問い直す",
            size=11.6, color=PURPLE, weight="bold")
    textbox(cv, 200, 430, W - 400,
            ["毎年同じ問題が議題に上がるなら、回っているのは内側のループだけである"],
            11.6, style="navy", min_h=70)
    cv.save(P("f08_loop.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08):
        fn()
        print("ok", fn.__name__)
