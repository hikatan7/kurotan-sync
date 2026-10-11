# -*- coding: utf-8 -*-
"""㉚ 図版 第I部・第II部（図1-1 〜 図11-1）"""
from fig30common import (W, Canvas, Panel, LH, head, path, legend, steps,
                         decay, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                         ORANGE, PURPLE, C_PRES, C_FLOW, C_VOL, C_NOTE)


def f01():
    """自発呼吸と陽圧換気 ── 圧の向き"""
    cv = Canvas(W, 1120)
    y = head(cv, "図1-1　圧の向きが逆になる",
             "肺がふくらむ結果は同じでも、胸腔内圧の符号が逆になる。"
             "静脈還流と後負荷への影響はここから派生する。")
    bw = (W - 56 * 2 - 60) / 2
    for i, (title, style, arrow_dir, lines) in enumerate((
        ("自発呼吸（陰圧）", "blue", -1,
         ["横隔膜が下がる", "胸腔内圧　↓（陰圧）", "肺胞内圧　↓",
          "大気との差で空気が入る"]),
        ("陽圧換気（陽圧）", "red", 1,
         ["機械が気道の圧を上げる", "肺胞内圧　↑", "胸腔内圧　↑",
          "圧較差で空気が押し込まれる"]),
    )):
        x = 56 + i * (bw + 60)
        cv.box(x, y, bw, 470, style=style, lw=1.8)
        cv.text(x + bw / 2, y + 42, title, size=16, weight="bold",
                color=(BLUE if i == 0 else RED))
        # 胸郭の模式（枠と横隔膜）
        cx = x + bw / 2
        cv.rect(cx - 150, y + 82, 300, 130, fc="#ffffff", ec="#8d97a3", lw=1.6)
        dy = y + 212 + (18 if i == 0 else -6)
        cv.ax.plot([cx - 150, cx - 60, cx + 60, cx + 150],
                   [y + 206, dy, dy, y + 206], color="#8d97a3", lw=3.0, zorder=4)
        cv.arrow((cx, y + 100), (cx, y + 100 + 60 * (1 if i == 0 else -1)),
                 color=(BLUE if i == 0 else RED), lw=3.0, head=16)
        cv.text(cx + 200, y + 206, "横隔膜", size=11.5, color=GREY)
        yy = y + 262
        for ln in lines:
            cv.text(cx, yy, ln, size=13, color=INK)
            yy += LH(13, 1.25)

    y2 = y + 470 + 46
    h = textbox(cv, 56, y2, W - 112, [
        "胸腔内圧が上がる → 右房への静脈還流は減る（前負荷↓）／左室の後負荷は下がる",
        "循環血液量が少ない患者では前者が前面に出て血圧が落ちる",
        "心不全の患者では後者が助けになる ── 同じ操作が毒にも薬にもなる",
    ], 14, style="navy", title="陽圧がもたらす二つの結果", title_size=15)
    cv.save(path("f01_pressure_direction.png"))


def f02():
    """一回の呼吸の四つの局面"""
    cv = Canvas(W, 1120)
    y = head(cv, "図2-1　一回の呼吸を四つの局面で読む",
             "モードの違いは、この四つのどこを機械が決め、どこを患者に委ねるかの違いである。")
    p = Panel(cv, 150, y, W - 150 - 320, 250, "気道内圧", color=C_PRES)
    pts = [(0.00, 0.10), (0.05, 0.08), (0.08, 0.72), (0.34, 0.76),
           (0.37, 0.10), (0.50, 0.10), (0.55, 0.08), (0.58, 0.72),
           (0.84, 0.76), (0.87, 0.10), (1.00, 0.10)]
    p.plot(pts, color=C_PRES)
    p.hline(0.10, color="#9aa6b4")
    p.label_left(0.10, "PEEP")
    for t, s, col in ((0.065, "①トリガ", ORANGE), (0.21, "②リミット", BLUE),
                      (0.365, "③サイクル", GREEN)):
        p.vline(t, color=col, lw=1.6)
        p.note(t, 0.88, s, color=col, size=13)
    p.note(0.045, 0.30, "④PEEP", color=PURPLE, size=13, ha="left")

    y2 = y + 250 + 46
    bw = (W - 112 - 3 * 26) / 4
    for i, (t, ttl, lines, st) in enumerate((
        (ORANGE, "①トリガ", ["誰が吸気を始めるか", "時間／患者（圧・フロー）"], "amber"),
        (BLUE, "②リミット", ["吸気中に何を守るか", "圧か、量か"], "blue"),
        (GREEN, "③サイクル", ["何が吸気を終わらせるか", "量／時間／流量(%)"], "green"),
        (PURPLE, "④PEEP", ["呼気の終わりの圧", "吸気の決め方とは独立"], "purple"),
    )):
        textbox(cv, 56 + i * (bw + 26), y2, bw, lines, 13.5, style=st,
                title=ttl, title_size=15, min_h=150)

    y3 = y2 + 150 + 40
    textbox(cv, 56, y3, W - 112, [
        "A/C（補助／調節換気）＝トリガは患者にも機械にも、リミットとサイクルは機械",
        "PSV（圧支持換気）＝トリガもサイクルも患者、リミットだけが機械の圧",
        "SIMV ＝決められた回数だけ機械が握り、それ以外はサイクルを患者に返す",
    ], 14, style="grey", title="四つの言葉でモードを言い換える", title_size=15)
    cv.save(path("f02_four_phases.png"))


