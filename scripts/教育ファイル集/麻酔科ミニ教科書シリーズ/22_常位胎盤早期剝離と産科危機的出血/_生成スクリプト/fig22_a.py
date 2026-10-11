# -*- coding: utf-8 -*-
"""第22巻 図版 f01〜f10"""
import math
import os
from matplotlib.patches import Ellipse, Wedge, Polygon
from figlib import (Canvas, textbox, NAVY, INK, GREY, RED, GREEN, FILL)
from trimfig import trim_bottom

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "図版")
os.makedirs(OUT, exist_ok=True)
W = 2000


def save(cv, name):
    path = os.path.join(OUT, name)
    cv.save(path)
    trim_bottom(path)
    print("  ", name)


# ---------------------------------------------------------------- f01
def f01():
    cv = Canvas(W, 1400)
    cv.title(40, 52, "剝離面から始まり、全身の凝固能が枯れるまで")
    cv.text(40, 100, "── 見える出血が少なくても、血管内では凝固が進行している",
            size=12, color=GREY, ha="left")

    xs = [40, 430, 820, 1210, 1600]
    bw = 360
    steps = [
        ("① 胎盤の剝離", ["脱落膜の螺旋動脈が破綻", "後血腫が胎盤を剝がす",
                      "剝離面が広がっていく"], "red"),
        ("② 組織因子の流入", ["剝離面と脱落膜から", "組織因子が母体循環へ",
                        "大量に入り込む"], "amber"),
        ("③ トロンビン産生", ["外因系が爆発的に作動", "血管内でフィブリンが",
                        "次々と形成される"], "blue"),
        ("④ 消費", ["フィブリノゲン・第V因子", "第VIII因子・血小板が",
                  "使い尽くされる"], "purple"),
        ("⑤ 線溶亢進", ["プラスミンが活性化し", "できた血栓も溶ける",
                    "FDP・D-dimer が上がる"], "green"),
    ]
    y = 170
    hmax = 0
    for i, (t, lines, st) in enumerate(steps):
        h = textbox(cv, xs[i], y, bw, lines, 12.5, style=st, title=t,
                    title_size=15, pad_y=20, min_h=240)
        hmax = max(hmax, h)
        if i < 4:
            cv.arrow((xs[i] + bw + 6, y + h / 2), (xs[i + 1] - 6, y + h / 2),
                     color=GREY, lw=2.6, head=15)
    y2 = y + hmax + 55
    cv.rect(40, y2, W - 80, 3, fc="#d8dee6")

    y3 = y2 + 45
    hb1 = textbox(cv, 40, y3, 940,
            ["剝離面は子宮筋層側にあり、児頭や卵膜が栓の役割をする。",
             "血液は子宮筋層内・後腹膜・羊水腔へ流れ込み、外へは出ない。",
             "「外出血が少ない」は「出血量が少ない」を意味しない。"],
            13, style="grey", title="外へは出ない出血", title_size=15, pad_y=20)
    textbox(cv, 1020, y3, 940,
            ["第 I 因子（フィブリノゲン）が最も早く、最も深く落ちる。",
             "妊娠中は 400–600 mg/dL あるため、低下の初期は",
             "「基準値内」に見える。ここが最大の落とし穴である。"],
            13, style="red", title="最初に枯れるのはフィブリノゲン",
            title_size=15, pad_y=20)

    cv.text(40, y3 + hb1 + 46, "※ 数値は妊娠後期の代表値。実際には施設の基準値で読み替えること。",
            size=10.5, color=GREY, ha="left")
    save(cv, "f01_pathway.png")


