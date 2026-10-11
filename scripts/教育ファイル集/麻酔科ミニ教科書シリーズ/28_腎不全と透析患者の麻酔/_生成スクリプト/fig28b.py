# -*- coding: utf-8 -*-
"""㉘ 図版 f08〜f14"""
import os

from fig28common import (Canvas, LH, textbox, cap, msg, fitlines, card, band,
                         stat, tick_axis, outpath, save, W, TEAL, FC,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)

OUT = outpath()


def P(n):
    return os.path.join(OUT, n)


def checklist(cv, x, y, w, title, items, color, mark, fc=None, size=11.0,
              title_size=12.2):
    """見出し＋印つきの箇条書き。返り値は高さ"""
    fc = fc or FC.get(color, "#f2f4f6")
    ts, tl = fitlines(cv, [title], w - 32, title_size, weight="bold",
                      floor=9.4)
    th = 20 + LH(ts, 1.45) * len(tl)
    lines = []
    for it in items:
        lines.extend(cv.wrap(it, w - 78, size))
    lh = LH(size, 1.8)
    bh = 26 + lh * len(lines)
    cv.box(x, y, w, th, fc=color, ec=color, lw=0, radius=8)
    cv.block(x, y + (th - LH(ts, 1.45) * len(tl)) / 2, w, tl, ts,
             color="white", weight="bold")
    cv.box(x, y + th + 8, w, bh, fc=fc, ec=color, lw=1.7, radius=8)
    k = 0
    for it in items:
        wl = cv.wrap(it, w - 78, size)
        cv.text(x + 26, y + th + 8 + 13 + lh * (k + 0.5), mark, size=size + 1.4,
                color=color, weight="bold", ha="left")
        for j, ln in enumerate(wl):
            cv.text(x + 54, y + th + 8 + 13 + lh * (k + j + 0.5), ln,
                    size=size, color=INK, ha="left")
        k += len(wl)
    return th + 8 + bh


# ---------------------------------------------------------------- f08
def f08():
    """術前休薬の時間表"""
    ROWS = [
        ("SGLT2 阻害薬", -3.0, "3 日前に中止（エルツグリフロジンは 4 日前）", RED),
        ("GLP-1 受容体作動薬", -1.2,
         "2024年以降はリスク層別。胃不全麻痺なら個別に", ORANGE),
        ("RAS 阻害薬（ACE-I / ARB）", -0.3, "手術当日の朝は中止", ORANGE),
        ("抗血小板薬・抗凝固薬", -5.0, "薬剤ごと・腎機能ごとの表で決める", PURPLE),
        ("リン吸着薬", -0.3, "絶食中は不要。食事とともに再開", GREY),
        ("ESA・HIF-PH 阻害薬", None, "継続", GREEN),
        ("活性型ビタミンD・Ca 受容体作動薬", None, "継続", GREEN),
        ("免疫抑制薬（移植腎）", None, "絶対に中断しない", GREEN),
    ]
    LW = 560
    X0, X1, AY = LW + 60, 1400, 172
    RY, RH, GAP = AY + 62, 74, 12
    cv = Canvas(W, 1500)
    cap(cv, 46, "術前休薬の時間表 ── 止めるもの、続けるもの")

    LO = -7.0

    def px(d):
        return X0 + (X1 - X0) * (d - LO) / (0 - LO)

    tick_axis(cv, X0, X1, AY,
              [(0.0, "7 日前"), (2 / 7, "5 日前"), (4 / 7, "3 日前"),
               (6 / 7, "前日"), (1.0, "手術")])
    cv.ax.plot([px(0), px(0)], [AY - 20, RY + len(ROWS) * (RH + GAP) - 6],
               color=NAVY, lw=2.4, zorder=2)

    for i, (name, stop, note, color) in enumerate(ROWS):
        y = RY + i * (RH + GAP)
        ns, nl = fitlines(cv, [name], LW - 20, 11.6, weight="bold", floor=9.0)
        ds, dl = fitlines(cv, [note], LW - 20, 10.4, floor=8.8)
        blk = LH(ns, 1.45) * len(nl) + LH(ds, 1.5) * len(dl)
        top = y + (RH - blk) / 2
        cv.block(44, top, LW - 20, nl, ns, color=color, weight="bold",
                 ha="left")
        cv.block(44, top + LH(ns, 1.45) * len(nl), LW - 20, dl, ds, color=GREY,
                 ha="left")

        if stop is None:
            cv.box(px(LO), y + 14, px(0) - px(LO), RH - 28, fc=FC[GREEN],
                   ec=GREEN, lw=1.7, radius=8)
            cv.text((px(LO) + px(0)) / 2, y + RH / 2, "服用を続ける",
                    size=11.4, color=GREEN, weight="bold")
        else:
            xa = px(max(stop, LO))
            cv.rect(px(LO), y + 14, xa - px(LO), RH - 28, fc="#e9edf1")
            if xa - px(LO) > 150:
                cv.text((px(LO) + xa) / 2, y + RH / 2, "服用", size=10.8,
                        color=GREY)
            cv.box(xa, y + 14, px(0) - xa, RH - 28, fc=FC[color], ec=color,
                   lw=1.8, radius=8)
            if px(0) - xa > 150:
                cv.text((xa + px(0)) / 2, y + RH / 2, "休　薬", size=11.4,
                        color=color, weight="bold")
            cv.ax.plot([xa, xa], [y + 6, y + RH - 6], color=color, lw=2.8,
                       zorder=5)

    msg(cv, RY + len(ROWS) * (RH + GAP) + 18,
        "3 日休薬しても正常血糖ケトアシドーシスは起こりうる。"
        "術後の説明のつかないアシドーシスでは服薬歴に戻る")
    save(cv, P("f08_drug_hold.png"))


