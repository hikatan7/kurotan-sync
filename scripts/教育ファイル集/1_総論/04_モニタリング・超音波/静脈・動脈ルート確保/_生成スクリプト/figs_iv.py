# -*- coding: utf-8 -*-
"""静脈・動脈ルート確保の図版。figlib で文字を測ってから枠を決め、保存後に余白を切り詰める。"""
import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageChops
from figlib import Canvas, textbox, boxrow, LH, NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE, FILL

OUT = os.path.join(HERE, "..", "図版")
os.makedirs(OUT, exist_ok=True)


def save(cv, name):
    p = os.path.join(OUT, name)
    cv.save(p)
    im = Image.open(p).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        pad = 24
        l, t, r, b = bbox
        im = im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))
    im.save(p)
    print("saved", name, im.size)


def col(st):
    return FILL[st][1]


# ---------------------------------------------------------------- 図1 デバイスの選び方
def fig_device():
    W = 1700
    cv = Canvas(W, 1500)
    cv.title(W / 2, 50, "末梢ルートは「何を・何日・どれだけ」で選ぶ", size=20, ha="center")
    y = 110
    h = textbox(cv, 150, y, W - 300,
                ["何を入れるか（末梢から入れてよい薬か、起壊死性・刺激性か）",
                 "何日使うか（予定期間）／どれだけ速く入れるか（急速輸液の要否）"],
                15, style="navy", weight="bold")
    y += h + 70
    cv.arrow((W / 2, y - 62), (W / 2, y - 8), lw=2.4, head=14)
    items = [
        ("5 日以内", ["短い末梢カテーテル", "見つからなければ", "超音波ガイド下で"], "green"),
        ("6〜14 日", ["ミッドラインまたは", "超音波ガイド下の", "長めの末梢カテーテル", "（PICC より優先）"], "blue"),
        ("15 日以上・起壊死性", ["PICC または", "中心静脈カテーテル", "重症で 14 日以内なら", "非トンネル型 CVC"], "purple"),
    ]
    gap = 50
    bw = (W - 300 - 2 * gap) / 3
    h = boxrow(cv, 150, y, bw, gap, items, 15, title_size=17)
    y += h + 50
    h = textbox(cv, 150, y, W - 300,
                ["CDC 2011：6 日を超えそうならミッドラインか PICC（カテゴリー II）",
                 "壊死を起こしうる薬液に金属針（翼状針）を使わない（カテゴリー IA）"],
                14, style="grey")
    cv.h = y + h + 40
    save(cv, "fig1_device.png")


