# -*- coding: utf-8 -*-
"""第22巻 図版 f11〜f20"""
import os
from figlib import (Canvas, textbox, NAVY, INK, GREY, RED, GREEN, FILL)
from trimfig import trim_bottom

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "図版")
os.makedirs(OUT, exist_ok=True)
W = 2000


def save(cv, name):
    path = os.path.join(OUT, name)
    cv.save(path)
    trim_bottom(path)
    print("  ", name)


# ---------------------------------------------------------------- f11
def f11():
    cv = Canvas(W, 1500)
    cv.title(40, 52, "lethal diamond ── 四つが互いを悪化させる")

    cx, cy, r = 1000, 580, 330
    nodes = [(cx, cy - r, "低体温", ["凝固酵素は 37℃ を前提に", "活性が決まっている"], "blue"),
             (cx + r + 120, cy, "低カルシウム", ["クエン酸が Ca を奪う", "心収縮も凝固も落ちる"], "purple"),
             (cx, cy + r, "アシドーシス", ["pH 7.2 以下で", "凝固反応が失速する"], "amber"),
             (cx - r - 120, cy, "希釈・消費", ["フィブリノゲンと", "血小板が足りない"], "red")]
    for x, y, t, lines, st in nodes:
        textbox(cv, x - 280, y - 105, 560, lines, 12.5, style=st, title=t,
                title_size=16, pad_y=18, min_h=200)

    # 循環する矢印
    for a, b in [((cx + 180, cy - r + 110), (cx + r - 30, cy - 120)),
                 ((cx + r - 30, cy + 120), (cx + 180, cy + r - 110)),
                 ((cx - 180, cy + r - 110), (cx - r + 30, cy + 120)),
                 ((cx - r + 30, cy - 120), (cx - 180, cy - r + 110))]:
        cv.arrow(a, b, color=RED, lw=3, head=18)

    textbox(cv, cx - 155, cy - 66, 310, ["出　血"], 19, style="grey",
            pad_y=26, fc="#ffffff", ec="#8d97a3")

    y2 = cy + r + 150
    textbox(cv, 40, y2, 940,
            ["どれか一つを直しても、残り三つが引き戻す。",
             "だから同時に、しかも予防的に直す。",
             "「出血が落ち着いてから体温を上げよう」では手遅れになる。"],
            13, style="navy", title="輪は同時に断つ", title_size=15, pad_y=20)
    textbox(cv, 1020, y2, 940,
            ["出血が多いのに昇圧薬が効かない",
             "──このときの鑑別第一位は低カルシウムである。",
             "総カルシウムや補正値ではなく、",
             "血液ガスのイオン化カルシウムで見る。"],
            13, style="purple", title="効かないときに疑うもの", title_size=15,
            pad_y=20)
    save(cv, "f11_lethal_diamond.png")


# ---------------------------------------------------------------- f12
def f12():
    cv = Canvas(W, 1750)
    cv.title(40, 52, "止血のエスカレーション ── 段を飛ばしてよい場面がある")

    steps = [("① 子宮収縮薬", ["オキシトシン／メチルエルゴメトリン／プロスタグランジン",
                           "まず子宮を縮める。ここが効けば大半は止まる"], "green"),
             ("② 双手圧迫・子宮内バルーン", ["物理的に圧迫する。時間を稼ぐ手段でもある",
                                  "効かないと分かるまでに時間をかけすぎない"], "blue"),
             ("③ 子宮圧迫縫合", ["B-Lynch など。子宮を残す前提の手技",
                           "凝固が破綻していると縫合部からも出血する"], "amber"),
             ("④ 動脈塞栓術（IR）", ["血管内治療室まで患者を動かせるかが条件",
                              "循環が不安定なら選べない"], "purple"),
             ("⑤ 子宮摘出", ["出血源と凝固因子消費の場を、まとめて取り除く",
                        "敗北ではなく、救命の手段である"], "red")]
    y = 170
    for t, lines, st in steps:
        h = textbox(cv, 40, y, 1250, lines, 13, style=st, title=t,
                    title_size=16, pad_y=20)
        cv.arrow((660, y + h + 4), (660, y + h + 44), color=GREY, lw=2.4,
                 head=14) if t != "⑤ 子宮摘出" else None
        y += h + 48

    textbox(cv, 1330, 170, 630,
            ["次の三つがそろったら、",
             "順番どおりに上がっている余裕はない。",
             "",
             "・製剤を入れてもフィブリノゲンが上がらない",
             "・大量輸血を回しても止血できない",
             "・乳酸が上がり、pH が下がり、",
             "　昇圧薬から離脱できない",
             "",
             "このとき③④を飛ばして⑤へ進む判断が、",
             "母体を救う。"],
            13, style="red", title="段を飛ばす条件", title_size=16, pad_y=22)

    textbox(cv, 1330, 780, 630,
            ["Couvelaire uterus は所見であって、",
             "子宮摘出の適応ではない。",
             "",
             "紫青色に見えても、収縮が得られれば",
             "子宮は残せる。",
             "",
             "判断材料は色ではなく、",
             "「縮むか」と「固まるか」である。"],
            13, style="grey", title="色で決めない", title_size=16, pad_y=22)

    textbox(cv, 40, y + 20, W - 80,
            ["決めておくべきは順番そのものではなく、「次の段へ上がる判断を、誰が、何分後に下すか」である。",
             "時間を決めずに同じ手技を続けることが、最も多い失敗の形である。"],
            13.5, style="navy", pad_y=20)
    save(cv, "f12_escalation.png")


