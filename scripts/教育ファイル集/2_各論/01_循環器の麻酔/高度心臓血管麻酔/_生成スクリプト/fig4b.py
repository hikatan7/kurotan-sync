# -*- coding: utf-8 -*-
"""第Ⅳ章 M-TEER　図版 m08〜m15"""
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


# ---------------------------------------------------------------- m08
def m08():
    """合併症と TEE での検出"""
    cv = Canvas(W, 1800)
    cap(cv, 44, "何が起こりうるか、そのとき何が見えるか")

    ROWS = [("心タンポナーデ", RED, "中隔穿刺・ガイド操作",
             "血圧低下＋心嚢液の出現。まず TEE で心嚢を見る"),
            ("単尖弁離脱（SLDA）", RED, "把持が浅い・緊張が強い",
             "急な逆流の増加。3D と二平面でクリップと弁尖の関係を見る"),
            ("医原性の僧帽弁狭窄", ORANGE, "クリップの入れすぎ",
             "拡張期の平均圧較差が上がる。留置ごとに測る"),
            ("デバイスの脱落・塞栓", RED, "把持不全",
             "左房・左室内の異物。逆流の急変で気づく"),
            ("空気塞栓", ORANGE, "シース操作・脱気不良",
             "突然の低血圧と ST 変化。右冠動脈領域に多い"),
            ("血管損傷・後腹膜血腫", ORANGE, "大腿静脈の穿刺",
             "術後の血圧低下と貧血。穿刺部だけを見ない"),
            ("心房中隔欠損の遺残", GREY, "大口径シースの通過",
             "右左シャントによる低酸素。カラードプラで確認"),
            ("TEE 関連の食道・胃損傷", PURPLE, "長時間のプローブ操作",
             "嚥下痛・嚥下障害。手技時間が長いほど増える")]

    y = 130
    for name, col, cause, what in ROWS:
        h = 106
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.5, radius=8)
        cv.box(70, y, 330, h, fc="#fbfcfd", ec=col, lw=0, radius=8)
        cv.text(94, y + 40, name, size=fit(cv, name, 290, 11.2, "bold"),
                color=col, weight="bold", ha="left")
        cv.text(94, y + 74, cause, size=fit(cv, cause, 290, 9.4), color=GREY,
                ha="left")
        cv.text(420, y + h / 2, what, size=fit(cv, what, W - 510, 10.6),
                color=INK, ha="left")
        y += h + 10

    th = textbox(cv, 70, y + 12, W - 140,
                 ["経食道プローブによる合併症は、無視できる大きさではない。",
                  "M-TEER 442 例の検討では 17 例（3.8%）に TEE 関連の合併症があり、"
                  "嚥下障害が 53%、新規の逆流症状が 35% を占めた。",
                  "構造的心疾患インターベンション 50 例で術後に内視鏡を行った研究では、"
                  "86% に新たな粘膜傷害が見つかり、40% は複雑な病変であった。"],
                 10.5, style="purple", title="プローブそのもののリスク",
                 title_color=PURPLE, pad_y=16)
    cv.save(P("m08_complications.png"))
    crop_bottom(P("m08_complications.png"))


