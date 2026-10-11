# -*- coding: utf-8 -*-
"""㉚ 図版 第V部・第VI部（図26-1 〜 図35-1）"""
from fig30common import (W, Canvas, Panel, LH, head, path, legend, decay,
                         textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                         ORANGE, PURPLE, C_PRES, C_FLOW, C_VOL, C_NOTE)


def f26():
    """ARDS 定義の変遷"""
    cv = Canvas(W, 1280)
    y = head(cv, "図26-1　ARDS の定義は何を変えてきたか",
             "定義を変えることは、誰を数えるかを変えることでもある。")
    bw = (W - 112 - 2 * 34) / 3
    cols = (
        ("1967年　Ashbaugh ら", "red",
         ["12例の症例集積", "急激な頻呼吸と低酸素血症",
          "両側のびまん性陰影", "コンプライアンスの低下",
          "PEEP を試して酸素化が改善"]),
        ("2012年　ベルリン定義", "blue",
         ["一週間以内の発症", "両側性の陰影",
          "心不全・体液過剰で説明できない", "PEEP 5 以上での酸素化",
          "軽症・中等症・重症の三段階"]),
        ("2024年　グローバル定義", "green",
         ["高流量鼻カニュラ下も対象に", "SpO₂/FiO₂ 比で診断できる",
          "胸部超音波を画像所見に含む", "資源の限られた環境にも開いた",
          "試験の対象と日常の対象がずれうる"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        x = 56 + i * (bw + 34)
        hs.append(textbox(cv, x, y, bw, lines, 13.5, style=st, title=ttl,
                          title_size=15, min_h=300))
        if i < 2:
            cv.arrow((x + bw + 4, y + 150), (x + bw + 30, y + 150),
                     color=GREY, lw=2.2, head=13)
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "adult（成人）の A は、小児にも同じ病態が起こると分かって acute（急性）の A になった",
        "名前がついたから、研究の対象として数えられるようになった",
        "論文を読むときは、その研究がどの定義で人を集めたのかを確かめる",
    ], 14, style="navy", title="定義の変遷が語っていること", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "肺炎・誤嚥・敗血症・外傷・輸血関連 ── 入口は違っても、"
        "肺胞上皮と血管内皮の傷害という同じ場所に集まる",
        "だから治療は「原因への治療」と「肺を壊さずに時間を稼ぐ換気」の二本立てになる",
    ], 14, style="grey", title="ARDS は原因ではなく共通の到達点", title_size=15)
    cv.save(path("f26_ards_definition.png"))


def f27():
    """PEEP の決め方"""
    cv = Canvas(W, 1240)
    y = head(cv, "図27-1　PEEP の決め方 ── 三つの流儀",
             "どの流儀を採っても、本体は「上げたあとに何を見るか」を決めておくことである。")
    bw = (W - 112 - 2 * 34) / 3
    cols = (
        ("① 表で決める", "blue",
         ["PEEP/FiO₂ table に従う", "再現性が高く、教育しやすい",
          "個々の肺の事情は反映されない"]),
        ("② 力学で決める", "purple",
         ["駆動圧が最小になる点を探す", "食道内圧を基準にする",
          "測定の手間と解釈の訓練が要る"]),
        ("③ 画像で決める", "green",
         ["EIT・肺エコーで見ながら", "開く領域と過膨張する領域を比べる",
          "予後改善を示した試験はまだない"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 34), y, bw, lines, 13.5,
                          style=st, title=ttl, title_size=16, min_h=240))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "つぶれた肺胞が多く、上げれば開く肺 ── リクルータビリティが高い",
        "すでに開いている肺が過膨張するだけの肺 ── リクルータビリティが低い",
        "同じ ARDS でも、この比率は患者ごとに大きく違う（R/I 比などで見積もる）",
    ], 14, style="amber", title="なぜ答えが一つにならないのか", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "① 酸素化は改善したか（数分から十数分待つ）",
        "② 駆動圧は下がったか（上がったなら過膨張を疑う）",
        "③ 血圧・心拍出量は保たれているか",
        "④ 戻すときの基準も同時に決めたか ── 上げっぱなしにしない",
    ], 14, style="navy", title="PEEP を上げたあとに見る四つ", title_size=15)
    cv.save(path("f27_peep_strategies.png"))


