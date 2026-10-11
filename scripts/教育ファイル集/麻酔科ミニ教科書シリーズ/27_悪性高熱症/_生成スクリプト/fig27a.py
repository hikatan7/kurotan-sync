# -*- coding: utf-8 -*-
"""㉗ 悪性高熱症　図版 f01〜f10"""
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


def cap(cv, y, s, color=NAVY, size=12.5):
    sz = cv.fit_size([s], W - 90, size, weight="bold")
    cv.title(W / 2, y, s, size=sz, ha="center", color=color)


def msg(cv, y, s, fc="#e4f2f4", ec=TEAL, tc=TEAL, size=13.0, x=44, w=None):
    w = w or (W - 88)
    sz = cv.fit_size([s], w - 56, size, weight="bold")
    h = 30 + LH(sz, 1.5)
    cv.box(x, y, w, h, fc=fc, ec=ec, lw=2.0, radius=8)
    cv.text(x + w / 2, y + h / 2, s, size=sz, color=tc, weight="bold")
    return h


def fitlines(cv, lines, w, size, weight="normal", floor=8.6):
    s = cv.fit_size(lines, w, size, min_size=floor, weight=weight)
    if all(cv.width(l, s, weight) <= w for l in lines):
        return s, list(lines)
    out = []
    for l in lines:
        out.extend(cv.wrap(l, w, s, weight))
    return s, out


def card(cv, x, y, w, head, lines, color, fc, head_h=54, body_h=None,
         head_size=12.0, body_size=10.4, lh=1.65):
    hs, hl = fitlines(cv, [head], w - 36, head_size, weight="bold", floor=9.0)
    head_h = max(head_h, 20 + LH(hs, 1.45) * len(hl))
    cv.box(x, y, w, head_h, fc=color, ec=color, lw=0, radius=8)
    cv.block(x, y + (head_h - LH(hs, 1.45) * len(hl)) / 2, w, hl, hs,
             color="white", weight="bold")
    s, bl = fitlines(cv, lines, w - 40, body_size)
    bh = body_h or (30 + LH(s, lh) * len(bl))
    cv.box(x, y + head_h + 10, w, bh, fc=fc, ec=color, lw=1.8, radius=8)
    for j, ln in enumerate(bl):
        cv.text(x + w / 2, y + head_h + 10 + 15 + LH(s, lh) * (j + 0.5), ln,
                size=s, color=INK)
    return head_h + 10 + bh


# ---------------------------------------------------------------- f01
def f01():
    """RYR1 と Ca 放出"""
    cv = Canvas(W, 840)
    cap(cv, 44, "一つのチャネルが開きっぱなしになる")

    STEPS = [
        ("引き金薬が入る", ["揮発性吸入麻酔薬", "脱分極性筋弛緩薬"],
         RED, "#fceeec"),
        ("RYR1 が異常に開く", ["筋小胞体から細胞質へ", "Ca が漏れ続ける"],
         ORANGE, "#fdf3e3"),
        ("取り込みが追いつかない", ["Ca-ATPase の汲み戻しを", "放出速度が超える"],
         PURPLE, "#f1ecf8"),
        ("細胞質 Ca が上がりきる", ["筋収縮が持続", "ATP を際限なく消費"],
         BLUE, "#eaf1f8"),
        ("熱と二酸化炭素", ["ATP 消費と PLA2 活性化", "酸素消費も増える"],
         GREEN, "#eaf5ee"),
    ]
    CW, GAP, L = 272, 18, 60
    hmax = 0
    for i, (head, lines, color, fc) in enumerate(STEPS):
        x = L + i * (CW + GAP)
        hmax = max(hmax, card(cv, x, 110, CW, head, lines, color, fc,
                              head_size=10.6, body_size=9.8, lh=1.9))
        if i:
            cv.arrow((x - 16, 150), (x - 2, 150), color=GREY, lw=2.2, head=11)

    y = 110 + hmax + 34
    h = textbox(cv, 60, y, W - 120,
                ["ダントロレンはこの図の 2 段目にだけ効く。"
                 "RYR1 に直接作用して Ca 放出を抑える。",
                 "冷却も重炭酸も利尿も、3 段目から下で起きたことの後始末である。"
                 "順番を取り違えない。"],
                11.0, fc="white", ec=NAVY, title="どこに効く薬なのか",
                title_color=NAVY, lw=1.8)

    y2 = y + h + 30
    textbox(cv, 60, y2, W - 120,
            ["血中に出てくるもの：カリウム、乳酸、ミオグロビン、CK",
             "体で起きること：高二酸化炭素血症、高体温、筋組織の低酸素、筋壊死",
             "行き着く先：腎不全、不整脈、心停止、意識障害、DIC"],
            10.6, fc="#fceeec", ec=RED, title="細胞の外へ出ていくもの",
            title_color=RED, lw=1.8, lh_scale=1.9)
    cv.save(P("f01_ryr1.png"))