def f03():
    """VCV と PCV の波形比較"""
    cv = Canvas(W, 1200)
    y = head(cv, "図3-1　量を決めるか、圧を決めるか",
             "片方を設定すれば、もう片方は肺が決める。どちらを「見張る値」にするかの選択である。")
    bw = (W - 56 * 2 - 70) / 2
    for i, (ttl, col) in enumerate((("量規定換気（VCV）", BLUE),
                                    ("圧規定換気（PCV）", GREEN))):
        x = 56 + i * (bw + 70)
        cv.text(x + bw / 2, y - 32, ttl, size=16, weight="bold", color=col)
        yy = y + 46
        p1 = Panel(cv, x + 110, yy, bw - 130, 180, "圧", color=C_PRES)
        p2 = Panel(cv, x + 110, yy + 246, bw - 130, 180, "流量", color=C_FLOW)
        if i == 0:
            p1.plot([(0, .12), (.06, .10), (.10, .40), (.45, .86), (.48, .12),
                     (.62, .12), (.66, .10), (.70, .40), (1.0, .80)], color=C_PRES)
            p2.plot([(0, .5), (.08, .5), (.10, .85), (.46, .85), (.48, .16),
                     (.60, .5), (.62, .5), (.68, .85), (1.0, .85)], color=C_FLOW)
            p1.caption("圧は肺が決める（変動する）", color=C_NOTE)
            p2.caption("流量は設定どおり（矩形）")
        else:
            p1.plot([(0, .12), (.06, .10), (.09, .78), (.46, .78), (.49, .12),
                     (.62, .12), (.66, .10), (.69, .78), (1.0, .78)], color=C_PRES)
            p2.plot(decay(.09, .46, .92, .52) + [(.48, .14)] +
                    decay(.69, 1.0, .92, .62), color=C_FLOW)
            p1.caption("圧は設定どおり（一定）")
            p2.caption("流量は漸減波になる")
    y4 = y + 46 + 246 + 180 + 46
    bw2 = (W - 112 - 40) / 2
    textbox(cv, 56, y4, bw2, [
        "量は保証され、圧は保証されない",
        "肺が硬くなれば気道内圧が上がる",
        "見張るのは上限圧アラーム",
    ], 14, style="blue", title="VCV を選んだとき", title_size=15, min_h=190)
    textbox(cv, 56 + bw2 + 40, y4, bw2, [
        "圧は保証され、量は保証されない",
        "肺が硬くなれば一回換気量が減る",
        "見張るのは分時換気量の下限アラーム",
    ], 14, style="green", title="PCV を選んだとき", title_size=15, min_h=190)
    cv.save(path("f03_vcv_pcv_waveform.png"))


