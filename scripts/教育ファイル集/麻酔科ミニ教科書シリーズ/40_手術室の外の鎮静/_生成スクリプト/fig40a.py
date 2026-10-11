# -*- coding: utf-8 -*-
"""㊵ 図版（図1-1 〜 図19-1）"""
from fig40common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f01():
    cv = Canvas(W, 1280)
    y = head(cv, "図1-1　手術室の外で足りないもの",
             "鎮静そのものの難しさより、この五つの不足が事故の背景になる。")
    bw = (W - 112 - 4 * 20) / 5
    cols = (
        ("① モニタと器材", "blue", ["場所によって違う", "探すところから始まる"]),
        ("② 人手", "green", ["誰を呼ぶかが", "決まっていない"]),
        ("③ 薬と器具", "amber", ["手元にない", "棚の奥にある"]),
        ("④ 情報", "purple", ["「検査の予定」しか", "分からないことがある"]),
        ("⑤ 慣れた手順", "red", ["その場の判断が多い", "訓練されていない"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12,
                          style=st, title=ttl, title_size=13.5, min_h=200))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "暗い・狭い・患者から離れている",
        "気道と処置が同じ場所を使う（内視鏡・歯科）",
        "騒音でアラームが聞こえない（放射線検査室）",
        "処置をする人が、患者も見ることになりやすい",
    ], 14, style="navy", title="場所そのものが持ち込む条件", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "遠隔地での麻酔に関する訴訟データの解析では、"
        "呼吸に関連した有害事象の割合が高く、"
        "監視が不十分だったと判断された例が相当数を占めた。",
        "これは「特殊な手技の失敗」ではなく、「見ていなかった」という形の問題である。",
    ], 14, style="red", min_h=160)
    cv.save(path("f01_why_harder.png"))


def f02():
    cv = Canvas(W, 1240)
    y = head(cv, "図2-1　鎮静の深さは連続している",
             "境目に壁はなく、意図した深さより深くなることは普通に起こる。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 240, "", color=INK)
    cv.text(x - 14, y + 120, "深さ", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.12, "軽い鎮静", "正常に答える", GREEN),
             (0.38, "中等度鎮静", "呼びかけ・\n軽い刺激で", BLUE),
             (0.64, "深い鎮静", "繰り返す刺激\n痛み刺激で", ORANGE),
             (0.90, "全身麻酔", "覚醒しない", RED))
    for t, when, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, when, color=col, size=13.5)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12)
    p.note(0.5, 0.10, "境目に壁はない", color=GREY, size=13)
    y2 = y + 240 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "中等度鎮静を行うなら、深い鎮静の状態から引き上げられること",
        "深い鎮静を行うなら、全身麻酔の状態から引き上げられること",
        "つまり「一段深い状態に対応できる能力と体制」が前提になる",
    ], 14, style="navy", title="指針が要求していること", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「どのくらいの深さを目指すか」は計画であって、",
        "「どのくらいの深さになったか」は結果である。この二つを混同しない。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f02_continuum.png"))


def f03():
    cv = Canvas(W, 1240)
    y = head(cv, "図6-1　どこで行うかを決める四つの材料",
             "四つが揃わないなら、場所を変えるか、"
             "麻酔科が出向くか、全身麻酔に切り替える。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① 患者のリスク", "blue", ["気道", "心肺疾患",
                                    "睡眠時無呼吸"]),
        ("② 処置の侵襲と時間", "green", ["痛みの強さ", "体位",
                                         "体動を許容できるか"]),
        ("③ その場所の設備と人手", "amber", ["モニタと器材",
                                             "見る人を確保できるか"]),
        ("④ 困ったときに来られる人", "red", ["誰を呼ぶか",
                                             "何分で来るか"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=13.5, min_h=220))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "気道が難しそう ── 手術室で行う／麻酔科が同席する",
        "処置が長い、体位がきつい ── 全身麻酔を検討する",
        "体動を許容できない処置 ── 浅い鎮静では成り立たない",
        "緊急で絶飲食が守られていない ── 気道確保を含めて設計し直す",
    ], 14, style="navy", title="考えたい選択肢", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「鎮静でやる」と決まっているから鎮静でやる、という進み方がいちばん危ない。",
        "処置を依頼する側は、鎮静の難しさを見積もる立場にないことが多い。",
    ], 14, style="amber", min_h=140)
    cv.save(path("f03_where.png"))


