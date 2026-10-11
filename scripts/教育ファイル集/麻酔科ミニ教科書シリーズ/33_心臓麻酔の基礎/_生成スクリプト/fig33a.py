# -*- coding: utf-8 -*-
"""㉝ 図版（図1-1 〜 図20-1）"""
from fig33common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE,
                         C_NOTE)


def f01():
    cv = Canvas(W, 1180)
    y = head(cv, "図1-1　心臓麻酔で動かす五つのつまみ",
             "病態ごとに「上げたいもの」と「下げたいもの」が違う。")
    bw = (W - 112 - 4 * 22) / 5
    items = (
        ("前負荷", "blue", ["拡張末期の容量", "輸液・体位・静脈拡張"]),
        ("後負荷", "green", ["駆出に対抗する負荷", "血管収縮薬・拡張薬"]),
        ("収縮性", "amber", ["心筋そのものの力", "強心薬・虚血・電解質"]),
        ("心拍数とリズム", "purple", ["充満と逆流の時間", "ペーシング・抗不整脈薬"]),
        ("冠灌流", "red", ["拡張期圧と拡張期の長さ", "血圧・心拍数"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(items):
        hs.append(textbox(cv, 56 + i * (bw + 22), y, bw, lines, 12.5, style=st,
                          title=ttl, title_size=15, min_h=220))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "麻酔計画は薬の選択から始めない ── 「何を守るか」から始める",
        "守るものが決まれば、薬も輸液も自然に決まる（第3章）",
    ], 14, style="navy", title="計画の順番", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "判断が集中するのは、導入から人工心肺確立までと、離脱の前後",
        "この間は、術者・臨床工学技士・看護師と同じ画面を見ながら動く",
    ], 14, style="grey", min_h=120)
    cv.save(path("f01_five_levers.png"))


def f02():
    cv = Canvas(W, 1220)
    y = head(cv, "図3-1　病態ごとの血行動態の目標",
             "同じ「血圧を保つ」でも、狭窄性と逆流性では心拍数と後負荷の扱いが逆になる。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "充満に時間が要る",
        "→ 心拍数は遅め",
        "→ 心房収縮（洞調律）を守る",
        "→ 後負荷は下げない（冠灌流）",
        "",
        "AS・MS・肥大型（SAM）",
    ], 14, style="blue", title="狭窄性の病変", title_size=17, min_h=310)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "逆流する時間を短くしたい",
        "→ 心拍数は速め",
        "→ 後負荷を下げる",
        "→ 徐脈を避ける",
        "",
        "AR・MR",
    ], 14, style="green", title="逆流性の病変", title_size=17, min_h=310)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "冠動脈疾患 ── 頻脈は二重に悪い（供給を減らし、需要を増やす）",
        "右心不全・肺高血圧 ── 肺血管抵抗を上げず、体血圧を保つ",
        "SAM ── 強心薬で悪化する。前負荷と後負荷を上げ、心拍数を下げる",
    ], 14, style="amber", title="別の理屈で動くもの", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "表は暗記するものではなく、理屈を辿るための地図である（第II部）",
    ], 14.5, style="navy", min_h=110)
    cv.save(path("f02_targets.png"))


def f03():
    cv = Canvas(W, 1180)
    y = head(cv, "図5-1　大動脈弁狭窄症で守るもの",
             "四つが崩れると、短時間で虚血と低血圧の悪循環に入る。")
    bw = (W - 112 - 3 * 24) / 4
    items = (
        ("遅い心拍数", "blue", ["硬い左室は", "充満に時間が要る"]),
        ("十分な前負荷", "green", ["硬い左室を満たすには", "圧も容量も要る"]),
        ("下げない後負荷", "red", ["肥大心筋の冠灌流は", "拡張期圧に依存する"]),
        ("洞調律", "purple", ["心房収縮の寄与が大きい", "心房細動で破綻する"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(items):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 13, style=st,
                          title=ttl, title_size=15.5, min_h=210))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "頻脈 → 充満不足 → 心拍出量の低下 → 血圧低下 → 冠灌流の低下 →",
        "心筋虚血 → 収縮低下 → さらに血圧低下",
    ], 14, style="red", title="入ってはいけない悪循環", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "低血圧のときは、リズム → 心拍数 → 前負荷 → 血管収縮薬 の順に見る",
        "強心薬から手を出さない",
    ], 14, style="navy", title="低血圧になったときの順番", title_size=15)
    cv.save(path("f03_as.png"))


