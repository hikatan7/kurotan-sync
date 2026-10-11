# -*- coding: utf-8 -*-
"""㊸ 図版（図1-1 〜 図22-1）"""
from fig43common import (W, Canvas, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f01():
    cv = Canvas(W, 1320)
    y = head(cv, "図1-1　腹腔は閉じた空間である",
             "腹腔内圧が上がると、離れた臓器が同時に動く。"
             "原因が気腹でも、腸閉塞でも、出血でも同じである。")
    h0 = textbox(cv, 56, y, W - 112, [
        "腹壁・横隔膜・後腹膜に囲まれた袋。",
        "途中まではゆるく、あるところから急に硬くなる。",
    ], 14.5, style="navy", title="腹腔内圧が上がる", title_size=17, min_h=175)
    y2 = y + h0 + 56
    bw = (W - 112 - 3 * 22) / 4
    cols = (
        ("横隔膜が上がる", "blue",
         ["肺が小さくなる", "気道内圧が上がる", "無気肺ができる"]),
        ("静脈が還らない", "green",
         ["下大静脈の圧迫", "胸腔内圧の上昇", "前負荷が減る"]),
        ("腎の出口が細る", "purple",
         ["腎静脈圧の上昇", "腎実質の圧迫", "尿が減る"]),
        ("内臓が虚血になる", "red",
         ["灌流圧の低下", "腸管が最初に不利", "外からは見えない"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 22), y2, bw, lines, 13,
                          style=st, title=ttl, title_size=14, min_h=240))
    y3 = y2 + max(hs) + 56
    textbox(cv, 56, y3, W - 112, [
        "この四つは、気腹でも、腸閉塞でも、腹腔内出血でも同じ順序で起きる。",
        "原因は違っても「腹腔内圧が上がる」という一点が共通しているからである。",
    ], 14.5, style="amber", min_h=150)
    cv.save(path("f01_abdominal_space.png"))


def f02():
    cv = Canvas(W, 1300)
    y = head(cv, "図2-1　開腹と腹腔鏡 ── 麻酔にとっての違い",
             "外科にとっての違いは術野の作り方。麻酔にとっては「開けるか、加圧するか」である。")
    bw = (W - 112 - 40) / 2
    h1 = textbox(cv, 56, y, bw, [
        "腹腔が大気圧に開く",
        "広い面から熱と水分が逃げる",
        "体液の移動と出血が主役",
        "創が大きく、痛みが呼吸を妨げる",
        "腸管の回復が遅れやすい",
    ], 14, style="blue", title="開腹", title_size=18, min_h=330)
    h2 = textbox(cv, 56 + bw + 40, y, bw, [
        "閉じたまま持続的に加圧される",
        "炭酸ガスが腹膜から吸収される",
        "圧と体位で循環が刻々と変わる",
        "創は小さいが肩の痛みが出る",
        "術後の回復は早い",
    ], 14, style="green", title="腹腔鏡・ロボット支援", title_size=18, min_h=330)
    y2 = y + max(h1, h2) + 56
    h3 = textbox(cv, 56, y2, W - 112, [
        "術後の回復が早いことと、術中の生理が穏やかであることは別である。",
        "術中に限れば、動く量はむしろ腹腔鏡のほうが大きい。",
    ], 15, style="navy", title="読み違えやすいところ", title_size=17)
    y3 = y2 + h3 + 50
    textbox(cv, 56, y3, W - 112, [
        "創が小さいぶん、生理の変化が外から見えない。",
        "そして腹腔鏡が開腹へ移行するときは、たいてい急いでいる。",
    ], 14.5, style="red", min_h=150)
    cv.save(path("f02_open_vs_lap.png"))


def f03():
    cv = Canvas(W, 1340)
    y = head(cv, "図4-1　気腹が呼吸・循環・腎に及ぼす作用",
             "三つは別々に起きるのではなく、腹腔内圧という一つの原因から出ている。")
    h0 = textbox(cv, 56, y, W - 112, [
        "炭酸ガスを腹腔へ送り込む ── 腹腔内圧が上がり、ガスが吸収される",
    ], 15, style="navy", title="気腹", title_size=17, min_h=155)
    y2 = y + h0 + 54
    bw = (W - 112 - 2 * 28) / 3
    cols = (
        ("呼吸", "blue",
         ["横隔膜が頭側へ",
          "機能的残気量の減少",
          "コンプライアンスの低下",
          "炭酸ガスの吸収",
          "── 出したいが、圧は上げたくない"]),
        ("循環", "green",
         ["低い圧では静脈還流が増え",
          "高い圧では減る（二相性）",
          "後負荷は増える",
          "交感神経系が刺激される",
          "── 血圧は保たれても心拍出量は落ちうる"]),
        ("腎・内臓", "purple",
         ["腎静脈圧の上昇",
          "腎実質の圧迫",
          "ホルモン系の作動",
          "内臓灌流の低下",
          "── 乏尿は容量不足の指標ではない"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 28), y2, bw, lines, 13,
                          style=st, title=ttl, title_size=16, min_h=330))
    y3 = y2 + max(hs) + 54
    textbox(cv, 56, y3, W - 112, [
        "呼気終末二酸化炭素分圧と動脈血の値の差は、気腹中に開きやすい。",
        "長時間・高度肥満・慢性肺疾患では、血液ガスで一度は確かめる。",
    ], 14.5, style="amber", title="見落としやすいこと", title_size=16)
    cv.save(path("f03_pneumoperitoneum.png"))


def f04():
    cv = Canvas(W, 1300)
    y = head(cv, "図7-1　頭低位と気腹が重なると何が起きるか",
             "二つの負荷は互いに打ち消さず、同じ方向に足し合わさる。")
    bw = (W - 112 - 40) / 2
    h1 = textbox(cv, 56, y, bw, [
        "横隔膜が頭側へ",
        "機能的残気量の減少",
        "気道内圧の上昇",
        "炭酸ガスの吸収",
    ], 14, style="blue", title="気腹", title_size=17, min_h=290)
    h2 = textbox(cv, 56 + bw + 40, y, bw, [
        "腹部臓器がさらに頭側へ",
        "頭部からの静脈還流が減る",
        "顔面・結膜・気道の浮腫",
        "眼圧と脳静脈圧の上昇",
    ], 14, style="purple", title="急な頭低位", title_size=17, min_h=290)
    y2 = y + max(h1, h2) + 30
    cv.arrow((56 + bw / 2, y2), (W / 2 - 40, y2 + 66), color=GREY, lw=2.6)
    cv.arrow((56 + bw + 40 + bw / 2, y2), (W / 2 + 40, y2 + 66), color=GREY, lw=2.6)
    y3 = y2 + 92
    h3 = textbox(cv, 56, y3, W - 112, [
        "肺は小さく、気道内圧は高く、顔と気道は浮腫み、",
        "それが数時間続く ── ロボット支援の骨盤内手術では、これが日常である。",
    ], 15, style="navy", title="重なった結果", title_size=17)
    y4 = y3 + h3 + 48
    textbox(cv, 56, y4, W - 112, [
        "抜管前に、顔・舌・結膜の浮腫を実際に見る。",
        "「入れたときと同じ気道」と思い込まない。",
    ], 14.5, style="red", min_h=150)
    cv.save(path("f04_position.png"))


def f05():
    cv = Canvas(W, 1300)
    y = head(cv, "図9-1　ERAS の構造",
             "個々の項目ではなく、術前から術後までがひと続きになっていることが本体である。")
    bw = (W - 112 - 2 * 26) / 3
    cols = (
        ("術前", "blue",
         ["絶飲食を長くしない", "炭水化物の負荷", "体を整える", "貧血の是正"]),
        ("術中（麻酔科の持ち場）", "green",
         ["輸液の量とタイミング", "オピオイドに偏らない鎮痛",
          "体温の維持", "筋弛緩からの確実な回復"]),
        ("術後", "purple",
         ["術後悪心嘔吐の予防", "早期の経口摂取", "早期離床", "点滴からの離脱"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 26), y, bw, lines, 13.5,
                          style=st, title=ttl, title_size=15, min_h=290))
    yb = y + max(hs)
    cv.arrow((56 + bw, yb - 140), (56 + bw + 26, yb - 140), color=GREY, lw=3)
    cv.arrow((56 + 2 * bw + 26, yb - 140), (56 + 2 * bw + 52, yb - 140),
             color=GREY, lw=3)
    y2 = yb + 56
    h2 = textbox(cv, 56, y2, W - 112, [
        "「早期の経口摂取」は、術後悪心嘔吐が抑えられていて初めて成り立つ。",
        "「早期離床」は、鎮痛ができていて、過剰な輸液で浮腫んでいないから成り立つ。",
    ], 14.5, style="navy", title="項目は互いに支え合っている", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "遵守率だけを追いかけると、成り立たない条件のまま項目だけを実行することになる。",
        "麻酔科が見るべきなのは、自分の担当項目が次の項目を成り立たせているかである。",
    ], 14.5, style="amber", min_h=150)
    cv.save(path("f05_eras.png"))


