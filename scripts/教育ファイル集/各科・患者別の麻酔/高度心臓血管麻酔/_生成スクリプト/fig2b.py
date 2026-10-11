# -*- coding: utf-8 -*-
"""第Ⅱ章 大動脈手術の脳保護　図版 g08〜g13"""
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
from figcrop import crop_bottom

OUT = sys.argv[1] if len(sys.argv) > 1 else "fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = JP
plt.rcParams["axes.unicode_minus"] = False


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- g08
def g08():
    """rSO2 が下がったときの鑑別"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "rSO2 が下がった ── 何が足りていないのかを分けて考える")

    cx = W / 2
    TW = 580
    cv.box(cx - TW / 2, 110, TW, 76, fc="#fceeec", ec=RED, lw=2.0, radius=10)
    tt = "rSO2 が baseline から低下した"
    cv.text(cx, 148, tt, size=cv.fit_size([tt], TW - 60, 12.4, weight="bold"),
            color=RED, weight="bold")

    ITEMS = [("供給側：運ぶ量", BLUE, "#eaf1f8",
              ["ポンプ流量は足りているか", "Hb は下がっていないか",
               "送血カニューレの位置は", "分枝が遮断されていないか"]),
             ("需要側：使う量", PURPLE, "#f1ecf8",
              ["温度は狙いどおりか", "麻酔深度は足りているか",
               "けいれんを起こしていないか"]),
             ("血管側：流れる条件", GREEN, "#eaf5ee",
              ["PaCO2 は適切か（過換気は血管を締める）",
               "静脈のうっ滞はないか（上大静脈圧）",
               "頭位・カニューレによる静脈閉塞"]),
             ("信号側：本当に脳か", ORANGE, "#fdf3e3",
              ["センサの貼付位置・接触", "頭蓋外の血流の影響",
               "左右差があるか（片側なら灌流の偏り）"])]

    w = (W - 140 - 90) / 4
    for i, (t, col, fc, lines) in enumerate(ITEMS):
        x = 70 + (w + 30) * i
        cv.arrow((cx, 190), (x + w / 2, 236), color="#b9c2cc", lw=1.6, head=8)
        card(cv, x, 240, w, t, lines, col, fc, body_size=10.0, lh=1.8)

    th = textbox(cv, 70, 640, W - 140,
                 ["CPB 中に昇圧薬で平均血圧を 45 mmHg から 67 mmHg へ上げた"
                  "無作為化試験では、",
                  "平均 rSO2 はむしろ低下し（差 3.5、95%CI 0.9-6.1）、",
                  "baseline から 10% 以上・20% 以上低下する患者が高血圧群で多かった。",
                  "著者らは「脳酸素飽和度の低下に対して昇圧薬で血圧を上げることは"
                  "勧められない」と結論している。"],
                 10.6, style="red", title="反射的に昇圧してはいけない",
                 title_color=RED, pad_y=16)

    msg(cv, 640 + th + 30,
        "rSO2 低下は「血圧を上げる合図」ではなく、「原因を探す合図」である",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("g08_rso2_differential.png"))


# ---------------------------------------------------------------- g09
def g09():
    """GERAADA 早期と長期"""
    cv = Canvas(W, 900)
    cap(cv, 44, "神経合併症は、手術室を出たあとも起こる")

    PW = (W - 190) / 2
    PY, PH = 130, 520
    x1, x2 = 70, 70 + PW + 50

    def donut(x, title, color, pct, n_txt, lines):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        ts = cv.fit_size([title], PW - 44, 12.0, weight="bold")
        cv.text(x + PW / 2, PY + 34, title, size=ts, color=color,
                weight="bold")
        # 100 マスで割合を示す
        gx, gy = x + PW / 2 - 200, PY + 84
        for k in range(100):
            r, c = divmod(k, 20)
            fc = color if k < pct else "#e8ecf0"
            cv.rect(gx + c * 20, gy + r * 20, 15, 15, fc=fc)
        cv.text(x + PW / 2, gy + 122, "%d%%" % pct, size=22, color=color,
                weight="bold")
        cv.text(x + PW / 2, gy + 156, n_txt, size=10.0, color=GREY)
        s, bl = fitlines(cv, lines, PW - 60, 10.2)
        for j, ln in enumerate(bl):
            cv.text(x + PW / 2, PY + 366 + LH(s, 1.7) * (j + 0.5), ln,
                    size=s, color=INK)

    donut(x1, "入院中の新規神経障害", RED, 15, "2,686 例中 415 例",
          ["危険因子は年齢・腎灌流障害・弓部分枝の解離・",
           "体外循環時間・再開胸",
           "部分弓部置換はむしろ保護的（OR 0.68）"])
    donut(x2, "退院後に生じた二次性の神経障害", PURPLE, 23,
          "追跡できた 814 例中 188 例",
          ["中央値 10.2 年の追跡",
           "長期の危険因子は遷延する脳灌流障害と晩期再手術",
           "周術期の術式と長期転帰に関連は見いだせなかった"])

    textbox(cv, 70, PY + PH + 26, W - 140,
            ["同じ登録研究では、脳保護の方法（ACP・RCP・単独循環停止）も"
             "温度管理も、",
             "入院中の神経学的転帰に有意差を生まなかった。",
             "「どの方法を選ぶか」よりも、"
             "灌流障害を残さないことと、退院後も診ることが効いている。"],
            10.6, style="navy", pad_y=14)
    cv.save(P("g09_geraada.png"))


# ---------------------------------------------------------------- g10
def g10():
    """FET における脳と脊髄"""
    cv = Canvas(W, 960)
    cap(cv, 44, "弓部を治すと、脊髄が危なくなる")

    cv.box(70, 130, W - 140, 150, fc="#f4f6f9", ec="#c9d2dc", lw=1.6,
           radius=10)
    cv.text(W / 2, 176, "frozen elephant trunk（弓部置換＋下行大動脈ステント）",
            size=12.4, color=NAVY, weight="bold")
    cv.text(W / 2, 226,
            "弓部を人工血管で置換し、下行大動脈にステントグラフトを伸ばす",
            size=10.6, color=INK)

    NUM = [("脊髄虚血", "4.7%", "95%CI 3.5-6.2", RED, "#fceeec"),
           ("脳卒中", "7.6%", "95%CI 5.0-11.5", BLUE, "#eaf1f8"),
           ("手術死亡", "8.8%", "95%CI 7.0-10.9", GREY, "#f2f4f6")]
    w = (W - 140 - 60) / 3
    for i, (lab, val, ci, col, fc) in enumerate(NUM):
        x = 70 + (w + 30) * i
        cv.box(x, 320, w, 170, fc=fc, ec=col, lw=1.8, radius=10)
        cv.text(x + w / 2, 358, lab, size=11.6, color=col, weight="bold")
        cv.text(x + w / 2, 410, val, size=26, color=col, weight="bold")
        cv.text(x + w / 2, 456, ci, size=9.8, color=GREY)

    cv.text(W / 2, 520, "35 研究 3,154 例のメタ解析", size=10.2, color=GREY)

    th = textbox(cv, 70, 556, W - 140,
                 ["ステントの長さが 15 cm 以上、あるいは被覆が T8 以遠に及ぶと、",
                  "脊髄虚血の発生率が高くなる。",
                  "弓部の手術でありながら、"
                  "下行大動脈をどこまで覆うかが脊髄の運命を決める。"],
                 10.6, style="red", title="どこまで覆うかで変わる",
                 title_color=RED, pad_y=16)

    msg(cv, 556 + th + 28, "第Ⅲ章（脊髄保護）は、ここから始まる")
    cv.save(P("g10_fet.png"))


# ---------------------------------------------------------------- g11
def g11():
    """Alg2-1 脳保護戦略の選択"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 1　弓部手術の脳保護戦略を決める")

    cx = W / 2
    bw = 740
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["部分弓部置換か、全弓部置換か、frozen elephant trunk か",
              "循環停止はおよそ何分になりそうか",
              "弓部分枝に解離・狭窄・石灰化はないか"],
             style="navy", title="① 何をする手術かを共有する",
             title_color=NAVY)
    y += h
    down(cv, cx, y, y + 46)
    y += 46
    cw = 460
    lx, rx = 70, W - 70 - cw
    side(cv, cx - 40, lx + cw + 10, y + 70)
    side(cv, cx + 40, rx - 10, y + 70)
    hl = step(cv, lx, y, cw,
              ["停止時間が短く見込める（部分弓部など）",
               "RCP は脳灌流なしより脳卒中が少ない",
               "空気・デブリの洗い出しを狙える"],
              style="green", title="短時間の循環停止", title_color=GREEN)
    hr = step(cv, rx, y, cw,
              ["停止時間が長くなる（全弓部・FET）",
               "ACP を選び、灌流圧と流量を決めておく",
               "片側か両側かは解剖と停止時間で決める"],
              style="blue", title="長時間の循環停止", title_color=BLUE)
    y += max(hl, hr)
    down(cv, lx + cw / 2, y, y + 44)
    down(cv, rx + cw / 2, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["深く冷やすほど安全とは限らない（DHCA は MHCA より脳卒中が多い）",
              "一方で、停止時間が長いなら冷却の裏づけが要る",
              "施設が慣れている温度帯を基準にし、術式で微調整する"],
             style="amber", title="② 温度を決める", title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 46)
    y += 46
    h = step(cv, cx - bw / 2, y, bw,
             ["送血部位（腋窩・大腿・上行・腕頭）と ACP への移行手順",
              "NIRS の baseline を麻酔導入前に取る",
              "左右差を見るため両側にセンサを貼る",
              "脳波・TCD を使うなら、誰が見るかを決めておく"],
             style="blue", title="③ 入室前に整えるもの", title_color=BLUE)
    y += h
    down(cv, cx, y, y + 46)
    y += 46
    step(cv, cx - bw / 2, y, bw,
         ["循環停止に入る時刻と、ACP 開始時刻を全員で共有する",
          "rSO2 の低下は、低下幅と持続時間で記録する",
          "復温の速度と到達温度を決めておく（過度の高温は避ける）"],
         style="purple", title="④ 術中に共有し続けること",
         title_color=PURPLE)
    cv.save(P("g11_alg_strategy.png"))
    crop_bottom(P("g11_alg_strategy.png"))


