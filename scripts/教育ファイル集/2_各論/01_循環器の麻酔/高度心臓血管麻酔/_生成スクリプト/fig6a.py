# -*- coding: utf-8 -*-
"""第Ⅵ章 透析患者の心大血管手術　図版 q01〜q07"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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


# ---------------------------------------------------------------- q01
def q01():
    """ESKD を一枚で理解する"""
    cv = Canvas(W, 1200)
    cap(cv, 44, "腎臓が働いていないということは、六つのことが同時に起きている")

    cx = W / 2
    cv.box(cx - 280, 110, 560, 80, fc="#0f6d78", ec="#0f6d78", lw=0,
           radius=10)
    t = "維持透析中の患者が手術に来た"
    cv.text(cx, 150, t, size=fit(cv, t, 500, 13.6, "bold"), color="white",
            weight="bold")

    ITEMS = [("容量", BLUE, "#eaf1f8",
              ["最終透析からの時間で変わる", "dry weight との差を見る",
               "溢れても引けない"]),
             ("電解質", RED, "#fceeec",
              ["カリウムは値より変動幅", "カルシウム・マグネシウム",
               "酸塩基も透析の周期で動く"]),
             ("貧血", PURPLE, "#f1ecf8",
              ["エリスロポエチン不足", "鉄利用障害",
               "慢性的に低い Hb に適応している"]),
             ("血小板機能", ORANGE, "#fdf3e3",
              ["数は正常でも機能が落ちる", "尿毒症性血小板機能異常",
               "貧血そのものも出血を助長する"]),
             ("血管アクセス", GREEN, "#eaf5ee",
              ["シャント肢では血圧を測らない", "駆血・穿刺を避ける",
               "低血圧は閉塞の原因になる"]),
             ("心血管疾患", TEAL, "#e4f2f4",
              ["冠動脈・弁の石灰化が進む", "左室肥大と拡張障害",
               "自律神経障害も伴う"])]

    w = (W - 140 - 60) / 3
    for i, (t2, col, fc, lines) in enumerate(ITEMS):
        r, c = divmod(i, 3)
        x = 70 + (w + 30) * c
        y = 240 + r * 250
        if r == 0:
            cv.arrow((cx, 194), (x + w / 2, y - 8), color="#b9c2cc", lw=1.6,
                     head=8)
        card(cv, x, y, w, t2, lines, col, fc, body_size=10.2, lh=1.8)

    th = textbox(cv, 70, 760, W - 140,
                 ["この六つは別々の問題ではない。",
                  "貧血は出血を助長し、容量は電解質に影響し、"
                  "低血圧はアクセスを失わせる。",
                  "麻酔管理のどの判断も、"
                  "この六つのうち複数に同時に触れることになる。"],
                 10.8, style="navy", title="つながっている",
                 title_color=NAVY, pad_y=16)

    msg(cv, 760 + th + 28,
        "「腎不全がある」ではなく、「腎臓の仕事が六つ止まっている」と考える")
    cv.save(P("q01_eskd_overview.png"))
    crop_bottom(P("q01_eskd_overview.png"))


# ---------------------------------------------------------------- q02
def q02():
    """透析患者の心臓手術の成績"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "透析患者の心臓手術は、どれくらい危ないのか")

    x0, y0 = 70, 130
    cv.box(x0, y0, W - 140, 300, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    t = "全国データ 114,496 件（うち長期透析 1,241 件、腎移植後 298 件）"
    cv.text(W / 2, y0 + 38, t, size=fit(cv, t, W - 220, 12.2, "bold"),
            color=NAVY, weight="bold")
    BARS = [("弁手術＋冠動脈バイパス（透析）", 18.78, RED,
             "95%CI 13.37-25.25"),
            ("弁手術＋冠動脈バイパス（腎移植後）", 14.00, ORANGE,
             "95%CI 5.82-26.74")]
    yy = y0 + 86
    for lab, val, col, ci in BARS:
        cv.text(100, yy + 20, lab, size=fit(cv, lab, 560, 10.8), color=INK,
                ha="left")
        full = W - 800
        full = W - 100 - 700 - 230          # 数字の置き場を右に確保する
        cv.rect(700, yy + 4, full, 34, fc="#eef1f5")
        cv.rect(700, yy + 4, full * val / 25.0, 34, fc=col)
        cv.text(W - 100, yy + 21, "%.2f / 100 手術" % val, size=12.0,
                color=col, ha="right", weight="bold")
        cv.text(100, yy + 54, ci, size=9.4, color=GREY, ha="left")
        yy += 96
    cv.text(W / 2, y0 + 268,
            "透析患者は、調整後の死亡オッズが有意に高かった", size=10.6,
            color=INK)

    y1 = y0 + 330
    cv.box(70, y1, W - 140, 250, fc="#ffffff", ec=RED, lw=1.8, radius=10)
    t2 = "国家レジストリの比較（透析依存 104 例 対 腎機能正常 8,103 例）"
    cv.text(W / 2, y1 + 38, t2, size=fit(cv, t2, W - 220, 12.2, "bold"),
            color=RED, weight="bold")
    PAIR = [("30 日死亡", "14.4%", "2.3%"), ("4 年生存", "44%", "91%")]
    w2 = (W - 200) / 2
    for i, (lab, a, b) in enumerate(PAIR):
        x = 100 + w2 * i
        cv.text(x + w2 / 2, y1 + 86, lab, size=11.2, color=INK)
        duo(cv, x + w2 / 2, y1 + 150, a, b, size=24, col_a=RED,
            lab_a="透析", lab_b="腎機能正常", lab_dy=44, max_w=w2 - 20)

    th = textbox(cv, 70, y1 + 280, W - 140,
                 ["この数字は、手術を避ける理由ではない。",
                  "同じ弁膜症・冠動脈疾患を放置したときの予後も、透析患者では悪い。",
                  "数字が意味するのは、"
                  "「同じ手術でも、透析患者では別の準備が要る」ということである。"],
                 10.8, style="navy", title="この数字の使い方",
                 title_color=NAVY, pad_y=16)
    cv.save(P("q02_outcomes.png"))
    crop_bottom(P("q02_outcomes.png"))


# ---------------------------------------------------------------- q03
def q03():
    """術中低血圧になりやすい"""
    cv = Canvas(W, 1400)
    cap(cv, 44, "透析患者は、術中に血圧が下がりやすい")

    x0, y0 = 90, 160
    pw, ph = W - 180 - 230, 300
    cv.rect(x0, y0, pw, ph, fc="#fbfcfd", ec="#dde3ea", lw=1.4)
    thr = y0 + ph * 0.42
    cv.ax.plot([x0, x0 + pw], [thr, thr], color=RED, lw=2.0, linestyle="--")
    cv.text(x0 + 14, y0 + ph - 20, "--- MAP 65 mmHg", size=10.0, color=RED,
            ha="left")

    import numpy as np
    t = np.linspace(0, 1, 700)
    for lab, amp, off, col, lw in (("腎疾患なし", 8, -34, GREY, 1.8),
                                   ("非透析 CKD", 9, -14, BLUE, 1.8),
                                   ("透析患者", 11, 22, RED, 2.6)):
        y = thr + off + np.sin(t * 34) * amp + np.sin(t * 11) * 6
        cv.ax.plot(x0 + t * pw, y, color=col, lw=lw, zorder=4)
        cv.text(x0 + pw + 8, thr + {-34: -46, -14: -14, 22: 22}[off], lab, size=10.0,
                color=col, ha="left")
    # 塗りつぶし（閾値以下）
    yd = thr + 22 + np.sin(t * 34) * 11 + np.sin(t * 11) * 6
    cv.ax.fill_between(x0 + t * pw, thr, yd, where=(yd > thr),
                       color="#fceeec", zorder=2)

    BW, BH = 900, 110
    bx = (W - BW) / 2
    by = y0 + ph + 40
    cv.box(bx, by, BW, BH, fc="#fceeec", ec=RED, lw=1.8, radius=8)
    cv.text(bx + BW / 2, by + 36, "MAP 65 mmHg 未満の面積の差",
            size=11.2, color=RED, weight="bold")
    d2 = "中央値で 18.4 mmHg・分（98.75%CI 11.3-25.6、p<0.001）"
    cv.text(bx + BW / 2, by + 76, d2, size=fit(cv, d2, BW - 60, 10.6),
            color=INK)

    th = textbox(cv, 70, by + BH + 30, W - 140,
                 ["123,761 例から、透析依存の慢性腎臓病・非透析の慢性腎臓病・"
                  "腎疾患なしの三群を",
                  "1 対 1 対 1 で一致させ（各群 1,886 例）、非心臓手術の術中血圧を比較した研究である。",
                  "透析患者では、平均動脈圧が 65 mmHg を下回っている"
                  "時間と深さの積が有意に大きかった。"],
                 10.6, style="navy", title="どういう研究か", title_color=NAVY,
                 pad_y=16)

    msg(cv, by + BH + 30 + th + 28,
        "「透析患者は血圧が下がりやすい」は印象ではなく、測られた事実である",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("q03_hypotension.png"))
    crop_bottom(P("q03_hypotension.png"))


# ---------------------------------------------------------------- q04
def q04():
    """透析患者の「正常値」の読み替え"""
    cv = Canvas(W, 1900)
    cap(cv, 44, "同じ検査値でも、意味が違う")

    ROWS = [("カリウム", RED, "6.0 mEq/L",
             "透析前には珍しくない。問題は値そのものより、"
             "上がった速さと心電図変化"),
            ("ナトリウム", BLUE, "低ナトリウム",
             "急速な補正は避ける。透析で一気に動かさない"),
            ("カルシウム", GREEN, "総 Ca が低い",
             "低アルブミンの影響。イオン化カルシウムで判断する"),
            ("リン", PURPLE, "高リン",
             "CKD-MBD の一部。血管石灰化の背景でもある"),
            ("ヘモグロビン", ORANGE, "9〜10 g/dL",
             "慢性的に低い値に適応している。輸血閾値も別に考える"),
            ("血小板", ORANGE, "数は正常",
             "数が正常でも機能は落ちている。数だけで安心しない"),
            ("尿素窒素・クレアチニン", GREY, "高い",
             "腎機能の指標としての意味がない。baseline との比較で見る"),
            ("酸塩基", TEAL, "代謝性アシドーシス",
             "透析の周期で動く。最終透析からの時間を必ず確認する"),
            ("体重", BLUE, "dry weight との差",
             "容量の唯一の実用的な指標。当日の体重を聞く")]

    y = 130
    for name, col, val, note in ROWS:
        h = 112
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.5, radius=8)
        cv.box(70, y, 300, h, fc="#fbfcfd", ec=col, lw=0, radius=8)
        cv.text(94, y + 44, name, size=fit(cv, name, 260, 11.4, "bold"),
                color=col, weight="bold", ha="left")
        cv.text(94, y + 80, val, size=fit(cv, val, 260, 10.0), color=GREY,
                ha="left")
        cv.text(390, y + h / 2, note, size=fit(cv, note, W - 480, 10.6),
                color=INK, ha="left")
        y += h + 10

    th = textbox(cv, 70, y + 12, W - 140,
                 ["検査値の解釈がずれると、そのあとの判断がすべてずれる。",
                  "「クレアチニンが高いから腎機能が悪い」という読み方は、"
                  "透析患者では意味をなさない。",
                  "見るべきは、その患者の baseline からどう動いたかである。"],
                 10.6, style="amber", title="読み替えの原則",
                 title_color="#9a6510", pad_y=16)
    cv.save(P("q04_lab_values.png"))
    crop_bottom(P("q04_lab_values.png"))


