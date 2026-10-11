# -*- coding: utf-8 -*-
"""第15巻 手術体位と末梢神経障害 図版 f15〜f21"""
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


# ---------------------------------------------------------------- f15
def f15():
    W, H = 1520, 660
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "ロボット骨盤手術 —— 一つの複合体位として扱う",
             size=12.5, ha="center")
    ITEMS = [("砕石位", "#c0392b", "下肢神経と灌流"),
             ("急峻頭低位", "#7b52a8", "腕神経叢とずれ"),
             ("気腹", "#2e6da4", "静脈還流と腹圧"),
             ("長時間", "#b8760f", "累積する圧迫と虚血"),
             ("ドッキング", "#1f6b47", "再体位が容易でない")]
    L, R = 48, W - 48
    GAP = 14
    CW = (R - L - GAP * 4) / 5
    TOP, HH = 92, 50
    BTOP = TOP + HH + 8
    bsz = min(cv.fit_size([i[2] for i in ITEMS], CW - 34, 9.8), 9.8)
    BH = 30 + LH(bsz, 1.0) + 22
    for i, (head, col, body) in enumerate(ITEMS):
        x = L + i * (CW + GAP)
        cv.box(x, TOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, TOP + HH / 2, head, size=11.0, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.6, radius=7)
        cv.text(x + CW / 2, BTOP + BH / 2, body, size=bsz, color=INK)
        cv.arrow((x + CW / 2, BTOP + BH + 2), (x + CW / 2, BTOP + BH + 30),
                 color="#8d97a3", lw=2.0, head=8)
    # 中段：数値の読み方
    my = BTOP + BH + 36
    MSG = "同じ「位置関連障害」でも 0.8〜6.6% と幅がある —— 定義・追跡・術式・経験曲線が違う"
    msz = cv.fit_size([MSG], R - L - 60, 12, weight="bold")
    mh = 30 + LH(msz, 1.5)
    cv.box(L, my, R - L, mh, fc="#fbeeee", ec="#c0392b", lw=2.0, radius=8)
    cv.text(W / 2, my + mh / 2, MSG, size=msz, color="#9c2b26", weight="bold")
    # 下段：時点ごとの確認
    ROWS = [("ドッキング前", "#1f6b47",
             "滑り止め、肩固定具の要否、上肢中間位、手指、腓骨頭、股関節角度をチームで確認"),
            ("長時間化", "#b8760f",
             "時間、台角度、血圧、末梢浮腫、下肢支持、上肢のずれを再確認"),
            ("術後", "#c0392b",
             "上肢・下肢の感覚運動を術前所見と比較。進行する疼痛と緊満を確認")]
    ry = my + mh + 26
    NAME_SZ = 10.8
    NAMEW = max(cv.measure(r[0], NAME_SZ, weight="bold")[0] for r in ROWS) + 44
    rsz = min(cv.fit_size([r[2] for r in ROWS], R - L - NAMEW - 70, 9.9), 9.9)
    RH = 34 + LH(rsz, 1.0) * 0.5 + 22
    for i, (name, col, body) in enumerate(ROWS):
        y = ry + i * (RH + 12)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.7, radius=7)
        cv.box(L, y, NAMEW, RH, fc=col, ec=col, lw=0, radius=7)
        cv.text(L + NAMEW / 2, y + RH / 2, name, size=NAME_SZ, color="white",
                weight="bold")
        cv.text(L + NAMEW + 30, y + RH / 2, body, size=rsz, color=INK,
                ha="left")
    cv.save(P("f15_robotic.png"))


