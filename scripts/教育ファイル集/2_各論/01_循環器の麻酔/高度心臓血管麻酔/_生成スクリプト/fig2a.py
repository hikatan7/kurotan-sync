# -*- coding: utf-8 -*-
"""第Ⅱ章 大動脈手術の脳保護　図版 g01〜g07"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)
from fig1a import cap, msg, fitlines, card, W, TEAL

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- g01
def g01():
    """脳が傷つく二つの道筋"""
    cv = Canvas(W, 900)
    cap(cv, 44, "大動脈手術で脳が傷つく道筋は二つある")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 560

    def panel(x, title, color, fc, steps, bottom):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.box(x, PY, PW, 56, fc=color, ec=color, lw=0, radius=10)
        ts = cv.fit_size([title], PW - 44, 12.4, weight="bold")
        cv.text(x + PW / 2, PY + 28, title, size=ts, color="white",
                weight="bold")
        y = PY + 86
        for i, (s, sub) in enumerate(steps):
            ss = cv.fit_size([s], PW - 120, 10.8, weight="bold")
            us = cv.fit_size([sub], PW - 110, 9.6)
            h = 16 + LH(ss, 1.25) + LH(us, 1.25) + 12
            cv.box(x + 34, y, PW - 68, h, fc=fc, ec=color, lw=1.5, radius=8)
            cv.text(x + PW / 2, y + 16 + LH(ss, 1.25) / 2, s, size=ss, color=INK,
                    weight="bold")
            cv.text(x + PW / 2, y + 16 + LH(ss, 1.25) + LH(us, 1.25) / 2, sub,
                    size=us, color=GREY)
            if i < len(steps) - 1:
                cv.arrow((x + PW / 2, y + h + 2), (x + PW / 2, y + h + 22),
                         color=color, lw=2.0, head=10)
            y += h + 24
        bl = cv.wrap(bottom, PW - 80, 10.4)
        cv.block(x + 34, PY + PH - 26 - LH(10.4, 1.6) * len(bl), PW - 68,
                 bl, 10.4, color=color, weight="bold")

    panel(x1, "① 塞栓（飛ぶ）", BLUE, "#eaf1f8",
          [("大動脈壁の粥腫・血栓・空気", "遮断・送血・脱気の操作で剝がれる"),
           ("弓部分枝へ流れ込む", "どこへ飛ぶかは制御できない"),
           ("局所の梗塞", "片麻痺・失語など巣症状として出る")],
          "対策は「飛ばさない」こと。操作そのものを設計する")

    panel(x2, "② 低灌流（足りない）", RED, "#fceeec",
          [("循環停止・分枝遮断・送血不良", "脳へ行く血流が減る"),
           ("酸素供給が需要を下回る", "温度を下げれば需要は減る"),
           ("境界領域の虚血", "びまん性、覚醒遅延として出る")],
          "対策は「時間を買う」こと。低体温と選択的灌流")

    msg(cv, PY + PH + 30,
        "この二つは原因も対策も違う。どちらを相手にしているのかを、常に意識する")
    cv.save(P("g01_two_mechanisms.png"))


# ---------------------------------------------------------------- g02
def g02():
    """弓部の解剖と Willis 動脈輪"""
    cv = Canvas(W, 900)
    cap(cv, 44, "片側送血で両半球が灌流されるかどうかは、患者によって違う")

    # 左：弓部分枝
    LX, LY, LW, LH_ = 70, 130, 660, 560
    cv.box(LX, LY, LW, LH_, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(LX + LW / 2, LY + 32, "弓部の三分枝", size=12.2, color=NAVY,
            weight="bold")
    # 大動脈弓
    cv.box(LX + 120, LY + 300, 420, 150, fc="#f4f6f9", ec="#c9d2dc", lw=1.6,
           radius=60)
    cv.text(LX + 330, LY + 400, "大動脈弓", size=10.6, color=GREY)
    BR = [("腕頭動脈", LX + 150, BLUE, ["右総頸動脈", "右鎖骨下動脈"]),
          ("左総頸動脈", LX + 330, GREEN, ["左半球へ"]),
          ("左鎖骨下動脈", LX + 510, PURPLE, ["左椎骨動脈"])]
    for name, bx, col, subs in BR:
        cv.arrow((bx, LY + 300), (bx, LY + 216), color=col, lw=2.6, head=10,
                 style="-")
        ns = cv.fit_size([name], 150, 10.4, weight="bold")
        us = min(cv.fit_size([s_], 150, 9.2) for s_ in subs)
        bh = 18 + LH(ns, 1.3) + LH(us, 1.3) * len(subs) + 12
        top = LY + 210 - bh
        cv.box(bx - 84, top, 168, bh, fc="#ffffff", ec=col, lw=1.6,
               radius=8)
        cv.text(bx, top + 18 + LH(ns, 1.3) / 2, name, size=ns, color=col,
                weight="bold")
        for j, sub in enumerate(subs):
            cv.text(bx, top + 18 + LH(ns, 1.3) + LH(us, 1.3) * (j + 0.5), sub,
                    size=us, color=GREY)

    # 右：Willis 輪
    RX = LX + LW + 30
    RW = W - 70 - RX
    cv.box(RX, LY, RW, LH_, fc="#ffffff", ec=TEAL, lw=1.8, radius=10)
    cv.text(RX + RW / 2, LY + 32, "Willis 動脈輪", size=12.2, color=TEAL,
            weight="bold")
    cx, cy = RX + RW / 2, LY + 240
    cv.box(cx - 145, cy - 88, 290, 176, fc="#eef6f7", ec=TEAL, lw=1.8,
           radius=80)
    wl = ["前交通動脈・後交通動脈", "による左右の連絡"]
    ws = cv.fit_size(wl, 230, 10.4)
    cv.block(cx - 145, cy - LH(ws, 1.6), 290, wl, ws, color=INK,
             lh=LH(ws, 1.6))
    cv.arrow((cx - 224, cy), (cx - 149, cy), color=BLUE, lw=2.4, head=10)
    cv.text(cx - 232, cy, "右から", size=9.8, color=BLUE, ha="right")
    cv.arrow((cx + 224, cy), (cx + 149, cy), color=GREEN, lw=2.4, head=10)
    cv.text(cx + 232, cy, "左から", size=9.8, color=GREEN, ha="left")

    textbox(cv, RX + 30, LY + 360, RW - 60,
            ["交通動脈が細い、または存在しない人がいる",
             "動脈硬化で分枝が閉塞していることがある",
             "解離では分枝が偽腔から灌流されていることがある"],
            10.4, style="amber", title="片側灌流が届かない理由",
            title_color="#9a6510", pad_y=14)

    msg(cv, LY + LH_ + 30,
        "「片側でも Willis 輪が補う」は前提であって、確認すべき仮説である")
    cv.save(P("g02_arch_willis.png"))


# ---------------------------------------------------------------- g03
def g03():
    """ACP・RCP・DHCA の灌流経路"""
    cv = Canvas(W, 900)
    cap(cv, 44, "三つの方法は、脳に対して別のことをしている")

    CW = (W - 140 - 60) / 3
    PY, PH = 130, 520
    D = [("DHCA（単独循環停止）", GREY, "#f2f4f6", "none",
          ["脳への血流をいったん止める",
           "低体温で代謝を落として耐える",
           "時間が延びるほど不利になる"]),
         ("ACP（順行性脳灌流）", BLUE, "#eaf1f8", "ante",
          ["弓部分枝から生理的な向きで送る",
           "比較的長い時間に耐えられる",
           "分枝の操作とカニュレーションが要る"]),
         ("RCP（逆行性脳灌流）", GREEN, "#eaf5ee", "retro",
          ["上大静脈から逆向きに送る",
           "空気やデブリの洗い出しを狙う",
           "灌流量としては限定的"])]

    for i, (title, col, fc, mode, lines) in enumerate(D):
        x = 70 + (CW + 30) * i
        cv.box(x, PY, CW, PH, fc="#ffffff", ec=col, lw=1.8, radius=10)
        ts = cv.fit_size([title], CW - 40, 11.8, weight="bold")
        cv.text(x + CW / 2, PY + 32, title, size=ts, color=col, weight="bold")
        # 模式図
        hx, hy = x + CW / 2, PY + 170
        cv.box(hx - 90, hy - 62, 180, 96, fc=fc, ec=col, lw=1.6, radius=40)
        cv.text(hx, hy - 14, "脳", size=12, color=col, weight="bold")
        if mode == "none":
            cv.text(hx, hy + 78, "血流なし", size=11, color=RED, weight="bold")
            cv.text(hx, hy + 106, "（低体温で代謝を下げる）", size=9.4,
                    color=GREY)
        elif mode == "ante":
            cv.arrow((hx, hy + 110), (hx, hy + 40), color=col, lw=3.0, head=13)
            cv.text(hx, hy + 134, "動脈側から順行性に", size=9.8, color=col)
        else:
            cv.arrow((hx + 108, hy + 110), (hx + 44, hy + 40), color=col,
                     lw=3.0, head=13)
            cv.text(hx + 20, hy + 136, "上大静脈から逆行性に", size=9.8,
                    color=col)
        s, bl = fitlines(cv, lines, CW - 46, 10.2)
        for j, ln in enumerate(bl):
            cv.text(x + CW / 2, PY + 340 + LH(s, 1.7) * (j + 0.5), ln,
                    size=s, color=INK)

    textbox(cv, 70, PY + PH + 26, W - 140,
            ["ACP と RCP を比較した 19 研究 15,365 例のメタ解析では、",
             "脳卒中（OR 0.92、95%CI 0.79-1.08）にも死亡にも有意差はなかった。",
             "どちらが優れているかではなく、どの状況でどれを選ぶかという問題である。"],
            10.6, style="navy", pad_y=14)
    cv.save(P("g03_acp_rcp_dhca.png"))


# ---------------------------------------------------------------- g04
def g04():
    """送血部位"""
    cv = Canvas(W, 1000)
    cap(cv, 44, "どこから送るかで、脳卒中の頻度が変わる")

    C = [("腋窩動脈", BLUE, "#eaf1f8",
          ["順行性に送れる", "ACP へ移行しやすい", "解離では真腔に入りやすい",
           "露出に時間がかかる"]),
         ("大腿動脈", ORANGE, "#fdf3e3",
          ["速く確保できる", "逆行性送血になる", "偽腔送血・塞栓の懸念",
           "緊急時の選択肢"]),
         ("上行大動脈・腕頭動脈", GREEN, "#eaf5ee",
          ["直接カニュレーション", "エコー下に真腔を確認",
           "施設の習熟による", "解離で用いる施設が増えている"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 130, w, t, lines, col, fc,
             body_size=10.4, lh=1.8)

    # データ帯
    y0 = 470
    cv.text(W / 2, y0 + 34, "腋窩送血と大腿送血を比べた実データ", size=12,
            color=NAVY, weight="bold")
    ROWS = [("腋窩 対 大腿のメタ解析（2,621 例）",
             "短期死亡 OR 0.42（95%CI 0.25-0.70）　／　"
             "神経学的合併症 OR 0.63（0.42-0.94）", BLUE),
            ("STS データベース（A 型解離 7,353 例）",
             "手術死亡 17%・術後脳卒中 13%。腋窩は大腿に比べ脳卒中 OR 0.60"
             "（p<0.001）", GREEN)]
    yy = y0 + 62
    for lab, a, col in ROWS:
        ls = cv.fit_size([lab], W - 240, 10.4, weight="bold")
        vs = cv.fit_size([a], W - 240, 10.2)
        rh = 14 + LH(ls, 1.3) + LH(vs, 1.3) + 10
        cv.box(94, yy, W - 188, rh, fc="#fbfcfd", ec=col, lw=1.4, radius=8)
        cv.text(118, yy + 14 + LH(ls, 1.3) / 2, lab, size=ls, color=col,
                weight="bold", ha="left")
        cv.text(118, yy + 14 + LH(ls, 1.3) + LH(vs, 1.3) / 2, a, size=vs,
                color=INK, ha="left")
        yy += rh + 12
    # 帯の枠は中身に合わせて描き直す
    cv.box(70, y0, W - 140, yy - y0 + 10, fc="none", ec=NAVY, lw=1.8, radius=10)

    msg(cv, yy + 40,
        "腋窩送血は「丁寧だが遅い」ではなく、脳卒中を減らす選択肢として扱う",
        fc="#eaf1f8", ec=BLUE, tc=BLUE)
    cv.save(P("g04_cannulation.png"))


# ---------------------------------------------------------------- g05
def g05():
    """温度戦略"""
    cv = Canvas(W, 960)
    cap(cv, 44, "深く冷やすほど安全、ではなかった")

    BAND = [("深低体温 DHCA", "20 °C 以下", RED, "#fceeec", 0),
            ("中等度低体温 MHCA", "20.1〜25 °C", ORANGE, "#fdf3e3", 1),
            ("軽度低体温 mild", "25 °C 超", GREEN, "#eaf5ee", 2)]
    y0 = 130
    bw = (W - 140 - 60) / 3
    for t, r, col, fc, i in BAND:
        x = 70 + (bw + 30) * i
        cv.box(x, y0, bw, 110, fc=fc, ec=col, lw=1.8, radius=10)
        cv.text(x + bw / 2, y0 + 40, t, size=12.2, color=col, weight="bold")
        cv.text(x + bw / 2, y0 + 76, r, size=11.0, color=INK)

    y1 = y0 + 150
    cv.box(70, y1, W - 140, 360, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(W / 2, y1 + 34, "34 研究 12,370 例のネットワークメタ解析", size=12,
            color=NAVY, weight="bold")
    L = [("脳卒中", "DHCA は MHCA より多い", "OR 1.46（95%CI 1.19-1.78）", RED),
         ("脳卒中", "DHCA は mild より多い", "OR 1.50（95%CI 1.14-1.98）", RED),
         ("手術死亡", "DHCA・MHCA とも mild より多い",
          "DHCA OR 1.71（1.23-2.39）", ORANGE)]
    yy = y1 + 74
    for lab, txt, num, col in L:
        cv.box(94, yy, 130, 46, fc="#f2f4f6", ec=col, lw=1.4, radius=6)
        cv.text(159, yy + 23, lab, size=10.4, color=col, weight="bold")
        cv.text(250, yy + 23, txt, size=10.6, color=INK, ha="left")
        cv.text(W - 96, yy + 23, num, size=10.4, color=col, ha="right",
                weight="bold")
        yy += 62
    fn = ["別の 24 研究 6,018 例（deep 2,978・moderate 2,525・mild 515）の解析でも、",
          "死亡は mild 対 deep で OR 0.50、moderate 対 deep で OR 0.68 と同じ向きであった"]
    fs = cv.fit_size(fn, W - 220, 9.8)
    cv.block(70, y1 + 256, W - 140, fn, fs, color=GREY, lh=LH(fs, 1.5))

    textbox(cv, 70, y1 + 390, W - 140,
            ["ただし観察研究をまとめた解析であり、",
             "「浅く冷やせるほど短時間で済む症例だった」という交絡は否定できない。",
             "腎機能では、中等度低体温のほうが腎不全が少ないという報告がある"
             "（OR 0.73、95%CI 0.54-0.99）。ただし停止時間が 30 分を超えると差は消えた。"],
            10.5, style="amber", title="この数字の読み方",
            title_color="#9a6510", pad_y=14)
    cv.save(P("g05_temperature.png"))


# ---------------------------------------------------------------- g06
def g06():
    """NIRS の時間軸"""
    cv = Canvas(W, 900)
    cap(cv, 44, "rSO2 は「値」ではなく「経過」で読む")

    x0, y0 = 90, 160
    pw, ph = W - 180, 330
    cv.rect(x0, y0, pw, ph, fc="#fbfcfd", ec="#dde3ea", lw=1.4)
    # 目盛り
    for v, lab in ((0.15, "80"), (0.4, "70"), (0.65, "60"), (0.9, "50")):
        yy = y0 + ph * v
        cv.ax.plot([x0, x0 + pw], [yy, yy], color="#e8ecf0", lw=1.0, zorder=1)
        cv.text(x0 - 16, yy, lab, size=9.2, color=GREY, ha="right")
    cv.text(x0 + 6, y0 - 16, "rSO2 (%)", size=9.4, color=GREY, ha="left")

    PH_ = [("baseline", 0.06, 0.32), ("CPB 開始", 0.18, 0.36),
           ("冷却", 0.30, 0.22), ("循環停止", 0.44, 0.70),
           ("ACP 開始", 0.56, 0.40), ("復温", 0.72, 0.30),
           ("離脱", 0.88, 0.34)]
    xs = [x0 + pw * p for _, p, _ in PH_]
    ys = [y0 + ph * v for _, _, v in PH_]
    cv.ax.plot(xs, ys, color=NAVY, lw=2.6, marker="o", markersize=5,
               zorder=4)
    for (lab, p, v), xx, yy in zip(PH_, xs, ys):
        cv.text(xx, y0 + ph + 26, lab, size=9.8, color=INK)
        cv.ax.plot([xx, xx], [y0, y0 + ph], color="#eef1f5", lw=1.0, zorder=0)
    # baseline からの低下を示す帯
    cv.rect(x0 + pw * 0.40, y0, pw * 0.18, ph, fc="#fceeec", alpha=0.6)
    cv.text(x0 + pw * 0.49, y0 - 18, "循環停止中は下がって当然", size=10.0,
            color=RED, weight="bold")
    cv.arrow((x0 + pw * 0.44, y0 + ph * 0.34), (x0 + pw * 0.44, y0 + ph * 0.66),
             color=RED, lw=2.0, head=10)
    cv.text(x0 + pw * 0.30, y0 + ph * 0.50, "baseline からの低下幅で見る",
            size=9.8, color=RED, ha="right")

    textbox(cv, 70, y0 + ph + 70, (W - 160) / 2,
            ["麻酔導入前の覚醒時の値を必ず記録する",
             "左右差は、送血の偏りやカニューレ位置のサイン",
             "絶対値より、baseline からの低下幅と持続時間"],
            10.5, style="blue", title="読み方の原則", title_color=BLUE,
            pad_y=14)
    textbox(cv, 90 + (W - 160) / 2, y0 + ph + 70, (W - 160) / 2,
            ["センサは前額部の皮膚・頭蓋外の血流も拾う",
             "モニタによって表示される数字の意味が違う",
             "「測れば転帰が良くなる」ことは証明されていない"],
            10.5, style="amber", title="限界", title_color="#9a6510",
            pad_y=14)
    cv.save(P("g06_nirs_timeline.png"))


# ---------------------------------------------------------------- g07
def g07():
    """モニタの役割分担"""
    cv = Canvas(W, 900)
    cap(cv, 44, "何を検出できて、何を検出できないのか")

    ROWS = [("NIRS（近赤外線脳酸素モニター）", BLUE, "#eaf1f8",
             "前額部の酸素需給バランス", "前方循環の一部のみ。頭蓋外の影響を受ける"),
            ("処理脳波・生脳波", PURPLE, "#f1ecf8",
             "皮質の電気的活動、冷却の到達度", "深部の虚血は捉えにくい。麻酔薬の影響"),
            ("経頭蓋ドプラ（TCD）", GREEN, "#eaf5ee",
             "中大脳動脈の血流速度と塞栓シグナル", "側頭骨の窓がない人がいる。固定が難しい"),
            ("体性感覚誘発電位（SSEP）", ORANGE, "#fdf3e3",
             "感覚路の伝導", "運動路は評価できない。麻酔・低体温の影響が大きい")]
    y = 140
    for name, col, fc, can, cannot in ROWS:
        h = 130
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.7, radius=10)
        cv.box(70, y, 340, h, fc=fc, ec=col, lw=0, radius=10)
        nl = [name] if cv.width(name, 11.0, "bold") <= 300 else             [name[:name.index("（")], name[name.index("（"):]]   # 括弧の前で折る
        for j, ln in enumerate(nl):
            cv.text(240, y + h / 2 + LH(11.0, 1.35) * (j - (len(nl) - 1) / 2), ln,
                    size=11.0, color=col, weight="bold")
        lx = 440
        vx = lx + cv.width("検出できない", 9.6, "bold") + 28
        vs = min(cv.fit_size([can, cannot], W - 90 - vx, 10.4), 10.4)
        cv.text(lx, y + 40, "検出できる", size=9.6, color=GREEN, ha="left",
                weight="bold")
        cv.text(vx, y + 40, can, size=vs, color=INK, ha="left")
        cv.text(lx, y + 88, "検出できない", size=9.6, color=RED, ha="left",
                weight="bold")
        cv.text(vx, y + 88, cannot, size=vs, color=INK, ha="left")
        y += h + 16

    msg(cv, y + 16,
        "一つのモニタで脳全体は見えない。組み合わせても「見えない場所」は残る")
    cv.save(P("g07_monitors.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (g01, g02, g03, g04, g05, g06, g07):
        fn()
        print("ok", fn.__name__)