# ---------------------------------------------------------------- m09
def m09():
    """実臨床レジストリ"""
    cv = Canvas(W, 900)
    cap(cv, 44, "試験の外では、何が起きているのか")

    C = [("COAPT 市販後研究", BLUE, "#eaf1f8",
          ["5,000 例。試験より重症で併存症が多い",
           "デバイス成功率 97.7%",
           "1 年で MR 2+ 以下が約 90%",
           "試験の結果は実臨床でも再現された"]),
         ("EuroSMR レジストリ", PURPLE, "#f1ecf8",
          ["1,628 例（平均 73.8 歳）",
           "MR 2+ 以下：退院時 92.2% → 5 年 85.5%",
           "5 年生存は 35.0%",
           "逆流は抑えられても、予後は重い"]),
         ("EXPAND / 第 4 世代", GREEN, "#eaf5ee",
          ["心房性機能性 MR という新しい病型",
           "デバイスの世代で成績が変わる",
           "古い試験の数字をそのまま使わない"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 130, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    th = textbox(cv, 70, 460, W - 140,
                 ["EuroSMR の 5 年生存 35.0% という数字は、"
                  "この治療の位置づけを端的に示している。",
                  "逆流は確かに減る。しかし患者はもともと重い心不全を抱えている。",
                  "M-TEER は「心不全を治す治療」ではなく、"
                  "「逆流という負荷を取り除く治療」である。"],
                 10.8, style="navy", title="数字の読み方", title_color=NAVY,
                 pad_y=16)

    msg(cv, 460 + th + 28,
        "麻酔科が向き合うのは、5 年生存が 35% という集団である")
    cv.save(P("m09_registries.png"))
    crop_bottom(P("m09_registries.png"))


# ---------------------------------------------------------------- m10
def m10():
    """麻酔法の比較"""
    cv = Canvas(W, 1700)
    cap(cv, 44, "全身麻酔か、深鎮静か")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 400

    def panel(x, title, color, fc, pros, cons):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.box(x, PY, PW, 54, fc=color, ec=color, lw=0, radius=10)
        cv.text(x + PW / 2, PY + 27, title,
                size=fit(cv, title, PW - 40, 12.2, "bold"), color="white",
                weight="bold")
        yy = PY + 78
        for lab, items, c in (("向いている点", pros, GREEN),
                              ("難しい点", cons, RED)):
            cv.text(x + 30, yy, lab, size=10.2, color=c, weight="bold",
                    ha="left")
            yy += 30
            for it in items:
                cv.text(x + 44, yy, "・" + it,
                        size=fit(cv, "・" + it, PW - 80, 10.0), color=INK,
                        ha="left")
                yy += 28
            yy += 10

    panel(x1, "全身麻酔", BLUE, "#eaf1f8",
          ["気道が確保されている", "長時間の TEE に耐えられる",
           "体動がない", "急変時の対応が速い"],
          ["循環抑制が加わる", "抜管までの時間がかかる"])
    panel(x2, "深鎮静・監視下麻酔", GREEN, "#eaf5ee",
          ["循環への影響が小さい", "ICU 滞在が短い",
           "回復が速い"],
          ["気道が確保されていない", "体動と嚥下でプローブ操作が難しい",
           "急変時は全身麻酔へ移行が要る"])

    DATA = [("232 例の比較（深鎮静 対 全身麻酔）",
             "主要安全性エンドポイント（心血管イベント・外科転換・"
             "血管合併症・肺炎）に差はなかった"),
            ("別の比較研究",
             "手技成功率は 100% 対 96.7% で同等。ICU 滞在は深鎮静で有意に短く、"
             "在院日数には差がなかった"),
            ("鎮静レジメンの報告",
             "デクスメデトミジンとレミフェンタニルの併用 26 例と"
             "全身麻酔 53 例の比較。年齢中央値は両群とも 81 歳")]
    y = PY + PH + 30
    for lab, det in DATA:
        dl = cv.wrap(det, W - 200, 10.4)
        bh = 68 + LH(10.4, 1.45) * len(dl) + 4
        cv.box(70, y, W - 140, bh, fc="#fbfcfd", ec="#dde3ea", lw=1.4,
               radius=8)
        cv.text(96, y + 34, lab, size=fit(cv, lab, W - 200, 10.8, "bold"),
                color=NAVY, weight="bold", ha="left")
        for j, ln in enumerate(dl):
            cv.text(96, y + 68 + LH(10.4, 1.45) * j, ln, size=10.4,
                    color=INK, ha="left")
        y += bh + 12

    msg(cv, y + 8,
        "どちらでもよいのではない。TEE の時間と患者の呼吸予備能で決まる")
    cv.save(P("m10_anesthesia.png"))
    crop_bottom(P("m10_anesthesia.png"))


# ---------------------------------------------------------------- m11
def m11():
    """Alg4-1 麻酔法の選択"""
    cv = Canvas(W, 1800)
    cap(cv, 44, "アルゴリズム 1　M-TEER の麻酔法を決める")

    cx = W / 2
    bw = 800
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["解剖は単純か（逆流の機序・弁尖の長さ・弁口面積）",
              "何個クリップを置く見込みか",
              "施設の経験（手技時間はどれくらいか）"],
             style="navy", title="① 手技の難度を見積もる", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["仰臥位で何分寝ていられるか（起坐呼吸はないか）",
              "肺高血圧・右心不全はどの程度か",
              "腎機能・意識・協力度",
              "食道・胃の疾患（TEE を長時間かけられるか）"],
             style="red", title="② 患者側の条件を見積もる", title_color=RED)
    y += h
    down(cv, cx, y, y + 50)
    y += 50
    cw = 520
    lx, rx = 70, W - 70 - cw
    side(cv, cx - 40, lx + cw + 10, y + 74)
    side(cv, cx + 40, rx - 10, y + 74)
    hl = step(cv, lx, y, cw,
              ["解剖が複雑、手技が長くなりそう",
               "起坐呼吸がある、協力が得られない",
               "食道の操作に時間がかかりそう",
               "→ 全身麻酔"],
              style="blue", title="全身麻酔を選ぶ", title_color=BLUE)
    hr = step(cv, rx, y, cw,
              ["解剖が単純で短時間が見込める",
               "呼吸予備能があり、協力が得られる",
               "早期の離床・退院を狙う",
               "→ 深鎮静（移行の準備はしておく）"],
              style="green", title="深鎮静を選ぶ", title_color=GREEN)
    y += max(hl, hr)
    down(cv, lx + cw / 2, y, y + 44)
    down(cv, rx + cw / 2, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["深鎮静でも、全身麻酔へ移行できる準備をしておく",
              "誰が気道を確保するか、器材はどこにあるかを確認する",
              "移行の判断基準（SpO2・体動・手技の中断）を共有する"],
             style="amber", title="③ どちらでも決めておくこと",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["クリップ留置後に後負荷が上がることを、全員が知っている",
          "昇圧薬・強心薬を手元に置く",
          "循環補助が必要になったときの手順を決めておく"],
         style="purple", title="④ 麻酔法によらず必要なこと",
         title_color=PURPLE)
    cv.save(P("m11_alg_anesthesia.png"))
    crop_bottom(P("m11_alg_anesthesia.png"))


# ---------------------------------------------------------------- m12
def m12():
    """Alg4-2 術中の突然の低血圧"""
    cv = Canvas(W, 1800)
    cap(cv, 44, "アルゴリズム 2　術中に突然血圧が下がった")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["いま手技のどの段階か（中隔穿刺・ガイド操作・把持・留置）",
              "段階によって、疑うべき原因が違う"],
             style="navy", title="① まず、段階を確認する", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["心嚢液はあるか（タンポナーデ）",
              "逆流が急に増えていないか（SLDA・弁尖損傷）",
              "左室の動きはどうか（後負荷ミスマッチ）",
              "右室は張っていないか（空気塞栓・肺塞栓）"],
             style="red", title="② TEE で四つを順に見る", title_color=RED)
    y += h
    down(cv, cx, y, y + 50)
    y += 50
    cw = 340
    gap = (W - 140 - cw * 3) / 2
    LABS = [("心嚢液がある", RED, "#fceeec",
             ["タンポナーデとして対応する", "輸液・昇圧・心膜穿刺の準備",
              "術者に操作を止めてもらう"]),
            ("逆流が増えた", ORANGE, "#fdf3e3",
             ["クリップの状態を 3D で確認", "SLDA なら再把持・回収を検討",
              "循環を支えながら判断する"]),
            ("逆流は減っている", BLUE, "#eaf1f8",
             ["後負荷ミスマッチを疑う", "強心薬と後負荷の調整",
              "左室の収縮を直接見る"])]
    for i, (t, col, fc, lines) in enumerate(LABS):
        x = 70 + (cw + gap) * i
        cv.arrow((cx, y - 10), (x + cw / 2, y + 16), color="#b9c2cc", lw=1.6,
                 head=8)
        card(cv, x, y + 20, cw, t, lines, col, fc, body_size=10.0, lh=1.8)
    y += 20 + 250
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["血管合併症（後腹膜血腫）は、術野では見えない",
          "穿刺部だけでなく、腹部の膨隆と Hb の推移を見る",
          "原因が特定できないときは、複数を同時に疑い続ける"],
         style="purple", title="③ TEE で見えない原因もある",
         title_color=PURPLE)
    cv.save(P("m12_alg_hypotension.png"))
    crop_bottom(P("m12_alg_hypotension.png"))