# ---------------------------------------------------------------- 図2 前腕の危険域
def fig_forearm():
    W, H = 1700, 1400
    cv = Canvas(W, H)
    cv.title(W / 2, 50, "前腕・肘窩で神経損傷が起きやすい 3 か所（右前腕・手掌側の模式図）", size=18, ha="center")
    import numpy as np
    from matplotlib.patches import Circle
    x0, x1, yt, yb = 170, 1530, 200, 690
    cv.text(x0 + 10, yt - 32, "橈側（母指側）", size=14, color=GREY, ha="left")
    cv.text(x0 + 10, yb + 32, "尺側（小指側）", size=14, color=GREY, ha="left")
    cv.text(x0 - 20, (yt + yb) / 2, "手関節", size=15, color=GREY, ha="right")
    cv.text(x1 + 20, (yt + yb) / 2, "肘", size=15, color=GREY, ha="left")
    cv.box(x0, yt, x1 - x0, yb - yt, style="grey", fc="#fbf7f2", ec="#b9a99a", lw=2.2, radius=60)
    ax = cv.ax
    xs = np.linspace(x0 + 25, x1 - 25, 200)
    ceph = yt + 90 + 14 * np.sin((xs - x0) / 160)
    basil = yb - 90 + 12 * np.sin((xs - x0) / 190 + 1)
    ax.plot(xs, ceph, color=BLUE, lw=7, solid_capstyle="round", zorder=3)
    ax.plot(xs, basil, color=BLUE, lw=7, solid_capstyle="round", zorder=3)
    ax.plot([1200, 1440], [basil[155], ceph[188]], color=BLUE, lw=7, zorder=3)
    dash = dict(color=ORANGE, lw=4.5, ls=(0, (6, 4)), zorder=4)
    sx = np.linspace(x0 + 25, 650, 80)
    ax.plot(sx, yt + 70 + 28 * np.sin((sx - x0) / 70), **dash)
    lx = np.linspace(1250, x1 - 25, 40)
    ax.plot(lx, ceph[-40:] + 12 * np.sin(lx / 30), **dash)
    mx = np.linspace(1200, x1 - 25, 40)
    ax.plot(mx, basil[-40:] - 10 * np.sin(mx / 28), **dash)
    zones = [(x0 + 12, yt + 18, 650 - x0, 170, "1", 650 + 45, yt + 100),
             (1240, yt + 18, x1 - 1252, 160, "2", 1200, yt + 100),
             (1180, yb - 190, x1 - 1192, 172, "3", 1140, yb - 100)]
    for zx, zy, zw, zh, n, cx, cy in zones:
        cv.rect(zx, zy, zw, zh, fc=RED, alpha=0.13, z=2)
        ax.add_patch(Circle((cx, cy), 30, facecolor=RED, zorder=6))
        cv.text(cx, cy, n, size=17, color="white", weight="bold", z=7)
    cv.arrow((x0 + 12, yt + 260), (650, yt + 260), color=RED, lw=2.4, head=12, style="<|-|>")
    cv.text((x0 + 650) / 2, yt + 296, "橈骨茎状突起から約 12 cm", size=15, color=RED, weight="bold")
    # 説明（図の外に置く）
    y = yb + 90
    rows = [("1", "手関節の橈側皮静脈", "橈骨神経浅枝が静脈と交差・並走する"),
            ("2", "肘窩の橈側", "外側前腕皮神経が静脈の上や下を走る"),
            ("3", "肘窩の尺側", "内側前腕皮神経・正中神経・上腕動脈が近い")]
    for n, a, b in rows:
        ax.add_patch(Circle((215, y), 24, facecolor=RED, zorder=6))
        cv.text(215, y, n, size=15, color="white", weight="bold", z=7)
        cv.text(260, y, a, size=15.5, color=NAVY, weight="bold", ha="left")
        cv.text(720, y, b, size=15, color=INK, ha="left")
        y += 66
    y += 20
    ax.plot([215, 295], [y, y], color=BLUE, lw=7)
    cv.text(310, y, "皮静脈", size=14, ha="left")
    ax.plot([520, 600], [y, y], color=ORANGE, lw=4.5, ls=(0, (6, 4)))
    cv.text(615, y, "皮神経", size=14, ha="left")
    cv.rect(830, y - 18, 70, 36, fc=RED, alpha=0.13)
    cv.text(915, y, "神経損傷の危険域", size=14, ha="left")
    cv.text(W / 2, y + 70, "交差する位置には個人差が大きく、「安全な範囲」は定義できない。図は位置関係の目安である。",
            size=13.5, color=GREY)
    save(cv, "fig2_forearm.png")


# ---------------------------------------------------------------- 図3 ポアズイユの法則
def fig_flow():
    W, H = 1700, 1250
    cv = Canvas(W, H)
    cv.title(W / 2, 50, "流量は内径の 4 乗に比例し、長さに反比例する", size=20, ha="center")
    textbox(cv, 380, 100, W - 760, ["流量 ∝ ΔP × r⁴ ／（η × L）"], 18, style="navy", weight="bold")
    # 棒グラフ：相対流量
    items = [("基準", 1.0, "内径 1.0・長さ 1.0"), ("内径 1.2 倍", 1.2 ** 4, "同じ長さ"),
             ("内径 1.5 倍", 1.5 ** 4, "同じ長さ"), ("長さ 2 倍", 0.5, "同じ内径")]
    bx, by, bh = 260, 330, 480
    maxv = 5.5
    bw = 220
    gap = (W - 2 * bx - 4 * bw) / 3
    ax = cv.ax
    ax.plot([bx - 30, W - bx + 30], [by + bh, by + bh], color=GREY, lw=1.5)
    for i, (lab, v, sub) in enumerate(items):
        x = bx + i * (bw + gap)
        hh = bh * v / maxv
        c = [GREY, BLUE, BLUE, RED][i]
        cv.rect(x, by + bh - hh, bw, hh, fc=c, alpha=0.85)
        cv.text(x + bw / 2, by + bh - hh - 30, "%.1f 倍" % v, size=17, color=c, weight="bold")
        cv.text(x + bw / 2, by + bh + 40, lab, size=16, color=NAVY, weight="bold")
        cv.text(x + bw / 2, by + bh + 82, sub, size=14, color=GREY)
    textbox(cv, 200, by + bh + 140, W - 400,
            ["急速輸液には「太く・短い」カテーテル。延長チューブや",
             "ニードルレスコネクタも流量を落とす（実測で最大 41%）"],
            15, style="amber")
    save(cv, "fig3_flow.png")


