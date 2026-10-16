# -*- coding: utf-8 -*-
"""総目次の図版 t01〜t03"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)
from fig1a import cap, msg, fitlines, card, W, TEAL
from fig4a import fit
from figcrop import crop_bottom

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


CH = [("第Ⅰ章", "ペースメーカー・ICD", BLUE, "止めるべきものが二つある", 34),
      ("第Ⅱ章", "大血管手術の脳保護", PURPLE, "届いているかを見る", 30),
      ("第Ⅲ章", "脊髄保護と髄液ドレナージ", GREEN, "引き算で守る", 31),
      ("第Ⅳ章", "M-TEER と僧帽弁", RED, "止めた瞬間に条件が変わる", 29),
      ("第Ⅴ章", "TAVI と三尖弁", ORANGE, "開く弁と、閉じない弁", 28),
      ("第Ⅵ章", "透析患者の心大血管手術", TEAL, "腎臓の仕事が六つ止まる", 27),
      ("第Ⅶ章", "人工心肺・出血・循環の目標", "#1f5f8b", "全章を横断する枠組み", 27),
      ("第Ⅷ章", "心臓麻酔と神経モニタリング", "#7a3b6e", "三つの問いを混ぜない", 40)]


# ---------------------------------------------------------------- t01
def t01():
    """本書の地図"""
    cv = Canvas(W, 1400)
    cap(cv, 44, "本書の八つの章 ── 全 246 頁・図版 115 点・表 28 点")

    w = (W - 140 - 3 * 24) / 4
    for i, (no, name, col, sub, pg) in enumerate(CH):
        r, c = divmod(i, 4)
        x = 70 + (w + 24) * c
        y = 130 + r * 300
        cv.box(x, y, w, 260, fc="#ffffff", ec=col, lw=1.8, radius=10)
        cv.box(x, y, w, 54, fc=col, ec=col, lw=0, radius=10)
        cv.text(x + w / 2, y + 27, no, size=12.6, color="white", weight="bold")
        s, lines = fitlines(cv, [name], w - 26, 11.6, weight="bold")
        for j, ln in enumerate(lines):
            cv.text(x + w / 2, y + 92 + LH(s, 1.5) * j, ln, size=s, color=col,
                    weight="bold")
        s2, l2 = fitlines(cv, [sub], w - 30, 10.4)
        y2 = y + 178 - LH(s2, 1.6) * (len(l2) - 1) / 2
        for j, ln in enumerate(l2):
            cv.text(x + w / 2, y2 + LH(s2, 1.6) * j, ln, size=s2, color=INK)
        cv.text(x + w / 2, y + 232, "%d 頁" % pg, size=10.6, color=GREY)

    y = 740
    th = textbox(cv, 70, y, W - 140,
                 ["第Ⅰ章から第Ⅵ章までは、主題ごとに一つの領域を扱う。",
                  "第Ⅶ章は人工心肺・輸血・循環の目標を横断的に扱い、"
                  "六つの章の共通の枠組みを取り出す。",
                  "第Ⅷ章は脳のモニタと、そのときの麻酔を扱う。"
                  "第Ⅱ章・第Ⅲ章と重なる数字を、あえて再掲している。"],
                 11.0, style="navy", title="章の並び", title_color=NAVY,
                 pad_y=18)

    msg(cv, y + th + 30,
        "どの章も、病態・解剖・血行動態・術前・導入・監視・節目・補助・凝固・引き継ぎの順で書いてある")
    cv.save(P("t01_book_map8.png"))
    crop_bottom(P("t01_book_map8.png"))


# ---------------------------------------------------------------- t02
def t02():
    """本書を貫く主題"""
    cv = Canvas(W, 2500)
    cap(cv, 44, "本書を貫く一つの主題 ──「測れること」「できること」は「転帰が変わること」とは別である")

    ROWS = [("第Ⅱ章", "近赤外線脳酸素モニター", "脳酸素飽和度の低下を検出できる",
             "無作為化試験では転帰の改善は示されていない", PURPLE),
            ("第Ⅱ章", "昇圧薬で平均血圧を上げる", "血圧は確実に上がる",
             "rSO2 はむしろ下がった（差 3.5、95%CI 0.9〜6.1）", PURPLE),
            ("第Ⅲ章", "髄液ドレナージ", "脊髄灌流圧を上げられる",
             "有効とする試験と、差がないとする試験が並んでいる", GREEN),
            ("第Ⅲ章", "治療的ドレナージ", "麻痺の発症後に挿入できる",
             "15 例中 10 例は麻痺が残存した", GREEN),
            ("第Ⅳ章", "クリップの追加", "残存逆流を減らせる",
             "圧較差が上がり、5 mmHg 超は 1 年死亡 3.42 倍", RED),
            ("第Ⅴ章", "脳塞栓防止デバイス", "デブリを捕捉できる",
             "7,635 例で脳卒中 2.1% 対 2.2%（p=0.94）", ORANGE),
            ("第Ⅵ章", "高カリウム血症の薬物治療", "カリウムを下げられる",
             "下がるのは平均 0.7〜1.2 mEq/L にとどまる", TEAL),
            ("第Ⅶ章", "急性腎障害の予防バンドル", "実施率を上げられる",
             "全体の発生率に有意差はなかった（46.3% 対 41.5%）", "#1f5f8b"),
            ("第Ⅷ章", "脳波ガイド麻酔", "抑制時間を三分の一にできる",
             "せん妄 18.15% 対 18.10%（ENGAGES-Canada）", "#7a3b6e"),
            ("第Ⅷ章", "多部位の組織酸素モニタ", "基準値からの逸脱を減らせる",
             "主要転帰 47.3% 対 47.8%（Bottomline-CS）", "#7a3b6e"),
            ("第Ⅷ章", "自動調節能に基づく血圧", "その患者の下限・最適値を出せる",
             "せん妄は減った（38% 対 53%、8.2% 対 14.9%）", "#2e7d52")]

    y = 130
    for ch, what, can, but, col in ROWS:
        h = 152
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.5, radius=8)
        cv.box(70, y, 200, h, fc=col, ec=col, lw=0, radius=8)
        cv.text(170, y + h / 2, ch, size=12.4, color="white", weight="bold")
        cv.text(300, y + 44, what, size=fit(cv, what, 430, 11.4, "bold"),
                color=col, ha="left", weight="bold")
        cv.text(300, y + 82, can, size=fit(cv, can, 430, 10.4), color=GREY,
                ha="left")
        cv.text(300, y + 120, but, size=fit(cv, but, W - 400, 11.0),
                color=INK, ha="left")
        y += h + 12

    th = textbox(cv, 70, y + 16, W - 140,
                 ["最後の一行だけが、転帰の側にも届いている。",
                  "「異常が出たら戻す」のではなく、"
                  "「その患者の目標値をあらかじめ決めて、そこに置き続ける」"
                  "という形の介入であった。",
                  "この表は、モニタを外す理由ではない。"
                  "外れたときに何をするかを、先に決めておくための表である。"],
                 11.0, style="navy", title="この表の読み方", title_color=NAVY,
                 pad_y=18)

    msg(cv, y + 16 + th + 28,
        "三つの問い ── それは測れるか。測れたとして、できることがあるか。"
        "できたとして、転帰は変わるか")
    cv.save(P("t02_thesis.png"))
    crop_bottom(P("t02_thesis.png"))


# ---------------------------------------------------------------- t03
def t03():
    """読む順序の提案"""
    cv = Canvas(W, 1400)
    cap(cv, 44, "どこから読むか ── 三つの入口")

    WAYS = [("はじめて心臓麻酔を担当する", BLUE, "#eaf0f8",
             ["第Ⅷ章 第 1 部（モニタが答える問い）",
              "第Ⅶ章 第 1 部（人工心肺の基本）",
              "第Ⅰ章（デバイスを読む）",
              "その後、担当する術式の章へ"]),
            ("明日この手術がある", GREEN, "#eaf5ee",
             ["該当する章の「はじめに」と「まとめ」",
              "その章の付録（施設で決めておくこと）",
              "その章のアルゴリズム図",
              "時間があれば本文へ"]),
            ("施設の手順を作りたい", ORANGE, "#fdf3e6",
             ["各章の付録（施設で決めておくこと）を集める",
              "第Ⅶ章・第Ⅷ章の横断の枠組み",
              "文献台帳（284 件）から根拠を引く",
              "「確認できなかった資料」も併せて読む"])]

    w = (W - 140 - 2 * 28) / 3
    for i, (head, col, fc, lines) in enumerate(WAYS):
        card(cv, 70 + (w + 28) * i, 130, w, head, lines, col, fc,
             body_size=10.6, lh=2.0)

    y = 560
    th = textbox(cv, 70, y, W - 140,
                 ["各章は独立して読めるように書いてある。",
                  "ただし、繰り返し出てくる数字がいくつかある。",
                  "近赤外線脳酸素モニターの試験（第Ⅱ章・第Ⅷ章）、"
                  "髄液ドレナージの割れた結論（第Ⅲ章）、",
                  "トラネキサム酸とけいれん（第Ⅶ章・第Ⅷ章）、"
                  "そして脳塞栓防止デバイス（第Ⅴ章・第Ⅷ章）。",
                  "同じ数字が別の章に出てきたときは、"
                  "そこが本書の主題に触れている場所である。"],
                 11.0, style="grey", title="章をまたぐ数字", title_color=NAVY,
                 pad_y=18)

    y2 = y + th + 30
    th2 = textbox(cv, 70, y2, W - 140,
                  ["本文で引用した文献は、著者・雑誌・年・PMID・DOI まで"
                   "確認できたものに限っている。",
                   "確認できなかった資料は、各章の付録に"
                   "「確認できなかった資料」として記録し、本文では使っていない。",
                   "数値はすべて、抄録の結果・結論の記載から採っている。"],
                  11.0, style="teal", title="引用の方針", title_color=TEAL,
                  pad_y=18)

    msg(cv, y2 + th2 + 30,
        "確認できない資料は、書かない。書いたものは、出典まで戻れるようにする")
    cv.save(P("t03_how_to_read.png"))
    crop_bottom(P("t03_how_to_read.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (t01, t02, t03):
        fn()
        print("ok", fn.__name__)
