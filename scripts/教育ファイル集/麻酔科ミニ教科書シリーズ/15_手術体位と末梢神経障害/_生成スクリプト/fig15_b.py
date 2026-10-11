# -*- coding: utf-8 -*-
"""第15巻 手術体位と末梢神経障害 図版 f08〜f14"""
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


# ---------------------------------------------------------------- f08
def f08():
    W, H = 1520, 730
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "体位と神経の対応表 —— 体位名から、確認すべき場所を連想する",
             size=12.5, ha="center")
    ROWS = [
        ("仰臥位", "#2e6da4", ["尺骨神経（肘部）"],
         "アームボード上の前腕回内、体側への tuck、肘屈曲"),
        ("急峻頭低位", "#7b52a8", ["腕神経叢"],
         "頭側へのずれ、肩固定具、上肢外転、頸部回旋"),
        ("腹臥位", "#1f6b47", ["腕神経叢", "尺骨神経", "顔面・眼"],
         "肩外転・外旋、肘屈曲、頭頸部回旋、胸郭支持"),
        ("側臥位", "#b8760f", ["腕神経叢（下側）", "腓骨頭（下側）"],
         "腋窩の直接圧、頸部の側屈、上側上肢の牽引"),
        ("砕石位・半砕石位", "#c0392b",
         ["総腓骨神経", "坐骨神経", "大腿神経", "閉鎖神経", "WLCS"],
         "腓骨頭の直接圧、股関節の過屈曲・外転、下肢挙上"),
    ]
    L, R = 48, W - 48
    NAME_SZ = 11.2
    NAMEW = max(cv.measure(r[0], NAME_SZ, weight="bold")[0] for r in ROWS) + 48
    TOP, RH, GAP = 100, 92, 14
    TAG_SZ = 9.4
    tagw = {}
    for r in ROWS:
        tagw[r[0]] = [cv.measure(t, TAG_SZ, weight="bold")[0] + 26 for t in r[2]]
    TAGZONE = max(sum(v) + 10 * (len(v) - 1) for v in tagw.values()) + 30
    bsz = min(cv.fit_size([r[3] for r in ROWS],
                          R - L - NAMEW - TAGZONE - 60, 9.8), 9.8)
    for i, (name, col, tags, note) in enumerate(ROWS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L, y, NAMEW, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(L + NAMEW / 2, y + RH / 2, name, size=NAME_SZ, color="white",
                weight="bold")
        tx = L + NAMEW + 24
        for t, tw in zip(tags, tagw[name]):
            cv.box(tx, y + 14, tw, 36, fc="#f2f5f8", ec=col, lw=1.4, radius=6)
            cv.text(tx + tw / 2, y + 32, t, size=TAG_SZ, color=col,
                    weight="bold")
            tx += tw + 10
        cv.text(L + NAMEW + 24, y + RH - 24, "見るところ　" + note, size=bsz,
                color="#5d6875", ha="left")
    NOTE = ("※ 発生率の順位ではない。体位だけで危険が決まるのではなく、"
            "支持具・関節角度・台の角度・時間・循環状態を加えて読む。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, TOP + 5 * (RH + GAP) + 22 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f08_position_map.png"))