# ---------------------------------------------------------------- 図4 針先を追う（DNTP）
def fig_dntp():
    W, H = 1700, 1350
    cv = Canvas(W, H)
    cv.title(W / 2, 50, "短軸で針先を追う（dynamic needle tip positioning）", size=20, ha="center")
    from matplotlib.patches import Circle
    steps = [
        ("1", "針先を血管の真上に", ["白い点が見えたら", "その位置で針を止める"], "top"),
        ("2", "プローブを少し近位へ", ["点が消える", "＝針先より先を見ている"], "none"),
        ("3", "針を進めて点を戻す", ["点が再び現れた位置が", "その時点の針先"], "mid"),
        ("4", "管腔の中央まで繰り返す", ["血管内で針先を数 mm", "進めてから外套を送る"], "in"),
    ]
    pw, ph, gx, gy = 740, 470, 60, 40
    for i, (n, a, body, pos) in enumerate(steps):
        x = 100 + (i % 2) * (pw + gx)
        y = 110 + (i // 2) * (ph + gy)
        cv.box(x, y, pw, ph, style="grey", fc="white", ec="#9aa6b4", lw=2)
        cv.text(x + 45, y + 50, n, size=24, color=NAVY, weight="bold")
        cv.text(x + 85, y + 50, a, size=17, color=NAVY, weight="bold", ha="left")
        sx, sy, sw, sh = x + 30, y + 100, 250, 330
        cv.rect(sx, sy, sw, sh, fc="#2b3038")
        cx, cy = sx + sw / 2, sy + sh / 2 + 10
        cv.ax.add_patch(Circle((cx, cy), 62, facecolor="#11151a", edgecolor=BLUE, lw=4, zorder=3))
        dot = {"top": (cx, cy - 100), "mid": (cx, cy - 66), "in": (cx, cy), "none": None}[pos]
        if dot:
            cv.ax.add_patch(Circle(dot, 10, facecolor="white", zorder=4))
        cv.text(cx, sy + sh - 24, "静脈（短軸）", size=12.5, color="#9cc3e6")
        tw = pw - sw - 80
        fs = cv.fit_size(body, tw, 17)
        cv.block(sx + sw + 25, sy + 100, tw, body, fs, color=INK, ha="left")
    yb = 110 + 2 * ph + gy + 40
    cv.text(W / 2, yb, "画面の白い点は「走査面と針の交点」であって、針先とは限らない。",
            size=14.5, color=GREY)
    cv.text(W / 2, yb + 45, "点を追わずに針を進めないことが、後壁の貫通と血腫を減らす。", size=14.5, color=GREY)
    save(cv, "fig4_dntp.png")


# ---------------------------------------------------------------- 図5 浸透圧の許容範囲と時間
def fig_osm():
    W, H = 1700, 1000
    cv = Canvas(W, H)
    cv.title(W / 2, 50, "末梢静脈が耐えられる浸透圧は、投与時間が長いほど下がる", size=19, ha="center")
    data = [("8 時間", 820), ("12 時間", 690), ("24 時間", 550)]
    bx, by, bh, bw = 330, 160, 520, 260
    maxv = 1000
    gap = (W - 2 * bx - 3 * bw) / 2
    ax = cv.ax
    ax.plot([bx - 40, W - bx + 40], [by + bh, by + bh], color=GREY, lw=1.5)
    # 等張の目安
    yi = by + bh - bh * 290 / maxv
    ax.plot([bx - 40, W - bx + 40], [yi, yi], color=GREEN, lw=2, ls="--")
    cv.text(W - bx + 50, yi, "血漿 ≒ 290", size=13.5, color=GREEN, ha="left")
    for i, (lab, v) in enumerate(data):
        x = bx + i * (bw + gap)
        hh = bh * v / maxv
        cv.rect(x, by + bh - hh, bw, hh, fc=ORANGE, alpha=0.85)
        cv.text(x + bw / 2, by + bh - hh - 30, "約 %d" % v, size=18, color=ORANGE, weight="bold")
        cv.text(x + bw / 2, by + bh + 40, lab, size=16, color=NAVY, weight="bold")
    cv.text(bx - 60, by - 10, "mOsm/kg", size=13.5, color=GREY, ha="left")
    textbox(cv, 200, by + bh + 90, W - 400,
            ["ウサギ耳静脈の実験。速く入れて投与時間を短くすると静脈炎が減った",
             "酸性（pH 4.9）の液は浸透圧が低くても静脈炎を起こした"],
            14.5, style="grey")
    save(cv, "fig5_osm.png")


# ---------------------------------------------------------------- 図6 静脈炎の 3 機序
def fig_phleb():
    W = 1700
    cv = Canvas(W, 1300)
    cv.title(W / 2, 50, "静脈炎は原因で 3 つに分けると予防が決まる", size=20, ha="center")
    items = [
        ("機械的", ["原因：挿入時の損傷、", "太すぎる針、関節部、", "固定不良による", "カテーテルの動き", "",
                  "予防：必要最小の太さ、", "屈曲部を避ける、", "ハブをしっかり固定"], "blue"),
        ("化学的", ["原因：酸性・アルカリ性・", "高浸透圧の薬液、", "乾く前の消毒薬", "",
                  "予防：太い静脈・十分な", "血流で希釈、消毒薬を", "乾かす、刺激性薬は中心へ"], "amber"),
        ("細菌性", ["原因：手指衛生・皮膚消毒・", "ドレッシングの不備、", "回路の開放、長期留置", "",
                  "予防：アルコール含有の", "クロルヘキシジン、閉鎖回路、", "毎勤務の観察、不要なら抜去"], "red"),
    ]
    gap = 40
    bw = (W - 200 - 2 * gap) / 3
    h = boxrow(cv, 100, 110, bw, gap, items, 14.5, title_size=19)
    textbox(cv, 100, 110 + h + 40, W - 200,
            ["どの型でも、発赤・疼痛・腫脹・索状硬結が出たら抜去する（CDC 2011：カテゴリー IB）"],
            14.5, style="navy", weight="bold")
    save(cv, "fig6_phlebitis.png")


# ---------------------------------------------------------------- 図7 動脈ラインの合併症頻度
def fig_aline():
    W, H = 1700, 1150
    cv = Canvas(W, H)
    cv.title(W / 2, 50, "橈骨動脈ラインの合併症 ── 多いものは軽く、重いものはまれ", size=19, ha="center")
    data = [("一過性の動脈閉塞", 19.7, BLUE), ("血腫", 14.4, BLUE), ("局所感染", 0.72, ORANGE),
            ("出血", 0.53, ORANGE), ("敗血症", 0.13, RED), ("永続的な虚血", 0.09, RED),
            ("仮性動脈瘤", 0.09, RED)]
    lx, rx, y0, rh = 430, 1500, 130, 108
    lo, hi = math.log10(0.05), math.log10(30)
    ax = cv.ax
    for t in (0.1, 1, 10):
        xx = lx + (rx - lx) * (math.log10(t) - lo) / (hi - lo)
        ax.plot([xx, xx], [y0 - 10, y0 + rh * len(data)], color="#d5dae0", lw=1.2, zorder=1)
        cv.text(xx, y0 + rh * len(data) + 30, "%g%%" % t, size=13.5, color=GREY)
    for i, (lab, v, c) in enumerate(data):
        y = y0 + i * rh
        xx = lx + (rx - lx) * (math.log10(v) - lo) / (hi - lo)
        cv.rect(lx, y + 18, xx - lx, rh - 40, fc=c, alpha=0.85, z=2)
        cv.text(lx - 20, y + rh / 2, lab, size=15.5, color=NAVY, weight="bold", ha="right")
        cv.text(xx + 15, y + rh / 2, "%g%%" % v, size=15, color=c, weight="bold", ha="left")
    cv.text(W / 2, y0 + rh * len(data) + 85, "横軸は対数目盛。橈骨動脈 19,617 本を集めた系統的レビューの値",
            size=13.5, color=GREY)
    save(cv, "fig7_aline.png")


if __name__ == "__main__":
    for f in (fig_device, fig_forearm, fig_flow, fig_dntp, fig_osm, fig_phleb, fig_aline):
        f()
