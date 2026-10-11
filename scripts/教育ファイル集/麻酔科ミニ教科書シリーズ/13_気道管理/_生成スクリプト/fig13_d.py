# -*- coding: utf-8 -*-
"""第13巻 気道管理 図版 f16〜f20"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Ellipse, FancyBboxPatch
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f16
def f16():
    W, H = 1520, 616
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "CICO —— 宣言してから、メス・ブジー・チューブの4動作",
             size=12.5, ha="center")
    STEPS = [
        ("① 触知して固定", ["左手で喉頭を握り（laryngeal handshake）",
                       "輪状甲状膜を人差し指で押さえ続ける"]),
        ("② 横に切開", ["メスを刃を下（尾側）に向けて刺入し、",
                    "触知できなければ正中を縦に大きく切る"]),
        ("③ ブジーを気管へ", ["刃を 90°回して尾側に向け、",
                        "刃に沿ってブジーを気管内へ滑らせる"]),
        ("④ チューブを進める", ["内径 6.0 mm のチューブを通し、",
                         "カフを膨らませ、波形カプノで確認する"]),
    ]
    PW, PTOP, PH = 340, 88, 300
    for i, (head, lines) in enumerate(STEPS):
        px = 42 + i * (PW + 22)
        fc, ec = ("#fbeeee", "#c0392b")
        cv.box(px, PTOP, PW, PH, fc=fc, ec=ec, lw=1.9, radius=8)
        cv.text(px + PW / 2, PTOP + 36, head, size=11.4, color=ec,
                weight="bold", z=9)
        # 頸部の模式（正中断面）
        cxx = px + PW / 2 - 56
        top = PTOP + 74
        ax.add_patch(Rectangle((cxx - 46, top), 92, 62, facecolor="#e6d4c8",
                               edgecolor="#b98f78", lw=1.6, zorder=3))
        cv.text(cxx, top + 31, "甲状軟骨", size=8.6, color="#8a5a3c", z=4)
        ax.add_patch(Rectangle((cxx - 46, top + 66), 92, 26,
                               facecolor="#fbe3d6", edgecolor="#c0392b",
                               lw=1.8, zorder=3))
        cv.text(cxx + 56, top + 79, "輪状甲状膜", size=8.4, color="#c0392b",
                ha="left", z=4)
        ax.add_patch(Rectangle((cxx - 46, top + 96), 92, 40,
                               facecolor="#e6d4c8", edgecolor="#b98f78",
                               lw=1.6, zorder=3))
        cv.text(cxx, top + 116, "輪状軟骨", size=8.6, color="#8a5a3c", z=4)
        ax.add_patch(Rectangle((cxx - 34, top + 140), 68, 66,
                               facecolor="#eef1f5", edgecolor="#9aa4b0",
                               lw=1.5, zorder=3))
        cv.text(cxx, top + 174, "気管", size=8.6, color="#6b7785", z=4)
        y_mem = top + 79
        if i == 0:
            ax.plot([cxx - 90, cxx - 52], [y_mem, y_mem], color="#1f6b47",
                    lw=6, solid_capstyle="round", zorder=6)
            cv.text(cxx - 71, y_mem - 22, "指", size=9.0, color="#1f6b47", z=6)
        if i >= 1:
            ax.add_patch(Polygon([[cxx - 92, y_mem - 16], [cxx - 40, y_mem - 3],
                                  [cxx - 40, y_mem + 3], [cxx - 92, y_mem + 16]],
                                 closed=True, facecolor="#7c8894",
                                 edgecolor="#4a5768", lw=1.3, zorder=6))
            cv.text(cxx - 74, y_mem - 32, "メス", size=9.0, color="#4a5768", z=6)
        if i >= 2:
            ax.plot([cxx - 40, cxx + 6, cxx + 6], [y_mem, y_mem, y_mem + 128],
                    color="#d98e2b", lw=4.5, solid_capstyle="round", zorder=7)
            cv.text(cxx + 62, y_mem + 116, "ブジー", size=9.0, color="#b8760f",
                    ha="left", z=7)
        if i == 3:
            ax.add_patch(Rectangle((cxx - 14, y_mem - 6), 28, 132,
                                   facecolor="#cfe0ef", edgecolor="#2e6da4",
                                   lw=1.8, zorder=8))
            cv.text(cxx + 62, y_mem + 40, "チューブ", size=9.0, color="#2e6da4",
                    ha="left", z=8)
        for j, ln in enumerate(lines):
            cv.text(px + PW / 2, PTOP + PH + 30 + LH(9.6, 1.42) * j, ln,
                    size=min(cv.fit_size([ln], PW - 20, 9.6), 9.6), color=INK)
    NOTE = ("※ 「まだ挿管できるかもしれない」と迷っている間に低酸素が進む。"
            "挿管不能・マスク不能・SGA 不能が揃った時点で声に出して宣言し、この4動作へ移る。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, H - 66 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f16_cico.png"))


# ---------------------------------------------------------------- f17
def f17():
    W, H = 1520, 760
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "輪状甲状膜をどう見つけるか —— 触れないなら超音波で線を引く",
             size=12, ha="center")
    # 左：正面解剖
    LX, LY, LW, LH_ = 60, 88, 560, 490
    cv.box(LX, LY, LW, LH_, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    cv.text(LX + LW / 2, LY + 34, "前頸部の正中構造", size=11.4, color=NAVY,
            weight="bold")
    cxx = LX + LW / 2 - 40
    y0 = LY + 74
    ax.add_patch(Polygon([[cxx - 60, y0 + 78], [cxx - 60, y0 + 18],
                          [cxx, y0], [cxx + 60, y0 + 18], [cxx + 60, y0 + 78]],
                         closed=True, facecolor="#e6d4c8", edgecolor="#b98f78",
                         lw=1.8, zorder=3))
    cv.text(cxx, y0 + 46, "甲状軟骨", size=9.4, color="#8a5a3c", z=4)
    ax.add_patch(Rectangle((cxx - 60, y0 + 82), 120, 34, facecolor="#fbe3d6",
                           edgecolor="#c0392b", lw=2.2, zorder=3))
    ax.add_patch(Rectangle((cxx - 60, y0 + 120), 120, 46, facecolor="#e6d4c8",
                           edgecolor="#b98f78", lw=1.8, zorder=3))
    cv.text(cxx, y0 + 143, "輪状軟骨", size=9.4, color="#8a5a3c", z=4)
    for k in range(4):
        ax.add_patch(Rectangle((cxx - 46, y0 + 174 + k * 30), 92, 22,
                               facecolor="#eef1f5", edgecolor="#9aa4b0",
                               lw=1.4, zorder=3))
    cv.text(cxx, y0 + 294, "気管軟骨", size=9.4, color="#6b7785", z=4)
    # 寸法
    ax.annotate("", xy=(cxx + 82, y0 + 82), xytext=(cxx + 82, y0 + 116),
                arrowprops=dict(arrowstyle="<|-|>", color="#c0392b", lw=1.6))
    cv.text(cxx + 92, y0 + 99, "高さ 約 9 mm", size=9.4, color="#c0392b",
            ha="left", z=5)
    ax.annotate("", xy=(cxx - 58, y0 + 110), xytext=(cxx + 58, y0 + 110),
                arrowprops=dict(arrowstyle="<|-|>", color="#2e6da4", lw=1.6),
                zorder=6)
    cv.text(cxx + 92, y0 + 136, "幅 約 30 mm", size=9.4, color="#2e6da4",
            ha="left", z=5)
    cv.text(cxx - 96, y0 + 99, "輪状甲状膜", size=10, color="#c0392b",
            ha="right", weight="bold", z=5)
    ax.plot([cxx - 92, cxx - 62], [y0 + 99, y0 + 99], color="#c0392b",
            lw=1.4, ls=":", zorder=5)

    # 右：手順
    RX, RW_ = 660, W - 60 - 660
    ITEMS = [
        ("① 触知（laryngeal handshake）", "#1f6b47",
         ["母指と中指で甲状軟骨を挟み、",
          "示指を尾側へ滑らせて陥凹を探す"]),
        ("② 触れないとき", "#b8760f",
         ["高度肥満・浮腫・血腫・頸部手術後では",
          "触知の正答率が大きく落ちる"]),
        ("③ 超音波で線を引く", "#2e6da4",
         ["高周波リニアで正中縦走査、",
          "気管輪と輪状軟骨を数えて位置に印を付ける"]),
        ("④ 印は導入前に付ける", "#c0392b",
         ["困難が予想される症例では、",
          "麻酔導入の前に皮膚マーキングを済ませる"]),
    ]
    IY, IH, IG = LY + 8, 118, 12
    for i, (head, col, lines) in enumerate(ITEMS):
        y = IY + i * (IH + IG)
        cv.box(RX, y, RW_, IH, fc="white", ec=col, lw=1.7, radius=8)
        cv.text(RX + 24, y + 28, head, size=10.6, color=col, weight="bold",
                ha="left")
        for j, ln in enumerate(lines):
            cv.text(RX + 24, y + 60 + LH(9.6, 1.35) * j, ln, size=9.6,
                    color=INK, ha="left")
    NOTE = ("※ 「だいたいこの辺」で切ると、甲状腺や大血管に入る。"
            "触知が確実でないなら、事前に超音波で線を引いておくことが最大の準備になる。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, H - 66 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f17_cricothyroid.png"))


# ---------------------------------------------------------------- f18
def f18():
    W, H, DPI = 1520, 780, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    fig.suptitle("カプノグラムは「換気の有無」だけでなく「どこが詰まっているか」を語る",
                 fontsize=12.5, color="#0A1830", fontweight="bold", y=0.968)
    t = np.linspace(0, 3, 900)

    def sq(rise, plateau, fall, slope=0.0, amp=38):
        y = np.zeros_like(t)
        for k in range(3):
            t0 = k * 1.0
            up = np.clip((t - (t0 + 0.05)) / rise, 0, 1)
            dn = np.clip(((t0 + 0.05 + rise + plateau + fall) - t) / fall, 0, 1)
            seg = np.minimum(up, dn)
            seg = np.clip(seg, 0, 1)
            y = np.maximum(y, seg * (amp + slope * np.clip(
                (t - (t0 + 0.05 + rise)) / max(plateau, 1e-6), 0, 1) * amp))
        return y

    PANELS = [
        ("正常波形", "#1f6b47", sq(0.08, 0.42, 0.06, slope=0.06),
         "急峻な立ち上がり、平坦な呼気相、鋭い下降"),
        ("食道挿管", "#c0392b", np.zeros_like(t) + 0.4,
         "波形が出ない、または数回で消える"),
        ("気管支痙攣・下気道閉塞", "#b8760f", sq(0.24, 0.30, 0.08, slope=0.42),
         "立ち上がりが鈍り、平坦部が右上がり（shark fin）"),
        ("回路リーク・カフ漏れ", "#2e6da4", sq(0.08, 0.42, 0.06, slope=0.06,
                                     amp=22),
         "波形の形は保たれるが高さが下がる"),
    ]
    for i, (name, col, y, desc) in enumerate(PANELS):
        ax = fig.add_axes([0.128 + (i % 2) * 0.478, 0.600 - (i // 2) * 0.395,
                           0.355, 0.245])
        ax.plot(t, y, color=col, lw=2.8)
        ax.set_xlim(0, 3)
        ax.set_ylim(-3, 62)
        ax.set_yticks([0, 20, 40])
        ax.set_xticks([])
        ax.set_ylabel("EtCO₂\n(mmHg)", fontsize=9.5, color=INK, labelpad=8,
                      linespacing=1.5)
        ax.set_title(name, fontsize=11, color=col, fontweight="bold", pad=8)
        ax.tick_params(labelsize=9.5, colors=INK)
        ax.grid(axis="y", color="#eceff2", lw=0.9)
        ax.set_axisbelow(True)
        for s in ax.spines.values():
            s.set_color("#9aa4b0")
        ax.text(0.5, -0.24, desc, transform=ax.transAxes, fontsize=9.6,
                color=INK, ha="center", va="top")
    for i, ln in enumerate([
            "※ 波形が出ないことは食道挿管の強い証拠だが、心停止や完全閉塞でも出ない。",
            "　 「出ない＝抜く」と決める前に、循環と回路を同時に確かめる。"]):
        fig.text(0.5, 0.072 - i * 0.038, ln, fontsize=9.6, color="#8d97a3",
                 ha="center", va="center")
    fig.savefig(P("f18_capnogram.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f19
def f19():
    W, H = 1520, 718
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "抜管は「導入の逆再生」ではない —— 計画して行う手技である",
             size=12.5, ha="center")
    COLS = [
        ("低リスク抜管", "#eaf4ee", "#1f6b47",
         ["気道は導入時と変わっていない", "換気・酸素化・循環が安定",
          "十分に覚醒し、指示に従える", "筋弛緩が完全に回復（TOF比 > 0.9）"],
         ["十分な酸素化ののち抜管", "抜管後も酸素と観察を継続"]),
        ("高リスク抜管", "#fbeeee", "#c0392b",
         ["挿管が困難だった", "頸部・気道の手術、長時間の腹臥位",
          "浮腫・出血・血腫が疑われる", "肥満・OSA・呼吸筋力の低下"],
         ["カフリークテストと直視下確認", "気道交換用カテーテルを留置",
          "再挿管の人員と器具を室内に置く", "覚醒室ではなく ICU での抜管も選ぶ"]),
    ]
    L, R = 56, W - 56
    GAP = 26
    CW = (R - L - GAP) / 2
    HTOP, HH = 100, 56
    BTOP = HTOP + HH + 8
    a_sz = min(cv.fit_size([l for c in COLS for l in c[3]], CW - 56, 10.4), 10.4)
    b_sz = min(cv.fit_size([l for c in COLS for l in c[4]], CW - 56, 10.4), 10.4)
    nmax = max(len(c[4]) for c in COLS)
    BH = 30 + LH(a_sz, 1.55) * 4 + 34 + 26 + LH(b_sz, 1.55) * nmax + 26
    for i, (head, fc, ec, crit, plan) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=ec, ec=ec, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.6, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc=fc, ec=ec, lw=1.8, radius=8)
        cy = BTOP + 26
        cv.text(x + 30, cy, "こういう状況", size=9.6, color=ec, weight="bold",
                ha="left")
        cy += 20
        for j, ln in enumerate(crit):
            cv.text(x + 30, cy + LH(a_sz, 1.55) * (j + 0.5), "・" + ln,
                    size=a_sz, color=INK, ha="left")
        cy += LH(a_sz, 1.55) * 4 + 20
        cv.ax.plot([x + 30, x + CW - 30], [cy, cy], color=ec, lw=1.2,
                   ls=":", zorder=4)
        cy += 24
        cv.text(x + 30, cy, "こうする", size=9.6, color=ec, weight="bold",
                ha="left")
        cy += 20
        for j, ln in enumerate(plan):
            cv.text(x + 30, cy + LH(b_sz, 1.55) * (j + 0.5), "・" + ln,
                    size=b_sz, color=INK, ha="left")
    NOTE = ("※ 抜管直後の再挿管は、導入時よりも条件が悪い。"
            "浮腫・出血・分泌があり、患者は疲れ、術者は油断している。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, BTOP + BH + 36 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f19_extubation.png"))


# ---------------------------------------------------------------- f20
def f20():
    W, H = 1520, 730
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "困難気道カート —— 段の順番が、そのままアルゴリズムの順番になる",
             size=12.5, ha="center")
    DRAWERS = [
        ("最上段", "#1f6b47", "呼ぶ・知らせる",
         "アルゴリズムカード／応援要請の連絡先／記録用紙"),
        ("第2段", "#2e6da4", "換気を立て直す",
         "各サイズの第2世代 SGA／経口・経鼻エアウェイ／2人法用のマスク"),
        ("第3段", "#7b52a8", "見る・通す",
         "ビデオ喉頭鏡（標準ブレードと強湾曲ブレード）／ブジー／専用スタイレット"),
        ("第4段", "#b8760f", "細い道を通す",
         "気管支鏡と光源／気道交換用カテーテル／細径チューブ（内径 5.0〜6.0 mm）"),
        ("最下段", "#c0392b", "前頸部へ",
         "メス（No.10）／ブジー／カフ付きチューブ 内径 6.0 mm／固定用テープ"),
    ]
    L, R = 60, W - 60
    TOP, RH, GAP = 104, 88, 14
    TAGW, ACTW = 130, 250
    body_sz = min(cv.fit_size([d[3] for d in DRAWERS],
                              R - L - TAGW - ACTW - 90, 10), 10)
    for i, (tag, col, act, body) in enumerate(DRAWERS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc="#f7f8f9", ec=col, lw=1.8, radius=8)
        cv.box(L + 12, y + 14, TAGW, RH - 28, fc=col, ec=col, lw=0, radius=6)
        cv.text(L + 12 + TAGW / 2, y + RH / 2, tag, size=10.6, color="white",
                weight="bold")
        cv.text(L + TAGW + 40, y + RH / 2, act, size=11, color=col,
                weight="bold", ha="left")
        cv.text(L + TAGW + ACTW + 60, y + RH / 2, body, size=body_sz,
                color=INK, ha="left")
    NOTE = ("※ 中身より配置が大事である。誰が開けても同じ順に同じ物が出てくること、"
            "そして月1回、実際に開けて期限と作動を確認することが、カートの価値を決める。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, TOP + 5 * (RH + GAP) + 26 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f20_cart.png"))


for fn in (f16, f17):
    fn()
    print("ok", fn.__name__)
