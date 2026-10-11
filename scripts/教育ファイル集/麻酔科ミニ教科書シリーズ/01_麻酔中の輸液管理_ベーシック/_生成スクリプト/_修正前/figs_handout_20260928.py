# -*- coding: utf-8 -*-
"""研修医向け配布資料「周術期の輸液」の図版。

figlib（22巻の生成スクリプト）を使い、文字を実測してから枠を決める。
座標はピクセル（左上原点、y は下向き）。
"""
import os
import sys

KIT = (r"C:\Users\junch\OneDrive\_旧デスクトップ\教育ファイル集"
       r"\麻酔科ミニ教科書シリーズ\22_常位胎盤早期剝離と産科危機的出血\_生成スクリプト")
sys.path.insert(0, KIT)

from figlib import (Canvas, textbox, LH, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, FILL)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fig")
os.makedirs(OUT, exist_ok=True)

W = 1700
M = 90                      # 左右の余白


def _save(cv, name, crop=False):
    p = os.path.join(OUT, name)
    cv.save(p)
    if crop:                       # 下の余白だけ落とす（高さを読み切れない図で使う）
        from PIL import Image, ImageChops
        im = Image.open(p).convert("RGB")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bb = ImageChops.difference(im, bg).getbbox()
        if bb:
            im.crop((0, 0, im.width, min(im.height, bb[3] + 30))).save(p)
    print("  %s" % name)
    return p


def wbox(cv, x, y, w, text, size, style="grey", title=None, title_size=None,
         pad_x=16, **kw):
    """本文を枠幅に合わせて折り返してから textbox に渡す。"""
    lines = []
    for para in (text if isinstance(text, (list, tuple)) else [text]):
        lines += cv.wrap(para, w - 2 * pad_x, size)
    return textbox(cv, x, y, w, lines, size, style=style, title=title,
                   title_size=title_size, pad_x=pad_x, **kw)


# ---------------------------------------------------------------- 図1
def f1_compartments():
    """体重70 kg の体液区画を、面積そのままの帯で示す。"""
    H = 1100
    cv = Canvas(W, H)
    cv.title(M - 20, 62, "体重 70 kg のからだの水　── 42 L を 3 つの箱に分ける")

    x0, x1 = M, W - M
    bw = x1 - x0
    top, bh = 320, 160
    w_icf = bw * 2 / 3
    w_isf = bw * 1 / 4
    w_pla = bw - w_icf - w_isf
    b1 = x0 + w_icf                      # 細胞膜
    b2 = x0 + w_icf + w_isf              # 血管内皮

    for x, w, style in ((x0, w_icf, "green"), (b1, w_isf, "amber"),
                        (b2, w_pla, "red")):
        fc, ec = FILL[style]
        cv.rect(x, top, w, bh, fc=fc, ec=ec, lw=1.6, z=2)

    # バリアは縦の帯で描き、ラベルは帯の上に置く（左右にずらして重ねない）
    for bx, label, style, ha, tx in ((b1, "細胞膜", "green", "center", b1),
                                     (b2, "血管内皮", "red", "right", x1)):
        ec = FILL[style][1]
        cv.rect(bx - 3, top - 14, 6, bh + 28, fc=ec, z=4)
        cv.text(tx, top - 36, label, size=15, color=ec, weight="bold", ha=ha)
    cv.text(x0, top - 36, "この 2 枚は、性質のまったく違うバリア",
            size=13, color=GREY, ha="left")

    # 細胞外液のくくりは帯の上に置く
    cv.rect(b1, top - 84, w_isf + w_pla, 5, fc=FILL["navy"][1], z=4)
    cv.text(x1, top - 108, "細胞外液（ECF）14 L ／ 体重の 20 %", size=14,
            color=NAVY, weight="bold", ha="right")
    cv.text(x0, top - 108, "全身の水 42 L ／ 体重の 60 %", size=14,
            color=GREY, weight="bold", ha="left")

    # 区画の説明は帯の下に 3 つ並べ、引き出し線でつなぐ
    cards = [
        ("green", "細胞内液（ICF）",
         "28 L ／ 体重の 40 %　　K⁺ が主役。水は自由に出入りするが、"
         "Na⁺ は入ってこられない", x0 + w_icf / 2),
        ("amber", "間質液",
         "10.5 L ／ 体重の 15 %　　細胞のまわりを満たす液。"
         "むくみは、ここに溜まった水", b1 + w_isf / 2),
        ("red", "血漿（＝血管内）",
         "3.5 L ／ 体重の 5 %　　輸液で「増やしたい」のは、たいていここ",
         b2 + w_pla / 2),
    ]
    cy = top + bh + 110
    cw = (bw - 60) / 3
    ch = 0
    for i, (style, title, body, sx) in enumerate(cards):
        x = x0 + i * (cw + 30)
        h = wbox(cv, x, cy, cw, [body], 13.5, style=style, title=title,
                 title_size=16, min_h=200)
        ch = max(ch, h)
        cv.arrow((sx, top + bh + 8), (x + cw / 2, cy - 8),
                 color=FILL[style][1], lw=1.8, head=9)

    return _save(cv, "h1_compartments.png", crop=True)


