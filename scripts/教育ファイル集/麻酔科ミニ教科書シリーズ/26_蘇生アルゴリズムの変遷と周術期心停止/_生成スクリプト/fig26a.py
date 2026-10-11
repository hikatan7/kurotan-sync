# -*- coding: utf-8 -*-
"""㉖ 蘇生アルゴリズムの変遷と周術期心停止　図版 f01〜f15"""
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
SOFT = "#f2f4f6"


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
    """幅 w に収まる字送りを返す。floor まで縮めても入らない行は折り返す。"""
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
    """60年の年表"""
    cv = Canvas(W, 1190)
    cap(cv, 44, "心肺蘇生ガイドラインの 60 年 ── 会議と公表")

    ITEMS = [
        (1966, "第 1 回会議（NAS-NRC）",
         "医療者に外胸圧迫の訓練を。市民には教えない方針", NAVY, "#e8edf5"),
        (1974, "最初の標準（JAMA）",
         "市民への CPR 訓練を解禁。ACLS という言葉が入る", BLUE, "#eaf1f8"),
        (1980, "1979 年会議の公表",
         "ACLS を体系として確立。訓練・試験・監督の推奨", BLUE, "#eaf1f8"),
        (1986, "1985 年会議の公表",
         "小児 BLS／ALS が独立。研究の蓄積を反映", BLUE, "#eaf1f8"),
        (1992, "第 5 回会議・ILCOR 創設",
         "救命の連鎖を採用。国際調整の枠組みができる", PURPLE, "#f1ecf8"),
        (2000, "初の国際ガイドライン",
         "初のエビデンスベース。推奨クラスの導入", PURPLE, "#f1ecf8"),
        (2005, "質への回帰",
         "30 : 2 に統一。3 連続ショックを 1 回に", GREEN, "#eaf5ee"),
        (2010, "C-A-B（CPR 50 周年）",
         "順序を入れ替え。アトロピンを削除", GREEN, "#eaf5ee"),
        (2015, "連続エビデンス評価へ",
         "テンポ 100-120／深さ 5-6 cm。バソプレシン削除", ORANGE, "#fdf3e3"),
        (2020, "6 本目の鎖「回復」",
         "491 勧告。妊娠・オピオイドのアルゴリズム新設", ORANGE, "#fdf3e3"),
        (2025, "760 勧告・鎖を 1 本に",
         "背部叩打が先。静脈路優先。機械的 CPR は非推奨", RED, "#fceeec"),
        (2026, "JRC 蘇生ガイドライン 2025",
         "書籍版は 2026 年 7 月 13 日刊行", TEAL, "#e4f2f4"),
    ]
    CW, GAP, L, TOP, RH, CH = 690, 30, 60, 106, 158, 140
    for i, (yr, head, body, color, fc) in enumerate(ITEMS):
        col, row = i // 6, i % 6
        x = L + col * (CW + GAP)
        y = TOP + row * RH
        cv.box(x, y, CW, CH, fc=fc, ec=color, lw=2.0, radius=8)
        cv.box(x, y, 132, CH, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + 66, y + CH / 2, str(yr), size=17.0, color="white",
                weight="bold")
        hs, hl = fitlines(cv, [head], CW - 170, 12.2, weight="bold", floor=9.5)
        cv.block(x + 150, y + 18, CW - 170, hl, hs, color=color,
                 weight="bold", ha="left")
        bs, bl = fitlines(cv, [body], CW - 170, 10.5, floor=8.8)
        cv.block(x + 150, y + 68, CW - 170, bl, bs, color=INK,
                 ha="left", lh=LH(bs, 1.5))

    msg(cv, TOP + 6 * RH + 6,
        "会議の年と公表の年は 1 年ずれる。"
        "1973 年会議は 1974 年に、1979 年会議は 1980 年に公表された。")
    cv.save(P("f01_timeline.png"))


