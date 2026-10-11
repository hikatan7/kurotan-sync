# -*- coding: utf-8 -*-
"""㊳ 図版（図1-1 〜 図19-1）"""
from fig38common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f01():
    cv = Canvas(W, 1260)
    y = head(cv, "図1-1　産科麻酔が同時に見ているもの",
             "三つは多くの場面で同じ方向を向くが、食い違う場面もある。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 母体の安全", "blue", ["気道・呼吸・誤嚥", "血圧と出血",
                                  "痛みと不安"]),
        ("② 胎児の安全", "green", ["母体の血圧＝胎盤の灌流",
                                   "薬は胎盤を越える",
                                   "娩出までの時間"]),
        ("③ 分娩の進行", "amber", ["痛みを取ると変わるのか",
                                   "いつ始めるか",
                                   "器械分娩・帝王切開"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13,
                          style=st, title=ttl, title_size=15, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "母体の血圧を保つことは胎児の灌流を保つことでもあるが、"
        "母体に投与した薬は胎盤を越える",
        "母体の痛みを取ることは分娩の進行に影響しうるし、"
        "分娩を急ぐことは母体の負担を増やす",
        "この綱引きが、産科麻酔のほとんどの判断の背後にある",
    ], 13.5, style="navy", title="食い違うとき", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "産科麻酔はチームでしか成立しない ── "
        "産科医・助産師・新生児科と同じ言葉で話せることが前提になる。",
    ], 14.5, style="red", min_h=120)
    cv.save(path("f01_two_patients.png"))


def f02():
    cv = Canvas(W, 1260)
    y = head(cv, "図5-1　いつ始めるかをめぐる、二つの立場",
             "研究が示しているのは、開始の時期で"
             "帝王切開率と器械分娩率が変わらないということである。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "痛いときに取りたい",
        "",
        "「子宮口が何センチ」という条件は",
        "本人にとって意味を持たない",
        "",
        "待たされることが不信につながる",
    ], 14, style="blue", title="妊婦の立場", title_size=16.5, min_h=280)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "分娩の進行や出産方法が変わらないか",
        "",
        "早く始めると遅れるのではないか",
        "帝王切開が増えるのではないか",
        "",
        "自分たちの分娩の歴史がある",
    ], 14, style="amber", title="医療者の立場", title_size=16.5, min_h=280)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "早期に開始した場合と遅らせた場合を比較した系統的レビューでは、",
        "帝王切開率と器械分娩率に差が示されなかった",
        "つまり「痛みが出たときに始める」ことを妨げる根拠は乏しい",
    ], 14, style="navy", title="研究が示していること", title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "ただし「いつでも誰でも始めてよい」という意味ではない。"
        "前駆陣痛の段階で始めれば別の問題が生じる ── 判断は産科と共有する。",
    ], 14, style="grey", min_h=120)
    cv.save(path("f02_when_to_start.png"))


def f03():
    cv = Canvas(W, 1240)
    y = head(cv, "図6-1　「分娩が遅くなる」という議論の変化",
             "古い研究の結論を、そのまま当てはめられない。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "濃い局所麻酔薬",
        "　運動神経も遮断される",
        "　いきめない",
        "",
        "→ 分娩が遅れる",
        "→ 器械分娩が増える",
    ], 14, style="red", title="かつての方法", title_size=16.5, min_h=290)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "薄い局所麻酔薬＋オピオイド",
        "　運動神経は遮断しない",
        "　いきめる",
        "",
        "→ 第二期の長さに差が示されない",
        "→ 影響は小さくなった",
    ], 14, style="blue", title="現在の方法", title_size=16.5, min_h=290)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "第二期に局所麻酔薬を流し続ける群と偽薬に切り替える群を比較した",
        "無作為化試験で、第二期の長さに差が示されなかった",
    ], 14, style="navy", title="何が変わったのか", title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "産科・助産師との議論が噛み合わないとき、",
        "「どの時代の方法を前提にしているか」が原因であることがある。",
    ], 14.5, style="amber", min_h=140)
    cv.save(path("f03_labor_duration.png"))


def f04():
    cv = Canvas(W, 1260)
    y = head(cv, "図10-1　全身麻酔を避ける三つの理由",
             "この三つが重なるのは、妊婦に特有の状況である。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 気道", "red", ["浮腫と血管の怒張", "乳房の増大で",
                           "喉頭鏡の操作が制限される"]),
        ("② 呼吸", "amber", ["機能的残気量が小さい", "酸素消費が増えている",
                             "無呼吸で急速に低酸素"]),
        ("③ 誤嚥", "purple", ["胃内容が停滞している", "括約筋の緊張が下がる",
                              "腹腔内圧も上がっている"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13,
                          style=st, title=ttl, title_size=15.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "時間がない（母体または胎児が切迫している）",
        "脊髄幹麻酔が禁忌 ── 凝固障害、感染、循環の破綻",
        "脊髄幹麻酔が失敗した、あるいは範囲が足りない",
        "大量出血が進行しており、意識と気道を確保したい",
    ], 14, style="navy", title="それでも全身麻酔を選ぶ場面", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "全身麻酔は「選ばない」のではなく、"
        "「必要なときに選べるよう準備しておく」もの（第13章）。",
    ], 14.5, style="red", min_h=120)
    cv.save(path("f04_why_neuraxial.png"))