# ---------------------------------------------------------------- m13
def m13():
    """Alg4-3 クリップを追加するか"""
    cv = Canvas(W, 1700)
    cap(cv, 44, "アルゴリズム 3　クリップを追加するか、止めるか")

    cx = W / 2
    bw = 800
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["残存する逆流はどの程度か（複数の指標で評価する）",
              "拡張期の平均圧較差は何 mmHg か",
              "肺静脈血流の逆行性成分は改善したか",
              "左房圧は下がったか"],
             style="navy", title="① 留置のたびに測る", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 50)
    y += 50
    cw = 520
    lx, rx = 70, W - 70 - cw
    side(cv, cx - 40, lx + cw + 10, y + 74)
    side(cv, cx + 40, rx - 10, y + 74)
    hl = step(cv, lx, y, cw,
              ["逆流が中等度以上残っている",
               "圧較差はまだ低い",
               "解剖学的に追加できる位置がある",
               "→ 追加を検討する"],
              style="green", title="追加する方向", title_color=GREEN)
    hr = step(cv, rx, y, cw,
              ["圧較差がすでに上がってきている",
               "術前の弁口面積が小さかった",
               "逆流は軽度まで減っている",
               "→ ここで止める"],
              style="red", title="止める方向", title_color=RED)
    y += max(hl, hr)
    down(cv, lx + cw / 2, y, y + 44)
    down(cv, rx + cw / 2, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["術前の弁口面積が 4.0 cm2 未満では、86% に圧較差の上昇が生じた",
              "4.0〜6.0 cm2 で 28%、6.0 cm2 超で 14%",
              "術後の平均圧較差 5 mmHg 超は、1 年全死亡の 3.42 倍のリスク",
              "小さい弁口面積が予後と関連したのは変性性 MR であった"],
             style="amber", title="② 判断を支える数字", title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["最終的な決定は術者が行う。麻酔科は数字を提供する",
          "「逆流はこれだけ残り、圧較差はこれだけ上がった」と言語化する",
          "判断の根拠を記録に残す"],
         style="purple", title="③ 役割を分ける", title_color=PURPLE)
    cv.save(P("m13_alg_gradient.png"))
    crop_bottom(P("m13_alg_gradient.png"))


