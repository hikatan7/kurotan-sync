# -*- coding: utf-8 -*-
"""⑦麻酔薬理（専攻医版）・⑫BIS（要点ガイド）・アルブミン製剤ミニテキストの図 11 点を描き直す。
短縮版用：図の中に見出しは置かない（キャプションが担う）。文字は 16cm 幅で約 10〜11pt になる大きさ。
"""
import os, sys, math
KIT = (r"C:\Users\junch\OneDrive\_旧デスクトップ\教育ファイル集\麻酔科ミニ教科書シリーズ"
       r"\53_ステロイドホルモン\_生成スクリプト")
sys.path.insert(0, KIT)
import numpy as np
import figlib
from figlib import Canvas, textbox, LH, NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE, FILL
from matplotlib.patches import Circle, Wedge, Rectangle

W = 1800
L, R = 56, W - 56
OUT = os.environ.get('OUT', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'redraw', 'new'))
os.makedirs(OUT, exist_ok=True)
AMBER = "#c98a1e"


def save(cv, name):
    p = os.path.join(OUT, name)
    cv.save(p)
    import trimfig
    trimfig.trim_bottom(p)
    return p


def down(cv, x, y0, y1, color="#5b6675"):
    cv.arrow((x, y0 + 4), (x, y1 - 4), color=color, lw=2.6, head=20)


def right(cv, x0, x1, y, color="#5b6675"):
    cv.arrow((x0 + 4, y), (x1 - 4, y), color=color, lw=2.6, head=20)


def header(cv, x, y, w, h, s, color, size=17):
    cv.box(x, y, w, h, fc=color, ec=color, lw=0, radius=7)
    cv.text(x + w / 2, y + h / 2, s, size=size, color="white", weight="bold")


def listbox(cv, x, y, w, lines, size, style="grey", title=None, ts=None, bullet=True, pad=30):
    """左揃えの箇条を枠に入れる。長い行は折り返す。返り値は高さ。"""
    ts = ts or size + 1.5
    col = FILL.get(style, FILL["grey"])[1]
    out = []
    for ln in lines:
        cont = ln.startswith("　")
        ln = ln.lstrip("　")
        ws = cv.wrap(ln, w - 2 * pad - (30 if bullet else 0), size)
        first = ("" if (cont or not bullet) else "・") + ws[0]
        out += [(first, 30 if (cont and bullet) else 0)] + [(s_, 30 if bullet else 0) for s_ in ws[1:]]
    lh = LH(size, 1.55)
    th = LH(ts, 1.5) if title else 0
    h = 22 * 2 + th + lh * len(out)
    cv.box(x, y, w, h, style=style)
    yy = y + 22
    if title:
        cv.text(x + w / 2, yy + th / 2, title, size=ts, color=col, weight="bold")
        yy += th
    for i, (s_, ind) in enumerate(out):
        cv.text(x + pad + ind, yy + lh * (i + 0.5), s_, size=size, color=INK, ha="left")
    return h


# ---------------------------------------------------------------- ⑦
def p07_1():
    """全身麻酔の4本柱"""
    cv = Canvas(W, 1500)
    tw, th = 640, 96
    tx = (W - tw) / 2
    header(cv, tx, 30, tw, th, "全身麻酔", NAVY, size=22)
    items = [("① 鎮静・催眠", BLUE, "blue", ["「意識をなくす」", "プロポフォール", "セボフルラン", "デスフルラン", "レミマゾラム"]),
             ("② 鎮痛", RED, "red", ["「痛みを取る」", "レミフェンタニル", "フェンタニル", "モルヒネ", "（＋区域麻酔）"]),
             ("③ 筋弛緩", GREEN, "green", ["「術野をつくる」", "ロクロニウム", "ベクロニウム", "スキサメトニウム", "拮抗：スガマデクス"]),
             ("④ 自律神経管理", AMBER, "amber", ["「生体を守る」", "循環作動薬", "輸液・輸血", "体温・換気管理"])]
    gap = 24
    bw = (R - L - 3 * gap) / 4
    y = 250
    for i, (t, c, st, lines) in enumerate(items):
        x = L + i * (bw + gap)
        cv.arrow((W / 2, 30 + th + 6), (x + bw / 2, y - 6), color=c, lw=2.6, head=20)
        header(cv, x, y, bw, 84, t, c, size=18)
    y2 = y + 96
    hs = [textbox(cv, L + i * (bw + gap), y2, bw, it[3], 16.5, style=it[2], min_h=330, fc="white", dry=True)
          for i, it in enumerate(items)]
    for i, it in enumerate(items):
        textbox(cv, L + i * (bw + gap), y2, bw, it[3], 16.5, style=it[2], min_h=max(hs), fc="white")
    y3 = y2 + max(hs) + 40
    textbox(cv, L, y3, R - L, ["この4つが揃ってはじめて「全身麻酔」 ── 麻酔は“眠らせる”ことではない"],
            17.5, style="amber", weight="bold", pad_y=26)
    return save(cv, "07_f1_four_pillars.png")