# ---------------------------------------------------------------- f13
def f13():
    cv = Canvas(W, 1550)
    cv.title(40, 52, "投与量の設計 ── 「3 g で 100 上がる」は妊婦では過大評価")

    textbox(cv, 40, 165, 940,
            ["血漿量 2.5–3.0 L（非妊娠成人）",
             "3 g ÷ 2.8 L ≒ 107 mg/dL",
             "",
             "教科書の「3 g で約 100 mg/dL」は",
             "この前提で書かれている。"],
            13.5, style="grey", title="非妊娠時の計算", title_size=16,
            pad_y=22, min_h=330)
    textbox(cv, 1020, 165, 940,
            ["血漿量 3.5–4.0 L（妊娠末期は約 1.5 倍）",
             "3 g ÷ 3.8 L ≒ 79 mg/dL",
             "",
             "消費も希釈もない理想状態で、これである。",
             "実際にはこれを下回る。"],
            13.5, style="red", title="妊娠末期の計算", title_size=16,
            pad_y=22, min_h=330)

    y = 578
    textbox(cv, 40, y, W - 80,
            ["必要量（mg/kg）　＝　［ 目標 Fbg − 現在 Fbg（mg/dL）］　÷　1.7"],
            18, style="blue", title="国際的に用いられる投与量計算式", title_size=16,
            pad_y=26)

    y2 = y + 210
    h13 = textbox(cv, 40, y2, 940,
            ["体重 70 kg、現在 100 mg/dL、目標 200 mg/dL",
             "（200 − 100）÷ 1.7 ＝ 59 mg/kg",
             "59 mg/kg × 70 kg ＝ 4.1 g"],
            14, style="amber", title="計算してみる", title_size=16, pad_y=22,
            min_h=280)
    h13 = max(h13, textbox(cv, 1020, y2, 940,
            ["理論上、すでに 3 g では足りない。",
             "",
             "「3 g 入れたのに上がらない」の原因の一つは、",
             "消費でも希釈でもなく、単純な投与量不足である。",
             "まずそれを疑う。"],
            14, style="red", title="ここから分かること", title_size=16,
            pad_y=22, min_h=280))

    textbox(cv, 40, y2 + h13 + 46, W - 80,
            ["投与したら必ず再検する。上がり方が計算より悪ければ、出血が続いているか、消費が止まっていない。",
             "実際の投与量・投与法は添付文書と施設の使用基準に従うこと。本図は考え方を示したものである。"],
            13, style="navy", pad_y=20)
    save(cv, "f13_dose.png")


# ---------------------------------------------------------------- f14
def f14():
    cv = Canvas(W, 1250)
    cv.title(40, 52, "新鮮凍結血漿でフィブリノゲンは上がらない ── 算数で確かめる")

    textbox(cv, 40, 165, W - 80,
            ["現在 Fbg 100 mg/dL ／ 血漿量 3.5 L ／ FFP の Fbg 濃度 200 mg/dL",
             "ここに FFP を 1 L 投与すると──",
             "（100 × 3.5 ＋ 200 × 1.0）÷（3.5 ＋ 1.0）　＝　122 mg/dL"],
            15, style="blue", title="前提と計算", title_size=16, pad_y=24)

    y = 520
    textbox(cv, 40, y, 620, ["1 L 投与して", "＋22 mg/dL"], 17, style="red",
            title="FFP", title_size=17, pad_y=24, min_h=250)
    textbox(cv, 690, y, 620, ["容量負荷が小さく", "確実に上がる"], 15,
            style="green", title="フィブリノゲン濃縮製剤", title_size=17,
            pad_y=24, min_h=250)
    textbox(cv, 1340, y, 620, ["高濃度・少容量", "院内調製の含有量に幅がある"], 14,
            style="amber", title="クリオプレシピテート", title_size=17,
            pad_y=24, min_h=250)

    textbox(cv, 40, y + 300, W - 80,
            ["しかも実際には、投与している間も出血で失われるので、これを下回る。",
             "FFP は「複数の凝固因子を補う」ためには有効だが、"
             "「低フィブリノゲン血症を是正する」ためには数学的に不向きである。",
             "この一点が腑に落ちれば、なぜ濃縮製剤やクリオが要るのかを説明する必要はなくなる。"],
            13.5, style="navy", title="結論", title_size=16, pad_y=20)
    save(cv, "f14_ffp_math.png")