# ---------------------------------------------------------------- f16
def f16():
    W, H = 1520, 560
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "心臓手術の上肢障害 —— 体位だけの問題ではない",
             size=12.5, ha="center")
    COLS = [
        ("胸骨開創", "#c0392b",
         ["鎖骨と第1肋骨のあいだで腕神経叢が圧迫される",
          "左右非対称・過度の開創で固定点間距離が伸び、牽引が加わる"]),
        ("内胸動脈採取", "#b8760f",
         ["開創が片側に偏りやすい",
          "同側の神経叢への負荷が増える"]),
        ("循環・全身条件", "#2e6da4",
         ["体外循環、低灌流、低体温、浮腫",
          "糖尿病・動脈硬化・既存の神経症状が背景にある"]),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 92, 52
    BTOP = HTOP + HH + 8
    bsz = min(cv.fit_size(["・" + l for c in COLS for l in c[2]], CW - 46, 9.8),
              9.8)
    nl = max(sum(len(cv.wrap(l, CW - 52, bsz)) for l in c[2]) for c in COLS)
    BH = 30 + LH(bsz, 1.6) * (nl - 1) + LH(bsz, 1.0) * 0.5 + 22
    for i, (head, col, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.4, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        k = 0
        for ln in lines:
            for j, sub in enumerate(cv.wrap(ln, CW - 52, bsz)):
                cv.text(x + 24, BTOP + 30 + LH(bsz, 1.6) * k,
                        ("・" if j == 0 else "　") + sub, size=bsz, color=INK,
                        ha="left")
                k += 1
    NOTE = ("※ 電気生理学的な異常を積極的に拾った研究の数値を、"
            "一般外科の「臨床症状の発生率」と単純に比べない。"
            "術後に手指のしびれを診たら、尺骨神経単独か、神経叢レベルか、既存障害の症候化かを分けて考える。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, BTOP + BH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f16_sternotomy.png"))


# ---------------------------------------------------------------- f17
def f17():
    W, H = 1520, 620
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "パッドは「置く」のではなく、荷重を分散する",
             size=12.5, ha="center")
    PANELS = [
        ("悪い例", "#c0392b", False,
         ["神経走行部を局所的に締めつける", "硬い接触面に荷重が集中する",
          "パッドそのものが新しい圧迫点になる"]),
        ("良い例", "#1f6b47", True,
         ["荷重を広い面に分散する", "骨突出部の接触圧を下げる",
          "皮膚・しわ・異物・ラインを毎回確認する"]),
    ]
    L, GAPX = 70, 60
    PW = (W - L * 2 - GAPX) / 2.0
    PTOP = 88
    ILL = 190
    bsz = min(cv.fit_size(["・" + l for p in PANELS for l in p[3]],
                          PW - 56, 10.0), 10.0)
    PH = 40 + ILL + 22 + LH(bsz, 1.85) * 2 + LH(bsz, 1.0) * 0.5 + 22
    for i, (title, col, good, lines) in enumerate(PANELS):
        px = L + i * (PW + GAPX)
        cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
        cv.text(px + PW / 2, PTOP + 30, title, size=12, color=col,
                weight="bold")
        # 支持面と骨突出部
        sy = PTOP + 40 + ILL - 46
        ax.add_patch(Rectangle((px + 50, sy), PW - 100, 20,
                               facecolor="#cfd6de", edgecolor="#9aa4b0",
                               lw=1.4, zorder=2))
        cxx = px + PW / 2
        # パッド
        if good:
            ax.add_patch(Ellipse((cxx, sy - 12), PW - 160, 52,
                                 facecolor="#dceaf5", edgecolor="#5b8fd0",
                                 lw=1.8, zorder=3))
        else:
            ax.add_patch(Rectangle((cxx - 40, sy - 34), 80, 34,
                                   facecolor="#fbe3d6", edgecolor="#c0392b",
                                   lw=1.8, zorder=3))
        # 骨突出部
        ax.add_patch(Circle((cxx, sy - 54), 34, facecolor="#e6dfd3",
                            edgecolor="#b8ac99", lw=1.8, zorder=4))
        cv.text(cxx, sy - 54, "骨", size=9.4, color="#8a7a63", z=5)
        # 荷重の矢印
        if good:
            for dx in (-96, -48, 0, 48, 96):
                cv.arrow((cxx + dx, sy - 96), (cxx + dx, sy - 30),
                         color=col, lw=1.6, head=7, z=6)
        else:
            cv.arrow((cxx, sy - 108), (cxx, sy - 30), color=col, lw=3.4,
                     head=12, z=6)
        for j, ln in enumerate(lines):
            cv.text(px + 26, PTOP + 40 + ILL + 26 + LH(bsz, 1.85) * j,
                    "・" + ln, size=bsz, color=INK, ha="left")
    NOTE = ("※ パッドは厚さではなく、局所圧を広い面に分散できているかで評価する。"
            "支持具が体格と関節可動域に合っているか、ライン・チューブ・金具が神経走行部に重なっていないかも見る。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, PTOP + PH + 32 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f17_padding.png"))