def p07_2():
    """CSHT"""
    import matplotlib.pyplot as plt
    from scipy.interpolate import PchipInterpolator
    hrs = [0, 0.5, 1, 2, 3, 4, 5, 6, 8, 10]
    data = [
        ("レミフェンタニル", RED, [0, 3, 3.5, 3.7, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8]),
        ("プロポフォール", BLUE, [0, 6, 8, 12, 16, 19, 22, 24, 28, 32]),
        ("レミマゾラム", PURPLE, [0, 6, 7, 8, 9, 10, 10.5, 11, 12, 13]),
        ("スフェンタニル", "#0e8a8a", [0, 14, 20, 28, 32, 34, 34.5, 35, 35, 35]),
        ("フェンタニル", "#d39200", [0, 22, 45, 100, 170, 230, 260, 280, 300, 310]),
        ("ミダゾラム", GREEN, [0, 20, 35, 55, 70, 80, 88, 95, 105, 115]),
    ]
    plt.rcParams["font.family"] = figlib.JP
    fig, ax = plt.subplots(figsize=(9, 5.9), dpi=200)
    t = np.linspace(0, 10, 400)
    for name, c, v in data:
        ax.plot(t, PchipInterpolator(hrs, v)(t), color=c, lw=3.4, label=name)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 330)
    ax.set_xlabel("持続投与時間（時間）", fontsize=16)
    ax.set_ylabel("CSHT（分）", fontsize=16)
    ax.tick_params(labelsize=15)
    ax.grid(color="#e3e7ec", lw=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=14.5, ncol=2, loc="upper left", frameon=True, framealpha=0.95,
              handlelength=1.6, columnspacing=1.2)
    ax.annotate("フェンタニルは\n時間とともに急峻に延長", xy=(6, 280), xytext=(6.3, 175),
                fontsize=15, color="#b07800", weight="bold",
                arrowprops=dict(arrowstyle="->", color="#b07800", lw=2))
    ax.annotate("レミフェンタニルは\nほぼ一定（約3〜4分）", xy=(8, 5), xytext=(5.6, 52),
                fontsize=15, color=RED, weight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    fig.tight_layout()
    p = os.path.join(OUT, "07_f2_csht.png")
    fig.savefig(p, dpi=200, facecolor="white")
    plt.close(fig)
    return p


def p07_3():
    """デクスメデトミジンの機序"""
    cv = Canvas(W, 1300)
    gap = 70
    bw = (R - L - 2 * gap) / 3
    x1, x2, x3 = L, L + bw + gap, L + 2 * (bw + gap)
    s = 16.5
    y = 30
    h1 = textbox(cv, x1, y, bw, ["デクスメデトミジン"], 18, style="amber", fc="#d98e2b", color="white",
                 weight="bold", pad_y=24)
    ya = y + h1 + 46
    h2 = textbox(cv, x1, ya, bw, ["青斑核（LC）の", "α₂受容体を刺激"], s, style="amber", min_h=160)
    yb = ya + h2 + 46
    h3 = textbox(cv, x1, yb, bw, ["ノルアドレナリン", "放出が減少"], s, style="amber", min_h=160)
    down(cv, x1 + bw / 2, y + h1, ya)
    down(cv, x1 + bw / 2, ya + h2, yb)
    textbox(cv, x2, yb, bw, ["VLPO（腹外側視索前野）", "の脱抑制"], s, style="green", min_h=160)
    right(cv, x1 + bw, x2, yb + 80)
    textbox(cv, x2, ya, bw, ["GABA・ガラニンが", "覚醒系を抑制"], s, style="green", min_h=160)
    cv.arrow((x2 + bw / 2, yb - 4), (x2 + bw / 2, ya + 160 + 4), color="#5b6675", lw=2.6, head=20)
    hr = textbox(cv, x3, ya - 40, bw, ["ノンレム睡眠 stage 2", "に酷似した鎮静", "", "呼びかけで覚醒 → 会話可",
                                       "呼吸ドライブは保たれる"], s, style="blue")
    right(cv, x2 + bw, x3, ya + 80)
    y4 = yb + 160 + 50
    textbox(cv, L, y4, R - L, ["GABA-A 受容体を直接叩かない ＝ 皮質を“麻痺”させない。",
                               "これが cooperative sedation と、せん妄リスク低減の背景である。"], 16.5, style="grey", pad_y=20)
    return save(cv, "07_f3_dexmedetomidine.png")


def _nmj(cv, x, w, top, label, lcolor, blocked):
    cv.text(x + w / 2, top, label, size=17, color=lcolor, weight="bold")
    ny = top + 50
    cv.box(x, ny, w, 200, style="blue")
    cv.text(x + w / 2, ny + 40, "運動神経終末", size=16, color=BLUE)
    rng = np.random.RandomState(3 if blocked else 1)
    for k in range(7):
        cx = x + 80 + k * (w - 160) / 6 + rng.uniform(-15, 15)
        cy = ny + 120 + rng.uniform(-30, 30)
        cv.ax.add_patch(Circle((cx, cy), 13, fc="white", ec=BLUE, lw=2, zorder=4))
    my = ny + 200 + 150
    cv.box(x, my, w, 200, style="green")
    cv.text(x + w / 2, my + 130, "筋終板（ニコチン性 ACh 受容体）", size=16, color=GREEN)
    n = 5
    for k in range(n):
        rx = x + 70 + k * (w - 140 - 60) / (n - 1)
        cv.rect(rx, my - 34, 60, 64, fc="white", ec=GREEN, lw=2.2, z=4)
        if blocked:
            cv.rect(rx - 8, my - 82, 76, 52, fc=RED, z=5)
        else:
            cv.ax.add_patch(Circle((rx + 30, my - 58), 26, fc=BLUE, ec="none", zorder=5))
            cv.arrow((rx + 30, ny + 216), (rx + 30, my - 92), color=BLUE, lw=2.2, head=16)
    return my + 200


def p07_4():
    """神経筋接合部"""
    cv = Canvas(W, 1400)
    gap = 70
    w = (R - L - gap) / 2
    b1 = _nmj(cv, L, w, 40, "① 正常：ACh が受容体に結合", GREEN, False)
    _nmj(cv, L + w + gap, w, 40, "② 非脱分極性筋弛緩薬（ロクロニウム）", RED, True)
    y = b1 + 30
    h1 = textbox(cv, L, y, w, ["ACh 2分子が結合 → チャネル開口", "→ Na⁺ 流入 → 終板電位", "→ 筋収縮"],
                 16, style="green", fc="white")
    h2 = textbox(cv, L + w + gap, y, w, ["受容体を“占拠するだけ”で開口させない", "（競合的拮抗）", "→ 終板電位が閾値に届かない → 弛緩"],
                 16, style="red", fc="white")
    y2 = y + max(h1, h2) + 30
    textbox(cv, L, y2, R - L, ["受容体の 70〜75% が占拠されて初めて筋力低下が現れ、", "90% 以上で完全遮断 ── これが“安全域”の正体。"],
            16, style="grey", pad_y=18)
    return save(cv, "07_f4_nmj.png")


def _ring(cv, cx, cy, r0, r1, core=None):
    for k in range(8):
        a0 = k * 45 + 3
        cv.ax.add_patch(Wedge((cx, cy), r1, a0, a0 + 39, width=r1 - r0, fc=PURPLE, ec="none", zorder=4))
    if core:
        cv.ax.add_patch(Circle((cx, cy), r0 - 16, fc=core, ec="none", zorder=5))


def p07_5():
    """スガマデクス"""
    cv = Canvas(W, 1200)
    cy = 230
    # 左：NMJ の中のロクロニウム
    bx, bw, bh = L, 470, 330
    cv.box(bx, cy - bh / 2, bw, bh, style="green")
    cv.text(bx + bw / 2, cy - bh / 2 + 36, "神経筋接合部", size=16, color=GREEN)
    for dx, dy in [(-80, -10), (40, -40), (-120, 80), (60, 70)]:
        cv.ax.add_patch(Circle((bx + bw / 2 + dx, cy + dy + 20), 28, fc=RED, ec="none", zorder=5))
    _ring(cv, 860, cy, 70, 128)
    _ring(cv, 1440, cy, 70, 128, core=RED)
    right(cv, bx + bw + 20, 860 - 150, cy)
    right(cv, 860 + 150, 1440 - 150, cy)
    cv.text(1150, cy - 36, "捕捉", size=17, weight="bold")
    ty = cy + 190
    cv.block(bx, ty, bw, ["ロクロニウムが", "受容体を占拠中"], 16.5, color=RED)
    cv.block(860 - 240, ty, 480, ["スガマデクス", "（γ-シクロデキストリン）", "内側が疎水性", "外側が親水性"], 16.5, color=PURPLE)
    cv.block(1440 - 260, ty, 520, ["1：1 の包接複合体", "血中に閉じ込め", "→ 腎から排泄", "数分で TOF 比 0.9 以上"], 16.5, color=GREEN)
    y2 = ty + LH(16.5) * 4 + 50
    textbox(cv, L, y2, R - L, ["ネオスチグミンは“ACh を増やして押し勝つ” ＝ 深い遮断では効かず、天井がある。",
                               "スガマデクスは“遮断薬を消す” ＝ 深い遮断でも拮抗できる。"], 16.5, style="grey", pad_y=20)
    return save(cv, "07_f5_sugammadex.png")


# ---------------------------------------------------------------- ⑫
def p12_1():
    """BIS の 4 点セット"""
    cv = Canvas(W, 1400)
    tw = 560
    header(cv, (W - tw) / 2, 30, tw, 96, "BIS の数字", NAVY, size=21)
    items = [("SQI", ["信号品質（0〜100）", "この数字を", "信じてよいか", "低ければ何も", "言えない"]),
             ("EMG", ["筋電図の混入", "高いと BIS は", "高めに出る"]),
             ("SR", ["平坦区間の割合", "0% でなければ", "深すぎる"]),
             ("raw EEG", ["実際の波形", "最終的な判断は", "ここでする"])]
    gap = 22
    bw = (R - L - 3 * gap) / 4
    y = 220
    hs = []
    for i, (t, lines) in enumerate(items):
        x = L + i * (bw + gap)
        cv.arrow((W / 2, 130), (x + bw / 2, y - 6), color="#8d9bb3", lw=2.6, head=20)
        hs.append(textbox(cv, x, y, bw, lines, 16.5, style="navy", title=t, title_size=20, dry=True))
    for i, (t, lines) in enumerate(items):
        textbox(cv, L + i * (bw + gap), y, bw, lines, 16.5, style="navy", title=t, title_size=20, min_h=max(hs))
    y2 = y + max(hs) + 40
    h = textbox(cv, L, y2, R - L, ["この4つが揃って初めて「麻酔深度の評価」になる。",
                                   "BIS 単独での判断は、血圧計のホースを見ずに数字だけ読むのと同じ。"],
                17.5, style="amber", weight="bold", pad_y=22)
    y3 = y2 + h + 30
    h = textbox(cv, L, y3, R - L, ["① SQI で信用度を決める → ② EMG で偽高値を除く",
                                   "→ ③ SR で深すぎを除く → ④ raw EEG で確定する"],
                17, style="navy", title="読む順番", title_size=17.5)
    y4 = y3 + h + 24
    cv.text(L, y4 + 20, "※ ①②を飛ばして③④に行くと、アーチファクトを「所見」として読んでしまう。",
            size=15.5, color=GREY, ha="left")
    return save(cv, "12_f1_four_points.png")


def p12_2():
    """BIS が下がったときに踏む順番"""
    cv = Canvas(W, 2200)
    cw = 740
    cx = (W - cw) / 2 - 60
    s = 17
    y = 30
    h = textbox(cv, cx, y, cw, ["BIS が 40 を下回った"], 18.5, fc=NAVY, ec=NAVY, color="white", weight="bold", pad_y=22)
    y1 = y + h + 50
    down(cv, (cx + cw / 2), y + h, y1)
    h1 = textbox(cv, cx, y1, cw, ["① SQI は良好か（≧50）"], s, style="navy", weight="bold", pad_y=20)
    # いいえ → 右
    nx = cx + cw + 120
    textbox(cv, nx, y1 - 10, R - nx, ["電極・接触を確認", "判断を保留"], 15, style="red", weight="bold")
    right(cv, cx + cw, nx, y1 + h1 / 2, color=RED)
    cv.text(cx + cw + 52, y1 + h1 / 2 + 28, "いいえ", size=14, color=RED, weight="bold")
    y2 = y1 + h1 + 56
    down(cv, (cx + cw / 2), y1 + h1, y2)
    cv.text((cx + cw / 2) + 16, (y1 + h1 + y2) / 2, "はい", size=15, color=GREEN, weight="bold", ha="left")
    h2 = textbox(cv, cx, y2, cw, ["② EMG は高くないか"], s, style="navy", weight="bold", pad_y=20)
    y3 = y2 + h2 + 80
    down(cv, (cx + cw / 2), y2 + h2, y3)
    cv.text((cx + cw / 2) + 16, (y2 + h2 + y3) / 2, "高ければ偽高値の可能性（低値では逆に稀）", size=15, color=GREY, ha="left")
    h3 = textbox(cv, cx, y3, cw, ["③ raw EEG を見る"], s, style="navy", weight="bold", pad_y=20)
    # 分岐
    bw = 700
    lx, rx = L + 10, R - 10 - bw
    y4 = y3 + h3 + 70
    cv.arrow(((cx + cw / 2) - 120, y3 + h3 + 4), (lx + bw / 2, y4 - 4), color="#5b6675", lw=2.6, head=20)
    cv.arrow(((cx + cw / 2) + 120, y3 + h3 + 4), (rx + bw / 2, y4 - 4), color="#5b6675", lw=2.6, head=20)
    ha = textbox(cv, lx, y4, bw, ["continuous slow wave", "（連続した徐波）"], s, style="green", weight="bold")
    textbox(cv, rx, y4, bw, ["burst suppression", "（平坦が混じる）"], s, style="red", weight="bold")
    y5 = y4 + ha + 50
    down(cv, lx + bw / 2, y4 + ha, y5)
    down(cv, rx + bw / 2, y4 + ha, y5)
    hb = textbox(cv, lx, y5, bw, ["深麻酔として妥当か", "手術侵襲・薬剤量を評価"], 16.5, fc="white", ec=NAVY)
    textbox(cv, rx, y5, bw, ["SR と持続時間を読む", "（累積が効く）"], 16.5, fc="white", ec=NAVY)
    y6 = y5 + hb + 70
    cv.arrow((lx + bw / 2, y5 + hb + 4), (cx + 60, y6 - 4), color="#5b6675", lw=2.6, head=20)
    cv.arrow((rx + bw / 2, y5 + hb + 4), (cx + cw - 60, y6 - 4), color="#5b6675", lw=2.6, head=20)
    h6 = textbox(cv, cx, y6, cw, ["④ 患者背景を確認", "高齢・低体温・低血圧・低灌流"], s, style="amber", weight="bold")
    y7 = y6 + h6 + 50
    down(cv, (cx + cw / 2), y6 + h6, y7)
    textbox(cv, cx, y7, cw, ["⑤ 麻酔薬を減らす／", "循環・体温を是正する"], 18, fc=NAVY, ec=NAVY, color="white", weight="bold")
    return save(cv, "12_f2_bis_low_steps.png")


def _eeg(kind, n=4000, seed=0):
    rng = np.random.RandomState(seed)
    t = np.linspace(0, 10, n)

    def noise(a, k=3):
        return np.convolve(rng.randn(n), np.ones(k) / k, mode="same") * a

    if kind == 0:      # 覚醒：低振幅・高周波
        y = noise(0.30, 2)
    elif kind == 1:    # 鎮静：β〜α
        y = noise(0.30, 3) + 0.28 * np.sin(2 * np.pi * 11 * t + rng.rand()) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.4 * t))
    elif kind == 2:    # 全身麻酔：α紡錘＋slow-delta
        env = 0.45 + 0.55 * np.sin(2 * np.pi * 0.8 * t + 0.3) ** 2
        y = 0.5 * np.sin(2 * np.pi * 0.9 * t) + 0.42 * env * np.sin(2 * np.pi * 10 * t) + noise(0.06)
    elif kind == 3:    # 深い催眠：大振幅 delta（不規則）
        y = 0.75 * np.sin(2 * np.pi * 0.9 * t + 0.6 * np.sin(2 * np.pi * 0.23 * t))             + 0.25 * np.sin(2 * np.pi * 1.7 * t + 1.0) + noise(0.05, 5)
    elif kind == 4:    # burst suppression
        y = noise(0.02)
        for c in (0.7, 3.2, 6.6, 9.1):
            m = np.exp(-((t - c) / 0.2) ** 2)
            y = y + 0.9 * m * np.sin(2 * np.pi * 7 * (t - c)) + 0.3 * m * np.sin(2 * np.pi * 2 * (t - c))
    else:              # 平坦
        y = noise(0.02)
    return t, y