# ---------------------------------------------------------------- f15
def f15():
    cv = Canvas(W, 1700)
    cv.title(40, 52, "大量輸血戦略の振り子 ── 50 年で 4 回振れた")

    eras = [("〜1970年代", "全　血", ["失ったものと同じものを入れる",
                                 "最も単純で、最も生理学的だった"],
             "供給と保存の制約", "green"),
            ("1980–2000年代", "成分輸血＋検査待ち", ["必要なものを必要なだけ",
                                            "効率的で合理的に見えた"],
             "待つ間に凝固が破綻する", "grey"),
            ("2000年代後半〜", "固定比率（1:1:1）", ["検査を待たず比率で入れる",
                                             "全血の再発明だった"],
             "必要のない人にも入れる", "blue"),
            ("2010年代〜", "粘弾性検査で個別化", ["足りないものを、足りないだけ",
                                         "FFP を減らして成績が上がった"],
             "機器がない施設で成立しない", "red")]
    y = 170
    for era, title, lines, weak, st in eras:
        cv.text(40, y + 60, era, size=12.5, color=GREY, ha="left",
                weight="bold")
        h = textbox(cv, 440, y, 900, lines, 13, style=st, title=title,
                    title_size=16, pad_y=20, min_h=185)
        textbox(cv, 1370, y, 590, [weak], 12.5, style="grey",
                title="弱点", title_size=13, title_color=GREY, pad_y=18,
                min_h=185)
        y += h + 30

    y += 20
    textbox(cv, 40, y, W - 80,
            ["両端が言っていることは、実は同じである。",
             "足りないものを、足りないだけ、間に合ううちに入れる。",
             "1960 年代に全血でやっていたことを、いま粘弾性検査でやっている。道具が変わっただけである。"],
            14, style="navy", title="振り子はどこへ行ったか", title_size=16,
            pad_y=22)
    save(cv, "f15_mtp_history.png")


# ---------------------------------------------------------------- f16
def f16():
    cv = Canvas(W, 1450)
    cv.title(40, 52, "術後最初の 6 時間 ── 何を、どこまで戻すか")

    rows = [("平均血圧", "≧ 65 mmHg", "臓器灌流。妊娠高血圧症候群合併例は個別化する", "blue"),
            ("乳　酸", "< 2.0 mmol/L\nまたは初回値から 50% 低下", "戻らない乳酸は、見えていない出血か低灌流である", "red"),
            ("ベースエクセス", "> −5 mEq/L", "アシドーシスは凝固を止める", "amber"),
            ("尿　量", "≧ 0.5 mL/kg/h", "腎皮質壊死を早く捕まえる", "green"),
            ("体　温", "≧ 36.0 ℃", "凝固酵素の活性は温度に依存する", "blue"),
            ("イオン化 Ca", "≧ 1.0 mmol/L", "大量輸血中は反復測定する", "purple"),
            ("ヘモグロビン", "7–9 g/dL", "出血が止まった後の目標", "grey"),
            ("血小板", "≧ 50,000/μL（出血中）", "止血後は 30,000 でよい", "grey"),
            ("フィブリノゲン", "≧ 200 mg/dL（出血中）", "止血後は 150 を下回らせない", "red")]
    y = 165
    for lab, tgt, note, st in rows:
        lines = tgt.split("\n")
        rh = 92 if len(lines) == 1 else 124      # 2行のセルは行高を広げる
        cv.rect(40, y, 400, rh, fc=FILL[st][1])
        cv.text(240, y + rh / 2, lab, size=14.5, color="white",
                weight="bold", z=6)
        cv.rect(452, y, 560, rh, fc=FILL[st][0], ec=FILL[st][1], lw=1.3)
        cv.block(468, y + rh / 2 - 27 * len(lines), 528, lines, 13.5,
                 color=FILL[st][1], weight="bold")
        cv.text(1036, y + rh / 2, note, size=12.5, color=INK, ha="left")
        y += rh + 10

    textbox(cv, 40, y + 20, W - 80,
            ["これは「正常値に戻す」ための表ではなく、「ここまで戻っていなければ何かが続いている」を見るための表である。",
             "乳酸が下がらない、イオン化 Ca が上がらない、フィブリノゲンが維持できない──いずれも出血の継続を示唆する。"],
            13.5, style="navy", pad_y=20)
    save(cv, "f16_gdt.png")


