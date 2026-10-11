# -*- coding: utf-8 -*-
"""第13巻 気道管理 図版 f12〜f15"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle, Rectangle
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f12
def f12():
    W, H = 1520, 720
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "「見える線」と「チューブを通す線」は別物である",
             size=12.5, ha="center")
    PW, PTOP, PH = 690, 88, 344
    for px, title, col, mode, caption in (
            (56, "直接喉頭鏡", "#2e6da4", "dl",
             ["術者の目から声門まで一直線に見通す必要がある",
              "見えた＝同じ線でチューブも入る"]),
            (774, "ビデオ喉頭鏡（強湾曲）", "#c0392b", "vl",
             ["先端のカメラが曲がった先を映すので見通しは要らない",
              "見えていても、チューブの通り道は別に作らねばならない"])):
        cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
        cv.text(px + PW / 2, PTOP + 34, title, size=11.5, color=col,
                weight="bold")
        # 口腔〜咽頭〜喉頭の通路（曲がった管）
        tt = np.linspace(0, 1, 300)
        chx = px + 96 + 470 * tt
        chy = PTOP + 132 + 130 * tt ** 2.1
        ax.plot(chx, chy - 46, color="#c08d72", lw=3.0, zorder=3)
        ax.plot(chx, chy + 46, color="#c08d72", lw=3.0, zorder=3)
        ax.fill_between(chx, chy - 46, chy + 46, color="#f7e4da", zorder=2)
        gl = (chx[-1], chy[-1])
        ax.add_patch(Ellipse(gl, 40, 62, facecolor="#8f4a4a",
                             edgecolor="#5d2f2f", lw=1.6, zorder=5))
        cv.text(gl[0] + 34, gl[1], "声門", size=9.4, color="#8f4a4a",
                ha="left", z=6)
        eye = (px + 74, PTOP + 118)
        if mode == "dl":
            ax.add_patch(Circle(eye, 15, facecolor="#2e6da4",
                                edgecolor="none", zorder=6))
            cv.text(eye[0], eye[1] - 32, "術者の目", size=9.2, color="#2e6da4", z=6)
            ax.plot([eye[0], gl[0]], [eye[1], gl[1]], color="#2e6da4",
                    lw=2.6, zorder=6)
            cv.text((eye[0] + gl[0]) / 2, (eye[1] + gl[1]) / 2 - 22,
                    "見える線＝通す線", size=10, color="#2e6da4", weight="bold", z=7)
        else:
            cam = (chx[210], chy[210])
            ax.add_patch(Circle(cam, 14, facecolor="#1f6b47",
                                edgecolor="none", zorder=6))
            cv.text(cam[0] - 10, cam[1] - 34, "先端カメラ", size=9.2,
                    color="#1f6b47", ha="right", z=6)
            ax.plot([cam[0], gl[0]], [cam[1], gl[1]], color="#1f6b47",
                    lw=2.6, ls=(0, (5, 4)), zorder=6)
            cv.text(px + 300, PTOP + 108, "見える線（カメラ）", size=10,
                    color="#1f6b47", weight="bold", ha="left", z=7)
            ax.plot(chx, chy, color="#d98e2b", lw=3.4, zorder=6)
            cv.text(px + 250, PTOP + 268, "通す線（チューブ）", size=10,
                    color="#b8760f", weight="bold", ha="left", z=7)
        for i, ln in enumerate(caption):
            cv.text(px + PW / 2, PTOP + PH + 34 + LH(10, 1.42) * i, ln,
                    size=min(cv.fit_size([ln], PW - 30, 10), 10), color=INK)
    NOTE = ("※ 画面いっぱいに声門が映っていてもチューブが進まないのは、"
            "術者の腕でも器具の不良でもなく、この2本の線の食い違いによる。"
            "専用スタイレットで形を作り、必要なら角度を浅くして見え方を犠牲にする。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 140, 9.8)):
        cv.text(W / 2, H - 82 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f12_laryngoscope.png"))


# ---------------------------------------------------------------- f13
def f13():
    W, H = 1520, 700
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "Cormack-Lehane 分類と POGO —— 何が見えているかを言葉にする",
             size=12, ha="center")
    GRADES = [
        ("Grade 1", "声門が全部見える", 0.00, "POGO 100%"),
        ("Grade 2", "後方の一部のみ", 0.55, "POGO 20〜50%"),
        ("Grade 3", "喉頭蓋のみ", 1.00, "POGO 0%"),
        ("Grade 4", "喉頭蓋も見えない", 1.35, "POGO 0%"),
    ]
    PW, PTOP, PH = 340, 88, 292
    for i, (name, desc, occ, pogo) in enumerate(GRADES):
        px = 42 + i * (PW + 22)
        cv.box(px, PTOP, PW, PH, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
        cx, cy = px + PW / 2, PTOP + 176
        cv.text(cx, PTOP + 40, name, size=12, color=NAVY, weight="bold", z=9)
        ring = Ellipse((cx, cy), 190, 176, facecolor="#f3d9cd",
                       edgecolor="#b98f78", lw=2.2, zorder=2)
        ax.add_patch(ring)
        clip = Ellipse((cx, cy), 190, 176, transform=ax.transData)
        # 声門（三角）
        glo = Polygon([[cx, cy - 62], [cx - 30, cy + 56], [cx + 30, cy + 56]],
                      closed=True, facecolor="#3a3f4a", edgecolor="#d9dde3",
                      lw=2.0, zorder=4)
        ax.add_patch(glo)
        glo.set_clip_path(clip)
        for sgn in (-1, 1):
            band = Polygon([[cx + sgn * 4, cy - 62],
                            [cx + sgn * 34, cy + 56],
                            [cx + sgn * 52, cy + 56],
                            [cx + sgn * 12, cy - 62]], closed=True,
                           facecolor="#f0e2dc", edgecolor="#c9b3a9", lw=1.2,
                           zorder=5)
            ax.add_patch(band)
            band.set_clip_path(clip)
        # 喉頭蓋（上から降りて隠す）
        epi = Ellipse((cx, cy - 108 + occ * 132), 152, 92,
                      facecolor="#f2c4ae", edgecolor="#c08d72", lw=1.8,
                      zorder=6)
        ax.add_patch(epi)
        epi.set_clip_path(clip)
        if occ >= 1.3:
            tongue = Rectangle((cx - 100, cy - 20), 200, 130,
                               facecolor="#f2c4ae", edgecolor="none", zorder=7)
            ax.add_patch(tongue)
            tongue.set_clip_path(clip)
        ax.add_patch(Ellipse((cx, cy), 190, 176, facecolor="none",
                             edgecolor="#b98f78", lw=2.4, zorder=8))
        cv.text(cx, PTOP + PH + 30, desc, size=9.8, color=INK)
        cv.text(cx, PTOP + PH + 30 + LH(9.8, 1.5), pogo, size=9.8,
                color="#2e6da4", weight="bold")
    NOTE = ("※ Cormack-Lehane は直接喉頭鏡の視野の分類である。"
            "ビデオ喉頭鏡の画面所見に同じ Grade を当てると、"
            "直視下の難易度を過小評価する。記録には器具名も併記する。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 140, 9.8)):
        cv.text(W / 2, H - 76 + LH(9.8, 1.45) * i, ln, size=9.8, color="#5d6875")
    cv.save(P("f13_cl_pogo.png"))


# ---------------------------------------------------------------- f14
def f14():
    W, H = 1520, 800
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "覚醒下気管挿管 —— 自発呼吸と気道反射を手放さない",
             size=12.5, ha="center")
    STEPS = [
        ("① 適応を決める", "気道の狭窄・偏位、高度開口障害、換気困難の予想。"
                       "「導入したら戻れない」と判断したら覚醒下を選ぶ"),
        ("② 説明と同意", "何をするか、どこまで苦しいか、途中で中止する条件を伝える"),
        ("③ 酸素と抗コリン薬", "経鼻から酸素を流し続ける。分泌を減らすと表面麻酔が効く"),
        ("④ 表面麻酔", "鼻腔・咽頭・喉頭・気管へ段階的に。総投与量の上限を必ず計算する"),
        ("⑤ 鎮静は最小限", "自発呼吸と気道反射を保てる深さまで。"
                       "過量投与は覚醒下挿管を「無呼吸の緊急挿管」に変える"),
        ("⑥ 挿管と確認", "気管支鏡またはビデオ喉頭鏡で声門を通す。"
                      "波形カプノグラムを確認してから麻酔導入へ進む"),
    ]
    L, R = 60, W - 60
    TOP, RH, GAP = 100, 86, 13
    head_sz = 11
    body_sz = min(cv.fit_size([s[1] for s in STEPS], R - L - 300, 9.6), 9.6)
    for i, (head, body) in enumerate(STEPS):
        y = TOP + i * (RH + GAP)
        fc, ec = ("#eaf1f8", "#2e6da4") if i < 5 else ("#eaf4ee", "#1f6b47")
        cv.box(L, y, R - L, RH, fc=fc, ec=ec, lw=1.8, radius=8)
        cv.text(L + 28, y + RH / 2, head, size=head_sz, color=ec,
                weight="bold", ha="left")
        lines = cv.wrap(body, R - L - 320, body_sz)
        lh = LH(body_sz, 1.4)
        cy = y + RH / 2 - lh * (len(lines) - 1) / 2
        for j, ln in enumerate(lines):
            cv.text(L + 280, cy + lh * j, ln, size=body_sz, color=INK, ha="left")
        if i < len(STEPS) - 1:
            cv.arrow((W / 2, y + RH + 1), (W / 2, y + RH + GAP - 1),
                     color="#8d97a3", lw=2.0, head=8)
    NOTE = ("※ 中止の条件（酸素化の低下、出血、分泌過多、患者の協力不良）を"
            "始める前に決めておく。中止は失敗ではなく、計画の一部である。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 140, 9.8)):
        cv.text(W / 2, TOP + 6 * (RH + GAP) + 26 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f14_awake.png"))


# ---------------------------------------------------------------- f15
def f15():
    W, H = 1520, 726
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "予期せぬ挿管困難 —— Plan A から D へ、同じ手を繰り返さない",
             size=12.5, ha="center")
    ROWS = [
        ("Plan A", "#0f5c3f", "気管挿管",
         ["最適化して3回まで（術者交代は1回）", "体位・器具・ブジー・外部喉頭操作を変える"]),
        ("Plan B", "#173a6d", "SGA で換気を回復",
         ["第2世代 SGA を挿入し、酸素化を立て直す", "成功したら次の一手を落ち着いて選ぶ"]),
        ("Plan C", "#94620f", "フェイスマスク換気",
         ["2人法＋エアウェイ、十分な筋弛緩", "換気できたら覚醒させて出直す"]),
        ("Plan D", "#8f2b28", "CICO を宣言し前頸部へ",
         ["挿管不能・マスク不能・SGA 不能が揃った時点で宣言",
          "メス・ブジー・チューブ法へ移る"]),
    ]
    L, R = 56, W - 56
    BADGE_W, GAP = 150, 20
    MIDW = 330
    TOP, RH, RGAP = 106, 96, 16
    RIGHT_X = L + BADGE_W + GAP + MIDW + GAP
    body_sz = min(cv.fit_size([l for r in ROWS for l in r[3]],
                              R - RIGHT_X - 40, 9.8), 9.8)
    for i, (tag, col, mid, body) in enumerate(ROWS):
        y = TOP + i * (RH + RGAP)
        cv.box(L, y, BADGE_W, RH, fc=col, ec=col, lw=0, radius=7)
        cv.text(L + BADGE_W / 2, y + RH / 2, tag, size=12, color="white",
                weight="bold")
        mx = L + BADGE_W + GAP
        cv.box(mx, y, MIDW, RH, fc="#eef1f5", ec=col, lw=1.8, radius=8)
        cv.text(mx + MIDW / 2, y + RH / 2, mid,
                size=min(cv.fit_size([mid], MIDW - 30, 11.5, weight="bold"), 11.5),
                color=col, weight="bold")
        cv.box(RIGHT_X, y, R - RIGHT_X, RH, fc="white", ec="#c3ccd6",
               lw=1.5, radius=8)
        lh = LH(body_sz, 1.45)
        cy = y + RH / 2 - lh * (len(body) - 1) / 2
        for j, ln in enumerate(body):
            cv.text(RIGHT_X + 24, cy + lh * j, ln, size=body_sz, color=INK,
                    ha="left")
        if i < len(ROWS) - 1:
            cv.arrow((L + BADGE_W / 2, y + RH + 2),
                     (L + BADGE_W / 2, y + RH + RGAP - 2),
                     color="#8d97a3", lw=2.2, head=9)
    MSG = ["どの段でも共通するのは、酸素化を優先し、宣言し、応援を呼ぶこと。",
           "「あと1回」を積み重ねた結果が CICO である。"]
    by = TOP + 4 * (RH + RGAP) + 14
    msz = min(cv.fit_size(MSG, R - L - 60, 11), 11)
    mlh = LH(msz, 1.5)
    bh = 32 + mlh * len(MSG)
    cv.box(L, by, R - L, bh, fc="#e4f2f4", ec="#1f7f8b", lw=2.0, radius=8)
    cy = by + (bh - mlh * len(MSG)) / 2
    for i, ln in enumerate(MSG):
        cv.text(W / 2, cy + mlh * (i + 0.5), ln, size=msz, color="#0f6d78",
                weight="bold")
    cv.save(P("f15_plan_abcd.png"))


for fn in (f15,):
    fn()
    print("ok", fn.__name__)
