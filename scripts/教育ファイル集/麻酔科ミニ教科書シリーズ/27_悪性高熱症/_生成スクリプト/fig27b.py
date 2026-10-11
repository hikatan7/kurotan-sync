# -*- coding: utf-8 -*-
"""㉗ 悪性高熱症　図版 f11〜f20"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE)
from fig27a import P, cap, msg, card, fitlines, W, TEAL


# ---------------------------------------------------------------- f11
def f11():
    """対症療法"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "対症療法 ── 何を、どこまで")

    ROWS = [
        ("冷却", "冷却生理食塩水を静注（最大 50-60 mL/kg）。室温を下げ送風で体表冷却",
         "中枢温 38 ℃を下回ったら止める（EMHG は 38.5 ℃）", BLUE),
        ("高カリウム血症", "グルコース・インスリン療法、塩化カルシウムまたはグルコン酸カルシウム",
         "K > 5.9 mEq/L か心電図変化があれば", ORANGE),
        ("代謝性アシドーシス", "炭酸水素ナトリウム 1.0-2.0 mEq/kg（最大 50 mEq）",
         "BE ≦ −8.0。まず換気で CO2 を出す", ORANGE),
        ("ミオグロビン尿", "炭酸水素ナトリウム 1.0 mEq/kg/時で尿をアルカリ化",
         "CK・K の上昇、ミオグロビン尿に対して", PURPLE),
        ("利尿", "フロセミド 0.5-1.0 mg/kg（最大 20 mg）",
         "尿量 1.0 mL/kg/時を目安に", PURPLE),
        ("不整脈", "アミオダロン、マグネシウム、β 遮断薬（EMHG）",
         "カルシウム拮抗薬は使わない", RED),
        ("循環", "動脈ラインを確保する", "血液ガスを繰り返し測るため", GREEN),
        ("回路", "（可能なら）気化器を外し麻酔回路を交換",
         "人手と時間が要るので必須ではない", GREY),
    ]
    L, TOP = 60, 106
    NW = max(cv.width(r[0], 11.4, "bold") for r in ROWS) + 40
    SW = 430
    WW = W - 120 - 26 - NW - SW - 30
    y = TOP
    for i, (name, what, note, color) in enumerate(ROWS):
        wl = cv.wrap(what, WW, 10.4)
        sl = cv.wrap(note, SW - 16, 10.0)
        lh = LH(10.4, 1.35)
        rh = max(72, 26 + lh * max(len(wl), len(sl)))
        cv.box(L, y, W - 120, rh, fc="white", ec="#dde2e8", lw=1.4, radius=6)
        cv.rect(L, y, 8, rh, fc=color)
        cv.text(L + 26, y + rh / 2, name, size=11.4, color=color,
                weight="bold", ha="left")
        cv.block(L + 26 + NW, y + rh / 2 - lh * len(wl) / 2, WW, wl, 10.4,
                 color=INK, ha="left", lh=lh)
        cv.block(L + 26 + NW + WW + 30, y + rh / 2 - lh * len(sl) / 2, SW - 16,
                 sl, 10.0, color=GREY, ha="left", lh=lh)
        y += rh + 12

    msg(cv, y + 6,
        "この表のどれも、原因には効かない。"
        "ダントロレンが遅れているなら、まずそちらを取りに行く。")
    cv.save(P("f11_supportive.png"))