# ---------------------------------------------------------------- f17
def f17():
    cv = Canvas(W, 1200)
    cv.title(40, 52, "術後合併症は、時間差で現れる")

    x0, x1 = 490, 1930

    def px(h):
        return x0 + (x1 - x0) * (h ** 0.5) / (720 ** 0.5)

    lanes = [("進行性DIC・再出血", 0, 24, "red"),
             ("低カルシウム・低体温", 0, 12, "purple"),
             ("TRALI・TACO", 2, 24, "blue"),
             ("急性腎障害", 6, 168, "amber"),
             ("ARDS", 12, 168, "blue"),
             ("静脈血栓塞栓症", 24, 720, "green"),
             ("Sheehan 症候群", 24, 720, "grey")]
    y = 190
    for lab, a, b, st in lanes:
        cv.text(470, y + 30, lab, size=13.5, color=FILL[st][1],
                weight="bold", ha="right")
        cv.rect(px(max(a, 0.3)), y, px(b) - px(max(a, 0.3)), 60,
                fc=FILL[st][0], ec=FILL[st][1], lw=1.5)
        y += 80

    yb = y + 10
    cv.rect(x0, yb, x1 - x0, 4, fc="#8d97a3")
    for h, lab in ((0.3, "直後"), (6, "6 時間"), (24, "1 日"),
                   (72, "3 日"), (168, "1 週"), (720, "1 か月")):
        cv.rect(px(h), yb - 8, 2, 22, fc="#556070")
        cv.text(px(h), yb + 46, lab, size=12.5, color=INK)

    textbox(cv, 40, yb + 100, 940,
            ["「バイタルが安定したから一般病棟へ」が最も危ない。",
             "術中に Fbg < 150、大量輸血、昇圧薬使用のいずれかがあれば、",
             "最低 24 時間は ICU／HCU で管理する。"],
            13, style="red", title="早すぎる離脱", title_size=15, pad_y=20)
    textbox(cv, 1020, yb + 100, 940,
            ["出血で死ぬのを防いだ患者が、",
             "1 週間後に肺塞栓で死ぬ。",
             "これが早剝管理の最後の落とし穴である。",
             "止血した瞬間から、血栓の側を考え始める。"],
            13, style="green", title="最後の落とし穴", title_size=15, pad_y=20)
    save(cv, "f17_postop_timeline.png")


