# -*- coding: utf-8 -*-
"""第Ⅲ章 脊髄保護　図版 h08〜h15"""
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


# ---------------------------------------------------------------- h08
def h08():
    """CSF drainage のエビデンス"""
    cv = Canvas(W, 1700)
    cap(cv, 44, "髄液ドレナージのエビデンスは、一枚岩ではない")

    ROWS = [("Coselli RCT（2002）", "無作為化比較試験", GREEN,
             "extent I/II の胸腹部大動脈瘤 145 例",
             "対麻痺・不全麻痺 13.0% → 2.6%。30 日死亡は 5.3% 対 2.9% で差なし",
             "有効を示した"),
            ("Cochrane レビュー（2012）", "系統的レビュー", ORANGE,
             "3 試験 287 例",
             "最初の 98 例の試験では 30% 対 33% で差なし。全体として結論は限定的",
             "エビデンスは限定的"),
            ("Khan メタ解析（2016）", "系統的レビュー・メタ解析", GREEN,
             "腰椎ドレーン使用の有無",
             "SCI リスクがほぼ半減（RR 0.42、95%CI 0.25-0.70）。"
             "早期 SCI で有意、遅発性では非有意",
             "有効を支持する"),
            ("Seike ら（2022・日本）", "傾向スコア一致", RED,
             "TEVAR：留置 89 例 対 非留置 115 例（各 59 例を一致）",
             "SCI は 9.0% 対 5.2% で差なし。予防的な全例留置を支持しない",
             "否定的"),
            ("Ohashi ら（2025・日本）", "コホート", ORANGE,
             "予防的留置 135 例 対 非留置 315 例",
             "予防群 SCI 1.5%、非留置群 4.8%。"
             "非留置群の 15 例中 12 例に治療的ドレナージを行ったが 10 例は麻痺が残存",
             "選択的留置＋救済の限界")]

    y = 130
    for name, kind, col, pop, res, verdict in ROWS:
        h = 190
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.7, radius=10)
        cv.box(70, y, 360, h, fc="#fbfcfd", ec=col, lw=0, radius=10)
        ns = cv.fit_size([name], 320, 11.4, weight="bold")
        cv.text(250, y + 48, name, size=ns, color=col, weight="bold")
        ks = cv.fit_size([kind], 320, 9.6)
        cv.text(250, y + 80, kind, size=ks, color=GREY)
        cv.box(96, y + 108, 308, 54, fc=col, ec=col, lw=0, radius=8)
        vs = cv.fit_size([verdict], 280, 11.0, weight="bold")
        cv.text(250, y + 135, verdict, size=vs, color="white", weight="bold")
        ps = cv.fit_size([pop], W - 500, 10.2)
        cv.text(450, y + 52, pop, size=ps, color=GREY, ha="left")
        rl = cv.wrap(res, W - 510, 10.6)
        for j, ln in enumerate(rl):
            cv.text(450, y + 94 + LH(10.6, 1.5) * j, ln, size=10.6,
                    color=INK, ha="left")
        y += h + 16

    textbox(cv, 70, y + 10, W - 140,
            ["ドレナージが有効だという研究と、差がないという研究の両方がある。",
             "違いを生んでいるのは、術式（開胸か血管内か）、"
             "被覆範囲、そして併用している他の保護手段である。",
             "「全例に入れる」も「入れない」も、この表からは導けない。"],
            10.8, style="navy", title="この表の読み方", title_color=NAVY,
            pad_y=16)
    cv.save(P("h08_csfd_evidence.png"))
    crop_bottom(P("h08_csfd_evidence.png"))