# ---------------------------------------------------------------- f02
def f02():
    """1960 年に三つの技術が合流した"""
    cv = Canvas(W, 860)
    cap(cv, 44, "1960 年 ── 三本の川が一つになった")

    STREAMS = [
        ("換気", ["1732　Tossach が口対口で炭鉱夫を蘇生",
                "1740　パリ科学アカデミーが溺水に推奨",
                "1856/58　Hall 法・Silvester 法",
                "1954-56　Elam・Safar が呼気の十分性を証明"],
         BLUE, "#eaf1f8"),
        ("循環", ["1874　Schiff の開胸心マッサージ",
                "1878　Boehm が猫で外胸圧迫",
                "1891　Maass がヒトで外胸圧迫を提唱",
                "1933　Kouwenhoven が犬で再発見"],
         GREEN, "#eaf5ee"),
        ("除細動", ["1775　Abildgaard の逆説的な鶏",
                 "1947　Beck が開胸下で初成功",
                 "1956　Zoll が体外式で初成功",
                 "1957　可搬型除細動器（90 kg）"],
         PURPLE, "#f1ecf8"),
    ]
    CW, GAP, L = 448, 28, 60
    hmax = 0
    for i, (head, lines, color, fc) in enumerate(STREAMS):
        x = L + i * (CW + GAP)
        hmax = max(hmax, card(cv, x, 100, CW, head, lines, color, fc,
                              body_size=10.6, lh=1.9))
    by = 100 + hmax + 60
    for i in range(3):
        x = L + i * (CW + GAP) + CW / 2
        cv.arrow((x, 100 + hmax + 6), (760 - 220 + i * 220, by - 6),
                 color="#c3cad3", lw=2.0, head=11)
    t1 = "1960　Kouwenhoven・Jude・Knickerbocker"
    t2 = "「二つの手さえあればよい」── 現代の CPR が成立"
    bw = max(cv.width(t1, 13.5, "bold"), cv.width(t2, 11.5)) + 90
    cv.box(760 - bw / 2, by, bw, 110, fc="#e8edf5", ec=NAVY, lw=2.4, radius=10)
    cv.text(760, by + 36, t1,
            size=13.5, color=NAVY, weight="bold")
    cv.text(760, by + 76, t2,
            size=11.5, color=INK)

    msg(cv, by + 140, "最初の症例集は、その多くが麻酔導入時の心停止だった。"
                      "現代の CPR は手術室から出てきた技術である。")
    cv.save(P("f02_three_streams.png"))


# ---------------------------------------------------------------- f03
def f03():
    """救命の連鎖の変遷"""
    cv = Canvas(W, 830)
    cap(cv, 44, "救命の連鎖 ── 4 環から 6 環へ、4 本から 1 本へ")

    ROWS = [
        ("1991／1992", 4, ["早期認識", "早期 CPR", "早期除細動", "早期 ALS"],
         BLUE, "Cummins が提唱し、1992 年版が採用"),
        ("2000-2015", 5, ["認識と通報", "早期 CPR", "早期除細動",
                          "二次救命処置", "心拍再開後の治療"],
         GREEN, "心拍再開後の治療が 5 本目として加わる"),
        ("2020", 6, ["認識と通報", "早期 CPR", "早期除細動",
                     "二次救命処置", "心拍再開後", "回復"],
         ORANGE, "「回復」が 6 本目に。院内・院外×成人・小児で 4 種類"),
        ("2025", 6, ["認識と通報", "早期 CPR", "早期除細動",
                     "二次救命処置", "心拍再開後", "回復"],
         RED, "4 種類を 1 本に統合。7 本目「予防」は定義を詰めてから"),
    ]
    L, R = 290, W - 70
    for r, (era, n, labels, color, note) in enumerate(ROWS):
        y = 130 + r * 152
        cv.text(268, y + 30, era, size=11.6, color=NAVY, weight="bold",
                ha="right")
        cw = (R - L - (n - 1) * 12) / n
        for i, lab in enumerate(labels):
            x = L + i * (cw + 12)
            cv.box(x, y, cw, 60, fc="white", ec=color, lw=2.2, radius=8)
            s = cv.fit_size([lab], cw - 20, 10.8, weight="bold")
            cv.text(x + cw / 2, y + 30, lab, size=s, color=color,
                    weight="bold")
            if i:
                cv.ax.plot([x - 12, x], [y + 30, y + 30], color=color, lw=2.2)
        s = cv.fit_size([note], R - L, 10.2)
        cv.text(L, y + 88, note, size=s, color=GREY, ha="left")

    msg(cv, 748, "鎖が増えたのは、治療が増えたからではない。"
                 "「どこで切れるか」を数える単位が増えたからである。")
    cv.save(P("f03_chain.png"))


# ---------------------------------------------------------------- f04
def f04():
    """A-B-C から C-A-B へ"""
    cv = Canvas(W, 900)
    cap(cv, 44, "2010 年 ── 順序を入れ替えた理由")

    L, CW = 60, 690
    from figlib import boxrow
    hh = boxrow(cv, L, 110, CW, 30, [
        ("A-B-C（〜2005）",
         ["気道を確保し、換気を 2 回入れてから、圧迫を始める。",
          "気道確保に手間取ると、最初の圧迫まで 30 秒近くかかる。",
          "訓練を受けていない市民は、口対口で手が止まる。"], "grey"),
        ("C-A-B（2010〜）",
         ["胸骨圧迫を最初に置く。換気は 30 回圧迫のあとに回す。",
          "成人の突然の心停止は、直後の血液になお酸素が残っている。",
          "圧迫の開始が早まり、市民が手を出しやすくなる。"], "green"),
    ], 11.0, min_h=210, lw=2.0)
    cv.arrow((L + CW + 4, 110 + hh / 2), (L + CW + 26, 110 + hh / 2), color=NAVY,
             lw=3.0, head=16)

    by = 110 + hh + 30
    ITEMS = [("アトロピン", "PEA・心静止から削除"),
             ("輪状軟骨圧迫", "ルーチン使用を非推奨"),
             ("「見て・聴いて・感じて」", "呼吸確認の手順から削除"),
             ("テンポと深さ", "「約 100 回」→「100 回以上」／「4-5 cm」→「5 cm 以上」")]
    lh = LH(10.8, 1.7)
    bh = 76 + lh * len(ITEMS) + 10
    cv.box(60, by, W - 120, bh, fc="white", ec=NAVY, lw=1.8, radius=8)
    cv.text(W / 2, by + 36, "同じ年に消えたもの・変わったもの", size=12.5,
            color=NAVY, weight="bold")
    for i, (a, b) in enumerate(ITEMS):
        y = by + 76 + lh * (i + 0.5)
        cv.text(440, y, a, size=10.8, color=RED, weight="bold", ha="right")
        cv.text(462, y, "→", size=10.8, color=GREY, ha="center")
        cv.text(488, y, b, size=10.8, color=INK, ha="left")

    msg(cv, by + bh + 28, "順序の変更は新しい治療ではない。"
                 "「最初の 30 秒に何をしているか」を作り直したのである。")
    cv.save(P("f04_cab.png"))