# ---------------------------------------------------------------- f18
def f18():
    cv = Canvas(W, 2400)
    cv.title(40, 52, "早剝の周術期管理 ── 全体像")

    def band(y, title, lines, st, h=None):
        return textbox(cv, 40, y, W - 80, lines, 13, style=st, title=title,
                       title_size=16, pad_y=20, min_h=h)

    y = 165
    for title, lines, st in [
        ("Ⅰ　連絡を受けた時点", [
            "太い静脈路 2 本（16 G 以上）／観血的動脈圧ライン／加温装置／急速輸液装置",
            "血算・PT・APTT・フィブリノゲン・FDP・D-dimer・血液ガス（乳酸・イオン化 Ca）",
            "輸血部へ連絡し、赤血球・新鮮凍結血漿・血小板・フィブリノゲン製剤の所在を確認する",
            "産科・輸血部・臨床工学技士・看護師に「大量出血症例として動く」と宣言する"], "blue"),
        ("Ⅱ　麻酔法の決定", [
            "凝固が区域麻酔に耐えるかを先に問う（血小板・Fbg・PT-INR・出血の持続）",
            "不明なら全身麻酔。迅速導入。ただしショックでは通常量の導入薬を使わない",
            "導入前に昇圧薬を走らせ、輸血をつなぎ、子宮左方転位を確実にする"], "amber"),
        ("Ⅲ　娩出と同時に進める治療", [
            "出血量・子宮収縮・フィブリノゲン・乳酸・イオン化 Ca・体温を並行して追う",
            "Fbg < 200 で補充を準備、< 150 で投与する。粘弾性検査があれば FIBTEM A5 で先回りする",
            "赤血球だけを入れ続けない。新鮮凍結血漿・血小板・フィブリノゲンを組み合わせる",
            "低体温・アシドーシス・低カルシウムを、同時に、予防的に直す"], "red"),
        ("Ⅳ　止血", [
            "子宮収縮薬 → 双手圧迫・子宮内バルーン → 圧迫縫合 → 動脈塞栓術 → 子宮摘出",
            "「次の段へ上がる判断を、誰が、何分後に下すか」を先に決めておく",
            "製剤を入れても Fbg が上がらないなら、段を飛ばす"], "purple"),
        ("Ⅴ　術後", [
            "大量輸血・Fbg < 150・ショック・昇圧薬使用のいずれかがあれば ICU／HCU へ",
            "最初の 6 時間：平均血圧 ≧ 65、乳酸 < 2.0、尿量 ≧ 0.5 mL/kg/h、体温 ≧ 36℃",
            "止血後は血栓の側へ視点を移す。間欠的空気圧迫を即日、薬物予防は凝固回復後に判断する",
            "硬膜外カテーテルは凝固が戻るまで抜かない。抜去後 12 時間は神経学的観察を続ける"], "green")]:
        h = band(y, title, lines, st)
        y += h + 26

    textbox(cv, 40, y + 14, W - 80,
            ["早剝の帝王切開は「児を早く出す手術」ではない。",
             "「児を娩出しながら、母体の播種性血管内凝固を同時に治療する手術」である。"],
            15, style="navy", pad_y=24)
    save(cv, "f18_overall.png")


# ---------------------------------------------------------------- f19
def f19():
    cv = Canvas(W, 1700)
    cv.title(40, 52, "早剝と凝固障害 ── 発見の 120 年")

    items = [("1901", "DeLee", ["早剝の患者が「血が固まらずに」死亡した 1 例を報告。",
                                "消費性凝固障害の、人類最初の記載である。"], "red"),
             ("1911", "Couvelaire", ["子宮筋層に血液が浸潤する所見を記載し、",
                                     "「子宮胎盤卒中」と名づけた。摘出の適応とは書かなかった。"], "purple"),
             ("1930–50s", "Dieckmann／Schneider", ["早剝でフィブリノゲンが著明に低下することを実測。",
                                                "胎盤由来の「トロンボプラスチン」説を提唱した。"], "amber"),
             ("1950s", "Ratnoff／Pritchard", ["分娩時の低フィブリノゲン血症を系統的に記述。",
                                              "「出血したから足りない」から「凝固が起きたから枯れた」へ。"], "blue"),
             ("1960s", "Parkland", ["新鮮全血の大量投与と子宮温存で母体死亡率を下げた。",
                                    "理論ではなく経験で、いまと同じ結論に到達していた。"], "green"),
             ("2000s–", "現代", ["「トロンボプラスチン」は組織因子と呼ばれ、",
                               "「固まらない血」は FIBTEM A5 として 5 分で数値化される。"], "navy")]
    x0 = 300
    cv.rect(x0 - 4, 155, 6, 140 * len(items) - 40, fc="#c8d0da")
    y = 165
    for yr, who, lines, st in items:
        cv.text(270, y + 62, yr, size=16, color=NAVY, weight="bold", ha="right")
        cv.rect(x0 - 18, y + 52, 34, 20, fc=FILL[st][1])
        h = textbox(cv, x0 + 40, y, W - x0 - 80, lines, 13, style=st,
                    title=who, title_size=15, pad_y=18, min_h=124)
        y += max(h, 124) + 26

    textbox(cv, 40, y + 14, W - 80,
            ["DeLee が 1901 年に書いた一文は、まだ古くなっていない。",
             "── 見えている出血より先に、血液そのものが変質している。"],
            14.5, style="navy", pad_y=24)
    save(cv, "f19_history.png")