def f04():
    """二つのつまみ"""
    cv = Canvas(W, 1100)
    y = head(cv, "図4-1　換気と酸素化は別々のつまみ",
             "PaCO₂ と PaO₂ は別の回路でつながっている。触るつまみを間違えると効かない。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "一回換気量　×　換気回数",
        "＝ 分時換気量",
        "そのうち肺胞に届いた分だけが効く",
    ], 15, style="blue", title="PaCO₂ を動かすつまみ", title_size=16, min_h=210)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "FiO₂（吸入酸素濃度）",
        "平均気道内圧（主に PEEP）",
        "＝ 使える肺胞をどれだけ開くか",
    ], 15, style="green", title="PaO₂ を動かすつまみ", title_size=16, min_h=210)

    y2 = y + max(h1, h2, 210) + 44
    cv.arrow((56 + bw / 2, y2 - 32), (56 + bw / 2, y2 + 4), color=BLUE, lw=2.4)
    cv.arrow((56 + bw + 60 + bw / 2, y2 - 32),
             (56 + bw + 60 + bw / 2, y2 + 4), color=GREEN, lw=2.4)
    textbox(cv, 56, y2 + 8, bw, [
        "死腔が増えると効かなくなる",
        "・浅く速い呼吸",
        "・過膨張（auto-PEEP）",
        "・肺塞栓、回路の死腔",
    ], 13.5, style="amber", title="効かないときに疑うもの", title_size=14.5, min_h=210)
    textbox(cv, 56 + bw + 60, y2 + 8, bw, [
        "シャントが増えると効かなくなる",
        "・無気肺、肺炎、肺水腫",
        "・FiO₂ を上げても反応しない",
        "・反応しないこと自体が所見になる",
    ], 13.5, style="amber", title="効かないときに疑うもの", title_size=14.5, min_h=210)
    cv.save(path("f04_two_knobs.png"))


def f05():
    """VCV の波形と吸気ポーズ"""
    cv = Canvas(W, 1400)
    y = head(cv, "図5-1　量規定換気の波形",
             "流量は設定どおりに出る。圧は肺の硬さに応じて受動的に決まるので、圧波形が情報になる。")
    x = 170
    w = W - x - 90
    p1 = Panel(cv, x, y, w, 210, "圧", color=C_PRES)
    p1.plot([(0, .12), (.06, .10), (.09, .40), (.42, .84), (.45, .12),
             (.60, .12), (.64, .10), (.67, .40), (1.0, .84)], color=C_PRES)
    p1.hline(0.12, color="#9aa6b4")
    p1.label_left(0.12, "PEEP")
    p1.caption("肺が硬いほど、この傾きが急になる", color=C_NOTE)

    p2 = Panel(cv, x, y + 276, w, 210, "流量", color=C_FLOW, base=0.5)
    p2.plot([(0, .5), (.08, .5), (.09, .86), (.43, .86), (.45, .14),
             (.56, .48), (.60, .5), (.64, .5), (.66, .86), (1.0, .86)],
            color=C_FLOW)
    p2.caption("矩形波（設定流量で一定）")
    p2.note(.52, .12, "呼気は受動的", color=GREY, size=12.5)

    p3 = Panel(cv, x, y + 552, w, 190, "量", color=C_VOL)
    p3.plot([(0, .06), (.09, .06), (.43, .84), (.56, .08), (.66, .06),
             (1.0, .86)], color=C_VOL)
    p3.caption("一回換気量は毎回同じ")

    y2 = y + 552 + 190 + 42
    textbox(cv, 56, y2, W - 112, [
        "吸気の終わりに息を止める（吸気ポーズ）と流れが止まり、抵抗成分が消える",
        "→ 残った圧がプラトー圧。ピーク圧との差が抵抗、PEEP との差が駆動圧（第14章）",
        "強い吸気努力に設定流量が追いつかないと、吸気中の圧波形が凹む（フローの飢餓）",
    ], 14, style="navy", title="VCV だからできること・起きること", title_size=15)
    cv.save(path("f05_vcv_detail.png"))


def f06():
    """PCV とコンプライアンス低下"""
    cv = Canvas(W, 1400)
    y = head(cv, "図6-1　圧規定換気と、コンプライアンスが落ちたとき",
             "圧は設定どおりに保たれ、一回換気量のほうが静かに減る。")
    x = 170
    w = W - x - 90
    p1 = Panel(cv, x, y, w, 210, "圧", color=C_PRES)
    p1.plot([(0, .12), (.05, .10), (.08, .78), (.44, .78), (.47, .12),
             (.58, .12), (.62, .10), (.65, .78), (1.0, .78)], color=C_PRES)
    p1.caption("設定圧のまま変わらない")

    p2 = Panel(cv, x, y + 276, w, 210, "流量", color=C_FLOW, base=0.5)
    p2.plot(decay(.08, .44, .92, .54) + [(.46, .14)] + decay(.46, .57, .14, .48) +
            [(.62, .5)] + decay(.65, 1.0, .92, .66), color=C_FLOW)
    p2.note(.22, .86, "漸減波", color=GREY, size=12.5)
    p2.caption("硬くなると早く落ちる", color=C_NOTE)

    p3 = Panel(cv, x, y + 552, w, 200, "量", color=C_VOL)
    p3.plot([(0, .06), (.08, .06), (.44, .82), (.57, .08), (.65, .06),
             (1.0, .52)], color=C_VOL)
    p3.hline(.82, color="#c9d2dc", t0=.44, t1=1.0)
    p3.note(.82, .70, "一回換気量が減っている", color=C_NOTE, size=13)
    cv.arrow((p3.px(.98), p3.py(.82)), (p3.px(.98), p3.py(.54)),
             color=C_NOTE, lw=2.2, head=13)

    y2 = y + 552 + 200 + 40
    textbox(cv, 56, y2, W - 112, [
        "気づく手立ては、分時換気量の下限アラームだけである",
        "気管支攣縮・分泌物・腹圧上昇・患者が力んだとき、いずれも同じ形で現れる",
        "リークがあっても設定圧まで流量を出し続けるので、換気は破綻しにくい",
    ], 14, style="red", title="換気量が保証されないということ", title_size=15)
    cv.save(path("f06_pcv_detail.png"))


