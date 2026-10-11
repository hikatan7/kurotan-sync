# -*- coding: utf-8 -*-
"""第Ⅴ章 TAVI・三尖弁　図版 n08〜n15"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)
from fig1a import cap, msg, fitlines, card, W, TEAL
from fig1b import step, down, side
from fig4a import fit
from figcrop import crop_bottom

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- n08
def n08():
    """三尖弁逆流という病態"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "三尖弁逆流は、弁の病気とは限らない")

    C = [("一次性（弁そのもの）", BLUE, "#eaf1f8",
          ["粘液腫様変性・感染性心内膜炎", "外傷・カルチノイド",
           "頻度としては少数"]),
         ("二次性（弁輪と右室）", RED, "#fceeec",
          ["右室・右房の拡大で弁輪が広がる", "肺高血圧・左心系疾患・心房細動",
           "臨床で出会う多くはこちら"]),
         ("リード関連", PURPLE, "#f1ecf8",
          ["弁を跨ぐリードが接合を妨げる", "リードと弁尖の癒着",
           "第Ⅰ章の CIED がここで戻ってくる"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 130, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    y1 = 440
    cv.box(70, y1, W - 140, 330, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(W / 2, y1 + 38, "逆流が続くと何が起こるか", size=12.4,
            color=NAVY, weight="bold")
    CH = [("右房圧が上がる", "静脈系がうっ滞する"),
          ("肝うっ血", "肝機能障害・凝固異常"),
          ("腎うっ血", "利尿薬が効きにくくなる"),
          ("腸管浮腫", "経口薬の吸収が落ちる"),
          ("右室の拡大", "心室中隔が左室を圧排する")]
    w2 = (W - 200 - 4 * 16) / 5
    for i, (a, b) in enumerate(CH):
        x = 100 + (w2 + 16) * i
        cv.box(x, y1 + 78, w2, 210, fc="#f7f9fb", ec="#c9d2dc", lw=1.4,
               radius=8)
        for j, ln in enumerate(cv.wrap(a, w2 - 26, 10.8)):
            cv.text(x + w2 / 2, y1 + 116 + LH(10.8, 1.35) * j, ln, size=10.8, color=NAVY,
                    weight="bold")
        for j, ln in enumerate(cv.wrap(b, w2 - 26, 9.8)):
            cv.text(x + w2 / 2, y1 + 200 + LH(9.8, 1.35) * j, ln, size=9.8, color=INK)
        if i < 4:
            cv.arrow((x + w2 + 2, y1 + 183), (x + w2 + 14, y1 + 183),
                     color="#b9c2cc", lw=1.6, head=8)

    th = textbox(cv, 70, y1 + 360, W - 140,
                 ["麻酔科が出会うのは、この連鎖がすでに進んだ患者である。",
                  "肝機能が悪く、凝固が乱れ、利尿薬が効かず、腹水があり、"
                  "経口薬の吸収も不確かである。",
                  "手技そのものより、この状態の患者を数時間、"
                  "仰臥位で管理することのほうが難しい。"],
                 10.8, style="amber", title="麻酔科が引き受けるもの",
                 title_color="#9a6510", pad_y=16)
    cv.save(P("n08_tr_pathophysiology.png"))
    crop_bottom(P("n08_tr_pathophysiology.png"))


# ---------------------------------------------------------------- n09
def n09():
    """T-TEER の三つのデータ"""
    cv = Canvas(W, 1400)
    cap(cv, 44, "三尖弁を治すと、何が良くなるのか")

    ROWS = [("TRILUMINATE（2023）", GREEN, "重症 TR 350 例（各 175）",
             "主要評価項目は T-TEER 優位（win ratio 1.48、95%CI 1.06-2.13、"
             "p=0.02）",
             "ただし死亡・弁手術・心不全入院に差はなく、改善は主に QOL"),
            ("TRILUMINATE 2 年（2025）", BLUE, "同 350 例",
             "心不全入院 0.19 対 0.26 件/患者年（HR 0.72、p=0.02）",
             "2 年では入院に差が出た"),
            ("Tri.Fr（2025）", GREEN, "孤立性重症 TR 300 例（152／148）",
             "1 年の複合スコア改善 74.1% 対 40.6%",
             "massive/torrential TR は 6.8% 対 53.5%"),
            ("bRIGHT（2024）", PURPLE, "実臨床 511 例（79±7 歳）",
             "88% が massive/torrential TR、80% が NYHA III/IV",
             "1 年で TR 中等度以下 81%、NYHA I/II 21%→75%、KCCQ +19 点")]

    y = 130
    for name, col, pop, res1, res2 in ROWS:
        h = 190
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.7, radius=10)
        cv.box(70, y, 340, h, fc="#fbfcfd", ec=col, lw=0, radius=10)
        cv.text(94, y + 62, name, size=fit(cv, name, 300, 11.8, "bold"),
                color=col, weight="bold", ha="left")
        cv.text(94, y + 108, pop, size=fit(cv, pop, 300, 9.8), color=GREY,
                ha="left")
        for j, ln in enumerate(cv.wrap(res1, W - 500, 10.8)):
            cv.text(430, y + 64 + LH(10.8, 1.5) * j, ln, size=10.8,
                    color=INK, ha="left")
        r1 = cv.wrap(res1, W - 500, 10.8)
        for j, ln in enumerate(cv.wrap(res2, W - 500, 10.2)):
            cv.text(430, y + 64 + LH(10.8, 1.5) * len(r1) + 18 + LH(10.2, 1.5) * j,
                    ln, size=10.2, color=GREY, ha="left")
        y += h + 16

    textbox(cv, 70, y + 10, W - 140,
            ["三尖弁の治療は、まず「症状と QOL が良くなる」ことから示された。",
             "死亡や入院に差が出るかどうかは、追跡期間を延ばして初めて見えてくる。",
             "麻酔科にとっての含意は、"
             "「この手技は生命予後を変えるために行うとは限らない」ということである。",
             "だからこそ、手技に伴う侵襲を最小にする意味が大きい。"],
            10.6, style="navy", title="何を目指した治療なのか",
            title_color=NAVY, pad_y=16)
    cv.save(P("n09_tteer.png"))
    crop_bottom(P("n09_tteer.png"))


# ---------------------------------------------------------------- n10
def n10():
    """経カテーテル三尖弁置換"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "三尖弁を「置換する」という選択肢")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 430

    def panel(x, title, sub, color, rows, note):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.box(x, PY, PW, 56, fc=color, ec=color, lw=0, radius=10)
        cv.text(x + PW / 2, PY + 28, title,
                size=fit(cv, title, PW - 40, 12.2, "bold"), color="white",
                weight="bold")
        cv.text(x + PW / 2, PY + 86, sub, size=fit(cv, sub, PW - 60, 10.6),
                color=GREY)
        yy = PY + 130
        for lab, val in rows:
            cv.text(x + 40, yy, lab, size=10.4, color=INK, ha="left")
            cv.text(x + PW - 40, yy, val, size=13.0, color=color, ha="right",
                    weight="bold")
            yy += 46
        for j, ln in enumerate(cv.wrap(note, PW - 80, 10.2)):
            cv.text(x + PW / 2, PY + PH - 60 + LH(10.2, 1.5) * j, ln,
                    size=10.2, color=color, weight="bold")

    panel(x1, "TRISCEND II（2025）", "重症 TR 400 例（置換 267／対照 133）",
          BLUE,
          [("1 年の win ratio", "2.02"),
           ("95%CI", "1.56-2.62"),
           ("p 値", "<0.001")],
          "無作為化試験で有効性を示した")

    panel(x2, "TVT レジストリ（2026）", "実臨床 1,034 件（82 施設・平均 77.1 歳）",
          GREEN,
          [("植込み成功", "98.4%"),
           ("30 日死亡", "3.1%"),
           ("新規 CIED（未植込み例）", "15.9%")],
          "成功率は高いが、伝導障害の頻度に注意")

    th = textbox(cv, 70, PY + PH + 26, W - 140,
                 ["三尖弁置換で特徴的なのは、新規のデバイス植込みが 15.9% に生じることである。",
                  "三尖弁輪の直下を刺激伝導系が走っているためで、"
                  "大動脈弁の TAVI と同じ構造の問題である。",
                  "術前に一時ペーシングの経路を確保しておくかどうかを、"
                  "チームで決めておく必要がある。"],
                 10.6, style="red", title="麻酔科が備えること",
                 title_color=RED, pad_y=16)
    cv.save(P("n10_ttvr.png"))
    crop_bottom(P("n10_ttvr.png"))


# ---------------------------------------------------------------- n11
def n11():
    """右室不全のスパイラルと管理目標"""
    cv = Canvas(W, 1600)
    cap(cv, 44, "右室が破綻するとき、何が起きているのか")

    cx, cy = 430, 380
    SP = [("右室が拡大する", -1, -1), ("心室中隔が左室を圧排する", 1, -1),
          ("左室の充満が減る", 1, 1), ("体血圧が下がる", 0, 1.35),
          ("右冠動脈の灌流が減る", -1, 1), ("右室の収縮が落ちる", -1, 0)]
    R = 250
    import math
    pts = []
    for i, (lab, dx, dy) in enumerate(SP):
        ang = -math.pi / 2 + 2 * math.pi * i / len(SP)
        x = cx + R * math.cos(ang)
        y = cy + R * math.sin(ang)
        pts.append((x, y, lab))
    for i, (x, y, lab) in enumerate(pts):
        cv.box(x - 130, y - 34, 260, 68, fc="#fceeec", ec=RED, lw=1.6,
               radius=8)
        cv.text(x, y, lab, size=fit(cv, lab, 240, 10.0), color=INK)
        x2, y2, _ = pts[(i + 1) % len(pts)]
        cv.arrow((x + (x2 - x) * 0.30, y + (y2 - y) * 0.30),
                 (x + (x2 - x) * 0.70, y + (y2 - y) * 0.70),
                 color="#d98e8e", lw=2.0, head=10)
    cv.text(cx, cy, "右室不全の\nスパイラル", size=13.0, color=RED,
            weight="bold")

    RX = 810
    RW = W - 70 - RX
    ITEMS = [("前負荷", BLUE, "#eaf1f8",
              ["足りなければ充満しない", "多すぎれば右室がさらに広がる",
               "「とりあえず輸液」は危険"]),
             ("肺血管抵抗", GREEN, "#eaf5ee",
              ["低酸素・高二酸化炭素・アシドーシスを避ける",
               "無気肺と過膨張のどちらも抵抗を上げる"]),
             ("体血圧", RED, "#fceeec",
              ["右冠動脈の灌流圧を保つ", "低血圧はそれ自体が悪循環の入口"]),
             ("収縮力とリズム", PURPLE, "#f1ecf8",
              ["強心薬の使いどころ", "洞調律と房室同期を保つ"])]
    y = 140
    for t, col, fc, lines in ITEMS:
        h = card(cv, RX, y, RW, t, lines, col, fc, body_size=10.0, lh=1.75)
        y += h + 20

    ty = max(700, y + 16)
    th = textbox(cv, 70, ty, W - 140,
                 ["肺高血圧と右心不全の周術期管理については、"
                  "国際心肺移植学会の合意文書（2022 年）と",
                  "英国麻酔科学会誌の系統的レビュー・専門家合意（2021 年）がある。",
                  "三尖弁のインターベンションは、"
                  "これらの患者管理を数時間にわたって行う場面である。"],
                 10.6, style="navy", title="依拠できる文書",
                 title_color=NAVY, pad_y=16)

    msg(cv, ty + th + 28,
        "右室は「押せば出る」臓器ではない。四つの条件を同時に整える",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("n11_rv_failure.png"))
    crop_bottom(P("n11_rv_failure.png"))


# ---------------------------------------------------------------- n12
def n12():
    """CIED リードと三尖弁"""
    cv = Canvas(W, 900)
    cap(cv, 44, "弁を跨ぐリードを、どう扱うか")

    OPT = [("リードを残したまま治療する", BLUE, "#eaf1f8",
            ["もっとも侵襲が小さい", "リードが接合の邪魔になることがある",
             "デバイスがリードを挟み込む可能性"]),
           ("リードを抜去してから治療する", RED, "#fceeec",
            ["抜去そのものが大血管手術である（第Ⅰ章）",
             "ペーシング依存なら代替手段が要る", "感染例では抜去が前提になる"]),
           ("リードを跨いで弁を留置する", PURPLE, "#f1ecf8",
            ["レジストリで成績が報告され始めた", "リードの機能への影響を追跡する",
             "施設の経験に依存する"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(OPT):
        card(cv, 70 + (w + 30) * i, 140, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    th = textbox(cv, 70, 460, W - 140,
                 ["この判断は、循環器内科・不整脈チーム・心臓外科・麻酔科の"
                  "合議事項である。",
                  "近年は heart team アプローチとして明文化されつつあり、"
                  "リードを跨いだ弁置換のレジストリも報告されている。",
                  "麻酔科が確認すべきことは一つ。"
                  "「この患者はペーシング依存か」である。"],
                 10.8, style="navy", title="誰が決めるのか",
                 title_color=NAVY, pad_y=16)

    msg(cv, 460 + th + 28,
        "第Ⅰ章（CIED）と第Ⅴ章（三尖弁）は、この一点で交差する")
    cv.save(P("n12_lead_tricuspid.png"))
    crop_bottom(P("n12_lead_tricuspid.png"))


# ---------------------------------------------------------------- n13
def n13():
    """Alg5-1 TAVI の麻酔法"""
    cv = Canvas(W, 1800)
    cap(cv, 44, "アルゴリズム 1　TAVI の麻酔法を決める")

    cx = W / 2
    bw = 800
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["経大腿アクセスか、それ以外か（経心尖・経大動脈・経鎖骨下）",
              "弁尖切開や valve-in-valve を併用するか",
              "施設の手技時間はどれくらいか"],
             style="navy", title="① 手技の条件", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["仰臥位で静かにしていられるか（認知症・体動・起坐呼吸）",
              "呼吸予備能はどうか",
              "大動脈弁狭窄そのものによる循環予備能の乏しさ"],
             style="red", title="② 患者の条件", title_color=RED)
    y += h
    down(cv, cx, y, y + 50)
    y += 50
    cw = 520
    lx, rx = 70, W - 70 - cw
    side(cv, cx - 40, lx + cw + 10, y + 74)
    side(cv, cx + 40, rx - 10, y + 74)
    hl = step(cv, lx, y, cw,
              ["経大腿・単純な症例",
               "協力が得られ、体動が少ない",
               "→ 局所麻酔＋鎮静",
               "→ 覚醒下なら神経所見で脳卒中に気づける"],
              style="green", title="局所麻酔と鎮静", title_color=GREEN)
    hr = step(cv, rx, y, cw,
              ["経心尖・経大動脈などの外科的アクセス",
               "弁尖切開や複雑な併用手技",
               "体動が抑えられない、気道が危うい",
               "→ 全身麻酔（TEE も使いやすい）"],
              style="blue", title="全身麻酔", title_color=BLUE)
    y += max(hl, hr)
    down(cv, lx + cw / 2, y, y + 44)
    down(cv, rx + cw / 2, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["一時ペーシングの経路（rapid pacing と術後の徐脈に備える）",
              "動脈圧ラインと、急速輸血に耐える静脈路",
              "体外循環・外科的バックアップの待機状況",
              "鎮静でも、全身麻酔へ移行できる準備"],
             style="amber", title="③ どちらでも必要な準備",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["術後の伝導障害は数日後に出ることがある",
          "ペーシングをいつまで確保しておくかを決めておく",
          "早期離床・早期退院の流れに、監視の計画を合わせる"],
         style="purple", title="④ 術後の決めごと", title_color=PURPLE)
    cv.save(P("n13_alg_tavi_anesthesia.png"))
    crop_bottom(P("n13_alg_tavi_anesthesia.png"))


# ---------------------------------------------------------------- n14
def n14():
    """Alg5-2 TAVI 術中の急変"""
    cv = Canvas(W, 1800)
    cap(cv, 44, "アルゴリズム 2　TAVI 術中に血圧が下がった")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["いま手技のどの段階か（ワイヤ通過・rapid pacing・弁の展開・止血）",
              "rapid pacing 直後なら、まず回復を待つ（戻らなければ異常）"],
             style="navy", title="① 段階を確認する", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 50)
    y += 50
    cw = 340
    gap = (W - 140 - cw * 3) / 2
    LABS = [("心電図が変化した", RED, "#fceeec",
             ["冠動脈閉塞を疑う", "ST 変化・心室性不整脈",
              "ただちに術者へ伝える"]),
            ("心嚢液が出た", RED, "#fceeec",
             ["弁輪破裂・穿孔を疑う", "心タンポナーデとして対応",
              "外科と体外循環を呼ぶ"]),
            ("徐脈になった", PURPLE, "#f1ecf8",
             ["完全房室ブロックを疑う", "一時ペーシングを作動させる",
              "薬剤より確実な手段を先に"])]
    for i, (t, col, fc, lines) in enumerate(LABS):
        x = 70 + (cw + gap) * i
        cv.arrow((cx, y - 12), (x + cw / 2, y + 14), color="#b9c2cc", lw=1.6,
                 head=8)
        card(cv, x, y + 18, cw, t, lines, col, fc, body_size=10.0, lh=1.8)
    y += 18 + 250
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["どれにも当てはまらないなら、出血を疑う",
              "穿刺部・後腹膜・大動脈の損傷",
              "術野では見えない。Hb・腹部・血管エコーで探す"],
             style="orange" if False else "amber",
             title="② 見えないところの出血", title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["鎮静で行っている場合、意識レベルの変化は脳卒中のサインでもある",
          "「反応が鈍い」を鎮静深度のせいだけにしない",
          "神経所見を確認できることは、鎮静で行うことの利点である"],
         style="blue", title="③ 鎮静症例での追加の視点", title_color=BLUE)
    cv.save(P("n14_alg_tavi_emergency.png"))
    crop_bottom(P("n14_alg_tavi_emergency.png"))


# ---------------------------------------------------------------- n15
def n15():
    """Alg5-3 三尖弁インターベンションの周術期"""
    cv = Canvas(W, 1800)
    cap(cv, 44, "アルゴリズム 3　三尖弁インターベンションの周術期")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["右室機能と肺高血圧の程度（この手技の予後を決める）",
              "肝機能・凝固・腹水（うっ血がどこまで進んでいるか）",
              "腎機能と利尿薬への反応",
              "CIED のリードが弁を跨いでいないか、ペーシング依存か"],
             style="navy", title="① 術前に確認すること", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["長時間の経食道心エコーが必要（多くは全身麻酔）",
              "陽圧換気は前負荷を下げ、肺血管抵抗を上げうる",
              "低酸素・高二酸化炭素・アシドーシスを避ける",
              "腹水がある患者では、換気条件そのものが難しい"],
             style="red", title="② 麻酔導入と換気", title_color=RED)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["逆流が減ると、右室の後負荷が上がる",
              "右室が耐えられるかを、留置ごとに評価する",
              "前負荷・肺血管抵抗・体血圧・収縮力の四つを同時に整える",
              "「輸液で埋める」という反射を避ける"],
             style="amber", title="③ 逆流を減らした瞬間",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["三尖弁置換では新規のデバイス植込みが 15.9% に生じた",
              "術中・術後の徐脈に備え、ペーシングの経路を決めておく",
              "抜管後も、伝導障害の出現を監視する"],
             style="purple", title="④ 伝導障害への備え", title_color=PURPLE)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["この治療の主な目的は症状と QOL の改善である",
          "手技の侵襲を最小にすることが、そのまま治療目的に沿う",
          "術後はうっ血の改善（体重・腹囲・肝機能）を追う"],
         style="green", title="⑤ 何のための治療かを忘れない",
         title_color=GREEN)
    cv.save(P("n15_alg_tricuspid.png"))
    crop_bottom(P("n15_alg_tricuspid.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (n08, n09, n10, n11, n12, n13, n14, n15):
        fn()
        print("ok", fn.__name__)