# ---------------------------------------------------------------- m14
def m14():
    """Alg4-4 心原性ショックでの M-TEER"""
    cv = Canvas(W, 1700)
    cap(cv, 44, "アルゴリズム 4　心原性ショックのなかで行う M-TEER")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["急性の重症 MR（腱索断裂・乳頭筋断裂・虚血性）か",
              "慢性の MR が急性増悪したのか",
              "すでにカテコラミン・IABP・ECMO が入っているか"],
             style="navy", title="① どういうショックかを分ける",
             title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["循環補助を続けたまま手技に入れるか",
              "TEE を長時間かけられる呼吸状態か（多くは全身麻酔）",
              "手技が失敗したときの次の手（外科・補助循環）を決めてあるか"],
             style="red", title="② 手技に入れる状態かを見る",
             title_color=RED)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["逆流が減った瞬間、左室の後負荷が上がる",
              "ショック例では、この変化に耐えられないことがある",
              "強心薬と後負荷を、留置の前後で調整できるようにしておく",
              "補助循環の離脱を急がない"],
             style="amber", title="③ 留置の瞬間に備える",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["ショック例での M-TEER は、系統的レビューで報告が蓄積してきた段階",
          "無作為化試験はなく、適応は施設とチームの判断による",
          "「できる」ことと「するべき」ことは別であると、"
          "チームで確認してから始める"],
         style="purple", title="④ エビデンスの位置づけ", title_color=PURPLE)
    cv.save(P("m14_alg_shock.png"))
    crop_bottom(P("m14_alg_shock.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (m08, m09, m10, m11, m12, m13, m14):
        fn()
        print("ok", fn.__name__)
