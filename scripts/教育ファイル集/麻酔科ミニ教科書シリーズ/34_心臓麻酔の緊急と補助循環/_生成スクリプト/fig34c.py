# -*- coding: utf-8 -*-
"""㉞ 図版 その3（図19-1 〜 図22-1）"""
from fig34common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f10():
    cv = Canvas(W, 1340)
    y = head(cv, "図19-1　人工心肺から離脱できないとき、原因を六つに分ける",
             "薬を足す前に分ける。TEE がいちばん速く答える場面である。")
    bw = (W - 112 - 2 * 30) / 3
    row1 = (
        ("① 収縮の低下", "red", ["左室の動きが悪い",
                                 "強心薬、虚血の検索"]),
        ("② 前負荷の不足", "blue", ["心室が小さい",
                                    "輸液"]),
        ("③ 後負荷の問題", "green", ["開いている／締まりすぎ",
                                     "血管作動薬"]),
    )
    row2 = (
        ("④ リズム", "purple", ["同期していない、細動",
                                "ペーシング、除細動"]),
        ("⑤ 右心不全", "amber", ["右室が拡大、中隔が押される",
                                 "後負荷↓、体血圧を保つ（㉝）"]),
        ("⑥ 外科的問題", "navy", ["壁運動異常、弁、流出路狭窄",
                                  "術者に戻す"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(row1):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13,
                          style=st, title=ttl, title_size=15.5, min_h=200))
    y2 = y + max(hs) + 40
    hs2 = []
    for i, (ttl, st, lines) in enumerate(row2):
        hs2.append(textbox(cv, 56 + i * (bw + 30), y2, bw, lines, 13,
                           style=st, title=ttl, title_size=15.5, min_h=200))
    y3 = y2 + max(hs2) + 52
    h3 = textbox(cv, 56, y3, W - 112, [
        "体温・電解質・酸塩基・ヘマトクリット ── "
        "これらが崩れていれば、どの薬も本来の効果を出さない",
        "SAM のように、強心薬が病態を悪化させる場合もある（㉝第8章）",
    ], 14, style="navy", title="分ける前に、土台を確かめる", title_size=16)
    y4 = y3 + h3 + 46
    textbox(cv, 56, y4, W - 112, [
        "六つに分けても離脱できなければ、補助循環が選択肢になる（第20章）。"
        "そのときは「何を足したいのか」を先に言葉にする。",
    ], 14, style="amber", min_h=130)
    cv.save(path("f10_failed_weaning.png"))


def f11():
    cv = Canvas(W, 1220)
    y = head(cv, "図21-1　補助循環は、入れる前に出口を決めておく",
             "難しいのは入れることではなく、止めること。"
             "装置が入ってから議論を始めると、選択肢が残っていない。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("何が回復すれば離脱できるか", "blue",
         ["心機能か", "肺か", "両方か"]),
        ("どのくらいの期間を見るか", "green",
         ["目安を決めておく", "延ばす判断も", "決めておく"]),
        ("回復しなかったら", "amber",
         ["長期補助", "移植", "あるいは中止"]),
        ("誰が、いつ、どう共有するか", "purple",
         ["診療科をまたぐ", "患者・家族を含む", "記録に残す"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14.5, min_h=240))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "装置が入ってから「どこまでやるか」を議論すると、"
        "選択肢が事実上なくなっていることがある。",
        "「出口を先に決める」のは、医学的な判断であると同時に、"
        "倫理的な準備でもある。",
    ], 14.5, style="navy", min_h=170)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "この会話は、患者と家族にも関わる ── 入れる前に始めておく",
    ], 14.5, style="red", min_h=110)
    cv.save(path("f11_exit.png"))


def f12():
    cv = Canvas(W, 1260)
    y = head(cv, "図22-1　心臓手術関連の急性腎障害",
             "単独で効く介入はない。"
             "決め手がないぶん、「決めた項目を全例で回す」ことが効く。")
    bw = (W - 112 - 4 * 20) / 5
    cols = (
        ("腎毒性を避ける", "red", ["薬剤を見直す", "減らす・止める"]),
        ("血行動態を保つ", "blue", ["低血圧の時間を短く", "（㉝第22章）"]),
        ("容量を過不足なく", "green", ["過剰輸液も", "腎を悪くする"]),
        ("血糖を管理する", "amber", ["高血糖を避ける", "低血糖も避ける"]),
        ("追いかける", "purple", ["尿量とクレアチニン", "決めた間隔で"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12,
                          style=st, title=ttl, title_size=13.5, min_h=210))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "バイオマーカーで高リスク患者を選び、KDIGO の推奨を束にして実行する"
        "戦略（PrevAKI）が、単施設と多施設で検証されている",
        "効果の大きさには議論がある ── しかし束そのものは、"
        "どの施設でも今日から実行できる",
    ], 14, style="navy", title="研究が示していること", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "麻酔科が持っているのは、灌流圧・容量・薬剤・輸血の四つ。",
        "どれも単独では決め手にならないが、どれも外すと悪くなる。",
    ], 14.5, style="amber", min_h=140)
    cv.save(path("f12_csa_aki.png"))


if __name__ == "__main__":
    for fn in (f10, f11, f12):
        fn()
        print("ok:", fn.__name__)