def f04():
    cv = Canvas(W, 1180)
    y = head(cv, "図8-1　SAM が起きたときの対応は、直観と逆になる",
             "強心薬を足すと悪化する。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "強心薬を増やす",
        "前負荷を減らす（利尿・脱水）",
        "後負荷を下げる（血管拡張薬）",
        "心拍数を上げる",
        "",
        "→ いずれも流出路狭窄を悪化させる",
    ], 13.5, style="red", title="やってはいけない", title_size=16.5, min_h=300)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "強心薬を止める・減らす",
        "前負荷を増やす（輸液）",
        "後負荷を上げる（血管収縮薬）",
        "心拍数を下げる",
        "",
        "→ それでも続けば外科的再検討",
    ], 13.5, style="green", title="やること", title_size=16.5, min_h=300)
    y2 = y + max(h1, h2) + 50
    textbox(cv, 56, y2, W - 112, [
        "僧帽弁形成術のあと、前尖が収縮期に左室流出路へ引き込まれる",
        "流出路狭窄と僧帽弁逆流が同時に起こる",
        "離脱時に「低血圧なのに強心薬が効かない」ときは、まず SAM を疑う",
    ], 14, style="navy", title="何が起きているか", title_size=15)
    cv.save(path("f04_sam.png"))


def f05():
    cv = Canvas(W, 1180)
    y = head(cv, "図10-1　TEE は判断を変えるための道具である",
             "何を見るかより先に、「何が分かれば手が変わるか」を決める。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("深さで決まる", "blue", ["上部食道", "中部食道", "経胃",
                                  "プローブを進める・引く"]),
        ("角度で決まる", "green", ["0°〜180°", "同じ位置でも断面が変わる",
                                   "角度を回して面を作る"]),
        ("目的で選ぶ", "amber", ["基本検査：限られた断面で全体像",
                                 "包括的検査：弁と壁運動を体系的に",
                                 "術式別：意思決定を助ける"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13, style=st,
                          title=ttl, title_size=16, min_h=250))
    y2 = y + max(hs) + 50
    textbox(cv, 56, y2, W - 112, [
        "所見は必ず外科医と共有する ── 見ているだけでは判断は変わらない",
        "同じ断面を毎回同じ順番で見る ── 変化に気づける",
        "禁忌（食道狭窄・静脈瘤・穿孔の既往）は術前に確認する",
        "画像が悪いときに、無理に結論を出さない",
    ], 14, style="navy", title="TEE を使うときの原則", title_size=15)
    cv.save(path("f05_tee_views.png"))


def f06():
    cv = Canvas(W, 1560)
    y = head(cv, "図13-1　離脱時に TEE で見る順番",
             "一巡してから、薬を動かす。")
    steps = (
        ("① 空気", "grey", "心腔内に残っていないか。脱気を続けるかの判断"),
        ("② 心機能", "blue", "収縮はどうか。後負荷が低いと良く見えることに注意"),
        ("③ 容量", "green", "拡張末期面積。頻脈と低血圧では小さく見える"),
        ("④ 修復した弁", "purple", "逆流は減ったか。狭窄を作っていないか"),
        ("⑤ 壁運動", "amber", "新たな異常はないか。冠動脈の問題を示唆する"),
        ("⑥ 流出路", "red", "SAM はないか（第8章）"),
    )
    yy = y
    for i, (ttl, st, memo) in enumerate(steps):
        h = textbox(cv, 56 + i * 26, yy, W - 112 - i * 52, [memo], 13.5,
                    style=st, title=ttl, title_size=15, min_h=115)
        yy += h + 14
    y2 = yy + 32
    textbox(cv, 56, y2, W - 112, [
        "順番を決めておくと、見落としが減り、伝える言葉も毎回同じになる",
        "「収縮は良い、容量は少ない、弁は問題ない、新しい壁運動異常はない」",
        "── この形で伝えれば、外科医も同じ枠で聞ける",
    ], 14, style="navy", title="順番を決める二つの利点", title_size=15)
    cv.save(path("f06_weaning_tee.png"))


def f07():
    cv = Canvas(W, 1180)
    y = head(cv, "図14-1　人工心肺が生体に与える四つの変化",
             "術後の多くの現象は、この四つから説明できる。")
    bw = (W - 112 - 3 * 24) / 4
    items = (
        ("① 非拍動流", "blue", ["拍動がなくなる", "微小循環と臓器灌流に影響"]),
        ("② 異物との接触", "red", ["炎症と凝固の活性化", "血小板機能の低下"]),
        ("③ 血液希釈", "green", ["充填液による希釈", "凝固因子とヘマトクリットの低下"]),
        ("④ 温度の操作", "amber", ["冷却と復温", "凝固・代謝・脳への影響"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(items):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 13, style=st,
                          title=ttl, title_size=15.5, min_h=220))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "CPB が置き換えるのは「血液を送ること」と「ガス交換」だけである",
        "生体の調節そのものは置き換えられない",
    ], 14, style="navy", title="置き換えられるもの・られないもの", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "麻酔科が判断に関わるのは、灌流圧・流量・温度・ヘマトクリット・血糖・麻酔深度",
        "運転そのものは臨床工学技士の領分 ── 目標を共有して進める",
    ], 14, style="grey", min_h=120)
    cv.save(path("f07_cpb_physiology.png"))