# ---------------------------------------------------------------- f18
def f18():
    W, H = 1520, 530
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "長時間症例では、体位を繰り返し再評価する",
             size=12.5, ha="center")
    STEPS = [("① 置く", "#1f6b47", "体位を作り、圧迫点を確認する"),
             ("② 見る", "#2e6da4", "ずれ、角度、支持具、皮膚、灌流"),
             ("③ 直す", "#7b52a8", "可能な範囲で緩める・戻す"),
             ("④ 記録する", "#b8760f", "時刻・変更内容・循環イベント"),
             ("⑤ 引き継ぐ", "#c0392b", "次の担当と術後の観察者へ")]
    L, R = 48, W - 48
    GAP = 14
    CW = (R - L - GAP * 4) / 5
    TOP, HH = 96, 52
    BTOP = TOP + HH + 8
    bsz = min(cv.fit_size([s[2] for s in STEPS], CW - 34, 9.8), 9.8)
    nl = max(len(cv.wrap(s[2], CW - 34, bsz)) for s in STEPS)
    BH = 28 + LH(bsz, 1.45) * (nl - 1) + LH(bsz, 1.0) * 0.5 + 20
    for i, (head, col, body) in enumerate(STEPS):
        x = L + i * (CW + GAP)
        cv.box(x, TOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, TOP + HH / 2, head, size=11.2, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.7, radius=7)
        for j, sub in enumerate(cv.wrap(body, CW - 34, bsz)):
            cv.text(x + CW / 2, BTOP + 28 + LH(bsz, 1.45) * j, sub, size=bsz,
                    color=INK)
        if i < len(STEPS) - 1:
            cv.arrow((x + CW + 1, TOP + HH / 2), (x + CW + GAP - 1, TOP + HH / 2),
                     color="#8d97a3", lw=2.0, head=9)
    # ②へ戻るループ
    ly = BTOP + BH + 26
    x2 = L + 1 * (CW + GAP) + CW / 2
    x5 = L + 4 * (CW + GAP) + CW / 2
    ax.plot([x5, x5], [BTOP + BH, ly], color="#8d97a3", lw=2.0, zorder=3)
    ax.plot([x2, x5], [ly, ly], color="#8d97a3", lw=2.0, zorder=3)
    cv.arrow((x2, ly), (x2, BTOP + BH + 2), color="#8d97a3", lw=2.0, head=9)
    cv.text((x2 + x5) / 2, ly + 22, "②へ戻る", size=9.6, color="#5d6875")
    # 再評価のきっかけ
    TRIG = ["予定より長くなった", "台の角度を変えた", "出血・昇圧薬が増えた",
            "気腹を開始・変更した", "手術チームが交代した"]
    ty = ly + 48
    tsz = min(cv.fit_size(TRIG, (R - L - 60) / 5 - 24, 10.2), 10.2)
    TH = 40 + LH(tsz, 1.0) + 24
    cv.box(L, ty, R - L, TH, fc="#f2f5f8", ec="#5d6875", lw=1.8, radius=8)
    cv.text(L + 24, ty + 28, "再評価のきっかけ", size=10.6, color=NAVY,
            weight="bold", ha="left")
    cw2 = (R - L - 48) / 5
    for i, t in enumerate(TRIG):
        cv.text(L + 24 + cw2 * (i + 0.5) - cw2 / 2 + cw2 / 2,
                ty + TH - 26, t, size=tsz, color=INK)
    NOTE = ("※ 時刻は一律の閾値ではない。体位変換の直後に一度確認するだけでは、"
            "術中のずれ・台の傾斜・ロボットアーム・支持具の移動・浮腫・低体温・血圧変動を捕まえられない。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, ty + TH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f18_reassess_loop.png"))


