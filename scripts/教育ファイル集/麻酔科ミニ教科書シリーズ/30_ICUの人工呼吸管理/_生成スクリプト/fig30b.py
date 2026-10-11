# -*- coding: utf-8 -*-
"""㉚ 図版 第III部・第IV部（図13-1 〜 図25-1）"""
from fig30common import (W, Canvas, Panel, LH, head, path, legend, decay,
                         textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                         ORANGE, PURPLE, C_PRES, C_FLOW, C_VOL, C_NOTE)


def f13():
    """三つの波形の読み所"""
    cv = Canvas(W, 1400)
    y = head(cv, "図13-1　三つの波形の読み所",
             "モードが分かれば、どれが「機械の意思」で、どれが「肺の応答」かが決まる。"
             "見るのは応答した側である。")
    x = 190
    w = W - x - 90
    p1 = Panel(cv, x, y, w, 210, "圧", color=C_PRES)
    p1.plot([(0, .14), (.05, .12), (.08, .44), (.16, .56), (.19, .48),
             (.23, .60), (.40, .82), (.43, .14),
             (.56, .14), (.60, .12), (.63, .44), (.95, .82), (.98, .14),
             (1.0, .14)], color=C_PRES)
    p1.caption("量規定なら「肺の応答」／圧規定なら「機械の意思」", color=C_PRES)
    p1.note(.30, .30, "立ち上がりの凹み＝患者の努力", color=C_NOTE, size=12)

    p2 = Panel(cv, x, y + 280, w, 210, "流量", color=C_FLOW, base=.5)
    p2.plot([(0, .5), (.07, .5), (.08, .86), (.41, .86), (.43, .12)] +
            decay(.43, .56, .12, .48) + [(.60, .5), (.62, .5), (.63, .86),
            (.96, .86), (.98, .12)] + decay(.98, 1.0, .12, .30), color=C_FLOW)
    p2.caption("まず呼気側を見る ── 基線に戻っているか", color=C_FLOW)
    p2.note(.52, .22, "ここが戻りきる前に次の吸気なら auto-PEEP",
            color=C_NOTE, size=12)

    p3 = Panel(cv, x, y + 560, w, 210, "量", color=C_VOL)
    p3.plot([(0, .08), (.08, .08), (.41, .80), (.56, .10), (.63, .08),
             (.96, .80), (1.0, .34)], color=C_VOL)
    p3.caption("吸気量と呼気量の差＝リーク", color=C_VOL)
    p3.note(.30, .28, "呼気側が戻りきらない＝リーク／エアトラッピング",
            color=C_NOTE, size=12)

    y2 = y + 560 + 210 + 56
    textbox(cv, 56, y2, W - 112, [
        "① 呼気流量は基線に戻っているか（auto-PEEP）",
        "② 吸気圧の立ち上がりに凹みはないか（患者の努力）／階段状なら回路",
        "③ 吸気量と呼気量は一致しているか（リーク）",
        "④ 一回ごとの形はそろっているか（非同調は「ばらつき」として見える）",
    ], 14, style="navy", title="波形を見る順番（一巡10秒）", title_size=15)
    cv.save(path("f13_three_waveforms.png"))


