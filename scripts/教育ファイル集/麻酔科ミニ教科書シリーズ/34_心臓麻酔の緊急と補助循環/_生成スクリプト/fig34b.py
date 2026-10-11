# -*- coding: utf-8 -*-
"""㉞ 図版 その2（図10-1 〜 図16-1）"""
from fig34common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE)


def f05():
    cv = Canvas(W, 1320)
    y = head(cv, "図10-1　補助循環が実際にしていることは、四つしかない",
             "心筋仕事を減らす方向と、全身への流量を足す方向は、別のことである。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("前負荷を下げる", "purple", ["心室に入る量を減らす",
                                      "拡張末期圧が下がる", "うっ血が軽くなる"]),
        ("後負荷を下げる", "blue", ["心室が押し出す抵抗を減らす",
                                    "心筋の仕事が減る", "冠灌流が助かる"]),
        ("流量を足す", "green", ["全身へ送る血液を増やす",
                                 "臓器灌流を保つ", "心臓の代わりに送る"]),
        ("ガス交換をする", "amber", ["膜型肺で酸素化と除炭酸",
                                     "肺の代わりをする", "VA-ECMO だけ"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=15, min_h=240))
    y2 = y + max(hs) + 52
    bw2 = (W - 112 - 50) / 2
    h1 = textbox(cv, 56, y2, bw2, [
        "IABP ── 後負荷を下げ、冠灌流を助ける",
        "微小軸流ポンプ ── 左室から直接脱血し、前負荷を下げる",
        "",
        "「心臓を休ませたい」ときの方向",
    ], 14, style="blue", title="心筋仕事を減らす方向", title_size=16.5,
        min_h=250)
    h2 = textbox(cv, 56 + bw2 + 50, y2, bw2, [
        "VA-ECMO ── 大きく流量を足し、ガス交換もする",
        "ただし送血が逆行性のため、左室の後負荷は上がる",
        "",
        "「臓器灌流が足りない」ときの方向",
    ], 14, style="green", title="全身への流量を足す方向", title_size=16.5,
        min_h=250)
    y3 = y2 + max(h1, h2) + 48
    textbox(cv, 56, y3, W - 112, [
        "装置を選ぶ前に、「いま足りないのはどちらか」を言葉にする。",
        "流量なのか、心筋仕事を減らすことなのか、ガス交換なのか ── "
        "この三つのどれを狙うかで、選ぶ装置は決まる。",
    ], 14.5, style="navy", min_h=140)
    cv.save(path("f05_mcs_what.png"))


def f06():
    cv = Canvas(W, 1340)
    y = head(cv, "図13-1　VA-ECMO が作る三つの問題と、その見つけ方",
             "いずれも「装置が作った問題」である。だから監視の対象を先に決めておく。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 左室の後負荷が上がる", "red",
         ["送血が逆行性のため", "左室が空にならない",
          "→ 左室拡大・肺うっ血・心内血栓"]),
        ("② 上下半身で酸素化が違う", "purple",
         ["心拍出が回復してくると", "上半身は自己の肺から",
          "→ 差動性低酸素"]),
        ("③ 送血側の下肢が虚血になる", "amber",
         ["動脈を送血管が占める", "遠位の灌流が落ちる",
          "→ 下肢虚血・コンパートメント"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=15, min_h=260))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "① 左室が空になっているか ── TEE で大動脈弁が開いているかを見る。"
        "開かなければ左室減圧（venting）を検討する",
        "② 右手の SpO₂ と動脈血ガス ── 左手や下肢で測ると気づけない",
        "③ 送血側下肢の色・温度・NIRS ── 定時に見る項目として決めておく",
    ], 14, style="navy", title="見つけ方 ── どこを、何で見るか", title_size=16)
    y3 = y2 + h2 + 48
    textbox(cv, 56, y3, W - 112, [
        "溶血・血小板減少・出血 ── 抗凝固の管理は㉛『心臓麻酔の止血戦略』へ",
        "移動と体位変換はカニューレ事故が起こる場面（第15章）",
        "心筋梗塞後のショックでは、無作為化試験で死亡率は改善しなかった",
        "postcardiotomy shock では事実上の選択肢だが、成績は施設に依存する",
    ], 13.5, style="grey", min_h=180)
    cv.save(path("f06_ecmo.png"))


