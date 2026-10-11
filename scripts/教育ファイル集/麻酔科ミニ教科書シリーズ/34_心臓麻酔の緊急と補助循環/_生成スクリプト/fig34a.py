# -*- coding: utf-8 -*-
"""㉞ 図版 その1（図1-1 〜 図6-1）"""
from fig34common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f01():
    cv = Canvas(W, 1180)
    y = head(cv, "図1-1　A 型解離では、三つの時計が同時に走っている",
             "麻酔科が短くできるのは三番目だけ。だからこそ、"
             "省いてよい準備と省けない準備を先に決めておく。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 破裂・タンポナーデ", "red",
         ["心嚢内への出血", "進行すると充満できなくなる",
          "止められるのは手術だけ"]),
        ("② 灌流障害による臓器傷害", "amber",
         ["脳・冠・腸管・腎・下肢", "虚血の時間が転帰を決める",
          "血圧を下げると顕在化する"]),
        ("③ 手術開始までの準備", "blue",
         ["搬送・診断・入室", "モニタ・ライン・輸血の確保",
          "麻酔科が短くできるのはここ"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13.5,
                          style=st, title=ttl, title_size=15.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "省けない ── 解離の及んでいない側の動脈圧ライン、輸血の確保、",
        "　　　　　　執刀できる状態（消毒・ドレープ・人工心肺の準備）",
        "省いてよい ── 破綻が差し迫っているときの、追加の穿刺や検査",
    ], 14, style="navy", title="準備の時計を短くするために", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "三つの時計は独立していない ── 血圧を下げれば②が進み、"
        "下げなければ①が進む",
        "だから「目標血圧」は一つに決まらない（第2章）",
    ], 14, style="red", min_h=130)
    cv.save(path("f01_dissection_clock.png"))


def f02():
    cv = Canvas(W, 1180)
    y = head(cv, "図2-1　導入時の綱引き ── 下げたい理由と、下げられない理由",
             "この綱引きは解けない。幅の中で動かし、根拠を術者と共有する。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "大動脈壁にかかる剪断応力を下げる",
        "血圧・心拍数・立ち上がりの速さ",
        "",
        "喉頭鏡・挿管で血圧が跳ねる",
        "→ 鎮痛を先に十分に",
    ], 14, style="blue", title="下げたい（破裂を遅らせる）", title_size=16.5,
        min_h=290)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "灌流障害 ── 脳・腎・腸管の灌流が閾値を割る",
        "タンポナーデ ── 前負荷・心拍数・交感神経緊張",
        "　に依存して拍出が保たれている",
        "",
        "急性 AR ── 徐脈で逆流が増える",
    ], 14, style="red", title="下げられない（灌流が破綻する）",
        title_size=16.5, min_h=290)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "薬はゆっくり、少量ずつ ── 効果を見てから足す",
        "動脈圧ラインは解離の及んでいない側で。左右差を必ず測る",
        "輸血・昇圧薬・執刀の準備が整ってから導入する",
    ], 14, style="navy", title="どちらに転んでも耐えられる導入にする",
        title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "実務の要点 ── 「執刀できる状態になってから導入する」。"
        "消毒・ドレープが済み、術者が手を置いた状態で導入すれば、"
        "破綻したときに打つ手が残る。",
    ], 14.5, style="amber", min_h=130)
    cv.save(path("f02_induction.png"))


def f03():
    cv = Canvas(W, 1300)
    y = head(cv, "図4-1　灌流障害の五つの領域と、麻酔科が気づける徴候",
             "いずれも「血圧を下げた直後」に顕在化することがある。")
    bw = (W - 112 - 4 * 22) / 5
    cols = (
        ("脳", "purple", ["意識障害", "瞳孔不同", "NIRS の左右差"]),
        ("冠動脈", "red", ["ST 変化", "壁運動異常", "急性 AR との合併"]),
        ("腸管", "amber", ["乳酸の上昇", "腹部膨満", "所見が乏しいことも"]),
        ("腎", "blue", ["尿量低下", "単独では判断しない", "経時変化で見る"]),
        ("下肢・脊髄", "green", ["脈の消失", "血圧の左右差", "対麻痺（㉜）"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 22), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=15, min_h=230))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "血圧を下げる ── 剪断応力は下がるが、閾値ぎりぎりの臓器は虚血に落ちる",
        "血圧を保つ ── 臓器は灌流されるが、破裂までの時間が短くなる",
        "だから「下げてみて、何が起きるかを見る」しかない。",
        "そのために、見る指標（意識・NIRS・乳酸・尿量・脈）を先に決めておく",
    ], 14, style="navy", title="原則と要請の衝突", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "灌流障害は、解離の分枝への進展でも、フラップによる入口の閉塞でも起こる",
        "どの機序かで、手術で解決するか、追加の処置が要るかが変わる",
        "麻酔科は「気づいて伝える」ところまでを持ち場とする",
    ], 13.5, style="grey", min_h=150)
    cv.save(path("f03_malperfusion.png"))


def f04():
    cv = Canvas(W, 1380)
    y = head(cv, "図6-1　心臓手術後の心停止 ── 最初にすることが違う",
             "通常の蘇生手順をそのまま当てはめない。"
             "除細動とペーシングが先に来て、緊急再開胸が手順に入る。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 230, "", color=INK)
    cv.text(x - 14, y + 115, "時間", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.13, "0 秒", "リズムを見る", BLUE),
             (0.36, "ただちに", "除細動（三回まで）\nまたはペーシング", RED),
             (0.62, "並行して", "可逆的原因を探す", ORANGE),
             (0.87, "数分以内", "緊急再開胸", PURPLE))
    for t, when, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.76, when, color=col, size=12.5)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.42 - j * 0.16, ln, color=col, size=13)
    y2 = y + 230 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "胸骨圧迫は吻合部・移植片・人工弁を損傷しうる",
        "→ 開始のタイミングと適応が通常と異なる",
        "除細動可能なリズムなら、圧迫より先に除細動する",
    ], 14, style="red", title="胸骨圧迫の扱いが違う理由", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "再開胸セットの置き場所を全員が知っている",
        "誰が開けるか、誰を呼ぶかが決まっている",
        "ペーシング電極の有無が入室時に確認されている",
        "訓練されている ── 手順書があるだけでは動けない",
    ], 14, style="navy", title="この手順が成り立つ四つの条件", title_size=16)
    cv.save(path("f04_arrest.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04):
        fn()
        print("ok:", fn.__name__)