# ---------------------------------------------------------------- f19
def f19():
    W, H = 1520, 720
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "術後に神経症状を疑ったら —— 局在化と緊急度を同時に進める",
             size=12.5, ha="center")
    TOPBOX = "術後に、しびれ・筋力低下・疼痛を訴えた／診察で見つけた"
    L, R = 52, W - 52
    tsz = cv.fit_size([TOPBOX], R - L - 60, 12, weight="bold")
    th = 30 + LH(tsz, 1.5)
    cv.box(L, 88, R - L, th, fc="#eef1f5", ec="#5d6875", lw=1.9, radius=8)
    cv.text(W / 2, 88 + th / 2, TOPBOX, size=tsz, color=NAVY, weight="bold")
    y0 = 88 + th
    cv.arrow((W / 2, y0 + 2), (W / 2, y0 + 30), color="#8d97a3", lw=2.2,
             head=9)
    # 2分岐
    BR = [
        ("緊急", "#c0392b", "#fbeeee",
         ["進行する強い疼痛、他動伸展痛", "著明な緊満・腫脹、冷感・変色",
          "急速に進む運動低下"],
         ["圧迫・体位を直ちに解除する", "WLCS・血管障害・血腫・圧迫性病変を除外する",
          "関連診療科へ直ちに連絡する"]),
        ("局在化して追う", "#2e6da4", "#eaf1f8",
         ["限局した感覚異常", "進行しない", "疼痛・腫脹・色調変化を伴わない"],
         ["術前所見・体位・支持具・時間・循環を記録する",
          "経時的に比較する（単回評価にしない）",
          "運動障害が続くなら神経内科・専門科と評価計画を立てる"]),
    ]
    by = y0 + 36
    GAPX = 40
    BW = (R - L - GAPX) / 2.0
    ssz = min(cv.fit_size(["・" + l for b in BR for l in b[3] + b[4]],
                          BW - 56, 9.9), 9.9)
    HH = 48
    S1 = 26 + LH(ssz, 1.75) * 2 + LH(ssz, 1.0) * 0.5 + 18
    S2 = 26 + LH(ssz, 1.9) * 2 + LH(ssz, 1.0) * 0.5 + 18
    for i, (head, col, fc, signs, acts) in enumerate(BR):
        x = L + i * (BW + GAPX)
        cv.box(x, by, BW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + BW / 2, by + HH / 2, head, size=12, color="white",
                weight="bold")
        cv.box(x, by + HH + 8, BW, S1, fc=fc, ec=col, lw=1.7, radius=8)
        for j, ln in enumerate(signs):
            cv.text(x + 24, by + HH + 34 + LH(ssz, 1.75) * j, "・" + ln,
                    size=ssz, color=INK, ha="left")
        ay = by + HH + 8 + S1
        cv.arrow((x + BW / 2, ay + 2), (x + BW / 2, ay + 26), color=col,
                 lw=2.2, head=9)
        cv.box(x, ay + 32, BW, S2, fc="white", ec=col, lw=1.7, radius=8)
        for j, ln in enumerate(acts):
            for k, sub in enumerate(cv.wrap(ln, BW - 56, ssz)):
                cv.text(x + 24, ay + 58 + LH(ssz, 1.9) * j + LH(ssz, 1.3) * k,
                        ("・" if k == 0 else "　") + sub, size=ssz, color=INK,
                        ha="left")
    NOTE = ("※ 局在化は診断の終点ではなく、緊急病態を除外するための手段である。"
            "区域麻酔、術後鎮痛、浮腫、せん妄、既存の神経疾患は所見を曖昧にする。単回評価より経時比較。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, by + HH + 8 + S1 + 32 + S2 + 34 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f19_postop_flow.png"))


