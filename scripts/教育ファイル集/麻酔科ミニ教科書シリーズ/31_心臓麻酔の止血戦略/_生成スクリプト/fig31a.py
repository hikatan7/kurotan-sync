# -*- coding: utf-8 -*-
"""㉛ 図版 第I部・第II部（図1-1 〜 図8-1）"""
from fig31common import (W, Canvas, Panel, LH, head, path, legend, decay,
                         textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                         ORANGE, PURPLE, C_PRES, C_FLOW, C_VOL, C_NOTE)


def f01():
    """人工心肺が凝固系にすること"""
    cv = Canvas(W, 1300)
    y = head(cv, "図1-1　人工心肺が凝固系にしていること",
             "五つの経路が同時に進む。どれが主役かは症例ごとに違う。")
    bw = (W - 112 - 4 * 22) / 5
    items = (
        ("① 希釈", "blue", ["回路充填 700〜1,500 mL", "開始時に 15〜30％ の希釈",
                            "心筋保護液がさらに加わる"]),
        ("② 活性化と消費", "amber", ["ACT 480 秒以上でも", "凝固活性化は止まらない",
                                     "因子が静かに減る"]),
        ("③ 線溶亢進", "red", ["α2-PI が希釈で低下", "プラスミンが",
                               "フィブリノゲンも分解する"]),
        ("④ 血小板", "purple", ["ずり応力と活性化", "数も機能も落ちる",
                                "プロタミンも機能を下げる"]),
        ("⑤ 薬剤", "green", ["ヘパリン残存", "プロタミン過量",
                             "どちらでも出血が増える"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(items):
        hs.append(textbox(cv, 56 + i * (bw + 22), y, bw, lines, 12.5, style=st,
                          title=ttl, title_size=14.5, min_h=250))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "この五つに同時に効く製剤はない",
        "どれが主役かを決めてから手を出す ── そのための道具が"
        "フィブリノゲン値と粘弾性検査である",
        "そして「どれでもない」可能性 ── 外科的出血 ── を常に残しておく",
    ], 14, style="navy", title="五つを一度に相手にしない", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "フィブリノゲンは、他の凝固因子より先に止血可能域を下回る（第2章）",
        "だから「最初に確かめるべき一つ」として扱う理由がある",
    ], 14, style="grey", title="五つのうち、なぜフィブリノゲンから見るのか", title_size=15)
    cv.save(path("f01_cpb_coagulopathy.png"))


def f02():
    """フィブリノゲンが最初に底をつく"""
    cv = Canvas(W, 1240)
    y = head(cv, "図2-1　希釈が進むと、フィブリノゲンが最初に底をつく",
             "他の因子は正常の 30％ 程度でも止血に足りる。フィブリノゲンは濃度そのものが血餅の強さを決める。")
    x = 520
    w = W - x - 120
    p = Panel(cv, x, y, w, 330, "残存率", color=INK)
    # 希釈に伴う低下（同じ傾き）と、止血可能域の違い
    p.plot([(0, .92), (1.0, .28)], color=BLUE, lw=3.0)
    p.plot([(0, .92), (1.0, .28)], color=PURPLE, lw=0.1)
    p.hline(.34, color=BLUE, t0=0, t1=1.0)
    p.hline(.62, color=RED, t0=0, t1=1.0)
    cv.text(p.x - 14, p.py(.62), "フィブリノゲンの止血可能域", size=12,
            color=RED, ha="right", va="center", weight="bold")
    cv.text(p.x - 14, p.py(.34), "他の因子の止血可能域", size=12,
            color=BLUE, ha="right", va="center", weight="bold")
    p.note(.52, .76, "希釈はどの因子にも等しく効く", color=GREY, size=12.5)
    p.note(.62, .40, "ここで先に足りなくなる", color=C_NOTE, size=12.5)
    cv.text(p.px(.5), p.y + p.h + 34, "→　血液希釈の進行", size=13, color=GREY)

    y2 = y + 330 + 80
    bw = (W - 112 - 2 * 30) / 3
    hs = []
    for i, (ttl, st, lines) in enumerate((
        ("150 mg/dL", "red", ["後天性低フィブリノゲン血症の定義",
                              "保険適応の境界（添付文書）"]),
        ("150〜200 mg/dL", "amber", ["大量出血で投与を考える範囲",
                                     "大量出血GL 2019 の提案"]),
        ("200 mg/dL", "green", ["止血が期待できる目標",
                                "3 g 投与で 150 から到達しうる水準"]),
    )):
        hs.append(textbox(cv, 56 + i * (bw + 30), y2, bw, lines, 13, style=st,
                          title=ttl, title_size=17, min_h=180))
    y3 = y2 + max(hs) + 44
    textbox(cv, 56, y3, W - 112, [
        "フィブリノゲンは急性期蛋白でもある ── 術前に 400〜500 mg/dL のこともある",
        "その患者が 180 mg/dL まで落ちたとき、「基準値内」とは言えない",
        "絶対値と、その患者の出発点からの落差の両方を見る",
    ], 14, style="navy", title="絶対値だけで判断しない", title_size=15)
    cv.save(path("f02_fibrinogen_first.png"))