# ---------------------------------------------------------------- f05
def f05():
    """数値の歴史"""
    cv = Canvas(W, 790)
    cap(cv, 44, "数値は少しずつ動いてきた ── 圧迫の深さ・テンポ・圧迫換気比")

    HEAD = ["", "1992", "2000", "2005", "2010", "2015〜2025"]
    ROWS = [
        ("圧迫のテンポ", "80-100 回/分", "約 100 回/分", "約 100 回/分",
         "100 回/分以上", "100-120 回/分"),
        ("圧迫の深さ（成人）", "3.8-5.1 cm", "3.8-5.1 cm", "4-5 cm",
         "5 cm 以上", "5-6 cm"),
        ("圧迫：換気（1 人法）", "15 : 2", "15 : 2", "30 : 2",
         "30 : 2", "30 : 2"),
        ("VF への初回対応", "3 連続ショック", "3 連続ショック", "1 ショック",
         "1 ショック", "1 ショック"),
        ("ショック後", "直ちにリズム確認", "直ちにリズム確認",
         "直ちに CPR 2 分", "直ちに CPR 2 分", "直ちに CPR 2 分"),
    ]
    L, R, TOP = 60, W - 60, 110
    ws = [300] + [(R - L - 300) / 5] * 5
    RH = 62
    for c in range(6):
        x = L + sum(ws[:c])
        cv.rect(x, TOP, ws[c] - 4, 46, fc=NAVY if c else "white")
        if c:
            cv.text(x + ws[c] / 2 - 2, TOP + 23, HEAD[c], size=11.2,
                    color="white", weight="bold")
    for r, row in enumerate(ROWS):
        y = TOP + 52 + r * RH
        for c in range(6):
            x = L + sum(ws[:c])
            fc = "#eef1f6" if c == 0 else ("#fafbfc" if r % 2 else "white")
            cv.rect(x, y, ws[c] - 4, RH - 6, fc=fc, ec="#dde2e8", lw=1.0)
            s = cv.fit_size([row[c]], ws[c] - 24, 10.6,
                            weight="bold" if c == 0 else "normal")
            cv.text(x + ws[c] / 2 - 2, y + (RH - 6) / 2, row[c], size=s,
                    color=NAVY if c == 0 else INK,
                    weight="bold" if c == 0 else "normal")

    msg(cv, 500, "「正しい深さ」が変わったのではない。"
                 "測れるようになったぶんだけ、幅が狭くなっただけである。")

    textbox(cv, 60, 590, W - 120,
            ["深さの上限（6 cm）は、深すぎる圧迫が損傷を増やすという観察から 2015 年に入った。",
             "テンポの上限（120 回/分）も同じ年に入った。速すぎると戻りが浅くなるためである。"],
            10.6, fc="white", ec=GREY, title="上限が書かれた理由",
            title_color=NAVY, lw=1.6)
    cv.save(P("f05_numbers.png"))


