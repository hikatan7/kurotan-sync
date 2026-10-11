# -*- coding: utf-8 -*-
"""㊴ 図版（図1-1 〜 図24-1）"""
from fig39common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f01():
    cv = Canvas(W, 1260)
    y = head(cv, "図1-1　術前評価が実際に答えている三つの問い",
             "「やめるかどうか」は①の一部にすぎず、"
             "実務で効くのは②と③のほうである。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① このまま進めてよいか", "red",
         ["延期する", "術式を変える",
          "方針そのものを見直す"]),
        ("② 進める前に直せるものはあるか", "green",
         ["貧血の是正", "心不全の代償",
          "薬の調整・禁煙"]),
        ("③ 何を見張り、何を準備するか", "blue",
         ["モニタリング", "術後の管理場所",
          "トロポニン・呼べる人"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13,
                          style=st, title=ttl, title_size=14.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "手術が必要だという判断は、たいてい外科側で済んでいる",
        "それを覆すだけの材料は、評価から出てこないことが多い",
        "だから①より②と③のほうが、実際には出番が多い",
    ], 14, style="navy", title="「やめるため」の評価ではない", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "この三つを分けておくと、"
        "「検査をしても方針が変わらないなら、その検査はしない」"
        "という判断が自然に出てくる。",
    ], 14.5, style="amber", min_h=120)
    cv.save(path("f01_purpose.png"))


def f02():
    cv = Canvas(W, 1240)
    y = head(cv, "図2-1　三つの指針と、その改訂",
             "手元に古い版しかない場合、"
             "とくに薬剤とバイオマーカーの扱いが変わっている。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 240, "", color=INK)
    cv.text(x - 14, y + 120, "改訂", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.12, "2014", "三者とも\n同じ年の版", GREY),
             (0.48, "2022", "欧州\n日本（英文は2023）", BLUE),
             (0.86, "2024", "米国\n10年ぶりの改訂", RED))
    for t, when, what, col in marks:
        p.vline(t, color=col, lw=2.2)
        p.note(t, 0.80, when, color=col, size=16)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12.5)
    y2 = y + 240 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "日本循環器学会 ── 2022年改訂版。循環器・外科・麻酔科の合同",
        "欧州心臓病学会 ── 2022年",
        "米国（AHA/ACC ほか）── 2024年。2014年版からの全面改訂",
    ], 14, style="navy", title="現行の版", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "この領域は、指針の改訂が推奨を反転させることがある。",
        "古い版を参照し続けることは、"
        "「情報が足りない」のではなく「逆向きの推奨に従う」ことになりうる。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f02_three_guidelines.png"))


def f03():
    cv = Canvas(W, 1240)
    y = head(cv, "図3-1　二つの軸で考える",
             "検査を足す意味があるのは、両方が高い領域だけである。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "低い ── 体表の小手術、白内障",
        "中等度 ── 腹腔鏡、整形外科、泌尿器科",
        "高い ── 開腹・開胸の大手術、大血管手術",
        "",
        "出血量・時間・体液移動で決まる",
    ], 13.5, style="blue", title="手術側のリスク", title_size=16.5,
        min_h=290)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "虚血性心疾患・心不全・脳血管疾患",
        "インスリンを要する糖尿病・腎機能低下",
        "弁膜症・肺高血圧・フレイル（指標に入らない）",
        "",
        "運動耐容能とバイオマーカーで足す",
    ], 13.5, style="green", title="患者側のリスク", title_size=16.5,
        min_h=290)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "どちらかが低ければ、追加の検査で方針が変わる余地は小さい",
        "両方が高いときだけ、検査を足す意味がある",
        "そしてもうひとつの軸が緊急度 ── 指針の最初の分岐はここである",
    ], 14, style="navy", title="組み合わせで決まる", title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "緊急に振り分けられれば、以降の枝はすべて飛ばされる。",
        "この構造自体が、術前評価の位置づけをよく表している。",
    ], 14.5, style="amber", min_h=140)
    cv.save(path("f03_two_axes.png"))


def f04():
    cv = Canvas(W, 1260)
    y = head(cv, "図6-1　運動耐容能をどう測るか",
             "この三つは一致しない。とくに①の精度は高くない。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 主観的な問診", "red",
         ["「階段は上がれますか」", "医師が頭の中で換算する",
          "心血管合併症を", "うまく予測しなかった"]),
        ("② 構造化した質問票", "green",
         ["決まった項目で聞く", "得点にする",
          "予測に寄与した"]),
        ("③ 心肺運動負荷試験", "blue",
         ["実際に運動して測る", "設備と時間が要る",
          "予測に寄与した"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "「動けますか」ではなく、具体的な日常動作で聞く",
        "できなくなった時期と、その理由を聞く",
        "整形外科的な理由で動けないのか、息切れで動けないのか",
        "動けない理由が心肺にあるなら、そこが評価の対象になる",
    ], 14, style="navy", title="実務でどうするか", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "動けるかどうかが分からないときは、バイオマーカーが補う（第7章）。",
    ], 14.5, style="grey", min_h=110)
    cv.save(path("f04_functional_capacity.png"))