def f14():
    """吸気ポーズによる圧の分解"""
    cv = Canvas(W, 1300)
    y = head(cv, "図14-1　吸気ポーズで圧を分解する",
             "同じピーク圧でも、中身が違えば取るべき手はまったく違う。")
    x = 230
    w = W - x - 430
    p = Panel(cv, x, y, w, 330, "気道内圧", color=C_PRES)
    p.plot([(0, .14), (.06, .12), (.09, .44), (.42, .88), (.44, .60),
            (.62, .58), (.64, .14), (.86, .14), (.90, .12), (.93, .44),
            (1.0, .70)], color=C_PRES)
    p.hline(.88, color="#c9d2dc", t0=.42, t1=1.0)
    p.hline(.58, color="#c9d2dc", t0=.44, t1=1.0)
    p.hline(.14, color="#9aa6b4", t0=0, t1=1.0)
    p.label_left(.88, "ピーク圧")
    p.label_left(.58, "プラトー圧")
    p.label_left(.14, "総 PEEP")
    p.caption("吸気ポーズ＝流れを止めて抵抗成分を消す", color=C_PRES)
    # 右側の寸法線
    xr = p.px(1.0) + 40
    cv.arrow((xr, p.py(.88)), (xr, p.py(.58)), color=ORANGE, lw=2.2, head=12,
             style="<|-|>")
    cv.arrow((xr, p.py(.58)), (xr, p.py(.14)), color=PURPLE, lw=2.2, head=12,
             style="<|-|>")
    cv.text(xr + 16, (p.py(.88) + p.py(.58)) / 2, "抵抗成分", size=13,
            color=ORANGE, ha="left", weight="bold")
    cv.text(xr + 16, (p.py(.58) + p.py(.14)) / 2, "駆動圧", size=13,
            color=PURPLE, ha="left", weight="bold")
    cv.text(xr + 16, (p.py(.58) + p.py(.14)) / 2 + 42, "（弾性成分）", size=12,
            color=PURPLE, ha="left")

    y2 = y + 330 + 60
    bw = (W - 112 - 40) / 2
    textbox(cv, 56, y2, bw, [
        "ピーク圧 − プラトー圧",
        "気道・チューブを通すための圧",
        "上がったら：分泌物・屈曲・攣縮・噛み込み",
    ], 14, style="amber", title="抵抗成分", title_size=15, min_h=210)
    textbox(cv, 56 + bw + 40, y2, bw, [
        "プラトー圧 − 総 PEEP ＝ 駆動圧",
        "一回換気量 ÷ コンプライアンス",
        "上がったら：肺水腫・無気肺・気胸・腹圧",
    ], 14, style="purple", title="弾性成分（駆動圧）", title_size=15, min_h=210)

    y3 = y2 + 210 + 44
    textbox(cv, 56, y3, W - 112, [
        "プラトー圧には胸壁の硬さも含まれる（肥満・高腹圧では高く出る）",
        "肺そのものが受けている圧を知りたければ、食道内圧が要る（第16章）",
    ], 14, style="grey", title="プラトー圧を読むときの注意", title_size=15)
    cv.save(path("f14_pressure_decomposition.png"))


