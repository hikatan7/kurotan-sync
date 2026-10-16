# -*- coding: utf-8 -*-
"""心臓手術後の心停止　要点 10 枚スライド（pptxlib の積み上げカーソルで組む）"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pptxlib
from pptxlib import Deck, L, CW, BODY_TOP, BODY_BOT, text_w, text_h

OUT = os.path.join(HERE, "..", "心臓手術後の心停止_要点10枚.pptx")
FIG = os.path.join(HERE, "..", "図版")
deck = Deck("心臓手術後の心停止（CALS）",
            "ICLS インストラクター用資料｜作成：麻酔科　玉里順子｜2026 年 9 月 27 日")
LOG = []


def check(sl, no):
    LOG.append((no, round(sl._cur, 2), round(sl._bfloor, 2)))


# ================================================================== 1
_t = deck.title_slide(
    series="ICLS インストラクター用資料", no="CALS",
    title="心臓手術後の心停止",
    sub="ICLS と何が違うか ── 最初の 1 分と 5 分",
    lead="術直後の ICU の心停止は、ICLS から意図的に外れる数少ない場面。"
         "圧迫をやめる手順ではなく、優先順位を入れ替える手順として教える。",
    cards=[("最初の 1 分", "VF は 3 連続ショック\n徐脈はペーシング", "red"),
           ("5 分・10 日", "5 分で再開胸\n術後 10 日まで", "purple"),
           ("アドレナリン", "1 mg を定型で\n入れない", "orange")],
    toc=[("1–3", "なぜ別扱いか／ガイドラインの現在地"),
         ("4–6", "最初の 1 分／3 回連続ショックの根拠／薬"),
         ("7–8", "胸骨圧迫と再開胸／6 つの役割と訓練"),
         ("9–10", "ICLS との対照表／よくある誤解と当院で明日から")],
    note="AHA 2025・ERC 2025・STS 2017・EACTS 2009 と国内報告にもとづく。詳細版・専攻医用テキストに出典つきで記載。",
    badge="ICLS インストラクター　10 枚",
    toc_title="10 枚の構成")




# ---- 用語欄：略語・専門用語を日本語で短く説明する（出典行の上に先に確保する） ----
GLOSS = {
 1: "CALS：心臓手術後の心停止に対する蘇生手順／ICLS：日本救急医学会の院内心停止対応コース／VF：心室細動／AHA：米国心臓協会／ERC：欧州蘇生協議会／STS：米国胸部外科学会／EACTS：欧州心臓胸部外科学会",
 2: "VF：心室細動／タンポナーデ：心嚢内の血液や凝血で心臓が圧迫され、広がれなくなった状態／心係数：体表面積あたりの心拍出量／冠灌流圧：冠動脈に血液を送り込む圧／ERC：欧州蘇生協議会",
 3: "「1・B-NR」など：推奨の強さ（1 行うべき・2a 妥当）と証拠の質（B-NR 非無作為化研究・C-EO 専門家の意見）／VF：心室細動／ECLS：ECMO などの体外式生命維持／STS：米国胸部外科学会",
 4: "VF：心室細動／無脈性 VT：脈の触れない心室頻拍／PEA：無脈性電気活動（波形はあるが脈がない）／DDD：心房と心室の両方を感知・ペーシングする設定／FiO2：吸入酸素濃度／PEEP：呼気終末陽圧／SpO2：経皮的酸素飽和度／EtCO2：呼気終末二酸化炭素分圧",
 5: "ACLS：二次救命処置／VF：心室細動／閾値試験：除細動が効く最小エネルギーを確かめる試験／ICU：集中治療室",
 6: "EACTS：欧州心臓胸部外科学会／STS：米国胸部外科学会／Class III harm：有害なので行わない／μg：マイクログラム（1 mg の 1000 分の 1）／VF：心室細動",
 7: "mmHg：血圧の単位（ここでは動脈圧の収縮期）／P：偶然でこの差が出る確率（小さいほど偶然では説明しにくい）／ICU：集中治療室",
 8: "FiO2：吸入酸素濃度／PEEP：呼気終末陽圧／内部パドル：開胸した心臓に直接当てる除細動の電極／ICU コーディネーター：人と物を集める調整役",
 9: "ALS：二次救命処置／DDD：心房と心室の両方を感知・ペーシングする設定／ECPR：ECMO を使う体外循環式心肺蘇生／IABP：大動脈内バルーンパンピング（圧トリガー 1：1＝動脈圧に合わせて毎拍補助）",
 10: "MICS：低侵襲心臓手術（胸骨を全部は切らない小切開の手術）／PEA：無脈性電気活動／VF：心室細動",
}
GLOSS_SIZE = 10.5


def _gloss_runs(no, size):
    runs = [("用語　", {"size": size, "bold": True, "color": pptxlib.RED})]
    for i, item in enumerate(GLOSS[no].split("／")):
        k, _, v = item.partition("：")
        if i:
            runs.append(("　", {"size": size}))
        runs.append((k, {"size": size, "bold": True, "color": pptxlib.INK}))
        runs.append(("：" + v, {"size": size, "bold": False, "color": pptxlib.GREY}))
    return runs


def gloss(s, no, x=None, y=None, width=None):
    """本文の下（出典行の上）に用語欄を置き、本文の下端を持ち上げる"""
    x = L if x is None else x
    width = CW if width is None else width
    plain = "用語　" + GLOSS[no].replace("／", "　")
    h = text_h(plain, width - 0.30, GLOSS_SIZE, False) + 0.12
    if y is None:
        y = s._bfloor - h
        s._bfloor = y - 0.10
    s.box(x, y, width, h, fill=pptxlib.RGBColor(0xF3, 0xF0, 0xE8))
    s.text(x + 0.15, y + 0.06, width - 0.30, h - 0.08, _gloss_runs(no, GLOSS_SIZE))
    return y + h

def set_sizes(z):
    pptxlib.BODY_BOLD = True
    pptxlib.CARD_BODY = z
    pptxlib.CARD_HEAD = z + 2.5
    pptxlib.STRIP_SIZE = z
    pptxlib.PANEL_TITLE = min(z + 1.0, 15.0)
    pptxlib.SRC_SIZE = 10.0
    pptxlib.KEY_SIZE = 16.0


def fits(sl):
    return sl._cur <= sl._bfloor + 0.01


def key_fits(lead, strong, tail=""):
    w = text_w("KEY MESSAGE：　", 10.0, True) + text_w(lead + strong + tail, pptxlib.KEY_SIZE, True)
    return w <= (CW - 0.50) * 72.0


def fit_and_draw(fn, no):
    """大きいサイズから試し、本文が下端を越えない最大のサイズで描く"""
    z = 18.0
    while z >= 9.0:
        set_sizes(z)
        tmp = Deck("x", "x")
        tmp.n = no - 1
        sl = fn(tmp, z)
        if fits(sl):
            break
        z -= 0.5
    set_sizes(z)
    sl = fn(deck, z)
    LOG.append((no, z, round(sl._cur, 2), round(sl._bfloor, 2)))
    return sl

def slide2(dk, z):
    s = dk.slide("WHY", "なぜ", "別の手順なのか")
    gloss(s, 2)
    s.cards([("原因が偏っている",
              "VF（虚血・ペースメーカ不具合）、タンポナーデ、出血。"
              "いずれも数分で手を打てる原因である（AHA 2025）。", "blue"),
             ("圧迫が効きにくい",
              "充満していない心臓は押しても拍出しない。術直後の胸骨・縫合線・グラフトを傷つけうる。", "red"),
             ("道具がそろっている",
              "波形モニタ、心外膜ペーシングワイヤ、数分で開ける胸骨。"
              "内胸マッサージは心係数・冠灌流圧が高い。", "green")],
            bottom=True)
    s.panel_grid("頻度と転帰 ── 分母によって 1% にも 5% にもなる",
                 [1.3, 2.2, 1.3, 2.2],
                 [["ERC 2025", "ガイドラインの記載", "2〜5%", "生存およそ 50%"],
                  ["Anthi 1998", "心臓手術 3,982 例・術後 24 時間", "0.7%", "退院 79%"],
                  ["LaPar 2014", "米国 17 施設 79,582 例", "5.2%", "救命失敗 60%（施設間 50〜83%）"],
                  ["高木 2023", "秋田大学 開心術 550 例", "1.1%", "6 例で CALS を発動"]],
                 colors=["navy", "blue", "blue", "green"], size=z, fill=True)
    s.source("ERC 2025、AHA 2025、Anthi 1998、LaPar 2014、高木 2023")
    s.keymsg("心停止の頻度より、", "起きたあとに救命できるか", "が施設で大きく違う。")
    return s

def slide3(dk, z):
    s = dk.slide("GUIDELINES", "AHA 2025 は", "成人に 6 つの勧告を置いた")
    gloss(s, 3)
    s.strip("「5 分以内」とアドレナリンの扱いは、AHA の勧告文にはない。ERC 2025 と STS 2017 で補う",
            key="orange", bottom=True)
    s.panel_grid("AHA 2025 Part 10 ── 心臓手術後の心停止（成人）",
                 [1.3, 7.0],
                 [["1・B-NR", "緊急再開胸がすぐにできなければ、胸骨圧迫を行う"],
                  ["1・C-EO", "VF を目撃したら、ただちに 3 回連続の除細動。1 分以内に成功しなければ心肺蘇生"],
                  ["1・C-EO", "心静止・徐脈で一時ペーシングワイヤがあれば、ただちにペーシング。1 分で成功しなければ心肺蘇生"],
                  ["2a・B-NR", "術後早期は、人員と設備の整った ICU で迅速に再開胸するのは妥当"],
                  ["2a・B-NR", "迅速に開胸できる術後早期には、内胸心マッサージが有用でありうる"],
                  ["2a・C-EO", "標準の蘇生に反応しなければ、ECLS は有効でありうる"]],
                 colors=["red", "red", "red", "purple", "purple", "green"], size=z, fill=True)
    s.source("AHA 2025 Part 10（Circulation 2025;152(16 Suppl 2):S578-S672）")
    s.keymsg("核となる 2 つ（3 回連続ショック・ペーシング先行）は ", "Class 1", "。")
    return s

def slide4(dk, z):
    s = dk.slide("THE FIRST MINUTE", "最初の 1 分は", "リズムで三つに分かれる")
    gloss(s, 4)
    s.strip("同時に：FiO2 100%・PEEP を外す／蘇生に不要な持続投与を止める／経食道心エコーでタンポナーデを探す",
            key="navy", bottom=True)
    s.cards([("VF／無脈性 VT",
              "除細動器がすぐ使えるなら、胸骨圧迫より先に 3 回連続でショック。1 分以内に終える。"
              "合間に圧迫を挟まない。", "red"),
             ("心静止・高度徐脈",
              "心外膜ワイヤがあれば、圧迫より先にペーシング。DDD・80〜100 回/分・最大出力。"
              "1 分で戻らなければ圧迫。", "blue"),
             ("PEA",
              "待たずに圧迫。ペーシング中なら止めて隠れた VF を確かめる。"
              "タンポナーデ・出血・緊張性気胸を探す。", "purple")])
    s.gap(0.18)
    s.panel_grid("認識の段階でやること",
                 [1.6, 6.5],
                 [["波形で見る", "脈を探さない。動脈圧・中心静脈圧・SpO2 の波形、EtCO2、心電図で判断する"],
                  ["3 つ同時に", "大声で応援要請／6 つの役割を宣言／再開胸セットを開く"]],
                 colors=["navy", "navy"], size=z, fill=True)
    s.source("AHA 2025、ERC 2025")
    s.keymsg("1 分は", "除細動・ペーシングのための時間", "。PEA では待たない。")
    return s

def slide5(dk, z):
    s = dk.slide("THREE SHOCKS", "なぜ", "3 回で区切るのか")
    gloss(s, 5)
    s.cards([("4 回目より再開胸",
              "成功率が下がっていく以上、4 回目に賭けるより再開胸へ進むほうが得が大きい。", "red"),
             ("標準 ACLS からの逸脱",
              "AHA 自身が「逸脱」と書いたうえで、厳重な監視下と圧迫・再開胸の危険から正当化している。", "navy"),
             ("教えるときの一言",
              "統合した 15 研究に、心臓手術後の ICU 患者を対象にしたものは一つもない。", "orange")],
            bottom=True)
    s.panel_grid("連続ショックの成功率（15 研究の統合値、Richardson 2007）",
                 [1.5, 2.1, 4.5],
                 [["1 回目", "78%", "除細動の閾値試験では初回成功が 90% 超の研究が多い"],
                  ["2 回目", "35%", "1 回目で止まらない VF は、2 回目で止まる見込みが半分以下"],
                  ["3 回目", "14%", "ここで区切る。止まらなければ圧迫を始めて再開胸へ"],
                  ["4 回目", "10% 未満（推定）", "データはほとんどない"]],
                 colors=["red", "red", "red", "navy"], size=z, fill=True)
    s.source("Richardson 2007（Interact Cardiovasc Thorac Surg）、AHA 2025")
    s.keymsg("3 回は根拠の強さではなく、", "再開胸までの時間を守るための区切り", "である。")
    return s

def slide6(dk, z):
    s = dk.slide("DRUGS", "アドレナリン 1 mg を", "定型で入れない")
    gloss(s, 6)
    s.cards([("なぜ危ないか",
              "タンポナーデや出血を解除して心拍が戻った瞬間に、1 mg が強い高血圧を起こし、縫合線・吻合部から出血する。", "red"),
             ("抗不整脈薬",
              "3 回のショックで止まらない VF に、アミオダロン 300 mg またはリドカイン 100 mg。", "blue"),
             ("アトロピン",
              "EACTS 2009 は 3 mg を残していたが、STS 2017 で定型から外れた。徐脈にはペーシング。", "green")],
            bottom=True)
    s.panel_grid("文書ごとのアドレナリンの扱い",
                 [1.5, 6.8],
                 [["EACTS 2009", "ルーチンには投与しない"],
                  ["STS 2017", "経験ある臨床医の指示がない限り投与しない（Class III harm）。バソプレシンも同じ"],
                  ["ERC 2025", "術直後の 1 mg は議論がある。心停止前後では 50〜100 μg を考慮してよい（専門家の合意）"],
                  ["AHA 2025", "心臓手術後の節にアドレナリンの勧告はない"]],
                 colors=["navy", "orange", "blue", "navy"], size=z, fill=True)
    s.source("EACTS 2009、STS 2017、ERC 2025、AHA 2025")
    s.keymsg("禁じられているのは「3〜5 分ごとに 1 mg」を", "手順に組み込むこと", "。")
    return s

def slide7(dk, z):
    s = dk.slide("COMPRESSIONS & RESTERNOTOMY", "圧迫はやめない。", "5 分で胸を開ける")
    gloss(s, 7)
    s.cards([("1 分", "待てるのは除細動・ペーシングの間だけ。再開胸がすぐできなければ圧迫（AHA Class 1）。", "blue"),
             ("60 mmHg", "効果は動脈圧で見る。届かなければタンポナーデか大出血を疑う（ERC 2025）。", "orange"),
             ("5 分・10 日", "戻らなければ 5 分以内に再開胸。術後少なくとも 10 日までは手順に含める。", "purple"),
             ("5 点のセット", "メス・ワイヤカッター・重持針器・開胸器・吸引。別にして点検する。", "green")])
    s.gap(0.18)
    s.panel_grid("時間と場所で生存が分かれる（Mackay 2002、心停止で再開胸した 79 例）",
                 [3.0, 2.4, 1.2],
                 [["10 分以内の再開胸 vs 10 分超", "48%（14/29）vs 12%（6/50）", "P<0.001"],
                  ["ICU での心停止 vs ICU の外", "33%（19/58）vs 5%（1/21）", "P=0.017"],
                  ["病棟でその場で再開胸", "0/12（全員死亡）", "—"]],
                 colors=["purple", "blue", "red"], size=z, fill=True)
    s.source("AHA 2025、ERC 2025、STS 2017、Mackay 2002")
    s.keymsg("ICU の外では開かない。", "ICU か手術室へ運ぶ", "。")
    return s

def slide8(dk, z):
    s = dk.slide("TEAM", "6 つの役割を", "最初に宣言する")
    gloss(s, 8)
    roles = [("1 外胸心マッサージ", "動脈圧で効果を見る。ショック中は待つ", "red"),
             ("2 気道と呼吸", "FiO2 100%、PEEP を外す。気胸を除外", "blue"),
             ("3 除細動・ペーシング", "再開胸では内部パドルを用意", "purple"),
             ("4 チームリーダー", "手を動かさず、手順と人を見る", "navy"),
             ("5 薬剤・ポンプ", "持続投与を止める。アドレナリンは指示時のみ", "orange"),
             ("6 ICU コーディネーター", "人と物を集め、再開胸セットを開く", "green")]
    y = BODY_TOP
    for row in (roles[0:2], roles[2:4], roles[4:6]):
        y = s.cards(row, x=L, y=y, width=7.3, height=0.5, gap=0.12, advance=False) + 0.14
    bot = y - 0.14
    x2 = L + 7.55
    y = BODY_TOP
    for head, body, key in [
            ("訓練で時間は縮む", "3 日間のコース前後で、再開胸・内胸マッサージまで 451 秒 → 228 秒（Dunning 2006）。", "green"),
            ("知識だけでは守れない", "講義形式の訓練でも、1 分以内に 3 回のショックを終えられたのは 43%（Peek 2023）。", "orange"),
            ("訓練している施設は少ない", "国際調査で定期的に訓練しているのは 7%、重要と答えたのは 80%（Adam 2009）。", "blue")]:
        y = s.cards([(head, body, key)], x=x2, y=y, width=CW - 7.55, height=0.5, advance=False) + 0.16
    s._cur = max(bot, y - 0.16)
    s.source("EACTS 2009、STS 2017、Dunning 2006、Peek 2023、Adam 2009")
    s.keymsg("役割を決めないと、", "全員が胸骨の上に集まる", "。")
    return s

def slide9(dk, z):
    s = dk.slide("ICLS vs CALS", "ICLS との違いを", "一枚で示す")
    gloss(s, 9)
    s.panel_grid("項目　／　ICLS（標準の ALS）　／　心臓手術後（CALS）",
                 [1.7, 2.8, 4.3],
                 [["胸骨圧迫の開始", "ただちに", "VF・徐脈は最初の 1 分は除細動・ペーシング優先。PEA はただちに"],
                  ["VF／無脈性 VT", "1 回ショック → 2 分間の圧迫", "3 回連続ショック（1 分以内）"],
                  ["心静止・徐脈", "圧迫＋アドレナリン", "心外膜ペーシングが先（DDD 80〜100・最大出力）"],
                  ["アドレナリン", "1 mg を 3〜5 分ごと", "定型では入れない。指示があれば少量"],
                  ["圧迫の評価", "深さ・テンポ・中断の少なさ", "動脈圧で収縮期 60 mmHg 以上"],
                  ["決定的な治療", "原因検索を続ける", "5 分以内の再開胸・内胸マッサージ"],
                  ["補助循環", "ECPR は限られた場面", "IABP を圧トリガー 1：1 に。人工心肺・ECPR へ"],
                  ["適用範囲", "場所・時期を問わない", "術後の ICU、少なくとも術後 10 日まで"]],
                 colors=["navy"] * 8, size=z, rowh=0.40, fill=True)
    s.source("AHA 2025、ERC 2025、STS 2017")
    s.keymsg("核は三つ ── ", "最初の 1 分・アドレナリン・5 分の再開胸", "。")
    return s

def slide10(dk, z):
    s = dk.slide("TAKE HOME", "よくある誤解と、", "当院で明日からやること")
    gloss(s, 10)
    s.cards([("A4 チャートを見直す",
              "骨格は 2025 年の文書と一致。ペーシング設定・PEA の書き分け・5 分の明記・MICS の扱いを関係部署と検討。", "navy"),
             ("シナリオを足す",
              "ICLS のブースに 15〜20 分。VF 型とタンポナーデ・出血型の 2 本（詳細版 第9章）。", "green"),
             ("セットを点検する",
              "5 点の再開胸セットが、術後患者のいる場所ですぐ出せるか確かめる。", "orange")],
            bottom=True)
    s.panel_grid("受講者がよく間違えること",
                 [3.0, 5.6],
                 [["CALS は胸骨圧迫をしない手順", "再開胸がすぐできなければ圧迫する（AHA Class 1）。PEA は待たない"],
                  ["78%→35%→14% は術後患者の成績", "心臓手術後の ICU 患者を含まない 15 研究の統合値"],
                  ["ペーシング波形があるから心拍はある", "ペーシングを止めて、隠れた VF を確かめる"],
                  ["どこで起きても再開胸すれば助かる", "病棟で開いた 12 例は全員死亡。ICU か手術室へ"]],
                 colors=["red", "red", "red", "red"], size=z, fill=True)
    s.source("AHA 2025、Richardson 2007、ERC 2025、Mackay 2002")
    s.keymsg("CALS は", "優先順位を入れ替える手順", "であって、圧迫をやめる手順ではない。")
    return s


gloss(_t, 1, y=6.70)
fit_and_draw(slide2, 2)
fit_and_draw(slide3, 3)
fit_and_draw(slide4, 4)
fit_and_draw(slide5, 5)
fit_and_draw(slide6, 6)
fit_and_draw(slide7, 7)
fit_and_draw(slide8, 8)
fit_and_draw(slide9, 9)
fit_and_draw(slide10, 10)

deck.save(OUT)
for row in LOG:
    print("slide %d  size=%.1f  cur=%.2f floor=%.2f" % row)
print("saved", os.path.abspath(OUT))