# ---------------------------------------------------------------- q05
def q05():
    """高カリウム血症の治療と効果量"""
    cv = Canvas(W, 1200)
    cap(cv, 44, "高カリウム血症の治療は、三つの働き方に分かれる")

    C = [("膜を守る", RED, "#fceeec",
          ["カルシウム製剤", "カリウム値は下がらない",
           "心電図変化があるときに使う", "効果は数分から数十分"]),
         ("細胞内へ移す", BLUE, "#eaf1f8",
          ["インスリン＋ブドウ糖", "β2 刺激薬の吸入・静注",
           "体内の総量は減らない", "平均 0.7〜1.2 mEq/L の低下"]),
         ("体外へ出す", GREEN, "#eaf5ee",
          ["透析", "利尿薬（尿が出るなら）",
           "陽イオン交換樹脂", "唯一、総量を減らす手段"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 140, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    y1 = 520
    cv.box(70, y1, W - 140, 240, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    t2 = "101 研究の系統的レビュー・メタ解析が示したこと"
    cv.text(W / 2, y1 + 38, t2, size=12.2, color=NAVY, weight="bold")
    L = ["インスリン＋ブドウ糖、サルブタモール吸入・静注、"
         "またはその併用による平均のカリウム低下は 0.7〜1.2 mEq/L",
         "エビデンスの確実性は「非常に低い」から「低い」と評価されている",
         "重炭酸ナトリウムの効果は限定的であった"]
    for j, ln in enumerate(L):
        cv.text(W / 2, y1 + 92 + 50 * j, ln,
                size=fit(cv, ln, W - 220, 10.6), color=INK)

    th = textbox(cv, 70, y1 + 270, W - 140,
                 ["この数字は、麻酔科にとって実務的な意味を持つ。",
                  "カリウム 6.5 の患者にインスリンとブドウ糖を投与しても、"
                  "下がるのは 1 mEq/L 程度である。",
                  "つまり「薬で下げてから導入する」という計画は、"
                  "しばしば期待どおりにはいかない。",
                  "透析ができるなら透析が、できないなら時間をかけた管理が必要になる。"],
                 10.6, style="red", title="効果量を知っておく",
                 title_color=RED, pad_y=16)
    cv.save(P("q05_hyperkalemia.png"))
    crop_bottom(P("q05_hyperkalemia.png"))


# ---------------------------------------------------------------- q06
def q06():
    """CPB 中のカリウム管理"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "人工心肺の回路の中で、カリウムをどうするか")

    cv.box(70, 130, W - 140, 190, fc="#fceeec", ec=RED, lw=1.8, radius=10)
    cv.text(W / 2, 172, "透析患者で CPB を回すと、カリウムは上がる方向に働く",
            size=12.4, color=RED, weight="bold")
    CAUSE = ["高カリウム心筋保護液が繰り返し投与される",
             "溶血と組織からの逸脱", "腎臓からの排泄がない"]
    for j, ln in enumerate(CAUSE):
        cv.text(W / 2, 216 + 36 * j, "・" + ln,
                size=fit(cv, "・" + ln, W - 240, 10.6), color=INK)

    C = [("血液濃縮器（ヘモフィルター）", BLUE, "#eaf1f8",
          ["回路に組み込む", "水を引くのが主目的",
           "カリウム除去の効率は限定的"]),
         ("ゼロバランス限外濾過", GREEN, "#eaf5ee",
          ["濾液と同量を補充する", "補充液を低カリウム透析液にする",
           "生理食塩水では高クロールになる"]),
         ("術中血液透析", PURPLE, "#f1ecf8",
          ["回路に透析を組み込む", "カリウム・尿素・クレアチニンが下がる",
           "CPB 離脱時のカテコラミンが少なく済んだ報告"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 360, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    th = textbox(cv, 70, 690, W - 140,
                 ["術中に血液濃縮器を用いた透析（後希釈式の血液透析濾過）と"
                  "通常の限外濾過を比較した日本の研究では、",
                  "透析群でカリウム・尿素窒素・クレアチニンが有意に低く、"
                  "CPB 離脱に要したカテコラミンが少なかった。",
                  "手術終了時の P/F 比も良好であった（450.8±149.7 対 279.3±153.5、"
                  "p<0.001）。"],
                 10.5, style="navy", title="術中透析という選択肢",
                 title_color=NAVY, pad_y=16)

    msg(cv, 690 + th + 28,
        "「離脱してから考える」のではなく、「回している間に整える」")
    cv.save(P("q06_cpb_potassium.png"))
    crop_bottom(P("q06_cpb_potassium.png"))


# ---------------------------------------------------------------- q07
def q07():
    """尿毒症性出血"""
    cv = Canvas(W, 1500)
    cap(cv, 44, "血小板の数が正常でも、止まらないことがある")

    STEP = [("尿毒素の蓄積", GREY), ("血小板の機能が落ちる", ORANGE),
            ("血小板と血管壁の相互作用が弱まる", RED),
            ("出血時間が延びる", RED)]
    x0 = 90
    bw, gap = (W - 180 - 3 * 26) / 4, 26
    for i, (t, col) in enumerate(STEP):
        x = x0 + (bw + gap) * i
        cv.box(x, 140, bw, 110, fc="#ffffff", ec=col, lw=1.7, radius=8)
        for j, ln in enumerate(cv.wrap(t, bw - 30, 10.4)):
            cv.text(x + bw / 2, 178 + LH(10.4, 1.35) * j, ln, size=10.4, color=INK)
        if i < 3:
            cv.arrow((x + bw + 4, 195), (x + bw + gap - 4, 195),
                     color="#b9c2cc", lw=1.8, head=9)

    C = [("悪化させるもの", RED, "#fceeec",
          ["貧血（赤血球が血小板を血管壁へ押しやる）",
           "抗血小板薬・抗凝固薬", "ヘパリン曝露（透析のたびに受けている）",
           "アシドーシス・低体温"]),
         ("できること", GREEN, "#eaf5ee",
          ["貧血の是正（Hb を上げると出血時間が短くなる）",
           "透析による尿毒素の除去", "抗血栓薬の調整",
           "デスモプレシン（後述の限界あり）"])]
    w = (W - 140 - 30) / 2
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 300, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    y1 = 630
    cv.box(70, y1, W - 140, 240, fc="#ffffff", ec=ORANGE, lw=1.8, radius=10)
    t2 = "デスモプレシンのメタ解析（21 研究 7,944 例）"
    cv.text(W / 2, y1 + 38, t2, size=12.2, color=ORANGE, weight="bold")
    L = [("全体の出血イベント", "OR 0.87（95%CI 0.57-1.33）", "有意差なし", GREY),
         ("無作為化試験だけに限ると", "OR 0.50（95%CI 0.29-0.87）", "有意に減少",
          GREEN),
         ("経鼻投与に限ると", "OR 0.52（95%CI 0.32-0.84）", "有意に減少", GREEN)]
    yy = y1 + 76
    for lab, val, judge, col in L:
        cv.text(110, yy + 20, lab, size=fit(cv, lab, 420, 10.6), color=INK,
                ha="left")
        cv.text(600, yy + 20, val, size=fit(cv, val, 400, 10.6), color=INK,
                ha="left")
        cv.text(W - 110, yy + 20, judge, size=10.6, color=col, ha="right",
                weight="bold")
        yy += 54

    th = textbox(cv, 70, y1 + 270, W - 140,
                 ["同じ薬について、「差がない」と「有意に減る」の両方が出ている。",
                  "違いは、どの研究を含めるかである。",
                  "観察研究を含めると差は消え、"
                  "無作為化試験に限ると有意になる。",
                  "この不一致そのものを、使うときの前提として知っておく。"],
                 10.6, style="amber", title="なぜ結論が割れるのか",
                 title_color="#9a6510", pad_y=16)
    cv.save(P("q07_uremic_bleeding.png"))
    crop_bottom(P("q07_uremic_bleeding.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (q01, q02, q03, q04, q05, q06, q07):
        fn()
        print("ok", fn.__name__)