def f06():
    cv = Canvas(W, 1280)
    y = head(cv, "図11-1　輸液の二つの軸",
             "「どれだけ入れるか」と「いつ、何を見て入れるか」は独立した問題である。")
    bw = (W - 112 - 40) / 2
    h1 = textbox(cv, 56, y, bw, [
        "制限的か、自由か",
        "大きな腹部手術の無作為化試験では、",
        "制限的な群で急性腎障害が多かった",
        "── 「絞ればよい」は成り立たない",
    ], 14, style="blue", title="軸① 総量", title_size=17, min_h=300)
    h2 = textbox(cv, 56 + bw + 40, y, bw, [
        "何を見て加減するか",
        "心拍出量などを指標にする管理は",
        "術後合併症を減らす方向にあるが、",
        "死亡率が動く証拠は弱い",
    ], 14, style="green", title="軸② 指標", title_size=17, min_h=300)
    y2 = y + max(h1, h2) + 54
    h3 = textbox(cv, 56, y2, W - 112, [
        "気腹中の尿量は、血管内容量の指標として使えない。",
        "「尿が出ないから輸液」が、腹腔鏡で輸液が過剰になる典型的な経路である。",
    ], 15, style="red", title="腹部手術に固有の落とし穴", title_size=17)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "術式で方向が変わる ── 肝切除の離断中と、膵頭十二指腸切除の長時間経過では、",
        "同じ「腹部手術」でも輸液の向きが逆になりうる。",
    ], 14.5, style="navy", min_h=150)
    cv.save(path("f06_fluid.png"))