# ---------------------------------------------------------------- f20
def f20():
    cv = Canvas(W, 1800)
    cv.title(40, 52, "日本のフィブリノゲン製剤 ── 60 年の道のり")

    items = [("1964", "承認", ["プール血漿由来の非加熱製剤として承認され、",
                             "産科出血をはじめ止血目的で広く使われた。"], "grey"),
             ("1977", "米国は承認取消", ["FDA が肝炎感染リスクを理由に承認を取り消す。",
                                    "日本では、その後も使用が続いた。"], "amber"),
             ("1980年代", "薬害肝炎", ["出産時に投与された女性たちに C 型肝炎の集団感染。",
                                   "1988 年に非加熱製剤が回収された。"], "red"),
             ("2008", "救済法", ["薬害肝炎救済法が成立。",
                               "適応は先天性低フィブリノゲン血症に限定されていた。"], "purple"),
             ("空白の約20年", "クリオを自分で作る時代", ["現場は FFP の大量投与か院内クリオ調製しか選べなかった。",
                                             "日本の施設が院内調製に習熟しているのは、この制約の産物である。"], "blue"),
             ("2020年代", "適応追加", ["ウイルス不活化を経た製剤に、",
                                  "産科危機的出血に伴う後天性低フィブリノゲン血症の適応が追加された。"], "green")]
    x0 = 380
    cv.rect(x0 - 4, 155, 6, 150 * len(items) - 50, fc="#c8d0da")
    y = 165
    for yr, who, lines, st in items:
        cv.text(350, y + 62, yr, size=15, color=NAVY, weight="bold", ha="right")
        cv.rect(x0 - 18, y + 52, 34, 20, fc=FILL[st][1])
        h = textbox(cv, x0 + 40, y, W - x0 - 80, lines, 13, style=st,
                    title=who, title_size=15, pad_y=18, min_h=124)
        y += max(h, 124) + 26

    textbox(cv, 40, y + 14, W - 80,
            ["使用条件が厳しいのは、規制当局が慎重すぎるからではない。過去に多数の患者が肝炎になったからである。",
             "同時に、必要な患者に投与しないこともまた害である。歴史が求めているのは忌避ではなく、",
             "適応の厳密さと、記録と、追跡可能性である。"],
            13.5, style="navy", pad_y=22)
    cv.text(40, y + 250,
            "※ 適応追加の正確な承認年月と現行の使用条件は、添付文書および行政通知の原本で確認すること。",
            size=11, color=GREY, ha="left")
    save(cv, "f20_jp_fibrinogen.png")


# ---------------------------------------------------------------- f21
def f21():
    cv = Canvas(W, 1600)
    cv.title(40, 52, "産科危機的出血への対応 ── 宣言の基準と、その後に同時に走るもの")

    y = 140
    h = textbox(cv, 40, y, W - 80,
                ["分娩後異常出血／出血が持続している　→　"
                 "ショックインデックス（SI）＝ 心拍数 ÷ 収縮期血圧 で出血量を見積もる",
                 "妊婦では SI 1 ≒ 1,500 mL、SI 1.5 ≒ 2,500 mL の出血量に相当すると推定される"],
                13.5, style="blue", pad_y=20)
    y += h + 16
    cv.arrow((1000, y), (1000, y + 40), color=GREY, lw=2.6, head=15)
    y += 50

    cv.text(40, y + 22, "宣言の基準 ── いずれか一つで足りる", size=15,
            color=NAVY, weight="bold", ha="left")
    y += 54
    cards = [("バイタルサイン異常", ["頻脈・末梢冷感"], "orange"),
             ("SI ≧ 1.5", ["約 2,500 mL の出血に相当"], "red"),
             ("産科DIC 8 点以上", ["早剝は入口で 4〜5 点"], "red"),
             ("フィブリノゲン < 150", ["単独で成立。出血量は問わない"], "purple")]
    cw = (W - 80 - 3 * 20) / 4
    hh = 0
    for i, (t, lines, st) in enumerate(cards):
        hh = max(hh, textbox(cv, 40 + i * (cw + 20), y, cw, lines, 12.5,
                             style=st, title=t, title_size=14, pad_y=18,
                             min_h=150))
    y += hh + 14
    cv.arrow((1000, y), (1000, y + 40), color=RED, lw=3, head=17)
    y += 50

    h = textbox(cv, 560, y, 880, ["「産科危機的出血」を宣言する"], 18,
                style="red", pad_y=22)
    y += h + 14
    cv.arrow((760, y), (640, y + 42), color=RED, lw=2.6, head=15)
    cv.arrow((1240, y), (1360, y + 42), color=RED, lw=2.6, head=15)
    y += 52

    h1 = textbox(cv, 40, y, 940,
                 ["赤血球・新鮮凍結血漿・血小板を固定比率で開始する",
                  "フィブリノゲン製剤／クリオを早期に組み込む",
                  "待てなければ O 型 RhD 陰性赤血球を考える"],
                 12.5, style="red", title="① 直ちに輸血を開始する",
                 title_size=15, pad_y=18)
    h2 = textbox(cv, 1020, y, 940,
                 ["自施設で対応できないと判断した時点で連絡する",
                  "動かせる状態にしてから動かす",
                  "搬送せずに済む場合もあるので、まず電話で相談する"],
                 12.5, style="blue", title="② 高次施設へ搬送する",
                 title_size=15, pad_y=18)
    y += max(h1, h2) + 26

    roles = [("産科", "amber"), ("麻酔科", "red"), ("救急科", "amber"),
             ("助産師・看護師", "amber"), ("集中治療部門", "amber"),
             ("輸血管理部門", "amber")]
    cv.text(40, y + 22, "動かす人 ── コマンダーを決め、並行して手配する",
            size=14, color=NAVY, weight="bold", ha="left")
    y += 50
    rw = (W - 80 - 5 * 14) / 6
    for i, (t, st) in enumerate(roles):
        x = 40 + i * (rw + 14)
        cv.rect(x, y, rw, 70, fc=FILL[st][0], ec=FILL[st][1],
                lw=2.4 if st == "red" else 1.3)
        cv.text(x + rw / 2, y + 35, t, size=13, color=FILL[st][1],
                weight="bold", z=6)
    y += 92

    cv.block(40, y, W - 80,
             ["出典：日本産科婦人科学会ほか5学会"
              "「産科危機的出血への対応指針2022」（2022年1月改訂）をもとに、",
              "麻酔科の視点で要点を図として再構成した。"],
             10.5, color=GREY, ha="left")
    save(cv, "f21_critical_hemorrhage.png")