# ---------------------------------------------------------------- f02
def f02():
    cv = Canvas(W, 1400)
    cv.title(40, 52, "外出血型と潜伏型 ── 同じ病気の二つの顔")

    CY = 520                      # 子宮の中心。表題と札が触れない高さに置く
    RX, RY = 440, 600

    def uterus(cx, label, hidden):
        cv.text(cx, CY - 360, label, size=17, color=NAVY, weight="bold", z=6)
        cv.ax.add_patch(Ellipse((cx, CY), RX, RY, facecolor="#fdf6f3",
                                edgecolor="#b0787a", lw=2.6, zorder=1))
        cv.ax.add_patch(Wedge((cx, CY), 224, 118, 208, width=46,
                              facecolor="#c98f8f", edgecolor="#9c5f61",
                              lw=1.4, zorder=3))
        cv.ax.add_patch(Wedge((cx, CY), 218, 128, 196, width=60,
                              facecolor="#8e2b2b", edgecolor="none", zorder=4))
        # 血腫の札は、扇形の中央（角度162°・半径188）の上に置く。
        # 子宮の中心に置くと薄い地の上に白文字が乗って読めなくなる。
        th = math.radians(162)
        cv.text(cx + 188 * math.cos(th), CY + 188 * math.sin(th), "血腫",
                size=12.5, color="white", weight="bold", z=6)
        if hidden:
            cv.text(cx, CY + 250, "外へ出ない", size=14, color=RED,
                    weight="bold", z=6)
        else:
            cv.ax.add_patch(Polygon([(cx - 24, CY + 292), (cx + 24, CY + 292),
                                     (cx + 13, CY + 402), (cx - 13, CY + 402)],
                                    facecolor="#8e2b2b", zorder=5))
            cv.text(cx, CY + 438, "腟からの出血", size=14, color=RED,
                    weight="bold", z=6)

    uterus(420, "外出血型（revealed）", False)
    uterus(1130, "潜伏型（concealed）", True)

    textbox(cv, 1450, 230, 510,
            ["全体のおよそ 2 割が潜伏型とされる。",
             "腟からの出血がまったくない、",
             "あるいはごく少量にとどまる。",
             "",
             "そして潜伏型のほうが",
             "剝離面が大きく、",
             "凝固障害も胎児死亡も多い。"],
            13, style="red", title="腟出血がないほうが重い", title_size=15,
            pad_y=22)

    textbox(cv, 40, CY + 500, W - 80,
            ["腟出血の量は、剝離の広さを反映しない。剝離面の血液が外へ出るかどうかは、",
             "胎盤の付着位置と、卵膜や児頭による栓の有無で決まるからである。"],
            13.5, style="navy", pad_y=18)
    save(cv, "f02_concealed.png")