def p12_3():
    """麻酔深度と frontal EEG"""
    rows = [("覚醒（開眼・会話）", "BIS 95 前後", "β優位・低振幅／高周波"),
            ("鎮静（呼びかけに反応）", "BIS 70〜85", "β〜α が混在、振幅がやや増える"),
            ("全身麻酔（手術可能）", "BIS 40〜60", "前頭部α紡錘＋slow-delta（＝麻酔の指紋）"),
            ("深い催眠", "BIS 30 前後", "大振幅の slow-delta 優位、α は消退"),
            ("burst suppression", "BIS 10〜25", "burst と平坦（suppression）の交代"),
            ("ほぼ電気的無活動", "BIS 0〜5", "平坦。SR が 100% に近づく")]
    hh, th, gap = 52, 150, 30
    cv = Canvas(W, 30 + len(rows) * (hh + th + gap) + 160)
    for i, (lab, bis, desc) in enumerate(rows):
        y = 30 + i * (hh + th + gap)
        cv.text(L, y + hh / 2, lab, size=17, color=NAVY, weight="bold", ha="left")
        x2 = L + cv.width(lab, 17, "bold") + 28
        cv.text(x2, y + hh / 2, bis, size=17, color=RED, weight="bold", ha="left")
        cv.text(R, y + hh / 2, desc, size=15.5, color=INK, ha="right")
        ty = y + hh
        cv.rect(L, ty, R - L, th, fc="#f7f9fc", ec="#cfd6e0", lw=1.2)
        t, v = _eeg(i, seed=i + 1)
        cv.ax.plot(L + t / 10 * (R - L), ty + th / 2 - v * th * 0.40, color=NAVY, lw=1.4, zorder=4)
    yb = 30 + len(rows) * (hh + th + gap)
    cv.block(L, yb, R - L, ["※ 10 秒間の模式図。縦軸は同一スケール。",
                            "BIS 値は目安であり、同じ波形でも年齢・薬剤で数値は動く。"], 15, color=GREY, ha="left")
    return save(cv, "12_f3_eeg_depth.png")


