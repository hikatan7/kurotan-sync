# -*- coding: utf-8 -*-
"""㉖ 蘇生アルゴリズムの変遷と周術期心停止　図版 f16〜f30"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE)
from fig26a import P, cap, msg, card, fitlines, W, TEAL


# ---------------------------------------------------------------- f16
def f16():
    """RRS の 4 要素"""
    cv = Canvas(W, 900)
    cap(cv, 44, "院内迅速対応システムの 4 要素")

    ITEMS = [
        ("起動要素", ["起動基準を決め、院内に周知する",
                  "バイタルを測る間隔を患者ごとに決めておく",
                  "基準を満たしたことが見てわかる仕組み",
                  "呼びやすい空気をつくる"], BLUE, "#eaf1f8"),
        ("対応要素", ["重症管理の経験がある医師または看護師",
                  "MET か RRT のどちらかの型をとる",
                  "要請から 15 分以内に現場へ",
                  "資機材を救急カート・携行バッグに"], GREEN, "#eaf5ee"),
        ("指揮調整要素", ["運営委員会がシステムを維持する",
                    "要綱と運営マニュアルを整える",
                    "全職員に教育と訓練の機会",
                    "主治医チームとの連携を設計する"], PURPLE, "#f1ecf8"),
        ("システム改善要素", ["起動事例の臨床データを集めて分析する",
                      "起動事例は全例を検討する",
                      "選んだ事例は多職種で振り返る",
                      "結果を各要素と病院全体に返す"], ORANGE, "#fdf3e3"),
    ]
    CW, GAP, L = 344, 24, 60
    hmax = 0
    for i, (head, lines, color, fc) in enumerate(ITEMS):
        hmax = max(hmax, card(cv, L + i * (CW + GAP), 106, CW, head, lines,
                              color, fc, body_size=9.8, lh=2.0))
    y = 106 + hmax + 34
    th = textbox(cv, 60, y, W - 120,
            ["前の 2 つは「その場」を、後ろの 2 つは「次回」を作る。",
             "起動と対応だけを整えた RRS は、"
             "動いてはいるが良くなっていかない。"],
            11.2, fc="white", ec=NAVY, title="前半は現場、後半は組織",
            title_color=NAVY, lw=1.8)
    msg(cv, y + th + 30,
        "4 要素は日本集中治療医学会「RRS 運用指針」"
        "（2024 年 1 月）の枠組みに沿っている。")
    cv.save(P("f16_rrs_four.png"))


# ---------------------------------------------------------------- f17
def f17():
    """MERIT が示したこと・示さなかったこと"""
    cv = Canvas(W, 880)
    cap(cv, 44, "MERIT 試験（2005）── 何が示され、何が示されなかったか")

    L, CW = 60, 690
    h1 = textbox(cv, L, 106, CW,
                 ["緊急コールは 3.1 → 8.7 / 1000 入院に増えた（p = 0.0001）",
                  "起動基準を満たして ICU 入室した患者の 30% に MET が呼ばれた",
                  "（対照病院は 9%、p = 0.009）",
                  "心停止・予期せぬ死亡は両群とも試験期間に減った"],
                 10.6, fc="#eaf5ee", ec=GREEN, title="示されたこと",
                 title_color=GREEN, lw=2.2, lh_scale=2.0)
    h2 = textbox(cv, L + CW + 30, 106, CW,
                 ["複合主要評価は 5.86 vs 5.31 / 1000 入院（p = 0.640）",
                  "心停止 1.64 vs 1.31（p = 0.736）",
                  "予定外 ICU 入室 4.68 vs 4.19（p = 0.599）",
                  "予期せぬ死亡 1.18 vs 1.06（p = 0.752）"],
                 10.6, fc="#fceeec", ec=RED, title="示されなかったこと",
                 title_color=RED, lw=2.2, lh_scale=2.0)
    y = 106 + max(h1, h2) + 34

    th = textbox(cv, 60, y, W - 120,
            ["豪州 23 病院のクラスター無作為化試験。介入は 4 か月の教育のあと 6 か月だけ。",
             "対照病院にも「心停止チーム」はあり、しかも試験期間中に対照群の成績も改善した。",
             "起動基準を満たした患者のうち、実際に呼ばれたのは 3 割にとどまった。",
             "つまりこの試験が測ったのは「MET の効果」ではなく「6 か月で導入した MET の効果」である。"],
            10.6, fc="white", ec=NAVY, title="結果をどう読むか",
            title_color=NAVY, lw=1.8, lh_scale=1.9)
    msg(cv, y + th + 30,
        "陰性の試験だったが、RRS は世界中に広がった。理由は次の図にある。")
    cv.save(P("f17_merit.png"))


# ---------------------------------------------------------------- f18
def f18():
    """早期コールの割合と有害事象"""
    cv = Canvas(W, 820)
    cap(cv, 44, "起動が増えることは、良いことである（MERIT 事後解析・Chen 2009）")

    hs, hl = fitlines(cv, ["早期コール（心停止にも死亡にも至っていない段階での要請）"
                           "の割合が 10% 増えるごとに"],
                      W - 200, 12.6, weight="bold", floor=10.0)
    hh = 44 + LH(hs, 1.5) * len(hl)
    cv.box(60, 106, W - 120, hh, fc="#e8edf5", ec=NAVY, lw=2.2, radius=8)
    cv.block(100, 106 + 22, W - 200, hl, hs, color=NAVY, weight="bold")

    ITEMS = [("予期せぬ心停止", "− 2.0", "／1 万入院", RED, "#fceeec"),
             ("心停止（全体）", "− 2.2", "／1 万入院", RED, "#fceeec"),
             ("予期せぬ死亡", "− 0.94", "／1 万入院", PURPLE, "#f1ecf8")]
    CW, GAP, L = 448, 28, 60
    cy = 106 + hh + 30
    for i, (name, val, unit, color, fc) in enumerate(ITEMS):
        x = L + i * (CW + GAP)
        cv.box(x, cy, CW, 190, fc=fc, ec=color, lw=2.2, radius=10)
        cv.text(x + CW / 2, cy + 38, name, size=12.4, color=color,
                weight="bold")
        cv.text(x + CW / 2, cy + 100, val, size=28, color=color, weight="bold")
        cv.text(x + CW / 2, cy + 160, unit, size=10.6, color=GREY)

    ty = cy + 220
    th = textbox(cv, 60, ty, W - 120,
            ["741,744 例、11,242 件の重大有害事象、3,700 件の緊急コールの解析。",
             "予定外 ICU 入室には同じ関係が見られなかった。",
             "MERIT では、起動のうち心停止・死亡に関連しないものが中央値 85.6%を占めていた。"],
            10.6, fc="white", ec=GREY, lw=1.6, lh_scale=1.9)

    msg(cv, ty + th + 30, "「呼びすぎではないか」という問いの答えは、"
                          "呼んだ回数ではなく、呼んだ時期で決まる。")
    cv.save(P("f18_early_call.png"))


# ---------------------------------------------------------------- f19
def f19():
    """日本の RRS 制度の流れ"""
    cv = Canvas(W, 800)
    cap(cv, 44, "日本で RRS が広がった順序 ── 学会・レジストリ・診療報酬")

    ITEMS = [
        ("2008", "医療安全全国共同行動",
         "行動目標 6 に院内急変。RRS が知られるきっかけ", NAVY, "#e8edf5"),
        ("2013", "RRS／IHCA レジストリ",
         "日本集中治療医学会と日本臨床救急医学会が開始", BLUE, "#eaf1f8"),
        ("2017", "RRS 用語集",
         "共通言語をそろえる。定義が施設ごとに違った", BLUE, "#eaf1f8"),
        ("2022", "急性期充実体制加算",
         "施設基準に RRS の体制整備。導入施設が急増", ORANGE, "#fdf3e3"),
        ("2024", "RRS 運用指針",
         "学会として初めて運用の水準を示した", GREEN, "#eaf5ee"),
        ("2026", "急性期総合体制加算",
         "総合入院体制加算と統合。急変の兆候を捉える体制を要件に",
         RED, "#fceeec"),
    ]
    CW, GAP, L, TOP, RH, CH = 690, 30, 60, 106, 158, 140
    for i, (yr, head, body, color, fc) in enumerate(ITEMS):
        col, row = i // 3, i % 3
        x = L + col * (CW + GAP)
        y = TOP + row * RH
        cv.box(x, y, CW, CH, fc=fc, ec=color, lw=2.0, radius=8)
        cv.box(x, y, 132, CH, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + 66, y + CH / 2, yr, size=17.0, color="white",
                weight="bold")
        hs, hl = fitlines(cv, [head], CW - 170, 12.2, weight="bold", floor=9.5)
        cv.block(x + 150, y + 18, CW - 170, hl, hs, color=color,
                 weight="bold", ha="left")
        bs, bl = fitlines(cv, [body], CW - 170, 10.5, floor=8.8)
        cv.block(x + 150, y + 68, CW - 170, bl, bs, color=INK, ha="left",
                 lh=LH(bs, 1.5))

    y = TOP + 3 * RH + 10
    textbox(cv, 60, y, W - 120,
            ["制度が先に動き、運用の指針が後から来た。"
             "そのため「加算のために作った RRS」が各地に残っている。",
             "運用指針が求めているのは、置くことではなく、"
             "起動事例を全例検討して各要素に返すことである。"],
            10.8, fc="white", ec=NAVY, title="順序の副作用",
            title_color=NAVY, lw=1.8)
    cv.save(P("f19_japan_rrs.png"))


# ---------------------------------------------------------------- f20
def f20():
    """指標の作り方"""
    cv = Canvas(W, 760)
    cap(cv, 44, "RRS を評価する指標 ── 何を分母に置くか")

    ROWS = [
        ("起動件数", "1000 入院あたりの起動件数",
         "実数だけでは病院の規模で変わる", BLUE),
        ("早期起動の割合", "心停止・死亡に至っていない起動 ÷ 全起動",
         "MERIT では中央値 85.6%。この比率が効果と相関する", GREEN),
        ("到着までの時間", "要請から現場到着までの中央値",
         "運用指針は 15 分以内を推奨している", GREEN),
        ("院内心停止の発生率", "1000 入院あたりの予期せぬ心停止",
         "下げたい数。ただし単独では動きにくい", ORANGE),
        ("起動基準を満たしたのに呼ばれなかった例", "見逃し率",
         "カルテのバイタルから後方視的に拾う。最も改善余地が大きい", RED),
        ("全例検討の実施率", "検討された起動事例 ÷ 全起動",
         "システム改善要素が動いているかの代理指標", PURPLE),
    ]
    L, TOP = 60, 106
    for i, (name, defn, note, color) in enumerate(ROWS):
        y = TOP + i * 88
        cv.box(L, y, W - 120, 76, fc="white", ec="#dde2e8", lw=1.4, radius=6)
        cv.rect(L, y, 8, 76, fc=color)
        ns, nl = fitlines(cv, [name], 380, 11.0, weight="bold", floor=8.8)
        cv.block(L + 26, y + 38 - LH(ns, 1.35) * len(nl) / 2, 380, nl, ns,
                 color=color, weight="bold", ha="left", lh=LH(ns, 1.35))
        ds, dl = fitlines(cv, [defn], 430, 10.4, floor=8.8)
        cv.block(L + 430, y + 38 - LH(ds, 1.35) * len(dl) / 2, 430, dl, ds,
                 color=INK, ha="left", lh=LH(ds, 1.35))
        ss, sl = fitlines(cv, [note], 500, 9.8, floor=8.4)
        cv.block(L + 880, y + 38 - LH(ss, 1.35) * len(sl) / 2, 500, sl, ss,
                 color=GREY, ha="left", lh=LH(ss, 1.35))

    msg(cv, TOP + 6 * 88 + 14,
        "起動件数が増えたことを「安全になった」と読める指標の組を、先に決めておく。")
    cv.save(P("f20_rrs_metrics.png"))


# ---------------------------------------------------------------- f21
def f21():
    """起動基準の例"""
    cv = Canvas(W, 700)
    cap(cv, 44, "起動基準の例（MERIT の基準）と、手術室・カテ室への読み替え")

    ROWS = [("A　気道", "気道が危うい", "回路・チューブの異常、抜管後の狭窄"),
            ("B　呼吸", "呼吸停止／呼吸数 5 未満または 36 超",
             "EtCO2 波形の変化、気道内圧の上昇"),
            ("C　循環", "心停止／脈拍 40 未満または 140 超／収縮期 90 未満",
             "動脈圧波形の平坦化、昇圧薬の急な増量"),
            ("D　意識", "GCS が 2 点以上低下／反復または遷延する痙攣",
             "鎮静下では使えない。代わりに瞳孔と筋緊張"),
            ("その他", "基準は満たさないが、スタッフが強く心配している",
             "「いつもと違う」を言葉にしてよいという許可")]
    L, TOP = 60, 106
    cv.box(L, TOP, W - 120, 46, fc=NAVY, ec=NAVY, lw=0, radius=6)
    for x, t in ((L + 110, "区分"), (L + 560, "一般病棟の基準"),
                 (L + 1130, "周術期での読み替え")):
        cv.text(x, TOP + 23, t, size=11.2, color="white", weight="bold")
    for i, (a, b, c) in enumerate(ROWS):
        y = TOP + 56 + i * 92
        cv.box(L, y, W - 120, 80, fc="#fafbfc" if i % 2 else "white",
               ec="#dde2e8", lw=1.2, radius=6)
        cv.text(L + 110, y + 40, a, size=11.4, color=NAVY, weight="bold")
        bs, bl = fitlines(cv, [b], 520, 10.4, floor=8.8)
        cv.block(L + 300, y + 40 - LH(bs, 1.4) * len(bl) / 2, 520, bl, bs,
                 color=INK, ha="left", lh=LH(bs, 1.4))
        cs, cl = fitlines(cv, [c], 440, 10.0, floor=8.6)
        cv.block(L + 900, y + 40 - LH(cs, 1.4) * len(cl) / 2, 440, cl, cs,
                 color=GREY, ha="left", lh=LH(cs, 1.4))

    msg(cv, TOP + 56 + 5 * 92 + 10,
        "最後の一行（スタッフが心配している）が、実務では最もよく使われる。")
    cv.save(P("f21_trigger.png"))


# ---------------------------------------------------------------- f22
def f22():
    """開心術後はなぜ別扱いか"""
    cv = Canvas(W, 840)
    cap(cv, 44, "開心術後の心停止が別扱いになる理由")

    ITEMS = [
        ("原因が偏っている", ["心室細動が 25-50%（虚血・ペーシング不全）",
                       "心タンポナーデ", "出血による循環血液量減少",
                       "いずれも数分で解除できる"], BLUE, "#eaf1f8"),
        ("外胸圧迫が効きにくい", ["タンポナーデと出血では、圧迫しても心臓が充満しない",
                          "胸骨の縫合線・グラフトを傷つけうる",
                          "内胸マッサージのほうが心係数・冠灌流圧が高い"],
         RED, "#fceeec"),
        ("手が届く道具がある", ["心外膜ペーシングワイヤが出ている",
                       "モニターが full monitoring",
                       "再開胸ができる人と器械がその場にある"],
         GREEN, "#eaf5ee"),
    ]
    CW, GAP, L = 448, 28, 60
    hmax = 0
    for i, (head, lines, color, fc) in enumerate(ITEMS):
        hmax = max(hmax, card(cv, L + i * (CW + GAP), 106, CW, head, lines,
                              color, fc, body_size=10.0, lh=1.95))
    y = 106 + hmax + 34

    bs, bl = fitlines(cv, ["EACTS 2009 は 17-79%、STS 2017 は「約半数」と報告している。"
                           "他の心停止とは別の病気だと考えたほうがよい"],
                      W - 220, 11.0, floor=9.4)
    bh = 62 + LH(bs, 1.6) * len(bl) + 18
    cv.box(60, y, W - 120, bh, fc="#e8edf5", ec=NAVY, lw=2.2, radius=10)
    cv.text(W / 2, y + 38, "だから、生存退院はおよそ半数に達する", size=13.4,
            color=NAVY, weight="bold")
    cv.block(110, y + 62, W - 220, bl, bs, color=INK, lh=LH(bs, 1.6))

    msg(cv, y + bh + 34, "この領域だけは、標準 ACLS から意図的に離れる。"
                     "「心臓マッサージをするな」から入るのが特徴である。")
    cv.save(P("f22_cals_why.png"))


# ---------------------------------------------------------------- f23
def f23():
    """CALS アルゴリズム"""
    cv = Canvas(W, 1030)
    cap(cv, 44, "開心術後の心停止 ── リズムで分かれる三つの道")

    _hw = cv.width("心停止の認識（波形で診断する）", 13.0, "bold") + 80
    cv.box(760 - _hw / 2, 96, _hw, 66, fc=NAVY, ec=NAVY, lw=0, radius=8)
    cv.text(760, 129, "心停止の認識（波形で診断する）", size=13.0,
            color="white", weight="bold")

    COLS = [
        ("心室細動／無脈性 VT", RED, "#fceeec",
         ["除細動器が 1 分以内に使えるなら",
          "外胸圧迫より先に 3 連続ショック",
          "",
          "成功率は 1 回目 78%、2 回目 35%、3 回目 14%",
          "",
          "3 回失敗 → 圧迫を開始しつつ再開胸へ",
          "3 回目のあとにアミオダロン 300 mg"]),
        ("心静止／高度徐脈", BLUE, "#eaf1f8",
         ["心外膜ワイヤがあるなら",
          "外胸圧迫より先にペーシング",
          "",
          "DDD・80-100 回/分・心房心室とも最大出力",
          "",
          "1 分で戻らなければ圧迫を開始",
          "体外式ペーシングは圧迫のあと"]),
        ("無脈性電気活動（PEA）", PURPLE, "#f1ecf8",
         ["ただちに外胸圧迫",
          "ペースメーカを一度止めて",
          "隠れた心室細動を除外する",
          "",
          "可逆的原因（気道・呼吸・気胸）を外す",
          "",
          "解決しなければ 5 分以内に再開胸"]),
    ]
    CW, GAP, L = 448, 28, 60
    hmax = 0
    for i, (head, color, fc, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.arrow((760, 164), (x + CW / 2, 196), color=color, lw=2.2, head=12)
        hmax = max(hmax, card(cv, x, 204, CW, head, lines, color, fc,
                              body_size=10.0, lh=1.85))

    ty = 204 + hmax + 34
    th = textbox(cv, 60, ty, W - 120,
            ["酸素を 100% に上げ、人工呼吸器を外してバッグ換気。両側の呼吸音と EtCO2 を確かめる。",
             "緊張性気胸を疑えば第 2 肋間鎖骨中線に太い針を刺す。確認できたら人工呼吸器に戻し PEEP は外す。",
             "心停止が確立したら、それまでの持続投与はいったんすべて止める（鎮静は続けてよい）。",
             "IABP は圧トリガーモード 1 : 1・最大 augmentation にする。"],
            10.6, fc="white", ec=NAVY, title="三つの道に共通して同時に進めること",
            title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, ty + th + 30, "外胸圧迫を「遅らせてよい」のは、"
                          "除細動器かペーシングが 1 分以内に届くときだけである。")
    cv.save(P("f23_cals_algo.png"))


# ---------------------------------------------------------------- f24
def f24():
    """CALS の系譜"""
    cv = Canvas(W, 900)
    cap(cv, 44, "開心術後心停止プロトコルの系譜")

    ITEMS = [
        ("2005", "ERC Guidelines",
         "初めて開心術後心停止の詳細な節を置いた", GREY, "#f2f4f6"),
        ("2009", "EACTS ガイドライン",
         "6 つの役割・3 連続ショック・先行ペーシング・早期再開胸・"
         "アドレナリンを入れない", BLUE, "#eaf1f8"),
        ("2017", "STS 専門家合意",
         "修正 Delphi 法。5 分以内の再開胸、10 日間はプロトコルの標準要素、"
         "小さな再開胸セット", GREEN, "#eaf5ee"),
        ("2021", "ERC Guidelines 2021",
         "EACTS／STS の内容を追認", GREY, "#f2f4f6"),
        ("2025", "AHA Guidelines Part 10",
         "AHA として初めて独立した節に。STS 2017 を明示的に参照", RED,
         "#fceeec"),
    ]
    L, TOP, CH, RH = 60, 106, 112, 126
    for i, (yr, head, body, color, fc) in enumerate(ITEMS):
        y = TOP + i * RH
        cv.box(L, y, W - 120, CH, fc=fc, ec=color, lw=2.0, radius=8)
        cv.box(L, y, 132, CH, fc=color, ec=color, lw=0, radius=8)
        cv.text(L + 66, y + CH / 2, yr, size=17.0, color="white",
                weight="bold")
        hs, hl = fitlines(cv, [head], 420, 12.4, weight="bold", floor=9.5)
        cv.block(L + 156, y + CH / 2 - LH(hs, 1.4) * len(hl) / 2, 420, hl, hs,
                 color=color, weight="bold", ha="left", lh=LH(hs, 1.4))
        bs, bl = fitlines(cv, [body], W - 740, 10.6, floor=8.8)
        cv.block(L + 600, y + CH / 2 - LH(bs, 1.5) * len(bl) / 2,
                 W - 740, bl, bs, color=INK, ha="left", lh=LH(bs, 1.5))

    ty = TOP + 5 * RH + 14
    textbox(cv, 60, ty, W - 120,
            ["AHA 2025 は「心臓手術後の VF に 3 連続ショックは標準 ALS より"
             "有益か」を研究上の空白として明記している。",
             "つまりこの領域の中心的な推奨は、"
             "いまも無作為化試験で確かめられていない。"],
            10.6, fc="white", ec=GREY, title="まだ試験がない",
            title_color=NAVY, lw=1.6)
    cv.save(P("f24_cals_lineage.png"))


# ---------------------------------------------------------------- f25
def f25():
    """6 つの役割"""
    cv = Canvas(W, 820)
    cap(cv, 44, "開心術後心停止で最初に割り当てる 6 つの役割")

    ROLES = [("1", "外胸心マッサージ", "100-120 回/分。動脈波形を見ながら",
              RED, "#fceeec"),
             ("2", "気道と呼吸", "酸素 100%、PEEP を外す、気胸・血胸を除外",
              BLUE, "#eaf1f8"),
             ("3", "除細動とペーシング", "内部除細動パドルを清潔野へ渡すのも担当",
              PURPLE, "#f1ecf8"),
             ("4", "チームリーダー", "手を動かさない。役割の割り当てと手順の確認",
              NAVY, "#e8edf5"),
             ("5", "薬剤とシリンジポンプ", "持続投与の中止と再開を管理する",
              ORANGE, "#fdf3e3"),
             ("6", "ICU コーディネーター", "人と物を集める。再開胸の準備を始める",
              GREEN, "#eaf5ee")]
    CW, GAP, L, CH, RH = 448, 28, 60, 186, 214
    for i, (no, name, body, color, fc) in enumerate(ROLES):
        r, c = i // 3, i % 3
        x = L + c * (CW + GAP)
        y = 106 + r * RH
        cv.box(x, y, CW, CH, fc=fc, ec=color, lw=2.2, radius=10)
        cv.box(x + 22, y + 20, 64, 64, fc=color, ec=color, lw=0, radius=10)
        cv.text(x + 54, y + 52, no, size=22, color="white", weight="bold")
        ns, nl = fitlines(cv, [name], CW - 130, 12.6, weight="bold", floor=9.6)
        cv.block(x + 104, y + 52 - LH(ns, 1.4) * len(nl) / 2, CW - 130, nl,
                 ns, color=color, weight="bold", ha="left", lh=LH(ns, 1.4))
        bs, bl = fitlines(cv, [body], CW - 60, 10.2, floor=8.8)
        cv.block(x + 30, y + 106, CW - 60, bl, bs, color=INK, ha="left",
                 lh=LH(bs, 1.6))

    y = 106 + 2 * RH + 8
    mh = msg(cv, y, "6 つの役割は EACTS 2009 が置き、STS 2017 が引き継いだ。"
                    "定期的にリハーサルすることまでが推奨である。")
    textbox(cv, 60, y + mh + 22, W - 120,
            ["役割を割り当てないと、全員が同じ場所（胸骨の上）に集まる。",
             "手術室でも同じことが起きる。だから本書は、"
             "順序より先に役割を書くことを勧める。"],
            10.6, fc="white", ec=GREY, lw=1.6)
    cv.save(P("f25_six_roles.png"))


# ---------------------------------------------------------------- f26
def f26():
    """再開胸の三つの数字"""
    cv = Canvas(W, 820)
    cap(cv, 44, "緊急再開胸の三つの数字")

    NUM = [("5 分以内", ["可逆的原因を外しても戻らない",
                      "非 VF/VT 心停止では、5 分以内に",
                      "再開胸する（STS 2017・Class I）"], RED, "#fceeec"),
           ("10 日間", ["術後少なくとも 10 日間は、",
                     "再開胸を蘇生プロトコルの",
                     "標準要素として置く"], ORANGE, "#fdf3e3"),
           ("5 点の器械", ["メス／ワイヤカッター／重持針器／",
                       "一体型開胸器／吸引。",
                       "フルセットは後で開ける"], GREEN, "#eaf5ee")]
    CW, GAP, L = 448, 28, 60
    for i, (title, lines, color, fc) in enumerate(NUM):
        x = L + i * (CW + GAP)
        cv.box(x, 106, CW, 252, fc=fc, ec=color, lw=2.4, radius=10)
        ts = cv.fit_size([title], CW - 60, 30, min_size=16, weight="bold")
        cv.text(x + CW / 2, 166, title, size=ts, color=color, weight="bold")
        s2, ls = fitlines(cv, lines, CW - 48, 10.4, floor=8.8)
        cv.block(x + 24, 212, CW - 48, ls, s2, color=INK, lh=LH(s2, 1.7))

    ty = 392
    th = textbox(cv, 60, ty, W - 120,
                 ["心停止コールと同時に 2-3 名がガウンと手袋をつける。"
                  "クローズドスリーブ法なら手洗いは不要。",
                  "再開胸は全心停止の 20-50%、心臓手術全体の 0.8-2.7% に必要になる。",
                  "ICU の外で行われた再開胸の成績は悪い。"
                  "つまり「どこで起きたか」で方針が変わる。",
                  "内胸マッサージは外胸圧迫より心係数と冠灌流圧が高い。"
                  "5 分を超えそうなら、はじめから内胸に切り替える。"],
                 10.6, fc="white", ec=NAVY, title="準備と現実",
                 title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, ty + th + 30, "「5 分以内」は手技の速さではなく、"
                          "呼んでから器械が開くまでの設計の問題である。")
    cv.save(P("f26_resternotomy.png"))


# ---------------------------------------------------------------- f27
def f27():
    """アドレナリンを入れない"""
    cv = Canvas(W, 680)
    cap(cv, 44, "開心術後だけ、アドレナリンをルーチンに入れない")

    L, CW = 60, 690
    h1 = textbox(cv, L, 106, CW,
                 ["可逆的原因が解除された瞬間に、極度の高血圧になる",
                  "縫合線・吻合部からの出血を誘発する",
                  "心拍再開後の大量出血の報告がある",
                  "この集団で有効性を示した文献がない"],
                 10.8, fc="#fceeec", ec=RED, title="入れない理由",
                 title_color=RED, lw=2.2, lh_scale=2.0)
    h2 = textbox(cv, L + CW + 30, 106, CW,
                 ["periarrest では 50-300 μg の少量なら許容される",
                  "使うなら、この集団での使用に慣れた医師の指示で",
                  "バソプレシンも同じ扱い（STS 2017：Class III harm）",
                  "アトロピンもルーチンには置かない（Class III no benefit）"],
                 10.8, fc="#eaf5ee", ec=GREEN, title="では、どうするか",
                 title_color=GREEN, lw=2.2, lh_scale=2.0)
    y = 106 + max(h1, h2) + 34

    cv.box(60, y, W - 120, 118, fc="#e8edf5", ec=NAVY, lw=2.2, radius=10)
    cv.text(W / 2, y + 36, "一般の ACLS と正反対になる、数少ない場面のひとつ",
            size=13.2, color=NAVY, weight="bold")
    cv.text(W / 2, y + 78, "静岡病院の A4 チャートも「アドレナリンは医師指示で」"
                           "と書き、定型の投与を外している",
            size=11.0, color=INK)

    msg(cv, y + 150, "覚えるのは用量ではない。"
                     "「原因が外れた直後に何が起きるか」である。")
    cv.save(P("f27_epi_in_cals.png"))


# ---------------------------------------------------------------- f28
def f28():
    """静岡病院 A4 チャート"""
    cv = Canvas(W, 1130)
    cap(cv, 44, "静岡病院の A4 チャート ── 胸骨正中切開後 10 日以内の心停止")

    cv.box(500, 96, 520, 62, fc=NAVY, ec=NAVY, lw=0, radius=8)
    cv.text(760, 127, "リズムチェック ＆ Dr. Call", size=13.0, color="white",
            weight="bold")

    COLS = [("Vf ／ VT", RED, "#fceeec",
             ["DC × 3（① 150 J　②③ 200 J）",
              "毎回リズムチェック",
              "",
              "続くならアミオダロン 300 mg",
              "（6 mL・2 A）＋ 5% ブドウ糖 20 mL を slow iv"]),
            ("心停止／PEA／徐脈", BLUE, "#eaf1f8",
             ["心室（V）リードでペーシング",
              "V を V にコネクトし電源 ON",
              "",
              "緊急設定はあらかじめ入れてある",
              "VVI ／ 60 ／ V-STIM 18.0 ／ V-SENSE 2.0"])]
    CW, GAP, L = 690, 30, 60
    hmax = 0
    for i, (head, color, fc, lines) in enumerate(COLS):
        x = L + i * (CW + GAP)
        cv.arrow((760, 160), (x + CW / 2, 192), color=color, lw=2.2, head=12)
        hmax = max(hmax, card(cv, x, 200, CW, head, lines, color, fc,
                              body_size=10.4, lh=1.8))

    y = 200 + hmax + 30
    cv.box(60, y, W - 120, 74, fc="#fdf3e3", ec=ORANGE, lw=2.2, radius=8)
    cv.text(W / 2, y + 37, "無効なら胸骨圧迫を開始", size=13.2, color=ORANGE,
            weight="bold")

    y2 = y + 74 + 48
    for i, (place, body, color, fc) in enumerate(
            [("ICU 版", "再開胸／VA-ECMO を考慮", PURPLE, "#f1ecf8"),
             ("HCU 版", "ICU へ移動", GREY, "#f2f4f6")]):
        x = 60 + i * (CW + GAP)
        cv.arrow((x + CW / 2, y + 78), (x + CW / 2, y2 - 6), color=color,
                 lw=2.2, head=12)
        cv.box(x, y2, CW, 76, fc=fc, ec=color, lw=2.2, radius=8)
        cv.text(x + 130, y2 + 38, place, size=12.4, color=color,
                weight="bold")
        cv.text(x + 430, y2 + 38, body, size=11.4, color=INK)

    textbox(cv, 60, y2 + 108, W - 120,
            ["以後は 2 分ごとにリズムチェック ± DC 200 J。",
             "並行して補液・血液ガス・エコー。"
             "人工呼吸器装着中なら酸素 100%・PEEP 0。",
             "アドレナリンは医師の指示で。準備物品は救急カート・除細動器・"
             "モニター・ペースメーカー。",
             "V リードは患者の左側（A ＝ 右房、V ＝ 右室）。"
             "延長コードの色は関係ない。"],
            10.4, fc="white", ec=NAVY, title="並行して行うこと",
            title_color=NAVY, lw=1.8, lh_scale=1.85)
    cv.save(P("f28_shizuoka_chart.png"))


# ---------------------------------------------------------------- f29
def f29():
    """デブリーフィング"""
    cv = Canvas(W, 800)
    cap(cv, 44, "振り返りの型 ── 熱いうちに、そして冷めてから")

    L, CW = 60, 690
    h1 = textbox(cv, L, 106, CW,
                 ["その場で、3 分から 5 分",
                  "誰が何をしたかではなく、何が起きたかを並べる",
                  "次に同じことが起きたら変えることを一つだけ決める",
                  "感情の整理はここではしない"],
                 10.8, fc="#fceeec", ec=RED, title="hot ── 直後の振り返り",
                 title_color=RED, lw=2.2, lh_scale=2.0)
    h2 = textbox(cv, L + CW + 30, 106, CW,
                 ["数日から数週あとに、多職種で",
                  "記録と時刻を並べ、仕組みの問題を探す",
                  "関係者の精神的な負担を扱えるのはこちら",
                  "決めたことを誰がいつまでにやるかまで書く"],
                 10.8, fc="#eaf1f8", ec=BLUE, title="cold ── 後日の振り返り",
                 title_color=BLUE, lw=2.2, lh_scale=2.0)
    y = 106 + max(h1, h2) + 34

    th = textbox(cv, 60, y, W - 120,
            ["2025 年版は、hot と cold の両方を取り入れることを新たに推奨した"
             "（Class 2a）。",
             "同じ年に、医療者のバーンアウトへの介入が初めて勧告に入った"
             "（Class 2b）。",
             "日本集中治療医学会の運用指針も、"
             "起動事例は全例を検討し、選んだ事例は多職種で振り返るとしている。"],
            10.6, fc="white", ec=NAVY, title="ガイドラインでの位置づけ",
            title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + th + 30,
        "見つかるのは、たいてい個人の技術ではなく仕組みの問題である。")
    cv.save(P("f29_debrief.png"))


# ---------------------------------------------------------------- f30
def f30():
    """三つの時間軸"""
    cv = Canvas(W, 820)
    cap(cv, 44, "三つの時間軸 ── 本書がどこを扱っているか")

    BANDS = [("予兆", "数時間〜数日", BLUE, "#eaf1f8",
              ["早期警告システム", "RRS の起動", "safety huddle",
               "手術室では「境目を言葉にする」"]),
             ("心停止", "分", RED, "#fceeec",
              ["圧迫と除細動", "原因の同時検索",
               "場面別のアルゴリズム", "開心術後は別プロトコル"]),
             ("回復", "日〜年", GREEN, "#eaf5ee",
              ["体温管理 32-37.5 ℃・36 時間以上", "神経学的予後予測",
               "サバイバーシップ", "振り返りと関係者の支援"])]
    CW, GAP, L = 448, 28, 60
    hmax = 0
    for i, (name, span, color, fc, lines) in enumerate(BANDS):
        x = L + i * (CW + GAP)
        cv.box(x, 106, CW, 66, fc=color, ec=color, lw=0, radius=8)
        cv.text(x + CW / 2 - 60, 139, name, size=15.0, color="white",
                weight="bold")
        cv.text(x + CW / 2 + 90, 141, span, size=11.0, color="white")
        s2, ls = fitlines(cv, lines, CW - 48, 10.4, floor=8.8)
        h = 34 + LH(s2, 2.0) * len(ls)
        hmax = max(hmax, h)
        cv.box(x, 182, CW, h, fc=fc, ec=color, lw=2.0, radius=8)
        cv.block(x + 24, 199, CW - 48, ls, s2, color=INK, lh=LH(s2, 2.0))
        if i:
            cv.arrow((x - 24, 139), (x - 4, 139), color=GREY, lw=2.4, head=13)

    ty = 182 + hmax + 32
    th = textbox(cv, 60, ty, W - 120,
                 ["2020 年版が 6 本目の鎖として「回復」を足し、"
                  "2025 年版が 7 本目として「予防」を検討している。",
                  "予防が鎖に入る日には、この図の左端が最も重い章になる。",
                  "手術室では、左端はすでに麻酔科医の仕事である。"],
                 10.8, fc="white", ec=NAVY, title="鎖はどちらへ伸びているか",
                 title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, ty + th + 30,
        "本書は左端と右端を扱う。真ん中の手順は第 ⑳ 巻にある。")
    cv.save(P("f30_three_times.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27,
               f28, f29, f30):
        fn()
        print("ok", fn.__name__)