# ---------------------------------------------------------------- f22
# 原典の表は解像度が低く判読できないため、全項目を組み直した自作の表。
DIC_COLS = [
    ("1. 基礎疾患", "該当するものを 1 つだけ選ぶ", "red", [
        ("sec", "1) 常位胎盤早期剝離", ""),
        ("row", "子宮硬直・児死亡", "5"),
        ("row", "子宮硬直・児生存", "4"),
        ("row", "超音波断層所見および CTG 所見における早剝の診断", "4"),
        ("sec", "2) 羊水塞栓症", ""),
        ("row", "急性肺性心", "4"),
        ("row", "人工換気", "3"),
        ("row", "補助呼吸", "2"),
        ("row", "酸素放流のみ", "1"),
        ("sec", "3) DIC 型後産期出血", ""),
        ("row", "子宮からの出血、または採血血液が低凝固性の場合", "4"),
        ("row", "2,000 mL 以上の出血（出血開始から 24 時間以内）", "3"),
        ("row", "1,000 mL 以上 2,000 mL 未満の出血（同上）", "1"),
        ("sec", "4) 子癇", ""),
        ("row", "子癇発作", "4"),
        ("sec", "5) その他", ""),
        ("row", "その他の基礎疾患", "1"),
    ]),
    ("2. 臨床症状", "", "amber", [
        ("sec", "1) 急性腎不全（1 つだけ選ぶ）", ""),
        ("row", "無尿（≦5 mL/時）", "4"),
        ("row", "乏尿（5〜≦20 mL/時）", "3"),
        ("sec", "2) 急性呼吸不全（羊水塞栓症を除く・1 つだけ選ぶ）", ""),
        ("row", "人工換気または時々の補助呼吸", "4"),
        ("row", "酸素放流のみ", "1"),
        ("sec", "3) 重篤な臓器障害（それぞれ加える・全て選ぶ）", ""),
        ("row", "心（ラ音または泡沫性の喀痰など）", "4"),
        ("row", "肝（可視黄疸など）", "4"),
        ("row", "脳（意識障害および痙攣など）", "4"),
        ("row", "消化管（壊死性腸炎など）", "4"),
        ("sec", "4) 出血傾向", ""),
        ("row", "肉眼的血尿・メレナ・紫斑・皮膚粘膜・歯肉・"
                "注射部位からの出血", "4"),
        ("sec", "5) その他（全て選ぶ）", ""),
        ("row", "脈拍 ≧100/分", "1"),
        ("row", "血圧 ≦90 mmHg（収縮期）または 40% 以上の低下", "1"),
        ("row", "冷汗", "1"),
        ("row", "蒼白", "1"),
    ]),
    ("3. 検査項目", "該当するものを全て選ぶ", "blue", [
        ("row", "血清 FDP ≧10 μg/mL", "1"),
        ("row", "血小板数 ≦10万/mm³", "1"),
        ("row", "フィブリノゲン ≦150 mg/dL", "1"),
        ("row", "プロトロンビン時間 ≧15 秒（≦50%）"
                "またはヘパプラスチンテスト ≦50%", "1"),
        ("row", "赤沈 ≦4 mm/15分 または ≦15 mm/時", "1"),
        ("row", "出血時間 ≧5 分", "1"),
        ("row", "その他の凝固・線溶・キニン系因子の異常"
                "（例：AT ≦18 mg/dL または ≦60%、プレカリクレイン、"
                "α2-PI、プラスミノゲン、その他の凝固因子 ≦50%）", "1"),
    ]),
]