# ---------------------------------------------------------------- f09
def f09():
    W, H = 1520, 620
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "肘部の尺骨神経 —— 前腕の向きで、当たる面が変わる",
             size=12.5, ha="center")
    PANELS = [
        ("回内（手のひらを下）", "#c0392b", 0.0,
         ["尺骨神経溝が下（アームボード）を向く",
          "神経が骨と支持面のあいだで直接圧を受ける"]),
        ("回外／中間位", "#1f6b47", 1.0,
         ["尺骨神経溝が内側〜上を向く",
          "接触面と神経のあいだに軟部組織が入る"]),
    ]
    L, GAPX = 70, 60
    PW = (W - L * 2 - GAPX) / 2.0
    PTOP = 88
    ILL_H = 210
    bsz = min(cv.fit_size(["・" + l for p in PANELS for l in p[3]],
                          PW - 60, 10.0), 10.0)
    PH = 44 + ILL_H + 22 + LH(bsz, 1.8) * 1 + LH(bsz, 1.0) * 0.5 + 24
    for i, (title, col, rot, lines) in enumerate(PANELS):
        px = L + i * (PW + GAPX)
        cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
        cv.text(px + PW / 2, PTOP + 30, title, size=11.6, color=col,
                weight="bold")
        # 前腕断面の模式
        cxx, cyy = px + PW / 2, PTOP + 44 + ILL_H / 2 - 16
        ax.add_patch(Rectangle((px + 60, cyy + 78), PW - 120, 18,
                               facecolor="#cfd6de", edgecolor="#9aa4b0",
                               lw=1.4, zorder=2))
        cv.text(px + 68, cyy + 112, "支持面（アームボード）", size=9.0,
                color="#6b7785", ha="left", z=4)
        ax.add_patch(Circle((cxx, cyy), 66, facecolor="#f7e3d8",
                            edgecolor="#c99a86", lw=2.0, zorder=3))
        ax.add_patch(Circle((cxx - 26, cyy - 8), 22, facecolor="#e6dfd3",
                            edgecolor="#b8ac99", lw=1.6, zorder=4))
        ax.add_patch(Circle((cxx + 26, cyy - 8), 20, facecolor="#e6dfd3",
                            edgecolor="#b8ac99", lw=1.6, zorder=4))
        # 尺骨神経の位置：回内では下、回外では内上方
        nx, ny = (cxx + 4, cyy + 52) if rot == 0.0 else (cxx - 54, cyy - 26)
        ax.add_patch(Circle((nx, ny), 12, facecolor="#c8a415",
                            edgecolor="white", lw=1.8, zorder=6))
        cv.arrow((nx + 96, ny - 44), (nx + 16, ny - 8), color=col, lw=2.0,
                 head=9, z=6)
        cv.text(nx + 102, ny - 52, "尺骨神経", size=9.4, color=col,
                weight="bold", ha="left", z=6)
        for j, ln in enumerate(lines):
            cv.text(px + 28, PTOP + 44 + ILL_H + 26 + LH(bsz, 1.8) * j,
                    "・" + ln, size=bsz, color=INK, ha="left")
    NOTE = ("※ ASA の実践勧告は、仰臥位でアームボードを用いるときに前腕を回外または中間位とし、"
            "肘部への直達圧を避けるよう示している。腕を体側へ tuck するときは中間位にする。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, PTOP + PH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f09_ulnar_forearm.png"))