# ---------------------------------------------------------------- f12
def f12():
    """麻酔器の準備"""
    cv = Canvas(W, 920)
    cap(cv, 44, "素因者の麻酔器をどう用意するか")

    ITEMS = [
        ("交換するもの", ["気化器を外す", "麻酔回路とバッグ", "二酸化炭素吸収剤"],
         BLUE, "#eaf1f8"),
        ("洗い流す", ["10 L/分以上の高流量で", "100% 酸素・空気・混合ガス",
                  "新しい機種ほど時間がかかる", "60-100 分（JSA 2025）"],
         ORANGE, "#fdf3e3"),
        ("止めない", ["使用開始まで高流量を続ける", "スタンバイにしない",
                  "流量を下げるとリバウンドで", "濃度が戻る"], RED, "#fceeec"),
        ("避けて通る", ["吸入麻酔器を使わない", "非循環式回路の人工呼吸器",
                   "この場合は洗い出し不要", "活性炭フィルタという手もある"],
         GREEN, "#eaf5ee"),
    ]
    CW, GAP, L = 344, 24, 60
    hmax = 0
    for i, (head, lines, color, fc) in enumerate(ITEMS):
        hmax = max(hmax, card(cv, L + i * (CW + GAP), 106, CW, head, lines,
                              color, fc, body_size=9.8, lh=2.0))
    y = 106 + hmax + 32

    h = textbox(cv, 60, y, W - 120,
                ["EMHG 2024 は、危機のさなかでも活性炭フィルタがあれば"
                 "吸気側と呼気側に入れることを勧めている。",
                 "フィルタを使えば、回路の洗い出しを待たずに"
                 "揮発性麻酔薬の濃度を下げられる。日本では常備していない施設が多い。",
                 "洗い出しの時間は機種によって違う。"
                 "自施設の麻酔器で何分かかるかを、一度だけ調べて紙に書いておく。"],
                10.8, fc="white", ec=NAVY, title="活性炭フィルタ",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 28,
        "「洗い出しに 60-100 分」は、当日の朝に始めても間に合わないことがある。")
    cv.save(P("f12_machine.png"))


# ---------------------------------------------------------------- f13
def f13():
    """検査の時系列"""
    cv = Canvas(W, 930)
    cap(cv, 44, "検査は、決めた時刻に繰り返す")

    TIMES = ["発症時", "30 分後", "4 時間後", "12 時間後", "24 時間後", "48 時間後"]
    X0, X1, Y = 120, W - 120, 180
    cv.rect(X0, Y - 3, X1 - X0, 6, fc="#cfd6de")
    for i, t in enumerate(TIMES):
        x = X0 + (X1 - X0) * i / (len(TIMES) - 1)
        cv.box(x - 86, Y - 34, 172, 68, fc="#e8edf5", ec=NAVY, lw=2.0,
               radius=8)
        s = cv.fit_size([t], 150, 11.6, weight="bold")
        cv.text(x, Y, t, size=s, color=NAVY, weight="bold")

    y = 268
    h = textbox(cv, 60, y, W - 120,
                ["動脈血液ガス分析／血糖／電解質／乳酸",
                 "CK／ミオグロビン（血液と尿、定性と定量）",
                 "生化学（腎機能・肝機能）",
                 "DIC 診断のための血液凝固系検査"],
                11.2, fc="#eef1f6", ec=NAVY, title="毎回とるもの",
                title_color=NAVY, lw=2.0, lh_scale=1.9)

    h2 = textbox(cv, 60, y + h + 26, W - 120,
                 ["「落ち着いたから終わり」にしない。48 時間までは表の時刻で回す。",
                  "再燃は 14.4-20.0% と報告されている。"
                  "JSA 2025 は、発症後少なくとも 24 時間の監視を求めている。"],
                 10.8, fc="#fceeec", ec=RED, title="なぜ 48 時間なのか",
                 title_color=RED, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + h2 + 52,
        "検査の時刻を先に決めておくと、誰が指示を出しても同じ間隔で回る。")
    cv.save(P("f13_labs.png"))