# ---------------------------------------------------------------- h09
def h09():
    """CSF ドレナージの合併症"""
    cv = Canvas(W, 1500)
    cap(cv, 44, "ドレーンは、無害なモニタではない")

    LEFT = [("ドレナージ関連死亡", "1.4%", RED),
            ("何らかの合併症", "25.6%", ORANGE),
            ("重症の合併症", "0.74%", RED),
            ("軽度の合併症", "17.8%", GREY)]
    x0, y0 = 70, 130
    lw = 560
    cv.box(x0, y0, lw, 440, fc="#ffffff", ec=RED, lw=1.8, radius=10)
    cv.text(x0 + lw / 2, y0 + 36, "報告されている頻度", size=12.2, color=RED,
            weight="bold")
    yy = y0 + 80
    for lab, val, col in LEFT:
        cv.box(x0 + 30, yy, lw - 60, 76, fc="#fbfcfd", ec="#dde3ea", lw=1.3,
               radius=8)
        ls = cv.fit_size([lab], 300, 10.8)
        cv.text(x0 + 56, yy + 38, lab, size=ls, color=INK, ha="left")
        cv.text(x0 + lw - 56, yy + 38, val, size=17, color=col, ha="right",
                weight="bold")
        yy += 86
    fn = "（F/B-EVAR 6 研究 1,079 例・開胸を含む単施設報告より）"
    cv.text(x0 + lw / 2, y0 + 424, fn,
            size=cv.fit_size([fn], lw - 50, 9.2), color=GREY)

    RX = x0 + lw + 30
    RW = W - 70 - RX
    ITEMS = [("何が起こるか", RED, "#fceeec",
              ["頭蓋内出血・硬膜下血腫（過剰排液）", "脊髄・硬膜外血腫（抗凝固下）",
               "髄膜炎・カテーテル感染", "血性髄液による手術延期",
               "カテーテル遺残・断裂"]),
             ("いつ起こるか", PURPLE, "#f1ecf8",
              ["挿入時（出血・穿刺困難）", "術中（抗凝固と併存）",
               "術後（排液量の管理を誤ったとき）", "抜去時・抜去後"])]
    y = y0
    for t, col, fc, lines in ITEMS:
        h = card(cv, RX, y, RW, t, lines, col, fc, body_size=10.2, lh=1.8)
        y += h + 26

    # 左右どちらの列が下まで伸びたかを測ってから、下の枠を置く。
    ty = max(y0 + 440, y - 26) + 34
    th = textbox(cv, 70, ty, W - 140,
                 ["日本の単施設報告では、術前に血性髄液のため手術を延期した例が 2.5%、"
                  "髄膜炎が 1.7%、",
                  "軽度の術前合併症が 32.4%、開胸手術での術後頭蓋内出血が 3.9% であった。",
                  "ドレーンを入れると決めた時点で、これらのリスクを引き受けている。"],
                 10.6, style="amber", title="日本からの報告",
                 title_color="#9a6510", pad_y=16)

    msg(cv, ty + th + 28,
        "入れるかどうかは、SCI のリスクとドレーンのリスクを並べて決める",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("h09_drain_complications.png"))
    crop_bottom(P("h09_drain_complications.png"))


# ---------------------------------------------------------------- h10
def h10():
    """MEP と術後延長モニタリング"""
    cv = Canvas(W, 900)
    cap(cv, 44, "術中に戻っても、術後に落ちることがある")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 420

    def block(x, title, color, big, sub, lines):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        ts = cv.fit_size([title], PW - 44, 12.0, weight="bold")
        cv.text(x + PW / 2, PY + 36, title, size=ts, color=color,
                weight="bold")
        cv.text(x + PW / 2, PY + 130, big, size=34, color=color,
                weight="bold")
        cv.text(x + PW / 2, PY + 180, sub, size=10.2, color=GREY)
        s, bl = fitlines(cv, lines, PW - 60, 10.2)
        for j, ln in enumerate(bl):
            cv.text(x + PW / 2, PY + 240 + LH(s, 1.7) * (j + 0.5), ln,
                    size=s, color=INK)

    block(x1, "術後も MEP を続けなかった群", RED, "90%",
          "遅発性脊髄虚血 21 例のうち 19 例",
          ["延長モニタリングを行っていなかった",
           "気づいたときには症状が出ている"])
    block(x2, "術後も MEP を続けた群", GREEN, "97%",
          "59 例のうち 57 例",
          ["遅発性脊髄虚血を起こさなかった",
           "独立した保護因子（OR 0.14、95%CI 0.03-0.65）"])

    textbox(cv, 70, PY + PH + 26, W - 140,
            ["150 例中 21 例（14%）に遅発性脊髄虚血が生じた研究である。",
             "術後まで運動誘発電位のモニタリングを延長した群では、"
             "発生が有意に少なかった（p=0.003）。",
             "麻酔科にとっての含意は、"
             "「手術室を出たあとも、下肢が動くかを繰り返し確かめる」ことである。"],
            10.6, style="green", title="観察を延ばすという保護手段",
            title_color=GREEN, pad_y=16)
    cv.save(P("h10_mep.png"))
    crop_bottom(P("h10_mep.png"))


