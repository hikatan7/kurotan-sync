# -*- coding: utf-8 -*-
"""第Ⅶ章 横断（CPB・PBM・循環）　図版 r08〜r14"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, duo, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)
from fig1a import cap, msg, fitlines, card, W, TEAL
from fig1b import step, down, side
from fig4a import fit
from figcrop import crop_bottom

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- r08
def r08():
    """周術期低血圧"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "低血圧は「値」ではなく「深さ×時間」で考える")

    x0, y0 = 90, 160
    pw, ph = W - 180 - 200, 280
    cv.rect(x0, y0, pw, ph, fc="#fbfcfd", ec="#dde3ea", lw=1.4)
    thr = y0 + ph * 0.40
    cv.ax.plot([x0, x0 + pw], [thr, thr], color=RED, lw=2.0, linestyle="--")
    cv.text(x0 + 12, y0 + ph - 20, "--- 閾値（例：MAP 65 mmHg）", size=10.0,
            color=RED, ha="left")

    import numpy as np
    t = np.linspace(0, 1, 800)
    y = thr - 30 + np.sin(t * 26) * 22 + np.sin(t * 7) * 14
    dip = np.where((t > 0.30) & (t < 0.50), 78, 0) + \
        np.where((t > 0.66) & (t < 0.72), 48, 0)
    y = y + dip
    cv.ax.plot(x0 + t * pw, y, color=NAVY, lw=2.2, zorder=4)
    cv.ax.fill_between(x0 + t * pw, thr, y, where=(y > thr), color="#fceeec",
                       zorder=2)
    cv.text(x0 + pw * 0.40, thr + 96, "深く・長い", size=10.6, color=RED,
            weight="bold")
    cv.text(x0 + pw * 0.69, thr + 74, "浅く・短い", size=10.0, color=GREY)

    L = [("曲線下面積という考え方", BLUE, "#eaf1f8",
          ["閾値を下回った深さと時間の積", "同じ最低血圧でも意味が違う",
           "第Ⅵ章の透析患者はこの面積が大きい"]),
         ("何が起こるか", RED, "#fceeec",
          ["心筋障害・腎障害との関連が報告されている",
           "第Ⅲ章では脊髄灌流圧の低下として現れる",
           "第Ⅰ章ではシャント閉塞の原因にもなる"])]
    w = (W - 140 - 30) / 2
    for i, (t2, col, fc, lines) in enumerate(L):
        card(cv, 70 + (w + 30) * i, y0 + ph + 60, w, t2, lines, col, fc,
             body_size=10.2, lh=1.8)

    th = textbox(cv, 70, y0 + ph + 340, W - 140,
                 ["ただし、「血圧を上げれば転帰が良くなる」ことは"
                  "まだ十分に証明されていない。",
                  "第Ⅱ章では、昇圧薬で平均血圧を上げた群でむしろ"
                  "脳酸素飽和度が下がった。",
                  "低血圧を避けることと、昇圧薬で血圧を上げることは、同じではない。"],
                 10.6, style="amber", title="ここでも同じ注意が要る",
                 title_color="#9a6510", pad_y=16)
    cv.save(P("r08_hypotension.png"))
    crop_bottom(P("r08_hypotension.png"))