def f07():
    """二重制御の制御ループ"""
    cv = Canvas(W, 1060)
    y = head(cv, "図7-1　二重制御（PRVC／AutoFlow など）の動き",
             "一呼吸ごとに吸気圧を調整する。吸気の途中で切り替わるわけではない。")
    x = 170
    w = W - x - 90
    p1 = Panel(cv, x, y, w, 230, "気道内圧", color=C_PRES)
    hs = (.74, .70, .64, .58, .66)
    for i, hgt in enumerate(hs):
        t0 = i * 0.2
        p1.plot([(t0 + .01, .10), (t0 + .03, hgt), (t0 + .14, hgt),
                 (t0 + .16, .10), (t0 + .19, .10)], color=C_PRES)
        p1.note(t0 + .085, hgt - .12, "%d" % (i + 1), color=GREY, size=12)
    p1.caption("努力が強まると支持が下がっていく", color=C_NOTE)

    y2 = y + 230 + 46
    bw = (W - 112 - 3 * 34) / 4
    from figlib import boxrow
    hh = boxrow(cv, 56, y2, bw, 34, [
        ("① 送る", ["設定した吸気圧で", "圧規定の一呼吸を送る"], "blue"),
        ("② 測る", ["得られた一回換気量を", "呼気側で測る"], "grey"),
        ("③ 比べる", ["目標一回換気量と", "比較する"], "grey"),
        ("④ 直す", ["足りなければ次の圧を上げ", "多ければ下げる"], "green"),
    ], 13.5, title_size=15, min_h=150, arrows=True, arrow_color=GREY)
    y3 = y2 + hh + 40
    textbox(cv, 56, y3, W - 112, [
        "患者の努力が強い → 換気量が目標を超える → 機械は支持を下げる（支援が引き算される）",
        "コンプライアンスが落ちた → 吸気圧が自動で上がる（悪化が画面の上で相殺される）",
        "自動で帳尻を合わせる機能は、悪化を隠す機能でもある",
    ], 14, style="amber", title="二重制御の二つの落とし穴", title_size=15)
    cv.save(path("f07_dual_control.png"))


def f08():
    """PSV の一呼吸"""
    cv = Canvas(W, 1120)
    y = head(cv, "図8-1　圧支持換気の一呼吸",
             "トリガもサイクルも患者が決める。機械が決めているのは支持圧だけである。")
    x = 170
    w = W - x - 110
    p1 = Panel(cv, x, y, w, 240, "圧", color=C_PRES)
    p1.plot([(0, .16), (.10, .16), (.13, .09), (.16, .74), (.52, .74),
             (.56, .16), (.75, .16), (.78, .09), (.81, .74), (1.0, .74)],
            color=C_PRES)
    p1.hline(.16, color="#9aa6b4")
    p1.label_left(.16, "PEEP")
    p1.vline(.135, color=ORANGE, lw=1.6)
    p1.vline(.54, color=GREEN, lw=1.6)
    p1.toplabel(.135, "①患者がトリガ", color=ORANGE)
    p1.toplabel(.34, "②③設定圧で支える", color=BLUE)
    p1.toplabel(.62, "④フローサイクル", color=GREEN)
    p1.note(.135, .32, "努力による圧の落ち込み", color=C_NOTE, size=12, ha="left")

    p2 = Panel(cv, x, y + 306, w, 240, "流量", color=C_FLOW, base=0.46)
    p2.plot([(0, .46), (.13, .46), (.15, .42)] + decay(.16, .54, .90, .50) +
            [(.56, .12)] + decay(.56, .74, .12, .44) +
            [(.78, .46), (.80, .42)] + decay(.81, 1.0, .90, .58), color=C_FLOW)
    p2.hline(.66, color="#c9d2dc", t0=.16, t1=.60)
    p2.caption("ピーク流量の 25％ 前後まで落ちたら呼気へ")

    y2 = y + 306 + 240 + 42
    bw = (W - 112 - 40) / 2
    textbox(cv, 56, y2, bw, [
        "呼気に時間が要る（閉塞性）",
        "→ サイクル％を高めにして吸気を早く切り上げる",
    ], 14, style="amber", title="フローサイクル％を上げる場面", title_size=15, min_h=170)
    textbox(cv, 56 + bw + 40, y2, bw, [
        "吸気が足りない（拘束性）",
        "→ サイクル％を低めにして吸気を長くとる",
    ], 14, style="blue", title="フローサイクル％を下げる場面", title_size=15, min_h=170)
    cv.save(path("f08_psv_cycle.png"))