# ---------------------------------------------------------------- f06
def f06():
    """薬の盛衰"""
    cv = Canvas(W, 920)
    cap(cv, 44, "薬は増えてきたのではなく、減ってきた")

    ROWS = [
        ("炭酸水素ナトリウム", 1974, 1986, "ルーチン → 限定的",
         "換気で二酸化炭素は出せる", RED),
        ("ブレチリウム", 1974, 2000, "第一選択 → 削除",
         "供給停止と代替薬の登場", RED),
        ("高用量アドレナリン", 1992, 2000, "推奨 → 非推奨",
         "生存は増えなかった", RED),
        ("アトロピン", 1974, 2010, "定番 → 削除",
         "生存利益を示せなかった", RED),
        ("バソプレシン", 2000, 2015, "代替薬 → 削除",
         "上乗せ効果がなかった", RED),
        ("アミオダロン／リドカイン", 2000, 2018, "併存 → どちらでも",
         "直接比較で差がつかず", GREEN),
        ("アドレナリン 1 mg", 1974, 2025, "残った",
         "心拍再開は増やす", GREEN),
    ]
    X0, X1 = 400, W - 500
    TOP = 120

    def px(yr):
        return X0 + (X1 - X0) * (yr - 1970) / 58.0

    for yr in (1974, 1986, 2000, 2010, 2025):
        x = px(yr)
        cv.ax.plot([x, x], [TOP - 16, TOP + len(ROWS) * 100 - 30],
                   color="#e3e8ee", lw=1.2)
        cv.text(x, TOP - 30, str(yr), size=10.0, color=GREY)

    for i, (name, a, b, chg, why, color) in enumerate(ROWS):
        y = TOP + i * 100 + 22
        ns, nl = fitlines(cv, [name], 330, 11.0, weight="bold", floor=9.0)
        cv.block(50, y - LH(ns, 1.35) * len(nl) / 2, 330, nl, ns,
                 color=NAVY, weight="bold", ha="right",
                 lh=LH(ns, 1.35))
        xa, xb = px(a), px(b)
        cv.rect(xa, y - 11, max(xb - xa, 6), 22, fc="#dbe3ec")
        cv.rect(xb - 5, y - 15, 10, 30, fc=color)
        RW = W - 84 - (X1 + 24)
        s, cl = fitlines(cv, [chg], RW, 10.0, weight="bold", floor=8.4)
        cv.block(X1 + 24, y - 34, RW, cl, s, color=color, weight="bold",
                 ha="left", lh=LH(s, 1.35))
        s2, wl = fitlines(cv, [why], RW, 9.4, floor=8.0)
        cv.block(X1 + 24, y - 2, RW, wl, s2, color=GREY, ha="left",
                 lh=LH(s2, 1.35))

    msg(cv, 838, "半世紀で残ったのは、電気と圧迫と、一つの昇圧薬だけである。"
                 "アルゴリズムの歴史は、引き算の歴史でもある。")
    cv.save(P("f06_drugs.png"))


# ---------------------------------------------------------------- f07
def f07():
    """2025 年ガイドラインの数字"""
    cv = Canvas(W, 700)
    cap(cv, 44, "2025 年ガイドライン ── 760 の勧告が立っている土台")

    LEFT = [("Class 1（強い推奨）", 233, "31%", GREEN),
            ("Class 2a（中等度）", 217, "29%", BLUE),
            ("Class 2b（弱い）", 234, "31%", ORANGE),
            ("Class 3 : No Benefit", 55, "7%", GREY),
            ("Class 3 : Harm", 21, "3%", RED)]
    RIGHT = [("LOE A（複数の RCT）", 11, "1%", GREEN),
             ("LOE B-R（RCT）", 82, "11%", BLUE),
             ("LOE B-NR（非 RCT）", 176, "23%", BLUE),
             ("LOE C-LD（限られたデータ）", 288, "38%", ORANGE),
             ("LOE C-EO（専門家の意見）", 203, "27%", RED)]
    for k, (title, data) in enumerate((("推奨の強さ", LEFT),
                                       ("根拠の質", RIGHT))):
        x = 60 + k * 730
        cv.box(x, 100, 700, 58, fc=NAVY, ec=NAVY, lw=0, radius=8)
        cv.text(x + 350, 129, title, size=12.5, color="white", weight="bold")
        for i, (lab, n, pct, color) in enumerate(data):
            y = 180 + i * 72
            cv.text(x + 14, y + 18, lab, size=10.6, color=INK, ha="left")
            bw = 420 * n / 300.0
            cv.rect(x + 14, y + 34, max(bw, 4), 22, fc=color)
            cv.text(x + 14 + max(bw, 4) + 12, y + 45,
                    "%d（%s）" % (n, pct), size=10.4, color=GREY, ha="left")

    msg(cv, 566, "38% が「限られたデータ」に、27% が「専門家の意見」に基づいている。"
                 "複数の RCT に支えられた勧告は 760 のうち 11 にすぎない。")
    textbox(cv, 60, 632, W - 120,
            ["2020 年版は 491 勧告のうち LOE A が 6（1.2%）だった。"
             "2025 年版は 760 のうち 11（1.4%）。分母は増えたが、比率はほとんど動いていない。"],
            10.4, fc="white", ec=GREY, lw=1.6)
    cv.save(P("f07_2025_numbers.png"))


