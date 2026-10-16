# -*- coding: utf-8 -*-
"""第Ⅶ章 横断（CPB・PBM・循環）　図版 r01〜r07"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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


# ---------------------------------------------------------------- r01
def r01():
    """本書全体の地図"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "本書が扱ってきた六つの章と、それを貫くもの")

    CH = [("第Ⅰ章", "CIED", BLUE, "止めるべきものが二つある"),
          ("第Ⅱ章", "脳保護", PURPLE, "方法ではなく、届いているか"),
          ("第Ⅲ章", "脊髄保護", GREEN, "引き算で守る"),
          ("第Ⅳ章", "M-TEER", RED, "逆流を止めた瞬間に条件が変わる"),
          ("第Ⅴ章", "TAVI・三尖弁", ORANGE, "開く弁と、閉じない弁"),
          ("第Ⅵ章", "透析患者", TEAL, "腎臓の仕事が六つ止まっている")]

    w = (W - 140 - 2 * 30) / 3
    for i, (no, name, col, sub) in enumerate(CH):
        r, c = divmod(i, 3)
        x = 70 + (w + 30) * c
        y = 130 + r * 230
        cv.box(x, y, w, 190, fc="#ffffff", ec=col, lw=1.8, radius=10)
        cv.box(x, y, w, 50, fc=col, ec=col, lw=0, radius=10)
        cv.text(x + w / 2, y + 25, "%s　%s" % (no, name),
                size=fit(cv, "%s　%s" % (no, name), w - 30, 11.8, "bold"),
                color="white", weight="bold")
        ss = fit(cv, sub, w - 34, 11.0, "normal")
        cv.text(x + w / 2, y + 118, sub, size=ss, color=INK)

    cx = W / 2
    cv.box(cx - 340, 600, 680, 90, fc="#0f6d78", ec="#0f6d78", lw=0,
           radius=10)
    t = "第Ⅶ章　すべての章を横断するもの"
    cv.text(cx, 645, t, size=fit(cv, t, 620, 14.0, "bold"), color="white",
            weight="bold")
    # 六つの章から第Ⅶ章へ：線が下段の箱を横切らないよう、下段の下で 1 本にまとめる
    yb = 130 + 230 + 190
    xs = [70 + (w + 30) * c + w / 2 for c in range(3)]
    for x in xs:
        cv.rect(x - 1, yb, 2, 16, fc="#b9c2cc")
    cv.rect(xs[0] - 1, yb + 15, xs[-1] - xs[0] + 2, 2, fc="#b9c2cc")
    cv.arrow((cx, yb + 16), (cx, 596), color="#b9c2cc", lw=1.6, head=9)

    C = [("人工心肺", BLUE, "#eaf1f8",
          ["抗凝固と ACT", "血液希釈と限外濾過", "温度管理と循環停止"]),
         ("出血と輸血", RED, "#fceeec",
          ["術前貧血", "輸血閾値", "線溶抑制と粘弾性検査"]),
         ("循環の目標", GREEN, "#eaf5ee",
          ["術中低血圧", "血管麻痺", "離脱困難と補助循環"])]
    w2 = (W - 140 - 60) / 3
    for i, (t2, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w2 + 30) * i, 730, w2, t2, lines, col, fc,
             body_size=10.4, lh=1.8)
    cv.save(P("r01_book_map.png"))
    crop_bottom(P("r01_book_map.png"))