# ---------------------------------------------------------------- f09
def f09():
    """シャント肢を守る"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "シャント肢を守る ── 何をしないか、どこを使うか")

    L, CW, GAP, TOP = 52, 700, 16, 106
    h1 = checklist(cv, L, TOP, CW, "シャント肢にしないこと", [
        "血圧計のカフを巻く",
        "末梢静脈路を取る・採血する",
        "同側に動脈ラインを取る",
        "腕を体幹の下に敷く、外転させすぎる",
        "抑制帯を直上に巻く",
        "消毒液が溜まったまま長時間圧迫する",
    ], RED, "✕")
    h2 = checklist(cv, L + CW + GAP, TOP, CW, "代わりに決めておくこと", [
        "反対側の上肢か、下肢のどこを使うか",
        "動脈ラインは足背動脈・大腿動脈も選択肢",
        "両上肢が使えないなら内頸静脈も検討",
        "シャント側が分かるように表示する",
        "術前訪問の段階で決める（当日ではない）",
        "例外を選んだら記録して腎臓内科へ伝える",
    ], GREEN, "✓")

    Y2 = TOP + max(h1, h2) + 26
    TH = [("入室時", "手術前の状態を記録する", BLUE),
          ("体位固定後", "体位そのものが原因になる。ここが最も重要", ORANGE),
          ("退室時", "何かあれば手術室を出る前に共有できる", PURPLE)]
    TW = (CW * 2 + GAP - 2 * 16) / 3
    # 見出しは「スリルを確かめる」を帯の上に 1 回だけ出し、箱には時点だけを書く
    cv.text(L, Y2 + 12, "スリルを確かめる ── 3 回", size=11.8, color=INK,
            weight="bold", ha="left")
    Y2 += 38
    lines = [cv.wrap(d, TW - 40, 10.8) for _, d, _ in TH]
    BH = 58 + LH(10.8, 1.45) * max(len(x) for x in lines) + 14
    for i, (t, d, color) in enumerate(TH):
        x = L + i * (TW + 16)
        cv.box(x, Y2, TW, BH, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.text(x + TW / 2, Y2 + 30, t, size=11.8, color=color, weight="bold")
        cv.block(x + 20, Y2 + 54, TW - 40, lines[i], 10.8)

    msg(cv, Y2 + BH + 18,
        "触れない・聞こえないときは、その場で報告する。時間が経つほど救えなくなる")
    save(cv, P("f09_access.png"))


# ---------------------------------------------------------------- f10
def f10():
    """腎不全での筋弛緩薬とその拮抗"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "腎不全での筋弛緩薬と、その拮抗")

    ITEMS = [("シスアトラクリウム",
              ["ホフマン脱離", "臓器に依存しない", "長時間症例で有利"], GREEN),
             ("ロクロニウム",
              ["主に肝・胆汁", "一部が腎排泄", "反復投与で蓄積"], ORANGE),
             ("ベクロニウム",
              ["活性代謝産物が腎排泄", "3-デスアセチル体", "長時間投与で遷延"], RED),
             ("スキサメトニウム",
              ["血漿コリンエステラーゼ", "K を約 0.5 mEq/L 上げる",
               "高カリウム時は避ける"], PURPLE)]
    L, CW, GAP, TOP = 52, 348, 16, 106
    h1 = 0
    for i, (h, lines, c) in enumerate(ITEMS):
        h1 = max(h1, card(cv, L + i * (CW + GAP), TOP, CW, h, lines, c,
                          head_size=12.0, body_size=10.6, lh=1.85))

    Y2 = TOP + h1 + 60
    cv.text(W / 2, Y2 - 26, "スガマデクス ── 同じデータを見て、解釈が違う",
            size=13.0, color=NAVY, weight="bold")
    PANE = [("国内の添付文書", ["9.2 腎機能障害患者", "「本剤は腎排泄されるため、",
                        "排泄が遅延するおそれがある」", "── 禁忌ではない"], BLUE),
            ("米国食品医薬品局", ["クレアチニンクリアランス",
                          "30 mL/分未満では推奨しない", "滞留の延長と遅発性事象が",
                          "読めないことを理由とする"], RED),
            ("透析での除去", ["high-flux 膜・平均 6 時間で",
                        "血漿中濃度が約 70% 減少", "low-flux 膜では除去されない",
                        "── 膜の種類を確認する"], PURPLE)]
    PW = (W - 2 * 52 - 2 * 20) / 3
    h2 = 0
    for i, (h, lines, c) in enumerate(PANE):
        h2 = max(h2, card(cv, 52 + i * (PW + 20), Y2, PW, h, lines, c,
                          head_size=12.2, body_size=10.6, lh=1.8))

    msg(cv, Y2 + h2 + 20,
        "「禁忌だから使えない」ではなく「延びた滞留を許容できるかを自分で判断する」")
    save(cv, P("f10_nmba.png"))