# ---------------------------------------------------------------- f08
def f08():
    """2025 年の主な変更"""
    cv = Canvas(W, 960)
    cap(cv, 44, "2025 年 ── 何が変わり、何が変わらなかったか")

    NEW = [("気道異物", "意識のある成人は背部叩打が先、次に腹部突き上げ"),
           ("血管路", "まず静脈路。取れなければ骨髄路（2024-25 年の 3 つの試験）"),
           ("機械的 CPR", "ルーチン使用は推奨しない（搬送中などは考慮可）"),
           ("Head-up CPR", "臨床試験の外では使わない"),
           ("多形性 VT", "常に不安定とみなし、ただちに除細動"),
           ("心房細動の同期通電", "初回から 200 J 以上"),
           ("体温管理", "32-37.5 ℃、総 36 時間以上"),
           ("用語", "rescue breaths を廃止。bystander より lay rescuer")]
    SAME = [("圧迫と除細動", "最も価値の高い行為であることは変わらない"),
            ("アドレナリン", "1 mg を 3-5 分ごと。非ショック適応では早く"),
            ("抗不整脈薬", "アミオダロンまたはリドカイン"),
            ("二重連続除細動", "有用性は未確立のまま（2b）"),
            ("2 分ごとのリズム確認", "変更なし")]

    L, CW = 60, 690
    cv.box(L, 100, CW, 58, fc=RED, ec=RED, lw=0, radius=8)
    cv.text(L + CW / 2, 129, "変わったところ", size=12.5, color="white",
            weight="bold")
    for i, (a, b) in enumerate(NEW):
        y = 176 + i * 84
        cv.box(L, y, CW, 74, fc="#fceeec", ec=RED, lw=1.6, radius=6)
        cv.text(L + 16, y + 20, a, size=10.8, color=RED, weight="bold",
                ha="left")
        s = cv.fit_size([b], CW - 36, 10.2)
        cv.text(L + 16, y + 52, b, size=s, color=INK, ha="left")

    L2 = L + CW + 30
    cv.box(L2, 100, CW, 58, fc=GREEN, ec=GREEN, lw=0, radius=8)
    cv.text(L2 + CW / 2, 129, "変わらなかったところ", size=12.5, color="white",
            weight="bold")
    for i, (a, b) in enumerate(SAME):
        y = 176 + i * 84
        cv.box(L2, y, CW, 74, fc="#eaf5ee", ec=GREEN, lw=1.6, radius=6)
        cv.text(L2 + 16, y + 20, a, size=10.8, color=GREEN, weight="bold",
                ha="left")
        s = cv.fit_size([b], CW - 36, 10.2)
        cv.text(L2 + 16, y + 52, b, size=s, color=INK, ha="left")

    textbox(cv, L2, 176 + 5 * 84 + 12, CW,
            ["救命の連鎖を 1 本に統合",
             "心停止後ケア・特殊状況・倫理を独立した章に",
             "高リスク患者の safety huddle を新たに推奨",
             "ECPR の体制（患者選択・カニュレーション・地域集約）を新設"],
            10.2, fc="white", ec=NAVY, title="構成そのものの変更",
            title_color=NAVY, lw=1.8)

    msg(cv, 176 + 8 * 84 + 14, "変更の多くは手技ではなく「順番」と「言葉」である。"
                 "教える側が書き換えるのは、手ではなく台本のほうである。")
    cv.save(P("f08_2025_changes.png"))


# ---------------------------------------------------------------- f09
def f09():
    """日本側の系譜"""
    cv = Canvas(W, 1040)
    cap(cv, 44, "日本側の系譜 ── 国際コンセンサスをどう受けてきたか")

    LANES = [
        ("ILCOR", [(2000, "国際ガイドライン"), (2005, "CoSTR"),
                   (2010, "CoSTR"), (2015, "連続評価へ"),
                   (2020, "CoSTR"), (2025, "CoSTR")], PURPLE),
        ("JRC", [(2006, "日本版ガイドライン"), (2011, "JRC 2010"),
                 (2016, "JRC 2015"), (2021, "JRC 2020"),
                 (2026, "JRC 2025")], BLUE),
        ("日本麻酔科学会", [(2014, "気道管理ガイドライン"),
                      (2017, "局所麻酔薬中毒"),
                      (2021, "術中心停止・安全な鎮静")], GREEN),
        ("集中治療・制度", [(2008, "医療安全全国共同行動"),
                      (2013, "RRS／IHCA レジストリ"),
                      (2017, "RRS 用語集"), (2022, "急性期充実体制加算"),
                      (2024, "RRS 運用指針"), (2027, "急性期総合体制加算")],
         ORANGE),
    ]
    X0, X1 = 250, W - 90
    span = 2032 - 1998

    def px(yr):
        return X0 + (X1 - X0) * (yr - 1998) / span

    for r, (name, items, color) in enumerate(LANES):
        y = 170 + r * 196
        cv.rect(X0, y + 22, X1 - X0, 4, fc="#e3e8ee")
        cv.text(230, y + 24, name, size=11.6, color=color, weight="bold",
                ha="right")
        for j, (yr, lab) in enumerate(items):
            x = px(yr)
            cv.rect(x - 2, y + 10, 4, 28, fc=color)
            yr_txt = "2026" if yr == 2027 else str(yr)
            dy = (-14, 56, -14, 56, -14, 56)[j % 6] if len(items) < 6                 else (-14, 56, -14, 84, -14, 56)[j]
            s = cv.fit_size([lab], 230, 9.6)
            if dy < 0:      # 線の上：上から 名称 → 年
                cv.text(x, y - 40, lab, size=s, color=INK)
                cv.text(x, y - 12, yr_txt, size=9.0, color=GREY)
            else:           # 線の下：上から 年 → 名称
                cv.text(x, y + dy, yr_txt, size=9.0, color=GREY)
                cv.text(x, y + dy + 28, lab, size=s, color=INK)

    msg(cv, 170 + 4 * 196 - 10, "JRC 蘇生ガイドライン 2025 は 2025 年 10 月 22 日にオンライン版が出て、"
                 "書籍は 2026 年 7 月 13 日に刊行された。")
    cv.save(P("f09_japan_lineage.png"))