# ---------------------------------------------------------------- f02
def f02():
    """引き金薬と安全な薬"""
    cv = Canvas(W, 880)
    cap(cv, 44, "引き金になる薬は、二種類しかない")

    L, CW = 60, 690
    h1 = textbox(cv, L, 106, CW,
                 ["揮発性吸入麻酔薬",
                  "　セボフルラン／デスフルラン／イソフルラン／ハロタン",
                  "",
                  "脱分極性筋弛緩薬",
                  "　スキサメトニウム"],
                 11.4, fc="#fceeec", ec=RED, title="引き金になるもの",
                 title_color=RED, lw=2.4, lh_scale=1.9)
    h2 = textbox(cv, L + CW + 30, 106, CW,
                 ["静脈麻酔薬（プロポフォール、レミマゾラム、チオペンタール）",
                  "オピオイド（フェンタニル、レミフェンタニル、モルヒネ）",
                  "非脱分極性筋弛緩薬（ロクロニウム、ベクロニウム）",
                  "局所麻酔薬、区域麻酔（脊髄くも膜下・硬膜外を含む）",
                  "亜酸化窒素、ベンゾジアゼピン、ケタミン"],
                 10.6, fc="#eaf5ee", ec=GREEN, title="安全に使えるもの",
                 title_color=GREEN, lw=2.4, lh_scale=1.9)
    y = 106 + max(h1, h2) + 34

    h3 = textbox(cv, 60, y, W - 120,
                 ["引き金薬を使って無事に終わった麻酔歴があっても、素因は否定できない。"
                  "浸透率は 40.6% と報告されている。",
                  "逆に、従来安全とされる麻酔で発症した報告もある"
                  "（477 例中 7 例）。「安全な薬だから起きない」とは言えない。",
                  "暑熱・湿潤環境、激しい運動、ストレスも"
                  "筋小胞体からの Ca 放出速度を高める。"],
                 10.8, fc="white", ec=NAVY, title="例外のほうを覚えておく",
                 title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h3 + 30, "ダントロレンとカルシウム拮抗薬の併用は禁忌。"
                         "致死的な高カリウム血症の報告がある。",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("f02_triggers.png"))