def f05():
    cv = Canvas(W, 1280)
    y = head(cv, "図11-1　脊髄くも膜下麻酔後の血圧低下 ── 先回りする",
             "「下がってから追いかける」と、"
             "母体の嘔気と胎児の灌流の両方が悪くなる。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 240, "", color=INK)
    cv.text(x - 14, y + 120, "順番", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.13, "①", "子宮を左へ", BLUE),
             (0.38, "②", "輸液を同時に", GREEN),
             (0.63, "③", "昇圧薬を\n予防的に開始", RED),
             (0.88, "④", "目標に対して\n調整", PURPLE))
    for t, no, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, no, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12.5)
    y2 = y + 240 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "子宮を左へずらす ── 最初にやること。忘れられやすい",
        "輸液は先に入れるより、麻酔と同時に入れるほうが効く",
        "α作動薬は反射性の徐脈が起こりうる。"
        "ノルアドレナリンは心拍数が落ちにくい",
        "目標は「元の血圧の何割を下回らない」という形で決めておく",
    ], 13.5, style="navy", title="それぞれの考えどころ", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "血圧低下は最も頻度が高く、最も対処法がはっきりしている合併症である。",
        "「少し下がったくらいなら」と待たないこと。",
    ], 14.5, style="amber", min_h=140)
    cv.save(path("f05_hypotension.png"))


def f06():
    cv = Canvas(W, 1280)
    y = head(cv, "図13-1　産科の全身麻酔で決めておくこと",
             "選ぶときはたいてい急いでいる。"
             "手順が決まっていないと、そのまま事故になる。")
    bw = (W - 112 - 4 * 20) / 5
    cols = (
        ("① 前酸素化", "blue", ["時間をかける", "機能的残気量が小さい"]),
        ("② 薬と順番", "green", ["迅速導入", "施設で統一する"]),
        ("③ 入らなかったら", "amber", ["次の手を決めておく",
                                       "回数の上限も"]),
        ("④ 声門上器具と外科的気道", "red", ["どこで切り替えるか",
                                             "器材の場所"]),
        ("⑤ 起こすか進むか", "purple", ["誰が言い出すか",
                                        "産科と先に話す"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12,
                          style=st, title=ttl, title_size=13, min_h=210))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "産科の困難気道・挿管失敗については専門学会の診療指針がまとめられている",
        "ビデオ喉頭鏡と直接喉頭鏡を比較した系統的レビューもある",
        "誤嚥への備え ── 吸引、体位、そして起きたときの対応",
    ], 14, style="navy", title="拠りどころ", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「母体を起こす」という判断は産科の緊急度と衝突する。",
        "その衝突を、その場で初めて議論することにならないようにしておく。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f06_ga_airway.png"))


def f07():
    cv = Canvas(W, 1280)
    y = head(cv, "図17-1　妊娠が循環にかける負荷と、その山場",
             "分娩直後の自己輸血が、心疾患合併妊娠でいちばん危ない。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "時期", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.12, "妊娠中期〜", "循環血液量↑\n心拍出量↑", BLUE),
             (0.40, "妊娠後期", "体血管抵抗↓\n凝固能↑", GREEN),
             (0.65, "分娩中", "いきみと痛み\n→肺血管抵抗↑", ORANGE),
             (0.90, "分娩直後", "自己輸血\n→前負荷↑↑", RED))
    for t, when, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, when, color=col, size=13)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12.5)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "痛みといきみを抑えることは、そのまま心負荷を抑えることになる",
        "だから心疾患合併妊娠では、硬膜外鎮痛が治療として位置づけられる",
        "「快適さ」ではなく「循環の管理」である",
    ], 14, style="navy", title="無痛分娩がここで持つ意味", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "分娩様式・モニタ・抗凝固・呼べる人 ── これらは妊娠中に決める。",
        "陣痛が来てからでは間に合わない。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f07_cardiac_pregnancy.png"))


def f08():
    cv = Canvas(W, 1300)
    y = head(cv, "図19-1　無痛分娩を始めるときに決めること",
             "手技ではなく、この五つが体制の中身である。")
    bw = (W - 112 - 4 * 20) / 5
    cols = (
        ("① 誰が、いつ呼ばれるか", "blue", ["対応できる時間帯",
                                            "呼び出しの経路"]),
        ("② どこで導入し、管理するか", "green", ["分娩室・手術室・病室",
                                                "移動できるか"]),
        ("③ 誰が何を見張るか", "amber", ["項目と間隔",
                                         "連絡する閾値"]),
        ("④ 帝王切開への移行", "red", ["誰が判断するか",
                                      "どこまで待つか"]),
        ("⑤ うまくいかないとき", "purple", ["相談先",
                                            "合併症の追跡"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12,
                          style=st, title=ttl, title_size=12.5, min_h=210))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "硬膜外鎮痛を使う分娩と使わない分娩は、",
        "診察の頻度も、誘発の考え方も、器械分娩の閾値も違ってくる",
        "そこを共有しないまま麻酔だけを始めると、摩擦が生まれる",
    ], 14, style="navy", title="分娩の管理そのものが変わる", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "病院・産科・助産師・麻酔科の全員が賛成して始めること。",
        "誰かが納得していないまま始めると、その摩擦は妊婦のところに現れる ── ",
        "呼んでも来ない、始めても効かない、途中で止められる、という形で。",
    ], 14, style="red", min_h=170)
    cv.save(path("f08_starting_program.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08):
        fn()
        print("ok:", fn.__name__)