# ---------------------------------------------------------------- f10
def f10():
    """周術期心停止の発生率（分母がちがう）"""
    cv = Canvas(W, 790)
    cap(cv, 44, "周術期心停止の発生率 ── 数字が合わないのは、数えているものが違うから")

    ROWS = [
        ("NAP7（英国 2021-22）", "3.0-3.5 / 1 万麻酔",
         "麻酔科医の管理下で胸骨圧迫 5 回以上または除細動", 3.25, RED),
        ("Cologne（独 2007-12）", "5.8 / 1 万麻酔",
         "術後 24 時間以内の心停止をインシデント報告から拾う", 5.8, ORANGE),
        ("NACOR（米 2010-13）", "5.6 / 1 万件",
         "術中と麻酔後回復室のみ。以後の入院期間は含まない", 5.6, ORANGE),
        ("SPOR（瑞 2013-22）", "2.4 / 1 万手術",
         "周術期と回復室。18 歳以上", 2.4, BLUE),
        ("JSA 偶発症例調査（2016）", "1.04 / 1 万麻酔",
         "麻酔科管理症例の心停止。施設からの年次報告", 1.04, GREEN),
        ("JIPAD（日 2015-23）", "手術室からの ICU 入室の 0.41%",
         "緊急 1.74%・待機 0.17%。分母が ICU 入室例に限られる", 0, PURPLE),
    ]
    L, TOP = 60, 110
    for i, (name, val, note, bar, color) in enumerate(ROWS):
        y = TOP + i * 96
        cv.box(L, y, W - 120, 84, fc="white", ec="#dde2e8", lw=1.4, radius=6)
        cv.text(L + 20, y + 26, name, size=11.4, color=NAVY, weight="bold",
                ha="left")
        s = cv.fit_size([note], 700, 9.8)
        cv.text(L + 20, y + 56, note, size=s, color=GREY, ha="left")
        if bar:
            cv.rect(L + 780, y + 34, 380 * bar / 6.5, 22, fc=color)
        cv.text(W - 80, y + 44, val, size=11.6, color=color, weight="bold",
                ha="right")

    msg(cv, 690, "分子（何を心停止と呼ぶか）も分母（誰を数えるか）も、"
                 "報告ごとに違う。比べるときは定義から読む。")
    cv.save(P("f10_incidence.png"))


# ---------------------------------------------------------------- f11
def f11():
    """手術室の有利・不利"""
    cv = Canvas(W, 900)
    cap(cv, 44, "手術室の心停止は、有利な条件と不利な条件を同時に持っている")

    GOOD = ["バイタルが連続してモニターされている",
            "気道がすでに確保されている",
            "静脈路が入っている",
            "予兆の段階から目撃されている",
            "全身麻酔中は酸素消費量が下がっている",
            "医師と看護師がその場にいる"]
    BAD = ["覆布に覆われ、体表に触れない",
           "仰臥位とは限らない（腹臥位・側臥位・砕石位）",
           "術野が開いている／器械が体に固定されている",
           "意識も呼吸も人工的なので、いつもの手がかりがない",
           "麻酔科医が原因究明に没頭し、圧迫の指示が遅れる",
           "「自分で解決できる」という判断が先に立つ"]
    L, CW = 60, 690
    h1 = textbox(cv, L, 110, CW, GOOD, 10.6, fc="#eaf5ee", ec=GREEN,
                 title="有利な条件", title_color=GREEN, lw=2.2, lh_scale=2.0)
    h2 = textbox(cv, L + CW + 30, 110, CW, BAD, 10.6, fc="#fceeec", ec=RED,
                 title="不利な条件", title_color=RED, lw=2.2, lh_scale=2.0)
    by = 110 + max(h1, h2) + 34

    cv.box(60, by, W - 120, 150, fc="#e8edf5", ec=NAVY, lw=2.0, radius=8)
    cv.text(W / 2, by + 36, "だから、術中心停止の生存率は他の心停止より高い",
            size=13.0, color=NAVY, weight="bold")
    cv.text(W / 2, by + 80, "院内心停止全体の生存退院が 2 割前後なのに対し、"
                            "術中心停止は 3 割から 8 割と報告されている",
            size=11.0, color=INK)
    cv.text(W / 2, by + 118, "── 有利さを使い切れるかどうかが、そのまま差になる",
            size=11.0, color=TEAL, weight="bold")

    msg(cv, by + 176,
        "胸骨圧迫が遅れる理由の多くは、知識ではなく役割の問題である。")
    cv.save(P("f11_or_context.png"))


