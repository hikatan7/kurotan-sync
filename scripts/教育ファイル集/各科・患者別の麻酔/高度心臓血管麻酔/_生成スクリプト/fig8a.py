# -*- coding: utf-8 -*-
"""第Ⅷ章 心臓麻酔と神経モニタリング　図版 s01〜s08"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from figlib import (Canvas, LH, textbox, duo, NAVY, INK, GREY, RED, BLUE, GREEN,
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


# ---------------------------------------------------------------- s01
def s01():
    """三つの問いと、三つの機械"""
    cv = Canvas(W, 1180)
    cap(cv, 44, "「麻酔が足りているか」「脳に届いているか」「脳が傷んでいないか」は別の問い")

    COL = [("麻酔は足りているか", BLUE, "#eaf0f8",
            ["脳波（生波形・スペクトログラム）", "処理脳波指数（BIS・PSI ほか）",
             "呼気終末麻酔薬濃度", "——", "時定数：秒", "答えるもの：意識・記憶"]),
           ("脳に届いているか", TEAL, "#e4f2f4",
            ["近赤外線脳酸素モニター（rSO2）", "経頭蓋ドプラ（流速・塞栓）",
             "自動調節能モニタ（COx・MAPopt）", "——", "時定数：秒〜分",
             "答えるもの：供給と需要"]),
           ("脳は傷んでいないか", PURPLE, "#f1ecf8",
            ["体性感覚誘発電位・運動誘発電位", "術後の神経学的診察",
             "画像（拡散強調 MRI）・バイオマーカー", "——", "時定数：分〜日",
             "答えるもの：機能の喪失"])]

    w = (W - 140 - 2 * 28) / 3
    for i, (head, col, fc, lines) in enumerate(COL):
        x = 70 + (w + 28) * i
        card(cv, x, 130, w, head, lines, col, fc, body_size=10.4, lh=1.9)

    y = 640
    th = textbox(cv, 70, y, W - 140,
                 ["この三つは、同じ「脳」を見ていても、答えている問いが違う。",
                  "脳波が深いことと、脳酸素が下がっていることは、"
                  "同時に起こりうるが別の事象である。",
                  "そして三つのどれもが、「転帰が変わるか」には"
                  "まだ十分に答えていない。"],
                 11.0, style="navy", title="この章の出発点",
                 title_color=NAVY, pad_y=18)

    msg(cv, y + th + 30, "機械を足す前に、その機械が答える問いを決める")
    cv.save(P("s01_three_questions.png"))
    crop_bottom(P("s01_three_questions.png"))


# ---------------------------------------------------------------- s02
def s02():
    """麻酔薬濃度と脳波の変化"""
    cv = Canvas(W, 1150)
    cap(cv, 44, "麻酔が深くなるにつれ、脳波は速い波から遅い波へ、そして途切れる")

    STAGES = [("覚醒", "β（13〜30 Hz）が優位", "低振幅・速い", GREEN, "#eaf5ee"),
              ("鎮静", "α（8〜12 Hz）が現れる", "後頭部優位", BLUE, "#eaf0f8"),
              ("全身麻酔", "前頭部の α 紡錘＋δ（<4 Hz）", "この状態を保ちたい",
               TEAL, "#e4f2f4"),
              ("深い麻酔", "δ が支配的、α が消える", "指数はまだ下がりきらない",
               ORANGE, "#fdf3e6"),
              ("バーストサプレッション", "平坦と群発が交互に出る",
               "薬が多い、または脳が弱い", RED, "#fceeec")]

    y = 130
    for name, wave, note, col, fc in STAGES:
        h = 130
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.6, radius=8)
        cv.box(70, y, 300, h, fc=col, ec=col, lw=0, radius=8)
        cv.text(220, y + h / 2, name,
                size=fit(cv, name, 270, 12.2, "bold"), color="white",
                weight="bold")
        cv.text(400, y + 48, wave, size=fit(cv, wave, 480, 11.4, "bold"),
                color=col, weight="bold", ha="left")
        cv.text(400, y + 88, note, size=fit(cv, note, 480, 10.4),
                color=INK, ha="left")
        # 模式波形
        x0, x1 = 920, W - 100
        t = np.linspace(0, 1, 600)
        if name == "覚醒":
            v = 0.35 * np.sin(2 * np.pi * 22 * t)
        elif name == "鎮静":
            v = 0.55 * np.sin(2 * np.pi * 10 * t)
        elif name == "全身麻酔":
            v = 0.5 * np.sin(2 * np.pi * 10 * t) + 0.7 * np.sin(2 * np.pi * 1.5 * t)
        elif name == "深い麻酔":
            v = 1.0 * np.sin(2 * np.pi * 1.2 * t)
        else:
            v = 0.9 * np.sin(2 * np.pi * 9 * t)
            v[(t > 0.18) & (t < 0.42)] = 0
            v[(t > 0.62) & (t < 0.88)] = 0
        cv.ax.plot(x0 + t * (x1 - x0), y + h / 2 - v * 34, color=col, lw=1.6,
                   zorder=4)
        y += h + 14

    th = textbox(cv, 70, y + 16, W - 140,
                 ["どの段階かは、指数の数字よりも波形のほうが早く、はっきり示す。",
                  "とくにバーストサプレッションは、"
                  "「薬が多い」場合と「脳がもろい」場合の両方で出る。",
                  "同じ濃度でも、高齢・併存症のある患者では"
                  "α のパワーが低く、抑制が出やすい（α が 1 dB 下がるごとに 1.33 倍）。"],
                 11.0, style="grey", title="読むときの要点",
                 title_color=NAVY, pad_y=18)
    cv.save(P("s02_eeg_stages.png"))
    crop_bottom(P("s02_eeg_stages.png"))


# ---------------------------------------------------------------- s03
def s03():
    """スペクトログラムの読み方"""
    cv = Canvas(W, 1150)
    cap(cv, 44, "スペクトログラム ── 横軸が時間、縦軸が周波数、色が強さ")

    x0, y0 = 150, 140
    pw, ph = W - 300, 330
    T = 420
    F = 200
    tt = np.linspace(0, 1, T)
    ff = np.linspace(0, 30, F)
    Z = np.zeros((F, T))
    for j, t in enumerate(tt):
        # δ は全域、α は維持期のみ、導入・覚醒では β
        depth = np.clip(np.sin(np.pi * min(max((t - 0.06) / 0.88, 0), 1)), 0, 1)
        for i, f in enumerate(ff):
            v = 0.0
            v += 1.5 * depth * np.exp(-((f - 1.5) ** 2) / 4.0)
            v += 1.5 * depth * np.exp(-((f - 10.0) ** 2) / 3.0)
            v += 0.8 * (1 - depth) * np.exp(-((f - 20.0) ** 2) / 30.0)
            Z[i, j] = v
    Z[:, int(T * 0.52):int(T * 0.60)] *= 0.12          # 抑制の帯
    cv.ax.imshow(Z[::-1], extent=[x0, x0 + pw, y0 + ph, y0], aspect="auto",
                 cmap="turbo", origin="upper", zorder=2)
    cv.rect(x0, y0, pw, ph, fc="none", ec="#8a94a2", lw=1.4, z=5)
    for v, lab in ((0, "30"), (1 / 3, "20"), (2 / 3, "10"), (1.0, "0")):
        cv.text(x0 - 18, y0 + ph * v, lab + " Hz", size=9.4, color=GREY,
                ha="right")
    for p, lab in ((0.03, "導入"), (0.30, "維持"), (0.56, "抑制"),
                   (0.80, "維持"), (0.97, "覚醒")):
        cv.text(x0 + pw * p, y0 + ph + 26, lab, size=10.0, color=INK)

    ANN = [(0.30, "前頭部 α 紡錘（8〜12 Hz）の帯", BLUE),
           (0.56, "帯が消える ＝ バーストサプレッション", RED),
           (0.97, "β が戻る ＝ 覚醒へ", GREEN)]
    yy = y0 + ph + 70
    for p, t, col in ANN:
        cv.text(x0, yy, "●　" + t, size=10.8, color=col, ha="left",
                weight="bold")
        yy += 34

    th = textbox(cv, 70, yy + 16, W - 140,
                 ["指数はこの絵を一つの数字に潰したものである。",
                  "潰す前の絵を見れば、α が細いのか、δ しかないのか、"
                  "抑制が入っているのかが区別できる。",
                  "自動計算された抑制率は、神経内科医の視察に比べて"
                  "抑制時間を著しく過小評価した。",
                  "視察による抑制分数はせん妄と関連し、"
                  "自動計算による分数は関連しなかった。"],
                 10.8, style="amber", title="指数ではなく絵を見る理由",
                 title_color="#9a6510", pad_y=18)
    cv.save(P("s03_spectrogram.png"))
    crop_bottom(P("s03_spectrogram.png"))


# ---------------------------------------------------------------- s04
def s04():
    """処理脳波指数の作られ方と限界"""
    cv = Canvas(W, 1250)
    cap(cv, 44, "処理脳波指数は、波形を一次元に潰した「要約」である")

    STEP = [("① 前額部から拾う", BLUE,
             ["電極は前頭部だけに置く", "後頭部・深部は見えない"]),
            ("② 雑音を取り除く", TEAL,
             ["筋電図・電気メス・体動", "ペーシングや補助循環の電気雑音"]),
            ("③ 特徴量を計算する", GREEN,
             ["周波数の分布・抑制の割合", "位相の関係など"]),
            ("④ 一つの数字にする", ORANGE,
             ["各社の非公開の重みづけ", "健常成人のデータで較正されている"])]
    w = (W - 140 - 3 * 22) / 4
    for i, (head, col, lines) in enumerate(STEP):
        x = 70 + (w + 22) * i
        card(cv, x, 130, w, head, lines, col, "#ffffff", body_size=10.0,
             lh=1.8)
        if i < 3:
            cv.arrow((x + w + 4, 230), (x + w + 18, 230), color=GREY, lw=2.0)

    y = 430
    th1 = textbox(cv, 70, y, (W - 170) / 2,
                  ["低体温そのもので下がる（BIS は約 1.12 単位/℃）",
                   "SedLine の PSI は 1℃ あたり 0.8 低下",
                   "抑制率は冷却で 2.9 上昇、復温で 2.2 低下",
                   "筋弛緩薬で筋電図が消えると下がる",
                   "同じ血漿濃度でも体外循環後は低く出る"],
                  10.6, style="red", title="数字が「下がる」理由は麻酔だけではない",
                  title_color=RED, pad_y=16)
    th2 = textbox(cv, 70 + (W - 170) / 2 + 30, y, (W - 170) / 2,
                  ["前額部の脳波は正常でも、後方の虚血は見えない",
                   "電気的無活動でも「浅い」とは言えない",
                   "指数が 40〜60 でも意識がつながっていることがある",
                   "孤立前腕法では挿管後の 4.6% が手を握り返した",
                   "心臓手術の 5.5% に「覚醒様」の脳波が出現した"],
                  10.6, style="purple", title="数字が「正常」でも安心できない理由",
                  title_color=PURPLE, pad_y=16)

    yy = y + max(th1, th2) + 30
    msg(cv, yy, "指数は入口。判断は波形と臨床の文脈で行う")
    cv.save(P("s04_index_limits.png"))
    crop_bottom(P("s04_index_limits.png"))


# ---------------------------------------------------------------- s05
def s05():
    """NIRS が見ているもの"""
    cv = Canvas(W, 1200)
    cap(cv, 44, "近赤外線脳酸素モニターが見ているのは、主として静脈側である")

    x0, y0 = 90, 130
    bw = 660
    cv.box(x0, y0, bw, 380, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(x0 + bw / 2, y0 + 40, "光が通る道", size=12.2, color=NAVY,
            weight="bold")
    LAYER = [("頭皮・頭蓋骨", "#e8ecf0", GREY, "ここも光は通る"),
             ("脳脊髄液", "#e4f2f4", TEAL, "層の厚みで値が変わる"),
             ("大脳皮質（前頭葉）", "#eaf0f8", BLUE, "見えるのはここだけ")]
    yy = y0 + 76
    for name, fc, col, note in LAYER:
        cv.box(x0 + 30, yy, bw - 60, 84, fc=fc, ec=col, lw=1.4, radius=8)
        cv.text(x0 + 60, yy + 32, name, size=11.2, color=col, ha="left",
                weight="bold")
        cv.text(x0 + 60, yy + 62, note, size=9.8, color=INK, ha="left")
        yy += 96

    rx = x0 + bw + 30
    rw = W - 70 - rx
    th = textbox(cv, rx, y0, rw,
                 ["動脈 25%、静脈 75% 程度の混合を見ている",
                  "したがって「酸素の使い残し」に近い",
                  "頭皮・頭蓋外の血流も混じる",
                  "絶対値には個人差が大きく、基準値からの変化で見る",
                  "術前の値そのものが患者の予備能を表す"],
                 10.8, style="teal", title="測っているもの", title_color=TEAL,
                 pad_y=16)
    th2 = textbox(cv, rx, y0 + th + 24, rw,
                  ["術前 rSO2 ≦50% ではせん妄 71%（20/28 例）",
                   "術前 rSO2 >50% ではせん妄 18%（41/221 例）",
                   "最低 rSO2 <35% では術後の検査異常が 44%・33%",
                   "（対照はそれぞれ 12%・9%）"],
                  10.6, style="amber", title="術前の値が語ること",
                  title_color="#9a6510", pad_y=16)

    y = max(y0 + 380, y0 + th + 24 + th2) + 34
    th3 = textbox(cv, 70, y, W - 140,
                  ["下がったら「供給・需要・血管・信号」の順に切り分ける。",
                   "供給＝流量・Hb・動脈血酸素分圧、需要＝温度・麻酔深度・けいれん、",
                   "血管＝送血管の位置・分枝の遮断・頸動脈病変、"
                   "信号＝プローブの位置・外光・頭皮の状態。"],
                  10.8, style="navy", title="下がったときの切り分け",
                  title_color=NAVY, pad_y=18)
    msg(cv, y + th3 + 28,
        "「下がったから昇圧」ではない。昇圧で rSO2 はむしろ下がったという試験がある",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("s05_nirs.png"))
    crop_bottom(P("s05_nirs.png"))


# ---------------------------------------------------------------- s06
def s06():
    """TCD と塞栓シグナル"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "塞栓の数は測れる。しかし数と症状は一致しない")

    y0 = 130
    cv.box(70, y0, W - 140, 250, fc="#ffffff", ec=BLUE, lw=1.8, radius=10)
    t = "冠動脈手術における中大脳動脈の塞栓シグナル数（中央値）"
    cv.text(W / 2, y0 + 40, t, size=fit(cv, t, W - 220, 12.0, "bold"),
            color=BLUE, weight="bold")
    PAIR = [("体外循環下", "79 個", "範囲 38〜876", RED),
            ("心拍動下（オフポンプ）", "3 個", "範囲 0〜18", GREEN)]
    w2 = (W - 200) / 2
    for i, (lab, val, rng, col) in enumerate(PAIR):
        x = 100 + w2 * i
        cv.text(x + w2 / 2, y0 + 92, lab, size=11.2, color=INK)
        cv.text(x + w2 / 2, y0 + 150, val, size=26, color=col, weight="bold")
        cv.text(x + w2 / 2, y0 + 200, rng, size=10.0, color=GREY)

    y = y0 + 280
    th = textbox(cv, 70, y, W - 140,
                 ["この研究では、どちらの群にも臨床的に明らかな神経脱落は生じなかった。",
                  "塞栓シグナルが 20 倍以上違っても、症状の差にはならなかった。",
                  "一方、塞栓が多い患者は体外循環からの離脱が難しく"
                  "（中等度塞栓群の離脱困難 OR 0.253、95%CI 0.111〜0.593）、",
                  "術後の臓器障害が長く続いたという報告がある。"],
                 10.8, style="grey", title="読み方", title_color=NAVY,
                 pad_y=18)

    USE = [("使える場面", GREEN, "#eaf5ee",
            ["送血開始・遮断解除・脱気の瞬間を可視化する",
             "手技を変えたときの効果を比べる", "送血の方向や位置の確認"]),
           ("使えない場面", RED, "#fceeec",
            ["側頭骨の窓が取れない患者（1〜2 割）",
             "プローブの固定が術野と干渉する", "数の多寡から予後を個人に当てはめる"])]
    w = (W - 140 - 30) / 2
    yy = y + th + 30
    for i, (head, col, fc, lines) in enumerate(USE):
        card(cv, 70 + (w + 30) * i, yy, w, head, lines, col, fc,
             body_size=10.2, lh=1.8)
    cv.save(P("s06_tcd.png"))
    crop_bottom(P("s06_tcd.png"))