def f15():
    """auto-PEEP"""
    cv = Canvas(W, 1360)
    y = head(cv, "図15-1　auto-PEEP（内因性 PEEP）",
             "吐ききる前に次の吸気が始まれば、肺胞に圧が残る。画面の PEEP には含まれない。")
    x = 210
    w = W - x - 90
    p1 = Panel(cv, x, y, w, 230, "呼気流量", color=C_FLOW, base=.78)
    ex = []
    for i in range(4):
        t0 = i * .25
        ex += [(t0 + .02, .78), (t0 + .04, .96), (t0 + .12, .96),
               (t0 + .14, .30)] + decay(t0 + .14, t0 + .24, .30, .66, n=12)
    p1.plot(ex, color=C_FLOW)
    p1.hline(.78, color="#9aa6b4")
    p1.caption("① 呼気流量が基線に戻る前に次の吸気が始まる", color=C_NOTE)
    p1.note(.62, .50, "ここで途切れている", color=C_NOTE, size=12.5)

    p2 = Panel(cv, x, y + 300, w, 230, "気道内圧（呼気ポーズ）", color=C_PRES)
    p2.plot([(0, .22), (.04, .80), (.16, .80), (.18, .22), (.26, .22),
             (.30, .80), (.42, .80), (.44, .22), (.52, .22), (.56, .80),
             (.68, .80), (.70, .22), (.74, .22), (.76, .40), (1.0, .40)],
            color=C_PRES)
    p2.hline(.22, color="#9aa6b4", t0=0, t1=.76)
    p2.hline(.40, color=ORANGE, t0=.74, t1=1.0)
    p2.label_left(.22, "設定 PEEP")
    p2.caption("② 呼気ポーズで、隠れていた圧が画面に現れる", color=ORANGE)
    p2.note(.82, .60, "総 PEEP（auto-PEEP を含む）", color=ORANGE, size=12.5)

    y2 = y + 300 + 230 + 56
    bw = (W - 112 - 2 * 34) / 3
    from figlib import boxrow
    hh = boxrow(cv, 56, y2, bw, 34, [
        ("循環", ["胸腔内圧が上がり続ける", "→ 静脈還流が減り血圧が下がる"], "red"),
        ("トリガ", ["残った陽圧を打ち消すまで", "吸気が始まらない（ミストリガ）"], "amber"),
        ("換気効率", ["過膨張した領域は死腔になる", "→ 回数を上げても CO₂ が下がらない"], "blue"),
    ], 13.5, title_size=15, min_h=170)
    y3 = y2 + hh + 44
    textbox(cv, 56, y3, W - 112, [
        "呼気時間を延ばす（換気回数を下げる・吸気時間を短くする）",
        "気道抵抗を下げる（気管支拡張薬・吸引）／一回換気量を減らす",
        "外因性 PEEP を足してトリガを楽にする ── ただし auto-PEEP の手前まで",
    ], 14, style="green", title="auto-PEEP を減らす手", title_size=15)
    cv.save(path("f15_autopeep.png"))


def f16():
    """経肺圧"""
    cv = Canvas(W, 1420)
    y = head(cv, "図16-1　圧の分け前 ── 経肺圧という考え方",
             "気道内圧は、肺をふくらませるぶんと胸郭を押しのけるぶんに分かれる。")
    bar_x, bar_w = 56, W - 112
    rows = (
        ("ふつうの胸壁", .58, .42, "気道内圧の多くが肺に届く", GREY),
        ("胸壁が硬い（肥満・高腹圧）", .32, .68,
         "同じ気道内圧でも、肺に届く分は小さい", GREY),
        ("強い自発呼吸", .96, -.16,
         "胸腔内圧が下がるぶん、経肺圧はかえって大きくなる", RED),
    )
    yy = y
    for name, lung, chest, memo, ccol in rows:
        cv.text(bar_x, yy - 26, name, size=14, color=INK, ha="left",
                weight="bold")
        lw_ = bar_w * lung
        cv.rect(bar_x, yy, lw_, 64, fc="#cfe0f0", ec=BLUE, lw=1.4)
        cv.text(bar_x + lw_ / 2, yy + 32, "経肺圧（肺が受ける伸び）", size=13,
                color=BLUE, va="center")
        if chest >= 0:
            cv.rect(bar_x + lw_, yy, bar_w * chest, 64,
                    fc="#e9edf2", ec=GREY, lw=1.4)
            cv.text(bar_x + lw_ + bar_w * chest / 2, yy + 32, "胸腔内圧",
                    size=13, color=GREY, va="center")
        else:
            cv.rect(bar_x + lw_ + bar_w * chest, yy, -bar_w * chest, 64,
                    fc="#fbe3e0", ec=RED, lw=1.4)
            cv.text(bar_x + lw_ + bar_w * chest / 2, yy + 32, "陰圧",
                    size=12.5, color=RED, va="center")
        cv.text(bar_x, yy + 96, memo, size=12.5, color=ccol, ha="left")
        yy += 170

    y2 = yy + 20
    bw = (W - 112 - 40) / 2
    textbox(cv, 56, y2, bw, [
        "食道バルーンで胸腔内圧を推定する",
        "胸壁由来で気道内圧が高いなら、",
        "PEEP を下げる理由にはならない",
        "食道内圧を基準にした PEEP 設定が",
        "予後を改善した証拠はまだない",
    ], 13.5, style="blue", title="測る ── 食道内圧", title_size=15, min_h=260)
    textbox(cv, 56 + bw + 40, y2, bw, [
        "呼気終末に一度だけ気道を閉塞する",
        "患者の努力で気道内圧が",
        "どれだけ落ちるかを見る（ΔPocc）",
        "特別なカテーテルが要らないので、",
        "日常の確認に使いやすい",
    ], 13.5, style="green", title="測る ── 呼気終末閉塞", title_size=15, min_h=260)
    cv.save(path("f16_transpulmonary.png"))