# ---------------------------------------------------------------- f03
def f03():
    """三つの数字"""
    cv = Canvas(W, 760)
    cap(cv, 44, "三つの数字 ── 発症・保因・浸透")

    NUM = [("0.18-3.9", "／10 万麻酔",
            ["臨床的に発症する頻度", "（JSA 2025）"], RED, "#fceeec"),
           ("1 / 856 - 1075", "人",
            ["原因遺伝子変異を持つ人の", "推定頻度。発症よりずっと多い"],
            ORANGE, "#fdf3e3"),
           ("40.6", "%",
            ["浸透率。素因があっても", "必ず発症するわけではない"],
            PURPLE, "#f1ecf8")]
    CW, GAP, L = 448, 28, 60
    for i, (n, unit, lines, color, fc) in enumerate(NUM):
        x = L + i * (CW + GAP)
        cv.box(x, 106, CW, 266, fc=fc, ec=color, lw=2.4, radius=10)
        ns = cv.fit_size([n], CW - 80, 30, min_size=16, weight="bold")
        cv.text(x + CW / 2, 162, n, size=ns, color=color, weight="bold")
        cv.text(x + CW / 2, 222, unit, size=12.0, color=color, weight="bold")
        s, ls = fitlines(cv, lines, CW - 48, 10.4, floor=8.8)
        cv.block(x + 24, 256, CW - 48, ls, s, color=INK, lh=LH(s, 1.75))

    y = 406
    h = textbox(cv, 60, y, W - 120,
                ["1960 年代から日本で報告された症例は 600 例を超える。"
                 "その半数以上が 18 歳未満で、男女比はおよそ 3 : 1。",
                 "死亡率は 1960 年代の 70-80% から、2010 年には 0-18.2% まで下がった。"
                 "ダントロレンを使った症例に限れば 10% 以下。",
                 "術後悪性高熱症は MH 症例の 1.9-8.3% と稀だが、死亡率は 12.2%。"],
                10.8, fc="white", ec=NAVY, title="日本での実数",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 30,
        "「一生に一度会うかどうか」の病気が、"
        "会ったときに 10 分で決着する。だから手順を紙にしておく。")
    cv.save(P("f03_numbers.png"))


# ---------------------------------------------------------------- f04
def f04():
    """初発症状"""
    cv = Canvas(W, 780)
    cap(cv, 44, "最初に出るのは、熱ではない")

    ROWS = [("ETCO2・PaCO2 の上昇", 30.7, 15.0),
            ("咬筋強直（開口障害）", 24.8, 29.5),
            ("原因不明の頻脈", 21.1, 27.9)]
    L, TOP = 420, 130
    BW = 340
    cv.text(L + BW / 2, TOP - 34, "Riazi 2014", size=11.0, color=BLUE,
            weight="bold")
    cv.text(L + BW + 120 + BW / 2, TOP - 34, "Visoiu 2014", size=11.0,
            color=PURPLE, weight="bold")
    for i, (name, a, b) in enumerate(ROWS):
        y = TOP + i * 86
        ns2, nl2 = fitlines(cv, [name], 340, 11.4, weight="bold", floor=9.4)
        cv.block(60, y + 22 - LH(ns2, 1.35) * len(nl2) / 2, 340, nl2, ns2,
                 color=NAVY, weight="bold", ha="right", lh=LH(ns2, 1.35))
        cv.rect(L, y + 6, BW * a / 35.0, 32, fc=BLUE)
        cv.text(L + BW * a / 35.0 + 12, y + 22, "%.1f%%" % a, size=10.6,
                color=BLUE, ha="left")
        x2 = L + BW + 140
        cv.rect(x2, y + 6, BW * b / 35.0, 32, fc=PURPLE)
        cv.text(x2 + BW * b / 35.0 + 12, y + 22, "%.1f%%" % b, size=10.6,
                color=PURPLE, ha="left")

    y = TOP + 3 * 86 + 16
    h = textbox(cv, 60, y, W - 120,
                ["同じ年に出た二つの報告で、初発症状の順位が入れ替わっている。"
                 "つまり「この症状から始まる」とは決まっていない。",
                 "体温上昇はむしろ遅れて出る。"
                 "「高熱が出ていないから違う」という除外の仕方が最も危険である。",
                 "分時換気量を増やしても下がらない ETCO2 が、"
                 "実務上いちばん早く気づける手がかりになる。"],
                10.8, fc="white", ec=NAVY, title="順序は決まっていない",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 30,
        "PaCO2 ＜ ETCO2 という逆転は、"
        "この病態でしか説明しにくい所見である。")
    cv.save(P("f04_first_signs.png"))