def f07():
    cv = Canvas(W, 1220)
    y = head(cv, "図11-1　SCAI のショック分類",
             "「どの段階で誰を呼ぶか」を決めるための共通言語。"
             "同じ「ショック」という言葉で違う状態を指していると、"
             "会話がすれ違う。")
    x = 230
    w = W - x - 110
    p = Panel(cv, x, y, w, 250, "", color=INK)
    cv.text(x - 14, y + 125, "重症度", size=13, color=INK, ha="right",
            va="center", weight="bold")
    marks = ((0.08, "A", "なりうる", GREEN),
             (0.28, "B", "血圧低下はあるが\n低灌流はない", BLUE),
             (0.50, "C", "低灌流があり\n介入を要する", ORANGE),
             (0.72, "D", "初期の介入に\n反応しない", RED),
             (0.92, "E", "循環虚脱・\n心停止に近い", PURPLE))
    for t, stg, what, col in marks:
        p.vline(t, color=col, lw=2.0)
        p.note(t, 0.80, stg, color=col, size=17)
        for j, ln in enumerate(what.split("\n")):
            p.note(t, 0.44 - j * 0.17, ln, color=col, size=12)
    y2 = y + 250 + 62
    h2 = textbox(cv, 56, y2, W - 112, [
        "この分類は治療方針を決める式ではない ── 重症度を揃える共通言語である",
        "実務上の価値は「どの段階で誰を呼ぶか」を事前に決められること",
        "段階が上がってから相談すると、装置を入れる時間そのものが足りなくなる",
    ], 14, style="navy", title="何のための分類か", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "C から D へ移る前に相談する ── これを施設の取り決めにしておく",
    ], 14.5, style="amber", min_h=110)
    cv.save(path("f07_scai.png"))


def f08():
    cv = Canvas(W, 1240)
    y = head(cv, "図12-1　IABP は何をしているか",
             "拡張期に膨らませて冠灌流を助け、収縮期直前に萎ませて後負荷を下げる。")
    x = 230
    w = W - x - 110
    p = Panel(cv, x, y, w, 260, "大動脈圧", color=BLUE, base=0.12)
    pts = []
    for i in range(0, 241):
        t = i / 240.0
        ph = (t * 3.0) % 1.0
        if ph < 0.10:
            v = 0.12 + (0.62 - 0.12) * (ph / 0.10)
        elif ph < 0.34:
            v = 0.62 - 0.18 * ((ph - 0.10) / 0.24)
        elif ph < 0.45:
            v = 0.44 + (0.84 - 0.44) * ((ph - 0.34) / 0.11)
        elif ph < 0.80:
            v = 0.84 - 0.62 * ((ph - 0.45) / 0.35)
        else:
            v = 0.22 - 0.10 * ((ph - 0.80) / 0.20)
        pts.append((t, v))
    p.plot(pts, color=BLUE, lw=2.8)
    p.toplabel(0.16, "収縮期", color=GREY)
    p.toplabel(0.47, "バルーンを膨らませる", color=RED)
    p.toplabel(0.83, "収縮期直前に萎ませる", color=GREEN)
    p.note(0.47, 0.20, "拡張期圧↑ → 冠灌流↑", color=RED, size=13)
    p.note(0.85, 0.20, "拡張末期圧↓ → 後負荷↓", color=GREEN, size=13)
    y2 = y + 260 + 66
    h2 = textbox(cv, 56, y2, W - 112, [
        "トリガは心電図または動脈圧波形 ── 心房細動や頻脈では乱れる",
        "大動脈解離・高度 AR は禁忌 ── 入れる前に TEE で確認する",
        "下肢虚血・血小板減少・溶血を経時的に見る",
    ], 14, style="navy", title="麻酔科が関わるところ", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "IABP-SHOCK II 試験（心筋梗塞に伴う心原性ショック）では、"
        "30日死亡率に有意差が示されなかった。",
        "位置づけは「循環を作り替える装置」ではなく、"
        "「後負荷を下げ、冠灌流を助ける補助」である。",
    ], 14, style="amber", min_h=150)
    cv.save(path("f08_iabp.png"))


def f09():
    cv = Canvas(W, 1240)
    y = head(cv, "図16-1　LVAD 装着患者が別の手術を受けるとき",
             "脈がない・前負荷に依存する・右室は助けられていない ── この三つが軸。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("脈がない", "blue", ["連続流のため脈圧が小さい",
                              "カフ血圧が測れないことがある",
                              "観血的動脈圧かドプラで平均血圧"]),
        ("前負荷に依存する", "green", ["脱水・出血に弱い",
                                       "吸引現象（サクション）",
                                       "容量を保つ"]),
        ("右室は助けていない", "red", ["LVAD は左室の補助",
                                       "右心不全は別の問題",
                                       "肺血管抵抗を上げない"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5,
                          style=st, title=ttl, title_size=15.5, min_h=250))
    y2 = y + max(hs) + 52
    h2 = textbox(cv, 56, y2, W - 112, [
        "抗凝固 ── 出血と血栓の両方のリスクを抱えている（㉛）",
        "不整脈 ── 心室頻拍でも意識があることがある",
        "電源と装置 ── バッテリー、予備、コントローラの扱いを確認する",
        "感染 ── ドライブライン感染。清潔操作を徹底する",
    ], 14, style="navy", title="併せて確認すること", title_size=16)
    y3 = y2 + h2 + 46
    textbox(cv, 56, y3, W - 112, [
        "この領域は装置と施設の運用に強く依存する。"
        "本書は原則だけを示す ── 実際の手順は装置の添付文書と"
        "施設の取り決めに従うこと。",
    ], 14, style="grey", min_h=130)
    cv.save(path("f09_lvad.png"))


if __name__ == "__main__":
    for fn in (f05, f06, f07, f08, f09):
        fn()
        print("ok:", fn.__name__)