def f05():
    cv = Canvas(W, 1300)
    y = head(cv, "図10-1　段階的に絞り込む ── ⑤で止まることが多い",
             "指針のフローチャートは、形は違ってもこの構造を共有している。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "順番", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.10, "①", "緊急か", RED),
             (0.30, "②", "手術側の\nリスクは", BLUE),
             (0.50, "③", "患者側の\nリスクは", GREEN),
             (0.70, "④", "運動耐容能", ORANGE),
             (0.90, "⑤", "方針が\n変わるか", PURPLE))
    for t, no, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, no, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12.5)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "①で「緊急」なら、以降はすべて飛ばして準備に集中する",
        "②③のどちらかが低ければ、そこで止まる",
        "⑤で「変わらない」なら、検査は行わない",
    ], 14, style="navy", title="止まる場所", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "検査の追加は手術を遅らせる ── 悪性腫瘍なら数週の遅れ自体が害になりうる。",
        "検査は無料ではない。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f05_stepwise.png"))


def f06():
    cv = Canvas(W, 1280)
    y = head(cv, "図11-1　予防的血行再建がうまくいかなかった構図",
             "「先に治しておけば安全になる」は、三つの理由で成り立たなかった。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 治療自体にリスクがある", "red",
         ["血行再建そのものの", "合併症と死亡"]),
        ("② 手術が遅れる", "amber",
         ["ステントを入れれば", "抗血小板薬が要る",
          "その分、手術を待つ"]),
        ("③ 機序が噛み合わない", "blue",
         ["術後の心筋傷害の多くは", "需要と供給の不均衡",
          "狭窄を広げても防げない"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14, min_h=240))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "大血管手術の患者を無作為に割り付けた試験で、長期の生存に差が出なかった",
        "近年の総説も、安定した患者への予防的血行再建を支持していない",
    ], 14, style="navy", title="示されたこと", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "血行再建を考えるのは「手術のために治す」ときではなく、",
        "「それ自体の適応があるから治す」ときである。",
        "この順序が入れ替わると、抗血小板薬の問題が手術の足を引っ張る。",
    ], 14, style="amber", min_h=170)
    cv.save(path("f06_revascularization.png"))


def f07():
    cv = Canvas(W, 1260)
    y = head(cv, "図7-1　抗血栓薬をどう扱うかを決める三つの軸",
             "この三つを揃えないと、判断は科のあいだで空回りする。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① なぜ飲んでいるのか", "blue",
         ["一次予防か", "ステントか（種類と時期）",
          "心房細動か、人工弁か"]),
        ("② 止めたら何が起きるか", "red",
         ["ステント血栓症", "心筋梗塞",
          "脳梗塞"]),
        ("③ 続けたら何が起きるか", "amber",
         ["出血の量", "出血する場所",
          "止血できる場所か"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "脊髄幹麻酔を行うなら、別の時間的制約が加わる（⑰）",
        "止める日と再開する日を、あらかじめ文書で決める",
        "再開の忘れが起こりやすい ── 誰が確認するかを決めておく",
        "この判断は麻酔科単独では決められない ── 循環器と外科に返す",
    ], 14, style="navy", title="そのうえで決めること", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "心房細動での「念のためのヘパリン橋渡し」は、"
        "血栓を減らさずに大出血を増やした（第16章）。",
    ], 14.5, style="red", min_h=120)
    cv.save(path("f07_antithrombotic.png"))


def f08():
    cv = Canvas(W, 1240)
    y = head(cv, "図23-1　術中低血圧と臓器傷害",
             "低さと、その状態が続いた時間の両方が効く。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "どのくらい低いか",
        "　絶対値だけでは決まらない",
        "　普段の血圧が高い患者では",
        "　同じ数字でも意味が違う",
        "",
        "だから「普段の血圧」を知っておく",
    ], 13.5, style="blue", title="深さ", title_size=16.5, min_h=290)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "どのくらい続いたか",
        "　短い低下と長い低下は違う",
        "　「下がってから追いかける」と",
        "　低い時間が長くなる",
        "",
        "だから下がらないようにする",
    ], 13.5, style="red", title="時間", title_size=16.5, min_h=290)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "複数の観察研究と系統的レビューで、"
        "急性腎障害と心筋傷害との関連が示されている",
        "ただし示されているのは関連であって、"
        "「血圧を上げれば転帰が良くなる」ことの証明ではない",
    ], 14, style="navy", title="分かっていること／いないこと", title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "術前の評価で動かせるものは限られている。",
        "麻酔科が直接動かせる要素の代表が、ここにある。",
    ], 14.5, style="amber", min_h=140)
    cv.save(path("f08_hypotension.png"))


def f09():
    cv = Canvas(W, 1280)
    y = head(cv, "図24-1　MINS ── 見に行かなければ見つからない",
             "無症候のトロポニン上昇が、死亡率と強く関連する。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① 症状がない", "grey", ["胸痛を訴えない", "麻薬と鎮静で",
                                  "隠れることもある"]),
        ("② 心電図も変わらない", "blue", ["典型的な変化を", "伴わないことが多い"]),
        ("③ トロポニンが上がる", "amber", ["測れば見つかる", "測らなければ",
                                          "見つからない"]),
        ("④ 死亡率が高い", "red", ["30日死亡と", "強く関連する"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14, min_h=230))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "測れば見つかる ── 見つかったら何をするのかを決めておく",
        "対象を決める ── 全例ではなく、リスクのある患者に絞る",
        "上がったときの対応と、退院後のフォローを決める",
        "この三つが決まっていないなら、測る意味は小さい",
    ], 14, style="navy", title="測る前に決めておくこと", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "MINS の多くが需要と供給の不均衡で起こるなら、",
        "術中の血圧・貧血・頻脈・低酸素の管理が、そのまま予防になる（第23章）。",
    ], 14.5, style="amber", min_h=140)
    cv.save(path("f09_mins.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09):
        fn()
        print("ok:", fn.__name__)