# ---------------------------------------------------------------- f14
def f14():
    """やめる判断・再燃"""
    cv = Canvas(W, 760)
    cap(cv, 44, "落ち着いたかどうかを、何で判断するか")

    ITEMS = [("ETCO2", "低下しているか、正常化している", GREEN, "#eaf5ee"),
             ("心拍数", "安定している、または不整脈が減っている", GREEN,
              "#eaf5ee"),
             ("体温", "体温管理の必要がなくなっている（平熱に戻った）", GREEN,
              "#eaf5ee"),
             ("筋硬直", "消失している", GREEN, "#eaf5ee")]
    CW, GAP, L = 690, 30, 60
    for i, (name, what, color, fc) in enumerate(ITEMS):
        r, c = i // 2, i % 2
        x = L + c * (CW + GAP)
        y = 106 + r * 106
        cv.box(x, y, CW, 88, fc=fc, ec=color, lw=2.0, radius=8)
        cv.box(x, y, 150, 88, fc=color, ec=color, lw=0, radius=8)
        ns = cv.fit_size([name], 130, 12.6, weight="bold")
        cv.text(x + 75, y + 44, name, size=ns, color="white", weight="bold")
        ws, wl = fitlines(cv, [what], CW - 180, 11.0, floor=9.0)
        cv.block(x + 168, y + 44 - LH(ws, 1.4) * len(wl) / 2, CW - 180, wl,
                 ws, color=INK, ha="left", lh=LH(ws, 1.4))

    y = 106 + 2 * 106 + 20
    h = textbox(cv, 60, y, W - 120,
                ["手術は早く中止し、後日やり直すのが最善である。"
                 "ただし典型的な MH とは言い難い場合は、"
                 "落ち着いてから再開する判断も許容される。",
                 "体温が 40 ℃を超えている場合は絶対に中止する。"
                 "この高体温では死亡率が極めて高い。",
                 "抜管後も 48 時間は厳重に監視する。"
                 "鎮静が不十分だと再燃しうる。"
                 "ダントロレンを大量に使った後は筋力低下と誤嚥に注意する。"],
                10.8, fc="white", ec=NAVY, title="手術をどうするか",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 28,
        "「症状が改善した」と「もう起きない」は別である。再燃は 2 割弱に起こる。")
    cv.save(P("f14_stop.png"))


# ---------------------------------------------------------------- f15
def f15():
    """JSA 2016 → 2025"""
    cv = Canvas(W, 960)
    cap(cv, 44, "日本麻酔科学会ガイドライン 2016 → 2025 の変更")

    ROWS = [
        ("ダントロレンの上限", "最大 7.0 mg/kg", "上限を設けない。改善するまで十分量",
         RED),
        ("投与時間", "15 分程度", "10 分程度", ORANGE),
        ("発症頻度", "全身麻酔 10 万に 1〜2 人", "0.18-3.9 / 10 万", BLUE),
        ("報告症例", "劇症型 400 例超", "600 例超。半数以上が 18 歳未満", BLUE),
        ("保因頻度", "（記載なし）", "1/856 - 1/1075。浸透率 40.6%", PURPLE),
        ("術後 MH の発症時期", "多くは 30 分以内、24 時間で 90%",
         "多くは 40 分以内。少なくとも 24 時間監視", ORANGE),
        ("遺伝子", "RYR1 中心", "RYR1 に加え CACNA1S。検出率 50-70%", PURPLE),
        ("麻酔器の洗い出し", "10-15 L/分で 30-90 分", "10 L/分で 60-100 分。"
         "スタンバイにしない", GREEN),
        ("対症療法の記述", "詳細に列挙", "不要な部分を整理して簡素化", GREY),
    ]
    L, TOP = 60, 106
    cv.box(L, TOP, W - 120, 46, fc=NAVY, ec=NAVY, lw=0, radius=6)
    for x, t in ((L + 200, "項目"), (L + 560, "2016 年版"),
                 (L + 1080, "2025 年版")):
        cv.text(x, TOP + 23, t, size=11.4, color="white", weight="bold")
    for i, (name, old, new, color) in enumerate(ROWS):
        y = TOP + 54 + i * 78
        cv.box(L, y, W - 120, 68, fc="#fafbfc" if i % 2 else "white",
               ec="#dde2e8", lw=1.2, radius=6)
        cv.rect(L, y, 8, 68, fc=color)
        ns, nl = fitlines(cv, [name], 330, 11.0, weight="bold", floor=9.0)
        cv.block(L + 26, y + 34 - LH(ns, 1.35) * len(nl) / 2, 330, nl, ns,
                 color=color, weight="bold", ha="left", lh=LH(ns, 1.35))
        os_, ol = fitlines(cv, [old], 400, 10.2, floor=8.4)
        cv.block(L + 380, y + 34 - LH(os_, 1.35) * len(ol) / 2, 400, ol, os_,
                 color=GREY, ha="left", lh=LH(os_, 1.35))
        ns2, nl2 = fitlines(cv, [new], 520, 10.2, floor=8.4)
        cv.block(L + 830, y + 34 - LH(ns2, 1.35) * len(nl2) / 2, 520, nl2,
                 ns2, color=INK, ha="left", lh=LH(ns2, 1.35))

    msg(cv, TOP + 54 + 9 * 78 + 14,
        "日本語版は 2025 年 3 月、英語版は Journal of Anesthesia 2026;40:4-12。"
        "手元のガイドラインが 2016 年版なら差し替える。")
    cv.save(P("f15_jsa_change.png"))