def f03():
    """ヘパリンとプロタミン"""
    cv = Canvas(W, 1180)
    y = head(cv, "図3-1　ヘパリンとプロタミンの綱引き",
             "不足でも過量でも出血は増える。ACT だけでは、どちら側に振れているか分からない。")
    bw = (W - 112 - 60) / 2
    from figlib import boxrow
    hh = boxrow(cv, 56, y, bw, 60, [
        ("プロタミンが足りないとき", ["ヘパリンが残る",
          "・プロタミンが足りない",
          "・回路や組織からの再分布（ヘパリンリバウンド）",
          "→ ACT 延長、にじむ出血"], "blue"),
        ("プロタミンが多すぎるとき", ["プロタミンそのものが抗凝固に働く",
          "・血小板機能も低下させる",
          "・投与速度が速いと血圧低下・肺高血圧",
          "→ ACT 延長、にじむ出血"], "red"),
    ], 13.5, title_size=15.5, min_h=250)
    y2 = y + hh + 46
    cv.arrow((56 + bw / 2, y2 - 40), (W / 2 - 60, y2 + 44), color=GREY, lw=2.2)
    cv.arrow((56 + bw + 60 + bw / 2, y2 - 40), (W / 2 + 60, y2 + 44),
             color=GREY, lw=2.2)
    h2 = textbox(cv, 56 + 180, y2 + 50, W - 112 - 360, [
        "どちらでも ACT は延びる ── 方向が分からない",
    ], 15, style="amber", title="同じ所見になってしまう", title_size=15.5, min_h=130)

    y3 = y2 + 50 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "HEPTEM（ヘパリナーゼ入り）と INTEM を比べる",
        "HEPTEM で凝固時間が短縮すれば、ヘパリンが残っている",
        "短縮しなければ、原因はヘパリンではない ── プロタミンを足す理由がない",
    ], 14, style="green", title="ROTEM なら方向が分かる", title_size=15)
    cv.save(path("f03_heparin_protamine.png"))


def f04():
    """一般凝固検査の限界"""
    cv = Canvas(W, 1180)
    y = head(cv, "図4-1　一般凝固検査が見ている範囲",
             "CPB 後に起きていることと、検査が見ている範囲はずれている。")
    rows = (
        ("PT・APTT", "血漿のトロンビン産生能", .34, "blue"),
        ("ACT", "ヘパリンの効き", .22, "amber"),
        ("血小板数", "数だけ（機能は見ない）", .28, "purple"),
        ("フィブリノゲン値", "量（働きは見ない）", .40, "green"),
        ("粘弾性検査", "全血の固まり方・強さ・溶け方", .88, "red"),
    )
    bar_x = 500
    bar_w = 640
    yy = y
    for name, memo, frac, st in rows:
        cv.text(56, yy + 30, name, size=13, color=INK, ha="left",
                va="center", weight="bold")
        cv.rect(bar_x, yy + 8, bar_w, 44, fc="#f2f4f6", ec="#c9d2dc", lw=1.0)
        from figlib import FILL
        f, e = FILL[st]
        cv.rect(bar_x, yy + 8, bar_w * frac, 44, fc=f, ec=e, lw=1.4)
        cv.text(bar_x + bar_w + 22, yy + 30, memo, size=12.5,
                color=INK, ha="left", va="center")
        yy += 74
    cv.text(bar_x, yy + 16, "→　CPB 後に起きていることの、どれだけを見ているか",
            size=12.5, color=GREY, ha="left")

    y2 = yy + 60
    bw = (W - 112 - 40) / 2
    hs = []
    hs.append(textbox(cv, 56, y2, bw, [
        "中央検査は結果まで少なくとも 30 分",
        "その間に術野の判断は進む",
        "結果として FFP と血小板が経験則で入る",
    ], 13.5, style="amber", title="時間の問題", title_size=15, min_h=210))
    hs.append(textbox(cv, 56 + bw + 40, y2, bw, [
        "Clauss 法は人工膠質液の影響で高めに出ることがある",
        "「足りているのに血餅が弱い」ときは測定法を疑う",
    ], 13.5, style="red", title="測定法の問題", title_size=15, min_h=210))
    cv.save(path("f04_lab_limits.png"))


