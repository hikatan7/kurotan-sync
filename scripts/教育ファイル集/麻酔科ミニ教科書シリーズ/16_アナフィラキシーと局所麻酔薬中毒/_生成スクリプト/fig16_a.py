# -*- coding: utf-8 -*-
"""第16巻 アナフィラキシーと局所麻酔薬中毒 図版 f01〜f10"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP
LAST_C, ANA_C = "#7b52a8", "#c0392b"


def P(n):
    return os.path.join(OUT, n)


def two_col(cv, W, PTOP, cols, head_sz=12.5, body_sz=10.2, gapx=50, L=64):
    """左右2枚のパネル。cols = [(見出し, 色, 淡色, [行...]), ...]。返り値は下端"""
    PW = (W - L * 2 - gapx) / 2.0
    HH = 54
    BTOP = PTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in cols for l in c[3]], PW - 56,
                         body_sz), body_sz)
    nl = max(sum(len(cv.wrap(l, PW - 62, sz)) for l in c[3]) for c in cols)
    BH = 30 + LH(sz, 1.85) * (nl - 1) + LH(sz, 1.0) * 0.5 + 22
    for i, (head, col, fc, lines) in enumerate(cols):
        px = L + i * (PW + gapx)
        cv.box(px, PTOP, PW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(px + PW / 2, PTOP + HH / 2, head, size=head_sz, color="white",
                weight="bold")
        cv.box(px, BTOP, PW, BH, fc=fc, ec=col, lw=1.8, radius=8)
        k = 0
        for ln in lines:
            for j, sub in enumerate(cv.wrap(ln, PW - 62, sz)):
                cv.text(px + 26, BTOP + 30 + LH(sz, 1.85) * k,
                        ("・" if j == 0 else "　") + sub, size=sz, color=INK,
                        ha="left")
                k += 1
    return BTOP + BH


def note(cv, W, y, text, size=9.8):
    for i, ln in enumerate(cv.wrap(text, W - 150, size)):
        cv.text(W / 2, y + LH(size, 1.45) * i, ln, size=size, color="#5d6875")


def banner(cv, W, y, msg, col="#c0392b", fc="#fbeeee", tc="#9c2b26", L=52):
    sz = cv.fit_size([msg], W - L * 2 - 60, 12, weight="bold")
    h = 30 + LH(sz, 1.5)
    cv.box(L, y, W - L * 2, h, fc=fc, ec=col, lw=2.0, radius=8)
    cv.text(W / 2, y + h / 2, msg, size=sz, color=tc, weight="bold")
    return y + h


# ---------------------------------------------------------------- f01
def f01():
    W, H = 1520, 660
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "見た目が似ていて、機序も治療も違う二つ",
             size=12.5, ha="center")
    y = two_col(cv, W, 90, [
        ("局所麻酔薬中毒（LAST）", LAST_C, "#f3eefa",
         ["機序　Na チャネル遮断の過剰",
          "標的　中枢神経系 → 心血管系",
          "発症　曝露後 数分〜数十分（遅発もある）",
          "初期　舌のしびれ、耳鳴、興奮、痙攣",
          "治療　痙攣の抑制と脂肪乳剤"]),
        ("アナフィラキシー", ANA_C, "#fbeeee",
         ["機序　肥満細胞が関与する I 型アレルギー反応",
          "標的　皮膚・粘膜、気道、循環、消化管",
          "発症　曝露後 数分〜30分",
          "初期　紅潮、浮腫、喘鳴、血圧低下",
          "治療　アドレナリンと大量輸液"]),
    ])
    y = banner(cv, W, y + 26,
               "どちらも「急に血圧が下がった」で始まる。分けるのは経過と随伴所見である")
    note(cv, W, y + 32,
         "※ 麻酔下では、患者は舌のしびれも耳鳴も訴えられない。"
         "LAST の警告症状が丸ごと失われるため、循環と心電図の変化が最初の徴候になりうる。")
    cv.save(P("f01_two_entities.png"))


# ---------------------------------------------------------------- f02
def f02():
    W, H = 1520, 660
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "局所麻酔薬中毒 —— 効果の延長線上にある",
             size=12.5, ha="center")
    STEPS = [("末梢神経の Na チャネルを遮断する", "#1f6b47", "目的とする作用"),
             ("血中濃度が上がる", "#2e6da4", "吸収・血管内注入・過量"),
             ("中枢神経系の Na チャネルまで遮断する", "#b8760f",
              "感受性が高いので先に出る"),
             ("心血管系の Na チャネルまで遮断する", "#c0392b",
              "心筋の直接抑制、伝導抑制、回帰性不整脈"),
             ("心停止", "#8f2b28", "ACLS＋脂肪乳剤。通常の蘇生と違う点がある")]
    L, R = 60, W - 60
    TOP, SH, SG = 96, 74, 20
    NAMEW = R - L - 420
    ssz = min(cv.fit_size([s[0] for s in STEPS], NAMEW - 40, 11.2), 11.2)
    nsz = min(cv.fit_size([s[2] for s in STEPS], 380, 9.8), 9.8)
    for i, (t, col, sub) in enumerate(STEPS):
        y = TOP + i * (SH + SG)
        cv.box(L, y, NAMEW, SH, fc="white", ec=col, lw=1.9, radius=8)
        ax.add_patch(Rectangle((L, y + 10), 8, SH - 20, facecolor=col,
                               edgecolor="none", zorder=4))
        cv.text(L + 28, y + SH / 2, t, size=ssz, color=col, weight="bold",
                ha="left")
        cv.text(L + NAMEW + 26, y + SH / 2, sub, size=nsz, color="#5d6875",
                ha="left")
        if i < len(STEPS) - 1:
            cv.arrow((L + NAMEW / 2, y + SH + 2),
                     (L + NAMEW / 2, y + SH + SG - 2),
                     color="#8d97a3", lw=2.2, head=9)
    note(cv, W, TOP + 5 * (SH + SG) + 20,
         "※ 中枢神経症状が心血管症状より先に出るのが典型だが、"
         "血管内へ急速に入った場合や、ブピバカインのような心毒性の強い薬では"
         "循環虚脱が先に来ることがある。")
    cv.save(P("f02_last_mechanism.png"))


# ---------------------------------------------------------------- f03
def f03():
    W, H = 1520, 660
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "血中濃度が上がるにつれて、何が起きるか（リドカインの目安）",
             size=12.5, ha="center")
    ROWS = [
        ("〜5 μg/mL", "#1f6b47", "治療域", "抗不整脈作用。鎮痛が得られる"),
        ("5〜10", "#b8760f", "前駆症状",
         "口周囲・舌のしびれ、金属味、耳鳴、めまい、多弁、視覚異常"),
        ("10〜15", "#d2762b", "興奮期", "振戦、筋攣縮、意識変容、全身痙攣"),
        ("15〜25", "#c0392b", "抑制期", "意識消失、呼吸抑制・停止"),
        ("25 以上", "#8f2b28", "心血管虚脱",
         "血圧低下、徐脈、房室ブロック、心室性不整脈、心停止"),
    ]
    L, R = 56, W - 56
    CONC_SZ = 11.0
    CONCW = max(cv.measure(r[0], CONC_SZ, weight="bold")[0] for r in ROWS) + 46
    TAG_SZ = 10.2
    TAGW = max(cv.measure(r[2], TAG_SZ, weight="bold")[0] for r in ROWS) + 34
    TOP, GAP = 96, 14
    bsz = min(cv.fit_size([r[3] for r in ROWS],
                          R - L - CONCW - TAGW - 90, 10.0), 10.0)
    nl = max(len(cv.wrap(r[3], R - L - CONCW - TAGW - 90, bsz)) for r in ROWS)
    RH = 30 + LH(bsz, 1.4) * (nl - 1) + LH(bsz, 1.0) * 0.5 + 26
    for i, (conc, col, tag, body) in enumerate(ROWS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L, y, CONCW, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(L + CONCW / 2, y + RH / 2, conc, size=CONC_SZ, color="white",
                weight="bold")
        cv.box(L + CONCW + 20, y + (RH - 44) / 2, TAGW, 44, fc="#f2f5f8",
               ec=col, lw=1.4, radius=6)
        cv.text(L + CONCW + 20 + TAGW / 2, y + RH / 2, tag, size=TAG_SZ,
                color=col, weight="bold")
        for j, sub in enumerate(cv.wrap(body, R - L - CONCW - TAGW - 90, bsz)):
            cv.text(L + CONCW + TAGW + 46,
                    y + RH / 2 - LH(bsz, 1.4) * (nl - 1) / 2
                    + LH(bsz, 1.4) * j, sub, size=bsz, color=INK, ha="left")
    note(cv, W, TOP + 5 * (RH + GAP) + 18,
         "※ 濃度の区切りは目安であり、個体差が大きい。"
         "全身麻酔・鎮静下では前駆症状を訴えられないため、この階段の上半分が見えない。"
         "薬剤によっても閾値は変わる（ブピバカインは低い濃度で心毒性が出る）。")
    cv.save(P("f03_concentration.png"))


# ---------------------------------------------------------------- f04
def f04():
    W, H = 1520, 790
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "同じ量でも、どこに入れるかで血中濃度は変わる",
             size=12.5, ha="center")
    ORDER = [("静脈内（誤注入）", 1.00, "#8f2b28"),
             ("肋間神経", 0.80, "#c0392b"),
             ("硬膜外", 0.62, "#d2762b"),
             ("腕神経叢", 0.46, "#b8760f"),
             ("坐骨神経・大腿神経", 0.32, "#7b52a8"),
             ("皮下投与", 0.18, "#2e6da4")]
    L, R = 60, W - 60
    LABW = 340
    TOP, BH_, GAP = 100, 56, 16
    barx0 = L + LABW + 24
    barw = R - barx0 - 40
    lsz = min(cv.fit_size([o[0] for o in ORDER], LABW - 20, 10.6), 10.6)
    for i, (lab, v, col) in enumerate(ORDER):
        y = TOP + i * (BH_ + GAP)
        cv.text(L + LABW, y + BH_ / 2, lab, size=lsz, color=INK, ha="right")
        ax.add_patch(Rectangle((barx0, y + 10), barw * v, BH_ - 20,
                               facecolor=col, edgecolor="none", zorder=4))
    cv.text(barx0, TOP + 6 * (BH_ + GAP) + 6, "血中濃度が上がりやすい　→",
            size=10.0, color="#5d6875", ha="left")
    y = banner(cv, W, TOP + 6 * (BH_ + GAP) + 34,
               "血流が豊富で、吸収面積が広い部位ほど速く上がる。炎症部位はとくに注意する",
               col="#b8760f", fc="#fdf1e0", tc="#8a5a0f")
    note(cv, W, y + 30,
         "※ 相対的な順序を示す模式図であり、目盛は濃度の実測値ではない。"
         "発生頻度は手技によって大きく異なり、1/10,000〜1/500 と報告されている。")
    cv.save(P("f04_site_absorption.png"))


# ---------------------------------------------------------------- f05
def f05():
    W, H = 1520, 700
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "起こしやすい背景 —— 遊離型が増える、あるいは代謝が落ちる",
             size=12.5, ha="center")
    COLS = [
        ("代謝・排泄が落ちる", "#2e6da4",
         ["高齢者", "新生児", "肝不全", "腎不全", "心不全（肝血流の低下）"]),
        ("遊離型が増える", "#b8760f",
         ["低蛋白血症", "アシドーシス", "低酸素", "脱水", "妊婦"]),
        ("効きが悪く、過量になりやすい", "#c0392b",
         ["炎症・発熱", "敗血症", "悪性腫瘍", "心筋梗塞後",
          "α1-酸性糖蛋白の増加"]),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 92, 90
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in COLS for l in c[2]], CW - 46, 10.2),
             10.2)
    BH = 30 + LH(sz, 1.9) * 4 + LH(sz, 1.0) * 0.5 + 22
    for i, (head, col, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        for j, sub in enumerate(cv.wrap(head, CW - 30, 11.2)):
            cv.text(x + CW / 2, HTOP + HH / 2 + (j - 0.5 *
                    (len(cv.wrap(head, CW - 30, 11.2)) - 1)) * LH(11.2, 1.3),
                    sub, size=11.2, color="white", weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            cv.text(x + 26, BTOP + 30 + LH(sz, 1.9) * j, "・" + ln, size=sz,
                    color=INK, ha="left")
    y = banner(cv, W, BTOP + BH + 26,
               "急性相蛋白が増えると遊離型が減って効きが悪くなり、"
               "追加投与を招いて結果的に中毒になる",
               col="#b8760f", fc="#fdf1e0", tc="#8a5a0f")
    note(cv, W, y + 30,
         "※ 「効かないから足す」という判断が、最も多い中毒の入り口である。"
         "効かない理由を先に考える。")
    cv.save(P("f05_background.png"))


# ---------------------------------------------------------------- f06
def f06():
    W, H = 1520, 890
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "局所麻酔薬中毒を疑ったら —— 順序が決まっている",
             size=12.5, ha="center")
    STEPS = [
        ("① 止める", "#c0392b",
         ["局所麻酔薬の投与を直ちに中止する", "応援を呼ぶ（人手が要る）"]),
        ("② 気道と酸素", "#b8760f",
         ["100% 酸素を投与し、換気を確保する",
          "低酸素とアシドーシスは中毒を悪化させる"]),
        ("③ 痙攣を止める", "#7b52a8",
         ["ベンゾジアゼピンを第一選択とする",
          "プロポフォールは抗痙攣目的では使わない（心抑制）"]),
        ("④ 脂肪乳剤", "#2e6da4",
         ["20% 脂肪乳剤を投与する（施設の手順と用量に従う）",
          "心血管症状があれば早期に開始する"]),
        ("⑤ 循環", "#1f6b47",
         ["心停止なら ACLS。ただし通常と違う点がある（図6-2）",
          "PCPS／ECMO が使える施設では並行して考慮する"]),
    ]
    L, R = 56, W - 56
    TAG_SZ = 11.0
    TAGW = max(cv.measure(s[0], TAG_SZ, weight="bold")[0] for s in STEPS) + 40
    TOP, GAP = 96, 14
    bsz = min(cv.fit_size([l for s in STEPS for l in s[2]],
                          R - L - TAGW - 90, 10.0), 10.0)
    RH = 30 + LH(bsz, 1.7) + LH(bsz, 1.0) * 0.5 + 26
    for i, (head, col, lines) in enumerate(STEPS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L + 12, y + 14, TAGW, RH - 28, fc=col, ec=col, lw=0, radius=6)
        cv.text(L + 12 + TAGW / 2, y + RH / 2, head, size=TAG_SZ,
                color="white", weight="bold")
        for j, ln in enumerate(lines):
            cv.text(L + TAGW + 44,
                    y + RH / 2 - LH(bsz, 1.7) * 0.5 + LH(bsz, 1.7) * j,
                    "・" + ln, size=bsz, color=INK, ha="left")
        if i < len(STEPS) - 1:
            cv.arrow((L + 12 + TAGW / 2, y + RH + 1),
                     (L + 12 + TAGW / 2, y + RH + GAP - 1),
                     color="#8d97a3", lw=2.0, head=8)
    note(cv, W, TOP + 5 * (RH + GAP) + 22,
         "※ 日本麻酔科学会「局所麻酔薬中毒への対応プラクティカルガイド」（2017）の"
         "枠組みに沿っている。用量と手順は施設の指示に従うこと。")
    cv.save(P("f06_last_response.png"))


# ---------------------------------------------------------------- f07
def f07():
    W, H = 1520, 640
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "局所麻酔薬中毒の ACLS —— 通常の蘇生と違うところ",
             size=12.5, ha="center")
    y = two_col(cv, W, 90, [
        ("使わない・減らす", "#c0392b", "#fbeeee",
         ["アドレナリンは少量から（1 μg/kg 未満が推奨されている）",
          "バソプレシンは原則使わない（予後不良・肺出血の報告）",
          "β遮断薬、Ca 拮抗薬は原則使わない",
          "Ⅰ群抗不整脈薬（リドカインなど）は使わない",
          "プロポフォールを抗痙攣薬として使わない"]),
        ("使う・考慮する", "#1f6b47", "#eaf4ee",
         ["ベンゾジアゼピンで痙攣を止める",
          "20% 脂肪乳剤を早期に投与する",
          "不整脈にはアミオダロンを用いる",
          "100% 酸素と確実な換気",
          "PCPS／ECMO を並行して考慮する"]),
    ], head_sz=12)
    y = banner(cv, W, y + 24,
               "通常量（1 mg）のアドレナリンは、蘇生後の不整脈リスクを上げると報告されている")
    note(cv, W, y + 30,
         "※ β遮断薬・Ca 拮抗薬の要否は循環器へコンサルトする。"
         "蘇生が長引くことがあるため、脂肪乳剤の追加投与と ECMO の適応を早い段階で相談する。")
    cv.save(P("f07_last_acls.png"))


# ---------------------------------------------------------------- f08
def f08():
    W, H = 1520, 620
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "脂肪乳剤 —— 何をしているのか、なぜ早いほうがよいのか",
             size=12.5, ha="center")
    COLS = [
        ("何をしているか", "#2e6da4",
         ["血中に脂質の相をつくり、脂溶性の局所麻酔薬を取り込む（lipid sink）",
          "心筋のエネルギー基質として働く可能性も指摘されている",
          "作用点から薬を引き剥がす、という発想の治療である"]),
        ("いつ始めるか", "#1f6b47",
         ["心血管症状（不整脈、血圧低下）が出た時点で開始する",
          "痙攣だけでも、重篤化が予想されるなら開始してよい",
          "「効かなかったら」ではなく「疑った時点で」"]),
        ("注意すること", "#b8760f",
         ["用量の上限がある（施設の手順に従う）",
          "肺障害、高脂血症、膵炎、血液濾過の目詰まりの報告がある",
          "投与後の検査値（脂質、アミラーゼ）が乱れる"]),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 92, 52
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in COLS for l in c[2]], CW - 46, 9.9),
             9.9)
    nl = max(sum(len(cv.wrap(l, CW - 56, sz)) for l in c[2]) for c in COLS)
    BH = 30 + LH(sz, 1.6) * (nl - 1) + LH(sz, 1.0) * 0.5 + 22
    for i, (head, col, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.4, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        k = 0
        for ln in lines:
            for j, sub in enumerate(cv.wrap(ln, CW - 56, sz)):
                cv.text(x + 24, BTOP + 30 + LH(sz, 1.6) * k,
                        ("・" if j == 0 else "　") + sub, size=sz, color=INK,
                        ha="left")
                k += 1
    note(cv, W, BTOP + BH + 30,
         "※ 1998年に解毒効果が報告され、2006年に人での臨床応用が報告された。"
         "2010年ごろから各国のガイドラインに掲載されている。"
         "具体的な用量は製剤と施設の手順に従うこと。")
    cv.save(P("f08_lipid.png"))


# ---------------------------------------------------------------- f09
def f09():
    W, H = 1520, 730
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "予防の7か条 —— 起きてからでは選択肢が少ない",
             size=12.5, ha="center")
    ITEMS = [("① 背景を把握する", "#2e6da4", "高齢、肝腎不全、低蛋白、炎症、妊娠"),
             ("② 総投与量を減らす", "#2e6da4", "必要最小限。濃度を先に薄める"),
             ("③ 少量分割投与", "#1f6b47", "一気に入れない。間を置いて反応を見る"),
             ("④ 薬を選ぶ", "#1f6b47", "中毒リスクの低い薬を選ぶ"),
             ("⑤ 吸引テスト", "#b8760f", "穿刺後に必ず吸引する"),
             ("⑥ 血管内投与を検知する", "#b8760f",
              "テストドーズ、アドレナリン添加"),
             ("⑦ 超音波で確認する", "#c0392b", "穿刺針とカテーテルの位置を見る")]
    L, R = 48, W - 48
    GAPX, GAPY = 20, 14
    CW = (R - L - GAPX) / 2.0
    TOP = 92
    hsz = 10.8
    bsz = min(cv.fit_size([i[2] for i in ITEMS], CW - 44, 9.8), 9.8)
    CH = 38 + LH(bsz, 1.4) + 24
    for k, (head, col, body) in enumerate(ITEMS):
        r, c = divmod(k, 2)
        x = L + c * (CW + GAPX)
        y = TOP + r * (CH + GAPY)
        cv.box(x, y, CW, CH, fc="white", ec=col, lw=1.7, radius=7)
        cv.ax.add_patch(Rectangle((x, y + 8), 7, CH - 16, facecolor=col,
                                  edgecolor="none", zorder=4))
        cv.text(x + 26, y + 30, head, size=hsz, color=col, weight="bold",
                ha="left")
        cv.text(x + 26, y + 30 + LH(bsz, 1.85), body, size=bsz, color=INK,
                ha="left")
    y = banner(cv, W, TOP + 4 * (CH + GAPY) + 20,
               "局所麻酔薬中毒が起きること自体は過失ではない。"
               "問われるのは説明・投与量・投与方法・体制・対処である")
    note(cv, W, y + 30,
         "※ 日本麻酔科学会「局所麻酔薬中毒への対応プラクティカルガイド」（2017）による。")
    cv.save(P("f09_prevention7.png"))


# ---------------------------------------------------------------- f10
def f10():
    W, H = 1520, 560
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "処置を始める前に整えておくもの",
             size=12.5, ha="center")
    COLS = [
        ("人と体制", "#2e6da4",
         ["複数の医療スタッフ", "静脈路の確保",
          "全身痙攣の抑制には大人数が要る",
          "召集時に「局所麻酔薬中毒の可能性」と言う"]),
        ("モニタと環境", "#1f6b47",
         ["心電図、パルスオキシメータ", "5分間隔の血圧測定",
          "酸素投与ができること", "緊急カートが使えること"]),
        ("薬", "#c0392b",
         ["ベンゾジアゼピン", "20% 脂肪乳剤",
          "アドレナリン（少量から使える希釈）", "アミオダロン"]),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 92, 52
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in COLS for l in c[2]], CW - 46, 10.0),
             10.0)
    nl = max(sum(len(cv.wrap(l, CW - 56, sz)) for l in c[2]) for c in COLS)
    BH = 30 + LH(sz, 1.85) * (nl - 1) + LH(sz, 1.0) * 0.5 + 22
    for i, (head, col, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.4, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        k = 0
        for ln in lines:
            for j, sub in enumerate(cv.wrap(ln, CW - 56, sz)):
                cv.text(x + 24, BTOP + 30 + LH(sz, 1.85) * k,
                        ("・" if j == 0 else "　") + sub, size=sz, color=INK,
                        ha="left")
                k += 1
    note(cv, W, BTOP + BH + 30,
         "※ 酸素投与 → 痙攣の抑制 → 気道・循環の管理 → 必要なら ACLS、の順に進む。"
         "全身痙攣や不整脈が出れば PCPS も同時に考慮する。")
    cv.save(P("f10_preparation.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10):
        fn()
        print("ok", fn.__name__)
