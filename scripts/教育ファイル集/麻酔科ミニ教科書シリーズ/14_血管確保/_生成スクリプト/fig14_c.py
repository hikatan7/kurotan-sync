# -*- coding: utf-8 -*-
"""第14巻 血管確保 図版 f15〜f18"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from figlib import Canvas, LH, NAVY, INK, JP

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f15
def f15():
    W, H = 1520, 748
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "入らないときに増やすのは、試行回数ではなく人手と道具である",
             size=12.5, ha="center")
    STEPS = [
        ("① 条件を整え直す", "#1f6b47",
         ["腕を心臓より下げる、温める、手を握ってもらう",
          "駆血帯は穿刺部の 10〜15 cm 近位に、動脈拍動が触れる強さで"]),
        ("② 部位を変える", "#2e6da4",
         ["同じ血管を刺し直さない。前腕の別区間、対側へ移る",
          "血腫のできた区間より近位を選ぶ"]),
        ("③ 超音波を出す", "#7b52a8",
         ["触知・視認できない、複数回失敗した、肥満・浮腫・薬物使用歴",
          "上腕の尺側皮静脈が標的。深さ 0.3〜1.5 cm、長めのカテーテルを使う"]),
        ("④ 人を替える", "#b8760f",
         ["回数の上限は刺す前に口に出しておく",
          "「あと1回」を積み重ねるほど、次の術者の条件も悪くなる"]),
        ("⑤ 経路を変える", "#c0392b",
         ["骨髄路、中心静脈、PICC を検討する",
          "薬剤が入らないこと自体が患者の不利益になっている、と考える"]),
    ]
    L, R = 52, W - 52
    TOP, RH, GAP = 100, 92, 14
    TAG_SZ = 10.8
    TAGW = max(cv.measure(s[0], TAG_SZ, weight="bold")[0] for s in STEPS) + 36
    body_sz = min(cv.fit_size([l for s in STEPS for l in s[2]],
                              R - L - TAGW - 90, 9.8), 9.8)
    for i, (head, col, lines) in enumerate(STEPS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L + 14, y + 16, TAGW, RH - 32, fc=col, ec=col, lw=0, radius=6)
        cv.text(L + 14 + TAGW / 2, y + RH / 2, head, size=TAG_SZ, color="white",
                weight="bold")
        for j, ln in enumerate(lines):
            cv.text(L + TAGW + 46, y + RH / 2 - LH(body_sz, 1.45) * 0.5
                    + LH(body_sz, 1.45) * j, ln, size=body_sz, color=INK,
                    ha="left")
        if i < len(STEPS) - 1:
            cv.arrow((L + 14 + TAGW / 2, y + RH + 1),
                     (L + 14 + TAGW / 2, y + RH + GAP - 1),
                     color="#8d97a3", lw=2.0, head=8)
    NOTE = ("※ 試行を重ねるほど血管壁の外傷・血腫・浮腫が蓄積し、"
            "そのあとの穿刺は自分にとっても次の術者にとっても難しくなる。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, TOP + 5 * (RH + GAP) + 26 + LH(9.8, 1.45) * i, ln,
                size=9.8, color="#5d6875")
    cv.save(P("f15_difficult_iv.png"))


# ---------------------------------------------------------------- f16
def f16():
    W, H = 1520, 500
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "感染対策 —— 手技ごとに必要なバリアは違う",
             size=12.5, ha="center")
    COLS = [
        ("末梢静脈路", "#eaf1f8", "#2e6da4",
         ["手指衛生", "アルコール含有クロルヘキシジンで消毒し、乾かす",
          "清潔手袋", "透明ドレッシングで刺入部が見えるように覆う"]),
        ("動脈ライン", "#fdf1e0", "#b8760f",
         ["手指衛生", "キャップ・マスク・滅菌手袋",
          "小型の滅菌有窓ドレープ", "超音波を使うならプローブカバーと滅菌ゲル"]),
        ("中心静脈カテーテル", "#fbeeee", "#c0392b",
         ["手指衛生", "マキシマル・バリア・プリコーション",
          "キャップ・マスク・滅菌ガウン・滅菌手袋", "全身を覆う大型滅菌ドレープ"]),
    ]
    L, R = 48, W - 48
    GAP = 22
    CW = (R - L - GAP * 2) / 3
    HTOP, HH = 96, 52
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size(["・" + l for c in COLS for l in c[3]], CW - 46, 9.8),
             9.8)
    BH = 30 + LH(sz, 1.7) * 3 + LH(sz, 1.0) * 0.5 + 18
    for i, (head, fc, ec, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=ec, ec=ec, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.4, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc=fc, ec=ec, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            cv.text(x + 24, BTOP + 30 + LH(sz, 1.7) * j, "・" + ln, size=sz,
                    color=INK, ha="left")
    MSG = "清潔なはずの視野に、非清潔のプローブが入ってくるのが最も多い破綻である"
    by = BTOP + BH + 28
    msz = cv.fit_size([MSG], R - L - 60, 11.5, weight="bold")
    bh = 30 + LH(msz, 1.5)
    cv.box(L, by, R - L, bh, fc="#fbeeee", ec="#c0392b", lw=2.0, radius=8)
    cv.text(W / 2, by + bh / 2, MSG, size=msz, color="#9c2b26", weight="bold")
    cv.save(P("f16_barrier.png"))


# ---------------------------------------------------------------- f17
def f17():
    W, H = 1520, 640
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "動脈と静脈を、画面上でどう見分けるか",
             size=12.5, ha="center")
    PANELS = [
        ("動脈", "#c0392b",
         ["拍動する", "圧迫しても潰れない", "円形を保つ", "壁が厚く輝度が高い"], False),
        ("静脈", "#2e6da4",
         ["拍動しない", "軽い圧迫で容易に潰れる", "不整形", "呼吸性に変動する"], True),
    ]
    L, GAPX = 70, 60
    PW = (W - L * 2 - GAPX) / 2.0
    PTOP = 88
    USW, USH = 214, 120        # 超音波像1枚の大きさ
    LAB = 26                   # 「圧迫なし／あり」ラベルの高さ
    BSZ = min(cv.fit_size(["・" + l for p in PANELS for l in p[2]],
                          PW - USW - 76, 10.4), 10.4)
    PH = 40 + LAB + USH + 16 + LAB + USH + 26
    for i, (title, col, lines, squash) in enumerate(PANELS):
        px = L + i * (PW + GAPX)
        cv.box(px, PTOP, PW, PH, fc="white", ec=col, lw=1.9, radius=8)
        cv.text(px + PW / 2, PTOP + 30, title, size=12, color=col,
                weight="bold")
        ux = px + 30
        for k, (tag, sq) in enumerate((("圧迫なし", False), ("圧迫あり", squash))):
            top = PTOP + 46 + k * (LAB + USH + 16)
            cv.text(ux, top + 10, tag, size=9.2, color="#5d6875", ha="left")
            uy = top + LAB
            ax.add_patch(Rectangle((ux, uy), USW, USH, facecolor="#2b2f36",
                                   edgecolor="none", zorder=2))
            vx, vy = ux + USW / 2, uy + USH / 2
            if sq:
                ax.add_patch(Rectangle((vx - 40, vy - 9), 80, 18,
                                       facecolor="#111417", edgecolor=col,
                                       lw=2.4, zorder=4))
            else:
                ax.add_patch(Circle((vx, vy), 36, facecolor="#111417",
                                    edgecolor=col, lw=2.6, zorder=4))
        for j, ln in enumerate(lines):
            cv.text(px + USW + 62, PTOP + 76 + LH(BSZ, 1.95) * j, "・" + ln,
                    size=BSZ, color=INK, ha="left")
    NOTE = ("※ 低血圧・低心拍出では動脈の拍動も弱くなる。血液の色と拍動だけで動静脈を判断しない ── "
            "ショックでは動脈血も暗色・非拍動性になりうる。迷ったら圧波形かカラードプラで確認する。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, PTOP + PH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f17_artery_vein.png"))


# ---------------------------------------------------------------- f18
def f18():
    W, H = 1520, 720
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "声に出して確認する —— 4つの場面",
             size=12.5, ha="center")
    COLS = [
        ("挿入前", "#1f6b47",
         ["本当にこのラインが必要か", "側・部位・灌流は適切か",
          "モニタ系と止血物品は準備済みか", "無菌操作と超音波の準備はできたか"]),
        ("穿刺中", "#2e6da4",
         ["針先を見失っていないか", "腫脹や抵抗はないか",
          "無理に押していないか", "何回で方針を変えるか"]),
        ("接続後・留置中", "#b8760f",
         ["波形は得られたか", "トランスデューサは心房位でゼロか",
          "気泡・屈曲・接続不良はないか", "刺入部・血腫・感染・末梢灌流・必要性"]),
        ("抜去時", "#c0392b",
         ["不要になったか", "抗凝固・出血リスクは",
          "十分な圧迫と止血確認をしたか", "遅発性の拍動性腫瘤はないか"]),
    ]
    L, R = 44, W - 44
    GAP = 16
    CW = (R - L - GAP * 3) / 4
    HTOP, HH = 96, 52
    BTOP = HTOP + HH + 8
    sz = min(cv.fit_size([l for c in COLS for l in c[2]], CW - 40, 9.8), 9.8)
    BH = 34 + LH(sz, 2.0) * 4
    for i, (head, col, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=11.4, color="white",
                weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.8, radius=8)
        for j, ln in enumerate(lines):
            yy = BTOP + 34 + LH(sz, 2.0) * j
            cv.ax.plot([x + 22, x + 34], [yy, yy], color=col, lw=1.6, zorder=4)
            for k, s in enumerate(cv.wrap(ln, CW - 60, sz)):
                cv.text(x + 42, yy + LH(sz, 1.35) * k, s, size=sz, color=INK,
                        ha="left")
    NOTE = ("※ 確認は頭の中でなく、声に出す。"
            "同じ失敗は同じ条件で必ず繰り返されるので、条件のほうを変える。")
    for i, ln in enumerate(cv.wrap(NOTE, W - 150, 9.8)):
        cv.text(W / 2, BTOP + BH + 34 + LH(9.8, 1.45) * i, ln, size=9.8,
                color="#5d6875")
    cv.save(P("f18_checklist.png"))


for fn in (f15, f16, f17, f18):
    fn()
    print("ok", fn.__name__)
