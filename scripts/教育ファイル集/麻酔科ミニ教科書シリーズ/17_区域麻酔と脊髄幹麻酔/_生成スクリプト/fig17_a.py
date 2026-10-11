# -*- coding: utf-8 -*-
"""第17巻 区域麻酔と脊髄幹麻酔 図版 f01〜f09"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, Ellipse
from figlib import Canvas, LH, NAVY, INK, JP
from figkit import two_col, three_col, rows, note, banner

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
plt.rcParams["font.family"] = JP


def P(n):
    return os.path.join(OUT, n)


# ---------------------------------------------------------------- f01
def f01():
    W, H = 1520, 700
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "区域麻酔は手技ではなく、リスクを調整する処方である",
             size=12.5, ha="center")
    y = three_col(cv, W, 92, [
        ("患者｜何を守るか", "#2e6da4",
         ["呼吸予備能（睡眠時無呼吸、慢性閉塞性肺疾患、横隔神経麻痺の許容度）",
          "循環・肝腎機能（遊離分画、代謝、排泄）",
          "神経学的なベースライン（既存のしびれ、筋力）",
          "抗血栓薬（深部・非圧迫性の部位ほど保守的に）",
          "体格と年齢（低体重・高齢は薬物予算を下げる）",
          "協力度と体位保持（深い鎮静が要るなら再考する）"]),
        ("手術｜何を減らすか", "#b8760f",
         ["痛みの時間軸と成分（皮膚・筋膜・骨・関節包・内臓）",
          "必要な麻酔範囲（知覚・運動・交感神経のどこまで）",
          "出血と体位（ブロック後に神経所見を評価できるか）",
          "止血帯の有無と時間（切開部位以外の痛み）",
          "術後にどの機能を残したいか"]),
        ("環境｜何ができるか", "#1f6b47",
         ["超音波装置と、その画質",
          "介助者と、体位を保持できる人手",
          "脂肪乳剤・蘇生薬・緊急導線",
          "術後に神経所見を追える体制",
          "できないなら、その手技は選ばない"]),
    ], body_sz=9.8)
    y = banner(cv, W, y + 26,
               "「このブロックができるか」ではなく「この患者に、この手術で、"
               "この環境で、何を選ぶか」",
               col="#2e6da4", fc="#eaf1f8", tc="#174682")
    note(cv, W, y + 30,
         "※ ブロック名を覚えることから始めると、選択の理由が抜け落ちる。"
         "神経支配・薬物予算・出血と呼吸のリスク・術後の機能を、一枚の判断へつなぐ。")
    cv.save(P("f01_prescription.png"))


# ---------------------------------------------------------------- f02
def f02():
    W, H = 1520, 660
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "組み立ての順序 —— 定義 → 計算 → 可視化 → 手技 → 再評価",
             size=12.5, ha="center")
    STEPS = [
        ("01 患者評価", "#2e6da4", "誰に、何を避けるか",
         ["術式と侵襲", "呼吸・循環の予備能", "抗血栓薬・感染", "既存の神経症状"]),
        ("02 薬物予算", "#7b52a8", "総量を足し算する",
         ["濃度 × mL ＝ mg", "mg/kg", "部位の吸収速度", "年齢・肝・心機能"]),
        ("03 画像読解", "#b8760f", "見えないなら進めない",
         ["標的神経", "血管・胸膜・骨", "針先の連続追跡", "薬液の拡がり"]),
        ("04 手技選択", "#1f6b47", "術後の機能まで選ぶ",
         ["神経軸／末梢", "浅部／深部", "単回／カテーテル", "鎮痛／運動温存"]),
        ("05 安全と再評価", "#c0392b", "異常を見つける係を決める",
         ["中毒の初期徴候", "血腫・感染・神経障害", "脂肪乳剤・緊急導線",
          "術後の歩行・呼吸"]),
    ]
    L, R = 40, W - 40
    GAP = 12
    CW = (R - L - GAP * 4) / 5
    HTOP, HH = 90, 48
    STOP = HTOP + HH
    SUBH = 34
    BTOP = STOP + SUBH + 8
    sz = min(cv.fit_size([l for s in STEPS for l in s[3]], CW - 40, 9.8), 9.8)
    BH = 26 + LH(sz, 1.85) * 3 + LH(sz, 1.0) * 0.5 + 20
    ssz = min(cv.fit_size([s[2] for s in STEPS], CW - 24, 9.4), 9.4)
    for i, (head, col, sub, lines) in enumerate(STEPS):
        x = L + i * (CW + GAP)
        cv.box(x, HTOP, CW, HH, fc=col, ec=col, lw=0, radius=7)
        cv.text(x + CW / 2, HTOP + HH / 2, head, size=10.8, color="white",
                weight="bold")
        cv.text(x + CW / 2, STOP + SUBH / 2, "「" + sub + "」", size=ssz,
                color=col, weight="bold")
        cv.box(x, BTOP, CW, BH, fc="white", ec=col, lw=1.7, radius=7)
        for j, ln in enumerate(lines):
            cv.text(x + CW / 2, BTOP + 26 + LH(sz, 1.85) * j, ln, size=sz,
                    color=INK)
        if i < 4:
            cv.arrow((x + CW + 1, HTOP + HH / 2), (x + CW + GAP - 1,
                     HTOP + HH / 2), color="#8d97a3", lw=2.0, head=8)
    note(cv, W, BTOP + BH + 32,
         "※ この順序が崩れると、"
         "「ブロックはできたが、総量を数えていなかった」"
         "「刺せたが、術後に誰も神経所見を見ていない」という形で破綻する。")
    cv.save(P("f02_learning_map.png"))


# ---------------------------------------------------------------- f03
def f03():
    W, H = 1520, 720
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "薬物予算 —— 濃度 × mL ＝ mg を、必ず一度は計算する",
             size=12.5, ha="center")
    L, R = 60, W - 60
    # 計算式の帯
    BY, BH_ = 92, 96
    cv.box(L, BY, R - L, BH_, fc="#eef1f5", ec="#5d6875", lw=1.8, radius=8)
    parts = [("濃度（%）", "#2e6da4"), ("×", "#5d6875"), ("10", "#5d6875"),
             ("×", "#5d6875"), ("容量（mL）", "#7b52a8"), ("＝", "#5d6875"),
             ("総量（mg）", "#c0392b")]
    total = sum(cv.measure(p[0], 14 if len(p[0]) > 2 else 13,
                           weight="bold")[0] + 22 for p in parts)
    x = L + (R - L - total) / 2
    for t, col in parts:
        w = cv.measure(t, 14 if len(t) > 2 else 13, weight="bold")[0] + 22
        cv.text(x + w / 2, BY + BH_ / 2 - 8, t,
                size=14 if len(t) > 2 else 13, color=col, weight="bold")
        x += w
    cv.text(W / 2, BY + BH_ - 22, "例：1% リドカイン 20 mL ＝ 1 × 10 × 20 ＝ 200 mg",
            size=10.2, color="#5d6875")
    y = three_col(cv, W, BY + BH_ + 26, [
        ("足し算する対象", "#7b52a8",
         ["ブロックに使った量", "術野の局所浸潤麻酔", "創部への追加",
          "別のブロックを併用した分", "硬膜外に入れた分"]),
        ("予算を下げる要因", "#b8760f",
         ["高齢、低体重、小児", "肝機能・心機能の低下", "低蛋白血症",
          "アシドーシス・低酸素", "妊娠"]),
        ("吸収を速める要因", "#c0392b",
         ["血流の豊富な部位", "吸収面積の広い部位", "炎症のある組織",
          "アドレナリン非添加", "肋間・硬膜外などの部位"]),
    ], body_sz=9.8)
    y = banner(cv, W, y + 24,
               "「そのブロック単独では極量以内」でも、合算すると超えていることがある")
    cv.save(P("f03_drug_budget.png"))


# ---------------------------------------------------------------- f04
def f04():
    W, H = 1520, 760
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "抗血栓薬と、部位の「引き返しやすさ」",
             size=12.5, ha="center")
    DATA = [
        ("圧迫できる浅部", "#1f6b47",
         ["出血しても外から押さえられる。神経障害に至りにくい",
          "例：浅頸神経叢、大腿神経、伏在神経、表在の筋膜面ブロック"]),
        ("圧迫できない深部", "#b8760f",
         ["出血しても押さえられない。血腫が周囲を圧迫する",
          "例：腰神経叢、傍脊椎、深部の体幹ブロック"]),
        ("神経軸（脊髄幹）", "#c0392b",
         ["硬膜外血腫は脊髄を圧迫し、対麻痺に至りうる",
          "抗血栓薬の休薬・再開の時間軸を、最も厳格に扱う部位"]),
    ]
    y = rows(cv, W, 96, DATA, lh=1.75)
    y = banner(cv, W, y + 26,
               "「刺せるか」ではなく「出血したときに、引き返せるか」で部位を格付けする")
    note(cv, W, y + 30,
         "※ 具体的な休薬期間と再開時期は、薬剤ごとに定められている。"
         "施設の基準と、日本ペインクリニック学会等のガイドラインに従うこと。"
         "本書では、部位ごとの考え方だけを扱う。")
    cv.save(P("f04_anticoagulant.png"))


# ---------------------------------------------------------------- f05
def f05():
    W, H = 1520, 760
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "背面から脊髄まで —— 針が通っていく順序",
             size=12.5, ha="center")
    LAYERS = [
        ("皮膚・皮下組織", "#f3ddd0", "#c99a86", ""),
        ("棘上靱帯", "#e8dcc8", "#b8ac99", "棘突起の背側をつなぐ"),
        ("棘間靱帯", "#e0d3bd", "#b8ac99", "棘突起のあいだにある薄い靱帯"),
        ("黄色靱帯", "#f2d96b", "#c8a415",
         "腰部で最も厚く、L2-3 で 3〜5 mm。抵抗を感じるのはここ"),
        ("硬膜外腔", "#dceaf5", "#2e6da4", "硬膜外麻酔はここに入れる"),
        ("硬膜・くも膜", "#e6d4e8", "#7b52a8", "第2仙椎の高さで終わる"),
        ("くも膜下腔（髄液）", "#cfe8f5", "#1f7f8b",
         "脊髄くも膜下麻酔はここに入れる"),
    ]
    L, R = 60, W - 60
    TOP = 96
    NAMEW = 300
    LH_ = 62
    GAP = 8
    dsz = min(cv.fit_size([l[3] for l in LAYERS if l[3]],
                          R - L - NAMEW - 300, 9.8), 9.8)
    for i, (name, fc, ec, desc) in enumerate(LAYERS):
        y = TOP + i * (LH_ + GAP)
        ax.add_patch(Rectangle((L, y), NAMEW, LH_, facecolor=fc,
                               edgecolor=ec, lw=1.8, zorder=3))
        cv.text(L + NAMEW / 2, y + LH_ / 2, name, size=10.6, color="#3a3f47",
                weight="bold", z=5)
        if desc:
            cv.text(L + NAMEW + 34, y + LH_ / 2, desc, size=dsz,
                    color=INK, ha="left")
    # 針
    ny = TOP - 16
    ax.plot([L + NAMEW / 2, L + NAMEW / 2], [ny, TOP + 6 * (LH_ + GAP) + LH_],
            color="#4a5768", lw=4.0, zorder=6)
    ax.add_patch(Polygon([[L + NAMEW / 2 - 7, TOP + 6 * (LH_ + GAP) + LH_],
                          [L + NAMEW / 2 + 7, TOP + 6 * (LH_ + GAP) + LH_],
                          [L + NAMEW / 2, TOP + 6 * (LH_ + GAP) + LH_ + 18]],
                         closed=True, facecolor="#4a5768", edgecolor="none",
                         zorder=6))
    cv.text(L + NAMEW / 2, ny - 16, "針", size=10.0, color="#4a5768",
            weight="bold")
    note(cv, W, TOP + 7 * (LH_ + GAP) + 32,
         "※ 皮膚から硬膜外腔までは、おおむね 4 cm 前後（体格で大きく変わる）。"
         "靱帯の厚みはおよそ 5 mm。模式図であり、縮尺は実際の厚みを表していない。")
    cv.save(P("f05_layers.png"))


# ---------------------------------------------------------------- f06
def f06():
    W, H = 1520, 720
    cv = Canvas(W, H)
    ax = cv.ax
    cv.title(W / 2, 44, "脊髄円錐はどこで終わるか —— 穿刺高位を決める理由",
             size=12.5, ha="center")
    # 左：脊柱の模式
    LX, LY, LW_, LH_ = 60, 90, 480, 520
    cv.box(LX, LY, LW_, LH_, fc="white", ec="#9aa4b0", lw=1.6, radius=8)
    cv.text(LX + LW_ / 2, LY + 30, "脊柱と脊髄（模式）", size=11.2, color=NAVY,
            weight="bold")
    cx = LX + 180
    top, bot = LY + 60, LY + LH_ - 40
    LEVELS = [("T12", 0.42), ("L1", 0.52), ("L2", 0.62), ("L3", 0.72),
              ("L4", 0.82), ("L5", 0.90), ("S", 0.97)]
    ax.add_patch(Rectangle((cx - 34, top), 68, bot - top,
                           facecolor="#f3ede2", edgecolor="#b8ac99", lw=1.6,
                           zorder=3))
    for name, f in LEVELS:
        y = top + (bot - top) * f
        ax.plot([cx - 34, cx + 34], [y, y], color="#b8ac99", lw=1.2, zorder=4)
        cv.text(cx - 46, y - 12, name, size=9.4, color="#8a7a63", ha="right",
                z=5)
    # 脊髄と馬尾
    cy1 = top + (bot - top) * 0.55
    ax.add_patch(Rectangle((cx - 14, top + 6), 28, cy1 - top - 6,
                           facecolor="#dceaf5", edgecolor="#2e6da4", lw=1.6,
                           zorder=5))
    ax.add_patch(Polygon([[cx - 14, cy1], [cx + 14, cy1], [cx, cy1 + 34]],
                         closed=True, facecolor="#dceaf5",
                         edgecolor="#2e6da4", lw=1.6, zorder=5))
    for k in range(7):
        ax.plot([cx - 10 + k * 3.4, cx - 16 + k * 5.4],
                [cy1 + 30, bot - 20], color="#8fb4d8", lw=1.4, zorder=5)
    cv.arrow((cx + 150, cy1 - 30), (cx + 22, cy1 + 4), color="#c0392b",
             lw=2.0, head=9, z=6)
    cv.text(cx + 156, cy1 - 38, "脊髄円錐", size=9.8, color="#c0392b",
            weight="bold", ha="left", z=6)
    cv.text(cx + 60, bot - 40, "馬尾", size=9.8, color="#2e6da4",
            weight="bold", ha="left", z=6)
    # 穿刺の推奨帯
    ys = top + (bot - top) * 0.74
    ye = top + (bot - top) * 0.92
    ax.add_patch(Rectangle((cx - 46, ys), 92, ye - ys, facecolor="#1f6b47",
                           alpha=0.16, edgecolor="#1f6b47", lw=1.6, zorder=6))
    cv.text(cx + 62, (ys + ye) / 2, "ここで刺す", size=9.8,
            color="#1f6b47", weight="bold", ha="left", z=7)
    # 右
    RX = LX + LW_ + 30
    DATA = [
        ("成人", "#2e6da4", ["脊髄の全長は 40〜50 cm。上端は環椎の上縁",
                           "下端は第1〜2腰椎付近で脊髄円錐となり、以降は馬尾"]),
        ("新生児・小児", "#b8760f", ["下端は第3腰椎付近まである",
                                "成長とともに頭側へ移動する"]),
        ("低位脊髄円錐", "#c0392b", ["軟部腫瘤、多毛、皮膚陥凹は潜在性二分脊椎のサイン",
                               "脊髄円錐が頭側へ移動していないことがある"]),
    ]
    RW_ = W - 60 - RX
    NAMEW2 = 190
    y = LY + 46
    bsz = min(cv.fit_size([l for d in DATA for l in d[2]],
                          RW_ - NAMEW2 - 50, 9.8), 9.8)
    RH = 30 + LH(bsz, 1.75) + LH(bsz, 1.0) * 0.5 + 22
    for i, (name, col, lines) in enumerate(DATA):
        yy = y + i * (RH + 16)
        cv.box(RX, yy, RW_, RH, fc="white", ec=col, lw=1.8, radius=8)
        cv.box(RX, yy, NAMEW2, RH, fc=col, ec=col, lw=0, radius=8)
        cv.text(RX + NAMEW2 / 2, yy + RH / 2, name, size=10.6, color="white",
                weight="bold")
        for j, ln in enumerate(lines):
            cv.text(RX + NAMEW2 + 26,
                    yy + RH / 2 - LH(bsz, 1.75) * 0.5 + LH(bsz, 1.75) * j,
                    ln, size=bsz, color=INK, ha="left")
    banner(cv, W, y + 3 * (RH + 16) + 10,
           "だから、成人では第2腰椎より尾側で刺す",
           col="#1f6b47", fc="#eaf4ee", tc="#0f5c3f", L=RX,
           size=11.5)
    note(cv, W, LY + LH_ + 34,
         "※ 模式図であり、椎体の比率や脊髄円錐の位置は個体差が大きい。"
         "皮膚のランドマークから椎間レベルを数えることの限界については第16章で扱う。")
    cv.save(P("f06_conus.png"))


# ---------------------------------------------------------------- f07
def f07():
    W, H = 1520, 600
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "脊髄の血管支配 —— 前と後で、支配も予備能も違う",
             size=12.5, ha="center")
    y = two_col(cv, W, 90, [
        ("前脊髄動脈", "#c0392b", "#fbeeee",
         ["脊髄の前 3分の2 を栄養する",
          "1本しかない",
          "アダムキーヴィッツ動脈（大前根動脈）が主要な供給源",
          "T12 または L1 の左側から分岐することが多い（およそ65%）",
          "T7〜L4 の範囲から分岐することもある（およそ35%）"]),
        ("後脊髄動脈", "#2e6da4", "#eaf1f8",
         ["脊髄の後ろ 3分の1 を栄養する",
          "左右2本ある",
          "前脊髄動脈との交通はない",
          "前が詰まっても後ろが代償することはない"]),
    ], head_sz=12)
    y = banner(cv, W, y + 24,
               "脊髄動脈は些細な外傷でも閉塞しうる。"
               "大動脈手術で血流が遮断されれば容易に虚血になる")
    note(cv, W, y + 30,
         "※ 脊髄幹麻酔の穿刺そのもので損傷する可能性、"
         "そしてアドレナリンなどの添加薬が虚血に関与する可能性も指摘されている。"
         "前後の交通がないという解剖が、この脆弱さの根拠になっている。")
    cv.save(P("f07_spinal_arteries.png"))


# ---------------------------------------------------------------- f08
def f08():
    W, H = 1520, 620
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "脊髄くも膜下麻酔と硬膜外麻酔 —— 入れる場所が違う",
             size=12.5, ha="center")
    y = two_col(cv, W, 90, [
        ("脊髄くも膜下麻酔", "#1f7f8b", "#e4f2f4",
         ["入れる場所　くも膜下腔（髄液のなか）",
          "効き方　直接、脊髄神経に届く。少量で確実に効く",
          "確認　髄液の逆流が得られる",
          "範囲　薬液の比重と体位で決まる。分節性ではない",
          "持続　単回投与が基本。時間で切れる"]),
        ("硬膜外麻酔", "#7b52a8", "#f3eefa",
         ["入れる場所　硬膜外腔",
          "効き方　硬膜を越えて拡散する。より多くの量が要る",
          "確認　抵抗消失。逆流するものはない",
          "範囲　分節性に得られる。入れた高さの上下へ広がる",
          "持続　カテーテルを置けば、何度でも追加できる"]),
    ], head_sz=12.5)
    y = banner(cv, W, y + 24,
               "「確実に効くが調節できない」のがくも膜下、"
               "「調節できるが確実さで劣る」のが硬膜外",
               col="#2e6da4", fc="#eaf1f8", tc="#174682")
    note(cv, W, y + 30,
         "※ 手技が比較的容易なため、麻酔科医以外が行うこともある。"
         "しかし生体への影響は大きく、重篤な合併症を引き起こしうる。"
         "「簡単な手技」と「安全な手技」は違う。")
    cv.save(P("f08_spinal_vs_epidural.png"))


# ---------------------------------------------------------------- f09
def f09():
    W, H = 1520, 700
    cv = Canvas(W, H)
    cv.title(W / 2, 44, "くも膜下麻酔の広がりを決めるもの",
             size=12.5, ha="center")
    y = three_col(cv, W, 92, [
        ("大きく効くもの", "#c0392b",
         ["薬液の比重（高比重か等比重か）",
          "投与直後の体位と、その保持時間",
          "投与した高さ（穿刺した椎間）",
          "投与量（mg）"]),
        ("影響するもの", "#b8760f",
         ["脊柱の彎曲（仰臥位ではT4〜6が最も低い）",
          "腹腔内圧（妊娠、腹水、肥満で髄液量が減る）",
          "身長（極端に低い・高い場合）",
          "注入速度とバルボタージュ"]),
        ("あまり関係しないもの", "#5d6875",
         ["体重（身長ほどには関係しない）",
          "性別",
          "穿刺針の太さ（広がりには影響しない）",
          "注入方向（諸説ある）"]),
    ], body_sz=9.9)
    y = banner(cv, W, y + 26,
               "投与したあと数分は、体位が薬の行き先を決めている。"
               "この間に体位を変えるかどうかは意図して選ぶ",
               col="#b8760f", fc="#fdf1e0", tc="#8a5a0f")
    note(cv, W, y + 30,
         "※ 高比重液は重力に従って動く。仰臥位では胸椎の彎曲の底（およそT4〜6）へ集まる。"
         "「思ったより効いた」「片側だけ効いた」の多くは、比重と体位で説明がつく。")
    cv.save(P("f09_spread.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09):
        fn()
        print("ok", fn.__name__)