def f05():
    """出血の見立て"""
    cv = Canvas(W, 1180)
    y = head(cv, "図5-1　外科的出血か、凝固障害か",
             "製剤を選ぶ前に、この区別をつける。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "一か所から拍動性・限局性に出る",
        "圧迫すれば止まる",
        "他の穿刺部は乾いている",
        "→ 術者に伝える。製剤で追いかけない",
    ], 14, style="red", title="外科的出血を示唆する所見", title_size=16, min_h=270)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "術野全体からじわじわ滲む",
        "縫合線・穿刺部・ドレーンからも出る",
        "圧迫しても止まらない場所が複数",
        "→ フィブリノゲン値と粘弾性検査へ",
    ], 14, style="blue", title="凝固障害を示唆する所見", title_size=16, min_h=270)

    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "縫合線　／　穿刺部　／　ドレーン　／　気道　／　尿",
        "複数の場所から出ていれば全身性、一か所だけなら局所 ── これが最初の分岐になる",
    ], 14.5, style="navy", title="五つの場所を見る", title_size=15.5)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "「いま止血材を当てたところは、止まっているか」",
        "止まらない場所が複数あるなら凝固障害、一か所だけなら外科的出血の可能性が高い",
    ], 14, style="grey", title="現場で効く一つの問い", title_size=15)
    cv.save(path("f05_bleeding_triage.png"))


def f06():
    """フィブリノゲンを測る三つの道"""
    cv = Canvas(W, 1160)
    y = head(cv, "図6-1　フィブリノゲンを測る三つの道",
             "測っているものと、返ってくるまでの時間が違う。")
    bw = (W - 112 - 2 * 34) / 3
    cols = (
        ("Clauss 法", "blue", ["中央検査室", "測るもの：量",
                               "30分前後", "膠質液で高めに出ることがある"]),
        ("FIBTEM", "green", ["ベッドサイド", "測るもの：働き（重合）",
                             "10〜20分", "血漿値と r = 0.85"]),
        ("血餅を見る", "grey", ["術野・回収血", "測るもの：印象",
                                "即時", "経験に依存する"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 34), y, bw, lines, 13.5, style=st,
                          title=ttl, title_size=16, min_h=260))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "Clauss 法はフィブリノゲンの「量」を、FIBTEM は「どれだけ固い網を作れるか」を見ている",
        "第 XIII 因子が低ければ、量があっても網は弱い",
        "膠質液が入っていれば、量は高く出ても網は弱い",
    ], 14, style="navy", title="量と働きは同じではない", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "両者がずれる場面こそ、粘弾性検査を持っている意味が出る場面である",
    ], 14.5, style="amber", min_h=110)
    cv.save(path("f06_fib_assay.png"))


