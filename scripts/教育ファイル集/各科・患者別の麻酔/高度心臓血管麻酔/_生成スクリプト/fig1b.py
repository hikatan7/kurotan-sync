# -*- coding: utf-8 -*-
"""第Ⅰ章 CIED　図版 f08〜f14（magnet・oversensing・リード抜去・アルゴリズム）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)
from fig1a import P, cap, msg, fitlines, card, W, TEAL
from figcrop import crop_bottom

plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


# ------------------------------------------------- アルゴリズム用の部品
def step(cv, x, y, w, lines, style="blue", size=10.6, title=None,
         title_color=None, pad_y=14):
    return textbox(cv, x, y, w, lines, size, style=style, title=title,
                   title_size=11.2, title_color=title_color, pad_y=pad_y)


def down(cv, x, y0, y1, label=None, color="#95a0ac"):
    cv.arrow((x, y0), (x, y1), color=color, lw=2.2, head=11)
    if label:
        cv.text(x + 14, (y0 + y1) / 2, label, size=9.6, color=color,
                ha="left")


def side(cv, x0, x1, y, label=None, color="#95a0ac"):
    cv.arrow((x0, y), (x1, y), color=color, lw=2.2, head=11)
    if label:
        cv.text((x0 + x1) / 2, y - 18, label, size=9.6, color=color)


# ---------------------------------------------------------------- f08
def f08():
    """magnet を置くと何が起きるか"""
    cv = Canvas(W, 900)
    cap(cv, 44, "magnet を置いたときに、実際に止まるもの・変わるもの")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 560

    def panel(x, title, color, fc, rows, bottom, bcolor):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.box(x, PY, PW, 56, fc=color, ec=color, lw=0, radius=10)
        ts = cv.fit_size([title], PW - 44, 12.2, weight="bold")
        cv.text(x + PW / 2, PY + 28, title, size=ts, color="white",
                weight="bold")
        y = PY + 84
        for mark, lab, col in rows:
            cv.text(x + 34, y + 20, mark, size=16, color=col, ha="left",
                    weight="bold")
            ls = cv.fit_size([lab], PW - 110, 10.6)
            cv.text(x + 74, y + 20, lab, size=ls, color=INK, ha="left")
            y += 54
        bl = cv.wrap(bottom, PW - 60, 10.4)
        bh = 26 + LH(10.4, 1.6) * len(bl)
        cv.box(x + 22, PY + PH - bh - 24, PW - 44, bh, fc=fc, ec=bcolor,
               lw=1.6, radius=8)
        for j, ln in enumerate(bl):
            cv.text(x + PW / 2, PY + PH - bh - 24 + 13 + LH(10.4, 1.6) * (j + 0.5),
                    ln, size=10.4, color=INK)

    panel(x1, "ペースメーカーに magnet を置く", BLUE, "#eaf1f8",
          [("→", "多くの機種で非同期ペーシングになる", BLUE),
           ("→", "レートは機種と電池残量で決まる", BLUE),
           ("→", "自己調律と競合する可能性がある", ORANGE),
           ("×", "頻拍治療という機能はそもそもない", GREY),
           ("!", "magnet に反応しない設定・機種がある", RED)],
          "EMI でペーシングが抑制されるのを防ぐ目的では有効。ただし機種を確認できていることが前提である。",
          BLUE)

    panel(x2, "ICD に magnet を置く", RED, "#fceeec",
          [("→", "頻拍治療（ATP とショック）が止まる", RED),
           ("×", "ペーシングは非同期にならない", RED),
           ("×", "徐脈ペーシングの設定は変わらない", RED),
           ("!", "ペーシング依存例は magnet では守れない", RED),
           ("!", "外した瞬間から治療が再開する", ORANGE)],
          "ペーシング依存の ICD 患者では、非同期化のために再プログラミングが必要になる。",
          RED)

    msg(cv, PY + PH + 30,
        "magnet は「頻拍治療を止める道具」であり、「ペーシングを守る道具」ではない",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("f08_magnet.png"))


# ---------------------------------------------------------------- f09
def f09():
    """oversensing で何が起きるか"""
    cv = Canvas(W, 900)
    cap(cv, 44, "EMI を心内電位と読み違えると、二通りの事故が起きる")

    def strip(x, y, w, h, title, color, mode):
        cv.box(x, y, w, h, fc="#ffffff", ec=color, lw=1.8, radius=10)
        ts = cv.fit_size([title], w - 44, 11.8, weight="bold")
        cv.text(x + w / 2, y + 30, title, size=ts, color=color, weight="bold")
        bx, by, bw, bh = x + 30, y + 60, w - 60, h - 150
        cv.rect(bx, by, bw, bh, fc="#fbfcfd", ec="#dde3ea", lw=1.2)
        base = by + bh * 0.62
        t = np.linspace(0, 1, 600)
        # 心電図らしい波形
        def beat(tt, c):
            return np.exp(-((tt - c) ** 2) / 0.00012) * -52

        if mode == "inhibit":
            ys = np.zeros_like(t)
            for c in (0.08, 0.2, 0.32):
                ys += beat(t, c)
            noise = (t > 0.42) & (t < 0.72)
            ys = ys + np.where(noise,
                               np.sin(t * 620) * 11 + np.sin(t * 271) * 6, 0)
            for c in (0.86, 0.97):
                ys += beat(t, c)
            cv.rect(bx + bw * 0.42, by + 12, bw * 0.30, bh - 24,
                    fc="#fdf3e3", alpha=0.75)
            cv.text(bx + bw * 0.57, by + 34, "電気メス通電", size=9.8,
                    color="#9a6510", weight="bold")
            cv.text(bx + bw / 2, by + bh + 30, "ペーシングが抑制され心拍が出ない",
                    size=10.2, color=RED, weight="bold")
        else:
            ys = np.zeros_like(t)
            for c in (0.08, 0.2, 0.32, 0.86, 0.97):
                ys += beat(t, c)
            noise = (t > 0.42) & (t < 0.68)
            ys = ys + np.where(noise,
                               np.sin(t * 700) * 13 + np.sin(t * 311) * 7, 0)
            cv.rect(bx + bw * 0.42, by + 12, bw * 0.26, bh - 24,
                    fc="#fdf3e3", alpha=0.75)
            cv.text(bx + bw * 0.55, by + 34, "電気メス通電", size=9.8,
                    color="#9a6510", weight="bold")
            cv.arrow((bx + bw * 0.74, by + 96), (bx + bw * 0.74, base - 16),
                     color=RED, lw=2.4, head=12)
            cv.text(bx + bw / 2, by + bh + 30, "洞調律なのにショックが入る",
                    size=10.2, color=RED, weight="bold")
        cv.ax.plot(bx + t * bw, base + ys, color=NAVY, lw=1.8, zorder=4)

    strip(70, 130, (W - 190) / 2, 420,
          "ペースメーカー：EMI を自己心拍と読み違える", BLUE, "inhibit")
    strip(70 + (W - 190) / 2 + 50, 130, (W - 190) / 2, 420,
          "ICD：EMI を心室細動と読み違える", RED, "shock")

    _h1 = textbox(cv, 70, 590, (W - 160) / 2,
            ["ペーシング依存であれば、抑制はそのまま心停止になる。",
             "非同期モードにしておけば、この事故は起きない。"],
            10.6, style="blue", title="抑制（inhibition）の帰結",
            title_color=BLUE, pad_y=14)
    _h2 = textbox(cv, 90 + (W - 160) / 2, 590, (W - 160) / 2,
            ["ショックは患者を動かし、循環を乱し、術野を危険にする。",
             "頻拍治療を止めておけば、この事故は起きない。"],
            10.6, style="red", title="不適切ショックの帰結",
            title_color=RED, pad_y=14)

    msg(cv, 590 + max(_h1, _h2) + 24, "止めるべきものが二つある。どちらを止めるかで手段が変わる")
    cv.save(P("f09_oversensing.png"))


# ---------------------------------------------------------------- f10
def f10():
    """リード抜去手術の体制"""
    cv = Canvas(W, 900)
    cap(cv, 44, "リード抜去は「デバイスの処置」ではなく「大血管手術」として準備する")

    C = [("なぜ抜くのか", GREEN, "#eaf5ee",
          ["リード関連感染・全身感染", "断線・機能不全", "静脈閉塞",
           "MRI や再植込みのため"]),
         ("何が起こりうるか", RED, "#fceeec",
          ["上大静脈裂傷", "心タンポナーデ", "三尖弁損傷",
           "肺塞栓・肺水腫", "突然の循環虚脱"]),
         ("だから何を用意するか", BLUE, "#eaf1f8",
          ["太い静脈路と動脈圧ライン", "交差適合済みの血液",
           "TEE と心嚢液の評価", "心臓外科と人工心肺の待機",
           "体外ペーシングの経路"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 130, w, t, lines, col, fc,
             body_size=10.6, lh=1.8)

    textbox(cv, 70, 520, W - 140,
            ["ペーシング依存の患者からリードを抜くということは、",
             "手術の途中で「ペーシングの出口が一時的になくなる」ということである。",
             "体外ペーシングをどの経路で確保するかを、切開の前に決めておく。"],
            10.8, style="amber", title="麻酔科が最初に確認すること",
            title_color="#9a6510", pad_y=16)

    msg(cv, 740,
        "2026 年の HRS ほか合同コンセンサスは、施設要件と多職種体制を明文化している",
        fc="#e8edf5", ec=NAVY, tc=NAVY)
    cv.save(P("f10_lead_extraction.png"))


# ---------------------------------------------------------------- f11
def f11():
    """Alg1-1 CIED 患者が手術に来たら"""
    cv = Canvas(W, 1900)
    cap(cv, 44, "アルゴリズム 1　CIED 患者が手術に来たら")

    cx = W / 2
    bw = 700
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["手帳・カード・胸部 X 線・遠隔モニタリング記録を集める",
              "メーカー・機種・植込み日・最終チェック日を特定する"],
             style="navy", title="① デバイスを同定する", title_color=NAVY)
    y2 = y + h
    down(cv, cx, y2, y2 + 46)
    y = y2 + 46
    h = step(cv, cx - bw / 2, y, bw,
             ["自己調律はあるか　　ペーシング率はどれくらいか",
              "止まったときに血行動態が保てるか"],
             style="red", title="② ペーシング依存かどうかを決める",
             title_color=RED)
    y2 = y + h
    down(cv, cx, y2, y2 + 46)
    y = y2 + 46
    h = step(cv, cx - bw / 2, y, bw,
             ["術野と本体・リードの位置関係　　モノポーラを使うか",
              "対極板をどこに貼るか　　通電は長いか短いか"],
             style="amber", title="③ EMI が起きそうかを見積もる",
             title_color="#9a6510")
    y2 = y + h
    down(cv, cx, y2, y2 + 52)

    # 分岐
    yb = y2 + 52
    cw = 460
    lx, rx = 70, W - 70 - cw
    side(cv, cx - 40, lx + cw + 10, yb + 60)
    side(cv, cx + 40, rx - 10, yb + 60)
    hl = step(cv, lx, yb, cw,
              ["ICD の頻拍治療を止めたいだけなら magnet でよい",
               "術中も磁石の位置がずれないことを確認する",
               "外した時点で治療は再開する"],
              style="green", title="magnet で足りる場合", title_color=GREEN)
    hr = step(cv, rx, yb, cw,
              ["ペーシング依存＋本体近傍でのモノポーラ",
               "magnet 応答が不明・反応しない機種",
               "S-ICD や leadless で magnet が使えない",
               "体位の都合で磁石を保持できない"],
              style="red", title="再プログラミングが要る場合",
              title_color=RED)
    yb2 = yb + max(hl, hr)
    down(cv, lx + cw / 2, yb2, yb2 + 44)
    down(cv, rx + cw / 2, yb2, yb2 + 44)
    y = yb2 + 44
    h = step(cv, cx - bw / 2, y, bw,
             ["体外ペーシング（経皮パッド）を貼り、位置を確認する",
              "除細動パッドは本体から離し、前後方向に貼る",
              "薬剤（アトロピン・イソプロテレノールなど）を手元に置く"],
             style="blue", title="④ どちらを選んでもバックアップを用意する",
             title_color=BLUE)
    y2 = y + h
    down(cv, cx, y2, y2 + 46)
    y = y2 + 46
    h = step(cv, cx - bw / 2, y, bw,
             ["設定を変えたなら、変えた人が戻すまで監視を続ける",
              "magnet だけなら、外したあとに作動状況を確認する",
              "誰がいつ interrogation するかを術前に決めておく"],
             style="purple", title="⑤ 術後に元へ戻す", title_color=PURPLE)
    cv.save(P("f11_alg_cied.png"))
    crop_bottom(P("f11_alg_cied.png"))


# ---------------------------------------------------------------- f12
def f12():
    """Alg1-2 ペーシング依存＋モノポーラ"""
    cv = Canvas(W, 1900)
    cap(cv, 44, "アルゴリズム 2　ペーシング依存の患者にモノポーラを使うとき")

    cx = W / 2
    bw = 760
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["ペーシング依存であることを術前に確認した",
              "術野は本体・リードの近く（胸部・頭頸部・上肢）である"],
             style="navy", title="前提", title_color=NAVY)
    y = y + h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["非同期モード（DOO・VOO など）にすれば抑制は起きない",
              "ただしレートは自己調律と競合しない値を選ぶ",
              "ICD では magnet で非同期にはならない。設定変更が要る"],
             style="green", title="まず非同期化を考える", title_color=GREEN)
    y = y + h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["対極板は術野の反対側に貼り、電流路が本体とリードを横切らないようにする",
              "可能ならバイポーラや超音波凝固に替える",
              "通電は短く、連続凝固を避ける"],
             style="amber", title="電流路を設計する", title_color="#9a6510")
    y = y + h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["体外ペーシングパッドを貼ってから入室させる",
              "心電図だけでなく、脈波（SpO2・観血的動脈圧）で拍出を確認する",
              "電気メスのアーチファクトで心電図が読めない前提で監視する"],
             style="blue", title="止まったときに気づける監視にする",
             title_color=BLUE)
    y = y + h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["通電を止める　　磁石があれば外す（あるいは当てる）",
          "体外ペーシングを開始する　　術者に手を止めてもらう",
          "原因を確かめてから再開する"],
         style="red", title="それでもペーシングが出なくなったら",
         title_color=RED)
    cv.save(P("f12_alg_dependent.png"))
    crop_bottom(P("f12_alg_dependent.png"))


# ---------------------------------------------------------------- f13
def f13():
    """Alg1-3 ICD 患者の手術"""
    cv = Canvas(W, 1900)
    cap(cv, 44, "アルゴリズム 3　ICD が入っている患者の手術")

    cx = W / 2
    bw = 780
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["EMI が予想されるなら、頻拍治療は止めておく",
              "止める手段は magnet か再プログラミングのどちらか"],
             style="navy", title="① 頻拍治療を止めるかどうか",
             title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    cw = 520
    lx, rx = 70, W - 70 - cw
    hl = step(cv, lx, y, cw,
              ["磁石を確実に保持できる体位・術野である",
               "その機種が magnet で治療停止することを確認した",
               "外せば即座に復帰する"],
              style="green", title="magnet を選ぶ", title_color=GREEN)
    hr = step(cv, rx, y, cw,
              ["ペーシング依存で非同期化も必要",
               "磁石を保持できない（腹臥位・術野が胸部）",
               "magnet 応答が特殊、または無効化されている"],
              style="red", title="再プログラミングを選ぶ", title_color=RED)
    y += max(hl, hr)
    down(cv, lx + cw / 2, y, y + 44)
    down(cv, rx + cw / 2, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["体外除細動パッドを貼る（本体から離し、前後方向）",
              "治療を止めている間は、心電図を見る人を決めておく",
              "抗頻拍治療が止まっている＝VT/VF は自分たちで治療する"],
             style="blue", title="② 止めている間の安全装置", title_color=BLUE)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["磁石を外す、あるいは設定を戻す",
          "戻ったことを確認するまで監視を続ける",
          "術中に不適切作動があれば、その記録を残す"],
         style="purple", title="③ 手術が終わったら", title_color=PURPLE)
    cv.save(P("f13_alg_icd.png"))
    crop_bottom(P("f13_alg_icd.png"))


# ---------------------------------------------------------------- f14
def f14():
    """Alg1-4 リード抜去の周術期"""
    cv = Canvas(W, 1900)
    cap(cv, 44, "アルゴリズム 4　リード抜去手術の周術期")

    cx = W / 2
    bw = 780
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["リードの本数・植込み年数・固定方法を確認する",
              "感染の範囲（ポケットか全身か）を把握する",
              "ペーシング依存かどうかを必ず確かめる"],
             style="navy", title="① 術前", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    h = step(cv, cx - bw / 2, y, bw,
             ["太い静脈路・観血的動脈圧・交差適合済み血液",
              "TEE を使える体制（心嚢液と血行動態の評価）",
              "心臓外科と人工心肺の待機、開胸の可否を確認",
              "ペーシング依存なら体外ペーシングの経路を先に確保"],
             style="red", title="② 入室前に整えるもの", title_color=RED)
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    h = step(cv, cx - bw / 2, y, bw,
             ["牽引や拡張シースの操作中は血圧から目を離さない",
              "突然の低血圧＝まず心タンポナーデと大血管裂傷を疑う",
              "TEE で心嚢液を確認し、輸血と開胸の判断を同時に進める"],
             style="amber", title="③ 術中", title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    step(cv, cx - bw / 2, y, bw,
         ["再植込みまでの間、徐脈をどう支えるかを決めておく",
          "感染例では培養と抗菌薬の期間を循環器・感染症科と共有する",
          "一時ペーシングのまま病棟へ戻す場合の監視体制を決める"],
         style="purple", title="④ 術後", title_color=PURPLE)
    cv.save(P("f14_alg_extraction.png"))
    crop_bottom(P("f14_alg_extraction.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f08, f09, f10, f11, f12, f13, f14):
        fn()
        print("ok", fn.__name__)