def f17():
    """VILI の四つの機序"""
    cv = Canvas(W, 1180)
    y = head(cv, "図17-1　人工呼吸器関連肺傷害（VILI）の四つの機序",
             "臨床の操作は、この四つのどれかに効いている。")
    bw = (W - 112 - 3 * 30) / 4
    items = (
        ("① 過伸展", "volutrauma", ["容量を超えて引き伸ばされ", "上皮と内皮が壊れる"],
         "効く操作：一回換気量・駆動圧を下げる", "red"),
        ("② 虚脱と再開放", "atelectrauma", ["呼気ごとにつぶれ", "吸気ごとに開く"],
         "効く操作：PEEP・体位", "amber"),
        ("③ 圧による破綻", "barotrauma", ["気胸・縦隔気腫として", "目に見える形で現れる"],
         "効く操作：圧の上限を守る", "blue"),
        ("④ 炎症の波及", "biotrauma", ["局所のサイトカインが", "血流に乗って全身へ"],
         "効く操作：①〜③を減らすこと", "purple"),
    )
    def _w(ls, s):
        out = []
        for l in ls:
            out += cv.wrap(l, bw - 28, s) if l else [""]
        return out
    n_t, n_p = len(cv.ax.texts), len(cv.ax.patches)
    h1 = max(textbox(cv, -5000, y, bw, _w(lines + ["", en], 13.5), 13.5,
                     title=ttl, title_size=16) for ttl, en, lines, act, st in items)
    h2 = max(textbox(cv, -5000, y, bw, _w([act], 12.5), 12.5) for *_, act, st in items)
    for a in list(cv.ax.texts[n_t:]) + list(cv.ax.patches[n_p:]):
        a.remove()
    h1, h2 = max(h1, 260), max(h2, 110)
    for i, (ttl, en, lines, act, st) in enumerate(items):
        x = 56 + i * (bw + 30)
        textbox(cv, x, y, bw, _w(lines + ["", en], 13.5), 13.5, style=st,
                title=ttl, title_size=16, min_h=h1)
        textbox(cv, x, y + h1 + 30, bw, _w([act], 12.5), 12.5, style="grey",
                min_h=h2)
    y2 = y + h1 + 30 + h2 + 50
    textbox(cv, 56, y2, W - 112, [
        "壊すのは「圧」そのものより「伸び」である ── 1974年の実験が起点",
        "PEEP が効くのは主に②に対して。①には一回換気量・駆動圧の制限が効く",
        "メカニカルパワーは①〜③を一つの量にまとめる試み。観察研究では死亡率と相関するが、"
        "下げる介入で予後が改善した試験はまだない",
    ], 14, style="navy", title="四つをつなぐ見方", title_size=15)
    cv.save(path("f17_vili_four.png"))