# ---------------------------------------------------------------- h11
def h11():
    """MIS2ACE"""
    cv = Canvas(W, 900)
    cap(cv, 44, "あらかじめ、少しずつ閉じておく")

    STEP = [("① 術前に分節動脈を選ぶ", BLUE, "#eaf1f8",
             ["CT で分節動脈を評価する", "一度に閉じる本数を決める"]),
            ("② 血管内にコイルで塞栓する", PURPLE, "#f1ecf8",
             ["低侵襲・局所麻酔で行える", "数回のセッションに分ける"]),
            ("③ 側副血行網が育つのを待つ", GREEN, "#eaf5ee",
             ["数日から数週の間隔をあける", "圧は 24 時間で 40%、120 時間で 90%"]),
            ("④ 本来の修復術を行う", TEAL, "#e4f2f4",
             ["脊髄はすでに慣れている", "背側からの steal も減る"])]
    w = (W - 140 - 90) / 4
    for i, (t, col, fc, lines) in enumerate(STEP):
        x = 70 + (w + 30) * i
        card(cv, x, 140, w, t, lines, col, fc, body_size=10.0, lh=1.8)
        if i < 3:
            cv.arrow((x + w + 4, 230), (x + w + 26, 230), color="#b9c2cc",
                     lw=2.0, head=10)

    th = textbox(cv, 70, 420, W - 140,
                 ["MIS2ACE（minimally invasive staged segmental artery coil "
                  "embolization）は、",
                  "側副血行網をあらかじめ育てておくという発想の治療である。",
                  "現時点では症例数が限られ、"
                  "緊急例・不良な解剖・shaggy aorta は適応外とされている。",
                  "有効性は現在進行中の無作為化試験（PAPAartis）の結果を待つ段階にある。"],
                 10.6, style="navy", title="どういう戦略か", title_color=NAVY,
                 pad_y=16)

    msg(cv, 420 + th + 28,
        "MIS2ACE を行っても、髄液ドレナージや MEP などの他の手段は併用する")
    cv.save(P("h11_misace.png"))
    crop_bottom(P("h11_misace.png"))


# ---------------------------------------------------------------- h12
def h12():
    """Alg3-1 ドレーンを入れるか"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 1　髄液ドレーンを入れるかどうか")

    cx = W / 2
    bw = 780
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["開胸の胸腹部大動脈瘤修復か、血管内修復か",
              "Crawford 分類の extent はどれか（I〜III は高リスク）",
              "被覆・遮断される分節動脈はどれくらいか",
              "既往（腹部大動脈手術・鎖骨下動脈の状態）はどうか"],
             style="navy", title="① 脊髄虚血のリスクを見積もる",
             title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["抗凝固・抗血小板薬は止められているか",
              "血小板数と凝固能は穿刺できる範囲か",
              "穿刺部位に感染・脊椎疾患はないか",
              "頭蓋内病変（出血リスク）はないか"],
             style="red", title="② ドレーン側のリスクを見積もる",
             title_color=RED)
    y += h
    down(cv, cx, y, y + 50)
    y += 50
    cw = 520
    lx, rx = 70, W - 70 - cw
    side(cv, cx - 40, lx + cw + 10, y + 74)
    side(cv, cx + 40, rx - 10, y + 74)
    hl = step(cv, lx, y, cw,
              ["開胸 TAAA（extent I〜III）など高リスク",
               "ガイドラインが推奨する状況",
               "→ 予防的に留置する",
               "→ 目標 CSF 圧と排液量の上限を決めておく"],
              style="green", title="入れる", title_color=GREEN)
    hr = step(cv, rx, y, cw,
              ["TEVAR で被覆が短い、低リスク",
               "抗凝固が止められない、穿刺が危険",
               "→ 留置せず、発症したら治療的に入れる",
               "→ ただし救済できない例があることを知っておく"],
              style="amber", title="入れない（選択的留置）",
              title_color="#9a6510")
    y += max(hl, hr)
    down(cv, lx + cw / 2, y, y + 44)
    down(cv, rx + cw / 2, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["どちらを選んだかを、術者・ICU・病棟で共有する",
          "入れなかった症例こそ、術後の神経所見の観察間隔を決めておく",
          "入れた症例では、抜去のタイミングと抗凝固再開の順番を決めておく"],
         style="purple", title="③ 決めたことを共有する", title_color=PURPLE)
    cv.save(P("h12_alg_drain.png"))
    crop_bottom(P("h12_alg_drain.png"))


# ---------------------------------------------------------------- h13
def h13():
    """Alg3-2 術中の SCPP 管理"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 2　術中の脊髄灌流圧管理")

    cx = W / 2
    bw = 780
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["MAP の目標値と、CSF 圧の上限を数字で決める",
              "遮断中・遮断解除後・閉創時で目標が変わることを共有する",
              "誰が SCPP を計算し、記録するかを決める"],
             style="navy", title="① 執刀前に目標を決める", title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["遮断で近位血圧は上がるが、遠位と脊髄の灌流は下がる",
              "遠位灌流を併用していても、上位胸髄には届きにくい",
              "分節動脈が結紮されるたびに、側副血行網の圧は落ちる"],
             style="amber", title="② 遮断中に起きていること",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["MEP・SSEP が落ちたら、まず MAP を上げ、CSF を排液する",
              "同時に、外科医に分節動脈の再建を検討してもらう",
              "Hb と酸素化も確認する（運べる量の問題かもしれない）"],
             style="red", title="③ 電位が落ちたとき", title_color=RED)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["排液は「量の上限」を決めて行う（一度に大量に抜かない）",
              "目標 CSF 圧に達したら止める",
              "ドレーンの高さと体位で圧は簡単に変わる"],
             style="green", title="④ 髄液排液の原則", title_color=GREEN)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["遮断解除後は血圧が下がりやすい。ここで SCPP が落ちる",
          "閉創・移送・ICU 入室の各段階で、MAP の目標を引き継ぐ",
          "「手術が終わったから目標も終わり」にしない"],
         style="purple", title="⑤ 遮断解除から ICU まで", title_color=PURPLE)
    cv.save(P("h13_alg_scpp.png"))
    crop_bottom(P("h13_alg_scpp.png"))