def f08():
    cv = Canvas(W, 1280)
    y = head(cv, "図18-1　人工心肺からの離脱の順番",
             "土台を整えてから、TEE で一巡し、そのあとで薬を動かす。")
    steps = (
        ("① 土台を整える", "blue",
         "体温・リズム・電解質・ヘマトクリット・換気・酸塩基"),
        ("② TEE で一巡", "green", "空気 → 心機能 → 容量 → 弁 → 壁運動 → 流出路"),
        ("③ 前負荷を戻す", "amber", "少しずつ戻し、心臓の応答を見る"),
        ("④ 必要なら薬を足す", "purple", "足りないものに合わせて選ぶ（第19章）"),
        ("⑤ 外れないとき", "red",
         "収縮・前負荷・後負荷・リズム・右心・外科的問題に分けて考える"),
    )
    yy = y
    for i, (ttl, st, memo) in enumerate(steps):
        h = textbox(cv, 56 + i * 30, yy, W - 112 - i * 60, [memo], 13.5,
                    style=st, title=ttl, title_size=15.5, min_h=125)
        yy += h + 16
    y2 = yy + 34
    textbox(cv, 56, y2, W - 112, [
        "整っていないまま薬を足すと、効かないか、効きすぎる",
        "アシドーシスがあれば昇圧薬は効きにくい",
        "体温が戻っていなければ、凝固障害と血管拡張が同時に来る",
    ], 14, style="navy", title="土台を先に整える理由", title_size=15)
    cv.save(path("f08_weaning_order.png"))


def f09():
    cv = Canvas(W, 1220)
    y = head(cv, "図19-1　何が足りないかで、薬が決まる",
             "血圧が上がっても心拍出量が増えていないことがある。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("血管が開いている", "red", ["末梢血管抵抗の低下", "→ 血管収縮薬",
                                     "ノルアドレナリン／バソプレシン"]),
        ("収縮が足りない", "blue", ["心筋そのものの力不足", "→ 強心薬",
                                    "頻脈と心筋酸素消費に注意"]),
        ("右心が回らない", "green", ["肺血管抵抗の上昇", "→ 抵抗を下げ体血圧を保つ",
                                     "吸入薬が有利（第20章）"]),
        ("前負荷が足りない", "amber", ["容量の不足", "→ まず輸液",
                                       "TEE で確認してから"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5, style=st,
                          title=ttl, title_size=15, min_h=240))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "レボシメンダンの二つの無作為化試験は、主要評価項目で有益性を示さなかった",
        "生理学的に理にかなった薬でも、転帰が変わるとは限らない",
    ], 14, style="navy", title="この領域の読み筋", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "薬を足したあとに、心拍出量が増えたかを確かめる",
        "血圧だけを見ていると、後負荷を上げて拍出を減らしていることに気づけない",
    ], 14, style="amber", min_h=120)
    cv.save(path("f09_inotropes.png"))


def f10():
    cv = Canvas(W, 1240)
    y = head(cv, "図20-1　右心不全の悪循環と、その断ち方",
             "右室の冠灌流は体血圧に依存する ── だから体血圧を保つ。")
    steps = (
        "肺血管抵抗の上昇",
        "右室の拡大と圧負荷",
        "心室中隔が左へ偏位",
        "左室の充満が低下",
        "体血圧の低下",
        "右室の冠灌流が低下",
    )
    bw = (W - 112 - 5 * 16) / 6
    for i, s in enumerate(steps):
        x = 56 + i * (bw + 16)
        textbox(cv, x, y, bw, [s], 12.5, style="red", min_h=150)
        if i < 5:
            cv.arrow((x + bw + 2, y + 75), (x + bw + 13, y + 75),
                     color=GREY, lw=2.0, head=11)
    y2 = y + 150 + 50
    bw2 = (W - 112 - 40) / 2
    h1 = textbox(cv, 56, y2, bw2, [
        "低酸素を作らない",
        "高二酸化炭素血症とアシドーシスを避ける",
        "過膨張を避ける（PEEP と一回換気量）",
        "低体温・疼痛・浅麻酔を避ける",
    ], 13.5, style="green", title="肺血管抵抗を上げない", title_size=15.5,
        min_h=250)
    h2 = textbox(cv, 56 + bw2 + 40, y2, bw2, [
        "体血圧を保つ（血管収縮薬）",
        "吸入薬なら体血圧を下げずに肺血管抵抗を下げられる",
        "過剰輸液で右室をさらに広げない",
        "リズムを整える（心房収縮の寄与が大きい）",
    ], 13.5, style="blue", title="冠灌流を保つ", title_size=15.5, min_h=250)
    y3 = y2 + max(h1, h2) + 44
    textbox(cv, 56, y3, W - 112, [
        "評価は数値より「右室が広がっていないか」「中隔が押されていないか」",
    ], 14.5, style="navy", min_h=110)
    cv.save(path("f10_rv.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10):
        fn()
        print("ok:", fn.__name__)