# ---------------------------------------------------------------- f12
def f12():
    """原因の系統樹"""
    cv = Canvas(W, 900)
    cap(cv, 44, "術中心停止に至る二つの道")

    cv.box(560, 100, 400, 70, fc=NAVY, ec=NAVY, lw=0, radius=8)
    cv.text(760, 135, "循環虚脱・心停止", size=14.0, color="white",
            weight="bold")

    LEFT = ["手術操作による迷走神経刺激",
            "薬物の過量投与（麻酔薬・β 遮断薬）",
            "心臓交感神経の遮断（T1-T4）",
            "房室ブロック",
            "低酸素血症の終末（先に頻脈、直前に徐脈）"]
    RIGHT = ["大量出血による循環血液量減少",
             "低酸素血症",
             "アナフィラキシー",
             "悪性高熱症",
             "心室性・上室性不整脈 → VF／頻脈性 PEA"]
    h1 = textbox(cv, 60, 250, 690, LEFT, 10.6, fc="#eaf1f8", ec=BLUE,
                 title="徐脈から入る道", title_color=BLUE, lw=2.2,
                 lh_scale=2.1)
    h2 = textbox(cv, 780, 250, 690, RIGHT, 10.6, fc="#fdf3e3", ec=ORANGE,
                 title="頻脈から入る道", title_color=ORANGE, lw=2.2,
                 lh_scale=2.1)
    by = 250 + max(h1, h2) + 36
    cv.arrow((560, 135), (405, 246), color=BLUE, lw=2.4, head=13)
    cv.arrow((960, 135), (1125, 246), color=ORANGE, lw=2.4, head=13)

    BOT = ["困難気道・窒息などの気道の喪失", "人工呼吸器の異常",
           "重症喘息・もともとの低肺機能", "術前からの低心機能の悪化",
           "心筋梗塞", "心タンポナーデ", "緊張性気胸",
           "脊髄くも膜下麻酔後の高位神経ブロック", "局所麻酔薬中毒",
           "アナフィラキシー", "肺塞栓症", "悪性高熱症"]
    per = 3
    nrow = (len(BOT) + per - 1) // per
    bh = 56 + nrow * 30
    cv.box(60, by, W - 120, bh, fc="white", ec=GREY, lw=1.8, radius=8)
    cv.text(W / 2, by + 28, "術中に想定しておくべき原因", size=12.0, color=NAVY,
            weight="bold")
    for i, t in enumerate(BOT):
        r, c = i // per, i % per
        sz = cv.fit_size(["・" + t], 430, 10.0, min_size=8.4)
        cv.text(96 + c * 460, by + 62 + r * 30, "・" + t, size=sz, color=INK,
                ha="left")
    cv.save(P("f12_cause_tree.png"))


# ---------------------------------------------------------------- f13
def f13():
    """JSA プラクティカルガイドの地図"""
    cv = Canvas(W, 790)
    cap(cv, 44, "日本麻酔科学会「術中心停止に対するプラクティカルガイド」（2021）の地図")

    cv.box(60, 100, W - 120, 74, fc=NAVY, ec=NAVY, lw=0, radius=8)
    cv.text(W / 2, 137, "1　総論 ── 認識・初期対応アルゴリズム・ACLS への接続",
            size=13.0, color="white", weight="bold")

    ITEMS = [("2", "気道管理", BLUE), ("3", "出血による心停止", RED),
             ("4", "右心不全／肺高血圧・肺塞栓症", PURPLE),
             ("5", "心原性ショックによる左心不全", PURPLE),
             ("6", "局所麻酔薬中毒", ORANGE),
             ("7", "悪性高熱症", ORANGE),
             ("8", "緊張性気胸と心タンポナーデ", RED),
             ("9", "アナフィラキシー", ORANGE),
             ("10", "仰臥位以外での心停止", GREEN),
             ("11", "母体の心停止", GREEN),
             ("12", "小児周術期蘇生の特殊性", GREEN)]
    CW, GAP, L = 344, 24, 60
    for i, (no, name, color) in enumerate(ITEMS):
        r, c = i // 4, i % 4
        x = L + c * (CW + GAP)
        y = 214 + r * 116
        if i == 8:
            x = L + (CW + GAP) / 2
        if i >= 8:
            x = L + (c) * (CW + GAP) + (CW + GAP) / 2
        cv.box(x, y, CW, 92, fc="white", ec=color, lw=2.0, radius=8)
        cv.box(x, y, 60, 92, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + 30, y + 46, no, size=15.0, color="white", weight="bold")
        s = cv.fit_size([name], CW - 90, 11.2, weight="bold")
        cv.text(x + 60 + (CW - 60) / 2, y + 46, name, size=s, color=color,
                weight="bold")

    msg(cv, 596, "総論が「順序」を、各論が「原因ごとの分岐」を受け持つ。"
                 "手術室のアルゴリズムは、原因で枝分かれする点が院外と違う。")
    textbox(cv, 60, 664, W - 120,
            ["制定 2021 年 2 月 26 日。安全委員会「術中の心肺蘇生ガイドライン作成 WG」"
             "（WG 長：髙橋伸二）。",
             "本ガイドに沿わない診療を否定するものではなく、"
             "法的責任の判断に用いることを目的としない、と明記されている。"],
            10.2, fc="white", ec=GREY, lw=1.6)
    cv.save(P("f13_jsa_map.png"))