def f28():
    """重症低酸素血症の階段"""
    cv = Canvas(W, 1240)
    y = head(cv, "図28-1　重症低酸素血症に対する段階",
             "階段を飛ばさないこと、そして下の段を続けたまま上に進むこと。")
    steps_ = (
        ("土台", "肺保護換気と原因治療", "grey",
         "一回換気量と駆動圧の制限、感染源の制御、体液管理"),
        ("第一段", "腹臥位療法", "green",
         "重症例で死亡率を下げる。長時間続けることが条件"),
        ("第二段", "筋弛緩薬", "amber",
         "強い自発努力・非同調が肺を傷めていると判断される場面で短期間"),
        ("第三段", "ECMO", "red",
         "経験のある施設へ早期に相談する。搬送体制も含めて考える"),
    )
    n = len(steps_)
    bh = 150
    for i, (lab, ttl, st, memo) in enumerate(steps_):
        # 下から積み上げる
        k = n - 1 - i
        x = 56 + k * 70
        w = W - 112 - k * 140
        yy = y + i * (bh + 22)
        textbox(cv, x, yy, w, [memo], 13.5, style=st,
                title="%s　%s" % (lab, ttl), title_size=16, min_h=bh)
    y2 = y + n * (bh + 22) + 40
    textbox(cv, 56, y2, W - 112, [
        "酸素化がよくなる介入は数多いが、死亡率を下げた介入は驚くほど少ない",
        "腹臥位と低換気量が生き残っているのは、そこを直接測った試験があるから",
        "高頻度振動換気は、生理学的にきれいでも患者の生存を改善しなかった（2013年）",
    ], 14, style="navy", title="階段を登る前に思い出すこと", title_size=15)
    cv.save(path("f28_rescue_ladder.png"))


def f29():
    """閉塞性疾患で呼気時間を稼ぐ"""
    cv = Canvas(W, 1340)
    y = head(cv, "図29-1　閉塞性疾患では、呼気時間を作ることが目標になる",
             "問題は「入らない」ことではなく「出ない」ことである。")
    x = 210
    w = W - x - 90
    p1 = Panel(cv, x, y, w, 220, "呼気流量（回数が多い）", color=C_FLOW, base=.80)
    ex = []
    for i in range(5):
        t0 = i * .20
        ex += [(t0 + .01, .80), (t0 + .03, .95), (t0 + .09, .95),
               (t0 + .11, .28)] + decay(t0 + .11, t0 + .19, .28, .64, n=10)
    p1.plot(ex, color=C_FLOW)
    p1.hline(.80, color="#9aa6b4")
    p1.caption("基線に戻る前に次の吸気 ── 空気がたまり続ける", color=C_NOTE)

    p2 = Panel(cv, x, y + 290, w, 220, "呼気流量（回数を下げた）", color=C_FLOW,
               base=.80)
    ex2 = []
    for i in range(3):
        t0 = i * .33
        ex2 += [(t0 + .01, .80), (t0 + .03, .95), (t0 + .09, .95),
                (t0 + .11, .28)] + decay(t0 + .11, t0 + .31, .28, .79, n=18)
    p2.plot(ex2, color=C_FLOW)
    p2.hline(.80, color="#9aa6b4")
    p2.caption("基線まで戻ってから次の吸気", color=GREEN)

    y2 = y + 290 + 220 + 56
    bw = (W - 112 - 2 * 34) / 3
    hs = []
    for i, (ttl, lines, st) in enumerate((
        ("換気回数を下げる", ["直観と逆向きの操作", "PaCO₂ が高くても、まず呼気時間"], "green"),
        ("吸気時間を短くする", ["吸気流量を上げる", "同じ量を早く入れて呼気に回す"], "blue"),
        ("一回換気量を抑える", ["吐くべき量そのものを減らす", "pH が保てるうちは許容する"], "amber"),
    )):
        hs.append(textbox(cv, 56 + i * (bw + 34), y2, bw, lines, 13.5,
                          style=st, title=ttl, title_size=15, min_h=170))
    y3 = y2 + max(hs) + 44
    textbox(cv, 56, y3, W - 112, [
        "気流制限のある患者では、呼気時に末梢気道が虚脱して空気が閉じ込められる",
        "適度な外因性 PEEP はこの虚脱を防ぎ、トリガに必要な努力も減らす",
        "ただし内因性 PEEP を超えて上げれば過膨張が進む ── 「auto-PEEP の手前まで」",
    ], 14, style="navy", title="外因性 PEEP を足すという逆説", title_size=15)
    cv.save(path("f29_obstructive.png"))