def f18():
    """呼吸ドライブ"""
    cv = Canvas(W, 1240)
    y = head(cv, "図18-1　呼吸ドライブは低すぎても高すぎても害になる",
             "鎮静の深さを決めるとき、私たちは呼吸中枢からの指令の強さを調節している。")
    x = 210
    w = (W - x - 90 - 80) / 3
    specs = (
        ("低すぎる", C_NOTE, [(0, .5), (.2, .5), (.26, .60), (.34, .5),
                              (.7, .5), (.76, .58), (.84, .5), (1.0, .5)],
         "無呼吸・トリガ消失", "red"),
        ("ちょうどよい", GREEN, [(0, .5), (.08, .74), (.22, .5), (.30, .5),
                                 (.38, .74), (.52, .5), (.60, .5), (.68, .74),
                                 (.82, .5), (1.0, .5)],
         "規則的・補助呼吸筋を使わない", "green"),
        ("高すぎる", C_NOTE, [(0, .5), (.05, .96), (.14, .5), (.18, .5),
                              (.23, .96), (.32, .5), (.36, .5), (.41, .96),
                              (.50, .5), (.54, .5), (.59, .96), (.68, .5),
                              (.72, .5), (.77, .96), (.86, .5), (1.0, .5)],
         "強い努力・二段呼吸・経肺圧の大振れ", "red"),
    )
    for i, (ttl, col, pts, memo, st) in enumerate(specs):
        px = x + i * (w + 40)
        cv.text(px + w / 2, y - 32, ttl, size=15.5, weight="bold", color=col)
        p = Panel(cv, px, y, w, 230, "努力" if i == 0 else "", color=col, base=.5)
        p.plot(pts, color=col)
        textbox(cv, px, y + 270, w, [memo], 13, style=st, min_h=130)
    y2 = y + 270 + 130 + 50
    bw = (W - 112 - 40) / 2
    textbox(cv, 56, y2, bw, [
        "低酸素血症・アシドーシス・発熱・疼痛・不安",
        "肺そのものの炎症による受容器刺激",
        "鎮静薬が効くのは、このうち不安と疼痛だけ",
    ], 13.5, style="amber", title="ドライブを上げる要因", title_size=15, min_h=210)
    textbox(cv, 56 + bw + 40, y2, bw, [
        "P0.1（吸気開始 0.1 秒の気道閉塞圧）",
        "食道内圧の振れ、ΔPocc",
        "Edi（横隔膜の電気活動）",
    ], 13.5, style="blue", title="ドライブを測る道具", title_size=15, min_h=210)
    cv.save(path("f18_drive.png"))


