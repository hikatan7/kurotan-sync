# -*- coding: utf-8 -*-
"""開心術後ALS 配布資料の図版（3点）。figlib で文字を測ってから枠を決める。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from figlib import Canvas, textbox, LH, NAVY, INK, GREY, RED, BLUE, GREEN, PURPLE, ORANGE

OUT = os.path.join(HERE, "..", "図版")
os.makedirs(OUT, exist_ok=True)


def wrapped_box(cv, x, y, w, text_lines, size, style, title=None, tsize=None,
                pad_x=18, pad_y=14, weight="normal", min_h=None, title_color=None):
    """段落のリストを幅に合わせて折り返してから枠に入れる。返り値は高さ"""
    inner = w - 2 * pad_x
    lines = []
    for t in text_lines:
        if t == "":
            lines.append("")
        else:
            lines += cv.wrap(t, inner, size, weight)
    return textbox(cv, x, y, w, lines, size, style=style, pad_x=pad_x, pad_y=pad_y,
                   title=title, title_size=tsize, weight=weight, min_h=min_h,
                   title_color=title_color)


def measure_wrapped(cv, w, text_lines, size, title=None, tsize=None, pad_x=18, pad_y=14):
    inner = w - 2 * pad_x
    n = 0
    for t in text_lines:
        n += 1 if t == "" else len(cv.wrap(t, inner, size))
    return pad_y * 2 + (LH(tsize or size) if title else 0) + LH(size) * n


# ------------------------------------------------------------------ 図1
def fig_algo():
    W, H = 1700, 1560
    cv = Canvas(W, H)
    cv.title(W / 2, 48, "開心術後の心停止 ── 最初の 1 分と 5 分", size=19, ha="center")

    top = ["波形で心停止を認識する（動脈圧・SpO2・EtCO2・心電図）",
           "大声で応援要請　／　6 つの役割を宣言　／　再開胸セットを開く"]
    y = 95
    h = wrapped_box(cv, 120, y, W - 240, top, 12.5, "navy", weight="bold")
    y += h + 40

    cols = [
        ("心室細動／無脈性 VT", "red",
         ["除細動器がすぐ使えるなら", "胸骨圧迫より先に", "3 回連続でショック",
          "（1 分以内に終える）", "", "合間に圧迫を挟まない"]),
        ("心静止／高度徐脈", "blue",
         ["心外膜ワイヤがあれば", "胸骨圧迫より先に", "ペーシング",
          "DDD 80〜100 回/分", "最大出力", "", "1 分で戻らなければ圧迫"]),
        ("無脈性電気活動（PEA）", "purple",
         ["ただちに胸骨圧迫", "", "ペーシング中なら止めて", "隠れた VF を除外する",
          "", "タンポナーデ・出血・", "緊張性気胸を探す"]),
    ]
    gap = 36
    cw = (W - 240 - gap * 2) / 3
    xs = [120 + i * (cw + gap) for i in range(3)]
    # 見出し帯
    for x, (t, st, _) in zip(xs, cols):
        cv.box(x, y, cw, 64, style=st, fc=textcol(st), ec=textcol(st), radius=6)
        s = cv.fit_size([t], cw - 30, 15, weight="bold")
        cv.text(x + cw / 2, y + 32, t, size=s, color="white", weight="bold")
    # 矢印（上の枠から各列へ）
    for x in xs:
        cv.arrow((W / 2, y - 38), (x + cw / 2, y - 4), color=GREY, lw=2)
    y += 64 + 14
    hs = [measure_wrapped(cv, cw, c[2], 11.5) for c in cols]
    hmax = max(hs)
    for x, (t, st, body) in zip(xs, cols):
        wrapped_box(cv, x, y, cw, body, 11.5, st, min_h=hmax)
    y += hmax + 26

    # 1 分で戻らなければ
    for x in xs:
        cv.arrow((x + cw / 2, y - 22), (x + cw / 2, y + 58), color=GREY, lw=2)
    lab = "1 分以内に戻らない（PEA はただちに）"
    lw_ = cv.width(lab, 12.5, "bold") + 40
    cv.rect(W / 2 - lw_ / 2, y + 2, lw_, 40, fc="white", z=4)
    cv.text(W / 2, y + 22, lab, size=12.5, color=NAVY, weight="bold")
    y += 66
    mid = ["胸骨圧迫と換気を開始する（収縮期 60 mmHg 以上を目安に、動脈圧で効果を見る）",
           "VF が続けば 2 分ごとに 1 回ショック。3 回失敗したら",
           "アミオダロン 300 mg またはリドカイン 100 mg を静注",
           "アドレナリン 1 mg を定型で入れない（使うなら経験ある医師の指示で少量）",
           "持続投与をいったん止める（鎮静は続けてよい）。FiO2 100%、PEEP を外す"]
    h = wrapped_box(cv, 120, y, W - 240, mid, 11.5, "grey", title="並行して進めること",
                    tsize=12.5, title_color=NAVY)
    y += h + 30
    cv.arrow((W / 2, y - 26), (W / 2, y + 4), color=RED, lw=2.5)
    y += 8
    last = ["心停止から 5 分以内に緊急再開胸 → 内胸心マッサージ・内部除細動",
            "（術後少なくとも 10 日までは標準の手順。ICU の外なら ICU／手術室へ）",
            "戻らなければ人工心肺の再開、または ECPR（VA-ECMO）"]
    h = wrapped_box(cv, 120, y, W - 240, last, 12.5, "red", weight="bold")
    y += h + 22
    src = "AHA 2025・ERC 2025・STS 2017 をもとに作成。手順の細部は施設のプロトコルに従う。"
    cv.text(W / 2, y + 10, src, size=9.5, color=GREY)
    y += 34
    cv.fig.set_size_inches(W / 200, y / 200)
    cv.ax.set_ylim(y, 0)
    cv.h = y
    cv.save(os.path.join(OUT, "fig1_algorithm.png"))


def textcol(st):
    return {"red": RED, "blue": BLUE, "purple": PURPLE, "green": GREEN,
            "navy": NAVY, "amber": ORANGE}.get(st, NAVY)


# ------------------------------------------------------------------ 図2
def fig_numbers():
    W = 1700
    cv = Canvas(W, 1000)
    cv.title(W / 2, 48, "覚える数字は四つ", size=19, ha="center")
    items = [
        ("3 回", "red", "連続ショックの上限",
         ["成功率は 1 回目 78%、2 回目 35%、3 回目 14%（15 研究の統合値）。",
          "4 回目に賭けるより、再開胸へ進むほうが得が大きい。"]),
        ("1 分", "blue", "胸骨圧迫を待てる時間",
         ["除細動・ペーシングを先に試してよいのは 1 分まで。",
          "PEA では待たない。再開胸がすぐできないなら圧迫する。"]),
        ("5 分", "purple", "再開胸までの目標",
         ["最初の介入で戻らなければ", "5 分以内に胸を開ける。",
          "10 分以内の再開胸で生存退院 48%、10 分超では 12%。"]),
        ("10 日", "green", "再開胸を手順に含める期間",
         ["癒着ができる前の、少なくとも術後 10 日まで。",
          "それ以降・MICS 後は ECPR を代替に考える（ERC 2025）。"]),
    ]
    gap = 30
    cw = (W - 200 - gap) / 2
    y0 = 100
    rows = [items[:2], items[2:]]
    y = y0
    for row in rows:
        hs = []
        for it in row:
            n = sum(len(cv.wrap(t, cw - 270, 11.5)) for t in it[3])
            hs.append(34 + LH(13) * 0.75 + LH(11.5) * n + 34)
        hh = max(hs)
        for i, (big, st, sub, body) in enumerate(row):
            x = 100 + i * (cw + gap)
            cv.box(x, y, cw, hh, style=st, lw=2)
            bs = cv.fit_size([big], 200, 28, weight="bold")
            cv.text(x + 120, y + hh / 2, big, size=bs, color=textcol(st), weight="bold")
            inner_x = x + 245
            lines = []
            for t in body:
                lines += cv.wrap(t, cw - 270, 11.5)
            cv.text(inner_x, y + 34, sub, size=13, color=textcol(st), weight="bold", ha="left")
            for k, ln in enumerate(lines):
                cv.text(inner_x, y + 34 + LH(13) * 0.75 + LH(11.5) * (k + 0.6), ln,
                        size=11.5, ha="left")
        y += hh + gap
    cv.text(W / 2, y + 12, "出典：AHA 2025、ERC 2025、STS 2017、Richardson 2007、Mackay 2002",
            size=9.5, color=GREY)
    y += 40
    cv.fig.set_size_inches(W / 200, y / 200)
    cv.ax.set_ylim(y, 0)
    cv.save(os.path.join(OUT, "fig2_numbers.png"))


# ------------------------------------------------------------------ 図3
def fig_roles():
    W = 1700
    cv = Canvas(W, 1100)
    cv.title(W / 2, 48, "最初に割り当てる 6 つの役割", size=19, ha="center")
    roles = [
        ("1", "外胸心マッサージ", "red",
         ["100〜120 回/分で圧迫", "動脈圧波形で効果を見る", "ショック・ペーシング中は待つ"]),
        ("2", "気道と呼吸", "blue",
         ["FiO2 100%、PEEP を外す", "チューブの位置を確認", "気胸・血胸を除外する"]),
        ("3", "除細動とペーシング", "purple",
         ["ショックとペーシング", "再開胸では", "内部除細動パドルを用意"]),
        ("4", "チームリーダー", "navy",
         ["自分の手は動かさない", "手順が守られているか", "役割に人がいるかを見る"]),
        ("5", "薬剤とシリンジポンプ", "amber",
         ["持続投与を止め", "再開を管理する", "アドレナリンは指示時のみ"]),
        ("6", "ICU コーディネーター", "green",
         ["人と物を集める", "再開胸セットを開く", "清潔の準備を始める"]),
    ]
    gap = 28
    cw = (W - 200 - gap * 2) / 3
    y = 100
    for r in range(2):
        row = roles[r * 3:(r + 1) * 3]
        bsz = cv.fit_size([l for rr in roles for l in rr[3]], cw - 44, 11.5)
        hh = 88 + LH(bsz) * 3 + 20
        for i, (no, t, st, body) in enumerate(row):
            x = 100 + i * (cw + gap)
            cv.box(x, y, cw, hh, style=st, lw=2.2)
            cv.box(x + 18, y + 16, 54, 54, style=st, fc=textcol(st), ec=textcol(st), radius=6)
            cv.text(x + 45, y + 43, no, size=19, color="white", weight="bold")
            s = cv.fit_size([t], cw - 110, 14, weight="bold")
            cv.text(x + 88, y + 43, t, size=s, color=textcol(st), weight="bold", ha="left")
            for k, ln in enumerate(body):
                cv.text(x + 22, y + 88 + LH(bsz) * (k + 0.5), ln, size=bsz, ha="left")
        y += hh + gap
    h = wrapped_box(cv, 100, y, W - 200,
                    ["役割を先に決めないと、全員が胸骨の上に集まり、気道・ペーシング・器械を見る人がいなくなる。",
                     "EACTS 2009 が置き、STS 2017 が引き継いだ。定期的なリハーサルまでが推奨である。"],
                    11.5, "grey")
    y += h + 20
    cv.fig.set_size_inches(W / 200, y / 200)
    cv.ax.set_ylim(y, 0)
    cv.save(os.path.join(OUT, "fig3_roles.png"))


if __name__ == "__main__":
    fig_algo()
    fig_numbers()
    fig_roles()
    print("ok")