def f09():
    """SIMV のタイムライン"""
    cv = Canvas(W, 1040)
    y = head(cv, "図9-1　SIMV のタイムライン",
             "強制換気の窓に患者の努力があれば同期して送り、なければ時間で送る。")
    x = 150
    w = W - x - 90
    p = Panel(cv, x, y, w, 260, "気道内圧", color=C_PRES)
    # 強制換気（大きい山）と自発呼吸（小さい山）
    p.plot([(0, .14), (.03, .12), (.06, .74), (.20, .74), (.23, .14),
            (.30, .14), (.32, .12), (.34, .30), (.40, .30), (.42, .14),
            (.47, .14), (.49, .12), (.51, .28), (.57, .28), (.59, .14),
            (.64, .14), (.66, .12), (.69, .74), (.83, .74), (.86, .14),
            (.93, .14), (.95, .12), (.97, .30), (1.0, .30)], color=C_PRES)
    for t in (.06, .69):
        cv.ax.plot([p.px(t - .05), p.px(t - .05)], [p.y + 6, p.y + p.h - 6],
                   color=ORANGE, lw=1.4, linestyle=(0, (4, 4)), zorder=3)
    p.note(.19, .86, "強制換気（機械が量／圧）", color=BLUE, size=12.5)
    p.note(.60, .86, "自発呼吸（圧支持がなければ素のまま）", color=GREEN, size=12.5)
    p.note(.02, .52, "同期の窓", color=ORANGE, size=11.5, ha="left")

    y2 = y + 260 + 44
    bw = (W - 112 - 40) / 2
    textbox(cv, 56, y2, bw, [
        "機械の呼吸と患者の呼吸がぶつかりにくい",
        "自発呼吸を残せる",
    ], 14, style="green", title="SIMV が解決したこと", title_size=15, min_h=190)
    textbox(cv, 56 + bw + 40, y2, bw, [
        "呼吸ごとに仕事量が変動する",
        "回数の漸減による離脱は、自発呼吸試験に劣った（1995年）",
    ], 14, style="red", title="SIMV が残したこと", title_size=15, min_h=190)
    cv.save(path("f09_simv_timeline.png"))