# ---------------------------------------------------------------- f03
def f03():
    cv = Canvas(W, 1500)
    cv.title(40, 52, "フィブリノゲンの読み方 ── 非妊娠時の物差しを当てない")

    x0, x1 = 300, 1900

    def px(v):
        return x0 + (x1 - x0) * v / 700.0

    bands = [(0, 100, "#8e2b2b", "致命的"), (100, 150, "#c0392b", "緊急"),
             (150, 200, "#d98e2b", "赤信号"), (200, 300, "#c8971f", "黄信号"),
             (300, 700, "#2e7d52", "許容")]
    yb, hb = 310, 106
    for a, b, c, lab in bands:
        cv.rect(px(a), yb, px(b) - px(a), hb, fc=c)
        cv.text((px(a) + px(b)) / 2, yb + hb / 2, lab, size=14,
                color="white", weight="bold", z=6)
    for v in (0, 100, 150, 200, 300, 400, 500, 600, 700):
        cv.rect(px(v), yb + hb, 2, 16, fc="#556070")
        cv.text(px(v), yb + hb + 46, str(v), size=12, color=INK)
    cv.text((x0 + x1) / 2, yb + hb + 92, "フィブリノゲン（mg/dL）",
            size=13, color=GREY)

    for y, lo, hi, col, lab in ((138, 150, 350, "#8d97a3", "非妊娠時の基準域 150–350"),
                                (190, 300, 600, "#2e6da4", "妊娠後期の基準域 300–600")):
        cv.rect(px(lo), y, px(hi) - px(lo), 30, fc=col, alpha=0.9)
        cv.text(px(lo) - 16, y + 15, lab, size=12.5, color=col, ha="right",
                weight="bold")

    cv.arrow((px(200), yb - 34), (px(200), yb - 4), color=RED, lw=3, head=16)
    cv.text(px(200), yb - 58, "200：実務上の分水嶺", size=14, color=RED,
            weight="bold")

    y2 = 530
    hs3 = []
    hs3.append(textbox(cv, 40, y2, 620,
            ["妊娠後期の 200 mg/dL は、", "非妊娠時に置き換えると",
             "およそ 100 mg/dL に相当する。", "",
             "「基準値内」という表示に", "だまされてはいけない。"],
            13, style="amber", title="相対的低フィブリノゲン血症",
            title_size=15, pad_y=22, min_h=290))
    hs3.append(textbox(cv, 690, y2, 620,
            ["早剝は産科DIC診断基準の入口で", "すでに 4〜5 点を持っている。",
             "Fbg ≦150 の 1 点に、冷汗・蒼白と", "FDP の上昇を足すだけで",
             "判定の 8 点に届いてしまう。", "",
             "対応指針では Fbg <150 が単独で", "危機的出血の宣言基準になる。"],
            13, style="red", title="150 未満は別格の意味を持つ",
            title_size=15, pad_y=22, min_h=290))
    hs3.append(textbox(cv, 1340, y2, 620,
            ["出血が続いている状況では", "「今の値」ではなく",
             "「30 分後の値」で判断する。", "",
             "早剝では 1 時間で 150 mg/dL", "落ちることが珍しくない。"],
            13, style="blue", title="見るべきは値ではなく傾き",
            title_size=15, pad_y=22, min_h=290))

    textbox(cv, 40, y2 + max(hs3) + 46, W - 80,
            ["赤信号（200 未満）で補充を考え、緊急（150 未満）で補充を始める。",
             "150 を確認してから動き出すのでは、製剤が届くころには 100 を切っている。"],
            14, style="navy", pad_y=20)
    save(cv, "f03_fbg_band.png")


# ---------------------------------------------------------------- f04
def f04():
    cv = Canvas(W, 1400)
    cv.title(40, 52, "「200」という数字はどこから来たか")
    cv.text(40, 100,
            "Charbit B, et al. J Thromb Haemost 2007;5:266-73.（産後出血 128 例の前向き観察）",
            size=12, color=GREY, ha="left")

    h1 = textbox(cv, 40, 165, 940,
            ["プロトロンビン時間", "活性化部分トロンボプラスチン時間",
             "アンチトロンビン", "血小板数", "第 V 因子・第 VIII 因子"],
            14, style="grey", title="重症化を予測しなかった項目",
            title_size=16, title_color=GREY, pad_y=24, min_h=310)
    h2 = textbox(cv, 1020, 165, 940,
            ["フィブリノゲン", "",
             "多変量解析で独立した予測因子は", "この 1 項目だけだった"],
            15, style="red", title="重症化を予測した唯一の項目",
            title_size=16, pad_y=24, min_h=310)

    y = 165 + max(h1, h2) + 40
    h4 = textbox(cv, 40, y, 920, ["重症産後出血の", "陽性的中率", "100 %"], 16,
            style="red", title="Fbg < 200 mg/dL", title_size=18,
            pad_y=26, min_h=290)
    textbox(cv, 1040, y, 920, ["重症化しないことの", "陰性的中率", "79 %"], 16,
            style="green", title="Fbg > 400 mg/dL", title_size=18,
            pad_y=26, min_h=290)

    textbox(cv, 40, y + h4 + 46, W - 80,
            ["この研究が変えたのは治療ではなく、見る場所である。",
             "それまで凝固の代表選手だった PT・APTT は産科出血の重症化を予測せず、",
             "フィブリノゲンだけが予測した。"],
            13.5, style="navy", pad_y=20)
    save(cv, "f04_charbit.png")