# ---------------------------------------------------------------- r09
def r09():
    """血管麻痺と昇圧薬"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "血管が開いてしまったとき、何を使うか")

    cv.box(70, 130, W - 140, 150, fc="#fceeec", ec=RED, lw=1.8, radius=10)
    cv.text(W / 2, 172, "人工心肺後の血管麻痺（vasoplegia）", size=12.6,
            color=RED, weight="bold")
    cv.text(W / 2, 220,
            "心拍出量は保たれているのに、体血管抵抗が下がって血圧が上がらない状態",
            size=fit(cv,
                     "心拍出量は保たれているのに、体血管抵抗が下がって血圧が上がらない状態",
                     W - 240, 10.8), color=INK)
    cv.text(W / 2, 254, "背景：炎症反応・長い体外循環・術前の降圧薬・敗血症",
            size=10.2, color=GREY)

    C = [("カテコラミン", BLUE, "#eaf1f8",
          ["ノルアドレナリンが基本", "受容体の反応性が落ちていることがある",
           "増量には限界がある"]),
         ("非アドレナリン系", GREEN, "#eaf5ee",
          ["バソプレシン", "メチレンブルー",
           "受容体が違うため、上乗せが期待できる"]),
         ("背景を直す", PURPLE, "#f1ecf8",
          ["アシドーシス・低カルシウム血症の補正",
           "出血・感染など原因の除去", "体温の維持"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 320, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    y1 = 660
    cv.box(70, y1, W - 140, 210, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    t2 = "51 の無作為化比較試験 5,715 例のメタ解析"
    cv.text(W / 2, y1 + 38, t2, size=12.2, color=NAVY, weight="bold")
    cv.text(W / 2, y1 + 84,
            "敗血症性ショック 30 研究・心臓手術 11 研究・非心臓手術 10 研究",
            size=10.2, color=GREY)
    cv.text(W / 2, y1 + 136,
            "敗血症性ショックでは、非アドレナリン系の追加で死亡が低下"
            "（43% 対 48%、リスク比 0.92）",
            size=fit(cv,
                     "敗血症性ショックでは、非アドレナリン系の追加で死亡が低下（43% 対 48%、リスク比 0.92）",
                     W - 240, 11.0), color=GREEN, weight="bold")
    cv.text(W / 2, y1 + 178,
            "心臓手術での効果については、さらに検証が必要である",
            size=10.4, color=INK)
    cv.save(P("r09_vasoplegia.png"))
    crop_bottom(P("r09_vasoplegia.png"))


# ---------------------------------------------------------------- r10
def r10():
    """PrevAKI バンドル"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "バンドルを守らせても、発生率は変わらなかった")

    x0, y0 = 70, 130
    cv.box(x0, y0, W - 140, 130, fc="#e8edf5", ec=NAVY, lw=1.8, radius=10)
    t = "バイオマーカーで高リスクと判定された心臓手術患者 278 例"
    cv.text(W / 2, y0 + 50, t, size=fit(cv, t, W - 220, 12.4, "bold"),
            color=NAVY, weight="bold")
    cv.text(W / 2, y0 + 92,
            "KDIGO の推奨（血行動態の最適化・腎毒性薬の中止・血糖管理など）"
            "をバンドルとして実施",
            size=fit(cv,
                     "KDIGO の推奨（血行動態の最適化・腎毒性薬の中止・血糖管理など）をバンドルとして実施",
                     W - 240, 10.6), color=INK)

    CARDS = [("バンドルの完遂率", "65.4%", "4.2%", "介入群 対 対照群", GREEN),
             ("急性腎障害の発生", "46.3%", "41.5%", "有意差なし", RED)]
    w = (W - 140 - 30) / 2
    for i, (lab, a, b, note, col) in enumerate(CARDS):
        x = 70 + (w + 30) * i
        cv.box(x, y0 + 160, w, 250, fc="#ffffff", ec=col, lw=1.8, radius=10)
        cv.text(x + w / 2, y0 + 202, lab, size=12.2, color=col,
                weight="bold")
        duo(cv, x + w / 2, y0 + 280, a, b, size=26, col_a=col,
            max_w=w - 40)
        cv.text(x + w / 2, y0 + 350, note, size=10.6, color=INK)

    th = textbox(cv, 70, y0 + 440, W - 140,
                 ["バンドルは確かに実施された（完遂率は 65.4% 対 4.2%）。",
                  "しかし急性腎障害の全体の発生率には有意差がなかった"
                  "（46.3% 対 41.5%）。",
                  "中等症以上に限ると差がみられたと報告されている。",
                  "「手順を守らせること」と「転帰が変わること」は、"
                  "ここでも別の問題であった。"],
                 10.6, style="red", title="実装研究が教えること",
                 title_color=RED, pad_y=16)

    msg(cv, y0 + 440 + th + 28,
        "それでも、何を守るべきかを決めておくことには意味がある")
    cv.save(P("r10_prevaki.png"))
    crop_bottom(P("r10_prevaki.png"))