# ---------------------------------------------------------------- f10
def f10():
    W, H = 1520, 760
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "急峻頭低位と腕神経叢 —— 4つの負荷が同時に増える",
             size=12.5, ha="center")
    # 左：模式図
    LX, LY, LW_, LH_ = 56, 88, 640, 520
    cv.box(LX, LY, LW_, LH_, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    cv.text(LX + LW_ / 2, LY + 30, "頭低位（上から見たところ・模式）", size=11.2,
            color=NAVY, weight="bold")
    # 手術台（頭側が上）
    tw_, th_ = 210, 340
    tx = LX + LW_ / 2 - tw_ / 2
    ty = LY + 74
    ax.add_patch(Rectangle((tx, ty), tw_, th_, facecolor="#eef1f5",
                           edgecolor="#9aa4b0", lw=1.6, zorder=2))
    cv.text(tx + tw_ / 2, ty - 14, "頭側", size=9.2, color="#6b7785", z=4)
    cv.text(tx + tw_ / 2, ty + th_ + 30, "足側", size=9.2, color="#6b7785", z=4)
    # 体幹と頭
    cxx = tx + tw_ / 2
    ax.add_patch(Ellipse((cxx, ty + 190), 132, 226, facecolor="#f7e3d8",
                         edgecolor="#c99a86", lw=1.8, zorder=3))
    ax.add_patch(Ellipse((cxx + 14, ty + 56), 62, 74, angle=18,
                         facecolor="#f7e3d8", edgecolor="#c99a86", lw=1.8,
                         zorder=4))
    cv.arrow((cxx + 60, ty + 34), (cxx + 30, ty + 46), color="#7b52a8",
             lw=1.8, head=8, z=6)
    cv.text(cxx + 66, ty + 28, "頸部回旋", size=9.2, color="#7b52a8",
            weight="bold", ha="left", z=6)
    # 外転した上肢（左右）
    for sgn in (-1, 1):
        ax.plot([cxx + sgn * 56, cxx + sgn * 168], [ty + 132, ty + 158],
                color="#c99a86", lw=17, solid_capstyle="round", zorder=4)
        ax.add_patch(Rectangle((cxx + sgn * 176 - (86 if sgn > 0 else 0),
                                ty + 138), 86, 34, facecolor="#cfd6de",
                               edgecolor="#9aa4b0", lw=1.4, zorder=3))
    cv.text(cxx - 190, ty + 196, "上肢外転", size=9.2, color="#2e6da4",
            weight="bold", ha="center", z=6)
    cv.text(cxx + 190, ty + 196, "アームボード", size=9.2, color="#6b7785",
            ha="center", z=6)
    # 肩固定具
    for sgn in (-1, 1):
        ax.add_patch(Rectangle((cxx + sgn * 44 - (30 if sgn > 0 else 0),
                                ty + 92), 30, 26, facecolor="#8f2b28",
                               edgecolor="none", zorder=6))
    cv.text(cxx - 54, ty + 105, "肩固定具", size=9.2, color="#8f2b28",
            weight="bold", ha="right", z=7)
    # 頭側へのずれ
    cv.arrow((cxx, ty + 306), (cxx, ty + 240), color="#c0392b", lw=2.8,
             head=13, z=6)
    cv.text(cxx, ty + 324, "患者は頭側へ滑る", size=9.6, color="#c0392b",
            weight="bold", z=6)
    # 右：4つの負荷
    RX = LX + LW_ + 30
    RW_ = W - 56 - RX
    ITEMS = [("頭側へのずれ", "#c0392b", "重力で体幹が頭側へ動く"),
             ("肩固定具", "#b8760f", "肩峰周囲の圧、鎖骨・第1肋骨での圧迫"),
             ("上肢外転", "#2e6da4", "神経叢の固定点間距離が伸びる"),
             ("頸部回旋・側屈", "#7b52a8", "反対側の神経叢がさらに引かれる")]
    isz = min(cv.fit_size([i[2] for i in ITEMS], RW_ - 50, 9.8), 9.8)
    IH = 40 + LH(isz, 1.5) + 20
    IG = 14
    for i, (head, col, body) in enumerate(ITEMS):
        y = LY + 46 + i * (IH + IG)
        cv.box(RX, y, RW_, IH, fc="white", ec=col, lw=1.8, radius=7)
        ax.add_patch(Rectangle((RX, y + 8), 7, IH - 16, facecolor=col,
                               edgecolor="none", zorder=4))
        cv.text(RX + 26, y + 30, head, size=10.8, color=col, weight="bold",
                ha="left")
        cv.text(RX + 26, y + 30 + LH(isz, 1.9), body, size=isz, color=INK,
                ha="left")
    MSG = "ASA は、可能なら肩固定具を避け、仰臥位での上肢外転を90°以内にすることを示している"
    by2 = LY + LH_ + 24
    msz = min(cv.fit_size([MSG], W - 112 - 60, 11.5, weight="bold"), 11.5)
    bh = 30 + LH(msz, 1.5)
    cv.box(56, by2, W - 112, bh, fc="#e4f2f4", ec="#1f7f8b", lw=2.0, radius=8)
    cv.text(W / 2, by2 + bh / 2, MSG, size=msz, color="#0f6d78", weight="bold")
    cv.save(P("f10_trendelenburg.png"))


# ---------------------------------------------------------------- f11
def f11():
    W, H = 1520, 560
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "腹臥位と側臥位 —— 一つずつは安全でも、組合せで危なくなる",
             size=12.5, ha="center")
    PANELS = [
        ("腹臥位（脊椎手術）", "#1f6b47",
         ["肩外転・外旋 ＋ 肘屈曲 ＋ 頭頸部回旋が重なる",
          "腕神経叢は牽引、尺骨神経は肘部圧迫",
          "顔面・眼周囲は直接圧を避ける",
          "腹部を圧迫しない（換気・静脈還流・出血・浮腫に効く）"]),
        ("側臥位（胸部・腎）", "#b8760f",
         ["下側の腋窩を直接圧迫しない",
          "腋窩ロールは腋窩ではなく胸郭側で圧を分散する",
          "頭頸部は中間位、下側の肩・上腕・腓骨頭を保護",
          "上側の腕は、肩が下方へ牽引されていないか見る"]),
    ]
    L, GAPX = 60, 40
    PW = (W - L * 2 - GAPX) / 2.0
    PTOP, HH = 92, 52
    BTOP = PTOP + HH + 8
    bsz = min(cv.fit_size(["・" + l for p in PANELS for l in p[2]],
                          PW - 56, 10.0), 10.0)
    BH = 30 + LH(bsz, 1.95) * 3 + LH(bsz, 1.0) * 0.5 + 22
    for i, (head, col, lines) in enumerate(PANELS):
        px = L + i * (PW + GAPX)
        cv.box(px, PTOP, PW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(px + PW / 2, PTOP + HH / 2, head, size=11.8, color="white",
                weight="bold")
        cv.box(px, BTOP, PW, BH, fc="white", ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            cv.text(px + 26, BTOP + 30 + LH(bsz, 1.95) * j, "・" + ln,
                    size=bsz, color=INK, ha="left")
    NOTE = ("※ どちらも、長時間・片肺換気・体幹ベルト・台の屈曲・術者側からの接触が加わる。"
            "局所の圧迫だけでなく、低酸素・低血圧・低体温による神経灌流の低下を同時に見る。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, BTOP + BH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f11_prone_lateral.png"))


# ---------------------------------------------------------------- f12
def f12():
    W, H = 1520, 940
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "砕石位 —— 症状から圧迫点を逆算する",
             size=12.5, ha="center")
    ROWS = [
        ("総腓骨神経", "#c0392b", "足背の感覚異常、足背屈の低下",
         "腓骨頭と支持具・ベッド縁の直接圧"),
        ("坐骨神経", "#b8760f", "下腿・足部の広い感覚／運動異常",
         "股関節の屈曲・外旋、膝伸展による牽引"),
        ("大腿神経", "#2e6da4", "膝伸展の低下、前大腿・内側下腿の感覚異常",
         "股関節の過屈曲、支持具・鼠径部周辺の負荷"),
        ("閉鎖神経", "#7b52a8", "大腿内転の低下、内側大腿の違和感",
         "大腿の過外転・牽引"),
        ("外側大腿皮神経", "#1f6b47", "大腿外側の感覚異常",
         "股関節屈曲、支持具、鼠径靱帯周辺の圧迫"),
    ]
    L, R = 48, W - 48
    NAME_SZ = 11.0
    NAMEW = max(cv.measure(r[0], NAME_SZ, weight="bold")[0] for r in ROWS) + 44
    TOP, GAP = 100, 14
    bsz = min(cv.fit_size([r[2] for r in ROWS] + [r[3] for r in ROWS],
                          R - L - NAMEW - 130, 9.9), 9.9)
    RH = 34 + LH(bsz, 2.0) + LH(bsz, 1.0) * 0.5 + 24
    for i, (name, col, sym, mech) in enumerate(ROWS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L, y, NAMEW, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(L + NAMEW / 2, y + RH / 2, name, size=NAME_SZ, color="white",
                weight="bold")
        cv.text(L + NAMEW + 30, y + 34, "症状　" + sym, size=bsz, color=INK,
                ha="left")
        cv.text(L + NAMEW + 30, y + 34 + LH(bsz, 2.0), "機序　" + mech,
                size=bsz, color="#5d6875", ha="left")
    NOTE = ("※ これは典型像であって、手術侵襲・局所麻酔・術後浮腫・腰椎病変・神経走行の個体差で変わる。"
            "多神経領域に及ぶ、進行する、強い疼痛や腫脹を伴うときは、"
            "一神経の圧迫と決めつけず WLCS・血管障害・血腫・中枢性病変も含めて評価する。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, TOP + 5 * (RH + GAP) + 22 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f12_lithotomy_nerves.png"))