# ---------------------------------------------------------------- f05
def f05():
    cv = Canvas(W, 1420)
    cv.title(40, 52, "重症度は「出血量」ではなく「胎児の生死」で分岐する")

    h = textbox(cv, 700, 150, 600, ["常位胎盤早期剝離"], 17, style="navy",
                pad_y=24)
    yb = 150 + h
    y = yb + 60
    cv.arrow((1000, yb + 4), (1000, y - 34), color=GREY, lw=2.6, head=1)

    cols = [(40, "Grade I", ["分娩後に胎盤を見て", "はじめて分かる程度",
                             "症状はほぼない"], "grey"),
            (540, "Grade II", ["母体症状あり", "胎児は生存",
                               "胎児機能不全を伴う"], "amber"),
            (1040, "Grade IIIa", ["胎児死亡", "凝固障害なし"], "blue"),
            (1540, "Grade IIIb", ["胎児死亡", "凝固障害あり",
                                  "＝麻酔科の主戦場"], "red")]
    cv.rect(250, y - 34, 1500, 3, fc="#8d97a3")
    hs = []
    for x, t, lines, st in cols:
        cv.arrow((x + 210, y - 32), (x + 210, y - 6), color=GREY, lw=2.2,
                 head=13)
        hs.append(textbox(cv, x, y, 420, lines, 13, style=st, title=t,
                          title_size=16, pad_y=22, min_h=270))

    y2 = y + max(hs) + 60
    h5 = textbox(cv, 40, y2, 940,
            ["胎児が生きている → 緊急度は最大である",
             "しかし凝固障害の頻度は相対的に低い",
             "分単位で娩出を目指す場面"],
            14, style="blue", title="緊急度が高い群", title_size=16,
            pad_y=22, min_h=250)
    textbox(cv, 1020, y2, 940,
            ["胎児が死亡している → 緊急度は下がる",
             "しかし凝固障害の頻度は最も高い",
             "経腟分娩を選べる場面であり、麻酔法の選択肢も広い"],
            14, style="red", title="危険度が高い群", title_size=16,
            pad_y=22, min_h=250)

    textbox(cv, 40, y2 + h5 + 46, W - 80,
            ["緊急度と危険度が逆転しうる、数少ない病態である。"
             "「急いでいない」ことと「安全である」ことは別である。"],
            14, style="navy", pad_y=20)
    save(cv, "f05_severity.png")


# ---------------------------------------------------------------- f06
def f06():
    cv = Canvas(W, 1500)
    cv.title(40, 52, "産科DICスコアの構造 ── 早剝は入口で 4〜5 点を持っている")

    blocks = [
        ("1. 基礎疾患", "該当するものを 1 つだけ選ぶ",
         [("常位胎盤早期剝離：子宮硬直・児死亡", "5"),
          ("常位胎盤早期剝離：子宮硬直・児生存", "4"),
          ("常位胎盤早期剝離：画像・CTG 所見による診断", "4")], "red"),
        ("2. 臨床症状", "項目ごとに加算する",
         [("出血傾向（肉眼的血尿・紫斑・注射部位からの出血など）", "4"),
          ("心・肝・脳・消化管の重篤な障害（それぞれ）", "4"),
          ("脈拍 ≧100/分／血圧 ≦90 mmHg／冷汗／蒼白（それぞれ）", "1")], "amber"),
        ("3. 検査項目", "該当するものを全て選ぶ（各 1 点）",
         [("FDP ≧10 μg/mL ／ 血小板 ≦10万/mm³ ／ フィブリノゲン ≦150 mg/dL", "1"),
          ("PT ≧15 秒（≦50%）／ 赤沈低下 ／ 出血時間 ≧5 分", "1"),
          ("その他の凝固・線溶・キニン系因子の異常（AT ≦60% など）", "1")], "blue"),
    ]
    y = 160
    for title, note, rows, st in blocks:
        cv.text(40, y + 26, title, size=16, color=NAVY, weight="bold", ha="left")
        cv.text(320, y + 27, note, size=12, color=GREY, ha="left")
        y += 56
        for lab, pt in rows:
            cv.rect(40, y, 1760, 62, fc=FILL[st][0], ec=FILL[st][1], lw=1.2)
            cv.text(66, y + 31, lab, size=12.5, color=INK, ha="left")
            cv.rect(1810, y, 150, 62, fc=FILL[st][1])
            cv.text(1885, y + 31, pt, size=15, color="white", weight="bold", z=6)
            y += 70
        y += 18

    cv.rect(40, y, W - 80, 3, fc="#d8dee6")
    y += 34
    textbox(cv, 40, y, W - 80,
            ["合計 8 点以上で DIC と判定し、治療を開始する。",
             "ただし、検査項目（上記 3）で 2 点以上が含まれている必要がある。"],
            14, style="navy", title="判　定", title_size=16, pad_y=20)

    y += 200
    textbox(cv, 40, y, W - 80,
            ["早剝（子宮硬直・児生存）4 ＋ 冷汗 1 ＋ 蒼白 1 ＋ FDP ≧10 で 1 ＋ Fbg ≦150 で 1 　＝　8 点",
             "検査項目が 2 点含まれているので、この時点で DIC と判定される。"],
            13.5, style="red", title="たとえば、こうなる", title_size=16, pad_y=20)

    cv.text(40, y + 230,
            "出典：産科DIC診断基準（日本産科婦人科学会誌 2006／産婦人科の実際 2013;62:153-161 ほか）。"
            "配点は原典で確認すること。",
            size=10.5, color=GREY, ha="left")
    save(cv, "f06_dicscore.png")