# ---------------------------------------------------------------- f11
def f11():
    """オピオイドの代謝産物"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "オピオイドと鎮痛薬 ── どこで詰まるか")

    L, CW, GAP, TOP = 52, 468, 20, 150
    cv.text(W / 2, 96,
            "親化合物ではなく、活性代謝産物が腎で詰まる ──"
            "「肝代謝だから安全」は成り立たない",
            size=12.2, color=GREY, weight="bold")

    COLS = [
        ("避ける", RED, [
            "モルヒネ ── M6G（活性）が蓄積。鎮静と呼吸抑制の遷延",
            "コデイン ── モルヒネへ代謝される",
            "ペチジン ── ノルペチジンが腎排泄。痙攣",
            "NSAIDs ── 残腎機能・血小板・消化管の三方向で不利",
        ]),
        ("減量して使う", ORANGE, [
            "トラマドール ── O-脱メチル体が腎排泄",
            "オキシコドン ── 代謝産物の活性は低いが蓄積しうる",
            "ガバペンチン・プレガバリン ── 代謝されず全量が腎排泄。"
            "通常量の数分の一",
        ]),
        ("使いやすい", GREEN, [
            "レミフェンタニル ── エステラーゼで分解。腎不全で最も予測可能",
            "フェンタニル ── 活性代謝産物なし。長時間持続では遷延",
            "アセトアミノフェン ── 通常量で使用可。定期投与の土台に",
        ]),
    ]
    hs = []
    for i, (title, color, items) in enumerate(COLS):
        hs.append(checklist(cv, L + i * (CW + GAP), TOP, CW, title, items,
                            color, "●", size=10.6, title_size=13.0))

    Y2 = TOP + max(hs) + 26
    band(cv, L, Y2, W - 2 * L, 84, "レミフェンタニルの設計",
         ["術中の鎮痛をレミフェンタニルで担い、"
          "術後鎮痛は区域麻酔かアセトアミノフェンで組む。"
          "切ったあとの鎮痛を用意しないまま終わらない"],
         BLUE, label_w=330, label_size=11.6, body_size=10.8)

    msg(cv, Y2 + 102,
        "ガバペンチノイドは他科から出されることがある。処方全体を見る")
    save(cv, P("f11_opioids.png"))


# ---------------------------------------------------------------- f12
def f12():
    """術中高カリウムへの手"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "術中の高カリウム ── 順番と、効くまでの時間")

    LAYERS = [
        ("① 心筋を守る", RED,
         ["カルシウム静注（グルコン酸／塩化）", "1〜3 分で発現、30〜60 分持続"],
         "カリウム値は下がらない"),
        ("② 細胞内へ移す", ORANGE,
         ["グルコース・インスリン／β2 刺激薬吸入",
          "15〜30 分で発現、いずれも 0.5〜1.0 mEq/L"],
         "体内の総量は変わらない ── 時間稼ぎ"),
        ("③ 体から出す", GREEN,
         ["血液透析（1 時間で 1 mEq/L 以上）", "カリウム吸着薬・利尿薬は補助"],
         "無尿の患者では、事実上これしかない"),
    ]
    L, RW, TOP, RH, GAP = 52, W - 104, 112, 152, 22
    for i, (title, color, lines, tail) in enumerate(LAYERS):
        y = TOP + i * (RH + GAP)
        cv.box(L, y, RW, RH, fc=FC[color], ec=color, lw=1.8, radius=8)
        cv.rect(L + 8, y + 8, 300, RH - 16, fc=color, ec="none")
        s, ln = fitlines(cv, [title], 266, 14.0, weight="bold", floor=10.0)
        cv.block(L + 8, y + (RH - LH(s, 1.45) * len(ln)) / 2, 300, ln, s,
                 color="white", weight="bold")
        for j, t in enumerate(lines):
            sz = cv.fit_size([t], RW - 360, 11.8)
            cv.text(L + 336, y + 44 + j * 34, t, size=sz, color=INK, ha="left")
        sz = cv.fit_size([tail], RW - 360, 11.6, weight="bold")
        cv.text(L + 336, y + RH - 36, "→ " + tail, size=sz, color=color,
                weight="bold", ha="left")
        if i < len(LAYERS) - 1:
            cv.arrow((L + RW / 2, y + RH + 2), (L + RW / 2, y + RH + GAP - 2),
                     color=GREY, lw=2.4, head=12)

    Y2 = TOP + 3 * (RH + GAP) + 6
    FIRST = ["心電図を見る（可能なら 12 誘導）",
             "採血をやり直す（溶血による偽高値を除外）",
             "心電図変化があれば結果を待たずにカルシウム",
             "同時に、透析の可否を誰かに確認させる",
             "原因を探す（輸血・駆血解除・アシドーシス・薬剤）"]
    h = checklist(cv, L, Y2, RW, "最初にすること", FIRST, NAVY, "□",
                  size=11.2, title_size=12.6)

    msg(cv, Y2 + h + 18,
        "薬だけで押し切ろうとすると、効果が切れる数時間後に同じ場面が戻ってくる")
    save(cv, P("f12_hyperk.png"))