# ---------------------------------------------------------------- r11
def r11():
    """本書を貫く一覧：測れることと転帰"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "「測れること」「できること」は、「転帰が変わること」とは別である")

    ROWS = [("第Ⅱ章", "NIRS", "脳酸素飽和度の低下を検出できる",
             "無作為化試験では転帰の改善は示されていない", PURPLE),
            ("第Ⅱ章", "昇圧薬で MAP を上げる", "血圧は確実に上がる",
             "rSO2 はむしろ下がった（差 3.5、95%CI 0.9-6.1）", PURPLE),
            ("第Ⅲ章", "髄液ドレナージ", "脊髄灌流圧を上げられる",
             "RCT では有効、Cochrane では限定的、日本の研究では差なし",
             GREEN),
            ("第Ⅲ章", "治療的ドレナージ", "発症後に挿入できる",
             "15 例中 10 例は麻痺が残存した", GREEN),
            ("第Ⅳ章", "クリップの追加", "残存逆流を減らせる",
             "圧較差が上がり、5 mmHg 超は 1 年死亡 3.42 倍", RED),
            ("第Ⅴ章", "脳塞栓防止デバイス", "デブリを捕捉できる",
             "7,635 例で脳卒中 2.1% 対 2.2%（p=0.94）", ORANGE),
            ("第Ⅵ章", "高カリウム血症の薬物治療", "カリウムを下げられる",
             "下がるのは平均 0.7〜1.2 mEq/L にとどまる", TEAL),
            ("第Ⅶ章", "AKI 予防バンドル", "実施率を上げられる",
             "全体の発生率に有意差はなかった", BLUE)]

    y = 130
    for ch, what, can, but, col in ROWS:
        h = 148
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.5, radius=8)
        cv.box(70, y, 210, h, fc=col, ec=col, lw=0, radius=8)
        cv.text(175, y + h / 2, ch, size=12.4, color="white", weight="bold")
        TX = 310   # 章の帯（幅 210）より右から書く
        cv.text(TX, y + 40, what, size=fit(cv, what, W - 70 - TX - 30, 11.4, "bold"),
                color=col, weight="bold", ha="left")
        cv.text(TX, y + 82, "できること：" + can,
                size=fit(cv, "できること：" + can, W - 70 - TX - 30, 10.4),
                color=INK, ha="left")
        cv.text(TX, y + 118, "しかし：" + but,
                size=fit(cv, "しかし：" + but, W - 70 - TX - 30, 10.4),
                color=GREY, ha="left")
        y += h + 10

    th = textbox(cv, 70, y + 12, W - 140,
                 ["この一覧は、本書のどの章にも共通する構造である。",
                  "新しい機器や手技に出会ったとき、"
                  "同じ三つの問いを立てられる。",
                  "何が測れるのか。それは何を意味するのか。"
                  "それに介入すると転帰は変わるのか。"],
                 10.8, style="navy", title="三つの問い", title_color=NAVY,
                 pad_y=16)
    cv.save(P("r11_measure_vs_outcome.png"))
    crop_bottom(P("r11_measure_vs_outcome.png"))


# ---------------------------------------------------------------- r12
def r12():
    """Alg7-1 CPB 後の出血"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 1　人工心肺後に出血が止まらない")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["外科的な出血点はないか（術者と確認する）",
              "ヘパリンが中和されているか（ACT・プロタミンの追加）",
              "体温・イオン化カルシウム・pH は保たれているか"],
             style="navy", title="① 最初に確かめる三つ", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["粘弾性検査があれば、何が足りないのかを分ける",
              "凝固開始が遅い → 凝固因子",
              "血餅が弱い → フィブリノゲン",
              "血小板寄与が低い → 血小板",
              "血餅が溶ける → 線溶抑制"],
             style="green", title="② 足りないものを特定する",
             title_color=GREEN)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["制限的な赤血球輸血は、寛容的な輸血に非劣性であった",
              "ただし出血が続いている場面では、閾値の議論は当てはまらない",
              "「今、出血しているか」と「貧血をどこまで許容するか」を分けて考える"],
             style="amber", title="③ 赤血球をどう考えるか",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["透析患者では血小板機能が落ちている（数では評価できない）",
              "貧血の是正そのものが止血に寄与する",
              "デスモプレシンの効果は研究により一致していない"],
             style="purple", title="④ 第Ⅵ章の患者では", title_color=PURPLE)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["止まらないなら、再開胸のタイミングを遅らせない",
          "輸血を重ねることは、再開胸の代わりにならない",
          "決断が遅れるほど、その後の経過は悪くなる"],
         style="red", title="⑤ 引き際を決めておく", title_color=RED)
    cv.save(P("r12_alg_bleeding.png"))
    crop_bottom(P("r12_alg_bleeding.png"))