def f22():
    CW_ = 630
    GAP = 25
    PAD = 14
    SZ = 11.0
    cv0 = Canvas(10, 10)                      # 行数の見積り用
    heights = []
    for _, _, _, rows in DIC_COLS:
        hh = 54
        for kind, label, _pt in rows:
            if kind == "sec":
                hh += 12 + 34 * len(cv0.wrap(label, CW_ - PAD * 2, 11.5))
            else:
                n = len(cv0.wrap(label, CW_ - 90 - PAD * 2, SZ))
                hh += max(46, n * 32 + 18)
        heights.append(hh)
    top = 160
    cv = Canvas(W, top + max(heights) + 430)
    cv.title(40, 52, "産科DIC診断基準 ── 全項目")
    cv.text(40, 100, "合計 8 点以上で DIC と判定する。"
                     "ただし検査項目（3）で 2 点以上が含まれること。",
            size=12.5, color=GREY, ha="left")

    for ci, (title, note, st, rows) in enumerate(DIC_COLS):
        x = 40 + ci * (CW_ + GAP)
        y = top
        cv.rect(x, y, CW_, 54, fc=FILL[st][1])
        cv.text(x + PAD, y + 27, title, size=13.5, color="white",
                weight="bold", ha="left", z=6)
        if note:
            cv.text(x + CW_ - PAD, y + 27, note, size=10.5, color="white",
                    ha="right", z=6)
        cv.rect(x + CW_ - 88, y, 2, 54, fc="white")
        y += 54
        for kind, label, pt in rows:
            if kind == "sec":
                sl = cv.wrap(label, CW_ - PAD * 2, 11.5)
                sh = 12 + 34 * len(sl)
                cv.rect(x, y, CW_, sh, fc=FILL[st][0])
                for i, ln in enumerate(sl):
                    cv.text(x + PAD, y + 6 + 17 + i * 34, ln, size=11.5,
                            color=FILL[st][1], weight="bold", ha="left", z=6)
                y += sh
                continue
            lines = cv.wrap(label, CW_ - 90 - PAD * 2, SZ)
            rh = max(46, len(lines) * 32 + 18)
            cv.rect(x, y, CW_, rh, fc="#ffffff", ec="#c8d0da", lw=1.0)
            cv.rect(x + CW_ - 88, y, 88, rh, fc="#f4f6f9", ec="#c8d0da",
                    lw=1.0)
            for i, ln in enumerate(lines):
                cv.text(x + PAD, y + rh / 2 - (len(lines) - 1) * 16 + i * 32,
                        ln, size=SZ, color=INK, ha="left", z=6)
            cv.text(x + CW_ - 44, y + rh / 2, pt, size=13, color=FILL[st][1],
                    weight="bold", z=6)
            y += rh

    y = top + max(heights) + 40
    textbox(cv, 40, y, W - 80,
            ["早剝は基礎疾患だけで 4〜5 点を持っている。"
             "そこに冷汗・蒼白（各 1 点）、FDP ≧10（1 点）、Fbg ≦150（1 点）を足すと、",
             "それだけで判定の 8 点に届く。"
             "検査項目が 2 点含まれているので、必須条件も同時に満たす。"],
            13, style="red", title="早剝では、こうなる", title_size=15, pad_y=20)

    cv.block(40, y + 200, W - 80,
             ["出典：産科DIC診断基準（日本産科婦人科学会誌 2006;61:N5-N32 ／ "
              "産婦人科の実際 2013;62:153-161 ／",
              "朝倉英策編著『臨床に直結する血栓止血学』中外医学社, 2013, 235-242）。"
              "判定は原典または自施設の様式で行うこと。"],
             10.5, color=GREY, ha="left")
    save(cv, "f22_dic_criteria_full.png")



if __name__ == "__main__":
    f11(); f12(); f13(); f14(); f15()
    f16(); f17(); f18(); f19(); f20(); f21(); f22()
    print("fig22_b done")