# ---------------------------------------------------------------- f05
def f05():
    """MH を疑う症状（JSA）"""
    cv = Canvas(W, 760)
    cap(cv, 44, "「MH を疑う症状」── 日本麻酔科学会が挙げる九つ")

    ITEMS = ["説明のできない ETCO2 の高値",
             "原因不明の頻脈",
             "体温上昇速度 ≧ 0.5 ℃/15 分",
             "体温 ≧ 38.8 ℃",
             "開口障害（咬筋強直）",
             "筋強直",
             "コーラ色の尿",
             "代謝性アシドーシス（BE ≦ −8.0）",
             "PaCO2 ＜ ETCO2"]
    CW, GAP, L = 448, 28, 60
    for i, t in enumerate(ITEMS):
        r, c = i // 3, i % 3
        x = L + c * (CW + GAP)
        y = 110 + r * 96
        color = RED if i in (0, 1, 3, 5) else NAVY
        fc = "#fceeec" if i in (0, 1, 3, 5) else "#eef1f6"
        s, ls = fitlines(cv, [t], CW - 90, 11.2, weight="bold", floor=9.6)
        bh = max(78, 26 + LH(s, 1.4) * len(ls))
        cv.box(x, y, CW, bh, fc=fc, ec=color, lw=2.0, radius=8)
        cv.box(x, y, 56, bh, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + 28, y + bh / 2, str(i + 1), size=15, color="white",
                weight="bold")
        cv.block(x + 74, y + bh / 2 - LH(s, 1.4) * len(ls) / 2, CW - 90, ls,
                 s, color=color, weight="bold", ha="left", lh=LH(s, 1.4))

    y = 110 + 3 * 96 + 14
    h = textbox(cv, 60, y, W - 120,
                ["初期症状 ── 分時換気量を増やしてもなお上昇する ETCO2、"
                 "原因不明の頻脈、高二酸化炭素血症、高体温、筋強直 ── があれば、"
                 "それだけでダントロレン投与の適応である。",
                 "高カリウム値と高乳酸値は診断を助けるが、"
                 "それだけでダントロレンを決める根拠にはしない。"],
                10.8, fc="white", ec=NAVY, title="どれで踏み切るか",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 26, "確定診断を待たない。疑ったら投与する。")
    cv.save(P("f05_nine_signs.png"))