def f31():
    """HFNC の効き方"""
    cv = Canvas(W, 1240)
    y = head(cv, "図31-1　高流量鼻カニュラ（HFNC）の効き方",
             "換気を肩代わりするわけではないが、呼吸仕事量は確実に減る。")
    bw = (W - 112 - 3 * 28) / 4
    items = (
        ("① 死腔の洗い出し", ["咽頭にたまった呼気を", "高流量で押し流す"], "blue"),
        ("② 吸気努力の軽減", ["患者の吸気流量を上回る流量", "→ 吸う仕事が減る"], "green"),
        ("③ わずかな陽圧", ["口を閉じていれば数 cmH₂O", "PEEP の代わりにはならない"], "amber"),
        ("④ 加温加湿と FiO₂", ["確実な加湿で分泌物が動く", "FiO₂ が希釈されず安定する"], "purple"),
    )
    hs = []
    for i, (ttl, lines, st) in enumerate(items):
        hs.append(textbox(cv, 56 + i * (bw + 28), y, bw, lines, 13, style=st,
                          title=ttl, title_size=15, min_h=210))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "COPD 増悪（高二酸化炭素血症）と心原性肺水腫 → NPPV の根拠が強い",
        "急性低酸素性呼吸不全 → HFNC が第一選択になりうる",
        "重症 ARDS → 挿管の遅れが害になりうる",
    ], 14, style="navy", title="病態ごとの第一選択", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "非侵襲的補助の下でも、強い吸気努力が続けば経肺圧は大きく振れ、肺は傷つく",
        "開始したら、改善の有無を評価する時刻をあらかじめ決めておく",
    ], 14, style="red", title="共通する最大の注意 ── 挿管が遅れること", title_size=15)
    cv.save(path("f31_niv_hfnc.png"))


def f32():
    """離脱の流れ"""
    cv = Canvas(W, 1240)
    y = head(cv, "図32-1　離脱の流れ",
             "SBT に通ることと、抜管できることは別の判断である。")
    bw = (W - 112 - 3 * 30) / 4
    steps_ = (
        ("① 毎日のスクリーニング", "blue",
         ["原因は改善したか", "低い FiO₂・PEEP で酸素化は保てるか",
          "昇圧薬は少量以下か", "指示に応じられるか、咳はできるか"]),
        ("② 覚醒試験（SAT）", "green",
         ["鎮静薬をいったん止める", "目を覚ますかを見る",
          "必要最小限で再開する"]),
        ("③ 自発呼吸試験（SBT）", "amber",
         ["支援をほぼ外して 30 分〜2 時間", "T ピース／CPAP／低い圧支持",
          "見るのは数値より患者"]),
        ("④ 抜管の判断", "purple",
         ["気道を自分で守れるか", "痰を出せるか、意識は十分か",
          "失敗したときの手は決まっているか"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(steps_):
        x = 56 + i * (bw + 30)
        hs.append(textbox(cv, x, y, bw, lines, 13, style=st, title=ttl,
                          title_size=15, min_h=280))
        if i < 3:
            cv.arrow((x + bw + 4, y + 140), (x + bw + 26, y + 140),
                     color=GREY, lw=2.2, head=13)
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "呼吸数の増加、浅速呼吸、補助呼吸筋の使用、発汗、頻脈、不穏 ── 出れば中止",
        "浅速呼吸指数（RSBI）は古典的な指標だが、単独で決めるものではない",
    ], 14, style="red", title="SBT 中に見るもの", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "離脱は「支援を少しずつ減らす作業」ではなく、"
        "「もう要らないのではないかを毎日確かめる作業」である",
    ], 14.5, style="navy", min_h=110)
    cv.save(path("f32_weaning_flow.png"))


def f35():
    """WIND 分類"""
    cv = Canvas(W, 1180)
    y = head(cv, "図35-1　離脱の経過による分類",
             "初回の離脱試行からどれだけの時間と回数を要したかで分ける。")
    bw = (W - 112 - 3 * 28) / 4
    cols = (
        ("試行なし", "grey", ["離脱が一度も試みられていない",
                              "無視できない割合を占める", "生理学ではなく手順の問題"]),
        ("短期", "green", ["最初の試行で離脱できた", "多くの患者がここに入る"]),
        ("難渋", "amber", ["複数回の試行を要した", "呼吸以外の要因を洗い直す時期"]),
        ("長期", "red", ["さらに長い経過をたどる", "心不全・栄養・筋力・せん妄・感染"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 28), y, bw, lines, 13, style=st,
                          title=ttl, title_size=16, min_h=230))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "離脱困難の一部は、生理学的な問題ではなく「試みられていないこと」による",
        "だからこそ、毎日のスクリーニングを手順として回す意味がある（第32章）",
    ], 14, style="navy", title="この分類がいちばん重く指摘したこと", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "人工呼吸開始から数日で横隔膜は薄くなりうる",
        "肺を守る設定と横隔膜を守る設定は、必ずしも同じではない",
        "人工呼吸中の判断は、退院後の生活（PICS）に続いている",
    ], 14, style="purple", title="長引いた患者で見落とされやすいもの", title_size=15)
    cv.save(path("f35_wind.png"))


if __name__ == "__main__":
    for fn in (f26, f27, f28, f29, f31, f32, f35):
        fn()
        print("ok:", fn.__name__)