# ---------------------------------------------------------------- r02
def r02():
    """共通フレーム 10 項目"""
    cv = Canvas(W, 1200)
    cap(cv, 44, "どの手術でも、この順に考える")

    ITEMS = [("① 病態", "何が壊れているのか"),
             ("② 解剖", "どこを触るのか"),
             ("③ 血行動態", "前負荷・後負荷・収縮力・リズム"),
             ("④ 術前リスク", "この患者は何に耐えられないか"),
             ("⑤ 麻酔導入", "どの瞬間が危ないか"),
             ("⑥ モニタリング", "何を測れば、何が分かるか"),
             ("⑦ 術操作の節目", "いつ条件が変わるのか"),
             ("⑧ 循環補助", "支える手段は何か"),
             ("⑨ 凝固と輸血", "止血をどう組み立てるか"),
             ("⑩ ICU・術後", "何を引き継ぐのか")]

    w = (W - 140 - 4 * 24) / 5
    for i, (t, sub) in enumerate(ITEMS):
        r, c = divmod(i, 5)
        x = 70 + (w + 24) * c
        y = 140 + r * 210
        cv.box(x, y, w, 170, fc="#ffffff", ec=NAVY, lw=1.6, radius=10)
        cv.box(x, y, w, 48, fc=NAVY, ec=NAVY, lw=0, radius=10)
        cv.text(x + w / 2, y + 24, t, size=fit(cv, t, w - 24, 11.2, "bold"),
                color="white", weight="bold")
        for j, ln in enumerate(cv.wrap(sub, w - 32, 10.0)):
            cv.text(x + w / 2, y + 88 + LH(10.0, 1.35) * j, ln, size=10.0, color=INK)
        if c < 4:
            cv.arrow((x + w + 3, y + 85), (x + w + 21, y + 85),
                     color="#b9c2cc", lw=1.6, head=8)

    th = textbox(cv, 70, 580, W - 140,
                 ["本書の六つの章は、いずれもこの十項目の順に書かれている。",
                  "章が変われば中身は変わるが、順序は変わらない。",
                  "新しいデバイスや術式に出会ったときも、"
                  "この順に埋めていけば計画は立つ。"],
                 10.8, style="navy", title="順序は変わらない",
                 title_color=NAVY, pad_y=16)

    y2 = 580 + th + 30
    KEY = [("⑥ で問うこと", PURPLE, "#f1ecf8",
            ["何を測れるのか", "測った値は何を意味するのか",
             "測って介入すると転帰は変わるのか"]),
           ("⑦ で問うこと", ORANGE, "#fdf3e3",
            ["いつ条件が変わるのか", "その瞬間に何が起こりうるか",
             "備えは何か"])]
    w3 = (W - 140 - 30) / 2
    for i, (t, col, fc, lines) in enumerate(KEY):
        card(cv, 70 + (w3 + 30) * i, y2, w3, t, lines, col, fc,
             body_size=10.4, lh=1.8)
    cv.save(P("r02_framework.png"))
    crop_bottom(P("r02_framework.png"))