# ---------------------------------------------------------------- f16
def f16():
    """素因の検査"""
    cv = Canvas(W, 900)
    cap(cv, 44, "素因を調べる三つの方法")

    ITEMS = [
        ("CICR 検査", ["日本で行われている方法",
                    "皮膚を剝いだ筋線維で、Ca 濃度を",
                    "5 段階（0・0.3・1.0・3.0・10 μM）に",
                    "変えて Ca 放出速度を測る",
                    "速度の亢進が素因を示す"], BLUE, "#eaf1f8"),
        ("IVCT／CHCT", ["欧州の IVCT、北米の CHCT",
                      "筋生検した筋線維に",
                      "カフェインとハロタンを当て",
                      "収縮の強さを見る",
                      "日本で常時行える施設はない"], PURPLE, "#f1ecf8"),
        ("遺伝子検査", ["RYR1 と CACNA1S",
                    "素因者で変異が見つかるのは 50-70%",
                    "病的でない変異も含まれる",
                    "陰性でも素因は否定できない",
                    "近年は実施が増えている"], GREEN, "#eaf5ee"),
    ]
    CW, GAP, L = 448, 28, 60
    hmax = 0
    for i, (head, lines, color, fc) in enumerate(ITEMS):
        hmax = max(hmax, card(cv, L + i * (CW + GAP), 106, CW, head, lines,
                              color, fc, body_size=10.0, lh=1.95))
    y = 106 + hmax + 32

    h = textbox(cv, 60, y, W - 120,
                ["いずれも侵襲があり、実施できる施設が限られる。"
                 "そのため検査を選ばない患者が増えている。",
                 "重要なのは、どの検査も陰性で素因を完全には否定できないことである。"
                 "検査の結果にかかわらず、次の麻酔は引き金薬を避けて組む。",
                 "安静時 CK 値と素因の関連には明らかな根拠がない。"
                 "ただし特発性高 CK 血症は素因を示唆することがある。"],
                10.8, fc="white", ec=NAVY, title="検査の限界",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 28,
        "陰性証明はできない。だから検査は「次の麻酔を変えるため」ではなく"
        "「家族に伝えるため」に行う。")
    cv.save(P("f16_testing.png"))


