# -*- coding: utf-8 -*-
"""第15巻 手術体位と末梢神経障害 図版 f01〜f07"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, Ellipse
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f01
def f01():
    W, H = 1520, 640
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "体位関連神経障害は「重なり」で生じる —— 一つの原因を探さない",
             size=12.5, ha="center")
    COLS = [
        ("患者因子", "#2e6da4",
         ["糖尿病・既存ニューロパチー", "末梢血管疾患", "体格の両極（低BMI／肥満）",
          "喫煙・慢性多量飲酒", "可動域制限"]),
        ("術式・体位因子", "#b8760f",
         ["圧迫（骨突出部・支持具）", "牽引（外転・回旋・過屈曲）",
          "台の角度・気腹", "手術時間", "ドレープ下でのずれ"]),
        ("循環・全身因子", "#1f6b47",
         ["低血圧", "低体温", "出血・貧血", "浮腫", "低酸素"]),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 92, 50
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in COLS for l in c[2]], CW - 46, 9.8),
             9.8)
    BH = 28 + LH(sz, 1.8) * 4 + LH(sz, 1.0) * 0.5 + 18
    for i, (head, col, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.4, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            cv.text(x + 24, BTOP + 28 + LH(sz, 1.8) * j, "・" + ln, size=sz,
                    color=INK, ha="left")
        cv.arrow((x + CW / 2, BTOP + BH + 2), (x + CW / 2, BTOP + BH + 34),
                 color="#8d97a3", lw=2.2, head=9)
    MSG = "神経内灌流圧の低下 と 神経内浮腫"
    by = BTOP + BH + 40
    msz = cv.fit_size([MSG], R - L - 60, 13, weight="bold")
    bh = 30 + LH(msz, 1.5)
    cv.box(L, by, R - L, bh, fc="#fbeeee", ec="#c0392b", lw=2.2, radius=8)
    cv.text(W / 2, by + bh / 2, MSG, size=msz, color="#9c2b26", weight="bold")
    NOTE = ("※ 全身麻酔・鎮静・筋弛緩の下では、痛みやしびれによる防御反応が働かない。"
            "覚醒していれば姿勢を変えるはずの圧迫と牽引が、術野の都合で続く。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, by + bh + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f01_overlap.png"))


# ---------------------------------------------------------------- f02
def f02():
    W, H = 1520, 840
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "神経内で何が起きているか —— 静脈還流が先に止まる",
             size=12.5, ha="center")
    # 左：神経の断面
    LX, LY, LW_, LH_ = 56, 88, 560, 600
    cv.box(LX, LY, LW_, LH_, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    cv.text(LX + LW_ / 2, LY + 32, "末梢神経の断面（模式）", size=11.2,
            color=NAVY, weight="bold")
    cx, cy = LX + LW_ / 2, LY + 210
    ax.add_patch(Circle((cx, cy), 132, facecolor="#f2e6da",
                        edgecolor="#b98f78", lw=2.4, zorder=3))
    for dx, dy in ((-58, -44), (58, -44), (0, 56)):
        ax.add_patch(Circle((cx + dx, cy + dy), 56, facecolor="#fdf5ee",
                            edgecolor="#c8a415", lw=2.0, zorder=4))
        for ax_dx, ax_dy in ((-22, -16), (14, -20), (-6, 18), (24, 14)):
            ax.add_patch(Circle((cx + dx + ax_dx, cy + dy + ax_dy), 9,
                                facecolor="#cfd6de", edgecolor="#8d97a3",
                                lw=1.0, zorder=5))
        ax.add_patch(Circle((cx + dx - 2, cy + dy + 36), 6.5,
                            facecolor="#c0392b", edgecolor="white", lw=1.0,
                            zorder=6))
    LEG = [("外膜", "#b98f78"), ("周膜（神経束を包む）", "#c8a415"),
           ("軸索", "#8d97a3"), ("神経内の微小血管", "#c0392b")]
    lsz = min(cv.fit_size([n for n, _ in LEG], LW_ - 120, 9.6), 9.6)
    for j, (name, col) in enumerate(LEG):
        yy = LY + LH_ - 176 + LH(lsz, 1.7) * j
        ax.add_patch(Circle((LX + 46, yy), 7, facecolor=col,
                            edgecolor="#9aa4b0", lw=1.0, zorder=5))
        cv.text(LX + 64, yy, name, size=lsz, color=INK, ha="left")
    # 右：悪循環
    RX = LX + LW_ + 30
    RW_ = W - 56 - RX
    STEPS = [("外から神経内圧が上がる", "#b8760f"),
             ("静脈還流が妨げられる", "#2e6da4"),
             ("神経内浮腫", "#7b52a8"),
             ("さらに神経内圧が上がる", "#b8760f"),
             ("動脈側の灌流も落ちる → 虚血", "#c0392b"),
             ("伝導遅延 → 脱髄・軸索障害", "#8f2b28")]
    ssz = min(cv.fit_size([s[0] for s in STEPS], RW_ - 60, 10.6), 10.6)
    SH = 52
    SG = 14
    for i, (t, col) in enumerate(STEPS):
        y = LY + 46 + i * (SH + SG)
        cv.box(RX, y, RW_, SH, fc="white", ec=col, lw=1.8, radius=7)
        cv.text(RX + RW_ / 2, y + SH / 2, t, size=ssz, color=col,
                weight="bold")
        if i < len(STEPS) - 1:
            cv.arrow((RX + RW_ / 2, y + SH + 1), (RX + RW_ / 2, y + SH + SG - 1),
                     color="#8d97a3", lw=2.0, head=8)
    NOTE = ("※ 圧迫でも牽引でも、行き着く先は同じ。"
            "だから「どちらだったか」を当てることより、灌流を落とす条件を減らすほうが実務的である。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, LY + LH_ + 44 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f02_nerve_section.png"))


# ---------------------------------------------------------------- f03
def f03():
    W, H = 1520, 520
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "圧迫と牽引は、別の言葉ではない",
             size=12.5, ha="center")
    PANELS = [
        ("圧迫", "#b8760f", "骨突出部・硬い支持具・寝具",
         ["神経の外から内圧を高める", "静脈還流を妨げる",
          "例：肘部の尺骨神経溝、腓骨頭"]),
        ("牽引", "#2e6da4", "外転・回旋・過屈曲・固定点間の伸長",
         ["軸索そのものを伸ばす", "神経を養う vasa nervorum を伸ばす",
          "例：上肢外転＋頸部回旋での腕神経叢"]),
    ]
    L, GAPX = 70, 60
    PW = (W - L * 2 - GAPX) / 2.0
    PTOP, PH = 88, 250
    bsz = min(cv.fit_size(["・" + l for p in PANELS for l in p[3]],
                          PW - 60, 10.2), 10.2)
    for i, (title, col, sub, lines) in enumerate(PANELS):
        px = L + i * (PW + GAPX)
        cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
        cv.text(px + PW / 2, PTOP + 34, title, size=13, color=col,
                weight="bold")
        cv.text(px + PW / 2, PTOP + 64, sub,
                size=min(cv.fit_size([sub], PW - 44, 9.6), 9.6),
                color="#5d6875")
        for j, ln in enumerate(lines):
            cv.text(px + 30, PTOP + 106 + LH(bsz, 1.8) * j, "・" + ln,
                    size=bsz, color=INK, ha="left")
        cv.arrow((px + PW / 2, PTOP + PH + 2), (px + PW / 2, PTOP + PH + 32),
                 color="#8d97a3", lw=2.2, head=9)
    MSG = "神経内の灌流低下と浮腫 —— どちらも同じところへ収束する"
    by = PTOP + PH + 38
    msz = cv.fit_size([MSG], W - L * 2 - 60, 12.5, weight="bold")
    bh = 30 + LH(msz, 1.5)
    cv.box(L, by, W - L * 2, bh, fc="#fbeeee", ec="#c0392b", lw=2.2, radius=8)
    cv.text(W / 2, by + bh / 2, MSG, size=msz, color="#9c2b26", weight="bold")
    cv.save(P("f03_compression_traction.png"))


# ---------------------------------------------------------------- f04
def f04():
    W, H = 1520, 620
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "障害の深さで、回復の時間軸が変わる —— 症状の強さでは決まらない",
             size=12.5, ha="center")
    ROWS = [
        ("neurapraxia", "伝導ブロック", "#1f6b47",
         "一過性の髄鞘・伝導障害が中心",
         "圧迫解除後に回復しうる。ただし「症状が軽い」という意味ではない"),
        ("axonotmesis", "軸索障害", "#b8760f",
         "軸索が損傷し、再支配に時間を要する",
         "運動障害、筋萎縮、持続する感覚異常があれば疑う"),
        ("neurotmesis", "完全断裂", "#c0392b",
         "神経の連続性が失われる",
         "体位関連では稀。外科的損傷・高度圧迫との鑑別が必要"),
    ]
    L, R = 52, W - 52
    ENG_SZ, JP_SZ = 11.4, 10.4
    NAMEW = max(cv.measure(r[0], ENG_SZ, weight="bold")[0] for r in ROWS) + 56
    TOP, RH, GAP = 100, 108, 18
    bsz = min(cv.fit_size([r[3] for r in ROWS] + [r[4] for r in ROWS],
                          R - L - NAMEW - 70, 10.0), 10.0)
    for i, (eng, jp, col, change, view) in enumerate(ROWS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L, y, NAMEW, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(L + NAMEW / 2, y + RH / 2 - 13, eng, size=ENG_SZ,
                color="white", weight="bold")
        cv.text(L + NAMEW / 2, y + RH / 2 + 15, jp, size=JP_SZ, color="#f0f4f8")
        cv.text(L + NAMEW + 34, y + 36, "変化　" + change, size=bsz,
                color=INK, ha="left")
        cv.text(L + NAMEW + 34, y + 36 + LH(bsz, 1.75), "見方　" + view,
                size=bsz, color="#5d6875", ha="left")
    NOTE = ("※ 術後早期に病変の深さは確定できない。"
            "術前からの症状との比較、分布の局在、時間経過、運動障害の有無で追う。"
            "神経伝導検査・針筋電図の時期は症状と専門医の判断による。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, TOP + 3 * (RH + GAP) + 22 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f04_severity.png"))


# ---------------------------------------------------------------- f05
def f05():
    W, H = 1520, 650
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "「何％か」は、分母と障害の定義で変わる",
             size=12.5, ha="center")
    BARS = [
        ("術後尺骨神経障害\n持続運動障害のみ・診療コードから後向きに抽出",
         0.007, "0.007%", "#2e6da4", "非心臓手術（Hewson 2023）"),
        ("術後尺骨神経障害\n術後7日まで積極的に診察した前向きコホート",
         0.52, "0.52%", "#b8760f", "同じレビュー内の別データ（Hewson 2023）"),
        ("砕石位の下肢ニューロパチー\n術後早期に問診・診察",
         1.5, "1.5%", "#7b52a8", "成人991例中15例（Warner 2000）"),
        ("ロボット前立腺全摘の位置関連末梢神経障害\n後ろ向き電話追跡",
         5.6, "5.6%", "#c0392b", "868例中49例（Göksu 2025）"),
    ]
    L, R = 56, W - 56
    LABW = 560
    TOP, BH_, GAP = 96, 88, 18
    MAXV = 6.0
    barx0 = L + LABW + 30
    barw = R - barx0 - 150
    lsz = min(cv.fit_size([s for b in BARS for s in b[0].split("\n")],
                          LABW - 24, 9.8), 9.8)
    for i, (lab, v, txt, col, src) in enumerate(BARS):
        y = TOP + i * (BH_ + GAP)
        cv.box(L, y, R - L, BH_, fc="white", ec="#c3ccd6", lw=1.4, radius=7)
        parts = lab.split("\n")
        cv.text(L + 20, y + 30, parts[0], size=lsz, color=INK, ha="left",
                weight="bold")
        cv.text(L + 20, y + 30 + LH(lsz, 1.75), parts[1], size=lsz - 0.6,
                color="#5d6875", ha="left")
        wpx = max(barw * v / MAXV, 3)
        # 棒と数値を上段、出典を下段に分けて重ねない
        ax.add_patch(Rectangle((barx0, y + 14), wpx, 24,
                               facecolor=col, edgecolor="none", zorder=4))
        cv.text(barx0 + wpx + 14, y + 26, txt, size=11.2, color=col,
                weight="bold", ha="left")
        cv.text(barx0, y + BH_ - 16, src, size=8.8, color="#8d97a3", ha="left")
    NOTE = ("※ 同じ「尺骨神経障害」でも、何を障害として数えたかで70倍以上違う。"
            "頻度を引用するときは、分母・手術と体位・障害の定義・追跡期間を必ず添える。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, TOP + 4 * (BH_ + GAP) + 24 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f05_incidence.png"))


# ---------------------------------------------------------------- f06
def f06():
    W, H = 1520, 730
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "高リスク患者を見抜く —— 「予言」ではなく「個別化」のための項目",
             size=12.5, ha="center")
    ITEMS = [
        ("糖尿病", "#c0392b", "代謝・微小循環の変化で神経の予備能が下がる"),
        ("既存ニューロパチー", "#c0392b", "二重絞扼の背景。小さな追加圧迫で症候化する"),
        ("末梢血管疾患", "#b8760f", "灌流予備能の低下。低血圧・下肢高位で安全域が狭い"),
        ("低BMI", "#b8760f", "骨突出部を覆う軟部組織が少なく、接触圧が局在する"),
        ("肥満", "#b8760f", "体重による圧迫、頭低位でのずれ、支持具負荷、時間延長"),
        ("喫煙", "#2e6da4", "微小循環と酸素化の脆弱性"),
        ("慢性多量飲酒", "#2e6da4", "毒性・栄養性の軸索ニューロパチーを合併しうる"),
        ("可動域制限・関節症", "#2e6da4", "無理な角度が牽引と圧迫になる"),
    ]
    L, R = 48, W - 48
    GAPX, GAPY = 20, 16
    CW = (R - L - GAPX) / 2.0
    TOP = 96
    hsz = 11.0
    bsz = min(cv.fit_size([i[2] for i in ITEMS], CW - 44, 9.8), 9.8)
    CH = 40 + LH(bsz, 1.4) + 26
    for k, (head, col, body) in enumerate(ITEMS):
        r, c = divmod(k, 2)
        x = L + c * (CW + GAPX)
        y = TOP + r * (CH + GAPY)
        cv.box(x, y, CW, CH, fc="white", ec=col, lw=1.7, radius=7)
        cv.ax.add_patch(Rectangle((x, y + 8), 7, CH - 16, facecolor=col,
                                  edgecolor="none", zorder=4))
        cv.text(x + 26, y + 32, head, size=hsz, color=col, weight="bold",
                ha="left")
        cv.text(x + 26, y + 32 + LH(bsz, 1.9), body, size=bsz, color=INK,
                ha="left")
    NOTE = ("※ ASA の実践勧告は、体格、既存の神経症状、糖尿病、末梢血管疾患、"
            "アルコール依存、関節炎、性別を術前の病歴と診察で確認するよう示している。"
            "「この患者は必ず起こす」ではなく、通常より低い負荷で症候化しうる神経を先に見つける。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, TOP + 4 * (CH + GAPY) + 22 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f06_highrisk.png"))


# ---------------------------------------------------------------- f07
def f07():
    W, H = 1520, 560
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "術前リスクプロファイルを30秒でつくる",
             size=12.5, ha="center")
    STEPS = [
        ("① 脆弱性", "#2e6da4",
         ["糖尿病・既存のしびれ・末梢血管疾患", "体格・骨突出・皮膚・浮腫",
          "可動域制限、装具の有無"]),
        ("② 負荷", "#b8760f",
         ["予定体位と台の角度", "上肢の位置・支持具・気腹",
          "予定手術時間、ロボットの使用"]),
        ("③ 設計", "#1f6b47",
         ["どの神経を最も守るかを決める", "長時間化したときの再評価担当を決める",
          "術後に比較する所見を先に記録する"]),
    ]
    L, R = 52, W - 52
    GAP = 24
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 94, 50
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for s in STEPS for l in s[2]], CW - 46, 9.8),
             9.8)
    BH = 28 + LH(sz, 1.9) * 2 + LH(sz, 1.0) * 0.5 + 20
    for i, (head, col, lines) in enumerate(STEPS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.6, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            cv.text(x + 24, BTOP + 28 + LH(sz, 1.9) * j, "・" + ln, size=sz,
                    color=INK, ha="left")
        if i < 2:
            cv.arrow((x + CW + 3, BTOP + BH / 2), (x + CW + GAP - 3, BTOP + BH / 2),
                     color="#8d97a3", lw=2.2, head=10)
    MSG = "高リスクは「診断名の数」ではなく、脆弱性 × 負荷 で決まる"
    by = BTOP + BH + 30
    msz = cv.fit_size([MSG], R - L - 60, 12.5, weight="bold")
    bh = 30 + LH(msz, 1.5)
    cv.box(L, by, R - L, bh, fc="#e4f2f4", ec="#1f7f8b", lw=2.0, radius=8)
    cv.text(W / 2, by + bh / 2, MSG, size=msz, color="#0f6d78", weight="bold")
    NOTE = "※ このプロファイルは、患者を手術から外すためのものではない。どこを見るかを先に共有するための設計図である。"
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, by + bh + 32 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f07_profile30.png"))


for fn in (f01, f02, f03, f04, f05, f06, f07):
    fn()
    print("ok", fn.__name__)