def f07():
    cv = Canvas(W, 1280)
    y = head(cv, "図20-1　緊急開腹の時間軸",
             "麻酔科が関わる時間は短く、そのあいだに決めることが多い。")
    bw = (W - 112 - 3 * 20) / 4
    cols = (
        ("診断・判断", "grey",
         ["いつ手術と決まったか", "画像はあるか", "ここで遅れることが多い"]),
        ("手術室へ", "amber",
         ["どれだけ脱水しているか", "敗血症はあるか",
          "満腹の胃として扱うか"]),
        ("術中", "red",
         ["導入で落ちる前提", "出血への備え", "抗菌薬と培養を止めない"]),
        ("術後", "blue",
         ["抜管するか、しないか", "閉創できたか", "どこへ帰すか"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14.5, min_h=250))
    y2 = y + max(hs) + 56
    h2 = textbox(cv, 56, y2, W - 112, [
        "この術式群の成績を決めているのは、個々の麻酔手技ではなく",
        "「誰がいつ判断し、どれだけ早く手術室に入るか」という体制である。",
    ], 15, style="navy", title="指針が体制の話をする理由", title_size=17)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「まだ整っていないので待ってください」ではなく、",
        "「整わないまま入ります。だから準備をこうします」と言う場面が多い。",
    ], 14.5, style="red", min_h=150)
    cv.save(path("f07_emergency.png"))


def f08():
    cv = Canvas(W, 1320)
    y = head(cv, "図22-1　腹腔内圧上昇の悪循環",
             "通常なら正しいはずの対応が、事態を悪化させうる。")
    bw = (W - 112 - 3 * 20) / 4
    steps = (
        ("① 腹腔内圧が上がる", "red",
         ["出血・腸管浮腫", "重症膵炎", "大量輸液のあと"]),
        ("② 心拍出量が落ちる", "amber",
         ["静脈還流の減少", "後負荷の増加"]),
        ("③ 尿が減る", "blue",
         ["腎静脈圧の上昇", "腎実質の圧迫", "灌流の低下"]),
        ("④ 輸液する", "purple",
         ["容量不足と読む", "腸管と後腹膜が浮腫む", "── ①へ戻る"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(steps):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14, min_h=250))
    yb = y + max(hs)
    for i in range(3):
        x0 = 56 + (i + 1) * bw + i * 20
        cv.arrow((x0, yb - 125), (x0 + 20, yb - 125), color=GREY, lw=3)
    y2 = yb + 56
    h2 = textbox(cv, 56, y2, W - 112, [
        "輪から抜けるには「圧が上がっていること自体が原因かもしれない」と",
        "一度疑う必要がある ── 疑わなければ、輸液は正しい対応に見え続ける。",
    ], 15, style="navy", title="この図の要点", title_size=17)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "腹部が硬い／気道内圧が説明なく上がる／輸液に反応しない乏尿が続く",
        "── このときに、腹腔内圧の上昇を思い出す。",
    ], 14.5, style="amber", min_h=150)
    cv.save(path("f08_iap_spiral.png"))


if __name__ == "__main__":
    for f in (f01, f02, f03, f04, f05, f06, f07, f08):
        f()
        print("ok", f.__name__)
