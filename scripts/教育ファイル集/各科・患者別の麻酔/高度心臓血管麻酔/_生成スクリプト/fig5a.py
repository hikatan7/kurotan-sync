# -*- coding: utf-8 -*-
"""第Ⅴ章 TAVI・三尖弁　図版 n01〜n07"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figlib import (Canvas, LH, textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
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


# ---------------------------------------------------------------- n01
def n01():
    """章の地図：開く弁と閉じない弁"""
    cv = Canvas(W, 1000)
    cap(cv, 44, "この章で扱う二つの弁は、麻酔科にとって別の問題である")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 520

    def panel(x, title, color, fc, big, lines, bottom):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.box(x, PY, PW, 58, fc=color, ec=color, lw=0, radius=10)
        cv.text(x + PW / 2, PY + 29, title,
                size=fit(cv, title, PW - 44, 12.6, "bold"), color="white",
                weight="bold")
        cv.text(x + PW / 2, PY + 110, big,
                size=fit(cv, big, PW - 60, 14.5, "bold"), color=color,
                weight="bold")
        yy = PY + 160
        for ln in lines:
            cv.text(x + PW / 2, yy, ln, size=fit(cv, ln, PW - 60, 10.6),
                    color=INK)
            yy += 38
        bl = cv.wrap(bottom, PW - 80, 10.4)
        bh = 26 + LH(10.4, 1.6) * len(bl)
        cv.box(x + 26, PY + PH - bh - 24, PW - 52, bh, fc=fc, ec=color,
               lw=1.6, radius=8)
        for j, ln in enumerate(bl):
            cv.text(x + PW / 2,
                    PY + PH - bh - 24 + 13 + LH(10.4, 1.6) * (j + 0.5), ln,
                    size=10.4, color=INK)

    panel(x1, "大動脈弁（TAVI）", BLUE, "#eaf1f8",
          "狭い弁が、急に開く",
          ["後負荷が一気に下がる", "冠動脈が塞がれることがある",
           "刺激伝導系がすぐ隣を走っている",
           "rapid pacing で意図的に心拍出を止める"],
          "多くは局所麻酔と鎮静で行われる。麻酔科は「急変したときの人」として立ち会う")

    panel(x2, "三尖弁（T-TEER・TTVR）", GREEN, "#eaf5ee",
          "閉じない弁を、閉じにいく",
          ["右室の後負荷が上がる", "もともと右心不全がある",
           "肝・腎のうっ血を抱えている",
           "リードが弁を跨いでいることがある"],
          "長時間の経食道心エコーが要る。全身麻酔が基本になる")

    th = textbox(cv, 70, PY + PH + 26, W - 140,
                 ["大動脈弁では「開いた瞬間」に、三尖弁では「閉じた瞬間」に、"
                  "心室の条件が変わる。",
                  "前章の僧帽弁と同じ構造である。"
                  "違うのは、どちらの心室が引き受けるかである。"],
                 10.8, style="navy", pad_y=16)
    cv.save(P("n01_map.png"))
    crop_bottom(P("n01_map.png"))


# ---------------------------------------------------------------- n02
def n02():
    """TAVI の主要試験"""
    cv = Canvas(W, 1700)
    cap(cv, 44, "TAVI はどこまで適応を広げたのか")

    ROWS = [("PARTNER 2（2016）", GREY, "中等度リスク",
             "TAVR は外科手術に非劣性であった", "中等度リスクへ"),
            ("PARTNER 3（2019）", GREEN, "低リスク 1,000 例（STS 1.9%）",
             "1 年の死亡・脳卒中・再入院は TAVR で有意に低い"
             "（HR 0.54、95%CI 0.37-0.79、p=0.001）", "低リスクへ"),
            ("Evolut Low Risk（2019）", BLUE, "低リスク 1,468 例",
             "24 か月の死亡・後遺症を残す脳卒中 5.3% 対 6.7% で非劣性",
             "自己拡張型でも低リスクへ"),
            ("Evolut 6 年（2026）", ORANGE, "同試験の長期追跡",
             "6 年の死亡・後遺症を残す脳卒中 23.3% 対 20.4%"
             "（差 2.8%、95%CI -1.9〜7.6、p=0.43）",
             "長期では差が縮まらない"),
            ("DEDICATE（2024）", PURPLE, "低〜中等度リスク 1,414 例",
             "1 年の死亡・脳卒中 5.4% 対 10.0%（HR 0.53）",
             "企業主導でない試験"),
            ("NOTION 10 年（2025）", TEAL, "低リスク・長期追跡",
             "10 年の成績が報告された（耐久性が論点）", "若年への適応の議論")]

    y = 130
    for name, col, pop, res, verdict in ROWS:
        h = 170
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.7, radius=10)
        cv.box(70, y, 330, h, fc="#fbfcfd", ec=col, lw=0, radius=10)
        cv.text(235, y + 50, name, size=fit(cv, name, 290, 11.8, "bold"),
                color=col, weight="bold")
        cv.box(96, y + 84, 278, 52, fc=col, ec=col, lw=0, radius=8)
        cv.text(235, y + 110, verdict,
                size=fit(cv, verdict, 250, 11.0, "bold"), color="white",
                weight="bold")
        cv.text(420, y + 48, pop, size=fit(cv, pop, W - 520, 10.2),
                color=GREY, ha="left")
        for j, ln in enumerate(cv.wrap(res, W - 520, 10.6)):
            cv.text(420, y + 92 + LH(10.6, 1.5) * j, ln, size=10.6,
                    color=INK, ha="left")
        y += h + 14

    textbox(cv, 70, y + 10, W - 140,
            ["低リスクへの拡大は、1 年の成績で決まった。",
             "しかし Evolut の 6 年追跡では、"
             "死亡・後遺症を残す脳卒中は 23.3% 対 20.4% と差がなくなっている。",
             "「若い患者に入れたあと、20 年後にどうするか」は未解決の問題である。"],
            10.6, style="amber", title="長期をどう考えるか",
            title_color="#9a6510", pad_y=16)
    cv.save(P("n02_tavi_trials.png"))
    crop_bottom(P("n02_tavi_trials.png"))


# ---------------------------------------------------------------- n03
def n03():
    """TAVI の手技と rapid pacing"""
    cv = Canvas(W, 1000)
    cap(cv, 44, "意図的に心拍出を止める時間がある")

    x0, y0 = 90, 170
    pw, ph = W - 180, 260
    cv.rect(x0, y0, pw, ph, fc="#fbfcfd", ec="#dde3ea", lw=1.4)
    cv.text(x0 + 6, y0 - 16, "血圧", size=9.6, color=GREY, ha="left")

    # 血圧曲線（rapid pacing で落ちる）
    import numpy as np
    t = np.linspace(0, 1, 800)
    base = y0 + ph * 0.42
    amp = 42
    wave = np.sin(t * 90) * amp
    drop = np.where((t > 0.42) & (t < 0.56), 1.0, 0.0)
    y = base - wave * (1 - drop * 0.86) + drop * 92
    cv.ax.plot(x0 + t * pw, y, color=NAVY, lw=2.0, zorder=4)
    cv.rect(x0 + pw * 0.40, y0 + 10, pw * 0.18, ph - 20, fc="#fceeec",
            alpha=0.75)
    cv.text(x0 + pw * 0.49, y0 + 40, "rapid pacing", size=11.0, color=RED,
            weight="bold")
    cv.text(x0 + pw * 0.49, y0 + ph - 26, "拍出がほぼ止まる", size=10.0,
            color=RED)

    STEP = [("① アクセス", "大腿動脈（多くは経皮）"),
            ("② ワイヤ通過", "狭窄した弁を越える"),
            ("③ rapid pacing", "拍出を止めて弁を留置する"),
            ("④ 弁の展開", "位置がずれれば戻せない"),
            ("⑤ 評価", "傍弁逆流・冠動脈・伝導障害"),
            ("⑥ 止血", "血管合併症はここで決まる")]
    w = (W - 140 - 5 * 20) / 6
    for i, (t2, sub) in enumerate(STEP):
        x = 70 + (w + 20) * i
        cv.box(x, 480, w, 130, fc="#ffffff", ec=NAVY, lw=1.6, radius=8)
        cv.text(x + w / 2, 512, t2, size=fit(cv, t2, w - 20, 10.6, "bold"),
                color=NAVY, weight="bold")
        for j, ln in enumerate(cv.wrap(sub, w - 24, 9.6)):
            cv.text(x + w / 2, 546 + LH(9.6, 1.35) * j, ln, size=9.6, color=INK)

    th = textbox(cv, 70, 650, W - 140,
                 ["rapid pacing は、心室を高頻度でペーシングして"
                  "拍出をほぼゼロにする手技である。",
                  "その間、冠灌流も脳灌流も止まる。"
                  "短時間で終えること、そして終了後に血圧が戻ることを確認することが要る。",
                  "戻らないときは、弁の位置・冠動脈・心タンポナーデを疑う。"],
                 10.6, style="red", title="麻酔科が見ているもの",
                 title_color=RED, pad_y=16)

    msg(cv, 650 + th + 28,
        "「止める時間」があることを、チーム全員が同じ理解で共有しておく")
    cv.save(P("n03_rapid_pacing.png"))
    crop_bottom(P("n03_rapid_pacing.png"))


# ---------------------------------------------------------------- n04
def n04():
    """TAVI の麻酔法"""
    cv = Canvas(W, 1200)
    cap(cv, 44, "TAVI の麻酔は、局所麻酔と鎮静が主流になった")

    x0, y0 = 70, 130
    cv.box(x0, y0, W - 140, 300, fc="#ffffff", ec=BLUE, lw=1.8, radius=10)
    cv.text(W / 2, y0 + 36, "40 研究 14,388 例のメタ解析（局所麻酔 7,754 例 対 全身麻酔 6,634 例）",
            size=fit(cv,
                     "40 研究 14,388 例のメタ解析（局所麻酔 7,754 例 対 全身麻酔 6,634 例）",
                     W - 220, 12.0, "bold"), color=BLUE, weight="bold")
    ITEM = [("30 日死亡", "RR 0.69", "p<0.01", GREEN),
            ("脳卒中", "RR 0.78", "p=0.02", GREEN),
            ("大出血", "RR 0.64", "p=0.01", GREEN),
            ("主要血管合併症", "RR 0.76", "p=0.02", GREEN),
            ("長期死亡", "RR 0.75", "p=0.009", GREEN),
            ("傍弁逆流", "RR 0.88", "p=0.12（差なし）", GREY)]
    w = (W - 200 - 5 * 16) / 6
    for i, (lab, rr, pv, col) in enumerate(ITEM):
        x = 100 + (w + 16) * i
        cv.box(x, y0 + 78, w, 190, fc="#fbfcfd", ec=col, lw=1.5, radius=8)
        cv.text(x + w / 2, y0 + 112, lab, size=fit(cv, lab, w - 16, 10.2),
                color=INK)
        cv.text(x + w / 2, y0 + 168, rr, size=fit(cv, rr, w - 20, 15, "bold"),
                color=col, weight="bold")
        cv.text(x + w / 2, y0 + 220, pv, size=fit(cv, pv, w - 16, 9.4),
                color=GREY)

    y1 = y0 + 330
    cv.box(70, y1, W - 140, 200, fc="#ffffff", ec=GREEN, lw=1.8, radius=10)
    cv.text(W / 2, y1 + 36, "ドイツ大動脈弁レジストリ 16,543 例（うち鎮静 49%）",
            size=12.0, color=GREEN, weight="bold")
    L = ["鎮静群では、低心拍出症候群・呼吸不全・せん妄・心肺蘇生・死亡が少なかった",
         "傍弁逆流（II 度以上）は 5% 対 4.8% で差はなかった",
         "ただし観察研究であり、患者選択の影響を否定できない"]
    for j, ln in enumerate(L):
        cv.text(W / 2, y1 + 86 + 44 * j, ln,
                size=fit(cv, ln, W - 220, 10.6), color=INK)

    th = textbox(cv, 70, y1 + 230, W - 140,
                 ["これらの数字は観察研究をまとめたものであり、"
                  "無作為化比較試験ではない。",
                  "「全身麻酔が悪い」のではなく、"
                  "「全身麻酔を選ばざるを得ない患者はもともと重い」可能性がある。",
                  "それでも、局所麻酔と鎮静で行える症例では"
                  "そちらを選ぶ流れが定着している。"],
                 10.6, style="amber", title="この数字の読み方",
                 title_color="#9a6510", pad_y=16)
    cv.save(P("n04_tavi_anesthesia.png"))
    crop_bottom(P("n04_tavi_anesthesia.png"))


# ---------------------------------------------------------------- n05
def n05():
    """TAVI の合併症"""
    cv = Canvas(W, 1300)
    cap(cv, 44, "TAVI で起こること、そのとき最初にすること")

    ROWS = [("冠動脈閉塞", RED, "弁尖が冠動脈入口部を覆う",
             "ST 上昇・心室細動・急な循環虚脱。心筋虚血として現れる"),
            ("弁輪破裂", RED, "過拡張・石灰化",
             "心タンポナーデ。経食道心エコーで心嚢を見る"),
            ("弁の位置異常・移動", ORANGE, "展開のタイミング",
             "傍弁逆流・僧帽弁の障害・冠動脈の閉塞につながる"),
            ("伝導障害・完全房室ブロック", PURPLE, "刺激伝導系が弁輪の直下にある",
             "徐脈。一時ペーシングの確保が前提になる"),
            ("血管合併症・出血", ORANGE, "大腿動脈のアクセス",
             "後腹膜出血は術野では見えない。Hb と腹部を見る"),
            ("脳卒中", BLUE, "石灰化片・空気の塞栓",
             "覚醒下なら神経所見で気づける（鎮静の利点のひとつ）"),
            ("急性大動脈弁逆流", RED, "弁の展開途中",
             "拡張期血圧の低下と左室の急激な負荷")]

    y = 130
    for name, col, cause, what in ROWS:
        h = 116
        cv.box(70, y, W - 140, h, fc="#ffffff", ec=col, lw=1.5, radius=8)
        cv.box(70, y, 340, h, fc="#fbfcfd", ec=col, lw=0, radius=8)
        cv.text(94, y + 44, name, size=fit(cv, name, 300, 11.4, "bold"),
                color=col, weight="bold", ha="left")
        cv.text(94, y + 80, cause, size=fit(cv, cause, 300, 9.4),
                color=GREY, ha="left")
        cv.text(430, y + h / 2, what, size=fit(cv, what, W - 520, 10.6),
                color=INK, ha="left")
        y += h + 10

    th = textbox(cv, 70, y + 12, W - 140,
                 ["PARTNER 3 では、主要血管合併症・新規ペースメーカー植込み・"
                  "中等度以上の傍弁逆流について、",
                  "TAVR と外科手術のあいだに有意差はなかった。",
                  "つまりこれらは「TAVI だから多い合併症」ではなく、"
                  "「この治療に伴う合併症」として扱う。"],
                 10.6, style="navy", title="頻度の位置づけ", title_color=NAVY,
                 pad_y=16)
    cv.save(P("n05_tavi_complications.png"))
    crop_bottom(P("n05_tavi_complications.png"))


# ---------------------------------------------------------------- n06
def n06():
    """脳塞栓防止デバイス"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "脳を守るデバイスは、脳卒中を減らさなかった")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 440

    def panel(x, title, n, color, rows, concl):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.box(x, PY, PW, 56, fc=color, ec=color, lw=0, radius=10)
        cv.text(x + PW / 2, PY + 28, title,
                size=fit(cv, title, PW - 40, 12.2, "bold"), color="white",
                weight="bold")
        cv.text(x + PW / 2, PY + 88, n, size=fit(cv, n, PW - 60, 11.0),
                color=GREY)
        yy = PY + 130
        for lab, a, b in rows:
            cv.text(x + 40, yy, lab, size=10.4, color=INK, ha="left")
            cv.text(x + PW - 40, yy, a, size=11.4, color=color, ha="right",
                    weight="bold")
            yy += 40
            cv.text(x + PW - 40, yy - 16, b, size=9.4, color=GREY,
                    ha="right")
            yy += 26
        cl = cv.wrap(concl, PW - 80, 10.4)
        for j, ln in enumerate(cl):
            cv.text(x + PW / 2, PY + PH - 70 + LH(10.4, 1.5) * j, ln,
                    size=10.4, color=color, weight="bold")

    panel(x1, "PROTECTED TAVR（2022）", "3,000 例（デバイス 1,501／対照 1,499）",
          BLUE,
          [("72 時間以内の脳卒中", "2.3% 対 2.9%", "有意差なし"),
           ("デバイス留置成功", "94.4%", "留置自体は可能")],
          "主要評価項目では差がなかった")

    panel(x2, "BHF PROTECT-TAVI（2025）",
          "7,635 例（デバイス 3,815／対照 3,820）", RED,
          [("脳卒中", "2.1% 対 2.2%", "差 -0.02%（95%CI -0.68〜0.63）"),
           ("後遺症を残す脳卒中", "1.2% 対 1.4%", "p=0.94")],
          "ルーチンでの使用は支持されない")

    th = textbox(cv, 70, PY + PH + 26, W - 140,
                 ["塞栓防止デバイスは、フィルターに実際にデブリが捕まる。",
                  "それでも臨床的な脳卒中は減らなかった。",
                  "「捕まえられること」と「転帰が変わること」は別である"
                  "という、この本で繰り返し出てくる主題がここにもある。"],
                 10.8, style="red", title="捕まえても、減らなかった",
                 title_color=RED, pad_y=16)

    msg(cv, PY + PH + 26 + th + 28,
        "7,635 例の無作為化試験が出た以上、この記述は更新しておく必要がある",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("n06_cep.png"))
    crop_bottom(P("n06_cep.png"))