def f10():
    """APRV の圧波形"""
    cv = Canvas(W, 1320)
    y = head(cv, "図10-1　APRV の圧波形",
             "高い圧を長く保ち、短時間だけ開放する。開放時間は呼気流量が"
             "基線に戻る前に打ち切るので、内因性 PEEP が意図的に残る。")
    x = 170
    w = W - x - 90
    p1 = Panel(cv, x, y, w, 250, "気道内圧", color=C_PRES)
    seq = []
    for i in range(3):
        t0 = i * .33
        seq += [(t0, .20), (t0 + .01, .72), (t0 + .10, .74), (t0 + .13, .73),
                (t0 + .16, .72), (t0 + .25, .73), (t0 + .27, .20),
                (t0 + .31, .20), (t0 + .32, .72)]
    p1.plot(seq[:-1], color=C_PRES)
    p1.hline(.72, color="#c9d2dc", t0=0, t1=.30)
    p1.hline(.20, color="#c9d2dc", t0=0, t1=.30)
    p1.label_left(.72, "P-high")
    p1.label_left(.20, "P-low")
    p1.note(.13, .86, "T-high（長い）", color=GREY, size=12.5)
    p1.note(.32, .10, "T-low（短い）", color=C_NOTE, size=12, ha="left")
    p1.caption("自発呼吸は P-high の期間に重なる", color=GREEN)

    p2 = Panel(cv, x, y + 316, w, 210, "呼気流量", color=C_FLOW, base=0.72)
    ex = []
    for i in range(3):
        t0 = i * .33
        ex += [(t0 + .27, .72)] + decay(t0 + .27, t0 + .31, .10, .58, n=14) + \
              [(t0 + .31, .72)]
    p2.plot([(0, .72)] + ex, color=C_FLOW)
    p2.hline(.72, color="#9aa6b4")
    p2.note(.55, .34, "基線に戻る前に打ち切る＝内因性 PEEP を残す",
            color=C_NOTE, size=12.5)

    y2 = y + 316 + 210 + 42
    textbox(cv, 56, y2, W - 112, [
        "平均気道内圧が高く保たれるので酸素化に有利",
        "「吐ききらせない」ことが仕様 ── 閉塞性疾患とは相性が悪い",
        "気道内圧が穏やかでも、強い自発努力があれば経肺圧は大きく振れる（第16章）",
    ], 14, style="amber", title="APRV を使うときに意識すること", title_size=15)
    cv.save(path("f10_aprv.png"))


def f11():
    """比例補助の考え方"""
    cv = Canvas(W, 1080)
    y = head(cv, "図11-1　努力に比例させるという考え方",
             "NAVA は横隔膜の電気活動に、PAV＋ は患者が生み出した流量と量に比例して支援量を決める。")
    bw = (W - 112 - 56) / 2
    # 左：従来
    cv.text(56 + bw / 2, y - 26, "従来のモード（引き金として使う）", size=15.5,
            weight="bold", color=GREY)
    p1 = Panel(cv, 56 + 96, y + 60, bw - 110, 190, "支援", color=C_PRES)
    p1.plot([(0, .10), (.04, .70), (.30, .70), (.33, .10), (.40, .10),
             (.44, .70), (.70, .70), (.73, .10), (.80, .10), (.84, .70),
             (1.0, .70)], color=C_PRES)
    p2 = Panel(cv, 56 + 96, y + 316, bw - 110, 170, "患者の努力", color=GREY)
    p2.plot([(0, .10), (.05, .30), (.30, .30), (.33, .10), (.40, .10),
             (.45, .62), (.70, .62), (.73, .10), (.80, .10), (.85, .88),
             (1.0, .88)], color=GREY)
    p1.caption("努力が変わっても支援は同じ", color=C_NOTE)

    # 右：比例
    x2 = 56 + bw + 56
    cv.text(x2 + bw / 2, y - 26, "比例補助（NAVA／PAV＋）", size=15.5,
            weight="bold", color=PURPLE)
    p3 = Panel(cv, x2 + 96, y + 60, bw - 110, 190, "支援", color=PURPLE)
    p3.plot([(0, .10), (.05, .28), (.30, .28), (.33, .10), (.40, .10),
             (.45, .58), (.70, .58), (.73, .10), (.80, .10), (.85, .86),
             (1.0, .86)], color=PURPLE)
    p4 = Panel(cv, x2 + 96, y + 316, bw - 110, 170, "患者の努力（Edi ほか）",
               color=GREY)
    p4.plot([(0, .10), (.05, .30), (.30, .30), (.33, .10), (.40, .10),
             (.45, .62), (.70, .62), (.73, .10), (.80, .10), (.85, .88),
             (1.0, .88)], color=GREY)
    p3.caption("努力の大きさに比例して支援が動く", color=PURPLE)

    y2 = y + 316 + 170 + 60
    bw2 = (W - 112 - 40) / 2
    textbox(cv, 56, y2, bw2, [
        "食道の電極で横隔膜の電気活動を拾う",
        "トリガの遅れが小さく、リークに強い",
        "Edi は「どれくらい頑張っているか」の指標にもなる",
    ], 13.5, style="purple", title="NAVA", title_size=15, min_h=200)
    textbox(cv, 56 + bw2 + 40, y2, bw2, [
        "回路側で呼吸力学を測り、仕事の一定割合を肩代わりする",
        "電極は不要だが、リークがあると推定が狂う",
    ], 13.5, style="blue", title="PAV＋", title_size=15, min_h=200)
    cv.save(path("f11_proportional.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11):
        fn()
        print("ok:", fn.__name__)