# ---------------------------------------------------------------- r03
def r03():
    """CPB ガイドライン 2024 の範囲"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "人工心肺のガイドラインが、扱う範囲を広げた")

    PW = (W - 190) / 2
    x1, x2 = 70, 70 + PW + 50
    PY, PH = 130, 420

    def panel(x, title, color, fc, lines):
        cv.box(x, PY, PW, PH, fc="#ffffff", ec=color, lw=1.8, radius=10)
        cv.box(x, PY, PW, 56, fc=color, ec=color, lw=0, radius=10)
        cv.text(x + PW / 2, PY + 28, title,
                size=fit(cv, title, PW - 40, 12.4, "bold"), color="white",
                weight="bold")
        yy = PY + 96
        for ln in lines:
            cv.text(x + 40, yy, "・" + ln,
                    size=fit(cv, "・" + ln, PW - 80, 10.6), color=INK,
                    ha="left")
            yy += 42

    panel(x1, "2019 年版までの主題", GREY, "#f2f4f6",
          ["回路と充填", "抗凝固とモニタリング（ACT）",
           "血液希釈と限外濾過", "灌流圧と流量",
           "心筋保護の実際"])
    panel(x2, "2024 年版で拡張された範囲", BLUE, "#eaf1f8",
          ["温度管理（冷却と復温の速度・目標）",
           "深低体温循環停止（DHCA）",
           "脳保護の補助手段との関係",
           "多職種（外科・麻酔・灌流）での運用",
           "施設としての質の担保"])

    th = textbox(cv, 70, PY + PH + 26, W - 140,
                 ["2024 年の EACTS・EACTAIC・EBCP 合同ガイドラインは、"
                  "2019 年版を改訂したものである。",
                  "温度管理と循環停止まで対象に含めたことで、"
                  "第Ⅱ章（脳保護）と同じ土俵に立った。",
                  "同じ年に、患者血液管理（PBM）のガイドラインも改訂されている。",
                  "いずれも 2025 年に各誌へ同時掲載されたため、"
                  "引用の年号には注意が要る。"],
                 10.6, style="navy", title="二つのガイドラインの関係",
                 title_color=NAVY, pad_y=16)

    msg(cv, PY + PH + 26 + th + 28,
        "灌流技士と同じ資料を読んでおくと、術中の会話が変わる")
    cv.save(P("r03_cpb_guideline.png"))
    crop_bottom(P("r03_cpb_guideline.png"))


# ---------------------------------------------------------------- r04
def r04():
    """PBM の三本柱"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "患者血液管理は、三つの柱で考える")

    C = [("① 赤血球量を増やす／守る", BLUE, "#eaf1f8",
          ["術前貧血の評価と治療", "鉄・造血刺激因子",
           "採血量そのものを減らす", "回収式自己血輸血"]),
         ("② 出血を減らす", RED, "#fceeec",
          ["抗血栓薬の管理", "外科的止血",
           "線溶抑制薬（トラネキサム酸）", "体温・カルシウム・pH を保つ"]),
         ("③ 貧血への耐性を高める", GREEN, "#eaf5ee",
          ["酸素需給の最適化", "適切な輸血閾値",
           "「Hb の数字」ではなく患者を見る"])]
    w = (W - 140 - 60) / 3
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 140, w, t, lines, col, fc,
             body_size=10.4, lh=1.8)

    y1 = 520
    cv.box(70, y1, W - 140, 260, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(W / 2, y1 + 38, "本書の各章との対応", size=12.4, color=NAVY,
            weight="bold")
    L = [("第Ⅲ章（脊髄保護）", "赤血球輸血は SCI の危険因子でもあり、"
          "同時に酸素運搬の手段でもある"),
         ("第Ⅵ章（透析患者）", "慢性貧血に適応した患者では、"
          "輸血閾値の考え方が変わる"),
         ("第Ⅳ・Ⅴ章（構造的心疾患）", "抗血栓薬の管理が、"
          "手技の合併症と直結する")]
    yy = y1 + 82
    for a, b in L:
        cv.text(110, yy + 20, a, size=fit(cv, a, 380, 10.8, "bold"),
                color=NAVY, weight="bold", ha="left")
        cv.text(520, yy + 20, b, size=fit(cv, b, W - 660, 10.6), color=INK,
                ha="left")
        yy += 56

    msg(cv, y1 + 290,
        "輸血を減らすことが目的ではない。酸素を届けることが目的である")
    cv.save(P("r04_pbm.png"))
    crop_bottom(P("r04_pbm.png"))


# ---------------------------------------------------------------- r05
def r05():
    """輸血閾値（TRICS III）"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "制限的な輸血で、転帰は変わらなかった")

    x0, y0 = 70, 130
    cv.box(x0, y0, W - 140, 120, fc="#e8edf5", ec=NAVY, lw=1.8, radius=10)
    t = "心臓手術 5,243 例を、制限的輸血と寛容的輸血に無作為に割り付けた"
    cv.text(W / 2, y0 + 62, t, size=fit(cv, t, W - 220, 12.6, "bold"),
            color=NAVY, weight="bold")

    ROWS = [("主要複合エンドポイント（退院時）", "11.4%", "12.5%",
             "オッズ比 0.90（非劣性 p<0.001）"),
            ("死亡（退院時）", "3.0%", "3.6%", "─"),
            ("主要複合エンドポイント（6 か月）", "17.4%", "17.1%",
             "オッズ比 1.02（非劣性 p=0.006）"),
            ("死亡（6 か月）", "6.2%", "6.4%", "オッズ比 0.95")]
    y = y0 + 150
    cv.box(70, y, W - 140, 60, fc="#1f3864", ec="#1f3864", lw=0, radius=8)
    for lab, px in (("項目", 0.24), ("制限的", 0.54), ("寛容的", 0.68),
                    ("統計", 0.86)):
        cv.text(70 + (W - 140) * px, y + 30, lab, size=10.8, color="white",
                weight="bold")
    y += 66
    for lab, a, b, st in ROWS:
        cv.box(70, y, W - 140, 74, fc="#ffffff", ec="#dde3ea", lw=1.3,
               radius=6)
        cv.text(110, y + 37, lab, size=fit(cv, lab, 560, 10.8), color=INK,
                ha="left")
        cv.text(70 + (W - 140) * 0.54, y + 37, a, size=12.4, color=BLUE,
                weight="bold")
        cv.text(70 + (W - 140) * 0.68, y + 37, b, size=12.4, color=GREY,
                weight="bold")
        cv.text(70 + (W - 140) * 0.86, y + 37, st,
                size=fit(cv, st, 330, 10.0), color=GREY)
        y += 82

    th = textbox(cv, 70, y + 14, W - 140,
                 ["制限的輸血は、退院時でも 6 か月後でも寛容的輸血に非劣性であった。",
                  "この結果は「輸血してはいけない」という意味ではない。",
                  "「Hb の数字だけで反射的に輸血する必要はない」という意味である。",
                  "第Ⅲ章では赤血球輸血が脊髄虚血の危険因子として挙がり、"
                  "第Ⅵ章では慢性貧血への適応が問題になった。",
                  "閾値は、患者と場面によって決まる。"],
                 10.6, style="navy", title="この結果の意味",
                 title_color=NAVY, pad_y=16)
    cv.save(P("r05_trics.png"))
    crop_bottom(P("r05_trics.png"))


# ---------------------------------------------------------------- r06
def r06():
    """トラネキサム酸（ATACAS）"""
    cv = Canvas(W, 1100)
    cap(cv, 44, "出血は減った。けいれんは増えた")

    x0, y0 = 70, 130
    cv.box(x0, y0, W - 140, 110, fc="#e8edf5", ec=NAVY, lw=1.8, radius=10)
    t = "冠動脈手術 4,631 例（トラネキサム酸 2,311 例 対 プラセボ 2,320 例）"
    cv.text(W / 2, y0 + 58, t, size=fit(cv, t, W - 220, 12.4, "bold"),
            color=NAVY, weight="bold")

    CARDS = [("主要エンドポイント\n（死亡・血栓性合併症）", "16.7%", "18.1%",
              "RR 0.92（0.81-1.05）　p=0.22", GREY, "#f2f4f6"),
             ("再開胸を要する大出血・\n心タンポナーデ", "1.4%", "2.8%",
              "p=0.001", GREEN, "#eaf5ee"),
             ("術後けいれん", "0.7%", "0.1%", "p=0.002", RED, "#fceeec")]
    w = (W - 140 - 60) / 3
    for i, (lab, a, b, st, col, fc) in enumerate(CARDS):
        x = 70 + (w + 30) * i
        cv.box(x, y0 + 140, w, 300, fc="#ffffff", ec=col, lw=1.8, radius=10)
        cv.box(x, y0 + 140, w, 76, fc=col, ec=col, lw=0, radius=10)
        for j, ln in enumerate(lab.split("\n")):
            cv.text(x + w / 2, y0 + 168 + 30 * j,
                    ln, size=fit(cv, ln, w - 30, 10.8, "bold"),
                    color="white", weight="bold")
        duo(cv, x + w / 2, y0 + 268, a, b, size=20, col_a=col,
            lab_a="TXA", lab_b="プラセボ", lab_dy=38, lab_size=9.4,
            sep_size=11, gap=22, max_w=w - 24)
        cv.text(x + w / 2, y0 + 380, st, size=fit(cv, st, w - 40, 10.4),
                color=INK)

    th = textbox(cv, 70, y0 + 470, W - 140,
                 ["トラネキサム酸は、出血と再開胸を減らした。",
                  "死亡や血栓性合併症は増えなかった。",
                  "一方で、術後けいれんは 0.1% から 0.7% へ増えた。",
                  "「効く」と「安全」は別の軸である。"
                  "どちらも数字で押さえてから使う。"],
                 10.8, style="amber", title="二つの結果を同時に見る",
                 title_color="#9a6510", pad_y=16)

    msg(cv, y0 + 470 + th + 28,
        "投与量と腎機能によってけいれんのリスクは変わる。施設の基準を確認する",
        fc="#fceeec", ec=RED, tc=RED)
    cv.save(P("r06_txa.png"))
    crop_bottom(P("r06_txa.png"))


# ---------------------------------------------------------------- r07
def r07():
    """粘弾性検査"""
    cv = Canvas(W, 1000)
    cap(cv, 44, "何が足りないのかを、その場で分ける")

    C = [("凝固因子が足りない", BLUE, "#eaf1f8",
          ["凝固開始が遅い", "新鮮凍結血漿・濃縮製剤"]),
         ("フィブリノゲンが足りない", GREEN, "#eaf5ee",
          ["血餅の強さが出ない", "フィブリノゲン製剤・クリオ"]),
         ("血小板が足りない・働かない", ORANGE, "#fdf3e3",
          ["血小板寄与分が低い", "血小板輸血"]),
         ("線溶が亢進している", RED, "#fceeec",
          ["血餅が溶けていく", "線溶抑制薬"])]
    w = (W - 140 - 90) / 4
    for i, (t, col, fc, lines) in enumerate(C):
        card(cv, 70 + (w + 30) * i, 140, w, t, lines, col, fc,
             body_size=10.2, lh=1.8)

    y1 = 420
    cv.box(70, y1, W - 140, 200, fc="#ffffff", ec=NAVY, lw=1.8, radius=10)
    cv.text(W / 2, y1 + 38, "7 つの無作為化比較試験 1,035 例のメタ解析",
            size=12.2, color=NAVY, weight="bold")
    L = [("赤血球輸血", "オッズ比 0.61（95%CI 0.37-0.99、p=0.04）"),
         ("新鮮凍結血漿", "リスク差 0.22（95%CI 0.11-0.33、p<0.0001）")]
    w2 = (W - 200) / 2
    for i, (a, b) in enumerate(L):
        x = 100 + w2 * i
        cv.text(x + w2 / 2, y1 + 92, a, size=11.4, color=INK)
        cv.text(x + w2 / 2, y1 + 144, b, size=fit(cv, b, w2 - 40, 11.0),
                color=GREEN, weight="bold")
    cv.text(W / 2, y1 + 178, "いずれも粘弾性検査に基づく輸血アルゴリズムで減少",
            size=10.0, color=GREY)

    th = textbox(cv, 70, y1 + 230, W - 140,
                 ["粘弾性検査の価値は、「輸血を減らすこと」そのものではない。",
                  "「何が足りないのか」をその場で分けられることにある。",
                  "分けられれば、足りないものだけを補える。",
                  "その結果として、使わずに済む製剤が出てくる。"],
                 10.8, style="navy", title="何のための検査か",
                 title_color=NAVY, pad_y=16)
    cv.save(P("r07_viscoelastic.png"))
    crop_bottom(P("r07_viscoelastic.png"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for fn in (r01, r02, r03, r04, r05, r06, r07):
        fn()
        print("ok", fn.__name__)
