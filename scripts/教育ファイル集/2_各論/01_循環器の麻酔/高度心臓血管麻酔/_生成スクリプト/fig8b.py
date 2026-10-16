# -*- coding: utf-8 -*-
"""第Ⅷ章 心臓麻酔と神経モニタリング　図版 s09〜s16"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from figlib import (Canvas, LH, textbox, duo, NAVY, INK, GREY, RED, BLUE, GREEN,
                    ORANGE, PURPLE, JP)
from fig1a import cap, msg, fitlines, card, W, TEAL
from fig4a import fit
from figcrop import crop_bottom

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- s09
def s09():
    """自動調節能の曲線と個人差"""
    cv = Canvas(W, 1220)
    cap(cv, 44, "自動調節能の「平らな部分」は、患者ごとに違う場所にある")

    x0, y0 = 150, 190
    pw, ph = W - 320, 300
    cv.rect(x0, y0, pw, ph, fc="#fbfcfd", ec="#dde3ea", lw=1.4)
    mn, mx = 30.0, 120.0
    def px(m):
        return x0 + pw * (m - mn) / (mx - mn)
    for m in (40, 60, 80, 100, 120):
        cv.ax.plot([px(m), px(m)], [y0, y0 + ph], color="#eef1f4", lw=1.0,
                   zorder=1)
        cv.text(px(m), y0 + ph + 26, "%d" % m, size=9.6, color=GREY)
    cv.text(x0 + pw / 2, y0 + ph + 60, "平均動脈圧（mmHg）", size=10.2,
            color=INK)
    cv.text(x0 + 8, y0 - 64, "脳血流", size=9.8, color=GREY, ha="left")

    mm = np.linspace(mn, mx, 400)
    flow = np.clip((mm - 40) / 25.0, 0, 1) * 0.72 + 0.14
    flow = np.where(mm > 84, 0.86 + (mm - 84) * 0.006, flow)
    flow = np.clip(flow, 0, 1.1)
    cv.ax.plot(px(mm), y0 + ph * (1 - flow * 0.82) - 12, color=NAVY, lw=2.8,
               zorder=4)
    cv.rect(px(65), y0 + 6, px(84) - px(65), ph - 12, fc="#e4f2f4",
            ec="none", alpha=0.75, z=2)
    # 三つの目盛りは近接するので、上下に段違いに置いて重なりを避ける
    for m, lab, col, dy in ((65, "下限 65±12", BLUE, -26),
                            (78, "最適 78±11", TEAL, -64),
                            (84, "上限 84±11", PURPLE, -26)):
        cv.ax.plot([px(m), px(m)], [y0 + 6, y0 + ph - 6], color=col, lw=2.0,
                   linestyle="--", zorder=5)
        cv.text(px(m), y0 + dy, lab, size=10.0, color=col, weight="bold")

    y = y0 + ph + 90
    w = (W - 140 - 30) / 2
    th1 = textbox(cv, 70, y, w,
                  ["17% の患者では、下限が最適値より高かった",
                   "29% の患者では、上限が最適値より低かった",
                   "つまり「平らな部分」が狭い、あるいはずれている患者がいる",
                   "全員に同じ目標値を当てると、この人たちを外す"],
                  10.6, style="navy", title="ばらつきの大きさ", title_color=NAVY,
                  pad_y=16)
    th2 = textbox(cv, 70 + w + 30, y, w,
                  ["下限より高い血圧を目標にした群でせん妄 38% 対 53%",
                   "（OR 0.55、95%CI 0.31〜0.97）",
                   "別の試験でも、主要転帰は変わらないが",
                   "せん妄は 8.2% 対 14.9%（RR 0.55、95%CI 0.32〜0.93）",
                   "上限を超えた分（mmHg・時）が増えるとせん妄 OR 1.09"],
                  10.6, style="green", title="個別化すると何が変わったか",
                  title_color=GREEN, pad_y=16)
    msg(cv, y + max(th1, th2) + 28,
        "「65 mmHg 以上」は平均の話。目の前の患者の下限は、測らないと分からない")
    cv.save(P("s09_autoregulation.png"))
    crop_bottom(P("s09_autoregulation.png"))


# ---------------------------------------------------------------- s10
def s10():
    """脳酸素低下とバーストサプレッションの同時発生"""
    cv = Canvas(W, 1200)
    cap(cv, 44, "脳酸素の低下とバーストサプレッションは、同じ時間帯に起こる")

    BARS = [("体外循環前", 1.0, "基準", GREY),
            ("体外循環中", 52.3, "同時発生 OR 52.3", RED),
            ("　うち遮断解除〜離脱", 10.0, "同時発生 OR 10.0", ORANGE),
            ("体外循環後", 12.7, "同時発生 OR 12.7", PURPLE)]
    x0, y0 = 460, 140
    bw = W - x0 - 110
    mx = 60.0
    yy = y0
    for lab, v, note, col in BARS:
        cv.text(x0 - 24, yy + 30, lab, size=11.0, color=INK, ha="right")
        blen = max(6, bw * v / mx)
        cv.rect(x0, yy + 12, blen, 38, fc=col, ec="none")
        # 棒が長いと注記が枠から出るので、そのときは棒の中に白字で入れる
        if x0 + blen + 24 + cv.width(note, 10.4, "bold") > W - 70:
            cv.text(x0 + blen - 18, yy + 31, note, size=10.4, color="white",
                    weight="bold", ha="right")
        else:
            cv.text(x0 + blen + 16, yy + 31, note, size=10.4,
                    color=col, weight="bold", ha="left")
        yy += 72

    y = yy + 24
    w = (W - 140 - 30) / 2
    th1 = textbox(cv, 70, y, w,
                  ["脳酸素が下がっていると、抑制のオッズは 1.52 倍",
                   "（95%CI 1.11〜2.07、P=.009）",
                   "体外循環中の脳酸素低下は OR 22.1",
                   "体外循環後の脳酸素低下は OR 18.2"],
                  10.6, style="teal", title="別々に見ると", title_color=TEAL,
                  pad_y=16)
    th2 = textbox(cv, 70 + w + 30, y, w,
                  ["体外循環中のバーストサプレッションがあった群のせん妄 25%",
                   "なかった群は 6%（多変量で OR 4.1、95%CI 1.5〜13.7）",
                   "抑制の予測因子は最低体温 OR 0.73 と α パワー OR 0.61",
                   "吸入麻酔薬 0.1% 増加ごとに抑制 OR 7.81"],
                  10.6, style="red", title="抑制とせん妄", title_color=RED,
                  pad_y=16)
    msg(cv, y + max(th1, th2) + 28,
        "遮断解除から離脱までの十数分が、脳にとって最も危うい時間帯である")
    cv.save(P("s10_desat_burst.png"))
    crop_bottom(P("s10_desat_burst.png"))


# ---------------------------------------------------------------- s11
def s11():
    """術中覚醒の数字"""
    cv = Canvas(W, 1250)
    cap(cv, 44, "術中覚醒 ── 心臓外科は、名指しされた危険因子である")

    y0 = 130
    cv.box(70, y0, W - 140, 110, fc="#eaf0f8", ec=NAVY, lw=1.8, radius=10)
    t = "英国 NAP5：全国の麻酔活動調査を分母とした発生率"
    cv.text(W / 2, y0 + 42, t, size=fit(cv, t, W - 220, 12.6, "bold"),
            color=NAVY, weight="bold")
    cv.text(W / 2, y0 + 82, "約 1:19,600（95%CI 1:16,700〜23,450）",
            size=12.0, color=INK)

    CARDS = [("筋弛緩薬を使ったとき", "1:8,200", RED, "#fceeec"),
             ("筋弛緩薬を使わないとき", "1:135,900", GREEN, "#eaf5ee"),
             ("帝王切開", "1:670", ORANGE, "#fdf3e6")]
    w = (W - 140 - 2 * 28) / 3
    yy = y0 + 140
    for i, (lab, val, col, fc) in enumerate(CARDS):
        x = 70 + (w + 28) * i
        cv.box(x, yy, w, 170, fc=fc, ec=col, lw=1.8, radius=10)
        cv.text(x + w / 2, yy + 46, lab, size=fit(cv, lab, w - 30, 11.2),
                color=INK)
        cv.text(x + w / 2, yy + 112, val,
                size=fit(cv, val, w - 40, 24.0, "bold"), color=col,
                weight="bold")

    y = yy + 200
    w2 = (W - 140 - 30) / 2
    th1 = textbox(cv, 70, y, w2,
                  ["女性", "若年成人（小児ではない）", "肥満",
                   "研修医が担当", "時間外・緊急", "産科・心臓外科・胸部外科",
                   "筋弛緩薬の使用"],
                  10.6, style="red", title="危険因子とされたもの", title_color=RED,
                  pad_y=16)
    th2 = textbox(cv, 70 + w2 + 30, y, w2,
                  ["66% は導入と覚醒、つまり「動きのある局面」で起きた",
                   "導入ではチオペンタール・迅速導入・肥満・困難気道・",
                   "麻酔導入室から手術室への移動中の投与の途切れ",
                   "覚醒では、残存筋弛緩が「覚醒」として体験された",
                   "維持期に起きたものの多くは、導入か終盤の問題に由来する"],
                  10.6, style="amber", title="いつ、どこで起きたか",
                  title_color="#9a6510", pad_y=16)
    msg(cv, y + max(th1, th2) + 28,
        "体外循環の前後と、筋弛緩からの回復を、意識して見張る")
    cv.save(P("s11_awareness.png"))
    crop_bottom(P("s11_awareness.png"))


# ---------------------------------------------------------------- s12
def s12():
    """麻酔深度の主要試験一覧"""
    cv = Canvas(W, 2100)
    cap(cv, 44, "「深さ」を割り付けた試験が示したこと")

    ROWS = [("B-Aware", "2004", "2,463 例・覚醒高リスク",
             "BIS ガイド 対 通常管理",
             "覚醒 2 例 対 11 例（P=0.022）、相対危険減少 82%", GREEN),
            ("BAG-RECALL", "2011", "6,041 例・覚醒高リスク",
             "BIS 対 呼気終末麻酔薬濃度",
             "確定覚醒 0.24% 対 0.07%。BIS の優越性は示されず", ORANGE),
            ("（心臓外科の下位解析）", "2013", "723 例",
             "BIS 対 呼気終末麻酔薬濃度",
             "抜管までの時間に差なし（OR 1.04、95%CI 0.88〜1.23）", ORANGE),
            ("BALANCED", "2019", "6,644 例・60歳以上の大手術",
             "BIS 50 目標 対 BIS 35 目標",
             "1年死亡 6.5% 対 7.2%（HR 0.88、95%CI 0.73〜1.07）", BLUE),
            ("ENGAGES", "2019", "1,232 例・大手術",
             "脳波ガイド 対 通常管理",
             "せん妄 26.0% 対 23.0%（差 3.0%、95%CI -2.0〜8.0）", PURPLE),
            ("ENGAGES 1年追跡", "2021", "1,232 例",
             "同上",
             "1年死亡 9.6% 対 10.3%（絶対差 -0.7%）", PURPLE),
            ("ENGAGES-Canada", "2024", "1,140 例・心臓手術",
             "脳波ガイド 対 通常管理",
             "せん妄 18.15% 対 18.10%。抑制時間 4.0 分 対 11.7 分", RED)]

    y = 130
    for name, yr, pop, arm, res, col in ROWS:
        h = 178
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.6, radius=8)
        cv.box(70, y, 260, h, fc=col, ec=col, lw=0, radius=8)
        cv.text(200, y + 68, name, size=fit(cv, name, 230, 12.0, "bold"),
                color="white", weight="bold")
        cv.text(200, y + 110, yr, size=11.0, color="white")
        cv.text(360, y + 44, pop, size=fit(cv, pop, W - 500, 10.8),
                color=GREY, ha="left")
        cv.text(360, y + 86, arm, size=fit(cv, arm, W - 500, 11.0, "bold"),
                color=col, ha="left", weight="bold")
        for j, ln in enumerate(cv.wrap(res, W - 500, 10.8)):
            cv.text(360, y + 128 + LH(10.8, 1.35) * j, ln, size=10.8, color=INK, ha="left")
        y += h + 14

    th = textbox(cv, 70, y + 16, W - 140,
                 ["覚醒を減らすという目的では、比較対象が「通常管理」なら差が出た。",
                  "比較対象を「呼気終末麻酔薬濃度の監視」にすると、差は消えた。",
                  "死亡やせん妄という目的では、"
                  "深さを割り付けても差は出ていない。",
                  "心臓外科に限った ENGAGES-Canada でも、"
                  "抑制時間は三分の一に減ったが、せん妄は動かなかった。"],
                 11.0, style="navy", title="四つの試験から読めること",
                 title_color=NAVY, pad_y=18)
    cv.save(P("s12_depth_trials.png"))
    crop_bottom(P("s12_depth_trials.png"))


# ---------------------------------------------------------------- s13
def s13():
    """揮発性麻酔薬と全静脈麻酔"""
    cv = Canvas(W, 1250)
    cap(cv, 44, "揮発性麻酔薬と全静脈麻酔 ── メタ解析と大規模試験が食い違う")

    y0 = 130
    cv.box(70, y0, W - 140, 276, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    t = "MYRIAD：待機的冠動脈バイパス 5,400 例（無益性のため中止）"
    cv.text(W / 2, y0 + 40, t, size=fit(cv, t, W - 220, 12.2, "bold"),
            color=NAVY, weight="bold")
    PAIR = [("1 年死亡", "2.8%", "3.0%"), ("30 日死亡", "1.4%", "1.3%")]
    w2 = (W - 200) / 2
    for i, (lab, a, b) in enumerate(PAIR):
        x = 100 + w2 * i
        cv.text(x + w2 / 2, y0 + 92, lab, size=11.4, color=INK)
        duo(cv, x + w2 / 2, y0 + 156, a, b, size=24, col_a=BLUE,
            lab_a="揮発性", lab_b="全静脈", lab_dy=46, max_w=w2 - 30)
    cv.text(W / 2, y0 + 248, "相対危険 0.94（95%CI 0.69〜1.29、P=0.71）",
            size=10.6, color=GREY)

    y = y0 + 306
    w = (W - 140 - 30) / 2
    th1 = textbox(cv, 70, y, w,
                  ["別の多施設無作為化試験 3,083 例（2024）",
                   "主要複合転帰 33.8% 対 33.2%",
                   "（RR 1.02、95%CI 0.92〜1.12、P=0.76）",
                   "弁手術 30,755 例の全国データ（2024）",
                   "1年死亡 HR 0.98（95%CI 0.90〜1.07）"],
                  10.6, style="blue", title="差がないとする側", title_color=BLUE,
                  pad_y=16)
    th2 = textbox(cv, 70 + w + 30, y, w,
                  ["42 研究・8,197 例のメタ解析（2020）",
                   "1年死亡 5.5% 対 6.8%",
                   "（OR 0.76、95%CI 0.60〜0.96、P=0.023）",
                   "心筋梗塞 OR 0.60、トロポニン放出も低い",
                   "小規模試験を足し合わせると差が見える"],
                  10.6, style="green", title="差があるとする側",
                  title_color=GREEN, pad_y=16)

    yy = y + max(th1, th2) + 28
    th3 = textbox(cv, 70, yy, W - 140,
                  ["麻酔科にとっての含意は、「どちらでもよい」ではなく",
                   "「この選択で転帰は決まらないから、"
                   "別の理由で選んでよい」ということである。",
                   "別の理由とは、循環の安定性、覚醒の速さ、"
                   "術後悪心、そして脳波の読みやすさである。"],
                  10.8, style="grey", title="では何で選ぶのか",
                  title_color=NAVY, pad_y=18)
    cv.save(P("s13_volatile_tiva.png"))
    crop_bottom(P("s13_volatile_tiva.png"))


# ---------------------------------------------------------------- s14
def s14():
    """せん妄をめぐる試験一覧"""
    cv = Canvas(W, 2200)
    cap(cv, 44, "心臓手術後のせん妄 ── 何を試し、何が変わらなかったか")

    ROWS = [("脳酸素モニタ", "249 例・無作為化",
             "rSO2 が基準の 75% を割ったら介入",
             "24.4% 対 24.6%（OR 0.98）", "変わらず", RED),
            ("脳酸素モニタ", "オフポンプ CABG・2026",
             "脳酸素ガイド 対 通常管理",
             "有意差なし（70 歳超では数値上の減少）", "変わらず", RED),
            ("多部位 NIRS", "1,960 例・Bottomline-CS",
             "組織酸素と血行動態のガイド",
             "主要複合転帰 47.3% 対 47.8%（RR 0.99）", "変わらず", RED),
            ("自動調節能", "199 例・入れ子無作為化",
             "下限より高い MAP を目標",
             "38% 対 53%（OR 0.55、95%CI 0.31〜0.97）", "減った", GREEN),
            ("自動調節能", "高リスク例・2021",
             "個別化した血圧目標",
             "8.2% 対 14.9%（RR 0.55、95%CI 0.32〜0.93）", "減った", GREEN),
            ("脳波ガイド麻酔", "1,140 例・ENGAGES-Canada",
             "抑制を減らすよう麻酔を調整",
             "18.15% 対 18.10%", "変わらず", RED),
            ("デクスメデトミジン", "794 例・DECADE",
             "導入時から 24 時間持続",
             "17% 対 12%（RR 1.48）むしろ増加傾向", "変わらず", RED),
            ("デクスメデトミジン", "331 例・術後夜間投与",
             "術後の夜だけ持続",
             "12.6% 対 12.4%。低血圧 7.3% 対 0.6%", "変わらず", RED),
            ("アセトアミノフェン", "121 例・DEXACET",
             "静注アセトアミノフェン併用",
             "10% 対 28%（差 -18%、95%CI -32〜-5）", "減った", GREEN),
            ("ケタミン", "672 例・PODCAST",
             "0.5／1.0 mg/kg",
             "19.45% 対 19.82%", "変わらず", RED),
            ("エスケタミン", "112 例・弁手術",
             "体外循環下の弁手術",
             "23.2% 対 44.6%（RR 0.52、95%CI 0.28〜0.91）", "減った", GREEN)]

    y = 130
    for what, pop, arm, res, verdict, col in ROWS:
        h = 126
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.4, radius=8)
        cv.box(70, y, 300, h, fc=col, ec=col, lw=0, radius=8)
        cv.text(220, y + 46, what, size=fit(cv, what, 260, 11.4, "bold"),
                color="white", weight="bold")
        cv.text(220, y + 84, verdict, size=10.6, color="white")
        cv.text(400, y + 40, pop, size=fit(cv, pop, 330, 10.4), color=GREY,
                ha="left")
        cv.text(400, y + 84, arm, size=fit(cv, arm, 330, 10.6), color=INK,
                ha="left")
        cv.text(760, y + h / 2, res, size=fit(cv, res, W - 860, 11.0, "bold"),
                color=col, ha="left", weight="bold")
        y += h + 10

    th = textbox(cv, 70, y + 16, W - 140,
                 ["減ったのは、血圧を個別化した二つの試験と、"
                  "鎮痛を足した一つの試験である。",
                  "モニタを足しただけ、薬を足しただけでは変わらなかった。",
                  "ネットワークメタ解析では"
                  "デクスメデトミジン＋メラトニンが最上位（RR 0.31）だが、"
                  "確実性は低い。"],
                 10.8, style="navy", title="並べて見えること",
                 title_color=NAVY, pad_y=18)
    cv.save(P("s14_delirium_trials.png"))
    crop_bottom(P("s14_delirium_trials.png"))


# ---------------------------------------------------------------- s15
def s15():
    """アルゴリズム：術中に脳波・脳酸素が変化したとき"""
    cv = Canvas(W, 2500)
    cap(cv, 44, "アルゴリズム　術中に脳波または脳酸素が変わったとき")

    STEPS = [("① まず、患者ではなく機械を疑う", "#e8edf5", NAVY,
              ["プローブ・電極の位置、外光、接触不良",
               "電気メス・ペーシング・補助循環の雑音",
               "体温を確認する（低体温だけで指数は下がる）"]),
             ("② 脳波が深くなった（抑制が出た）とき", "#fdf3e6", ORANGE,
              ["麻酔薬を減らす。ただし「深いから」ではなく「抑制だから」",
               "同時に血圧・脳酸素・体温を見る",
               "薬を減らしても抑制が続くなら、脳の側の問題を考える",
               "α パワーが低い患者はもともと抑制が出やすい"]),
             ("③ 脳酸素が下がったとき（供給・需要・血管・信号）", "#e4f2f4", TEAL,
              ["供給：ポンプ流量・Hb・動脈血酸素分圧・二酸化炭素分圧",
               "需要：体温・麻酔深度・けいれん",
               "血管：送血管の位置・分枝の遮断・頭位・頸動脈病変",
               "昇圧薬で上げても rSO2 は上がらないことがある"]),
             ("④ 左右差があるとき", "#f1ecf8", PURPLE,
              ["送血管の位置と、分枝の灌流をまず疑う",
               "外科医に伝え、送血の経路を確認してもらう",
               "頸部の体位（過度の回旋・屈曲）を直す"]),
             ("⑤ 遮断解除から離脱までは、別枠で見る", "#fceeec", RED,
              ["この区間で脳酸素低下と抑制の同時発生が最も多い",
               "（体外循環前と比べて同時発生 OR 10.0）",
               "復温速度・目標体温・血圧を、この区間だけ別に決めておく"]),
             ("⑥ 記録に残す", "#eaf5ee", GREEN,
              ["抑制が出ていた時間と、そのときの体温・血圧・薬物濃度",
               "脳酸素の基準値と、基準値から外れていた時間",
               "介入の内容と、介入後にどう戻ったか"])]

    y = 130
    for head, fc, col, lines in STEPS:
        hs = fit(cv, head, W - 240, 12.4, "bold")
        h = 46 + LH(hs, 1.5) + LH(10.6, 1.75) * len(lines)
        cv.box(70, y, W - 140, h, fc=fc, ec=col, lw=1.8, radius=10)
        cv.text(W / 2, y + 34, head, size=hs, color=col, weight="bold")
        for j, ln in enumerate(lines):
            s = fit(cv, ln, W - 220, 10.6)
            cv.text(W / 2, y + 46 + LH(hs, 1.5) + LH(10.6, 1.75) * (j + 0.5),
                    ln, size=s, color=INK)
        y += h + 20
        if head.startswith("①") or head.startswith("③"):
            cv.arrow((W / 2, y - 16), (W / 2, y - 2), color=GREY, lw=2.2)

    msg(cv, y + 8,
        "モニタは「異常を教える」。何をするかは、あらかじめ決めておく")
    cv.save(P("s15_alg_monitor.png"))
    crop_bottom(P("s15_alg_monitor.png"))


# ---------------------------------------------------------------- s16
def s16():
    """この章の「測れること」と「転帰」"""
    cv = Canvas(W, 2300)
    cap(cv, 44, "この章でも、「測れること」は「転帰が変わること」とは別であった")

    ROWS = [("処理脳波指数", "麻酔薬の量を減らせる",
             "ENGAGES-Canada でせん妄 18.15% 対 18.10%", BLUE),
            ("脳波の抑制", "抑制時間を三分の一にできる（4.0 分 対 11.7 分）",
             "それでもせん妄も死亡も動かなかった", BLUE),
            ("麻酔の深さ", "BIS 50 と 35 に確実に分けられる",
             "1年死亡 6.5% 対 7.2%（HR 0.88）", PURPLE),
            ("脳酸素モニタ", "脱飽和を検出し、基準値に戻せる",
             "Bottomline-CS で主要転帰 47.3% 対 47.8%", TEAL),
            ("経頭蓋ドプラ", "塞栓の数を数えられる（79 個 対 3 個）",
             "どちらの群にも臨床的な神経脱落はなかった", TEAL),
            ("自動調節能", "その患者の下限・最適値を出せる",
             "せん妄は減った（38% 対 53%、8.2% 対 14.9%）", GREEN),
            ("デクスメデトミジン", "鎮静を得られ、挿管時間を短くできる",
             "DECADE でせん妄 17% 対 12%（むしろ増加傾向）", RED),
            ("塞栓防止デバイス", "デブリを捕捉できる",
             "TAVI の無症候性梗塞の発生率は減らなかった", ORANGE)]

    y = 130
    for what, can, but, col in ROWS:
        h = 168
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.5, radius=8)
        cv.box(70, y, 330, h, fc=col, ec=col, lw=0, radius=8)
        wl = cv.wrap(what, 290, 11.6, "bold")
        for j, ln in enumerate(wl):
            cv.text(235, y + h / 2 - 16 * (len(wl) - 1) + 32 * j, ln,
                    size=11.6, color="white", weight="bold")
        cv.text(430, y + 52, "測れる／できる", size=9.8, color=GREY, ha="left")
        cv.text(430, y + 84, can, size=fit(cv, can, W - 530, 11.2, "bold"),
                color=col, ha="left", weight="bold")
        cv.text(430, y + 124, but, size=fit(cv, but, W - 530, 10.8),
                color=INK, ha="left")
        y += h + 12

    th = textbox(cv, 70, y + 16, W - 140,
                 ["この一覧は、モニタを外す理由ではない。",
                  "そのモニタが答える問いを決め、"
                  "外れたときに何をするかを決めておくための一覧である。",
                  "そして、決めた介入が転帰を変えるかどうかは、"
                  "まだ多くが分かっていない。"],
                 11.0, style="navy", title="この表の使い方",
                 title_color=NAVY, pad_y=18)
    cv.save(P("s16_measure_vs_outcome.png"))
    crop_bottom(P("s16_measure_vs_outcome.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (s09, s10, s11, s12, s13, s14, s15, s16):
        fn()
        print("ok", fn.__name__)