def f04():
    cv = Canvas(W, 1280)
    y = head(cv, "図9-1　酸素飽和度は、換気の異常に遅れて反応する",
             "その空白を埋めるのが、呼気二酸化炭素の監視である。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "時間", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.10, "①", "気道が落ちる\nいびき", BLUE),
             (0.34, "②", "換気が減る", GREEN),
             (0.58, "③", "二酸化炭素が\n溜まる", ORANGE),
             (0.84, "④", "酸素飽和度が\n下がる", RED))
    for t, no, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, no, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12.5)
    p.note(0.47, 0.10, "酸素を投与していると、この区間が長くなる",
           color=GREY, size=12.5)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "胸郭の動きと呼吸音 ── いちばん基本",
        "呼気二酸化炭素 ── 換気を直接見る",
        "酸素飽和度 ── 遅れて動く指標だと知って使う",
        "そして「患者を見る人の目」── 最も重要なモニタ",
    ], 14, style="navy", title="見るもの", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「酸素を投与しておけば安全」は、この構図では逆に働く。",
        "酸素は低酸素血症を遅らせるが、低換気そのものは止めない。",
        "遅らせているあいだに二酸化炭素は溜まり、気づいたときには深くなっている。",
    ], 14, style="red", min_h=170)
    cv.save(path("f04_monitoring.png"))


def f05():
    cv = Canvas(W, 1240)
    y = head(cv, "図10-1　鎮静に求めるものは、四つの組み合わせである",
             "どれが必要かで、使う薬と深さが決まる。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① 不安を取る", "green", ["説明と環境", "抗不安作用のある薬"]),
        ("② 痛みを取る", "red", ["局所麻酔", "鎮痛薬",
                                 "鎮静薬では取れない"]),
        ("③ 動かないようにする", "amber", ["深い鎮静か全身麻酔",
                                           "浅い鎮静では無理"]),
        ("④ 覚えていない", "purple", ["健忘作用のある薬",
                                      "ただし保証はできない"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14, min_h=220))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "痛い処置に鎮静薬を足していくと、痛みは取れないまま呼吸だけが止まる",
        "だから「痛みがあるなら、まず痛みを取る」",
        "局所麻酔を十分に効かせてから鎮静を考える",
    ], 14, style="navy", title="②がとくに重要", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「処置を早く終わらせたい」は、薬ではなく段取りの問題である。",
    ], 14.5, style="grey", min_h=110)
    cv.save(path("f05_what_you_need.png"))


def f06():
    cv = Canvas(W, 1280)
    y = head(cv, "図14-1　問題は、たいてい同じ順番で進む",
             "①②の段階で気づけるかどうかが分かれ目になる。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "進行", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.09, "①", "気道が落ちる", BLUE),
             (0.30, "②", "換気が減る", GREEN),
             (0.52, "③", "二酸化炭素\nが溜まる", ORANGE),
             (0.73, "④", "酸素飽和度\nが下がる", RED),
             (0.93, "⑤", "循環が\n破綻する", PURPLE))
    for t, no, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, no, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "①呼びかけて深さを確認 ②気道（頭位・下顎挙上・エアウェイ）",
        "③換気（胸郭・呼気二酸化炭素・補助換気）④酸素 ⑤循環",
        "⑥薬を止める。追加しない ⑦人を呼ぶ ── 遅らせない",
    ], 14, style="navy", title="困ったときの順番", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "体動・不穏に反射的に鎮静薬を足さない。",
        "その動きが低酸素によるものだった場合、薬を足すことは致命的になる。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f06_what_happens.png"))


def f07():
    cv = Canvas(W, 1280)
    y = head(cv, "図19-1　鎮静の体制を作るときの五つ",
             "この五つが決まっていれば、薬の選択は後からいくらでも調整できる。")
    bw = (W - 112 - 4 * 20) / 5
    cols = (
        ("① 誰が行い、誰が見るか", "blue", ["分けることを明記する",
                                            "途中で呼ばれない"]),
        ("② 何をそろえるか", "green", ["モニタと器材", "場所ごとに"]),
        ("③ どこまでの深さを、どこで", "amber", ["対象の処置",
                                                "場所を変える判断"]),
        ("④ 困ったときに誰を呼ぶか", "red", ["連絡経路",
                                            "何分で来るか"]),
        ("⑤ 記録し、集計し、振り返る", "purple", ["様式を決める",
                                                  "誰が見るか"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12,
                          style=st, title=ttl, title_size=12.5, min_h=210))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "「中等度鎮静のつもりで行った鎮静が、実際にはどのくらい深くなっているか」",
        "── これを数として見たことのある施設は多くない",
        "見えれば、議論の前提が変わる",
    ], 14, style="navy", title="集計すると見えるもの", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "麻酔科の役割は、すべての鎮静を自分でやることではない。",
        "この文書を作る側に立ち、"
        "「出向く場面」と「他科が行ってよい場面」の境目を一緒に決めること。",
    ], 14, style="amber", min_h=150)
    cv.save(path("f07_program.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07):
        fn()
        print("ok:", fn.__name__)
