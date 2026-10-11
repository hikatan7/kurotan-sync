# -*- coding: utf-8 -*-
"""㊷ 図版（図1-1 〜 図18-1）"""
from fig42common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f01():
    cv = Canvas(W, 1260)
    y = head(cv, "図1-1　麻酔科が実際に関わっている四つの場所",
             "どれも「外科の問題」でも「病棟の問題」でもない。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① 手術部位感染に効く術中の因子", "blue",
         ["抗菌薬の時刻と追加", "体温", "血糖・酸素"]),
        ("② 自分が入れるカテーテル", "green",
         ["中心静脈", "動脈ライン", "末梢ライン"]),
        ("③ 自分が行う手技", "purple",
         ["脊髄幹麻酔", "神経ブロック"]),
        ("④ 自分の手と作業域", "red",
         ["手指衛生", "薬剤と静脈路", "麻酔器の周囲"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=13, min_h=230))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "周術期の感染対策は「外科の問題」「病棟の問題」と整理されがちである",
        "しかしこの四つは、麻酔科が自分で動かしている",
        "本書は外科の手技や病棟でのカテーテル管理は扱わない ── この四つに絞る",
    ], 14, style="navy", title="本書の範囲", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "この領域には新しい発見がほとんど出てこない。",
        "課題は知識ではなく、"
        "知っていることを毎日、全例で、急いでいるときにも実行できるかである。",
    ], 14, style="amber", min_h=140)
    cv.save(path("f01_where_we_are.png"))


def f02():
    cv = Canvas(W, 1260)
    y = head(cv, "図3-1　予防投与が効くための三つの条件",
             "麻酔科が直接動かせるのは①と②である。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 切開のときに濃度がある", "red",
         ["投与から切開までの時間", "点滴で落とし切っているか",
          "駆血帯を巻く前か"]),
        ("② 手術のあいだ保たれる", "amber",
         ["追加投与（第4章）", "出血が多いとき",
          "最も忘れられやすい"]),
        ("③ 対象に合った薬", "blue",
         ["手術の種類", "患者の背景",
          "外科・感染対策チームと決める"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "入室が遅れ、投与から切開までが開きすぎる",
        "投与を忘れたまま切開される／点滴で落としている途中で切開される",
        "駆血帯を巻く手術で、巻く前に入れ終わっていない",
        "そして「誰が投与するか」が決まっていない",
    ], 14, style="navy", title="実務で失敗する場面", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "外科が指示し、麻酔科が投与し、看護が準備する ── "
        "この三者で責任が曖昧になると投与が抜ける。",
        "「麻酔科が投与し、切開前に声に出して確認する」と決めておく。",
    ], 14, style="red", min_h=150)
    cv.save(path("f02_prophylaxis.png"))


def f03():
    cv = Canvas(W, 1260)
    y = head(cv, "図10-1　麻酔中に手指衛生が必要になる場面",
             "数分ごとに機会が生じる ── これが実行率の上がりにくい理由でもある。")
    bw = (W - 112 - 4 * 20) / 5
    cols = (
        ("気道に触れたあと", "red", ["挿管・吸引", "マスク換気"]),
        ("薬を準備する前", "blue", ["アンプル", "注射器"]),
        ("静脈路を触る前", "green", ["三方活栓", "側管"]),
        ("記録を打ったあと", "amber", ["キーボード", "画面"]),
        ("患者に触れる前後", "purple", ["体位", "処置"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12,
                          style=st, title=ttl, title_size=13, min_h=190))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "機会が多すぎる／手が塞がっている／消毒剤が遠い／時間がない",
        "そして「見られていない」── 手術室は監査が入りにくい",
    ], 14, style="red", title="なぜ実行率が上がらないのか", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "改善の報告に共通しているのは、"
        "「意識を高める」だけでは変わらないということ。",
        "消毒剤を手の届く場所に置く、手袋の使い方と組み合わせる、"
        "実行率を測って返す ──",
        "環境と仕組みを変えた取り組みのほうが効果を示している。",
    ], 14, style="navy", min_h=170)
    cv.save(path("f03_hand_hygiene.png"))


