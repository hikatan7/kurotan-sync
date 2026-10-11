# -*- coding: utf-8 -*-
"""第Ⅳ章 M-TEER　図版 m01〜m07"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)
from fig1a import cap, msg, fitlines, card, W, TEAL
from figcrop import crop_bottom

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


def fit(cv, s, w, size, weight="normal"):
    return cv.fit_size([s], w, size, weight=weight)


# ---------------------------------------------------------------- m01
def m01():
    """Structural Heart の全体像"""
    cv = Canvas(W, 900)
    cap(cv, 44, "カテーテルで弁を治すという領域")

    cx = W / 2
    cv.box(cx - 260, 110, 520, 76, fc="#0f6d78", ec="#0f6d78", lw=0,
           radius=10)
    t = "構造的心疾患インターベンション"
    cv.text(cx, 148, t, size=fit(cv, t, 460, 13.6, "bold"), color="white",
            weight="bold")

    COL = [("大動脈弁", BLUE, "#eaf1f8",
            ["TAVI（経カテーテル大動脈弁置換）", "valve-in-valve",
             "弁尖切開（BASILICA）"]),
           ("僧帽弁", RED, "#fceeec",
            ["M-TEER（MitraClip・PASCAL）", "経カテーテル僧帽弁置換（TMVR）",
             "弁輪形成・傍弁逆流閉鎖"]),
           ("三尖弁", GREEN, "#eaf5ee",
            ["T-TEER（TriClip・PASCAL）", "経カテーテル三尖弁置換（EVOQUE）",
             "リードを跨ぐ治療"])]
    w = (W - 140 - 60) / 3
    for i, (t2, col, fc, lines) in enumerate(COL):
        x = 70 + (w + 30) * i
        cv.arrow((cx, 190), (x + w / 2, 236), color="#b9c2cc", lw=1.6, head=8)
        card(cv, x, 240, w, t2, lines, col, fc, body_size=10.2, lh=1.8)

    th = textbox(cv, 70, 530, W - 140,
                 ["この領域に共通するのは、"
                  "「開胸できない患者に、カテーテルで弁を治す」という前提である。",
                  "したがって患者は高齢で、心機能が悪く、併存疾患が多い。",
                  "麻酔科にとっては、手技そのものより"
                  "「その患者が手技に耐えられるか」が主題になる。"],
                 10.8, style="navy", title="共通する前提", title_color=NAVY,
                 pad_y=16)

    msg(cv, 530 + th + 28,
        "本章では僧帽弁の M-TEER を扱う。TAVI と三尖弁は第Ⅴ章で扱う")
    cv.save(P("m01_structural_heart.png"))
    crop_bottom(P("m01_structural_heart.png"))


# ---------------------------------------------------------------- m02
def m02():
    """M-TEER の手技ステップ"""
    cv = Canvas(W, 900)
    cap(cv, 44, "カテーテルはどこを通って僧帽弁に届くのか")

    STEP = [("① 大腿静脈", GREY, "穿刺・シース挿入"),
            ("② 右房", BLUE, "下大静脈から到達"),
            ("③ 心房中隔穿刺", RED, "ここが最初の山場"),
            ("④ 左房", PURPLE, "ガイドを進める"),
            ("⑤ 僧帽弁の上", TEAL, "クリップの向きを合わせる"),
            ("⑥ 弁尖を把持", ORANGE, "前尖と後尖をつかむ"),
            ("⑦ クリップ留置", GREEN, "逆流が減る")]

    x0, y0 = 90, 180
    bw, gap = (W - 180 - 6 * 22) / 7, 22
    for i, (t, col, sub) in enumerate(STEP):
        x = x0 + (bw + gap) * i
        cv.box(x, y0, bw, 172, fc="#ffffff", ec=col, lw=1.8, radius=10)
        cv.box(x, y0, bw, 46, fc=col, ec=col, lw=0, radius=10)
        cv.text(x + bw / 2, y0 + 23, t, size=fit(cv, t, bw - 16, 10.4, "bold"),
                color="white", weight="bold")
        for j, ln in enumerate(cv.wrap(sub, bw - 24, 9.6)):
            cv.text(x + bw / 2, y0 + 78 + LH(9.6, 1.35) * j, ln, size=9.6, color=INK)
        if i < 6:
            cv.arrow((x + bw + 2, y0 + 75), (x + bw + gap - 2, y0 + 75),
                     color="#b9c2cc", lw=1.8, head=9)

    KEY = [("心房中隔穿刺", RED, "#fceeec",
            ["針が左房に入る瞬間にタンポナーデが起こりうる",
             "穿刺の高さで、その後の操作性が決まる",
             "TEE（二平面・3D）で位置を確認しながら行う"]),
           ("弁尖の把持", ORANGE, "#fdf3e3",
            ["把持が浅いと、あとで外れる（SLDA）",
             "把持しすぎると、弁口が狭くなる",
             "この瞬間に何を見るかが、麻酔科の腕の見せどころ"])]
    w = (W - 140 - 30) / 2
    for i, (t, col, fc, lines) in enumerate(KEY):
        card(cv, 70 + (w + 30) * i, 390, w, t, lines, col, fc,
             body_size=10.4, lh=1.8)

    msg(cv, 690, "麻酔科医は、この七段階のどこにいるのかを常に把握しておく")
    cv.save(P("m02_procedure_steps.png"))
    crop_bottom(P("m02_procedure_steps.png"))


# ---------------------------------------------------------------- m03
def m03():
    """4 つの無作為化試験"""
    cv = Canvas(W, 1800)
    cap(cv, 44, "同じ治療なのに、試験によって結果が違った")

    ROWS = [("COAPT（2018）", GREEN, "614 例（機器 302／対照 312）",
             "心不全入院 35.8 対 67.9 件/患者年（HR 0.53、95%CI 0.40-0.70）",
             "5 年でも 33.1 対 57.2 件/年、全死亡 57.3% 対 67.2%", "有効"),
            ("MITRA-FR（2018）", RED, "304 例（各 152）",
             "1 年の死亡・心不全入院 54.6% 対 51.3%（OR 1.16、p=0.53）",
             "2 年でも差は生じなかった", "差なし"),
            ("RESHAPE-HF2（2024）", GREEN, "505 例（機器 250／対照 255）",
             "心不全入院・心血管死 37.0 対 58.9 件/100 患者年"
             "（率比 0.64、95%CI 0.48-0.85、p=0.002）",
             "中等度〜重度の MR を含む集団で有効性を示した", "有効"),
            ("MATTERHORN（2024）", BLUE, "210 例（TEER 対 外科手術）",
             "1 年の主要有効性エンドポイント 16.7% 対 22.5% で非劣性",
             "安全性イベントは TEER で少なかった", "外科に非劣性")]

    y = 130
    for name, col, pop, res1, res2, verdict in ROWS:
        h = 200
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.7, radius=10)
        cv.box(70, y, 330, h, fc="#fbfcfd", ec=col, lw=0, radius=10)
        cv.text(235, y + 54, name,
                size=fit(cv, name, 290, 12.0, "bold"), color=col,
                weight="bold")
        cv.box(96, y + 92, 278, 54, fc=col, ec=col, lw=0, radius=8)
        cv.text(235, y + 119, verdict,
                size=fit(cv, verdict, 250, 11.4, "bold"), color="white",
                weight="bold")
        cv.text(420, y + 46, pop, size=fit(cv, pop, W - 520, 10.2),
                color=GREY, ha="left")
        for j, ln in enumerate(cv.wrap(res1, W - 520, 10.6)):
            cv.text(420, y + 88 + LH(10.6, 1.5) * j, ln, size=10.6,
                    color=INK, ha="left")
        cv.text(420, y + 160, res2, size=fit(cv, res2, W - 520, 10.2),
                color=GREY, ha="left")
        y += h + 16

    textbox(cv, 70, y + 10, W - 140,
            ["COAPT と MITRA-FR は、同じ「二次性僧帽弁閉鎖不全」を対象にしながら、"
             "正反対の結果になった。",
             "違いを生んだのは、選んだ患者である。"
             "COAPT は逆流が重く左室がそれほど大きくない患者を、",
             "MITRA-FR は逆流の割に左室が大きい患者を多く含んでいた。"],
            10.6, style="navy", title="なぜ割れたのか", title_color=NAVY,
            pad_y=16)
    cv.save(P("m03_trials.png"))
    crop_bottom(P("m03_trials.png"))


# ---------------------------------------------------------------- m04
def m04():
    """比例・不比例の枠組み"""
    cv = Canvas(W, 960)
    cap(cv, 44, "逆流の重さは、左室の大きさとの釣り合いで決まる")

    x0, y0 = 500, 170
    pw, ph = 520, 380
    cv.rect(x0, y0, pw, ph, fc="#fbfcfd", ec="#dde3ea", lw=1.4)
    cv.ax.plot([x0, x0 + pw], [y0 + ph, y0], color="#b9c2cc", lw=2.0,
               linestyle="--")
    cv.text(x0 + pw * 0.30, y0 + ph * 0.86, "比例の線", size=9.8, color=GREY)
    cv.text(x0 + pw / 2, y0 + ph + 42, "左室の大きさ（拡張末期容積）",
            size=10.6, color=INK)
    cv.text(x0, y0 - 18, "縦軸：逆流の量（EROA）", size=10.2, color=INK,
            ha="left")

    ZONE = [("COAPT 型", 0.30, 0.22, GREEN, "#eaf5ee", "left",
             ["左室はそれほど大きくない", "しかし逆流は重い",
              "＝ 不比例に重い逆流", "→ 逆流を治すと良くなる"]),
            ("MITRA-FR 型", 0.74, 0.62, RED, "#fceeec", "right",
             ["左室がすでに大きい", "逆流は容積に見合う程度",
              "＝ 比例した逆流", "→ 逆流を治しても心筋は戻らない"])]
    for lab, px, py, col, fc, side, lines in ZONE:
        xx = x0 + pw * px
        yy = y0 + ph * py
        cv.ax.plot([xx], [yy], marker="o", markersize=15, color=col,
                   zorder=5)
        bw = 390
        bx = 70 if side == "left" else W - 70 - bw
        by = y0 - 20 if side == "left" else y0 + 190
        cv.box(bx, by, bw, 230, fc=fc, ec=col, lw=1.8, radius=10)
        cv.text(bx + bw / 2, by + 38, lab, size=12.4, color=col,
                weight="bold")
        for j, ln in enumerate(lines):
            cv.text(bx + bw / 2, by + 84 + 38 * j, ln,
                    size=fit(cv, ln, bw - 40, 10.4), color=INK)
        p0 = (bx + bw + 6, by + 115) if side == "left" else (bx - 6, by + 115)
        cv.arrow(p0, (xx + (-14 if side == "right" else 14), yy), color=col,
                 lw=1.8, head=9)

    textbox(cv, 70, y0 + ph + 80, W - 140,
            ["RESHAPE-HF2 が加わったことで、この枠組みはもう一段更新された。",
             "同試験は中等度〜重度の逆流を含む、より広い集団で有効性を示している。",
             "つまり境界は一本の線ではなく、"
             "逆流の量・左室の容積・薬物治療の最適化を合わせた帯である。"],
            10.6, style="amber", title="2024 年以降の読み方",
            title_color="#9a6510", pad_y=16)
    cv.save(P("m04_proportionality.png"))
    crop_bottom(P("m04_proportionality.png"))


# ---------------------------------------------------------------- m05
def m05():
    """TEER 前後の後負荷"""
    cv = Canvas(W, 900)
    cap(cv, 44, "逆流が閉じた瞬間、左室の後負荷が上がる")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 430

    def panel(x, title, color, fc, mode, lines):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.text(x + PW / 2, PY + 36, title,
                size=fit(cv, title, PW - 44, 12.2, "bold"), color=color,
                weight="bold")
        cx0 = x + PW / 2
        # 左室
        cv.box(cx0 - 190, PY + 80, 150, 150, fc="#f4f6f9", ec="#b9c2cc",
               lw=1.6, radius=20)
        cv.text(cx0 - 115, PY + 155, "左室", size=11.0, color=INK)
        # 大動脈
        cv.box(cx0 + 60, PY + 80, 130, 64, fc="#fceeec", ec=RED, lw=1.6,
               radius=12)
        cv.text(cx0 + 125, PY + 112, "大動脈", size=10.4, color=RED)
        # 左房
        cv.box(cx0 + 60, PY + 166, 130, 64, fc=fc, ec=color, lw=1.6,
               radius=12)
        cv.text(cx0 + 125, PY + 198, "左房", size=10.4, color=color)
        cv.arrow((cx0 - 36, PY + 120), (cx0 + 56, PY + 112), color=RED,
                 lw=2.6, head=11)
        if mode == "before":
            cv.arrow((cx0 - 36, PY + 190), (cx0 + 56, PY + 198), color=color,
                     lw=3.4, head=13)
            cv.text(cx0 + 10, PY + 238, "逃げ道", size=10.0, color=color)
        else:
            cv.ax.plot([cx0 - 20, cx0 + 40], [PY + 178, PY + 210],
                       color=GREY, lw=2.4)
            cv.ax.plot([cx0 - 20, cx0 + 40], [PY + 210, PY + 178],
                       color=GREY, lw=2.4)
            cv.text(cx0 + 10, PY + 238, "閉じた", size=10.0, color=GREY)
        for j, ln in enumerate(lines):
            cv.text(x + PW / 2, PY + 300 + 34 * j, ln,
                    size=fit(cv, ln, PW - 60, 10.4), color=INK)

    panel(x1, "TEER 前", BLUE, "#eaf1f8", "before",
          ["左室は大動脈と左房の二方向に駆出している",
           "左房は低圧なので、左室は「楽をしている」",
           "駆出率は実力より高く見える"])
    panel(x2, "TEER 後", RED, "#fceeec", "after",
          ["逃げ道が閉じ、全量を大動脈へ送ることになる",
           "後負荷が相対的に上がる（afterload mismatch）",
           "収縮力の乏しい左室では破綻しうる"])

    th = textbox(cv, 70, PY + PH + 26, W - 140,
                 ["この現象は 1985 年に「後負荷ミスマッチ」として記述されている。",
                  "弁膜症手術のあとに左室が破綻する理由として、"
                  "外科の時代から知られていた。",
                  "M-TEER では、それが数分のうちに起こる。"],
                 10.6, style="navy", title="古くて新しい現象",
                 title_color=NAVY, pad_y=16)

    msg(cv, PY + PH + 26 + th + 28,
        "クリップが留置された直後は、左室にとって条件が変わった瞬間である",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("m05_afterload.png"))
    crop_bottom(P("m05_afterload.png"))


# ---------------------------------------------------------------- m06
def m06():
    """TEE の時系列"""
    cv = Canvas(W, 1700)
    cap(cv, 44, "麻酔科医が TEE で見るものは、手技の段階ごとに変わる")

    ROWS = [("① 導入直後（ベースライン）", NAVY,
             "MR の機序と重症度、左室・右室機能、肺高血圧、心嚢液"),
            ("② 心房中隔穿刺", RED,
             "穿刺の高さと位置（二平面）、テンティング、心嚢液の出現"),
            ("③ ガイドの進入", BLUE,
             "左房内の位置、左心耳・肺静脈への迷入、血栓の有無"),
            ("④ クリップの向き合わせ", PURPLE,
             "3D 正面像で弁尖に直交しているか、把持する部位はどこか"),
            ("⑤ 弁尖の把持", ORANGE,
             "前尖・後尖の insertion の深さ（二平面で確認）"),
            ("⑥ 留置直後", TEAL,
             "残存 MR、平均圧較差、肺静脈血流の逆行性成分の改善"),
            ("⑦ 追加クリップの判断", GREEN,
             "残存 MR と圧較差のトレードオフ"),
            ("⑧ 終了時", GREY,
             "心嚢液、左室・右室機能、心房中隔欠損の遺残")]

    y = 130
    for lab, col, what in ROWS:
        h = 92
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.5, radius=8)
        cv.box(70, y, 360, h, fc="#fbfcfd", ec=col, lw=0, radius=8)
        cv.text(94, y + h / 2, lab, size=fit(cv, lab, 320, 11.0, "bold"),
                color=col, weight="bold", ha="left")
        cv.text(450, y + h / 2, what, size=fit(cv, what, W - 540, 10.6),
                color=INK, ha="left")
        y += h + 10

    th = textbox(cv, 70, y + 12, W - 140,
                 ["米国心エコー図学会は 2026 年、"
                  "M-TEER の術中画像に関するガイドラインを公表した。",
                  "それまで「術中画像を担当する術者向けの標準的な手順がなかった」"
                  "と明記したうえで、",
                  "撮るべき断面、手技の標準的な段階、"
                  "そして術者へ伝えるべき画像情報の内容を定めている。"],
                 10.6, style="green", title="2026 年に標準化された",
                 title_color=GREEN, pad_y=16)
    cv.save(P("m06_tee_timeline.png"))
    crop_bottom(P("m06_tee_timeline.png"))


# ---------------------------------------------------------------- m07
def m07():
    """残存 MR と圧較差のトレードオフ"""
    cv = Canvas(W, 1700)
    cap(cv, 44, "クリップを足すか、止めるか")

    cx = W / 2
    cv.box(cx - 300, 110, 600, 76, fc="#e8edf5", ec=NAVY, lw=2.0, radius=10)
    t = "クリップを 1 個追加すると何が起こるか"
    cv.text(cx, 148, t, size=fit(cv, t, 540, 12.6, "bold"), color=NAVY,
            weight="bold")

    SIDE = [("良くなること", GREEN, "#eaf5ee", -1,
             ["残存する逆流が減る", "肺静脈の逆流波形が改善する",
              "左房圧が下がる"]),
            ("悪くなること", RED, "#fceeec", 1,
             ["弁口面積が減る", "拡張期の平均圧較差が上がる",
              "医原性の僧帽弁狭窄になりうる"])]
    w = (W - 140 - 40) / 2
    for i, (t2, col, fc, d, lines) in enumerate(SIDE):
        x = 70 + (w + 40) * i
        cv.arrow((cx, 192), (x + w / 2, 236), color="#b9c2cc", lw=1.8,
                 head=9)
        card(cv, x, 240, w, t2, lines, col, fc, body_size=10.6, lh=1.8)

    DATA = [("術前の弁口面積が小さいほど、圧較差は上がりやすい", BLUE,
             "弁口面積 4.0 cm2 未満では 86%、4.0〜6.0 で 28%、"
             "6.0 超では 14% に圧較差の上昇が生じた"),
            ("圧較差の上昇は、予後と関連する", RED,
             "術後の平均圧較差 5 mmHg 超は、1 年全死亡の 3.42 倍のリスク"
             "（95%CI 1.08-10.87、p=0.04）"),
            ("小さい弁口面積が効くのは変性性 MR", PURPLE,
             "279 例の検討で、小さい弁口面積は変性性 MR で死亡と関連したが"
             "（p=0.01）、機能性 MR では関連しなかった（p=0.52）")]
    y = 500
    for lab, col, det in DATA:
        dl = cv.wrap(det, W - 200, 10.4)
        bh = 72 + LH(10.4, 1.5) * len(dl) + 4
        cv.box(70, y, W - 140, bh, fc="#ffffff", ec=col, lw=1.6, radius=10)
        cv.text(96, y + 36, lab, size=fit(cv, lab, W - 200, 11.0, "bold"),
                color=col, weight="bold", ha="left")
        for j, ln in enumerate(dl):
            cv.text(96, y + 72 + LH(10.4, 1.5) * j, ln, size=10.4,
                    color=INK, ha="left")
        y += bh + 12

    msg(cv, y + 10,
        "「逆流をゼロにする」ことが目標ではない。逆流と狭窄の釣り合いが目標である")
    cv.save(P("m07_gradient_tradeoff.png"))
    crop_bottom(P("m07_gradient_tradeoff.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (m01, m02, m03, m04, m05, m06, m07):
        fn()
        print("ok", fn.__name__)