# ---------------------------------------------------------------- r13
def r13():
    """Alg7-2 CPB 離脱困難"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 2　人工心肺から離脱できない")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["離脱の条件は整っているか（体温・電解質・リズム・換気）",
              "TEE で左室・右室のどちらが問題かを見る",
              "弁は正しく機能しているか、空気は残っていないか"],
             style="navy", title="① 離脱前に戻って確認する",
             title_color=NAVY)
    y += h
    down(cv, cx, y, y + 50)
    y += 50
    cw = 340
    gap = (W - 140 - cw * 3) / 2
    LABS = [("左室が動かない", RED, "#fceeec",
             ["強心薬と後負荷の調整", "冠血流（グラフト・空気）を疑う",
              "IABP を検討する"]),
            ("右室が動かない", ORANGE, "#fdf3e3",
             ["前負荷・肺血管抵抗・体血圧", "第Ⅴ章の四つの軸で整える",
              "肺血管拡張薬を検討する"]),
            ("血管が開いている", PURPLE, "#f1ecf8",
             ["血管麻痺として対応する", "非アドレナリン系の上乗せ",
              "背景（アシドーシス等）を直す"])]
    for i, (t, col, fc, lines) in enumerate(LABS):
        x = 70 + (cw + gap) * i
        cv.arrow((cx, y - 12), (x + cw / 2, y + 14), color="#b9c2cc", lw=1.6,
                 head=8)
        card(cv, x, y + 18, cw, t, lines, col, fc, body_size=10.0, lh=1.8)
    y += 18 + 250
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["それでも離脱できないなら、機械的補助を早く決める",
              "心臓術後の VA-ECMO では、院内死亡が 64.4%、1 年死亡が 67.2% と報告されている",
              "術前因子によるスコアで、死亡率は 45.6% から 89.7% まで分かれる",
              "経験の多い施設ほど成績が良いという報告がある"],
             style="red", title="② 補助循環を考える", title_color=RED)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["「まだいける」と思いながら時間が過ぎることが、もっとも危ない",
          "誰が、どの指標で、いつ決めるのかを、手術前に決めておく",
          "決めておけば、その場で議論せずに動ける"],
         style="purple", title="③ 決断を先に設計しておく",
         title_color=PURPLE)
    cv.save(P("r13_alg_weaning.png"))
    crop_bottom(P("r13_alg_weaning.png"))


# ---------------------------------------------------------------- r14
def r14():
    """本書の使い方と更新"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "この本を、どう使い、どう更新するか")

    C = [("使うとき", BLUE, "#eaf1f8",
          ["症例の前に、該当章の 10 チェックを見る",
           "本文ではなく、まず図とアルゴリズムを見る",
           "数字が必要なときは付録の文献表から原典へ"]),
         ("更新するとき", GREEN, "#eaf5ee",
          ["新しい試験が出たら、該当する図の数字を差し替える",
           "文献台帳（Source Ledger）に S-ID を追加する",
           "「どの図・表に使うか」を同時に決める"]),
         ("引用するとき", PURPLE, "#f1ecf8",
          ["著者・雑誌・年・識別子まで確認できたものだけを載せる",
           "確認できなかった資料は、その旨を記録に残す",
           "結論が割れている場合は、両方を並べる"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 140, w, t, lines, col, fc,
             body_size=10.2, lh=1.85)

    y1 = 500
    cv.box(70, y1, W - 140, 250, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(W / 2, y1 + 40, "本書の構成", size=12.6, color=NAVY,
            weight="bold")
    STAT = [("章", "7"), ("図版", "本文中に掲載"),
            ("文献台帳", "210 件"), ("実在確認", "全件を PubMed で照合")]
    w2 = (W - 200) / 4
    for i, (lab, val) in enumerate(STAT):
        x = 100 + w2 * i
        cv.text(x + w2 / 2, y1 + 110, lab, size=11.0, color=GREY)
        cv.text(x + w2 / 2, y1 + 170, val,
                size=fit(cv, val, w2 - 30, 15.0, "bold"), color=NAVY,
                weight="bold")
    cv.text(W / 2, y1 + 216,
            "参照候補に挙がりながら実在を確認できなかった資料は、各章の付録に記録した",
            size=10.2, color=GREY)

    msg(cv, y1 + 280,
        "数字は判断の材料であって、結論ではない")
    cv.save(P("r14_how_to_use.png"))
    crop_bottom(P("r14_how_to_use.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (r08, r09, r10, r11, r12, r13, r14):
        fn()
        print("ok", fn.__name__)