# ---------------------------------------------------------------- f07
def f07():
    cv = Canvas(W, 1150)
    cv.title(40, 52, "結果が返るまでの時間 ── その間に患者は変化している")

    x0, x1 = 470, 1930

    def px(m):
        return x0 + (x1 - x0) * m / 60.0

    lanes = [("FIBTEM A5", 5, "green", "測定開始から 5 分で読める"),
             ("Clauss 法 Fbg", 35, "amber", "採血から報告まで 30–60 分"),
             ("血算・PT・APTT", 30, "blue", "緊急検査でも 30 分前後"),
             ("交差適合済 RBC", 45, "red", "検体到着から 40–60 分")]
    y = 180
    for lab, m, st, note in lanes:
        cv.text(450, y + 28, lab, size=14, color=FILL[st][1], weight="bold",
                ha="right")
        cv.rect(x0, y, px(m) - x0, 56, fc=FILL[st][0], ec=FILL[st][1], lw=1.6)
        cv.rect(px(m) - 7, y, 7, 56, fc=FILL[st][1])
        cv.text(px(m) + 18, y + 28, note, size=12, color=GREY, ha="left")
        y += 86

    yb = y + 16
    cv.rect(x0, yb, x1 - x0, 4, fc="#8d97a3")
    for m in (0, 10, 20, 30, 40, 50, 60):
        cv.rect(px(m), yb - 8, 2, 22, fc="#556070")
        cv.text(px(m), yb + 44, "%d 分" % m, size=12.5, color=INK)
    cv.text(450, yb + 2, "採血", size=13, color=INK, ha="right")

    textbox(cv, 40, yb + 100, 940,
            ["早剝では、この 30 分でフィブリノゲンが",
             "100 mg/dL 落ちることがある。",
             "つまり Clauss 法の値は、手元に届いた瞬間には",
             "すでに過去の値である。"],
            13, style="red", title="30 分の意味", title_size=15, pad_y=20)
    textbox(cv, 1020, yb + 100, 940,
            ["粘弾性検査があるなら A5 を見て動く。",
             "なければ、Clauss 法を待たずに",
             "「早剝＋出血持続」という臨床像だけで",
             "製剤の手配と準備を始める。"],
            13, style="green", title="待たないための二つの道",
            title_size=15, pad_y=20)
    save(cv, "f07_lab_timeline.png")