# ---------------------------------------------------------------- f06
def f06():
    """治療の流れ"""
    cv = Canvas(W, 900)
    cap(cv, 44, "疑ってから 10 分でやること")

    cv.box(300, 96, 920, 68, fc=NAVY, ec=NAVY, lw=0, radius=8)
    ds = cv.fit_size(["「悪性高熱症による緊急事態」を宣言する"], 860, 13.6,
                     weight="bold")
    cv.text(760, 130, "「悪性高熱症による緊急事態」を宣言する", size=ds,
            color="white", weight="bold")

    COLS = [
        ("止める・呼ぶ", RED, "#fceeec",
         ["揮発性吸入麻酔薬とスキサメトニウムを中止",
          "静脈麻酔に変更する",
          "人を集める",
          "執刀医に手術の早期終了を要請",
          "筋弛緩は非脱分極性に"]),
        ("流す", ORANGE, "#fdf3e3",
         ["高流量純酸素（10 L/分以上）",
          "分時換気量を 2 倍以上",
          "（できれば）気化器を外し回路を交換",
          "活性炭フィルタがあれば吸気・呼気に"]),
        ("入れる", BLUE, "#eaf1f8",
         ["専用の太い末梢静脈路を確保",
          "1 瓶 20 mg を注射用水 60 mL で溶解",
          "1.0 mg/kg（できれば 2.0 mg/kg）を",
          "約 10 分で投与",
          "改善するまで繰り返す"]),
    ]
    CW, GAP, L = 448, 28, 60
    hmax = 0
    for i, (head, color, fc, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.arrow((760, 166), (x + CW / 2, 196), color=color, lw=2.2, head=12)
        hmax = max(hmax, card(cv, x, 204, CW, head, lines, color, fc,
                              body_size=10.2, lh=1.85))

    y = 204 + hmax + 30
    h = textbox(cv, 60, y, W - 120,
                ["動脈ラインを確保する。冷却した生理食塩水を静注する（最大 50-60 mL/kg）。",
                 "室温を下げ、送風で体表を冷やす。中枢温 38 ℃を下回ったら冷却は止める。",
                 "不整脈は適宜治療する。ただしカルシウム拮抗薬は使わない。",
                 "高カリウム血症、代謝性アシドーシス、"
                 "ミオグロビン尿に対する対症療法を並行する。"],
                10.6, fc="white", ec=NAVY, title="同時に進める対症療法",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 28,
        "ダントロレンだけが原因に効く。ほかはすべて、"
        "起きてしまったことの後始末である。")
    cv.save(P("f06_first10min.png"))


# ---------------------------------------------------------------- f07
def f07():
    """ダントロレンの用量：日本と欧米"""
    cv = Canvas(W, 820)
    cap(cv, 44, "ダントロレンの用量 ── 日本と欧米で違う")

    HEAD = ["", "日本の添付文書", "JSA 2016", "JSA 2025", "EMHG 2024"]
    ROWS = [
        ("初回量", "1 mg/kg", "1.0（できれば 2.0）mg/kg",
         "1.0 以上、できれば 2.0 mg/kg", "2〜2.5 mg/kg"),
        ("投与時間", "──", "15 分程度", "10 分程度", "10 分ごとに反復"),
        ("追加", "1 mg/kg ずつ", "適宜繰り返す", "症状改善まで",
         "10 分ごとに 2〜2.5 mg/kg"),
        ("上限", "総量 7 mg/kg", "最大 7 mg/kg",
         "上限を設けない", "1 回 300 mg・累積 10 mg/kg"),
        ("溶解", "注射用水のみ", "1 瓶 60 mL", "1 瓶 60 mL", "製剤による"),
    ]
    L, R, TOP = 60, W - 60, 106
    ws = [190] + [(R - L - 190) / 4] * 4
    RH = 74
    for c in range(5):
        x = L + sum(ws[:c])
        cv.rect(x, TOP, ws[c] - 4, 48, fc=NAVY if c else "white")
        if c:
            s = cv.fit_size([HEAD[c]], ws[c] - 20, 11.4, weight="bold")
            cv.text(x + ws[c] / 2 - 2, TOP + 24, HEAD[c], size=s,
                    color="white", weight="bold")
    for r, row in enumerate(ROWS):
        y = TOP + 54 + r * RH
        for c in range(5):
            x = L + sum(ws[:c])
            fc = "#eef1f6" if c == 0 else ("#fafbfc" if r % 2 else "white")
            cv.rect(x, y, ws[c] - 4, RH - 6, fc=fc, ec="#dde2e8", lw=1.0)
            s, ls = fitlines(cv, [row[c]], ws[c] - 24, 10.4,
                             weight="bold" if c == 0 else "normal", floor=8.4)
            cv.block(x + 10, y + (RH - 6) / 2 - LH(s, 1.35) * len(ls) / 2,
                     ws[c] - 24, ls, s,
                     color=NAVY if c == 0 else INK,
                     weight="bold" if c == 0 else "normal",
                     lh=LH(s, 1.35))

    y = TOP + 54 + 5 * RH + 18
    h = textbox(cv, 60, y, W - 120,
                ["2025 年版の最大の変更は、上限を書かなくなったことである。",
                 "添付文書は 7 mg/kg のままだが、"
                 "効いている限り 10 mg/kg を超える欧米の方針を紹介し、",
                 "「症状が改善するまで十分量を投与する」とした。"
                 "投与時間も 15 分から 10 分に短くなった。"],
                10.8, fc="white", ec=NAVY, title="2016 年版から変わったところ",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 26,
        "上限が消えたのではない。「上限で止める理由がない」と書き換えられた。")
    cv.save(P("f07_dose.png"))


# ---------------------------------------------------------------- f08
def f08():
    """在庫の算術"""
    cv = Canvas(W, 920)
    cap(cv, 44, "何本あるか ── 在庫の算術")

    cv.box(60, 106, W - 120, 74, fc="#e8edf5", ec=NAVY, lw=2.2, radius=8)
    cv.text(W / 2, 143, "ダントロレン 1 瓶 = 20 mg。"
                        "溶解には 1 瓶あたり注射用水 60 mL が要る。",
            size=13.0, color=NAVY, weight="bold")

    HEAD = ["体重", "1 mg/kg", "2 mg/kg", "7 mg/kg", "10 mg/kg"]
    ROWS = [("30 kg", "2 本", "3 本", "11 本", "15 本"),
            ("50 kg", "3 本", "5 本", "18 本", "25 本"),
            ("70 kg", "4 本", "7 本", "25 本", "35 本"),
            ("90 kg", "5 本", "9 本", "32 本", "45 本")]
    L, R, TOP = 60, W - 60, 202
    ws = [(R - L) / 5] * 5
    RH = 62
    for c in range(5):
        x = L + c * ws[0]
        cv.rect(x, TOP, ws[0] - 4, 46, fc=NAVY)
        cv.text(x + ws[0] / 2 - 2, TOP + 23, HEAD[c], size=11.4,
                color="white", weight="bold")
    for r, row in enumerate(ROWS):
        y = TOP + 52 + r * RH
        for c in range(5):
            x = L + c * ws[0]
            fc = "#eef1f6" if c == 0 else ("#fceeec" if c >= 3 else "white")
            cv.rect(x, y, ws[0] - 4, RH - 6, fc=fc, ec="#dde2e8", lw=1.0)
            cv.text(x + ws[0] / 2 - 2, y + (RH - 6) / 2, row[c], size=11.2,
                    color=NAVY if c == 0 else (RED if c >= 3 else INK),
                    weight="bold" if c == 0 or c >= 3 else "normal")

    y = TOP + 52 + 4 * RH + 20
    h = textbox(cv, 60, y, W - 120,
                ["当院の備蓄は手術室内 6 本、薬剤管理庫 8 本の計 14 本（280 mg）。"
                 "70 kg の患者に 2 mg/kg を入れた時点で、残りは 7 本になる。",
                 "EMHG は「即座に使える 36 瓶と、1 時間以内に手に入る 24 瓶」を求めている。"
                 "JSA 2025 は本数を決めず、施設ごとに判断するとした。",
                 "つまり「何本あるか」ではなく"
                 "「足りなくなったとき、次の 24 本はどこから来るか」を決めておく。"],
                10.8, fc="white", ec=RED, title="在庫は、たいてい足りない",
                title_color=RED, lw=2.0, lh_scale=1.9)

    msg(cv, y + h + 26,
        "溶解にも時間がかかる。35 本を 60 mL ずつ溶かすのは、一人では終わらない。")
    cv.save(P("f08_stock.png"))


# ---------------------------------------------------------------- f09
def f09():
    """鑑別"""
    cv = Canvas(W, 900)
    cap(cv, 44, "似ているもの ── 高体温と代謝亢進を起こす病態")

    ROWS = [
        ("敗血症", "感染源、経過が緩やか、CK は上がらないことが多い",
         "培養・炎症反応。ETCO2 の急上昇は説明しにくい", BLUE),
        ("甲状腺クリーゼ", "頻脈・発熱・意識障害。誘因は手術・感染",
         "甲状腺機能。筋強直は出ない", BLUE),
        ("悪性症候群（NMS）", "抗精神病薬。数日かけて進む",
         "経過が遅い。引き金薬が違う", PURPLE),
        ("セロトニン症候群", "セロトニン作動薬。ミオクローヌス・反射亢進",
         "腱反射亢進とクローヌスが手がかり", PURPLE),
        ("熱中症・労作性横紋筋融解", "暑熱、運動。RYR1 変異との関連が報告されている",
         "MH 素因と重なる家系がある。既往として必ず聞く", ORANGE),
        ("筋ジストロフィーの横紋筋融解", "スキサメトニウムや揮発性麻酔薬で高 K・心停止",
         "MH ではないが同じ薬で起きる。ダントロレンは効かない", RED),
        ("駆血解除・止血帯解除", "一過性の ETCO2 上昇",
         "数分で戻る。持続しない", GREY),
        ("換気不足・回路のトラブル", "ETCO2 上昇の最も多い原因",
         "まず回路と設定を見る。DOPE", GREY),
    ]
    L, TOP = 60, 106
    for i, (name, feat, key, color) in enumerate(ROWS):
        y = TOP + i * 86
        cv.box(L, y, W - 120, 74, fc="white", ec="#dde2e8", lw=1.4, radius=6)
        cv.rect(L, y, 8, 74, fc=color)
        ns, nl = fitlines(cv, [name], 330, 11.4, weight="bold", floor=9.0)
        cv.block(L + 26, y + 37 - LH(ns, 1.35) * len(nl) / 2, 330, nl, ns,
                 color=color, weight="bold", ha="left", lh=LH(ns, 1.35))
        fs, fl = fitlines(cv, [feat], 520, 10.2, floor=8.6)
        cv.block(L + 380, y + 37 - LH(fs, 1.35) * len(fl) / 2, 520, fl, fs,
                 color=INK, ha="left", lh=LH(fs, 1.35))
        ks, kl = fitlines(cv, [key], 460, 10.0, floor=8.4)
        cv.block(L + 920, y + 37 - LH(ks, 1.35) * len(kl) / 2, 460, kl, ks,
                 color=GREY, ha="left", lh=LH(ks, 1.35))

    msg(cv, TOP + 8 * 86 + 16,
        "鑑別に時間をかけない。"
        "「換気量を増やしても ETCO2 が下がらない」なら、先にダントロレンを準備する。")
    cv.save(P("f09_differential.png"))


# ---------------------------------------------------------------- f10
def f10():
    """術後悪性高熱症"""
    cv = Canvas(W, 780)
    cap(cv, 44, "術後悪性高熱症（PMH）── 麻酔が終わってから始まる")

    NUM = [("1.9 - 8.3", "%", ["MH 症例に占める割合"], BLUE, "#eaf1f8"),
           ("12.2", "%", ["死亡率。術中発症より高い"], RED, "#fceeec"),
           ("40", "分以内", ["多くはここで発症する", "（JSA 2025）"],
            ORANGE, "#fdf3e3")]
    CW, GAP, L = 448, 28, 60
    for i, (n, unit, lines, color, fc) in enumerate(NUM):
        x = L + i * (CW + GAP)
        cv.box(x, 106, CW, 214, fc=fc, ec=color, lw=2.4, radius=10)
        ns = cv.fit_size([n], CW - 140, 32, min_size=16, weight="bold")
        nw = cv.width(n, ns, "bold")
        uw = cv.width(unit, 12.5, "bold")
        x0 = x + (CW - (nw + 14 + uw)) / 2
        cv.text(x0, 166, n, size=ns, color=color, weight="bold", ha="left")
        cv.text(x0 + nw + 14, 172, unit, size=12.5, color=color,
                weight="bold", ha="left")
        s, ls = fitlines(cv, lines, CW - 48, 10.6, floor=8.8)
        cv.block(x + 24, 214, CW - 48, ls, s, color=INK, lh=LH(s, 1.8))

    y = 356
    h = textbox(cv, 60, y, W - 120,
                ["術中は何事もなく終わり、抜管後・帰室後・数日後に症状が出る。"
                 "誘因と機序は術中発症の MH とは違う可能性がある。",
                 "疑う症状は五つ ── 説明のできない ETCO2 の高値、コーラ色の尿、"
                 "代謝性アシドーシス（BE ≦ −8.0）、高 CK 血症、高ミオグロビン血症。",
                 "治療は術中の MH に準じる。"
                 "麻酔科医を呼び、挿管し、過換気とし、ダントロレンを入れる。",
                 "JSA 2025 は「少なくとも 24 時間は監視する」とした。"
                 "発症したあとの再燃もあるためである。"],
                10.8, fc="white", ec=NAVY, title="どう捉えるか",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 28,
        "退室基準を満たしていても、"
        "「説明のつかない発熱」だけは麻酔科に戻す約束にしておく。")
    cv.save(P("f10_pmh.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10):
        fn()
        print("ok", fn.__name__)
