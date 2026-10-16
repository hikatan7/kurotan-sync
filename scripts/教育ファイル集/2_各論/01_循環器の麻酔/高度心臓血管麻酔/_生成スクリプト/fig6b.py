# -*- coding: utf-8 -*-
"""第Ⅵ章 透析患者の心大血管手術　図版 q08〜q14"""
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


# ---------------------------------------------------------------- q08
def q08():
    """血管アクセスの保護"""
    cv = Canvas(W, 1000)
    cap(cv, 44, "シャントは、この患者の命綱である")

    C = [("してはいけないこと", RED, "#fceeec",
          ["シャント肢での血圧測定", "シャント肢での駆血・静脈路確保",
           "シャント肢での動脈ライン", "腕を圧迫する体位・固定"]),
         ("すること", GREEN, "#eaf5ee",
          ["入室時にスリル・血管雑音を確認する", "シャント肢に印をつける",
           "術中も定期的に確認する", "退室時に再確認して記録する"]),
         ("失う原因", ORANGE, "#fdf3e3",
          ["長時間の低血圧", "脱水・過度の除水", "圧迫",
           "血栓（凝固能の変化）"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 140, w, t, lines, col, fc,
             body_size=10.4, lh=1.8)

    th = textbox(cv, 70, 480, W - 140,
                 ["米国腎臓財団の血管アクセスガイドライン（2019 年改訂）は、"
                  "アクセスを「作る・維持する・守る」ことを",
                  "患者の生涯にわたる課題として位置づけている。",
                  "手術中の数時間の低血圧が、"
                  "その後の透析生活を変えてしまうことがある。"],
                 10.8, style="navy", title="なぜここまで気をつけるのか",
                 title_color=NAVY, pad_y=16)

    msg(cv, 480 + th + 28,
        "シャントを守ることは、術中管理の付随事項ではなく目的の一つである",
        fc="#eaf5ee", ec=GREEN, tc=GREEN)
    cv.save(P("q08_vascular_access.png"))
    crop_bottom(P("q08_vascular_access.png"))


# ---------------------------------------------------------------- q09
def q09():
    """TAVR と SAVR、弁の選択"""
    cv = Canvas(W, 1300)
    cap(cv, 44, "透析患者の大動脈弁を、どう治すか")

    x0, y0 = 70, 130
    cv.box(x0, y0, W - 140, 300, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    t = "透析患者における TAVR 対 SAVR（傾向スコア調整）"
    cv.text(W / 2, y0 + 38, t, size=12.2, color=NAVY, weight="bold")
    PAIR = [("院内死亡", "TAVR が低い", "OR 0.38（95%CI 0.27-0.52）", GREEN),
            ("3 年死亡", "TAVR が高い", "HR 1.24（95%CI 1.1-1.39）", RED)]
    w2 = (W - 200) / 2
    for i, (lab, dirn, val, col) in enumerate(PAIR):
        x = 100 + w2 * i
        cv.box(x + 20, y0 + 78, w2 - 40, 190, fc="#fbfcfd", ec=col, lw=1.6,
               radius=8)
        cv.text(x + w2 / 2, y0 + 118, lab, size=12.0, color=INK)
        cv.text(x + w2 / 2, y0 + 172, dirn, size=14.0, color=col,
                weight="bold")
        cv.text(x + w2 / 2, y0 + 224, val, size=fit(cv, val, w2 - 80, 10.6),
                color=GREY)

    y1 = y0 + 330
    cv.box(70, y1, W - 140, 330, fc="#ffffff", ec=PURPLE, lw=1.8, radius=10)
    cv.text(W / 2, y1 + 38, "人工弁の選択（生体弁か機械弁か）", size=12.2,
            color=PURPLE, weight="bold")
    ROWS = [("個別患者データのメタ解析（8 研究）",
             "機械弁 1,215 例 対 生体弁 1,851 例。平均追跡 43.1 か月",
             "機械弁で生存が良好（HR 0.76、95%CI 0.69-0.84、p<0.001）"),
            ("日本の単施設（491 例）",
             "生体弁 323 例 対 機械弁 168 例",
             "院内死亡 12.1% 対 8.9%（p=0.29）、5 年生存 39.3% 対 50.4%"
             "（p=0.42）")]
    yy = y1 + 76
    for a, b, c in ROWS:
        cv.text(100, yy + 22, a, size=fit(cv, a, W - 220, 11.0, "bold"),
                color=PURPLE, weight="bold", ha="left")
        cv.text(100, yy + 58, b, size=fit(cv, b, W - 220, 10.2), color=GREY,
                ha="left")
        cv.text(100, yy + 94, c, size=fit(cv, c, W - 220, 10.6), color=INK,
                ha="left")
        yy += 128

    th = textbox(cv, 70, y1 + 360, W - 140,
                 ["透析患者では、生体弁の劣化が速い一方、"
                  "機械弁では抗凝固に伴う出血が問題になる。",
                  "メタ解析は機械弁の生存優位を示すが、"
                  "日本の報告では 5 年生存に有意差がなかった。",
                  "いずれにせよ 5 年生存が 40〜50% という集団であり、"
                  "「どちらが長持ちするか」だけでは決まらない。"],
                 10.6, style="amber", title="どう読むか",
                 title_color="#9a6510", pad_y=16)
    cv.save(P("q09_valve_choice.png"))
    crop_bottom(P("q09_valve_choice.png"))


# ---------------------------------------------------------------- q10
def q10():
    """冠血行再建と術後 RRT"""
    cv = Canvas(W, 1300)
    cap(cv, 44, "冠血行再建の選択と、術後の腎代替療法")

    x0, y0 = 70, 130
    cv.box(x0, y0, W - 140, 250, fc="#ffffff", ec=GREEN, lw=1.8, radius=10)
    t = "透析患者における CABG 対 PCI（12 研究のメタ解析）"
    cv.text(W / 2, y0 + 38, t, size=12.2, color=GREEN, weight="bold")
    cv.text(W / 2, y0 + 92, "CABG 13,651 例　対　PCI 28,493 例",
            size=11.0, color=GREY)
    cv.text(W / 2, y0 + 150, "CABG のほうが生存が良好", size=15.0,
            color=GREEN, weight="bold")
    cv.text(W / 2, y0 + 200, "ハザード比 1.12（95%CI 1.09-1.16、p<0.0001）",
            size=10.8, color=INK)

    y1 = y0 + 280
    C = [("容量を引く", BLUE, "#eaf1f8",
          ["溢れた水を戻す", "利尿薬が効かない患者では唯一の手段"]),
         ("カリウムを下げる", RED, "#fceeec",
          ["薬では 1 mEq/L 程度しか下がらない", "確実に下げられる唯一の方法"]),
         ("酸塩基を整える", GREEN, "#eaf5ee",
          ["代謝性アシドーシスの補正", "カテコラミンの効きにも影響する"]),
         ("薬物を除去する", PURPLE, "#f1ecf8",
          ["蓄積した薬剤", "透析性の有無を確認しておく"])]
    w = (W - 140 - 90) / 4
    for i, (t2, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, y1, w, t2, lines, col, fc,
             body_size=10.0, lh=1.8)

    y2 = y1 + 290
    th = textbox(cv, 70, y2, W - 140,
                 ["術後の腎代替療法を「急性腎障害の治療」として考えると、"
                  "透析患者では意味がずれる。",
                  "すでに腎機能はないのだから、"
                  "開始の判断は「腎機能が悪化したか」ではなく、"
                  "「上の四つのどれが必要か」で決まる。",
                  "重症患者の開始時期を比較した大規模試験"
                  "（3,019 例）では、早期開始が 90 日死亡を下げなかった。",
                  "ただしこの試験の対象は急性腎障害であり、"
                  "維持透析患者にそのまま当てはめることはできない。"],
                 10.6, style="navy", title="透析患者にとっての RRT とは",
                 title_color=NAVY, pad_y=16)

    msg(cv, y2 + th + 28,
        "「いつ始めるか」ではなく、「何のために始めるか」で決める")
    cv.save(P("q10_revascularization_rrt.png"))
    crop_bottom(P("q10_revascularization_rrt.png"))


# ---------------------------------------------------------------- q11
def q11():
    """術前透析のタイミング"""
    cv = Canvas(W, 1000)
    cap(cv, 44, "前日に透析するか、当日に透析するか")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 420

    def panel(x, title, color, fc, pros, cons):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.box(x, PY, PW, 54, fc=color, ec=color, lw=0, radius=10)
        cv.text(x + PW / 2, PY + 27, title,
                size=fit(cv, title, PW - 40, 12.2, "bold"), color="white",
                weight="bold")
        yy = PY + 84
        for lab, items, c in (("利点", pros, GREEN), ("難点", cons, RED)):
            cv.text(x + 30, yy, lab, size=10.4, color=c, weight="bold",
                    ha="left")
            yy += 32
            for it in items:
                cv.text(x + 44, yy, "・" + it,
                        size=fit(cv, "・" + it, PW - 80, 10.0), color=INK,
                        ha="left")
                yy += 28
            yy += 12

    panel(x1, "前日に透析する", BLUE, "#eaf1f8",
          ["ヘパリンの影響が抜けている", "循環が落ち着いている",
           "手術の開始時刻に縛られない"],
          ["当日朝にはカリウムが上がっている", "容量も戻っている"])
    panel(x2, "当日に透析する", GREEN, "#eaf5ee",
          ["カリウムと容量を直前に整えられる"],
          ["ヘパリンの残存（出血・回路凝固）", "除水直後で血管内容量が少ない",
           "導入時の低血圧が起こりやすい", "手術開始が遅れる"])

    th = textbox(cv, 70, PY + PH + 26, W - 140,
                 ["どちらが正しいという答えはない。",
                  "決まっているのは、「最終透析がいつで、"
                  "何 kg 引いたか」を知らずに導入してはいけないということである。",
                  "そして当日透析を選んだ場合は、"
                  "除水直後の血管内容量の少なさを前提に導入する。"],
                 10.8, style="amber", title="決め方",
                 title_color="#9a6510", pad_y=16)

    msg(cv, PY + PH + 26 + th + 28,
        "確認するのは三つ。最終透析の時刻、除水量、そして dry weight との差")
    cv.save(P("q11_dialysis_timing.png"))
    crop_bottom(P("q11_dialysis_timing.png"))


# ---------------------------------------------------------------- q12
def q12():
    """Alg6-1 透析患者が心臓手術に来たら"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 1　透析患者が心臓手術に来たら")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["最終透析はいつか。何 kg 引いたか",
              "dry weight と当日の体重の差",
              "透析のスケジュール（週何回、どの曜日か）",
              "残存腎機能と尿量の有無"],
             style="navy", title="① 透析そのものを把握する",
             title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["カリウム（値と、直近の推移）と心電図",
              "ヘモグロビンと、輸血の準備",
              "血小板数と、抗血栓薬の内容・最終内服",
              "イオン化カルシウムと酸塩基"],
             style="red", title="② 数字を集める", title_color=RED)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["シャントの位置を確認し、印をつける",
              "血圧計・静脈路・動脈ラインをどの肢に置くか決める",
              "体位でシャント肢が圧迫されないようにする"],
             style="green", title="③ 血管アクセスを守る計画",
             title_color=GREEN)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["術中透析を行うか（回路と人員の手配）",
              "限外濾過の目標量",
              "心筋保護液によるカリウム負荷への対応",
              "術後の腎代替療法をどこで行うか"],
             style="amber", title="④ 人工心肺とその後の計画",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["術後の透析スケジュールを腎臓内科と共有する",
          "抗凝固の再開時期を決める",
          "シャントの開存を退室時と術後に確認する"],
         style="purple", title="⑤ 引き継ぎ", title_color=PURPLE)
    cv.save(P("q12_alg_preop.png"))
    crop_bottom(P("q12_alg_preop.png"))


# ---------------------------------------------------------------- q13
def q13():
    """Alg6-2 導入前のカリウム 6.0"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 2　導入前にカリウムが 6.0 mEq/L だった")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["心電図を見る（テント状 T 波・QRS 幅・P 波の消失）",
              "採血の時期と、最終透析からの時間を確認する",
              "溶血による偽高値ではないかを疑う"],
             style="navy", title="① 値だけで判断しない", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 50)
    y += 50
    cw = 520
    lx, rx = 70, W - 70 - cw
    side(cv, cx - 40, lx + cw + 10, y + 74)
    side(cv, cx + 40, rx - 10, y + 74)
    hl = step(cv, lx, y, cw,
              ["心電図変化がある、または上昇が速い",
               "→ カルシウムで膜を守る",
               "→ 同時にインスリン＋ブドウ糖",
               "→ 透析を手配する（手術の延期も選択肢）"],
              style="red", title="緊急性が高い", title_color=RED)
    hr = step(cv, rx, y, cw,
              ["心電図変化がなく、透析前の値",
               "→ 手術の緊急度と天秤にかける",
               "→ 術中透析ができるなら、それを前提に進める",
               "→ 進めるなら、頻回の測定を計画する"],
              style="green", title="緊急性が低い", title_color=GREEN)
    y += max(hl, hr)
    down(cv, lx + cw / 2, y, y + 44)
    down(cv, rx + cw / 2, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["薬物治療で下がるのは平均 0.7〜1.2 mEq/L 程度",
              "カルシウムはカリウム値を下げない（心筋膜を守るだけ）",
              "重炭酸の効果は限定的",
              "体外へ出せるのは透析だけ"],
             style="amber", title="② 効果量を前提に計画する",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["脱分極性筋弛緩薬を避ける",
          "アシドーシスを避ける（換気を保つ）",
          "細胞内へ移した分は、あとで戻ってくることを忘れない",
          "術中も定期的に測る"],
         style="purple", title="③ 導入する場合の注意", title_color=PURPLE)
    cv.save(P("q13_alg_hyperkalemia.png"))
    crop_bottom(P("q13_alg_hyperkalemia.png"))


# ---------------------------------------------------------------- q14
def q14():
    """Alg6-3 CPB 離脱とその後"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 3　人工心肺からの離脱と、その後")

    cx = W / 2
    bw = 820
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["カリウム（心筋保護液の影響が残っている）",
              "イオン化カルシウムとマグネシウム",
              "容量（限外濾過でどこまで引けたか）",
              "ヘモグロビンと凝固"],
             style="navy", title="① 離脱前に整えるもの", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["回している間に透析・限外濾過で整えておく",
              "離脱してからでは、引く手段が限られる",
              "術中透析を行った報告では、離脱時のカテコラミンが少なかった"],
             style="green", title="② 「回している間に」が原則",
             title_color=GREEN)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["血小板機能は数だけでは評価できない",
              "貧血の是正そのものが止血に寄与する",
              "粘弾性検査があれば、それに基づいて製剤を選ぶ",
              "デスモプレシンの効果は研究により一致していない"],
             style="red", title="③ 出血への対応", title_color=RED)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["容量・カリウム・酸塩基・薬物のどれが目的かを決める",
              "その目的に合った方法（間欠的透析か持続的療法か）を選ぶ",
              "腎臓内科と、術後の透析スケジュールを共有する"],
             style="amber", title="④ 術後の腎代替療法",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["シャントの開存を退室時に確認し、記録する",
          "血圧の下限を、病棟へ引き継ぐ",
          "抗凝固の再開時期を明記する"],
         style="purple", title="⑤ 退室時に残すもの", title_color=PURPLE)
    cv.save(P("q14_alg_cpb.png"))
    crop_bottom(P("q14_alg_cpb.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (q08, q09, q10, q11, q12, q13, q14):
        fn()
        print("ok", fn.__name__)