# ---------------------------------------------------------------- アルブミン
def pal_1():
    """凝固カスケード（従来図）"""
    cv = Canvas(W, 3000)
    gap = 40
    cw = (R - L - gap) / 2
    xl, xr = L, L + cw + gap
    s = 16
    header(cv, xl, 30, cw, 76, "内因系（接触相）", NAVY, size=18)
    header(cv, xr, 30, cw, 76, "外因系（組織因子経路）", "#b03030", size=18)
    cv.text(xl + cw / 2, 136, "APTT が見る：内因系＋共通系", size=15.5, color=NAVY, weight="bold")
    cv.text(xr + cw / 2, 136, "PT-INR が見る：外因系＋共通系", size=15.5, color="#b03030", weight="bold")
    y = 176
    a1 = textbox(cv, xl, y, cw, ["異物・陰性荷電面との接触", "XII → XIIa"], s, style="navy", min_h=130)
    b1 = textbox(cv, xr, y, cw, ["血管損傷で組織因子（TF）が露出", "TF ＋ VII → VIIa"], s, style="navy", min_h=130)
    y2 = y + 130 + 46
    down(cv, xl + cw / 2, y + 130, y2, NAVY)
    down(cv, xr + cw / 2, y + 130, y2, NAVY)
    textbox(cv, xl, y2, cw, ["XI → XIa"], 17, style="navy", weight="bold", min_h=100)
    textbox(cv, xr, y2, cw, ["TF ＋ VIIa ＋ Ca²⁺ ＋ リン脂質", "＝ 外因系テナーゼ"], 16.5, style="red", weight="bold", min_h=246)
    y3 = y2 + 100 + 46
    down(cv, xl + cw / 2, y2 + 100, y3, NAVY)
    textbox(cv, xl, y3, cw, ["IX → IXa", "IXa ＋ VIIIa ＋ Ca²⁺ ＋ リン脂質", "＝ 内因系テナーゼ"], 16.5, style="navy", weight="bold", min_h=0)
    h3 = textbox(cv, xl, y3, cw, ["IX → IXa", "IXa ＋ VIIIa ＋ Ca²⁺ ＋ リン脂質", "＝ 内因系テナーゼ"], 16.5, style="navy", weight="bold", dry=True)
    yc = y3 + h3 + 80
    cv.text(R, yc - 30, "共通系", size=17, color=NAVY, weight="bold", ha="right")
    cv.arrow((xl + cw / 2, y3 + h3 + 4), (W / 2 - 120, yc - 4), color=NAVY, lw=2.6, head=20)
    cv.arrow((xr + cw / 2, y2 + 246 + 4), (W / 2 + 120, yc - 4), color=NAVY, lw=2.6, head=20)
    fx = L
    fw = R - fx
    common = [(["X → Xa"], "navy", 17.5), (["Xa ＋ Va ＋ Ca²⁺ ＋ リン脂質 ＝ プロトロンビナーゼ"], "navy", 16.5),
              (["プロトロンビン（II） → トロンビン（IIa）"], "amber", 17.5),
              (["フィブリノゲン（I） → フィブリン（Ia）", "XIII → XIIIa が架橋し、安定化フィブリン網になる"], "green", 16.5)]
    yy = yc
    ythr = None
    for i, (ls, st, sz) in enumerate(common):
        h = textbox(cv, fx, yy, fw, ls, sz, style=st, weight="bold", pad_y=20)
        if i == 2:
            ythr = yy + h / 2
        if i < len(common) - 1:
            down(cv, fx + fw / 2, yy + h, yy + h + 40, NAVY)
            yy += h + 40
        else:
            yy += h
    yy += 24
    h = textbox(cv, fx, yy, fw, ["正のフィードバック：トロンビンが V・VIII・XI・XIII と血小板を活性化し、反応を加速する"],
                15.5, style="amber", pad_y=14)
    yy += h
    # 薬
    yd = yy + 60
    header(cv, L, yd, R - L, 70, "薬は、この図のどこを止めているか", "#4a5563", size=18)
    drugs = [("ワルファリン", "purple", ["ビタミン K 依存性因子（II・VII・IX・X）", "とプロテイン C/S の産生を落とす", "→ PT-INR で追う"]),
             ("ヘパリン（アンチトロンビン依存）", "green", ["AT を介して Xa と IIa を阻害", "→ APTT・抗 Xa 活性で追う"]),
             ("DOAC", "navy", ["直接 Xa 阻害（〜キサバン）", "直接 IIa 阻害（ダビガトラン）", "→ PT・APTT では効果を測れない"]),
             ("抗血小板薬（アスピリン等）", "red", ["止めているのは血小板の足場づくり", "→ PT・APTT・血小板数に表れない"]),
             ("トラネキサム酸", "amber", ["プラスミンによる線溶を阻害", "→ 図の一番下、血栓を守る薬"]),
             ("この図で見えないもの", "grey", ["血小板の数と機能（一次止血）", "フィブリンの重合強度（FIBTEM）",
                                          "線溶の亢進／体温・pH・イオン化 Ca", "第 XIII 因子（PT・APTT は正常）"])]
    g = 24
    dw = (R - L - g) / 2
    y = yd + 70 + 24
    for r in range(3):
        pair = drugs[2 * r:2 * r + 2]
        hs = [textbox(cv, 0, 0, dw, it[2], 15.5, style=it[1], title=it[0], title_size=17, dry=True) for it in pair]
        for c, it in enumerate(pair):
            textbox(cv, L + c * (dw + g), y, dw, it[2], 15.5, style=it[1], title=it[0], title_size=17, min_h=max(hs))
        y += max(hs) + g
    return save(cv, "alb_f1_cascade.png")


