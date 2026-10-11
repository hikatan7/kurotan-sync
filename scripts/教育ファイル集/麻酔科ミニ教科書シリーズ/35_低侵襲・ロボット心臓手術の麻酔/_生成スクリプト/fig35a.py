# -*- coding: utf-8 -*-
"""㉟ 図版 その1（図1-1 〜 図7-1）"""
from fig35common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f01():
    cv = Canvas(W, 1340)
    y = head(cv, "図1-1　胸骨を開けないぶん、仕事が麻酔側へ移る",
             "MICS の麻酔は新しい手技ではなく、"
             "「術者が失ったものを誰が補うか」を決めることである。")
    bw = (W - 112 - 4 * 20) / 5
    cols = (
        ("① 肺を虚脱させる", "blue", ["分離肺換気", "術野を作るため", "第II部"]),
        ("② 末梢から送脱血", "green", ["大腿動静脈・内頸静脈",
                                       "逆行性送血になる", "第III部"]),
        ("③ 器具を誘導する", "purple", ["TEE でワイヤ・管を追う",
                                        "術者には見えない", "第14章"]),
        ("④ 体表から除細動", "amber", ["パッドを先に貼る",
                                       "術野で当てられない", "第17章"]),
        ("⑤ 届かない状況に備える", "red", ["ドッキング中は動かせない",
                                           "移行に時間が要る", "第16・18章"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 20), y, bw, lines, 12,
                          style=st, title=ttl, title_size=13.5, min_h=230))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "術者が直接手を入れられない ── その分を麻酔科と臨床工学技士が埋める",
        "だから「新しい手技の習得」より「誰が何を補うかの取り決め」が効く",
        "この視点で読むと、本書の各章はすべてつながる",
    ], 14, style="navy", title="MICS の麻酔をひとことで言うと", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "患者にとっての利点 ── 創が小さい、輸血が減る、回復が早い",
        "麻酔科にとっての現実 ── 準備が増え、見る項目が増え、"
        "急変時の手数が増える",
    ], 14, style="amber", min_h=140)
    cv.save(path("f01_what_changes.png"))


def f02():
    cv = Canvas(W, 1240)
    y = head(cv, "図4-1　分離肺換気が持ち込む三つの負債",
             "得られるのは術野だけである。肺を落とす時間は短いほどよい。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 換気される肺が半分になる", "red",
         ["シャントができる", "低酸素の危険",
          "余裕のない患者ほど厳しい"]),
        ("② 虚脱と再開通を繰り返す", "amber",
         ["肺が傷む", "再開通には高い圧が要る",
          "術後の肺合併症につながる"]),
        ("③ 器具の位置がずれる", "blue",
         ["体位変換で", "術操作で",
          "人工心肺の前後で確認し直す"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "人工心肺が回っている間は、換気が止まっていても酸素化は保たれる",
        "つまり分離肺換気が本当に問題になるのは、人工心肺の前と後",
        "この二つの区間を短くできるかが、呼吸合併症を左右する",
    ], 14, style="navy", title="いつ問題になるのか", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "肺を虚脱させる目的は、術野を作ることだけ ── 呼吸生理上の必要はない",
    ], 14.5, style="grey", min_h=110)
    cv.save(path("f02_lung_isolation.png"))


def f03():
    cv = Canvas(W, 1300)
    y = head(cv, "図6-1　片肺換気で起きていること",
             "換気されない肺にも血液は流れる ── それがシャントになる。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "換気されない（虚脱した）肺",
        "　血流が残れば、酸素化されずに左心へ戻る",
        "　＝ 肺内シャント",
        "",
        "低酸素性肺血管収縮（HPV）が",
        "この血流を減らす方向に働く",
    ], 13.5, style="red", title="虚脱側で起きること", title_size=16.5,
        min_h=310)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "換気されている肺",
        "　血流が増え、ガス交換が増える",
        "　しかし受けられる量には限りがある",
        "",
        "高すぎる呼気終末陽圧は",
        "この側の血管を締め、血流を虚脱側へ押しやる",
    ], 13.5, style="blue", title="換気側で起きること", title_size=16.5,
        min_h=310)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "弱めるもの ── 吸入麻酔薬（濃度依存性）、血管拡張薬、"
        "低い混合静脈血酸素飽和度、肺血管の器質的変化",
        "保つもの ── 静脈麻酔薬（影響が小さい）、適切な心拍出量、"
        "正常範囲の二酸化炭素分圧",
    ], 13.5, style="navy", title="HPV を左右するもの", title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "だから片肺換気中の酸素化は、換気の設定だけで決まらない。",
        "循環と薬剤の影響を合わせて考える。",
    ], 14.5, style="amber", min_h=140)
    cv.save(path("f03_olv_physiology.png"))


def f04():
    cv = Canvas(W, 1300)
    y = head(cv, "図7-1　片肺換気中に低酸素になったときの順番",
             "慌てて酸素濃度だけを上げても、シャントが原因なら効きにくい。")
    x = 260
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "順番", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.13, "①", "位置を確認\n（最多）", BLUE),
             (0.29, "②", "酸素濃度", GREEN),
             (0.45, "③", "換気側を開く", ORANGE),
             (0.63, "④", "虚脱側に\n持続陽圧", PURPLE),
             (0.81, "⑤", "循環を\n立て直す", RED),
             (0.93, "⑥", "術者へ", GREY))
    for t, no, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, no, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "⑥の「両肺換気に戻す」は術野をつぶす ── 戻す前に術者へ伝える",
        "人工心肺が回り始めれば、この問題はいったん消える",
        "「どこまで粘るか」は、その見通しで決まる",
    ], 14, style="red", title="MICS で特に効いてくること", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "①で見つかることが多い ── 体位変換・術操作でずれる。"
        "気管支鏡は手元に置いておく。",
    ], 14, style="navy", min_h=120)
    cv.save(path("f04_olv_hypoxia.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04):
        fn()
        print("ok:", fn.__name__)