def f07():
    """粘弾性検査の原理"""
    cv = Canvas(W, 1220)
    y = head(cv, "図7-1　粘弾性検査が描く曲線と、四つの読みどころ",
             "四つは、それぞれ別の治療に対応している。")
    x = 200
    w = W - x - 110
    p = Panel(cv, x, y, w, 330, "", color=INK, base=.5)
    cv.text(x - 14, y + 165, "血餅の固さ", size=13, color=INK,
            ha="right", va="center", weight="bold")
    up = decay(.18, .62, .50, .90, n=30, k=2.6)
    dn = [(1.0 - t + 0.0, v) for t, v in []]
    upper = [(0, .5), (.16, .5)] + up + [(.78, .90), (1.0, .80)]
    lower = [(t, 1.0 - v) for t, v in upper]
    p.plot(upper, color=BLUE, lw=2.6)
    p.plot(lower, color=BLUE, lw=2.6)
    p.vline(.16, color=ORANGE, lw=1.6)
    p.vline(.40, color=GREEN, lw=1.6)
    p.hline(.90, color="#c9d2dc", t0=.55, t1=1.0)
    p.toplabel(.16, "①CT／R", color=ORANGE)
    p.toplabel(.40, "②CFT／K・α", color=GREEN)
    p.toplabel(.70, "③MCF／MA", color=BLUE)
    p.toplabel(.95, "④LI／LY30", color=RED)
    p.note(.90, .62, "溶け方", color=RED, size=12)

    y2 = y + 330 + 60
    bw = (W - 112 - 3 * 24) / 4
    items = (
        ("① 固まり始めまで", "amber", ["凝固因子・ヘパリン", "→ FFP／PCC／プロタミン"]),
        ("② 固さが増す速さ", "green", ["フィブリノゲン・血小板", "→ フィブリノゲン補充"]),
        ("③ 最大の固さ", "blue", ["フィブリン＋血小板", "→ FIBTEM との差で分ける"]),
        ("④ 溶け方", "red", ["線溶", "→ 抗線溶薬"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(items):
        hs.append(textbox(cv, 56 + i * (bw + 24), y2, bw, lines, 13, style=st,
                          title=ttl, title_size=14.5, min_h=170))
    y3 = y2 + max(hs) + 44
    textbox(cv, 56, y3, W - 112, [
        "EXTEM と FIBTEM を並べて見るのが基本の型。両者の差が血小板の寄与にあたる",
        "HEPTEM と INTEM の比較でヘパリン残存、APTEM で線溶亢進を分ける",
    ], 14, style="navy", title="測定ラインの組み合わせ方", title_size=15)
    cv.save(path("f07_viscoelastic_principle.png"))


def f08():
    """FIBTEM を軸にしたアルゴリズム"""
    cv = Canvas(W, 1240)
    y = head(cv, "図8-1　粘弾性検査の保険適応とエビデンス",
             "算定できる範囲と、効果が示されている使い方は、どちらも限定されている。")
    bw = (W - 112 - 40) / 2
    h1 = textbox(cv, 56, y, bw, [
        "D006-21 血液粘弾性検査（一連につき）600点",
        "対象：心臓手術（人工心肺を用いるものに限る）",
        "目的：製剤投与の必要性の判断、投与後の評価",
        "回数：術前・術中・術後 各1回（複数回でも一連で1回）",
    ], 13.5, style="blue", title="保険上の位置づけ", title_size=16, min_h=270)
    h2 = textbox(cv, 56 + bw + 40, y, bw, [
        "POC 検査をアルゴリズムに組み込んだ 7,402 例の試験",
        "赤血球輸血 RR 0.91／血小板輸血 RR 0.77／大量出血 RR 0.83",
        "国内報告では術中総輸血量が 24.5％ 減",
        "コクランは死亡率への効果を不確実とする",
    ], 13.5, style="green", title="エビデンス", title_size=16, min_h=270)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "効いているのは検査そのものではなく、検査を組み込んだアルゴリズムである",
        "装置を買っただけでは何も変わらない ── 誰が測り、誰が読み、誰が出すかを決める",
    ], 14, style="navy", title="読み筋", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "人工心肺を用いない心臓手術（OPCAB など）では算定できない",
        "心臓以外の手術でも算定できない ── 使ってもよいが、費用は算定外になる",
    ], 14, style="amber", title="算定でつまずきやすい点", title_size=15)
    cv.save(path("f08_fibtem_algorithm.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08):
        fn()
        print("ok:", fn.__name__)