# ---------------------------------------------------------------- f17
def f17():
    """次の麻酔の設計"""
    cv = Canvas(W, 800)
    cap(cv, 44, "素因者の麻酔を組む")

    L, CW = 60, 690
    h1 = textbox(cv, L, 106, CW,
                 ["区域麻酔（脊髄くも膜下・硬膜外を含む）は安全である",
                  "全身麻酔が要るなら静脈麻酔で組む",
                  "揮発性吸入麻酔薬は絶対に避ける",
                  "不安を減らすため静注鎮静薬を併用してよい",
                  "術前から適切に鎮静する（過度の緊張と興奮を避ける）"],
                 10.8, fc="#eaf5ee", ec=GREEN, title="やること",
                 title_color=GREEN, lw=2.2, lh_scale=2.0)
    h2 = textbox(cv, L + CW + 30, 106, CW,
                 ["ダントロレンの予防投与はしない（筋力低下が強い）",
                  "カルシウム拮抗薬は使わない",
                  "「安全な麻酔だから大丈夫」と考えない",
                  "ETCO2 と深部体温の連続モニターを外さない",
                  "術後の一般管理はふつうでよい（発症しなかった場合）"],
                 10.8, fc="#fceeec", ec=RED, title="やらないこと",
                 title_color=RED, lw=2.2, lh_scale=2.0)
    y = 106 + max(h1, h2) + 32

    h3 = textbox(cv, 60, y, W - 120,
                 ["患者の体重に合わせ、初回量 1.0 mg/kg 分のダントロレンと"
                  "溶解用の注射用水（1 瓶 20 mg につき 60 mL）を手元に置く。",
                  "日本麻酔科学会は、MH 発症時に迅速に対応できる認定施設での"
                  "医療を勧めるよう患者に説明することとしている。",
                  "全身麻酔が可能かどうかではなく、"
                  "「どこで」「誰と」行うかを先に決める。"],
                 10.8, fc="white", ec=NAVY, title="当日までに置いておくもの",
                 title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h3 + 28,
        "素因者の麻酔は難しくない。難しいのは、素因者だと知らずに始めることである。")
    cv.save(P("f17_trigger_free.png"))


# ---------------------------------------------------------------- f18
def f18():
    """患者・家族への説明"""
    cv = Canvas(W, 800)
    cap(cv, 44, "患者と家族に伝える ── 二つの塊")

    L, CW = 60, 690
    h1 = textbox(cv, L, 106, CW,
                 ["薬剤アレルギーではなく、遺伝性の筋疾患であること",
                  "日常生活では特異的な症状がほとんどないこと",
                  "術前の血液検査に特有の所見はないこと",
                  "血縁者にも素因がありうるので、親族に周知すること",
                  "運動誘発性横紋筋融解症や労作性熱中症を"
                  "合併している可能性があること"],
                 10.6, fc="#eaf1f8", ec=BLUE, title="この病気について",
                 title_color=BLUE, lw=2.2, lh_scale=2.0)
    h2 = textbox(cv, L + CW + 30, 106, CW,
                 ["ダントロレンの予防的な内服は勧められないこと",
                  "局所麻酔・区域麻酔は安全であること",
                  "全身麻酔も静脈麻酔なら実施できること",
                  "揮発性吸入麻酔薬は絶対に避けること",
                  "迅速に対応できる施設で受けるのが望ましいこと",
                  "検査が陰性でも素因を完全には否定できないこと"],
                 10.6, fc="#eaf5ee", ec=GREEN, title="次の麻酔について",
                 title_color=GREEN, lw=2.2, lh_scale=2.0)
    y = 106 + max(h1, h2) + 32

    h3 = textbox(cv, 60, y, W - 120,
                 ["日本麻酔科学会は、他施設へ患者を紹介するための"
                  "診療情報提供書の様式をガイドラインに載せている。",
                  "記載するのは、麻酔法と使用薬、九つの症状の有無、"
                  "ダントロレンの総投与量とその効果、そして転帰である。",
                  "この用紙を埋めておくことが、"
                  "次にこの患者を麻酔する誰かへの最良の申し送りになる。"],
                 10.8, fc="white", ec=NAVY, title="紙で渡す",
                 title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h3 + 28,
        "説明の相手は本人だけではない。素因は家系に配られている。")
    cv.save(P("f18_explain.png"))


