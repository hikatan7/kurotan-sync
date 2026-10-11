# -*- coding: utf-8 -*-
"""第14巻 血管確保 図版 f01〜f07"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, Polygon
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False
ART, VEIN, NERVE = "#c0392b", "#2e6da4", "#c8a415"
TENDON, SKIN = "#cfd6de", "#f3ddd0"


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f01
def f01():
    W, H = 1520, 620
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "3つの手技は「血管に針を入れる」だけが同じで、目的が違う",
             size=12.5, ha="center")
    COLS = [
        ("末梢静脈ライン", "#eaf1f8", "#2e6da4",
         ["目的：薬剤・輸液・輸血を", "血管内へ入れる"],
         ["求められるもの", "流量（太さと長さで決まる）"],
         "入らなければ薬が入らない"),
        ("橈骨動脈穿刺", "#fbeeee", "#c0392b",
         ["目的：動脈血を採る", "（血液ガス分析）"],
         ["求められるもの", "一回で入れて、早く止血する"],
         "失敗すれば血腫が残る"),
        ("観血的動脈圧ライン", "#eaf4ee", "#1f6b47",
         ["目的：拍動ごとの血圧を", "連続して測る"],
         ["求められるもの", "留置と回路の信頼性"],
         "入ったあとの回路で数値が変わる"),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH, BTOP = 96, 54, 156
    sz = min(cv.fit_size([l for c in COLS for l in c[3] + c[4]] +
                         [c[5] for c in COLS], CW - 40, 10.2), 10.2)
    D_AIM = 34
    D_DIV = D_AIM + LH(sz, 1.45) * 2 + 26
    D_NEED = D_DIV + 26
    D_RISKH = D_NEED + LH(sz, 1.5) + 46
    D_RISK = D_RISKH + LH(sz, 1.5)
    BH = D_RISK + LH(sz, 1.0) * 0.5 + 18
    for i, (head, fc, ec, aim, need, risk) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=ec, ec=ec, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.5, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc=fc, ec=ec, lw=1.8, radius=8)
        for j, ln in enumerate(aim):
            cv.text(x + CW / 2, BTOP + D_AIM + LH(sz, 1.45) * j, ln, size=sz,
                    color=INK)
        cv.ax.plot([x + 34, x + CW - 34], [BTOP + D_DIV, BTOP + D_DIV],
                   color=ec, lw=1.2, ls=":", zorder=4)
        cv.text(x + CW / 2, BTOP + D_NEED, need[0], size=sz - 0.6, color=ec,
                weight="bold")
        cv.text(x + CW / 2, BTOP + D_NEED + LH(sz, 1.5), need[1], size=sz,
                color=INK)
        cv.text(x + CW / 2, BTOP + D_RISKH, "失敗すると", size=sz - 0.8,
                color="#8d97a3")
        cv.text(x + CW / 2, BTOP + D_RISK, risk, size=sz, color=ec,
                weight="bold")
    MSG = "共通するのは3つ ── 入れる前に見る・測る／針先を見失わない／止めどきを決めておく"
    by = BTOP + BH + 26
    msz = cv.fit_size([MSG], R - L - 60, 11.5, weight="bold")
    bh = 30 + LH(msz, 1.5)
    cv.box(L, by, R - L, bh, fc="#e4f2f4", ec="#1f7f8b", lw=2.0, radius=8)
    cv.text(W / 2, by + bh / 2, MSG, size=msz, color="#0f6d78", weight="bold")
    cv.save(P("f01_three_procedures.png"))


# ---------------------------------------------------------------- f02
def f02():
    W, H = 1520, 700
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "上肢の短軸像 —— 針を進める前に「隣に何があるか」を見る",
             size=12.5, ha="center")
    PANELS = [
        (44, "上腕", [("上腕動脈", ART, (0, -8), 30),
                    ("正中神経", NERVE, (58, 6), 22),
                    ("尺側皮静脈", VEIN, (-72, 26), 34)],
         ["動脈のすぐ内側に正中神経が並走する"]),
        (400, "前腕近位", [("橈骨動脈", ART, (-8, 4), 24),
                       ("橈骨神経浅枝", NERVE, (46, -6), 16),
                       ("橈側皮静脈", VEIN, (-70, 30), 28)],
         ["橈骨神経の浅枝が伴走する"]),
        (756, "手関節（橈側）", [("橈骨動脈", ART, (-6, 6), 24),
                          ("橈側手根屈筋腱", TENDON, (58, 12), 26),
                          ("橈骨", "#e6dfd3", (-4, 62), 46)],
         ["正中神経は手根管の中にあり動脈から離れる"]),
        (1112, "手関節（尺側）", [("尺骨動脈", ART, (-10, 6), 24),
                          ("尺骨神経", NERVE, (34, 10), 20),
                          ("尺骨", "#e6dfd3", (6, 62), 44)],
         ["神経が動脈に接し、損傷のリスクが高い"]),
    ]
    PW, PTOP, PH = 340, 88, 330
    for px, title, items, caption in PANELS:
        cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
        cv.text(px + PW / 2, PTOP + 34, title, size=11.2, color=NAVY,
                weight="bold")
        cx, cy = px + PW / 2, PTOP + 190
        ax.add_patch(Rectangle((px + 34, PTOP + 62), PW - 68, PH - 96,
                               facecolor="#2b2f36", edgecolor="none", zorder=2))
        ax.add_patch(Rectangle((px + 34, PTOP + 62), PW - 68, 26,
                               facecolor=SKIN, edgecolor="none", zorder=3))
        cv.text(px + 44, PTOP + 75, "皮膚", size=8.4, color="#8a5a3c",
                ha="left", z=4)
        for name, col, (dx, dy), rr in items:
            ax.add_patch(Circle((cx + dx, cy + dy), rr, facecolor=col,
                                edgecolor="white", lw=1.6, zorder=5))
        for k, (name, col, (dx, dy), rr) in enumerate(items):
            side = -1 if dx <= 0 else 1
            lx = cx + dx + side * (rr + 10)
            cv.text(lx, cy + dy, name, size=8.6, color="white",
                    ha="left" if side > 0 else "right", z=6)
        for i2, ln in enumerate(caption):
            cv.text(px + PW / 2, PTOP + PH + 30 + LH(9.6, 1.4) * i2, ln,
                    size=min(cv.fit_size([ln], PW - 16, 9.6), 9.6), color=INK)
    NOTE = ("※ 模式図。実際の位置関係は個体差が大きい。"
            "触れる一点だけで決めず、走査して最も条件のよい区間を選ぶ。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, H - 66 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f02_us_anatomy.png"))


# ---------------------------------------------------------------- f03
def f03():
    W, H, DPI = 1520, 800, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0.115, 0.225, 0.855, 0.63])
    G = ["24 G", "22 G", "20 G", "18 G", "16 G", "14 G"]
    FLOW = [16, 33, 60, 98, 195, 290]
    COL = ["#e8c84a", "#5b8fd0", "#e58fb0", "#3f9b6a", "#8d97a3", "#e07b39"]
    x = np.arange(len(G))
    ax.bar(x, FLOW, 0.6, color=COL)
    base = FLOW[2]
    for xi, v in zip(x, FLOW):
        # 倍率は棒の中に入りきらないので、流量の下に2行目として出す
        ax.annotate("%d mL/分" % v, (xi, v), textcoords="offset points",
                    xytext=(0, 26), ha="center", fontsize=11, color=INK,
                    fontweight="bold")
        ax.annotate("（20 G の %.1f 倍）" % (v / base), (xi, v),
                    textcoords="offset points", xytext=(0, 7), ha="center",
                    fontsize=9, color="#5d6875")
    ax.set_xticks(x)
    ax.set_xticklabels(G, fontsize=12.5, color=INK)
    ax.set_ylim(0, 370)
    ax.set_ylabel("重力落下での流量の目安（mL/分）", fontsize=12, color=INK,
                  labelpad=10)
    ax.set_title("太さが流量を決める —— 内径の4乗に比例する", fontsize=13,
                 color="#0A1830", weight="bold", pad=16)
    ax.grid(axis="y", color="#eceff2", lw=1.0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11.5, colors=INK)
    for s in ax.spines.values():
        s.set_color("#7c8894")
    for i, ln in enumerate([
            "※ 製品と条件で変わる代表値。中心静脈カテーテルは「太い」が「長い」ため、",
            "　 急速輸液では末梢の 16〜18 G に劣ることがある。急ぐなら太く・短く・温める。"]):
        fig.text(0.5, 0.085 - i * 0.042, ln, fontsize=9.8, color="#8d97a3",
                 ha="center", va="center")
    fig.savefig(P("f03_gauge_flow.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f04
def f04():
    W, H = 1520, 740
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "末梢静脈路の部位 —— 関節をまたがず、直線的で、固定しやすい前腕から",
             size=12, ha="center")
    ROWS = [
        ("前腕（橈側・尺側皮静脈）", "#eaf4ee", "#1f6b47", "第一選択",
         "直線的で固定しやすく、関節をまたがない。18〜20 G が入りやすい"),
        ("肘窩（肘正中皮静脈）", "#e9f0fa", "#2e6da4", "緊急・造影",
         "太いが関節をまたぐ。屈曲でアラームと閉塞が増え、長期留置に向かない"),
        ("上腕（尺側皮静脈）", "#fdf1e0", "#b8760f", "超音波ガイドで",
         "深く触れない。上腕動脈・正中神経が近い。長めのカテーテルが要る"),
        ("手背", "#fdf1e0", "#b8760f", "細径のみ",
         "細く痛みが強い。手関節の動きで屈曲・閉塞しやすい"),
        ("下肢", "#fbeeee", "#c0392b", "やむを得ないとき",
         "成人では感染と静脈血栓のリスクが高い。早期に上肢へ入れ替える"),
    ]
    L, R = 52, W - 52
    NAME_SZ, TAG_SZ = 11.0, 9.8
    NAMEW = max(cv.measure(r[0], NAME_SZ, weight="bold")[0] for r in ROWS) + 52
    TAGW = max(cv.measure(r[3], TAG_SZ, weight="bold")[0] for r in ROWS) + 34
    TOP, RH, GAP = 100, 88, 14
    body_sz = min(cv.fit_size([r[4] for r in ROWS],
                              R - L - NAMEW - TAGW - 72, 10.2), 10.2)
    for i, (name, fc, ec, tag, body) in enumerate(ROWS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc=fc, ec=ec, lw=1.8, radius=8)
        cv.text(L + 26, y + RH / 2, name, size=NAME_SZ, color=ec, weight="bold",
                ha="left")
        cv.box(L + NAMEW, y + 18, TAGW, RH - 36, fc=ec, ec=ec, lw=0, radius=6)
        cv.text(L + NAMEW + TAGW / 2, y + RH / 2, tag, size=TAG_SZ,
                color="white", weight="bold")
        cv.text(L + NAMEW + TAGW + 30, y + RH / 2, body, size=body_sz,
                color=INK, ha="left")
    NOTE = ("※ カテーテル外径と血管径の比が大きいほど静脈炎・血栓・閉塞は増える。"
            "太ければよいのではなく、必要な流量から逆算する。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, TOP + 5 * (RH + GAP) + 28 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f04_pv_site.png"))


# ---------------------------------------------------------------- f05
def f05():
    W, H = 1520, 580
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "逆血のあとの3手 —— 内針の先端と外筒の先端には 1〜2 mm の差がある",
             size=12, ha="center")
    TX, TY, TW, TH = 60, 84, W - 120, 206
    cv.box(TX, TY, TW, TH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    vy = TY + 116
    ax.add_patch(Rectangle((TX + 60, vy - 34), TW - 120, 68,
                           facecolor="#dceaf5", edgecolor="#5b8fd0",
                           lw=2.0, zorder=3))
    cv.text(TX + 92, vy + 52, "血管腔", size=9.6, color="#2e6da4", ha="left", z=5)
    nx0, nx1 = TX + 120, TX + 700
    ax.add_patch(Rectangle((nx0, vy - 12), nx1 - nx0, 24,
                           facecolor="#cfd6de", edgecolor="#6b7785",
                           lw=1.4, zorder=4))
    cv.text(nx0 + 60, vy - 26, "外筒（カテーテル）", size=9.2, color="#4a5768",
            ha="left", z=6)
    ax.add_patch(Polygon([[nx1, vy - 7], [nx1 + 78, vy], [nx1, vy + 7]],
                         closed=True, facecolor="#8d97a3",
                         edgecolor="#4a5768", lw=1.2, zorder=5))
    ax.plot([nx1 + 78, nx1 + 78], [vy - 40, vy - 58], color="#c0392b", lw=1.4)
    cv.text(nx1 + 78, vy - 68, "内針の先端 ── ここで逆血が出る", size=9.4,
            color="#c0392b", z=6)
    ax.plot([nx1, nx1], [vy + 20, vy + 40], color="#b8760f", lw=1.4)
    cv.text(nx1, vy + 54, "外筒の先端はまだ 1〜2 mm 手前", size=9.4,
            color="#b8760f", z=6)

    STEPS = [
        ("① 寝かせる", "針の角度を浅くする。そのままだと後壁を突く", "#1f6b47"),
        ("② 1〜2 mm 進める", "外筒の先端まで管腔内に入れる。針先だけでは足りない", "#2e6da4"),
        ("③ 外筒だけ進める", "内針は動かさず、外筒を血管の走行に沿って送る", "#b8760f"),
    ]
    SY, SG = TY + TH + 30, 20
    SW = (W - 120 - SG * 2) / 3
    BSZ = 9.8
    nl = max(len(cv.wrap(s[1], SW - 40, BSZ)) for s in STEPS)
    SH = 76 + LH(BSZ, 1.4) * (nl - 1) + LH(BSZ, 1.0) * 0.5 + 20
    for i, (head, body, col) in enumerate(STEPS):
        x = 60 + i * (SW + SG)
        cv.box(x, SY, SW, SH, fc="white", ec=col, lw=1.9, radius=8)
        cv.text(x + SW / 2, SY + 34, head, size=11.2, color=col, weight="bold")
        for j, ln in enumerate(cv.wrap(body, SW - 40, BSZ)):
            cv.text(x + SW / 2, SY + 76 + LH(BSZ, 1.4) * j, ln, size=BSZ,
                    color=INK)
        if i < 2:
            cv.arrow((x + SW + 3, SY + SH / 2), (x + SW + SG - 3, SY + SH / 2),
                     color="#8d97a3", lw=2.2, head=10)
    NOTE = ("※ 「入らない」の大半は、穿刺の瞬間ではなく逆血が出たあとの2〜3秒で起きている。"
            "外筒が進まないときに力を加えない。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, SY + SH + 32 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f05_backflow.png"))


# ---------------------------------------------------------------- f06
def f06():
    W, H = 1520, 660
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "短軸法 —— 画面の白い点が「針先」であることを毎回確かめる",
             size=12.5, ha="center")
    PANELS = [
        ("A　針体が映っている", 0.0, False,
         "点は針のどこかであって、針先とは限らない"),
        ("B　扇状に振る（fanning）", 0.0, True,
         "点が消える位置を探す。そこが針先である"),
        ("C　針先を管腔内へ", 1.0, False,
         "プローブを近位へ滑らせ、点を追いながら進める"),
    ]
    PW, PTOP, PH = 452, 88, 340
    for i, (title, adv, fan, cap) in enumerate(PANELS):
        px = 56 + i * (PW + 22)
        cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
        cv.text(px + PW / 2, PTOP + 34, title, size=11, color=NAVY,
                weight="bold")
        ax.add_patch(Rectangle((px + 40, PTOP + 60), PW - 80, PH - 96,
                               facecolor="#2b2f36", edgecolor="none", zorder=2))
        cx, cy = px + PW / 2, PTOP + 210
        ax.add_patch(Circle((cx, cy), 44, facecolor="#111417",
                            edgecolor="#c0392b", lw=2.4, zorder=4))
        cv.text(cx, cy + 66, "動脈（短軸）", size=9, color="#e08b80", z=5)
        # 針の点
        pt = (cx, cy) if adv > 0 else (cx - 6, cy - 74)
        ax.add_patch(Circle(pt, 7, facecolor="white", edgecolor="none", zorder=6))
        if fan:
            for k, sgn in enumerate((-1, 1)):
                ax.annotate("", xy=(cx + sgn * 74, PTOP + 96),
                            xytext=(cx, PTOP + 76),
                            arrowprops=dict(arrowstyle="->", color="#8fd0c0",
                                            lw=1.8))
            cv.text(cx, PTOP + 82, "扇状に振る", size=9, color="#8fd0c0", z=6)
        for j, ln in enumerate(cv.wrap(cap, PW - 30, 9.8)):
            cv.text(px + PW / 2, PTOP + PH + 30 + LH(9.8, 1.4) * j, ln,
                    size=9.8, color=INK)
    NOTE = ("※ 短軸像に映る白い点は、走査面と針が交差した断面にすぎない。"
            "針先を追えていないまま前進させないことが、後壁穿刺と血腫を減らす。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, H - 66 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f06_short_axis.png"))


# ---------------------------------------------------------------- f07
def f07():
    W, H = 1520, 540
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "長軸・インプレーン法 —— 針の全長が1枚に映る代わりに、面を保つ技術が要る",
             size=11.5, ha="center")
    BX, BY, BW, BH = 60, 86, W - 120, 300
    cv.box(BX, BY, BW, BH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    ax.add_patch(Rectangle((BX + 40, BY + 34), BW - 80, BH - 68,
                           facecolor="#2b2f36", edgecolor="none", zorder=2))
    vy = BY + 200
    ax.add_patch(Rectangle((BX + 70, vy - 26), BW - 140, 52,
                           facecolor="#111417", edgecolor="#c0392b",
                           lw=2.2, zorder=3))
    cv.text(BX + 96, vy + 46, "動脈（長軸）", size=9.4, color="#e08b80",
            ha="left", z=5)
    for i, (frac, lab) in enumerate(((0.30, "A"), (0.52, "B"), (0.74, "C"))):
        x1 = BX + 70 + (BW - 140) * frac
        x0 = x1 - 240
        ax.plot([x0, x1], [vy - 92 + i * 4, vy], color="white", lw=3.4, zorder=5)
        ax.add_patch(Circle((x1, vy), 7, facecolor="#ffe680",
                            edgecolor="none", zorder=6))
        cv.text(x0 - 12, vy - 92 + i * 4, lab, size=10, color="white",
                ha="right", z=6)
    cv.text(BX + BW - 60, vy - 118, "針の全長が連続して映る", size=9.6,
            color="#8fd0c0", ha="right", z=6)
    CAPS = [
        ("利点", "#1f6b47", "針先と針体を取り違えない。後壁穿刺を避けやすい"),
        ("要求", "#b8760f", "プローブ・針・血管を同一平面に保つ。ずれると針が消える"),
        ("選び方", "#2e6da4", "優劣は一律に決まらない。針先を確実に追えるほうを選ぶ"),
    ]
    CY, CG = BY + BH + 16, 18
    CW = (W - 120 - CG * 2) / 3
    CSZ = 9.6
    nl = max(len(cv.wrap(c[2], CW - 44, CSZ)) for c in CAPS)
    CH = 62 + LH(CSZ, 1.4) * (nl - 1) + LH(CSZ, 1.0) * 0.5 + 16
    for i, (tag, col, body) in enumerate(CAPS):
        x = 60 + i * (CW + CG)
        cv.box(x, CY, CW, CH, fc="white", ec=col, lw=1.7, radius=8)
        cv.text(x + 22, CY + 26, tag, size=10.4, color=col, weight="bold",
                ha="left")
        for j, ln in enumerate(cv.wrap(body, CW - 44, CSZ)):
            cv.text(x + 22, CY + 62 + LH(CSZ, 1.4) * j, ln, size=CSZ,
                    color=INK, ha="left")
    cv.save(P("f07_long_axis.png"))


for fn in (f01, f03, f04, f05, f06, f07):  # f02 は fig14_f02.py で作り直した
    fn()
    print("ok", fn.__name__)