# ---------------------------------------------------------------- 図2
def f2_barriers():
    """2枚のバリアと、それぞれを通れるもの。"""
    H = 1190
    cv = Canvas(W, H)
    cv.title(M - 20, 62, "2 枚のバリア　── 「穴の大きさ」より「何が通れるか」")

    pw = (W - M * 2 - 40) / 2
    lx, rx = M, M + pw + 40
    top = 120
    ph = 880

    panels = [
        (lx, "red", "① 血管内皮＋グリコカリックス", "血漿 ⇄ 間質 のあいだ",
         [("○", "水・Na⁺・Cl⁻・ブドウ糖・尿素", "小さいので自由に行き来する",
           FILL["green"][1]),
          ("△", "アルブミン・HES（デンプン）",
           "正常ならほぼ保たれる。それでもアルブミンは約 5 %／時が間質へ漏れ、"
           "リンパ管を通って血管へ戻る", FILL["amber"][1]),
          ("×", "赤血球（直径 7〜8 µm）",
           "けた違いに大きく、血管の外へは出られない", FILL["red"][1])]),
        (rx, "green", "② 細胞膜", "間質 ⇄ 細胞内 のあいだ",
         [("○", "水", "アクアポリンという専用の通り道を通る", FILL["green"][1]),
          ("×", "Na⁺",
           "自由には通れない。入ってもポンプですぐ外へ汲み出される",
           FILL["red"][1]),
          ("△", "ブドウ糖",
           "運び屋（GLUT）に乗って細胞内へ入り、代謝されて消える",
           FILL["amber"][1])]),
    ]

    for x, style, title, sub, rows in panels:
        fc, ec = FILL[style]
        cv.box(x, top, pw, ph, style=style, lw=1.8)
        ts = cv.fit_size([title], pw - 60, 16, weight="bold")
        cv.text(x + pw / 2, top + 46, title, size=ts, color=ec, weight="bold")
        cv.text(x + pw / 2, top + 84, sub, size=13, color=GREY)

        y = top + 120
        cv.rect(x + 50, y, pw - 100, 130, fc="#ffffff", ec=ec, lw=1.6, z=2)
        for i in range(6):
            gx = x + 90 + i * (pw - 180) / 5
            cv.rect(gx - 4, y, 8, 130, fc="#f4f7fa", ec="#cfd8e3", lw=1.0, z=3)
        cv.text(x + pw / 2, y + 65,
                "内皮細胞＋グリコカリックス" if style == "red"
                else "脂質二重膜＋チャネル・ポンプ",
                size=13.5, color=ec, weight="bold", z=4)
        cv.text(x + pw / 2, y + 156, "すき間はごく小さい" if style == "red"
                else "通り道は物質ごとに決まっている", size=12.5, color=GREY)

        y += 200
        for mark, what, why, col in rows:
            ws = cv.fit_size([what], pw - 190, 14.5, weight="bold")
            lines = cv.wrap(why, pw - 190, 13)
            h = 44 + LH(13, 1.4) * len(lines)
            cv.rect(x + 34, y, pw - 68, h, fc="#ffffff", ec="#e3e8ee",
                    lw=1.2, z=3)
            cv.text(x + 72, y + h / 2, mark, size=22, color=col,
                    weight="bold", z=5)
            cv.text(x + 110, y + 28, what, size=ws, color=NAVY,
                    weight="bold", ha="left", z=5)
            for i, ln in enumerate(lines):
                cv.text(x + 110, y + 52 + LH(13, 1.4) * (i + 0.5), ln,
                        size=13, color=INK, ha="left", z=5)
            y += h + 16

    wbox(cv, M, top + ph + 30, W - M * 2,
         ["血管の外へ水が出るかどうかは「穴の直径」だけで決まるのではない。"
          "炎症・敗血症・手術侵襲でグリコカリックスが傷むと、"
          "同じ患者・同じ製剤でも行き先が変わる。"], 14, style="navy")
    return _save(cv, "h2_barriers.png")