# ---------------------------------------------------------------- f14
def f14():
    """アドレナリンのタイミング"""
    cv = Canvas(W, 900)
    cap(cv, 44, "アドレナリンは「早ければ早いほどよい」ではない")

    L, CW = 60, 690
    TOPS = [(["心停止の認識と同時に投与する。",
              "PEA・心静止では 1 サイクル目から。",
              "早期投与と心拍再開の関連は複数の観察研究で一貫している。"],
             "#eaf5ee", GREEN, "ショック非適応（PEA・心静止）"),
            (["除細動と質の高い圧迫を優先する。",
              "初回ショックの 2 分以内に入れると、かえって心拍再開率が下がる。",
              "院内心停止では、初回除細動前の投与率が高い病院ほど生存が約 10% 低い。"],
             "#fceeec", RED, "ショック適応（VF・無脈性 VT）")]
    def _w(ls, w, s):
        out = []
        for l in ls:
            out += cv.wrap(l, w, s)
        return out
    hs = []
    for k, (ls, fc, ec, ttl) in enumerate(TOPS):
        hs.append(textbox(cv, L + k * (CW + 30), 110, CW, _w(ls, CW - 40, 11.0),
                          11.0, fc=fc, ec=ec, title=ttl, title_color=ec, lw=2.2,
                          min_h=230))
    by = 110 + max(hs) + 30
    LINES = ["1 mg を 3-5 分ごと。実務上は「2 サイクルごと」と読み替えてよい。",
             "高用量アドレナリンが標準用量に勝るという証拠はない。"
             "標準より短い間隔で繰り返すことは有害の可能性がある。",
             "PARAMEDIC2 の事後解析では、無脈がおよそ 20 分続いた時点で"
             "プラセボとの差が消える。",
             "静注した昇圧薬は胸骨圧迫なしには効かない。投与後は生理食塩液 20 mL で後押しする。"]
    rows = []
    for ln in LINES:
        ws = cv.wrap("・" + ln, W - 220, 10.6)
        rows += [ws[0]] + ["　" + x for x in ws[1:]]
    lh = LH(10.6, 1.6)
    bh = 70 + lh * len(rows) + 16
    cv.box(60, by, W - 120, bh, fc="white", ec=NAVY, lw=1.8, radius=8)
    cv.text(W / 2, by + 34, "投与間隔と限界", size=12.5, color=NAVY, weight="bold")
    for i, ln in enumerate(rows):
        cv.text(110, by + 70 + lh * (i + 0.5), ln, size=10.6, color=INK, ha="left")

    msg(cv, by + bh + 22, "「何分後に何 mg」ではなく、"
                 "「いま一番価値の高い行為を邪魔していないか」で決める。")
    cv.save(P("f14_epinephrine_timing.png"))


# ---------------------------------------------------------------- f15
def f15():
    """CPR の質を測る"""
    cv = Canvas(W, 800)
    cap(cv, 44, "手術室にはすでに「質を測る道具」が付いている")

    ITEMS = [
        ("EtCO2", ["圧迫の質と心拍再開を映す",
                   "CPR 中は 20 mmHg 超を目安に",
                   "突然の低下は肺塞栓・回路異常"], TEAL, "#e4f2f4"),
        ("観血的動脈圧", ["拡張期圧が冠灌流圧の代理",
                    "波形の平坦化が最初の手がかり",
                    "交代の時期を数字で決められる"], BLUE, "#eaf1f8"),
        ("心エコー（経食道・経胸壁）", ["タンポナーデ・右心負荷を見る",
                             "圧迫を止めずに使えるか先に決める",
                             "所見が出るまで蘇生は止めない"], PURPLE,
         "#f1ecf8"),
    ]
    CW, GAP, L = 448, 28, 60
    hmax = 0
    for i, (head, lines, color, fc) in enumerate(ITEMS):
        hmax = max(hmax, card(cv, L + i * (CW + GAP), 110, CW, head, lines,
                              color, fc, body_size=10.4, lh=1.95))
    ty = 110 + hmax + 30
    th = textbox(cv, 60, ty, W - 120,
            ["院外心停止の研究では、リアルタイムの視聴覚フィードバック装置が"
             "圧迫の質を改善する（2025 年版でも推奨）。",
             "手術室では、装置を買わなくても EtCO2 と動脈圧がその役を果たす。"
             "問題は装置の有無ではなく、誰がその数字を読み上げるかである。"],
            10.8, fc="white", ec=NAVY, title="装置よりも役割",
            title_color=NAVY, lw=1.8)

    msg(cv, ty + th + 30,
        "測っていない蘇生は、うまくいったかどうかを後から語れない。")
    cv.save(P("f15_quality_monitors.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12,
               f13, f14, f15):
        fn()
        print("ok", fn.__name__)