# ---------------------------------------------------------------- n07
def n07():
    """冠動脈閉塞と弁尖切開"""
    cv = Canvas(W, 1000)
    cap(cv, 44, "弁尖が冠動脈をふさぐ前に、切っておく")

    STEP = [("① 危険を予測する", BLUE, "#eaf1f8",
             ["冠動脈入口部が低い", "Valsalva 洞が狭い",
              "生体弁の中に入れる（valve-in-valve）"]),
            ("② 弁尖を裂く", PURPLE, "#f1ecf8",
             ["電気を用いて弁尖を縦に切る", "血流の通り道をつくる"]),
            ("③ 弁を留置する", GREEN, "#eaf5ee",
             ["裂けた弁尖は冠動脈をふさがない", "そのまま TAVI を続ける"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(STEP):
        x = 70 + (w + 30) * i
        card(cv, x, 140, w, t, lines, col, fc, body_size=10.2, lh=1.8)
        if i < 2:
            cv.arrow((x + w + 4, 230), (x + w + 26, 230), color="#b9c2cc",
                     lw=2.0, head=10)

    y1 = 420
    cv.box(70, y1, W - 140, 200, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(W / 2, y1 + 38, "国際多施設レジストリ 214 例（25 施設）",
            size=12.2, color=NAVY, weight="bold")
    L = [("弁尖の通過成功", "94.9%"), ("弁尖の切開成功", "94.4%"),
         ("部分または完全な冠動脈閉塞", "4.7%")]
    w2 = (W - 200) / 3
    for i, (lab, val) in enumerate(L):
        x = 100 + w2 * i
        cv.text(x + w2 / 2, y1 + 96, lab, size=fit(cv, lab, w2 - 30, 10.6),
                color=INK)
        cv.text(x + w2 / 2, y1 + 150, val, size=20, color=NAVY,
                weight="bold")

    th = textbox(cv, 70, y1 + 230, W - 140,
                 ["対象の 72.8% は、劣化した生体弁の中に新しい弁を入れる症例であった。",
                  "麻酔科にとっての要点は、"
                  "「この症例は冠動脈閉塞のリスクが高い」と事前に共有されていることである。",
                  "起きてから対応するのと、起こりうると知って待つのとでは、"
                  "初動がまったく違う。"],
                 10.6, style="amber", title="誰に行うのか",
                 title_color="#9a6510", pad_y=16)
    cv.save(P("n07_basilica.png"))
    crop_bottom(P("n07_basilica.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (n01, n02, n03, n04, n05, n06, n07):
        fn()
        print("ok", fn.__name__)