def f19():
    """非同調の波形"""
    cv = Canvas(W, 1320)
    y = head(cv, "図19-1　代表的な非同調",
             "波形の「どこが」ずれているかで、触る設定が決まる。")
    cols, rows_n = 3, 2
    bw = (W - 112 - (cols - 1) * 40) / cols
    specs = (
        ("① ミストリガ", "努力はあるが送気がない", ORANGE,
         [(0, .5), (.06, .46), (.10, .90), (.26, .88), (.30, .5), (.40, .5),
          (.44, .42), (.48, .5), (.62, .5), (.66, .46), (.70, .90), (.86, .88),
          (.90, .5), (1.0, .5)], (.44, .30, "努力の跡だけ")),
        ("② オートトリガ", "努力がないのに送気される", BLUE,
         [(0, .5), (.06, .46), (.10, .90), (.26, .88), (.30, .5), (.36, .5),
          (.40, .90), (.56, .88), (.60, .5), (.70, .5), (.74, .46), (.78, .90),
          (.94, .88), (.98, .5), (1.0, .5)], (.48, .30, "引き金がない")),
        ("③ ダブルトリガ", "一回の努力に二回の送気", RED,
         [(0, .5), (.06, .46), (.10, .90), (.24, .88), (.27, .52), (.30, .90),
          (.44, .88), (.48, .5), (.62, .5), (.66, .46), (.70, .90), (.84, .88),
          (.87, .52), (.90, .90), (1.0, .88)], (.30, .28, "二段になる")),
        ("④ リバーストリガ", "送気に引き込まれて努力が起きる", PURPLE,
         [(0, .5), (.04, .90), (.20, .88), (.24, .5), (.30, .42), (.36, .5),
          (.50, .5), (.54, .90), (.70, .88), (.74, .5), (.80, .42), (.86, .5),
          (1.0, .5)], (.34, .26, "送気のあとに努力")),
        ("⑤ フローの飢餓", "吸気中に圧が凹む", ORANGE,
         [(0, .5), (.06, .46), (.10, .86), (.16, .70), (.22, .78), (.28, .86),
          (.32, .5), (.46, .5), (.52, .46), (.56, .86), (.62, .70), (.68, .78),
          (.74, .86), (.78, .5), (1.0, .5)], (.19, .56, "凹み")),
        ("⑥ サイクルの遅れ", "努力が終わっても吸気が続く", GREEN,
         [(0, .5), (.06, .46), (.10, .90), (.34, .88), (.38, .5), (.50, .5),
          (.56, .46), (.60, .90), (.84, .88), (.88, .5), (1.0, .5)],
         (.46, .30, "努力はここで終わっている")),
    )
    for i, (ttl, memo, col, pts, note) in enumerate(specs):
        r, c = divmod(i, cols)
        px = 56 + c * (bw + 40)
        py = y + 34 + r * 440
        cv.text(px, py - 72, ttl, size=15, weight="bold", color=col, ha="left")
        cv.text(px, py - 26, memo, size=12.5, color=GREY, ha="left")
        p = Panel(cv, px, py, bw, 200, "", color=col, base=.5)
        p.plot(pts, color=col)
        p.note(note[0], note[1], note[2], color=C_NOTE, size=11.5)
        textbox(cv, px, py + 230, bw, [{
            "① ミストリガ": "auto-PEEP を減らす／感度を上げる",
            "② オートトリガ": "回路の水・リークを直す／感度を下げる",
            "③ ダブルトリガ": "吸気時間・一回換気量を見直す",
            "④ リバーストリガ": "鎮静を見直す（足すとは限らない）",
            "⑤ フローの飢餓": "流量を上げる／圧規定へ変更",
            "⑥ サイクルの遅れ": "吸気時間を短く／サイクル％を上げる",
        }[ttl]], 12.5, style="grey", min_h=110)
    cv.save(path("f19_asynchrony.png"))


def f20():
    """予測体重は身長で決まる"""
    cv = Canvas(W, 1120)
    y = head(cv, "図20-1　一回換気量は「身長の関数」である",
             "体重が増えても肺は大きくならない。実測体重で計算すると過大換気になる。")
    bw = (W - 112 - 60) / 2
    textbox(cv, 56, y, bw, [
        "身長 165 cm・体重 60 kg",
        "実測体重で計算 → 予測体重で計算",
        "どちらで計算しても大きくは違わない",
    ], 14, style="blue", title="標準的な体格", title_size=16, min_h=230)
    textbox(cv, 56 + bw + 60, y, bw, [
        "身長 165 cm・体重 110 kg",
        "実測体重で計算すると、肺の大きさに対して",
        "明らかに過大な一回換気量になる",
    ], 14, style="red", title="肥満の患者", title_size=16, min_h=230)

    y2 = y + 230 + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "予測体重は性別と身長から計算する ── つまり、身長を測らないと決められない",
        "身長を 10 cm 高く見積もれば、一回換気量は 30 mL 以上大きくなる",
        "設定は 6 mL/kg のつもりでも、実際には 7 mL/kg を送ることになる",
    ], 14, style="amber", title="身長の誤差が、そのまま換気量の誤差になる", title_size=15)

    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "肺保護換気の第一歩は、メジャーを持つことである",
    ], 15, style="navy", min_h=110)
    cv.save(path("f20_pbw.png"))