# ---------------------------------------------------------------- 図3
def f3_where():
    """1 L を入れたときの、平衡時の理論分布。"""
    H = 1250
    cv = Canvas(W, H)
    cv.title(M - 20, 62, "1 L を入れたら、どこへ行くのか（平衡時のモデル）")

    x0 = 420
    bw = W - x0 - 120
    items = [
        ("5 % ブドウ糖液", [(1 / 12, "血漿\n83 mL", "red"),
                            (3 / 12, "間質\n250 mL", "amber"),
                            (8 / 12, "細胞内\n667 mL", "green")]),
        ("細胞外液補充液\n（生食・フィジオ140・\nソルアセトD）",
         [(1 / 4, "血漿\n250 mL", "red"), (3 / 4, "間質\n750 mL", "amber")]),
        ("膠質液\n（アルブミン・HES）",
         [(0.8, "血管内に\nより長くとどまる", "red"), (0.2, "間質へ", "amber")]),
    ]
    y = 190
    bh = 130
    for name, segs in items:
        lines = name.split("\n")
        s = cv.fit_size(lines, x0 - 140, 15)
        for i, ln in enumerate(lines):
            cv.text(x0 - 40, y + bh / 2 + LH(s, 1.35) * (i - (len(lines) - 1) / 2),
                    ln, size=s, color=NAVY, weight="bold", ha="right")
        x = x0
        for frac, label, style in segs:
            w = bw * frac
            fc, ec = FILL[style]
            cv.rect(x, y, w, bh, fc=fc, ec=ec, lw=1.6, z=2)
            ls = label.split("\n")
            fs = cv.fit_size(ls, w - 20, 14, min_size=9)
            for i, ln in enumerate(ls):
                cv.text(x + w / 2, y + bh / 2 + LH(fs, 1.35) * (i - (len(ls) - 1) / 2),
                        ln, size=fs, color=ec if i == 0 else INK,
                        weight="bold" if i == 0 else "normal", z=5)
            x += w
        y += bh + 60

    wbox(cv, M, y + 20, W - M * 2,
         ["これは「分布が終わったとき」の絵であって、入れた直後の絵ではない。"
          "1 L は最初は 1 L 全部が血管内にあり、そこから 20〜30 分かけて"
          "間質へ広がりながら、同時に腎臓から出ていく。",
          "麻酔・手術侵襲・出血・腎機能で速さは大きく変わる。"
          "「◯分で◯ mL 残る」という固定値としては使わないこと。"], 14,
         style="amber", title="◆ この図の読み方", title_size=15)
    return _save(cv, "h3_where.png", crop=True)