# ---------------------------------------------------------------- f08
def f08():
    cv = Canvas(W, 1250)
    cv.title(40, 52, "FIBTEM A5 ── フィブリノゲンを 5 分で推定する")

    x0, x1 = 260, 1900

    def px(v):
        return x0 + (x1 - x0) * v / 25.0

    yb, hb = 300, 100
    for a, b, c, lab in [(0, 7, "#c0392b", "< 7 mm"),
                         (7, 12, "#d98e2b", "7–12 mm"),
                         (12, 25, "#2e7d52", "≧ 12 mm")]:
        cv.rect(px(a), yb, px(b) - px(a), hb, fc=c)
        cv.text((px(a) + px(b)) / 2, yb + hb / 2, lab, size=15,
                color="white", weight="bold", z=6)
    for v in (0, 5, 7, 10, 12, 15, 20, 25):
        cv.rect(px(v), yb + hb, 2, 16, fc="#556070")
        cv.text(px(v), yb + hb + 44, str(v), size=12, color=INK)
    cv.text((x0 + x1) / 2, yb + hb + 88, "FIBTEM A5（mm）", size=13, color=GREY)

    for a, b, lab in [(0, 7, "Fbg < 150 相当"), (7, 12, "Fbg 150–200 相当"),
                      (12, 25, "Fbg > 200 相当")]:
        cv.text((px(a) + px(b)) / 2, yb - 48, lab, size=13.5, color=NAVY,
                weight="bold")

    y2 = 520
    textbox(cv, 40, y2, 620, ["ただちに補充する。", "Clauss 法の結果は待たない。"],
            13.5, style="red", title="A5 < 7 mm", title_size=16,
            pad_y=22, min_h=200)
    textbox(cv, 690, y2, 620, ["出血が続いているなら補充する。",
                               "止まっていれば再検して追う。"],
            13.5, style="amber", title="A5 7–12 mm", title_size=16,
            pad_y=22, min_h=200)
    textbox(cv, 1340, y2, 620, ["フィブリノゲンは足りている。",
                                "不足しているのは他の要素である。"],
            13.5, style="green", title="A5 ≧ 12 mm", title_size=16,
            pad_y=22, min_h=200)

    textbox(cv, 40, y2 + 240, W - 80,
            ["カットオフを 10 mm とする報告と 12 mm とする報告がある。装置・カートリッジ・対象集団で差が出るためである。",
             "自施設の装置で「Fbg 200 mg/dL に相当する A5 は何 mm か」を一度確かめ、その数字を使うのが正しい。",
             "EXTEM A5 は保たれているのに FIBTEM A5 だけ低い → フィブリノゲン単独の不足。両方低い → 血小板も足りない。"],
            13, style="navy", title="自施設の数字を持つこと", title_size=15,
            pad_y=20)
    save(cv, "f08_fibtem.png")