# ---------------------------------------------------------------- f20
def f20():
    W, H = 1520, 560
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "術後診察の最小セット —— 「しびれがありますか」で終わらせない",
             size=12.5, ha="center")
    COLS = [
        ("感覚", "#2e6da4",
         ["左右を比較する", "指・足背・足底・大腿の内外側",
          "疼痛の性質（灼熱感か、鈍いか）"],
         "左第4・5指の触覚低下、右との差"),
        ("運動", "#1f6b47",
         ["把握、手指の外転", "足の背屈", "膝伸展、股関節の内転"],
         "足背屈 MRC 3/5、膝伸展 5/5"),
        ("循環・筋区画", "#c0392b",
         ["色、温度、腫脹、緊満", "他動伸展痛", "脈拍（触れても否定できない）"],
         "下腿前方区画の緊満、足趾の他動伸展で疼痛"),
        ("時間経過", "#b8760f",
         ["いつ気づいたか", "進行しているか", "術前との比較"],
         "回復室ではなし、病棟で増悪"),
    ]
    L, R = 44, W - 44
    GAP = 16
    CW = (R - L - GAP * 3) / 4
    HTOP, HH = 92, 50
    BTOP = HTOP + HH + 8
    bsz = min(cv.fit_size(["・" + l for c in COLS for l in c[2]], CW - 40, 9.6),
              9.6)
    esz = min(cv.fit_size([c[3] for c in COLS], CW - 46, 9.2), 9.2)
    nel = max(len(cv.wrap(c[3], CW - 46, esz)) for c in COLS)
    BH = 28 + LH(bsz, 1.85) * 2 + 30 + LH(esz, 1.4) * nel + 18
    for i, (head, col, lines, ex) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.4, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            cv.text(x + 20, BTOP + 28 + LH(bsz, 1.85) * j, "・" + ln,
                    size=bsz, color=INK, ha="left")
        yy = BTOP + 28 + LH(bsz, 1.85) * 2 + 22
        cv.ax.plot([x + 20, x + CW - 20], [yy, yy], color=col, lw=1.0, ls=":",
                   zorder=4)
        for k, sub in enumerate(cv.wrap(ex, CW - 46, esz)):
            cv.text(x + CW / 2, yy + 22 + LH(esz, 1.4) * k, sub, size=esz,
                    color="#5d6875")
    NOTE = "※ 記録の目的は、原因を断定することではなく、次に診た人が変化を比較できるようにすることである。"
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, BTOP + BH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f20_postop_exam.png"))


# ---------------------------------------------------------------- f21
def f21():
    W, H = 1520, 620
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "声に出して確認する —— 4つの場面",
             size=12.5, ha="center")
    COLS = [
        ("麻酔導入前", "#1f6b47",
         ["既存の神経症状", "高リスク因子", "予想される体位と時間",
          "特殊な支持具の有無"]),
        ("体位固定後", "#2e6da4",
         ["頭頸部の位置", "上肢の角度と前腕の向き", "骨突出部と下肢支持",
          "手指・ライン・気道アクセス"]),
        ("長時間化・台角度変更", "#b8760f",
         ["ずれと圧迫点", "血圧・体温", "下肢の灌流",
          "再体位ができるかどうか"]),
        ("術後引継ぎ", "#c0392b",
         ["体位と固定時間", "特殊な支持具", "圧迫・循環のイベント",
          "比較すべき神経所見"]),
    ]
    L, R = 44, W - 44
    GAP = 16
    CW = (R - L - GAP * 3) / 4
    HTOP, HH = 92, 62
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size([l for c in COLS for l in c[2]], CW - 60, 9.8), 9.8)
    BH = 34 + LH(sz, 2.0) * 3 + LH(sz, 1.0) * 0.5 + 20
    for i, (head, col, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        for j, sub in enumerate(cv.wrap(head, CW - 30, 11.2)):
            cv.text(x + CW / 2, HTOP + HH / 2 - LH(11.2, 1.3)
                    * (len(cv.wrap(head, CW - 30, 11.2)) - 1) / 2
                    + LH(11.2, 1.3) * j, sub, size=11.2, color="white",
                    weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            yy = BTOP + 34 + LH(sz, 2.0) * j
            cv.ax.plot([x + 22, x + 34], [yy, yy], color=col, lw=1.6, zorder=4)
            for k, sub in enumerate(cv.wrap(ln, CW - 60, sz)):
                cv.text(x + 42, yy + LH(sz, 1.35) * k, sub, size=sz, color=INK,
                        ha="left")
    NOTE = ("※ 安全な体位は個人技ではなくチーム手順で守る。"
            "麻酔科は気道・ライン・循環・神経脆弱性、外科は術野・台角度・時間、"
            "看護師は支持具・皮膚・接触点・機器との干渉を見る。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, BTOP + BH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f21_checklist.png"))


for fn in (f15, f16, f17, f18, f19, f20, f21):
    fn()
    print("ok", fn.__name__)