# ---------------------------------------------------------------- 図4
def f4_na_scale():
    """Na 濃度の物差しに製剤を並べる（はしご型）。"""
    rows = [
        ("5 % ブドウ糖液", 0, "Na 0／ブドウ糖 5 %", "purple",
         "実質は自由水。全身の水に広がる"),
        ("KN1号輸液（1号液）", 77, "Na 77・Cl 77／ブドウ糖 2.5 %", "blue",
         "細胞外液と自由水を半分ずつ補う開始液"),
        ("ソルアセトD", 131, "Na 131・Cl 109・酢酸 28／糖 5 %", "green",
         "細胞外液補充＋糖（エネルギー）"),
        ("フィジオ140", 140, "Na 140・Cl 115・酢酸 25 ほか／糖 1 %", "green",
         "血漿に最も近い組成の細胞外液補充液"),
        ("生理食塩液", 154, "Na 154・Cl 154", "red",
         "細胞外液補充液。Cl⁻ が血漿より約 1.5 倍多い"),
        ("ボルベン（6 % HES）", 154, "Na 154・Cl 154＋デンプン 60 g/L", "red",
         "生理食塩液にデンプンを溶かした膠質液"),
    ]
    RH = 104
    H = 260 + len(rows) * RH + 190
    cv = Canvas(W, H)
    cv.title(M - 20, 62, "Na⁺ 濃度で並べると、製剤の性格が見える")

    lx, lw = M, 300                     # 製剤名
    bx, bwid = lx + lw + 20, 460        # 帯
    nx = bx + bwid + 80                 # 組成・ひとこと
    rw = W - M - nx

    def px(na):
        return bx + bwid * na / 160.0

    cv.text(bx, 150, "Na⁺（mEq/L）", size=13, color=GREY, ha="left")
    for na in (0, 40, 80, 120, 160):
        cv.text(px(na), 186, str(na), size=12, color=GREY)
        cv.rect(px(na) - 1, 202, 2, len(rows) * RH + 20, fc="#e6eaee", z=0)

    # 血漿 Na の帯
    cv.rect(px(138), 202, px(142) - px(138), len(rows) * RH + 20,
            fc="#dce9f6", z=1)
    cv.text(px(142) + 14, 150, "血漿 Na 138〜142", size=12.5,
            color=FILL["blue"][1], weight="bold", ha="left")

    y = 220
    for name, na, comp, style, note in rows:
        fc, ec = FILL[style]
        ns = cv.fit_size([name], lw, 15, weight="bold")
        cv.text(lx + lw, y + 36, name, size=ns, color=NAVY, weight="bold",
                ha="right")
        w = max(px(na) - bx, 6)
        cv.rect(bx, y + 16, w, 42, fc=fc, ec=ec, lw=1.6, z=3)
        cv.text(px(na) + 12, y + 37, str(na), size=13.5, color=ec,
                weight="bold", ha="left", z=4)
        csz = cv.fit_size([comp], rw, 12.5, min_size=9.5, weight="bold")
        cv.text(nx, y + 22, comp, size=csz, color=INK, weight="bold",
                ha="left")
        nsz = cv.fit_size([note], rw, 12, min_size=9.5)
        cv.text(nx, y + 58, note, size=nsz, color=GREY, ha="left")
        y += RH

    y += 40
    hw = (W - M * 2 - 40) / 2
    wbox(cv, M, y, hw, ["Na⁺ を連れていないぶんだけ、水は細胞内まで届く。"
                        "血管内はほとんど増えない。"], 14, style="purple",
         title="上へ行くほど「自由水」に近い", title_size=15, min_h=130)
    wbox(cv, M + hw + 40, y, hw, ["入れた水は細胞外にとどまり、"
                                  "血漿と間質を 1 : 3 で満たす。"], 14,
         style="red", title="下へ行くほど「細胞外液」そのもの", title_size=15,
         min_h=130)
    return _save(cv, "h4_na_scale.png")