# ---------------------------------------------------------------- h14
def h14():
    """Alg3-3 術後に下肢が動かない"""
    cv = Canvas(W, 2000)
    cap(cv, 44, "アルゴリズム 3　術後に下肢が動かないとき")

    cx = W / 2
    bw = 800
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["麻酔からの覚醒が不十分なだけではないか",
              "硬膜外麻酔・区域麻酔の影響が残っていないか",
              "左右差はあるか、感覚は残っているか（前脊髄動脈症候群か）"],
             style="navy", title="① まず、何が起きているかを分ける",
             title_color=NAVY)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["MAP をただちに上げる（目標を一段高く設定し直す）",
              "髄液を排液し、CSF 圧を下げる",
              "Hb を確認し、必要なら輸血する",
              "酸素化を最適化する"],
             style="red", title="② 同時に、SCPP を上げにいく",
             title_color=RED)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["ドレーンが入っていなければ、この時点で入れる判断をする",
              "ただし治療的な留置で救済できない例があることを知っておく",
              "抗凝固の状況を確認してから穿刺する"],
             style="amber", title="③ ドレーンが入っていない場合",
             title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["硬膜外血腫・脊髄血腫を除外する（緊急 MRI）",
              "血腫であれば、対応はまったく別になる",
              "画像を待つ間も、SCPP を上げる手は止めない"],
             style="blue", title="④ 鑑別を同時に進める", title_color=BLUE)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["発症時刻、そのときの MAP と CSF 圧、行った介入を記録する",
          "回復した症例でも、再発することがある（監視を続ける）",
          "遅発性対麻痺は予後を大きく変える。チームで情報を共有する"],
         style="purple", title="⑤ 記録と再発への備え", title_color=PURPLE)
    cv.save(P("h14_alg_rescue.png"))
    crop_bottom(P("h14_alg_rescue.png"))


# ---------------------------------------------------------------- h15
def h15():
    """Alg3-4 ドレーンのトラブル"""
    cv = Canvas(W, 1800)
    cap(cv, 44, "アルゴリズム 4　髄液ドレーンのトラブル対応")

    cx = W / 2
    bw = 800
    y = 110
    h = step(cv, cx - bw / 2, y, bw,
             ["排液が出ない：閉塞か、位置異常か、髄液圧が低いだけか",
              "波形が出ているかを確認する",
              "無理に吸引しない"],
             style="blue", title="① 排液が出ないとき", title_color=BLUE)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["決めた上限を超えて出ていないか",
              "過剰排液は頭蓋内低圧・硬膜下血腫の原因になる",
              "ドレーンの高さと開放時間を管理する"],
             style="red", title="② 出すぎているとき", title_color=RED)
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    h = step(cv, cx - bw / 2, y, bw,
             ["血性の髄液は、穿刺時の出血か、脊髄・硬膜下出血の可能性",
              "抗凝固の状況と神経所見を必ず合わせて評価する",
              "術前であれば、手術の延期を検討する状況でもある"],
             style="amber", title="③ 血性の排液", title_color="#9a6510")
    y += h
    down(cv, cx, y, y + 44)
    y += 44
    step(cv, cx - bw / 2, y, bw,
         ["抜去のタイミングは、神経所見が安定してから",
          "抗凝固再開との順番を決めておく（血腫のリスク）",
          "抜去後も、下肢の動きを一定時間観察する"],
         style="green", title="④ 抜去", title_color=GREEN)
    cv.save(P("h15_alg_drain_trouble.png"))
    crop_bottom(P("h15_alg_drain_trouble.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (h08, h09, h10, h11, h12, h13, h14, h15):
        fn()
        print("ok", fn.__name__)