# ---------------------------------------------------------------- s07
def s07():
    """低体温と脳波指数"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "低体温そのものが指数を下げる ── 「深い」のではない")

    x0, y0 = 150, 150
    pw, ph = W - 320, 300
    cv.rect(x0, y0, pw, ph, fc="#fbfcfd", ec="#dde3ea", lw=1.4)
    for v, lab in ((0.05, "60"), (0.35, "45"), (0.65, "30"), (0.95, "15")):
        yy = y0 + ph * v
        cv.ax.plot([x0, x0 + pw], [yy, yy], color="#e8ecf0", lw=1.0, zorder=1)
        cv.text(x0 - 16, yy, lab, size=9.4, color=GREY, ha="right")
    cv.text(x0 + pw, y0 - 26, "処理脳波指数（BIS 相当）", size=9.6, color=GREY,
            ha="right")

    TEMP = [37, 35, 33, 31, 29, 27]
    VAL = [48, 45.8, 43.5, 41.3, 39.1, 36.8]      # 約 1.12/℃
    xs = [x0 + pw * i / (len(TEMP) - 1) for i in range(len(TEMP))]
    ys = [y0 + ph * (1 - (v - 15) / 45.0) for v in VAL]
    cv.ax.plot(xs, ys, color=BLUE, lw=2.8, marker="o", markersize=6, zorder=4)
    for t, xx, yy, v in zip(TEMP, xs, ys, VAL):
        cv.text(xx, y0 + ph + 26, "%d℃" % t, size=9.6, color=INK)
        dx = 18 if xx == xs[0] else (-18 if xx == xs[-1] else 0)   # 両端は枠の内側へ寄せる
        cv.text(xx + dx, yy - 26, "%.0f" % v, size=10.2, color=BLUE, weight="bold")

    y = y0 + ph + 70
    w = (W - 140 - 30) / 2
    th1 = textbox(cv, 70, y, w,
                  ["BIS は体温にほぼ直線的に低下する（約 1.12 単位/℃）",
                   "SedLine の PSI は 1℃ あたり 0.8 低下（95%CI 0.7〜1.0）",
                   "復温では 1℃ あたり 0.7 上昇（95%CI 0.6〜0.8）",
                   "抑制率は冷却で 2.9 上昇、復温で 2.2 低下",
                   "スペクトルエッジ周波数は体温と関連しなかった"],
                  10.4, style="blue", title="低体温で起こること",
                  title_color=BLUE, pad_y=16)
    th2 = textbox(cv, 70 + w + 30, y, w,
                  ["低い数字を見て麻酔薬を減らすと、復温期に浅くなる",
                   "常温体外循環では、逆に「鎮静不足」に近い値まで上がる",
                   "超低体温循環停止では電気的無活動になる（これは目標）",
                   "復温時の脳波回復の遅さが術後せん妄を予測する",
                   "したがって「体温とセットで読む」以外に使い道がない"],
                  10.4, style="red", title="臨床で困ること",
                  title_color=RED, pad_y=16)
    msg(cv, y + max(th1, th2) + 28,
        "指数の値は、体温を書き添えて初めて意味をもつ")
    cv.save(P("s07_hypothermia_eeg.png"))
    crop_bottom(P("s07_hypothermia_eeg.png"))


# ---------------------------------------------------------------- s08
def s08():
    """体外循環と薬物動態"""
    cv = Canvas(W, 1200)
    cap(cv, 44, "体外循環が始まると、同じ投与量でも血中濃度は変わる")

    FAC = [("希釈", BLUE, "#eaf0f8",
            ["充填液が血液量に加わる", "開始直後に血漿濃度が落ちる"]),
           ("吸着", TEAL, "#e4f2f4",
            ["回路と人工肺の表面に薬が付く", "脂溶性が高い薬ほど付きやすい"]),
           ("肺の隔離", PURPLE, "#f1ecf8",
            ["肺循環が外れ、薬の出入りが止まる",
             "離脱で肺血流が戻ると放出される"]),
           ("低体温", ORANGE, "#fdf3e6",
            ["代謝と排泄が落ちる", "効果部位の感受性も変わる"])]
    w = (W - 140 - 3 * 22) / 4
    for i, (head, col, fc, lines) in enumerate(FAC):
        card(cv, 70 + (w + 22) * i, 130, w, head, lines, col, fc,
             body_size=10.0, lh=1.8)

    y = 420
    cv.box(70, y, W - 140, 250, fc="#ffffff", ec=RED, lw=1.8, radius=10)
    t = "常温体外循環の開始後、血漿プロポフォール濃度は対照値から低下した"
    cv.text(W / 2, y + 40, t, size=fit(cv, t, W - 220, 12.0, "bold"),
            color=RED, weight="bold")
    VALS = [("30%", "群 C"), ("35%", "群 B"), ("41%", "群 A")]
    w3 = (W - 200) / 3
    for i, (v, g) in enumerate(VALS):
        x = 100 + w3 * i
        cv.text(x + w3 / 2, y + 140, v, size=30, color=RED, weight="bold")
        cv.text(x + w3 / 2, y + 196, g + "（低下の幅）", size=10.2, color=GREY)

    yy = y + 280
    th = textbox(cv, 70, yy, W - 140,
                 ["一方で、体外循環を受けた患者では、"
                  "血漿濃度が同等でも処理脳波指数はより低く出た。",
                  "プロポフォール投与終了から抜管までの時間も長かった"
                  "（334±117 分 対 216±85 分）。",
                  "濃度は下がるのに、指数はむしろ深く出る。"
                  "この二つは矛盾ではなく、「濃度」と「効果」が別だという意味である。"],
                 10.8, style="navy", title="濃度が下がるのに、指数は下がる",
                 title_color=NAVY, pad_y=18)
    msg(cv, yy + th + 28,
        "目標制御輸注のモデルは、体外循環を想定して作られていない",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("s08_cpb_pk.png"))
    crop_bottom(P("s08_cpb_pk.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (s01, s02, s03, s04, s05, s06, s07, s08):
        fn()
        print("ok", fn.__name__)