# ---------------------------------------------------------------- f19
def f19():
    """シミュレーション"""
    cv = Canvas(W, 900)
    cap(cv, 44, "当院のシミュレーション ── 4 時間かけて上がっていく")

    ROWS = [("執刀", "36.6", "40", "97"),
            ("2 時間後", "37.5", "48", "97"),
            ("3 時間後", "38.1", "50", "97"),
            ("3 時間半後", "38.5", "62", "95"),
            ("4 時間後", "38.9", "93", "90")]
    HEAD = ["経過", "膀胱温（℃）", "ETCO2（mmHg）", "SpO2（%）"]
    L, R, TOP = 60, W - 60, 106
    ws = [(R - L) / 4] * 4
    RH = 62
    for c in range(4):
        x = L + c * ws[0]
        cv.rect(x, TOP, ws[0] - 4, 46, fc=NAVY)
        cv.text(x + ws[0] / 2 - 2, TOP + 23, HEAD[c], size=11.4,
                color="white", weight="bold")
    for r, row in enumerate(ROWS):
        y = TOP + 52 + r * RH
        for c in range(4):
            x = L + c * ws[0]
            hot = r >= 3 and c in (1, 2)
            fc = "#eef1f6" if c == 0 else ("#fceeec" if hot else "white")
            cv.rect(x, y, ws[0] - 4, RH - 6, fc=fc, ec="#dde2e8", lw=1.0)
            cv.text(x + ws[0] / 2 - 2, y + (RH - 6) / 2, row[c], size=11.2,
                    color=NAVY if c == 0 else (RED if hot else INK),
                    weight="bold" if c == 0 or hot else "normal")

    y = TOP + 52 + 5 * RH + 18
    h = textbox(cv, 60, y, W - 120,
                ["63 歳男性、168 cm 92 kg。横行結腸癌に対する腹腔鏡下結腸切除術。"
                 "全身麻酔と硬膜外麻酔。担当は 4 年目の麻酔科医。",
                 "振り返りで必ず出る問いは四つ ──"
                 "物品とその移動に不備はなかったか。"
                 "当院だけで十分なダントロレンを確保できたか。",
                 "近隣の病院を合わせて何本になるか。"
                 "1 mg/kg の投与を終えるまでに何分かかったか。",
                 "92 kg なら 1 mg/kg で 5 本、2 mg/kg で 9 本。"
                 "当院の在庫 14 本では 3 mg/kg に届かない。"],
                10.8, fc="white", ec=NAVY, title="シナリオと、振り返りの問い",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 28,
        "シミュレーションで見つかるのは、たいてい知識ではなく物流の問題である。")
    cv.save(P("f19_simulation.png"))


# ---------------------------------------------------------------- f20
def f20():
    """施設で決めておくこと"""
    cv = Canvas(W, 900)
    cap(cv, 44, "紙に書いておくこと")

    ITEMS = [
        ("置き場所", ["ダントロレンは何本、どこに",
                  "注射用水は足りているか",
                  "ガイドラインの最新版はどこに"], BLUE, "#eaf1f8"),
        ("呼び方", ["誰が「緊急事態」を宣言するか",
                 "何番に、誰を呼ぶか",
                 "溶解を担当する人を何人集めるか"], ORANGE, "#fdf3e3"),
        ("足りないとき", ["近隣で在庫を持つ施設と連絡先",
                    "取りに行く手段と所要時間",
                    "薬剤部の夜間・休日の動線"], RED, "#fceeec"),
        ("そのあと", ["監視をどこで何時間続けるか",
                  "検査の時刻表",
                  "診療情報提供書を誰が書くか"], GREEN, "#eaf5ee"),
    ]
    CW, GAP, L = 344, 24, 60
    hmax = 0
    for i, (head, lines, color, fc) in enumerate(ITEMS):
        hmax = max(hmax, card(cv, L + i * (CW + GAP), 106, CW, head, lines,
                              color, fc, body_size=9.8, lh=2.0))
    y = 106 + hmax + 32

    h = textbox(cv, 60, y, W - 120,
                ["この病気で失われる時間の大半は、判断ではなく調達に費やされる。",
                 "溶解に注射用水 60 mL が 1 瓶ごとに要ることを、"
                 "当日はじめて知る人がいないようにする。",
                 "年に一度、シミュレーションで実際に時間を測る。"
                 "測った数字を上の紙に書き足していく。"],
                10.8, fc="white", ec=NAVY, title="なぜ紙なのか",
                title_color=NAVY, lw=1.8, lh_scale=1.9)

    msg(cv, y + h + 28,
        "疑ってから投与するまでを 10 分に収める設計は、当日には作れない。")
    cv.save(P("f20_checklist.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (f11, f12, f13, f14, f15, f16, f17, f18, f19, f20):
        fn()
        print("ok", fn.__name__)