def f23():
    """ABCDEF バンドル"""
    cv = Canvas(W, 1180)
    y = head(cv, "図23-1　ABCDEF バンドル",
             "人工呼吸器の設定と同じ重みで、毎日回すべき項目である。")
    bw = (W - 112 - 5 * 22) / 6
    items = (
        ("A", "痛みの評価と対応", ["まず鎮痛", "評価してから薬を選ぶ"], "red"),
        ("B", "覚醒試験と呼吸試験", ["SAT と SBT を組にする", "起こしてから試す"], "amber"),
        ("C", "鎮痛・鎮静薬の選択", ["最小限にとどめる", "深鎮静を既定値にしない"], "blue"),
        ("D", "せん妄の評価と対応", ["毎日評価する", "原因を探す"], "purple"),
        ("E", "早期離床", ["人工呼吸中から始める", "退院時の自立に効く"], "green"),
        ("F", "家族の参加", ["説明と参加", "回復の一部として扱う"], "navy"),
    )
    from figlib import boxrow
    hh = boxrow(cv, 56, y, bw, 22, [(letter, [ttl] + lines, st)
                                    for letter, ttl, lines, st in items],
                12.5, title_size=22, min_h=280, arrows=True, arrow_color=GREY,
                pad_x=10)
    y2 = y + hh + 50
    textbox(cv, 56, y2, W - 112, [
        "毎日の鎮静中断は人工呼吸期間と ICU 滞在を短くした（2000年）",
        "覚醒試験と自発呼吸試験を組にすると、一年後の生存まで改善した（2008年）",
        "バンドルの実施割合が高いほど、死亡・せん妄・身体拘束が減る（用量反応的な関連）",
    ], 14, style="navy", title="束で回すことの意味", title_size=15)
    cv.save(path("f23_abcdef.png"))


def f25():
    """EIT の見え方"""
    cv = Canvas(W, 1180)
    y = head(cv, "図25-1　電気インピーダンス断層撮影（EIT）の見え方",
             "胸に巻いた電極帯から、換気が肺のどこに分布しているかを連続で描く。")
    bw = (W - 112 - 2 * 40) / 3
    labels = ("PEEP が低い", "適切な PEEP", "PEEP が高すぎる")
    dist = ((0.15, 0.30, 0.55), (0.30, 0.38, 0.32), (0.52, 0.30, 0.18))
    memo = ("背側がつぶれ、換気が腹側に偏る",
            "腹側と背側に均等に分布する",
            "腹側が過膨張し、換気がまた偏る")
    for i, (lab, d, m) in enumerate(zip(labels, dist, memo)):
        x = 56 + i * (bw + 40)
        cv.text(x + bw / 2, y - 30, lab, size=15.5, weight="bold",
                color=(C_NOTE if i != 1 else GREEN))
        # 胸部断面の模式（上＝腹側、下＝背側）
        cv.rect(x, y, bw, 300, fc="#fbfcfd", ec="#c9d2dc", lw=1.2)
        band = 300 / 3.0
        for k, frac in enumerate(d):
            g = 1.0 - min(frac / 0.6, 1.0) * 0.72
            cv.rect(x + 40, y + 16 + k * band, bw - 80, band - 14,
                    fc=(g * 0.55 + 0.30, g * 0.72 + 0.22, 1.0 * g * 0.55 + 0.42),
                    ec="#c9d2dc", lw=1.0)
            cv.text(x + bw / 2, y + 16 + k * band + (band - 14) / 2,
                    ["腹側", "中間", "背側"][k], size=12.5,
                    color=(INK if frac < 0.45 else "#ffffff"))
        textbox(cv, x, y + 330, bw, [m], 13, style="grey", min_h=130)
    y2 = y + 330 + 130 + 50
    textbox(cv, 56, y2, W - 112, [
        "放射線を使わないので、ベッドサイドで連続して見られる",
        "PEEP を変えた瞬間に、どこが開き、どこが過膨張するかが分かる",
        "用語と使い方には国際的な合意文書があるが、"
        "EIT で設定を決めた群の予後が改善したという大規模試験はまだない",
    ], 14, style="navy", title="EIT にできること・まだできないこと", title_size=15)
    cv.save(path("f25_eit.png"))


if __name__ == "__main__":
    for fn in (f13, f14, f15, f16, f17, f18, f19, f20, f23, f25):
        fn()
        print("ok:", fn.__name__)