def pal_2():
    """cell-based model"""
    cv = Canvas(W, 2600)
    gap = 44
    cw = (R - L - 2 * gap) / 3
    s = 16
    stages = [("① Initiation 開始", ["TF 発現細胞の上で", "「スイッチが入る」"],
               [(["組織因子（TF）が", "血流に露出"], "red", False), (["TF–VIIa 複合体", "（外因系テナーゼ）"], "navy", True),
                (["X → Xa　 IX → IXa"], "navy", False), (["ごく少量のトロンビン", "（fibrin はまだ作れない）"], "amber", True)],
               ["TF 発現細胞", "（線維芽細胞・血管外膜）"]),
              ("② Amplification 増幅", ["少量トロンビンが", "足場と補酵素を用意する"],
               [(["少量トロンビンが", "「点火」する"], "amber", False), (["血小板を活性化", "→ 膜リン脂質を露出"], "navy", False),
                (["V → Va", "VIII → VIIIa", "（vWF から遊離）"], "navy", False), (["XI → XIa", "（内因系ループを回す）"], "navy", False)],
               ["血小板", "（活性化しはじめる）"]),
              ("③ Propagation 伝播", ["活性化血小板の上で", "thrombin burst"],
               [(["IXa–VIIIa", "（内因系テナーゼ）", "が Xa を大量に作る"], "navy", True), (["Xa–Va", "（プロトロンビナーゼ）"], "navy", True),
                (["thrombin burst", "（爆発的産生）"], "amber", True), (["フィブリノゲン", "→ フィブリン", "XIIIa が架橋して", "血栓が固まる"], "green", True)],
               ["活性化血小板の膜", "（リン脂質の足場）"])]
    tops, bottoms = [], []
    for i, (t, sub, chain, place) in enumerate(stages):
        x = L + i * (cw + gap)
        cv.text(x + cw / 2, 46, t, size=18, color=NAVY, weight="bold")
        cv.block(x, 76, cw, sub, 15.5, color=GREY)
        y = 76 + LH(15.5) * len(sub) + 16
        tops.append(y)
        for k, (ls, st, bd) in enumerate(chain):
            h = textbox(cv, x, y, cw, ls, s, style=st, weight="bold" if bd else "normal", pad_y=14)
            if k < len(chain) - 1:
                down(cv, x + cw / 2, y + h, y + h + 32, NAVY)
                y += h + 32
            else:
                y += h
        bottoms.append(y)
    yb = max(bottoms) + 56
    for i, (t, sub, chain, place) in enumerate(stages):
        x = L + i * (cw + gap)
        down(cv, x + cw / 2, bottoms[i], yb, NAVY)
        textbox(cv, x, yb, cw, place, 15.5, style="grey", pad_y=12)
        if i < 2:
            right(cv, x + cw + 2, x + cw + gap - 2, (tops[i] + bottoms[i]) / 2, NAVY)
    return save(cv, "alb_f2_cell_based.png")