# ---------------------------------------------------------------- f13
def f13():
    W, H = 1520, 680
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "well-leg compartment syndrome —— 下肢を上げるほど、灌流圧は下がる",
             size=12.5, ha="center")
    # 左：静水圧の模式
    LX, LY, LW_, LH_ = 56, 88, 660, 440
    cv.box(LX, LY, LW_, LH_, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    cv.text(LX + LW_ / 2, LY + 30, "下肢挙上と局所灌流圧", size=11.2,
            color=NAVY, weight="bold")
    base_y = LY + 340
    ax.plot([LX + 60, LX + LW_ - 60], [base_y, base_y], color="#9aa4b0",
            lw=2.0, zorder=3)
    cv.text(LX + 64, base_y - 16, "右心房の高さ", size=9.4, color="#6b7785",
            ha="left", z=4)
    for k, (dh, col) in enumerate(((10, "#e0a83a"), (20, "#d2762b"),
                                   (30, "#c0392b"))):
        x = LX + 190 + k * 150
        y = base_y - dh * 6.4
        ax.plot([x, x], [base_y, y], color=col, lw=2.0, ls=":", zorder=4)
        ax.add_patch(Circle((x, y), 13, facecolor=col, edgecolor="white",
                            lw=1.6, zorder=5))
        cv.text(x, y - 32, "%d cm" % dh, size=9.8, color=col, weight="bold",
                z=6)
        cv.text(x, y - 64, "−%.1f mmHg" % (dh * 0.78), size=9.4, color=col,
                z=6)
    _cap = "血液の密度から、挙上 1 cm ごとにおよそ 0.78 mmHg 下がる"
    cv.text(LX + LW_ / 2, LY + LH_ - 30, _cap,
            size=min(cv.fit_size([_cap], LW_ - 60, 9.6), 9.6),
            color="#5d6875")
    # 右：悪循環
    RX = LX + LW_ + 30
    RW_ = W - 56 - RX
    STEPS = [("下肢挙上・膝屈曲・支持具", "#b8760f"),
             ("局所灌流圧の低下", "#2e6da4"),
             ("筋の虚血と浮腫", "#7b52a8"),
             ("区画内圧の上昇", "#c0392b"),
             ("さらに灌流が落ちる", "#8f2b28")]
    ssz = min(cv.fit_size([s[0] for s in STEPS], RW_ - 50, 10.6), 10.6)
    SH, SG = 56, 16
    for i, (t, col) in enumerate(STEPS):
        y = LY + 50 + i * (SH + SG)
        cv.box(RX, y, RW_, SH, fc="white", ec=col, lw=1.8, radius=7)
        cv.text(RX + RW_ / 2, y + SH / 2, t, size=ssz, color=col,
                weight="bold")
        if i < len(STEPS) - 1:
            cv.arrow((RX + RW_ / 2, y + SH + 1), (RX + RW_ / 2, y + SH + SG - 1),
                     color="#8d97a3", lw=2.0, head=8)
    NOTE = ("※ 数式を個々の患者にそのまま当てはめない。血圧、支持具、気腹、浮腫、手術時間を合わせて考える。"
            "砕石位・半砕石位に多く報告されるが、腹臥位・側臥位の報告もある。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, LY + LH_ + 40 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f13_wlcs_pressure.png"))