# ---------------------------------------------------------------- 図5
def f5_freewater():
    """5 % ブドウ糖液が自由水になるまで。"""
    H = 660
    cv = Canvas(W, H)
    cv.title(M - 20, 62, "5 % ブドウ糖液は、体の中で「ただの水」になる")

    steps = [
        ("投与直後", "ブドウ糖 50 g/L を含む。\n浸透圧はほぼ血漿並み\n（約 278 mOsm/L）", "blue"),
        ("10〜15 分", "ブドウ糖は細胞に取り込まれ、\n代謝されて消えていく", "amber"),
        ("30〜45 分", "残るのは Na⁺ を伴わない水\n＝ 自由水", "purple"),
        ("その後", "全身の水（42 L）の比率どおりに\n広がる。血管内に残るのは 1/12", "green"),
    ]
    n = len(steps)
    gap = 60
    bw = (W - M * 2 - gap * (n - 1)) / n
    y = 200
    for i, (t, body, style) in enumerate(steps):
        x = M + i * (bw + gap)
        h = textbox(cv, x, y, bw, body.split("\n"), 13.5, style=style,
                    title=t, title_size=16, min_h=230)
        if i < n - 1:
            cv.arrow((x + bw + 8, y + h / 2), (x + bw + gap - 8, y + h / 2),
                     color=GREY, lw=2.2, head=12)

    wbox(cv, M, 500, W - M * 2,
         ["だから 5 % ブドウ糖液は「血管内を増やす輸液」ではない。"
          "術中に循環血液量を支える目的では使わない。",
          "一方で、水そのものが足りないとき（高 Na 血症、不感蒸泄の補充）には、"
          "これが水を届ける手段になる。"], 14, style="navy")
    return _save(cv, "h5_freewater.png")


# ---------------------------------------------------------------- 図6
def f6_albumin_rbc():
    """アルブミンと赤血球の行き先。"""
    cv = Canvas(W, 1400)
    cv.title(M - 20, 62, "アルブミンと赤血球は、どこにいるのか")

    vx, vw = M + 10, 700
    vy = 170
    gap = 190

    vh = wbox(cv, vx, vy, vw,
              ["アルブミン ●　　　赤血球 ◆",
               "正常でも、体内アルブミンの約 40 % が血管内・約 60 % が血管外に"
               "ある。「入れたら全部ずっと血管内」ではない。"], 13.5,
              style="red", title="血管内（血漿）", title_size=17)
    iy = vy + vh + gap
    ih = wbox(cv, vx, iy, vw,
              ["赤血球はここには出られない（◆ は血管内だけ）。",
               "水と小さな電解質は自由に行き来する。"], 13.5,
              style="amber", title="間質", title_size=17)

    gy = vy + vh
    cv.arrow((vx + 60, gy + 12), (vx + 60, iy - 12),
             color=FILL["amber"][1], lw=2.4, head=12)
    cv.arrow((vx + vw - 60, iy - 12), (vx + vw - 60, gy + 12),
             color=FILL["green"][1], lw=2.4, head=12)
    free = vw - 200
    for dy, txt, style in ((66, "↓ 約 5 %／時が漏れる", "amber"),
                           (128, "↑ リンパ管で血管へ戻る", "green")):
        sz = cv.fit_size([txt], free, 13.5, min_size=10)
        cv.text(vx + vw / 2, gy + dy, txt, size=sz, color=FILL[style][1],
                weight="bold")

    rx = vx + vw + 60
    rw = W - rx - M
    y = vy
    y += wbox(cv, rx, y, rw,
              ["分子そのものの寿命は約 18〜21 日。一方「血管内を増やしている時間」"
               "は半日〜1 日ほど。この 2 つはまったく別の話。",
               "血管内から間質へ漏れる速さ（TER）は正常でも約 5 %／時で、"
               "漏れた分はリンパ管を通って血管へ戻ってくる。"], 13.5,
              style="blue", title="アルブミン", title_size=16) + 26
    y += wbox(cv, rx, y, rw,
              ["炎症・敗血症・大きな手術侵襲でグリコカリックスが傷むと、漏れる"
               "速さが上がり、血管内にとどまる時間は短くなる。"
               "「膠質液だから長く残る」とは限らない。"], 13.5,
              style="amber", title="侵襲があるとき", title_size=16) + 26
    wbox(cv, rx, y, rw,
         ["寿命は約 120 日。ただし保存血では、輸血後 24 時間で 1〜2 割が脾臓・"
          "肝臓で壊される。赤血球は「量」ではなく「酸素を運ぶ力」を足す製剤。"],
         13.5, style="green", title="赤血球", title_size=16)
    return _save(cv, "h6_albumin_rbc.png", crop=True)