def pal_3():
    """危機的出血の管理"""
    cv = Canvas(W, 3800)
    s = 16
    y = 30
    h = textbox(cv, L, y, R - L, ["危機的出血の認識 ── 出血速度、循環不全、外科的止血が追いつかない、輸血が続く",
                                  "→ 大量輸血プロトコル（MTP）起動・輸血部へ連絡・O 型／未交差血の要否を判断"],
                s, style="red", weight="bold", pad_y=20)
    y2 = y + h + 46
    down(cv, W / 2, y + h, y2, RED)
    h = listbox(cv, L, y2, R - L, ["RBC：FFP：PLT ≒ 1：1：1",
                                   "FFP/RBC ≧ 0.5 は最低ライン（心臓血管外科・産科は ≧ 1 を意識）",
                                   "FFP は 1 ラウンド 15〜20 mL/kg を RBC と同速で",
                                   "　（60〜70 kg なら約 1,000〜1,400 mL ＝ 8〜12 単位）"],
                s, style="blue", title="第1相　ratio-based（検査が返るまでの数十分）")
    y3 = y2 + h + 46
    down(cv, W / 2, y2 + h, y3, NAVY)
    h = listbox(cv, L, y3, R - L, ["フィブリノゲン・血算・PT-INR/APTT・イオン化 Ca・乳酸・血液ガス・",
                                   "VET（ROTEM/TEG）が返ったら、ratio-based から goal-directed へ切り替える"],
                s, style="amber", title="第2相　検査が返る", bullet=False)
    y4 = y3 + h + 66
    items = [("フィブリノゲン", ["Fbg ＜ 150 mg/dL（産科 ＜ 200）", "FIBTEM A5 ＜ 10 mm"],
              ["濃縮製剤 50 mg/kg（3〜4 g）", "またはクリオ／FFP"]),
             ("血小板", ["Plt ＜ 5万/μL（頭蓋内外傷 ＜ 10万）", "EXTEM A5 ＜ 35 mm"],
              ["濃厚血小板 10〜20 単位", "投与後 30〜60 分で再評価"]),
             ("凝固開始能", ["PT-INR ＞ 1.5・EXTEM CT 延長", "（Fbg・Plt を補ってなお）"],
              ["FFP 10〜15 mL/kg を追加", "（V・XI 欠乏は FFP が主役）"]),
             ("線溶", ["ML ＞ 15%・EXTEM/APTEM の乖離", "臨床的に oozing"],
              ["トラネキサム酸を追加", "線溶亢進型 DIC を疑う"])]
    g = 30
    bw = (R - L - g) / 2
    cv.text(W / 2, y4 - 30, "goal-directed：軸ごとに足りないものを補う", size=17, color=NAVY, weight="bold")
    y4 += 16
    hh = 70
    hc = max(textbox(cv, 0, 0, bw, it[1], 16, dry=True) for it in items)
    ha = max(textbox(cv, 0, 0, bw, it[2], 16, dry=True, weight="bold") for it in items)
    cell = hh + hc + ha
    for i, (t, crit, act) in enumerate(items):
        x = L + (i % 2) * (bw + g)
        yy = y4 + (i // 2) * (cell + g)
        header(cv, x, yy, bw, hh, t, NAVY, size=18.5)
        textbox(cv, x, yy + hh, bw, crit, 16, fc="white", ec=NAVY, min_h=hc, radius=2)
        textbox(cv, x, yy + hh + hc, bw, act, 16, style="navy", weight="bold", min_h=ha, radius=2)
    y5 = y4 + 2 * cell + g + 44
    down(cv, W / 2, y5 - 44, y5, NAVY)
    g2 = 30
    hw = (R - L - g2) / 2
    h1 = listbox(cv, L, y5, hw, ["15〜30 分ごと、または",
                                 "　製剤 1 ラウンドごとに見直す",
                                 "見るもの：出血速度・術野・",
                                 "　VET・Fbg・イオン化 Ca・体温",
                                 "止血できたら「走らせるのを",
                                 "　やめる」判断も同じ重さで",
                                 "ICU へ引き継ぐ：血液型・抗体・",
                                 "　緊急放出血・最終採血時刻"],
                 15.5, style="green", title="再評価", pad=22)
    listbox(cv, L + hw + g2, y5, hw, ["外科的止血・IVR・産科的介入",
                                      "深部体温 ≧ 36℃（最低 35℃）",
                                      "pH ≧ 7.2（アシドーシスの是正）",
                                      "イオン化 Ca ≧ 1.0〜1.1 mmol/L",
                                      "　（総 Ca ではなく実測で）",
                                      "トラネキサム酸 1 g/10 分 → 1 g/8 時間",
                                      "　（受傷・発症 3 時間以内に開始）"],
            15.5, style="red", title="常に並行して走らせる", pad=22)
    return save(cv, "alb_f3_mtp.png")


if __name__ == "__main__":
    import figqa
    names = sys.argv[1:] or [n for n in dir() if n[:1] == "p" and n[1:3] in ("07", "12", "al")]
    for n in sorted(names):
        p = globals()[n]()
        print(n, os.path.basename(p))
    for name, iss in figqa.report:
        print("QA", name, iss[:4])