# ---------------------------------------------------------------- f09
def f09():
    cv = Canvas(W, 1800)
    cv.title(40, 52, "麻酔法の選択 ── 問うべきは「脊麻か全麻か」ではない")

    h = textbox(cv, 660, 140, 680, ["早剝で緊急帝王切開が決まった"], 16,
                style="navy", pad_y=22)
    y = 140 + h + 44
    cv.arrow((1000, 140 + h + 4), (1000, y - 8), color=GREY, lw=2.6, head=15)

    q1 = textbox(cv, 560, y, 880,
                 ["母体の循環は保たれているか", "胎児は待てるか"], 15,
                 style="blue", title="問 1　時間はあるか", title_size=16,
                 pad_y=22)
    y2 = y + q1 + 46
    cv.arrow((1000, y + q1 + 4), (1000, y2 - 8), color=GREY, lw=2.6, head=15)

    q2 = textbox(cv, 560, y2, 880,
                 ["血小板 ≧ 70,000/μL か",
                  "フィブリノゲン ≧ 150–200 mg/dL か",
                  "PT-INR < 1.5、APTT は正常か",
                  "そして「30 分後もそうである」と言えるか"], 14,
                 style="amber", title="問 2　この凝固能は針に耐えるか",
                 title_size=16, pad_y=22)
    y3 = y2 + q2 + 66

    cv.arrow((760, y2 + q2 + 4), (540, y3 - 8), color=GREY, lw=2.6, head=15)
    cv.arrow((1240, y2 + q2 + 4), (1470, y3 - 8), color=GREY, lw=2.6, head=15)
    cv.text(470, y2 + q2 + 30, "すべて YES", size=13, color=GREEN, weight="bold")
    cv.text(1560, y2 + q2 + 30, "一つでも NO・不明", size=13, color=RED,
            weight="bold")

    h9 = textbox(cv, 80, y3, 900,
            ["脊髄くも膜下麻酔を選んでよい。",
             "ただし術中も凝固を追い続ける。",
             "悪化したら全身麻酔へ移行できる準備を",
             "手術室内に置いたままにしておく。"], 13.5,
            style="green", title="区域麻酔", title_size=17, pad_y=22,
            min_h=300)
    textbox(cv, 1020, y3, 900,
            ["全身麻酔。",
             "迅速導入を基本とするが、",
             "ショックでは通常量の導入薬を使わない。",
             "導入前に循環の支えを用意しておく。"], 13.5,
            style="red", title="全身麻酔", title_size=17, pad_y=22, min_h=300)

    textbox(cv, 40, y3 + h9 + 46, W - 80,
            ["「帝王切開だから脊麻」という反射をいったん止め、「この凝固能は針に耐えるか」を先に問う。",
             "入室時の値が正常でも、早剝では 30 分で変わる。だから判断は値だけでなく、",
             "出血が続いているかどうかと合わせて行う。"],
            13.5, style="navy", pad_y=20)
    save(cv, "f09_anesthesia.png")


# ---------------------------------------------------------------- f10
def f10():
    cv = Canvas(W, 1200)
    cv.title(40, 52, "導入で血圧が落ちる理由 ── 静脈還流が二重に減る")

    textbox(cv, 40, 170, 600,
            ["出血で循環血液量が減っている。",
             "交感神経の緊張だけで血圧を保っている。",
             "妊娠子宮が下大静脈を圧迫している。"],
            13, style="amber", title="導入前：ぎりぎり代償している",
            title_size=15, pad_y=22, min_h=280)

    cv.arrow((660, 310), (745, 310), color=GREY, lw=3, head=18)

    textbox(cv, 765, 170, 560,
            ["麻酔薬が交感神経緊張を解く", "→ 静脈容量が増え、還流が減る"],
            13, style="red", title="① 血管側", title_size=15, pad_y=22,
            min_h=280)
    textbox(cv, 1365, 170, 595,
            ["陽圧換気が胸腔内圧を上げる", "→ 右心への還流がさらに減る"],
            13, style="red", title="② 胸腔側", title_size=15, pad_y=22,
            min_h=280)

    cv.arrow((1045, 455), (1010, 545), color=RED, lw=3, head=18)
    cv.arrow((1660, 455), (1180, 545), color=RED, lw=3, head=18)

    textbox(cv, 560, 560, 880, ["心拍出量が急落し、血圧が保てなくなる"], 16,
            style="red", pad_y=24)

    y = 755
    textbox(cv, 40, y, 940,
            ["導入薬の種類より、用量と順番で決まる。",
             "昇圧薬を先に走らせる。輸液・輸血を先につなぐ。",
             "導入量は通常の半分以下に落とす。",
             "子宮左方転位を導入前から確実に行う。"],
            13, style="green", title="落とさないための設計", title_size=15,
            pad_y=20)
    textbox(cv, 1020, y, 940,
            ["エトミデートは本邦では臨床使用できない。",
             "ケタミンもカテコラミンが枯れた状態では",
             "直接の心筋抑制が表に出て血圧が下がる。",
             "「この薬なら安全」という薬は存在しない。"],
            13, style="red", title="薬の名前に頼らない", title_size=15,
            pad_y=20)
    save(cv, "f10_induction.png")


if __name__ == "__main__":
    f01(); f02(); f03(); f04(); f05()
    f06(); f07(); f08(); f09(); f10()
    print("fig22_a done")
