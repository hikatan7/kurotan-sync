# -*- coding: utf-8 -*-
"""第18巻 呼吸管理と分離肺換気 図版 f11〜f20"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Wedge
from figlib import Canvas, LH, NAVY, INK, JP, textbox
from figkit import two_col, three_col, rows, note, banner

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP

BLUE, RED, GREEN, AMBER, PURPLE, GREY = ("#2e6da4", "#c0392b", "#1f6b47",
                                         "#b8760f", "#7b52a8", "#5d6875")


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f11
def f11():
    W, H = 1520, 800
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "肺を分ける理由は二つ —— 「守る」ためか、「見る」ためか",
             size=12.5, ha="center")
    y = two_col(cv, W, 92, [
        ("絶対的な適応｜反対側の肺を守る", RED, "#fceeec",
         ["大量喀血（血液が健側へ流れ込むのを防ぐ）",
          "片側の感染・膿瘍（膿を渡さない）",
          "気管支胸膜瘻・気道の大きな損傷（陽圧がリークへ逃げる）",
          "片肺全体の気道閉塞や、巨大ブラの破裂の危険",
          "気管支肺胞洗浄（片側ずつ洗う）",
          "共通するのは「両肺をつなげたままでは危険」という状況"]),
        ("相対的な適応｜術野を作る", BLUE, "#eaf1f8",
         ["胸腔鏡・ロボット支援の肺切除（肺を虚脱させないと視野が取れない）",
          "開胸の肺葉切除・区域切除",
          "食道手術、縦隔腫瘍",
          "胸部大動脈の手術",
          "共通するのは「安全のためではなく、手術のため」",
          "だから、危険が上回るなら両肺換気に戻す判断が常にある"]),
    ], body_sz=10.0)
    y = banner(cv, W, y + 26,
               "相対的適応での分離肺換気は「戻せる選択」である。"
               "低酸素が続くなら、術野より換気を優先する",
               col=GREEN, fc="#eaf5ee", tc="#1f6b47")
    note(cv, W, y + 30,
         "※ 絶対的適応では、分離を解除すること自体が危険になる。"
         "この違いを最初に共有しておくと、術中の判断が速い。")
    cv.save(P("f11_olv_indication.png"))


# ---------------------------------------------------------------- f12
def f12():
    W, H = 1520, 820
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "ダブルルーメンチューブと気管支ブロッカー —— どちらを選ぶか",
             size=12.5, ha="center")
    y = two_col(cv, W, 92, [
        ("ダブルルーメンチューブ", BLUE, "#eaf1f8",
         ["虚脱が速く、確実。吸引もできる",
          "左右の換気を独立して操作できる（片側だけ呼気終末陽圧など）",
          "太いので、挿管困難・気道狭窄・小柄な体格では入りにくい",
          "術後に人工呼吸を続けるなら、単管への入れ替えが要る",
          "体位変換で位置がずれやすく、再確認が要る"]),
        ("気管支ブロッカー", AMBER, "#fdf3e3",
         ["通常の単管に通すため、挿管困難でも使いやすい",
          "術後もそのまま人工呼吸を続けられる",
          "虚脱は遅く、分泌物や血液の吸引はしにくい",
          "位置がずれると、主気管支まで戻って両肺を塞ぐことがある",
          "小児・気管切開・気道の変形では選択肢になる"]),
    ], body_sz=10.0)
    y = rows(cv, W, y + 24, [
        ("原則は左用を使う", GREEN,
         ["右上葉枝の分岐が近いため、右用は位置の許容範囲が狭い。",
          "左主気管支に病変がある、左肺全摘で左に置けない、といった場合に右用を考える。"]),
        ("サイズは身長と気管径から", BLUE,
         ["体重ではなく身長を手がかりにし、可能なら画像で気管・左主気管支径を確認する。",
          "太すぎれば気道損傷、細すぎればリークと位置のずれを招く。"]),
        ("どちらでも位置確認は気管支鏡", PURPLE,
         ["聴診だけでは位置異常を見逃す。挿入後と体位変換後の二度、必ず見る。",
          "「見ないで進めない」は気道でも同じである。"]),
    ], name_sz=10.4, body_sz=10.2, lh=1.55)
    note(cv, W, y + 24,
         "※ 具体的なサイズ表は施設・製品で異なる。付録Cに目安を示すが、"
         "最終的には画像と実物で決める。")
    cv.save(P("f12_device.png"))


# ---------------------------------------------------------------- f13
def _airway(cv, cx, top, tlen=132, tw=44):
    """気管・分岐部・左右主気管支の模式図。返り値は (分岐部y, 左端点, 右端点)。"""
    ax = cv.ax
    cv.rect(cx - tw / 2, top, tw, tlen, fc="#eef2f6", ec="#98a6b4", lw=1.6)
    car = top + tlen
    lend = (cx - 66, car + 104)
    rend = (cx + 60, car + 84)
    lb = Polygon([(cx - tw / 2, car - 6), (cx + 1, car - 6),
                  (lend[0] + 16, lend[1] + 6), (lend[0] - 12, lend[1] - 6)],
                 closed=True, facecolor="#eef2f6", edgecolor="#98a6b4",
                 lw=1.6, zorder=2)
    rb = Polygon([(cx - 1, car - 6), (cx + tw / 2, car - 6),
                  (rend[0] + 14, rend[1] + 8), (rend[0] - 10, rend[1] + 24)],
                 closed=True, facecolor="#eef2f6", edgecolor="#98a6b4",
                 lw=1.6, zorder=2)
    ax.add_patch(lb)
    ax.add_patch(rb)
    ax.plot([cx + 34, cx + 74], [car + 24, car + 6], color="#98a6b4",
            lw=3.0, zorder=3)
    return car, lend, rend


def f13():
    W, H = 1520, 1290
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44,
             "左用ダブルルーメンチューブ —— 正しい位置と、よくある3つのずれ",
             size=12.5, ha="center")
    PANELS = [
        ("正しい位置", GREEN, "left", 0.46,
         ["気管カフは声門より下、分岐部より上",
          "気管支カフは左主気管支の中にすべて収まる",
          "気管腔から分岐部と右主気管支が見える"]),
        ("浅すぎる", AMBER, "left", 0.02,
         ["気管支カフが分岐部にまたがる",
          "膨らませると分岐部を押し広げ、右の換気を妨げる",
          "分離が不完全で、肺が虚脱しない"]),
        ("深すぎる", RED, "left", 0.92,
         ["左上葉枝または下葉枝を塞ぐ",
          "換気側の気道内圧が上がり、換気量が減る",
          "左肺の一部しか換気されない"]),
        ("右へ入った", PURPLE, "right", 0.46,
         ["右主気管支に迷入し、右上葉枝を塞ぐ",
          "左肺が換気されず、酸素化が急に悪化する",
          "聴診だけでは「左が虚脱した」と誤認しやすい"]),
    ]
    L, R = 56, W - 56
    GAP = 18
    CW = (R - L - GAP * 3) / 4
    PTOP, PH = 148, 356
    for i, (head, col, side, frac, lines) in enumerate(PANELS):
        x = L + i * (CW + GAP)
        cv.box(x, 92, CW, 48, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, 116, head, size=11.4, color="white", weight="bold")
        cv.box(x, PTOP, CW, PH, fc="#fbfcfd", ec=col, lw=1.6, radius=8)
        cx = x + CW / 2
        car, lend, rend = _airway(cv, cx, PTOP + 34)
        ax.plot([cx, cx], [PTOP + 34, car - 8], color=NAVY, lw=4.2, zorder=5)
        ax.add_patch(Circle((cx, car - 62), 13, facecolor="white",
                            edgecolor=NAVY, lw=1.8, zorder=6))
        end = lend if side == "left" else rend
        bx = cx + (end[0] - cx) * frac
        by = car + (end[1] - car) * frac
        ax.plot([cx, bx], [car - 8, by], color=NAVY, lw=3.4, zorder=5)
        ax.add_patch(Circle((bx, by), 12, facecolor="#2e6da4",
                            edgecolor="#174682", lw=1.6, zorder=6))
        cv.text(lend[0] - 6, lend[1] + 30, "左肺", size=9.6, color=GREY, z=7)
        cv.text(rend[0] + 6, rend[1] + 34, "右肺", size=9.6, color=GREY, z=7)
        if i == 3:
            cv.text(lend[0] - 6, lend[1] + 60, "換気されない", size=9.0,
                    color=RED, weight="bold", z=7)
    y = rows(cv, W, PTOP + PH + 26,
             [(p[0], p[1], p[4]) for p in PANELS],
             name_sz=10.4, body_sz=10.0, lh=1.5)
    note(cv, W, y + 24,
         "※ 図は位置関係を示す模式であり、実際の気管支の角度・長さとは異なる。"
         "白いカフが気管カフ、青いカフが気管支カフ。"
         "挿入直後と体位変換後の二度、気管支鏡で確認する。")
    cv.save(P("f13_dlt_position.png"))


# ---------------------------------------------------------------- f14
def f14():
    W, H = 1520, 1110
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "気管支鏡で確認する三つの像 —— 何が見えれば正しいのか",
             size=12.5, ha="center")
    VIEWS = [
        ("① 気管分岐部", BLUE,
         "手前に縦走する軟骨、背側に膜様部。\n左右の主気管支が見える",
         ["膜様部（平らな側）が背側",
          "左は細く、より水平に走る",
          "右は太く、より垂直に近い"]),
        ("② 気管腔から見下ろす", GREEN,
         "青い気管支カフの上縁が\n左主気管支の入口のすぐ下に見える",
         ["カフが分岐部にはみ出していない",
          "右主気管支は開いたまま見える",
          "はみ出していれば浅すぎる"]),
        ("③ 気管支腔から見る", AMBER,
         "左主気管支の内腔と、\nその先の上葉枝・下葉枝の分岐",
         ["分岐が見えれば深すぎない",
          "内腔が閉じていれば深すぎる",
          "右で三分岐が見えたら迷入"]),
    ]
    L, R = 70, W - 70
    GAP = 34
    CW = (R - L - GAP * 2) / 3
    for i, (head, col, cap, lines) in enumerate(VIEWS):
        x = L + i * (CW + GAP)
        cv.box(x, 92, CW, 46, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, 115, head, size=11.4, color="white", weight="bold")
        cv.box(x, 146, CW, 330, fc="#fbfcfd", ec=col, lw=1.6, radius=8)
        ccx, ccy, rr = x + CW / 2, 262, 88
        ax.add_patch(Circle((ccx, ccy), rr, facecolor="#f6e7e2",
                            edgecolor="#b08a80", lw=2.0, zorder=3))
        if i == 0:
            ax.add_patch(Wedge((ccx, ccy), rr - 8, 200, 340,
                               facecolor="#e6cfc6", edgecolor="none", zorder=4))
            ax.add_patch(Circle((ccx - 34, ccy + 18), 24, facecolor="#3a3f47",
                                edgecolor="#20242a", lw=1.4, zorder=5))
            ax.add_patch(Circle((ccx + 32, ccy + 12), 30, facecolor="#3a3f47",
                                edgecolor="#20242a", lw=1.4, zorder=5))
            cv.text(ccx - 34, ccy + 18, "左", size=9.4, color="white", z=6)
            cv.text(ccx + 32, ccy + 12, "右", size=9.4, color="white", z=6)
            cv.text(ccx, ccy - 62, "膜様部", size=9.0, color="#6b5a54", z=6)
        elif i == 1:
            ax.add_patch(Circle((ccx + 30, ccy + 6), 32, facecolor="#3a3f47",
                                edgecolor="#20242a", lw=1.4, zorder=5))
            cv.text(ccx + 30, ccy + 6, "右", size=9.4, color="white", z=6)
            ax.add_patch(Wedge((ccx - 36, ccy + 10), 30, 180, 360,
                               facecolor="#2e6da4", edgecolor="#174682",
                               lw=1.6, zorder=5))
            cv.text(ccx - 36, ccy + 34, "カフ", size=9.0, color="white",
                    weight="bold", z=6)
        else:
            ax.add_patch(Circle((ccx - 26, ccy + 4), 30, facecolor="#3a3f47",
                                edgecolor="#20242a", lw=1.4, zorder=5))
            ax.add_patch(Circle((ccx + 34, ccy + 22), 24, facecolor="#3a3f47",
                                edgecolor="#20242a", lw=1.4, zorder=5))
            cv.text(ccx - 26, ccy + 4, "上葉", size=8.8, color="white", z=6)
            cv.text(ccx + 34, ccy + 22, "下葉", size=8.8, color="white", z=6)
        caplines = cap.split(chr(92) + "n")
        csz = min(cv.fit_size(caplines, CW - 44, 9.6), 9.6)
        for j, ln in enumerate(caplines):
            cv.text(x + CW / 2, 396 + 24 * j, ln, size=csz, color=INK)
    y = 512
    y = rows(cv, W, y, [(v[0], v[1], v[3]) for v in VIEWS],
             name_sz=10.4, body_sz=10.0, lh=1.5)
    note(cv, W, y + 24,
         "※ 図は解剖学的な左右で描いた模式であり、"
         "内視鏡画面上の左右は挿入の向きで変わる。実際の気管支鏡像とも異なる。"
         "右主気管支で「三つに分かれる枝」が見えたら右上葉枝であり、そこは左ではない。")
    cv.save(P("f14_bronchoscopy.png"))


# ---------------------------------------------------------------- f15
def f15():
    W, H = 1520, 800
    cv = Canvas(W, H)
    cv.title(W / 2, 44,
             "片肺換気の生理 —— シャントをどこまで自分で減らしてくれるか",
             size=12.5, ha="center")
    y = three_col(cv, W, 92, [
        ("虚脱側で起きること", RED,
         ["換気はゼロだが、血流はすぐにはゼロにならない",
          "その血液は酸素化されずに左心系へ戻る＝シャント",
          "低酸素性肺血管攣縮が血流を減らしていく",
          "効果が出るまで時間がかかり、数十分かけて進む"]),
        ("換気側で起きること", BLUE,
         ["両肺分の血流を受ける",
          "同じ一回換気量を入れれば過伸展する",
          "側臥位では下側になり、重力で血流が多い（有利）",
          "腹部臓器と縦隔に押されて容量が減る（不利）"]),
        ("攣縮を弱めるもの", AMBER,
         ["高濃度の揮発性麻酔薬（濃度依存性）",
          "血管拡張薬、一酸化窒素、一部の強心薬",
          "低い混合静脈血酸素分圧、低体温、感染",
          "肺高血圧や既存の肺疾患でも反応が鈍る"]),
    ], body_sz=9.8)
    y = banner(cv, W, y + 24,
               "片肺換気開始直後がいちばん苦しい。"
               "攣縮が効いてくるまでの時間を、設定と体位で乗り切る",
               col=BLUE, fc="#eaf1f8", tc="#174682")
    note(cv, W, y + 30,
         "※ 側臥位では、換気側が下（重力側）に来るため血流配分は有利に働く。"
         "仰臥位のまま片肺換気にすると、この利点が得られない。"
         "低酸素性肺血管攣縮の強さには個人差が大きい。")
    cv.save(P("f15_olv_physiology.png"))


# ---------------------------------------------------------------- f16
def f16():
    W, H = 1520, 1000
    cv = Canvas(W, H)
    cv.title(W / 2, 44,
             "片肺換気中に酸素化が落ちたら —— 順番を決めておく",
             size=12.5, ha="center")
    STEPS = [
        ("0", "まず知らせる", GREY,
         ["外科医に伝える。手術操作が原因のこともある",
          "モニタの信頼性を確認する（波形、体位、血圧計との干渉）"]),
        ("1", "酸素濃度を上げる", BLUE,
         ["時間を買う手段であり、原因の解決ではない",
          "上げても改善しないなら、それは純粋なシャントである"]),
        ("2", "位置を確認する", RED,
         ["気管支鏡で見る。ずれは最も多く、最も直しやすい原因",
          "分泌物・血液があれば吸引する"]),
        ("3", "換気側を立て直す", GREEN,
         ["肺を開き（リクルートメント）、呼気終末陽圧をかけ直す",
          "駆動圧を見ながら。かけすぎれば血流が虚脱側へ逃げる"]),
        ("4", "虚脱側に酸素を渡す", AMBER,
         ["持続気道陽圧または少量の酸素送気",
          "術野が膨らむため、外科医と相談してから"]),
        ("5", "戻す・止める", PURPLE,
         ["間欠的に両肺換気へ戻す",
          "肺動脈のクランプを外科医に依頼できる術式もある",
          "改善しないなら、術野より換気を優先する"]),
    ]
    L, R = 60, W - 60
    TOP, GAP = 96, 12
    NUMW = 66
    NAMEW = max(cv.width(s[1], 11.6, "bold") for s in STEPS) + 50
    BX = L + NUMW + NAMEW
    y0 = TOP
    for i, (num, name, col, lines) in enumerate(STEPS):
        lh = LH(10.2, 1.45)
        RH = max(96, 30 + lh * len(lines))
        cv.box(L, y0, R - L, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(L, y0, NUMW, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(L + NUMW / 2, y0 + RH / 2, num, size=17, color="white",
                weight="bold")
        cv.text(L + NUMW + 26, y0 + RH / 2, name, size=11.6, color=col,
                weight="bold", ha="left")
        for j, ln in enumerate(lines):
            cv.text(BX, y0 + RH / 2 + lh * (j - (len(lines) - 1) / 2), ln,
                    size=10.2, color=INK, ha="left")
        if i < len(STEPS) - 1:
            cv.arrow((L + NUMW / 2, y0 + RH), (L + NUMW / 2, y0 + RH + GAP),
                     color="#c9d2dc", lw=2.0, head=8)
        y0 += RH + GAP
    y = y0
    note(cv, W, y + 14,
         "※ 順番を決めておく理由は、低酸素の場面で考える時間がないから。"
         "「上げる → 見る → 開く → 渡す → 戻す」と覚える。"
         "1と2の順序は入れ替わってよいが、2を飛ばしてはいけない。")
    cv.save(P("f16_hypoxemia_olv.png"))


# ---------------------------------------------------------------- f17
def f17():
    W, H = 1520, 890
    cv = Canvas(W, H)
    cv.title(W / 2, 44,
             "気道内圧が上がった —— 抵抗の問題か、肺の硬さの問題か",
             size=12.5, ha="center")
    y = two_col(cv, W, 92, [
        ("最高気道内圧だけ上がる（抵抗の問題）", AMBER, "#fdf3e3",
         ["チューブの屈曲・閉塞・分泌物・血液",
          "気管支攣縮",
          "気管支カフの位置異常（分岐部にまたがる、深すぎる）",
          "回路のねじれ、フィルターの詰まり",
          "対処：吸引、気管支鏡、気管支拡張薬、位置の修正"]),
        ("プラトー圧も上がる（肺・胸郭の問題）", RED, "#fceeec",
         ["気胸（緊張性なら循環も落ちる）",
          "無気肺、肺水腫、誤嚥",
          "気腹・頭低位・腹腔内圧の上昇、術者の圧迫",
          "内因性呼気終末陽圧（吐ききれていない）",
          "筋弛緩が切れて胸郭が硬い",
          "対処：原因に応じて。胸腔ドレナージが要る場面を見落とさない"]),
    ], body_sz=10.0)
    y = rows(cv, W, y + 24, [
        ("最初にやること", BLUE,
         ["吸気ポーズをかけてプラトー圧を測り、最高気道内圧との差を見る。",
          "これだけで鑑別が左右どちらの表に入るか決まる。"]),
        ("片肺換気中に特有のこと", PURPLE,
         ["片肺になれば気道内圧が上がるのは当然。開始時の値を基準にする。",
          "「開始時より上がった」ときに、上の表を開く。"]),
        ("急変として扱う条件", RED,
         ["血圧が同時に落ちている、酸素化が急に落ちた、片側の呼吸音が消えた。",
          "このときは緊張性気胸を先に否定する。"]),
    ], name_sz=10.4, body_sz=10.2, lh=1.55)
    note(cv, W, y + 24,
         "※ 分離肺換気では「チューブが原因」の頻度が高い。"
         "しかし気胸を後回しにしてはいけない。"
         "循環が一緒に落ちているかが、最初の分かれ道になる。")
    cv.save(P("f17_high_pressure.png"))


# ---------------------------------------------------------------- f18
def f18():
    W, H = 1520, 820
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "術後肺合併症 —— 何が起きるのか、どこで減らせるのか",
             size=12.5, ha="center")
    y = three_col(cv, W, 92, [
        ("何が含まれるか", GREY,
         ["無気肺",
          "肺炎・気道感染",
          "呼吸不全と再挿管",
          "胸水・気胸・遷延する空気漏れ",
          "急性呼吸窮迫症候群",
          "肺切除後では、これらが在院日数と死亡に直結する"]),
        ("患者側のリスク", AMBER,
         ["高齢、低栄養、貧血",
          "慢性閉塞性肺疾患、喫煙",
          "術前の呼吸機能低下、拡散能の低下",
          "全身状態（ASA分類）",
          "変えられないものが多い"]),
        ("こちらで動かせるもの", GREEN,
         ["術前の禁煙と呼吸リハビリテーション",
          "術中の肺保護換気（量・駆動圧・呼気終末陽圧）",
          "筋弛緩の完全な回復と、確実な抜管",
          "術後の疼痛管理（深呼吸と咳ができること）",
          "早期離床と口腔ケア"]),
    ], body_sz=9.8)
    y = banner(cv, W, y + 24,
               "術中の設定だけでは決まらない。"
               "禁煙・鎮痛・離床まで含めて、はじめて「束」になる",
               col=GREEN, fc="#eaf5ee", tc="#1f6b47")
    note(cv, W, y + 30,
         "※ 硬膜外麻酔や傍脊椎ブロックによる鎮痛は、"
         "深呼吸と咳を可能にすることで肺合併症の予防に寄与する。"
         "区域麻酔の選択は、呼吸管理の一部である（本シリーズ⑰）。")
    cv.save(P("f18_ppc.png"))


# ---------------------------------------------------------------- f19
def f19():
    W, H = 1520, 800
    cv = Canvas(W, H)
    cv.title(W / 2, 44,
             "再膨張性肺水腫 —— 「開いた側」に起きる、遅れてくる合併症",
             size=12.5, ha="center")
    y = three_col(cv, W, 92, [
        ("成立しやすい条件", RED,
         ["虚脱していた時間が長い",
          "一気に、強い陰圧または陽圧で再膨張させた",
          "もともと虚脱していた側の肺",
          "低侵襲心臓手術・胸腔鏡手術・大量胸水の排液後"]),
        ("何が起きているか", AMBER,
         ["虚脱していた血管の透過性が上がる",
          "再灌流に伴う障害と炎症",
          "界面活性物質の減少",
          "多くは同側性だが、両側に及ぶこともある"]),
        ("避けるための考え方", GREEN,
         ["再膨張は段階的に行う",
          "急激な陰圧での排液を避ける",
          "戻したあとも数時間は酸素化を追う",
          "術直後に酸素化が落ちたら鑑別に入れる"]),
    ], body_sz=9.8)
    y = rows(cv, W, y + 24, [
        ("いつ気づくか", BLUE,
         ["再膨張の直後ではなく、数十分から数時間かけて悪化することがある。",
          "手術室を出た後に顕在化する例がある。"]),
        ("何と間違えるか", PURPLE,
         ["心原性肺水腫、輸血関連肺障害、誤嚥、肺炎。",
          "「開いた側に強く出ている」ことが手がかりになる。"]),
    ], name_sz=10.4, body_sz=10.2, lh=1.55)
    note(cv, W, y + 24,
         "※ 頻度は報告により大きく異なり、定義（画像だけか、"
         "酸素化の悪化を伴うか）に左右される。付録Dを参照。")
    cv.save(P("f19_reexpansion.png"))


# ---------------------------------------------------------------- f20
def f20():
    W, H = 1520, 980
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "抜管したあとの呼吸 —— 手段の位置づけを決めておく",
             size=12.5, ha="center")
    y = rows(cv, W, 96, [
        ("通常の酸素投与", GREY,
         ["鼻カニュラ、簡易マスク、リザーバー付きマスク。",
          "吸入酸素濃度は正確には決まらず、患者の吸気流量に左右される。"]),
        ("高流量鼻カニュラ", BLUE,
         ["加温加湿した高流量で、吸入酸素濃度が安定し、死腔を洗い流す。",
          "わずかな気道内陽圧も生じる。会話と経口摂取ができる。",
          "急性の低酸素性呼吸不全で、通常の酸素投与より有利という報告がある。"]),
        ("非侵襲的陽圧換気", GREEN,
         ["換気も助けられる。高二酸化炭素血症を伴う呼吸不全に向く。",
          "抜管後の再挿管予防としても使われる。",
          "意識・気道保護・分泌物・顔面の適合が使用の前提になる。"]),
        ("再挿管をためらわない", RED,
         ["改善しないまま非侵襲的手段を続けると、遅れた挿管は予後を悪くする。",
          "「いつまでに改善しなければ挿管するか」を先に決めておく。"]),
    ], name_sz=10.6, body_sz=10.2, lh=1.55)
    y = banner(cv, W, y + 26,
               "手段を増やすことではなく、"
               "「次に進む条件」を決めておくことが安全につながる",
               col=PURPLE, fc="#f1ecf8", tc="#4E387A")
    note(cv, W, y + 30,
         "※ 肺切除後は、空気漏れや断端への圧負荷の観点から"
         "陽圧を用いる手段の適応を外科医と相談する。"
         "出典と限界は付録D。")
    cv.save(P("f20_postop_oxygen.png"))


if __name__ == "__main__":
    for fn in (f11, f12, f13, f14, f15, f16, f17, f18, f19, f20):
        fn()
        print("ok", fn.__name__)