# ---------------------------------------------------------------- g12
def g12():
    """Alg2-2 rSO2 低下時の対応"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 2　rSO2 が下がったときの手順")

    cx = W / 2
    bw = 780
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["何%下がったか（baseline 比）、いつから、片側か両側か",
              "同時に何をしていたか（送血開始・遮断・体位・カニューレ操作）"],
             style="navy", title="① まず、下がり方を言葉にする",
             title_color=NAVY)
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    cw = 520
    lx, rx = 70, W - 70 - cw
    hl = step(cv, lx, y, cw,
              ["片側だけ下がっている",
               "→ 送血の偏り、カニューレ位置、分枝の閉塞を疑う",
               "→ 外科医に伝え、灌流経路を確認する"],
              style="red", title="左右差があるとき", title_color=RED)
    hr = step(cv, rx, y, cw,
              ["両側が同じように下がっている",
               "→ 流量・Hb・PaCO2・温度・麻酔深度を順に確認する",
               "→ センサや機器の問題も除外する"],
              style="blue", title="左右差がないとき", title_color=BLUE)
    y += max(hl, hr)
    down(cv, lx + cw / 2, y, y + 42)
    down(cv, rx + cw / 2, y, y + 42)
    y += 42
    h = step(cv, cx - bw / 2, y, bw,
             ["ポンプ流量を上げる（送れる量を増やす）",
              "Hb を上げる（運べる量を増やす）",
              "PaCO2 を上げる（血管を開く）",
              "温度と麻酔深度で需要を下げる"],
             style="green", title="② 原因に対応した手を打つ",
             title_color=GREEN)
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    h = step(cv, cx - bw / 2, y, bw,
             ["昇圧薬で血圧だけを上げても rSO2 は上がらないことがある",
              "無作為化試験では、MAP を上げた群でむしろ脳酸素飽和度が低く、"
              "脱飽和も多かった",
              "血圧は「原因を直した結果」として上がるのが望ましい"],
             style="red", title="③ 昇圧薬に手を伸ばす前に", title_color=RED)
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    step(cv, cx - bw / 2, y, bw,
         ["何をして、どう戻ったかを記録に残す",
          "戻らなかった場合は、循環停止・ACP の時刻と合わせて術後に共有する",
          "覚醒遅延があれば、この記録が鑑別の出発点になる"],
         style="purple", title="④ 記録する", title_color=PURPLE)
    cv.save(P("g12_alg_rso2.png"))
    crop_bottom(P("g12_alg_rso2.png"))


# ---------------------------------------------------------------- g13
def g13():
    """Alg2-3 A 型解離の麻酔導入"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 3　急性 A 型解離の麻酔導入")

    cx = W / 2
    bw = 780
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["両上肢と下肢の血圧を測る（左右差・上下肢差は灌流障害のサイン）",
              "意識・四肢の動き・瞳孔を、導入前に必ず記録する",
              "心嚢液・大動脈弁逆流・冠動脈への波及を確認する"],
             style="navy", title="① 入室直後に決めること", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    h = step(cv, cx - bw / 2, y, bw,
             ["太い静脈路、動脈圧ライン（測る側を外科医と相談する）",
              "交差適合済みの血液を手元に",
              "外科医と灌流技士が入室してから導入する"],
             style="red", title="② 導入前にそろえるもの", title_color=RED)
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    h = step(cv, cx - bw / 2, y, bw,
             ["血圧を上げない（咳・体動・喉頭展開の反応を抑える）",
              "血圧を下げすぎない（灌流障害のある臓器がある）",
              "タンポナーデがあれば、導入で循環が破綻しうる",
              "その場合は消毒・ドレープを先に済ませてから導入する"],
             style="amber", title="③ 導入の原則", title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    h = step(cv, cx - bw / 2, y, bw,
             ["entry の位置、偽腔の広がり、弓部分枝への波及",
              "大動脈弁逆流の機序と程度",
              "心嚢液と右心系の圧排",
              "送血部位の真腔・偽腔（送血開始後の再評価も）"],
             style="blue", title="④ 導入後の TEE で見るもの", title_color=BLUE)
    y += h
    down(cv, cx, y, y + 42)
    y += 42
    step(cv, cx - bw / 2, y, bw,
         ["送血開始直後に灌流障害が出ることがある",
          "NIRS の左右差、上肢下肢の圧差、尿量、乳酸を続けて見る",
          "「導入が終われば一段落」ではない"],
         style="purple", title="⑤ 送血開始後", title_color=PURPLE)
    cv.save(P("g13_alg_dissection.png"))
    crop_bottom(P("g13_alg_dissection.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (g08, g09, g10, g11, g12, g13):
        fn()
        print("ok", fn.__name__)
