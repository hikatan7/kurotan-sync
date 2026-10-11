# -*- coding: utf-8 -*-
"""㉟ 図版 その2（図10-1 〜 図20-1）"""
from fig35common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f05():
    cv = Canvas(W, 1300)
    y = head(cv, "図10-1　順行性と逆行性 ── 流れの向きが変わるということ",
             "だから術前 CT で大動脈の粥腫を見ることに意味がある。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "上行大動脈から送血する",
        "血液は心臓が押し出すのと同じ向きに流れる",
        "",
        "粥腫があっても、下流へ流れる",
        "内膜に対する力の向きも、通常と同じ",
    ], 13.5, style="blue", title="順行性（胸骨正中切開）", title_size=16.5,
        min_h=290)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "大腿動脈などから送血する",
        "血液は下行大動脈を上向きに流れる",
        "",
        "粥腫を上流（脳）へ押し流す経路ができる",
        "内膜に通常と逆向きの力がかかる",
    ], 13.5, style="red", title="逆行性（MICS）", title_size=16.5, min_h=290)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "送血開始直後の血圧と波形 ── 解離の兆候（第11章）",
        "近赤外分光法の左右差、瞳孔",
        "送血側下肢の灌流 ── 色・温度",
        "TEE での下行大動脈 ── フラップの出現",
    ], 14, style="navy", title="逆行性送血で麻酔科が見張るもの", title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "研究の結果は一致していない。共通しているのは"
        "「大動脈の粥腫が強い患者では危険が上がる」という点である。",
        "施設によっては、粥腫の強い患者で腋窩動脈などからの順行性送血を選ぶ。",
    ], 14, style="amber", min_h=150)
    cv.save(path("f05_retrograde.png"))


def f06():
    cv = Canvas(W, 1340)
    y = head(cv, "図14-1　MICS で TEE が担う四つの役割",
             "②と③は、胸骨正中切開なら術者が直接見ていたものである。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① 術前診断の確認", "blue",
         ["弁の病変と機序", "卵円孔開存", "大動脈弁逆流の程度"]),
        ("② 器具の誘導", "green",
         ["ガイドワイヤ", "脱血管の先端", "大動脈内バルーン"]),
        ("③ 合併症の早期発見", "red",
         ["下行大動脈のフラップ", "脱血不良", "心腔内の空気"]),
        ("④ 修復の評価と脱気", "purple",
         ["残存逆流・圧較差", "左房・左室・肺静脈", "上行大動脈"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=14.5, min_h=240))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "ガイドワイヤが右房・上大静脈に入っているか ── 肝静脈や奇静脈へ迷入しうる",
        "上大静脈側の脱血 ── 顔面の腫脹・結膜浮腫・近赤外分光法の低下で気づく",
        "大動脈内バルーンの位置と移動 ── 上流へ動けば腕頭動脈を塞ぎうる",
        "卵円孔開存 ── 右房を開ける術式では方針が変わる",
    ], 13.5, style="navy", title="MICS 特有の確認項目", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "これらを見るには、基本断面を確実に出せることが前提になる。",
        "土台は㉝『心臓麻酔の基礎』第III部が扱っている。",
    ], 14, style="grey", min_h=140)
    cv.save(path("f06_tee_roles.png"))


def f07():
    cv = Canvas(W, 1240)
    y = head(cv, "図16-1　ドッキング中にできなくなること",
             "だから「ドッキング前に済ませること」を項目として決めておく。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("① 体位を変えられない", "red", ["神経障害の予防は",
                                         "ドッキング前に完了させる"]),
        ("② 胸部に手が届かない", "amber", ["パッドの貼り直しができない",
                                           "聴診もできない"]),
        ("③ 器具の操作が制限される", "blue", ["気管支鏡・TEE の",
                                              "取り回しが難しくなる"]),
        ("④ 緊急時に時間が要る", "purple", ["まずアームを外す",
                                            "それから体位を戻す"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=13.5, min_h=210))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "分離用器具の位置を体位確定後に確認する（第5章）",
        "静脈路・動脈圧ライン・TEE の固定を確認する",
        "体表除細動パッドを貼る（第17章）",
        "点滴の延長と、薬剤の投与経路を手元にまとめる",
        "緊急時に誰が何をするかを、声に出して確認する",
    ], 14, style="navy", title="ドッキング前に済ませておくこと", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "強調されているのは手技そのものより、準備と段取りである。",
    ], 14.5, style="amber", min_h=110)
    cv.save(path("f07_robot_access.png"))


def f08():
    cv = Canvas(W, 1300)
    y = head(cv, "図18-1　胸骨切開へ移行するときの流れ",
             "この間、患者は不安定なままである。"
             "だから「何分かかるか」を施設で測っておく。")
    x = 250
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "手順", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.08, "①", "宣言する", RED),
             (0.26, "②", "アームを外す", PURPLE),
             (0.44, "③", "体位を戻す", ORANGE),
             (0.62, "④", "両肺換気へ", BLUE),
             (0.80, "⑤", "消毒・\nドレープ", GREEN),
             (0.95, "⑥", "開胸", GREY))
    for t, no, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, no, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12.5)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "輸血の手配 ── ①と並行して始める。予定より早く、多めに",
        "循環作動薬の準備と、投与経路の確保",
        "凝固の評価をやり直す（㉛）",
        "記録 ── 移行を決めた時刻と理由",
    ], 14, style="navy", title="麻酔科が並行して行うこと", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "「移行するかどうか」を議論している時間が、いちばん危ない。",
        "だから多くの施設が「迷ったら移行する」を原則として共有している。",
    ], 14.5, style="red", min_h=140)
    cv.save(path("f08_conversion.png"))


def f09():
    cv = Canvas(W, 1260)
    y = head(cv, "図20-1　小開胸の痛みと、胸壁のブロック",
             "「創が小さいから痛くない」とは限らない。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "肋間を開き、器具を出し入れする",
        "肋骨が圧迫される",
        "",
        "→ 体動と呼吸に伴う鋭い痛み",
        "→ 深呼吸と咳が妨げられる",
        "→ 早期離床が遅れる",
    ], 13.5, style="red", title="小開胸の痛みの質", title_size=16.5,
        min_h=300)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "傍脊椎ブロック",
        "前鋸筋面ブロック",
        "脊柱起立筋面ブロック",
        "",
        "いずれも報告は蓄積しているが、",
        "「どれが最善か」は決まっていない",
    ], 13.5, style="blue", title="用いられている胸壁ブロック",
        title_size=16.5, min_h=300)
    y2 = y + max(h1, h2) + 52
    h3 = textbox(cv, 56, y2, W - 112, [
        "抗凝固・抗血小板の状況を確認する（㉛・㉑）",
        "人工心肺後の凝固障害を見込んで、実施の時期を決める",
        "深いブロックほど、出血したときに気づきにくい",
        "施設の手順として合意を取る ── 個人判断で始めない",
    ], 14, style="navy", title="心臓手術で胸壁ブロックを考えるとき",
        title_size=16)
    y3 = y2 + h3 + 46
    textbox(cv, 56, y3, W - 112, [
        "ブロックだけで完結させず、多角的鎮痛の一部として組む。",
    ], 14.5, style="amber", min_h=110)
    cv.save(path("f09_blocks.png"))


if __name__ == "__main__":
    for fn in (f05, f06, f07, f08, f09):
        fn()
        print("ok:", fn.__name__)
