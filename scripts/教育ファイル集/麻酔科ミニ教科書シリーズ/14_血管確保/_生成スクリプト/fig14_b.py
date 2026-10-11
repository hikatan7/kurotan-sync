# -*- coding: utf-8 -*-
"""第14巻 血管確保 図版 f08〜f14"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyArrowPatch
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f08
def f08():
    W, H = 1520, 500
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "圧モニタ回路 —— 穿刺の前に組み立て、気泡を抜いておく",
             size=12.5, ha="center")
    ITEMS = [
        ("加圧バッグ", "#e9f0fa", "#2e6da4",
         ["生理食塩液を 300 mmHg に加圧", "持続灌流で凝血を防ぐ"]),
        ("耐圧チューブ", "#eaf4ee", "#1f6b47",
         ["短く・硬く・気泡なし", "延長するほど共振しやすい"]),
        ("トランスデューサ", "#fdf1e0", "#b8760f",
         ["右心房位＝第4肋間×中腋窩線", "大気開放でゼロ点校正"]),
        ("カテーテル", "#fbeeee", "#c0392b",
         ["成人は 20 G が標準", "細血管では 22 G を検討"]),
    ]
    L, R = 44, W - 44
    GAP = 16
    CW = (R - L - GAP * 3) / 4
    TOP, BSZ = 100, 9.8
    nl = max(sum(len(cv.wrap(ln, CW - 34, BSZ)) for ln in it[3]) for it in ITEMS)
    CH = 84 + LH(BSZ, 1.5) * (nl - 1) + LH(BSZ, 1.0) * 0.5 + 22
    for i, (head, fc, ec, lines) in enumerate(ITEMS):
        x = L + i * (CW + GAP)
        cv.box(x, TOP, CW, CH, fc=fc, ec=ec, lw=1.8, radius=8)
        cv.text(x + CW / 2, TOP + 40, head, size=11.2, color=ec, weight="bold")
        k = 0
        for ln in lines:
            for s in cv.wrap(ln, CW - 34, BSZ):
                cv.text(x + CW / 2, TOP + 84 + LH(BSZ, 1.5) * k, s,
                        size=BSZ, color=INK)
                k += 1
        if i < 3:
            cv.arrow((x + CW + 2, TOP + CH / 2), (x + CW + GAP - 2, TOP + CH / 2),
                     color="#8d97a3", lw=2.0, head=9)
    MSG = "挿入後に波形を得てから準備を始めると、必ずどこかで手戻りが起きる"
    by = TOP + CH + 28
    msz = cv.fit_size([MSG], R - L - 60, 11.5, weight="bold")
    bh = 30 + LH(msz, 1.5)
    cv.box(L, by, R - L, bh, fc="#e4f2f4", ec="#1f7f8b", lw=2.0, radius=8)
    cv.text(W / 2, by + bh / 2, MSG, size=msz, color="#0f6d78", weight="bold")
    cv.save(P("f08_pressure_circuit.png"))


# ---------------------------------------------------------------- f09
def f09():
    W, H, DPI = 1520, 780, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0.135, 0.25, 0.825, 0.60])
    d = np.linspace(-20, 20, 200)
    err = -d * 0.735
    ax.plot(d, err, color="#c0392b", lw=3.4)
    ax.axhline(0, color="#8d97a3", lw=1.4, ls=":")
    ax.axvline(0, color="#8d97a3", lw=1.4, ls=":")
    for dd in (-10, 10):
        ax.plot([dd], [-dd * 0.735], marker="o", ms=12, color="#c0392b", zorder=5)
    ax.annotate("心房位より 10 cm 高い\n→ 約 7.5 mmHg 低く表示",
                xy=(10, -7.35), xytext=(-19, -8), fontsize=11, color="#c0392b",
                ha="left", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.6))
    ax.annotate("心房位より 10 cm 低い\n→ 約 7.5 mmHg 高く表示",
                xy=(-10, 7.35), xytext=(2.0, 19), fontsize=11, color="#c0392b",
                ha="left", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.6))
    ax.set_xlim(-20, 20)
    ax.set_ylim(-22, 22)
    ax.set_xlabel("トランスデューサの高さ（右心房位からのずれ・cm）",
                  fontsize=12, color=INK, labelpad=10)
    ax.set_ylabel("測定値の誤差（mmHg）", fontsize=12, color=INK, labelpad=10)
    ax.set_title("高さのずれは、そのまま測定値の誤差になる", fontsize=13,
                 color="#0A1830", weight="bold", pad=16)
    ax.grid(color="#eceff2", lw=1.0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11.5, colors=INK)
    for s in ax.spines.values():
        s.set_color("#7c8894")
    for i, ln in enumerate([
            "※ 水柱 1 cmH₂O ≒ 0.735 mmHg。体位を変えたら必ずゼロ点を取り直す。",
            "　 「血圧が下がった」の前に、ベッドの高さが変わっていないかを見る。"]):
        fig.text(0.5, 0.082 - i * 0.042, ln, fontsize=9.8, color="#8d97a3",
                 ha="center", va="center")
    fig.savefig(P("f09_transducer_height.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f10
def f10():
    W, H, DPI = 1520, 700, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    fig.suptitle("スクエア波テスト —— 波形を疑う前に、回路の素性を見る",
                 fontsize=12.5, color="#0A1830", fontweight="bold", y=0.955)
    t = np.linspace(0, 1.6, 1200)
    CASES = [
        ("適正", "#1f6b47", 2, 26,
         ["1〜2 回の小さな振動のあと", "すみやかに基線へ戻る"],
         ["そのまま使ってよい"]),
        ("過減衰（over-damped）", "#b8760f", 0, 8,
         ["振動がなく", "なだらかに基線へ戻る"],
         ["気泡・屈曲・血栓・加圧不足", "収縮期血圧は低く出る"]),
        ("過小減衰（under-damped）", "#c0392b", 6, 60,
         ["振動が3回以上続く", ""],
         ["チューブが長い・軟らかい・共振", "収縮期血圧は高く出る"]),
    ]
    for i, (name, col, nosc, damp, desc, mean) in enumerate(CASES):
        ax = fig.add_axes([0.085 + i * 0.312, 0.455, 0.255, 0.375])
        y = np.zeros_like(t)
        y[t < 0.35] = 1.0
        m = t >= 0.35
        tt = t[m] - 0.35
        if nosc == 0:
            y[m] = np.exp(-tt * 14)
        else:
            y[m] = np.exp(-tt * damp) * np.cos(2 * np.pi * nosc * 2.6 * tt)
        ax.plot(t, y, color=col, lw=2.8)
        ax.axhline(0, color="#c3ccd6", lw=1.0, ls=":")
        ax.set_xlim(0, 1.6)
        ax.set_ylim(-0.75, 1.35)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(name, fontsize=11, color=col, fontweight="bold", pad=8)
        for s in ax.spines.values():
            s.set_color("#9aa4b0")
        for k, ln in enumerate(desc):
            if ln:
                ax.text(0.5, -0.14 - k * 0.15, ln, transform=ax.transAxes,
                        fontsize=9.4, color=INK, ha="center", va="top")
        for k, ln in enumerate(mean):
            ax.text(0.5, -0.50 - k * 0.15, ln, transform=ax.transAxes,
                    fontsize=9.4, color=col, ha="center", va="top")
    fig.text(0.5, 0.055,
             "※ フラッシュを離した直後の振動の数を見る。"
             "患者の治療を変える前に、まず回路を疑う。",
             fontsize=9.8, color="#8d97a3", ha="center", va="center")
    fig.savefig(P("f10_square_wave.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f11
def f11():
    W, H, DPI = 1520, 760, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0.125, 0.185, 0.84, 0.66])
    t = np.linspace(0, 2.0, 2000)
    y = np.zeros_like(t)
    for k in range(2):
        t0 = k * 1.0
        tt = t - t0
        up = np.clip(tt / 0.10, 0, 1) ** 1.4
        dn = np.exp(-np.clip(tt - 0.10, 0, None) / 0.30)
        seg = np.where((tt >= 0) & (tt < 1.0), 40 * up * dn + 78, 0)
        notch = 6.5 * np.exp(-((tt - 0.34) ** 2) / (2 * 0.022 ** 2))
        seg = np.where((tt >= 0) & (tt < 1.0), seg - notch, 0)
        y = np.maximum(y, seg)
    y[y == 0] = 78
    ax.plot(t, y, color="#c0392b", lw=3.2)
    ax.axhline(118, color="#8d97a3", lw=1.2, ls=":")
    ax.axhline(78, color="#8d97a3", lw=1.2, ls=":")
    ax.text(1.97, 120, "収縮期圧", fontsize=10.5, color="#6b7785",
            ha="right", va="bottom")
    ax.text(1.97, 74, "拡張期圧", fontsize=10.5, color="#6b7785",
            ha="right", va="top")
    ax.annotate("立ち上がり（dP/dt）\n心収縮性を反映", xy=(0.06, 100),
                xytext=(0.10, 136), fontsize=10.5, color="#2e6da4",
                ha="left", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="->", color="#2e6da4", lw=1.6))
    ax.annotate("重複切痕（dicrotic notch）\n大動脈弁の閉鎖", xy=(0.34, 96),
                xytext=(0.62, 142), fontsize=10.5, color="#1f6b47",
                ha="left", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="->", color="#1f6b47", lw=1.6))
    ax.annotate("下降脚の傾き\n血管抵抗を反映", xy=(0.72, 84),
                xytext=(1.30, 136), fontsize=10.5, color="#b8760f",
                ha="left", va="top", linespacing=1.6,
                arrowprops=dict(arrowstyle="->", color="#b8760f", lw=1.6))
    ax.set_xlim(0, 2.0)
    ax.set_ylim(60, 160)
    ax.set_xticks([])
    ax.set_yticks([60, 80, 100, 120, 140])
    ax.set_ylabel("動脈圧（mmHg）", fontsize=12, color=INK, labelpad=10)
    ax.set_title("動脈圧波形は「血圧の数字」以上のことを語る", fontsize=13,
                 color="#0A1830", weight="bold", pad=16)
    ax.grid(axis="y", color="#eceff2", lw=1.0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11.5, colors=INK)
    for s in ax.spines.values():
        s.set_color("#7c8894")
    fig.text(0.5, 0.065,
             "※ ただし、これらの読みは回路が適正に減衰しているときにだけ成り立つ（図10-1）。",
             fontsize=9.8, color="#8d97a3", ha="center", va="center")
    fig.savefig(P("f11_art_waveform.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f12
def f12():
    W, H = 1520, 648
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "逆血が得られたあとの4つの局面 —— 抵抗を感じたら押さない",
             size=12.5, ha="center")
    PANELS = [
        ("A　前壁を越えた", 0, False, "逆血が得られた。カテーテル先端はまだ外にある"),
        ("B　テンティング", 1, False, "血管が針で押されて変形している"),
        ("C　貫通", 2, False, "後壁を越えて血管を貫いた"),
        ("D　戻して確認", 1, True, "ゆっくり戻し、拍動性の逆血が戻る位置で進める"),
    ]
    PW, PTOP, PH = 340, 88, 262
    for i, (title, mode, back, cap) in enumerate(PANELS):
        px = 44 + i * (PW + 22)
        cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
        cv.text(px + PW / 2, PTOP + 32, title, size=10.8, color=NAVY,
                weight="bold")
        vy = PTOP + 150
        x0, x1 = px + 34, px + PW - 34
        top = np.full(200, vy - 30.0)
        bot = np.full(200, vy + 30.0)
        xs = np.linspace(x0, x1, 200)
        if mode == 1:      # テンティング
            bump = 22 * np.exp(-((xs - (px + PW * 0.60)) ** 2) / (2 * 26 ** 2))
            bot = bot + bump
        ax.fill_between(xs, top, bot, color="#dceaf5", zorder=2)
        ax.plot(xs, top, color="#c0392b", lw=2.2, zorder=3)
        ax.plot(xs, bot, color="#c0392b", lw=2.2, zorder=3)
        tipx = {0: px + PW * 0.55, 1: px + PW * 0.60, 2: px + PW * 0.70}[mode]
        tipy = vy + (34 if mode == 2 else 0)
        ax.plot([px + 8, tipx], [vy - 62, tipy], color="#4a5768", lw=5,
                solid_capstyle="round", zorder=5)
        ax.add_patch(Circle((tipx, tipy), 6, facecolor="#22303f",
                            edgecolor="none", zorder=6))
        if back:
            cv.arrow((tipx + 44, vy - 46), (tipx + 6, vy - 24),
                     color="#1f6b47", lw=2.0, head=10)
            cv.text(tipx + 52, vy - 54, "戻す", size=9.2, color="#1f6b47",
                    ha="left", z=7)
        if mode == 2:
            cv.text(px + PW / 2, vy + 66, "後壁を貫通", size=9.2,
                    color="#c0392b", z=7)
        for j, ln in enumerate(cv.wrap(cap, PW - 24, 9.4)):
            cv.text(px + PW / 2, PTOP + PH + 28 + LH(9.4, 1.4) * j, ln,
                    size=9.4, color=INK)
    NOTE = ("※ 逆血は「針先が管腔内」であって「カテーテル先端が管腔内」ではない。"
            "抵抗があれば、押すのではなく止めて位置を再評価する。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, H - 78 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f12_after_flashback.png"))


# ---------------------------------------------------------------- f13
def f13():
    W, H, DPI = 1520, 900, 200
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0.255, 0.27, 0.705, 0.60])
    ROWS = [("一過性動脈閉塞", 19.7), ("血腫", 14.4), ("局所感染", 0.72),
            ("出血", 0.53), ("敗血症", 0.13), ("永続的虚血性障害", 0.09),
            ("仮性動脈瘤", 0.09)]
    y = np.arange(len(ROWS))[::-1]
    col = ["#b8760f", "#b8760f", "#2e6da4", "#2e6da4", "#c0392b",
           "#c0392b", "#c0392b"]
    ax.barh(y, [r[1] for r in ROWS], 0.58, color=col)
    for yy, r in zip(y, ROWS):
        ax.annotate("%.2f%%" % r[1] if r[1] < 1 else "%.1f%%" % r[1],
                    (r[1], yy), textcoords="offset points", xytext=(8, 0),
                    va="center", fontsize=11, color=INK, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in ROWS], fontsize=12, color=INK)
    ax.set_xscale("log")
    ax.set_xlim(0.05, 60)
    ax.set_xticks([0.1, 1, 10])
    ax.set_xticklabels(["0.1%", "1%", "10%"])
    ax.set_xlabel("既報レビューでの参考頻度（対数目盛）", fontsize=12,
                  color=INK, labelpad=10)
    ax.set_title("橈骨動脈ラインの合併症 —— 頻度の桁を知っておく", fontsize=13,
                 color="#0A1830", weight="bold", pad=16)
    ax.grid(axis="x", color="#eceff2", lw=1.0, which="both")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11.5, colors=INK)
    for s in ax.spines.values():
        s.set_color("#7c8894")
    for i, ln in enumerate([
            "※ リスクの大小を理解するための歴史的な参考値であり、個々の患者の現在のリスク予測値ではない。",
            "　 頻度が低い合併症ほど、見逃したときの機能的な損失は大きい。"]):
        fig.text(0.5, 0.070 - i * 0.036, ln, fontsize=9.8, color="#8d97a3",
                 ha="center", va="center")
    fig.savefig(P("f13_complications.png"), dpi=DPI, facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- f14
def f14():
    W, H = 1520, 480
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "指が蒼白・冷たい —— 様子を見ない。順序立てて動く",
             size=12.5, ha="center")
    STEPS = [
        ("① まず抜く", "原因がカテーテルなら、抜去そのものが治療になる。迷う時間が障害をつくる"),
        ("② 圧迫を解く", "固定テープ、手関節の過伸展、包帯、同側の血圧計カフを外す"),
        ("③ 保温と挙上", "攣縮の要素があれば、これで改善することがある"),
        ("④ 評価と相談", "改善しなければドプラで血流を評価し、血管外科・形成外科へ"),
    ]
    L, R = 44, W - 44
    GAP = 16
    CW = (R - L - GAP * 3) / 4
    TOP, BSZ = 100, 9.6
    nl = max(len(cv.wrap(s[1], CW - 34, BSZ)) for s in STEPS)
    CH = 82 + LH(BSZ, 1.45) * (nl - 1) + LH(BSZ, 1.0) * 0.5 + 22
    for i, (head, body) in enumerate(STEPS):
        x = L + i * (CW + GAP)
        fc, ec = ("#fbeeee", "#c0392b") if i < 3 else ("#f6e0dd", "#8f2b28")
        cv.box(x, TOP, CW, CH, fc=fc, ec=ec, lw=1.9, radius=8)
        cv.text(x + CW / 2, TOP + 42, head, size=11.4, color=ec, weight="bold")
        for j, ln in enumerate(cv.wrap(body, CW - 34, BSZ)):
            cv.text(x + CW / 2, TOP + 82 + LH(BSZ, 1.45) * j, ln, size=BSZ,
                    color=INK)
        if i < 3:
            cv.arrow((x + CW + 1, TOP + CH / 2), (x + CW + GAP - 1, TOP + CH / 2),
                     color="#c0392b", lw=2.0, head=9)
    MSG = "「抜いたら血圧が測れなくなる」で残さない —— 非観血的血圧測定という代替がある"
    by = TOP + CH + 26
    msz = cv.fit_size([MSG], R - L - 60, 11.5, weight="bold")
    bh = 30 + LH(msz, 1.5)
    cv.box(L, by, R - L, bh, fc="#fbeeee", ec="#c0392b", lw=2.0, radius=8)
    cv.text(W / 2, by + bh / 2, MSG, size=msz, color="#9c2b26", weight="bold")
    cv.save(P("f14_ischemia_steps.png"))


for fn in (f08, f09, f10, f11, f12, f13, f14):
    fn()
    print("ok", fn.__name__)