# ---------------------------------------------------------------- 図7
def f7_choose():
    """何を届けたいかで選ぶ。"""
    H = 1400
    cv = Canvas(W, H)
    cv.title(M - 20, 62, "選ぶ順番　── 「何 mL 入れるか」の前に「何を届けたいか」")

    top = 130
    hw = 620
    hx = (W - hw) / 2
    hh = wbox(cv, hx, top, hw, ["この患者に足りないのは何か"], 15,
              style="navy", title="まず決める", title_size=17)

    items = [
        ("細胞の中まで含めた「水」", "5 % ブドウ糖液|KN1号輸液",
         "高 Na 血症、水分喪失の補充。血管内容量はほとんど増えない", "purple"),
        ("細胞外液（血漿＋間質）", "生理食塩液|フィジオ140|ソルアセトD",
         "出血・脱水・術中の基本。大量に使うなら Cl⁻ の少ない製剤を", "green"),
        ("血管内容量を素早く", "アルブミン製剤|ボルベン（HES）",
         "適応・上限・禁忌を確認して使う。晶質液の置き換えではない", "blue"),
        ("酸素を運ぶ力", "赤血球濃厚液",
         "Hb を上げる製剤。「500 mL の輸液」として数えない", "red"),
    ]
    n = len(items)
    gap = 26
    bw = (W - M * 2 - gap * (n - 1)) / n

    def need(text, size, nlines=None):
        k = nlines if nlines is not None else len(cv.wrap(text, bw - 32, size))
        return 24 + LH(size, 1.45) * k

    h1 = max(need(it[0], 14) for it in items)
    h2 = max(need(None, 14.5, it[1].count("|") + 1) for it in items)
    h3 = max(need(it[2], 12.5) for it in items)

    y = top + hh + 90
    for i, (need_t, drug, note, style) in enumerate(items):
        x = M + i * (bw + gap)
        cv.arrow((hx + hw / 2, top + hh + 6), (x + bw / 2, y - 8),
                 color=GREY, lw=1.6, head=9)
        wbox(cv, x, y, bw, [need_t], 14, style="grey", min_h=h1)
        textbox(cv, x, y + h1 + 14, bw, drug.split("|"), 14.5,
                style=style, min_h=h2)
        wbox(cv, x, y + h1 + h2 + 28, bw, [note], 12.5, style="grey",
             min_h=h3)

    wbox(cv, M, y + h1 + h2 + h3 + 70, W - M * 2,
         ["そして入れたあとに必ず確かめる ── 血圧が上がったかではなく、"
          "1 回拍出量（心拍出量）が増えたか。"
          "増えていないのに足し続けると、あとに残るのは浮腫だけになる。"], 14,
         style="red")
    return _save(cv, "h7_choose.png", crop=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f1_compartments, f2_barriers, f3_where, f4_na_scale,
               f5_freewater, f6_albumin_rbc, f7_choose):
        fn()
    print("done")