def f04():
    cv = Canvas(W, 1240)
    y = head(cv, "図11-1　作業域を介した伝播の三角形",
             "切りやすいのは「手」と「作業域」である。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("患者", "blue", ["気道の分泌物", "皮膚", "創部"]),
        ("麻酔科医の手", "red", ["触れ続けている", "手袋の付け外し",
                                 "ここを切るのが最も現実的"]),
        ("作業域", "amber", ["麻酔器・モニタ", "薬剤トレイ",
                             "キーボード・三方活栓"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=15, min_h=240))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "気道に触れたあと、必ず手指衛生を行う",
        "汚染しやすい手技のあとは手袋を替える",
        "薬剤と静脈路を触る前に手を清潔にする",
        "作業域を整理する ── 物が少ないほど清拭しやすい",
        "手術と手術のあいだの清拭に、麻酔器と作業域を含める",
    ], 13.5, style="navy", title="どこを切るか", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「汚染は起きている」という事実を前提に置く。",
        "そのうえで、どこを切るのがいちばん現実的かを考える。",
    ], 14.5, style="amber", min_h=130)
    cv.save(path("f04_work_area.png"))


def f05():
    cv = Canvas(W, 1280)
    y = head(cv, "図13-1　カテーテル関連感染を減らす五つ",
             "①と⑤が最も効果が大きく、そして最も忘れられやすい。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "順番", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.10, "①", "入れるか\nどうか", RED),
             (0.30, "②", "部位を選ぶ", BLUE),
             (0.50, "③", "無菌的\nバリア", GREEN),
             (0.70, "④", "管理する", ORANGE),
             (0.90, "⑤", "早く抜く", RED))
    for t, no, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, no, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12.5)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "手指衛生。最大限の無菌的バリア ── "
        "帽子、マスク、滅菌ガウン、滅菌手袋、全身を覆うドレープ",
        "皮膚消毒と、乾燥させる時間",
        "超音波を使うなら、プローブとゲルの清潔",
        "緊急で清潔が十分でなかった場合、その記録を残す",
    ], 13.5, style="navy", title="挿入のときに守ること", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "緊急時に清潔操作が不十分なまま挿入されたカテーテルは、",
        "「あとで入れ替える」判断の対象になる ── "
        "しかし記録がなければ、その機会そのものが失われる。",
    ], 14, style="red", min_h=150)
    cv.save(path("f05_catheter.png"))


def f06():
    cv = Canvas(W, 1240)
    y = head(cv, "図16-1　続けるための四つ",
             "「意識を高める」は、この四つのどれでもない。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① やりやすくする", "blue", ["消毒剤の配置", "物品の準備",
                                      "環境を変える"]),
        ("② 測る", "green", ["実施率", "遵守率",
                             "過程の指標を"]),
        ("③ 返す", "amber", ["測った結果を", "現場に戻す"]),
        ("④ 決める", "purple", ["手順を文書に", "誰が何をするか"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14, min_h=220))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "抗菌薬の予防投与の実施率と時刻／追加投与の実施率",
        "術中体温／カテーテル挿入時の清潔操作の遵守／手指衛生の実行率",
        "そして、感染そのものの発生率",
    ], 14, style="navy", title="測るもの", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "感染の発生率だけを測っても改善は難しい。",
        "頻度が低く、原因が多岐にわたるため、"
        "「どこを変えればよいか」が見えないからである。",
        "だから過程の指標を測る。",
    ], 14, style="amber", min_h=170)
    cv.save(path("f06_sustain.png"))


def f07():
    cv = Canvas(W, 1260)
    y = head(cv, "図18-1　一日の流れのなかの感染対策",
             "「切開前」と「術中の追加投与」は時刻に縛られた項目である。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "時点", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.08, "入室前", "抗菌薬の準備\n加温・物品", BLUE),
             (0.29, "導入", "手指衛生\n清潔操作", GREEN),
             (0.50, "切開前", "投与完了を\n声に出す", RED),
             (0.71, "術中", "追加投与\n体温・血糖", ORANGE),
             (0.92, "申し送り", "記録を渡す", PURPLE))
    for t, when, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, when, color=col, size=13)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "緊急で入れたライン ── 記録と申し送り",
        "清潔が不十分だった手技 ── 記録と申し送り",
        "留置したカテーテルの情報／抗菌薬の投与記録（初回と追加）",
    ], 14, style="navy", title="麻酔科から病棟へ渡すもの", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「緊急で入れた末梢ライン」「清潔が十分でなかった動脈ライン」──",
        "これらは伝えなければ、そのまま数日間使われる。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f07_timeline.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07):
        fn()
        print("ok:", fn.__name__)