# ---------------------------------------------------------------- f14
def f14():
    W, H = 1520, 520
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "しびれ と WLCS を、同じものとして扱わない",
             size=12.5, ha="center")
    COLS = [
        ("経過を見てよい所見", "#1f6b47", "#eaf4ee",
         ["一過性の軽いしびれ", "限局した感覚低下", "進行しない",
          "疼痛・腫脹・色調変化を伴わない"]),
        ("緊急に除外する所見", "#c0392b", "#fbeeee",
         ["進行する強い疼痛", "他動伸展痛", "著明な緊満・腫脹",
          "冷感・変色、急速に進む運動低下"]),
    ]
    L, GAPX = 70, 50
    PW = (W - L * 2 - GAPX) / 2.0
    PTOP, HH = 92, 54
    BTOP = PTOP + HH + 8
    bsz = min(cv.fit_size(["・" + l for c in COLS for l in c[3]],
                          PW - 56, 10.4), 10.4)
    BH = 30 + LH(bsz, 1.95) * 3 + LH(bsz, 1.0) * 0.5 + 22
    for i, (head, col, fc, lines) in enumerate(COLS):
        px = L + i * (PW + GAPX)
        cv.box(px, PTOP, PW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(px + PW / 2, PTOP + HH / 2, head, size=12, color="white",
                weight="bold")
        cv.box(px, BTOP, PW, BH, fc=fc, ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            cv.text(px + 28, BTOP + 30 + LH(bsz, 1.95) * j, "・" + ln,
                    size=bsz, color=INK, ha="left")
    MSG = "足背動脈が触れることは、コンパートメント症候群を否定する材料にならない"
    by = BTOP + BH + 26
    msz = cv.fit_size([MSG], W - L * 2 - 60, 12, weight="bold")
    bh = 30 + LH(msz, 1.5)
    cv.box(L, by, W - L * 2, bh, fc="#fbeeee", ec="#c0392b", lw=2.2, radius=8)
    cv.text(W / 2, by + bh / 2, MSG, size=msz, color="#9c2b26", weight="bold")
    cv.save(P("f14_wlcs_signs.png"))


for fn in (f08, f09, f10, f11, f12, f13, f14):
    fn()
    print("ok", fn.__name__)