# ---------------------------------------------------------------- f13
def f13():
    """術後の透析"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "術後の透析 ── 緊急と予定を分けて指示する")

    L = 52
    cv.box(W / 2 - 220, 100, 440, 74, fc=FC[NAVY], ec=NAVY, lw=2.0, radius=8)
    cv.text(W / 2, 137, "術後の透析が必要か", size=14.0, color=NAVY,
            weight="bold")

    CW = 700
    XA, XB, Y = L, L + CW + 16, 236
    cv.arrow((W / 2 - 120, 178), (XA + CW / 2, Y - 8), color=RED, lw=2.2,
             head=12)
    cv.arrow((W / 2 + 120, 178), (XB + CW / 2, Y - 8), color=BLUE, lw=2.2,
             head=12)

    hA = checklist(cv, XA, Y, CW, "緊急 ── 待たない", [
        "高カリウム血症（薬物療法で制御できない）",
        "体液過剰で酸素化が保てない",
        "重症の代謝性アシドーシス",
        "抜管より先に除水を選ぶ場面がある",
    ], RED, "▲", size=11.2)
    hB = checklist(cv, XB, Y, CW, "予定 ── 次回透析日", [
        "通常のスケジュールに戻す",
        "術後 24 時間以内なら無ヘパリンかナファモスタット",
        "出血の程度を麻酔科医と外科医から伝える",
        "透析室・臨床工学技士に前日までに連絡する",
    ], BLUE, "●", size=11.2)

    Y2 = Y + max(hA, hB) + 26
    h = checklist(cv, L, Y2, W - 2 * L, "無尿の患者の術後輸液指示で書くこと", [
        "維持輸液を出すなら、速度と総量の上限を数字で書く",
        "止める条件を書く（経口摂取が始まったら、など）",
        "抗菌薬や薬剤の希釈に使う液量も、一日の水分量に数える",
        "翌朝の体重測定を指示に入れる ── 最も分かりやすい指標",
    ], ORANGE, "□", size=11.2)

    msg(cv, Y2 + h + 18,
        "80 mL/時を漫然と流せば、無尿の患者では一日で約 2 L が体に残る")
    save(cv, P("f13_postop.png"))


# ---------------------------------------------------------------- f14
def f14():
    """当日の段取り"""
    cv = Canvas(W, 1500)
    cap(cv, 46, "当日の段取り ── 手術室に持ち込む一枚")

    L, CW, GAP, TOP = 52, 468, 20, 106
    COLS = [
        ("術前訪問で埋める", NAVY, "□", [
            "透析の型・曜日・最終透析日時",
            "ドライウェイトと当日体重、その差",
            "残尿量（一日何 mL 出るか）",
            "シャントの位置と種類、スリル",
            "最終の K・Hb・血液ガスと採血時刻",
            "心エコーの日付と要点",
            "止めた薬と、続けている薬",
            "出血の病歴（歯磨き・穿刺部）",
            "腎移植の待機中か／移植腎があるか",
        ]),
        ("入室前に確認する", ORANGE, "□", [
            "最終透析は終わっているか。終了時刻は",
            "当日の体重は測ったか",
            "血圧計とルートを取る腕は決まっているか",
            "昇圧薬は希釈して手元にあるか",
            "カルシウム製剤はどこにあるか",
            "透析が必要になったとき、誰に連絡するか",
            "術後の行き先は決まっているか",
        ]),
        ("引き継ぎで伝える", GREEN, "→", [
            "術中の総輸液量と出血量、差し引き",
            "最後のカリウムと、その測定時刻",
            "シャントのスリルを退室時に確認したか",
            "次の透析をいつ・どこで行う予定か",
            "誰と話がついているか",
        ]),
    ]
    hs = []
    for i, (title, color, mark, items) in enumerate(COLS):
        hs.append(checklist(cv, L + i * (CW + GAP), TOP, CW, title, items,
                            color, mark, size=10.8, title_size=13.0))

    Y2 = TOP + max(hs) + 26
    band(cv, L, Y2, W - 2 * L, 92, "最初の一問",
         ["「最後に透析をしたのはいつですか」 ── "
          "この一問で、検査値の読み方がすべて決まる"],
         TEAL, fc="#e4f2f4", label_w=280, label_size=12.6, body_size=12.0)

    msg(cv, Y2 + 110,
        "「透析患者です」だけでは足りない。数字で伝える")
    save(cv, P("f14_daycard.png"))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f08, f09, f10, f11, f12, f13, f14):
        fn()
        print("ok", fn.__name__)
