# -*- coding: utf-8 -*-
"""㉜ 図版（図1-1 〜 図24-1）"""
from fig32common import (W, Canvas, Panel, LH, head, path, textbox,
                         NAVY, INK, GREY, RED, BLUE, GREEN, ORANGE, PURPLE,
                         C_NOTE)


def f01():
    cv = Canvas(W, 1220)
    y = head(cv, "図1-1　脳と脊髄は、守り方の理屈が違う",
             "同じ大血管手術でも、この二つは別の設計になる。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "機序：塞栓と低灌流",
        "時間：循環停止時間が直接効く",
        "手段：低体温、選択的順行性脳灌流",
        "監視：NIRS、脳波、体温",
        "発症：覚醒時に判明することが多い",
        "可逆性：限定的",
    ], 13.5, style="blue", title="脳（弓部手術）", title_size=17, min_h=320)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "機序：分節動脈の喪失と再灌流障害",
        "時間：遮断時間＋術後数日の灌流",
        "手段：脊髄ドレナージ、灌流圧、段階的手術",
        "監視：MEP・SSEP、髄液圧、下肢運動",
        "発症：遅発性がある（数時間〜数週間）",
        "可逆性：灌流圧の是正で改善しうる",
    ], 13.5, style="green", title="脊髄（下行・胸腹部手術）", title_size=17,
        min_h=320)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "脳梗塞は起きてしまえば手が限られる",
        "脊髄虚血は遅れて起こり、しかも介入で戻ることがある",
        "だから脊髄については、手術が終わったあとの数日間こそが勝負になる",
    ], 14, style="navy", title="最後の二行がいちばん効く", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "FET（弓部再建＋下行ステントグラフト）では、この二つが同じ症例に同居する",
    ], 14.5, style="amber", min_h=110)
    cv.save(path("f01_two_systems.png"))


def f02():
    cv = Canvas(W, 1180)
    y = head(cv, "図2-1　脳を守る三つの方法と、体温の関係",
             "低体温は「止めていられる時間」を延ばし、脳灌流は時間の制約そのものを外す。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 循環停止のみ", "amber", ["深く冷やして代謝を下げる",
                                     "止めていられる時間には限りがある",
                                     "冷却・復温に時間がかかる"]),
        ("② 順行性脳灌流", "green", ["腕頭・左総頸から生理的な向きに送る",
                                     "停止時間の制約が実質外れる",
                                     "カニューレ位置のずれに注意"]),
        ("③ 逆行性脳灌流", "blue", ["上大静脈から逆向きに送る",
                                    "塞栓の洗い出しを期待",
                                    "毛細血管レベルの灌流量は議論がある"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13, style=st,
                          title=ttl, title_size=15.5, min_h=250))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "深く冷やす → 耐えられる停止時間は延びる／冷却・復温の時間、凝固障害、CPB 時間が増える",
        "脳へ血を送る → 停止時間の制約が外れる／カニュレーションと灌流管理が必要になる",
    ], 14, style="navy", title="得るものと失うもの", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "現在の主流は「中等度低体温＋順行性脳灌流」",
        "ただし比較研究は観察研究が中心で、「何度が正解」という単一の答えはない",
    ], 14, style="amber", min_h=120)
    cv.save(path("f02_brain_flow.png"))


def f03():
    cv = Canvas(W, 1240)
    y = head(cv, "図3-1　側副血行網という考え方",
             "脊髄は一本の動脈ではなく、網から灌流されている。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "Adamkiewicz 動脈という一本の大動脈が",
        "下部脊髄を養っている",
        "→ それを失えば対麻痺になる",
        "",
        "図にしやすく、因果も直観に合う",
        "しかし臨床の観察と合わなかった",
    ], 13.5, style="grey", title="古い理解（単一血管説）", title_size=16,
        min_h=300)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "分節動脈（肋間・腰動脈）",
        "傍脊柱筋の中の豊富な吻合",
        "椎骨動脈・鎖骨下動脈系",
        "内腸骨動脈系",
        "→ これらがつながった網から灌流される",
        "→ 網が育てば分節動脈の喪失を代償できる",
    ], 13.5, style="green", title="現在の理解（側副血行網）", title_size=16,
        min_h=300)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "① 分節動脈をすべて再建しなくてもよい可能性がある",
        "② 左鎖骨下動脈・内腸骨動脈の温存と再建が重要になる",
        "③ 網が育つ時間を稼ぐ「段階的手術」が戦略として成り立つ",
    ], 14, style="navy", title="見方が変わると、やることが変わる", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "ただし網は保険であって免除証ではない",
        "遠位大動脈灌流下でも、分節動脈が閉塞していれば脊髄灌流は低下しうる",
    ], 14, style="red", min_h=120)
    cv.save(path("f03_collateral_network.png"))


def f04():
    cv = Canvas(W, 1180)
    y = head(cv, "図4-1　脊髄灌流圧の式と、二つの手",
             "治療の手は、分子を上げるか分母側を下げるかの二つしかない。")
    h0 = textbox(cv, 56 + 200, y, W - 112 - 400, [
        "SCPP ＝ MAP − CSFP",
        "脊髄灌流圧 ＝ 平均動脈圧 − 脳脊髄液圧",
    ], 18, style="navy", min_h=180)
    y2 = y + h0 + 50
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y2, bw, [
        "昇圧薬、輸液、心拍出量の改善",
        "術中・術後の低血圧を避ける",
        "麻痺発症時には目標を上げる",
    ], 14, style="green", title="血圧を上げる（分子）", title_size=16, min_h=230)
    h2 = textbox(cv, 56 + bw + 60, y2, bw, [
        "脊髄ドレナージで髄液を抜く",
        "虚血と浮腫で上がった髄液圧を下げる",
        "抜きすぎれば頭蓋内出血を招く",
    ], 14, style="blue", title="髄液圧を下げる（分母側）", title_size=16,
        min_h=230)
    y3 = y2 + max(h1, h2) + 50
    textbox(cv, 56, y3, W - 112, [
        "虚血 → 浮腫 → 髄液圧の上昇 → さらに灌流が落ちる",
        "この悪循環を断つのが、脊髄ドレナージの理屈である",
    ], 14, style="amber", title="断ちたいのはこの悪循環", title_size=15)
    cv.save(path("f04_scpp.png"))


def f05():
    cv = Canvas(W, 1240)
    y = head(cv, "図5-1　脊髄虚血のリスク因子",
             "開胸手術とステントグラフト治療で、顔ぶれが違う。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("共通", "grey", ["腎機能障害", "心房細動", "術中・術後の低血圧",
                          "重度の動脈硬化", "胸部／腹部大動脈瘤の手術歴"]),
        ("開胸手術で特に", "blue", ["緊急手術（解離・破裂）", "長時間の大動脈遮断",
                                   "Crawford I・II 型", "鎖骨下・腹腔・上腸間膜動脈の狭窄",
                                   "高齢、糖尿病、脳梗塞の既往", "術後出血"]),
        ("ステントグラフトで特に", "amber",
         ["鎖骨下・腹腔・内腸骨動脈の塞栓", "鎖骨下・内腸骨動脈のカバー",
          "内臓・下半身の長時間虚血", "胸部から腹部に及ぶ広範囲留置",
          "大口径シースの長時間挿入", "外腸骨動脈損傷"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5, style=st,
                          title=ttl, title_size=15.5, min_h=300))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "血管内治療で効いてくるのは「側副血行路がどこで断たれるか」である",
        "左鎖骨下動脈と内腸骨動脈は、網への主要な流入路にあたる",
    ], 14, style="navy", title="血管内治療で見るべき一点", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "歴史的には胸部大動脈瘤手術後の脊髄虚血は 29％ とされたが、現在は 10〜11％ 程度",
        "「開胸だから高い、ステントだから低い」という単純な図式は成り立たない",
    ], 14, style="grey", min_h=120)
    cv.save(path("f05_risk.png"))


def f06():
    cv = Canvas(W, 1140)
    y = head(cv, "図6-1　冷やす深さと、得るもの・失うもの",
             "脳灌流を併用できるなら、深く冷やす必要は小さくなる。")
    x = 330
    w = W - x - 160
    p = Panel(cv, x, y, w, 300, "", color=INK)
    cv.text(x - 14, y + 150, "許容できる\n循環停止時間", size=12.5, color=INK,
            ha="right", va="center", weight="bold", linespacing=1.4)
    p.plot([(0, .16), (.35, .40), (.7, .70), (1.0, .88)], color=BLUE, lw=3.0)
    p.plot([(0, .24), (.35, .30), (.7, .36), (1.0, .42)], color=RED, lw=3.0,
           ls=(0, (6, 4)))
    p.note(.32, .62, "許容時間（青）", color=BLUE, size=12.5)
    p.note(.70, .20, "冷却・復温の時間、凝固障害（赤）", color=RED, size=12.5)
    cv.text(p.px(.5), p.y + p.h + 34, "→　冷やす深さ（深くなる方向）", size=13,
            color=GREY)

    y2 = y + 300 + 74
    bw = (W - 112 - 40) / 2
    h1 = textbox(cv, 56, y2, bw, [
        "早期死亡のリスクが低かったという報告",
        "順行性脳灌流との併用で安全性が示されている",
        "冷却・復温の時間が短い",
    ], 13.5, style="green", title="中等度低体温＋順行性脳灌流", title_size=15.5,
        min_h=210)
    h2 = textbox(cv, 56 + bw + 40, y2, bw, [
        "測定部位で温度は違う（鼻咽頭・膀胱・直腸）",
        "復温は急がない。高体温を作らない",
        "alpha-stat／pH-stat の方針を決めておく",
    ], 13.5, style="blue", title="麻酔側が関わる実務", title_size=15.5,
        min_h=210)
    cv.save(path("f06_hypothermia.png"))


def f08():
    cv = Canvas(W, 1180)
    y = head(cv, "図9-1　脳梗塞に至る二つの経路",
             "時間の管理は、右側にしか効かない。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "上行・弓部の粥腫",
        "遮断・脱血・送血の操作",
        "空気",
        "",
        "→ 効くのは送血部位の選択、操作の回数、",
        "　 術前の粥腫評価",
    ], 13.5, style="red", title="塞栓", title_size=17, min_h=300)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "循環停止時間",
        "灌流圧・流量の不足",
        "カニューレ位置のずれによる片側灌流",
        "",
        "→ 効くのは時間の管理と脳灌流の方法",
        "",
    ], 13.5, style="blue", title="低灌流", title_size=17, min_h=300)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "送血開始直後の NIRS 左右差 ── 送血部位の問題を示唆する",
        "解離腔への送血 ── 圧の異常と NIRS の低下が同時に起こりうる",
        "脱血不良と静脈うっ血 ── 脳静脈圧の上昇も灌流を妨げる",
        "術野の空気 ── 弓部開放時の操作と脱気の手順を共有しておく",
    ], 13.5, style="navy", title="麻酔科が気づける場面", title_size=15)
    cv.save(path("f08_embolism.png"))


def f09():
    cv = Canvas(W, 1140)
    y = head(cv, "図10-1　脳のモニタリングが見ているもの",
             "どれも脳全体を見てはいない。")
    bw = (W - 112 - 3 * 24) / 4
    cols = (
        ("NIRS", "green", ["前額部の局所酸素飽和度", "左右差と急な低下が手がかり",
                           "転帰改善の証拠は限定的"]),
        ("脳波", "blue", ["皮質の電気活動", "冷却の深さの目安にも使う",
                          "麻酔薬の影響を受ける"]),
        ("経頭蓋ドプラ", "purple", ["血流速度と塞栓シグナル", "描出できないことがある"]),
        ("体温", "amber", ["代謝の代理指標", "測定部位で値が違う",
                           "復温時の高体温に注意"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 24), y, bw, lines, 12.5, style=st,
                          title=ttl, title_size=15.5, min_h=230))
    y2 = y + max(hs) + 50
    textbox(cv, 56, y2, W - 112, [
        "① まず装置と貼付部位を疑う（プローブ、接触、光の漏れ）",
        "② 次に送血・灌流の物理的な問題を疑う（カニューレ位置、圧、流量）",
        "③ そのうえで全身の要因を見る（血圧、CO₂、ヘモグロビン、体温）",
        "目的は「数値を戻す」ことではなく「原因を見つける」こと",
    ], 14, style="navy", title="値が動いたときの順番", title_size=15)
    cv.save(path("f09_brain_monitor.png"))


def f11():
    cv = Canvas(W, 1180)
    y = head(cv, "図12-1　脊髄ドレナージのエビデンス",
             "推奨は、一本の無作為化試験と多数の観察研究の上に立っている。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("Coselli 2002", "green", ["Crawford I・II 型 145 例",
                                   "ドレナージの有無を無作為化",
                                   "ドレナージ群で対麻痺が有意に少ない",
                                   "単施設・特定の時代の研究"]),
        ("コクラン 2012", "amber", ["無作為化試験の数が少ない",
                                    "手技・併用手段・時代が揃わない",
                                    "予防効果を支持する証拠は限られる"]),
        ("ガイドライン", "blue", ["高リスクの胸腹部手術で",
                                  "脊髄保護戦略の一部として位置づけ",
                                  "国内ガイドラインも同様の枠組み"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13, style=st,
                          title=ttl, title_size=16, min_h=270))
    y2 = y + max(hs) + 50
    textbox(cv, 56, y2, W - 112, [
        "「置けば麻痺しない」ではない",
        "「高リスク症例で、灌流圧の維持・分節動脈の扱い・モニタリングと組み合わせて用いる」",
        "そして、この手技自体に固有の合併症がある（第14章）",
    ], 14, style="navy", title="ここは正確に言う", title_size=15)
    cv.save(path("f11_csfd_evidence.png"))


def f12():
    cv = Canvas(W, 1240)
    y = head(cv, "図13-1　脊髄ドレナージ管理の考え方",
             "設定圧を基準に、排液量で高さを調整する。性状の変化は警告である。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("多く出るとき", "amber", ["2 時間で 30 mL を超える",
                                   "→ 高さを 2 cmH₂O 上げる",
                                   "過剰排液は頭蓋内出血を招く"]),
        ("出ないとき", "blue", ["2 時間で 0 mL",
                                "→ 高さを 2 cmH₂O 下げる",
                                "最低 6 cmH₂O まで"]),
        ("性状が変わったとき", "red", ["透明 → 血性",
                                       "急激な増量を伴えばとくに危険",
                                       "→ 排液を中止し、早期に画像へ"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13, style=st,
                          title=ttl, title_size=15.5, min_h=250))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "ゼロ点は右房の高さ。設定圧 12 cmH₂O で開始（一施設の例）",
        "脊髄灌流圧の目標は 60 mmHg 以上、髄液圧は 12 cmH₂O 以下",
        "予防的留置は術後 72 時間を原則とする",
    ], 14, style="navy", title="骨格となる数値（付録B）", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "使用しないとき・移動時はすべてのクレンメをクランプする",
        "ゼロ点がどこかを、交代する人と必ず共有する",
        "接続部は三方活栓を使い、ガーゼでくるむ",
    ], 14, style="red", title="移動と交代で事故が起きる", title_size=15)
    cv.save(path("f12_csfd_practice.png"))


def f13():
    cv = Canvas(W, 1180)
    y = head(cv, "図15-1　MEP が低下したときに動かす三つのつまみ",
             "麻酔科が握っているのは、前の二つである。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 血圧を上げる", "green", ["SCPP の分子を上げる",
                                     "昇圧薬・輸液・心拍出量"]),
        ("② 髄液圧を下げる", "blue", ["ドレナージで排液",
                                      "設定圧を下げる"]),
        ("③ 血流を戻す", "amber", ["分節動脈の再建",
                                   "遠位灌流の追加・手技の変更",
                                   "→ 術者の判断"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13.5, style=st,
                          title=ttl, title_size=15.5, min_h=220))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "筋弛緩薬を使わない、あるいは厳密に管理する ── 記録できなくなる",
        "吸入麻酔薬は振幅を抑制する。静脈麻酔主体にするのが一般的",
        "低体温・低血圧・貧血も振幅を下げる ── 虚血と紛らわしい",
    ], 14, style="navy", title="MEP を取る日の麻酔", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "「変化した」と言われたら、まず麻酔要因を除外してから虚血を考える",
        "K930 脊髄誘発電位測定等加算 3,630点（大動脈瘤手術は対象に含まれる）",
    ], 14, style="amber", min_h=120)
    cv.save(path("f13_mep.png"))


def f14():
    cv = Canvas(W, 1160)
    y = head(cv, "図17-1　段階的手術とプレコンディショニング",
             "分節動脈を一度にすべて失うと、網が間に合わない。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "広範囲の分節動脈を一度に失う",
        "側副血行網が発達する時間がない",
        "→ 脊髄灌流が急に落ちる",
    ], 14, style="red", title="一期的に行う場合", title_size=16, min_h=240)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "先に一部の分節動脈を閉塞させる",
        "網が育つ時間を置く",
        "→ 本体の手術で代償が働く",
    ], 14, style="green", title="段階化する場合", title_size=16, min_h=240)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "MISACE：分節動脈をコイル塞栓してプレコンディショニングする低侵襲の手法",
        "血管内治療の前に虚血プレコンディショニングを行った臨床経験も報告されている",
        "PAPA-ARTiS 試験として多施設無作為化試験が進行中",
    ], 14, style="navy", title="実際の手段", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "脊髄虚血は「起きれば重大だが頻度は高くない」── 予防を試験にかけるのが難しい領域である",
    ], 14, style="grey", min_h=110)
    cv.save(path("f14_staged_misace.png"))


def f15():
    cv = Canvas(W, 1180)
    y = head(cv, "図18-1　血管内治療における脊髄保護のバンドル",
             "どれか一つではなく、束で効かせる。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("術前", "blue", ["段階的な留置の計画", "左鎖骨下動脈の再建を決める",
                          "内腸骨動脈の温存を検討", "リスクの層別化"]),
        ("術中", "green", ["一時的な瘤嚢灌流（TASP）", "補助的な灌流枝",
                           "大口径シースの留置時間を短く", "低血圧を作らない"]),
        ("術後", "amber", ["灌流圧の目標を決めて維持", "脊髄ドレナージの管理",
                           "下肢運動を各勤務帯で評価", "麻痺時の初動を決めておく"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13, style=st,
                          title=ttl, title_size=16, min_h=270))
    y2 = y + max(hs) + 50
    textbox(cv, 56, y2, W - 112, [
        "分枝型・開窓型ステントグラフトにバンドル化したプロトコルを導入した報告で、",
        "脊髄虚血のリスクが有意に低下した。近年の報告でも同じ方向が示されている",
        "効いているのは個々の手技ではなく、漏れなく実行する仕組みである",
    ], 14, style="navy", title="バンドルが成果を出した", title_size=15)
    cv.save(path("f15_endo_bundle.png"))


def f16():
    cv = Canvas(W, 1460)
    y = head(cv, "図19-1　麻痺に気づいたときの順番",
             "時間が結果を分ける。灌流圧が最優先。")
    steps = (
        ("① 灌流圧を上げる", "red", "平均動脈圧を上げる／髄液圧を下げる（ドレーンがあれば排液）"),
        ("② ドレーンを確認する", "amber", "抜去後の発症なら再留置を検討する"),
        ("③ 全身を整える", "blue", "ヘモグロビン、心拍出量、酸素化、CO₂"),
        ("④ 原因を検索する", "green", "画像評価。外科的に戻せる血流がないかを術者と確認"),
        ("⑤ 薬物を考える", "grey", "ナロキソン・ステロイドは限定的な場面での考慮にとどまる"),
    )
    yy = y
    for i, (ttl, st, memo) in enumerate(steps):
        h = textbox(cv, 56 + i * 34, yy, W - 112 - i * 68, [memo], 13.5,
                    style=st, title=ttl, title_size=15, min_h=120)
        yy += h + 16
    y2 = yy + 34
    textbox(cv, 56, y2, W - 112, [
        "遅発性対麻痺は術後 21 時間（中央値）、最長 27 日の報告がある",
        "覚醒したときに足が動いたことは、安全宣言ではない",
    ], 14, style="navy", title="遅れて起こる", title_size=15)
    cv.save(path("f16_delayed_paraplegia.png"))


def f17():
    cv = Canvas(W, 1120)
    y = head(cv, "図20-1　神経保護の土台",
             "どれかが崩れていれば、ドレナージも脳灌流も本来の効果を出せない。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("灌流圧", "blue", ["脊髄：SCPP ＝ MAP − CSFP",
                            "脳：MAP − 頭蓋内圧／静脈圧",
                            "術中も術後も低血圧を避ける"]),
        ("酸素運搬", "green", ["貧血の是正", "酸素飽和度の維持",
                               "低心拍出量を避ける"]),
        ("代謝", "amber", ["体温 ── 復温時の高体温を作らない",
                           "血糖の管理", "低二酸化炭素血症を避ける"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13.5, style=st,
                          title=ttl, title_size=16, min_h=250))
    y2 = y + max(hs) + 50
    textbox(cv, 56, y2, W - 112, [
        "この領域には確立した「効く薬」がない",
        "その分、手技と全身管理の比重が大きい",
    ], 14.5, style="navy", min_h=130)
    cv.save(path("f17_foundation.png"))


def f18():
    cv = Canvas(W, 1180)
    y = head(cv, "図24-1　プロトコルに書くべきこと",
             "このどれかが欠けると、現場で止まる。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("誰に・何を", "blue", ["適応（術式・範囲）", "禁忌と休薬",
                                "MEP を取る症例"]),
        ("どこまで・どう", "green", ["SCPP と CSFP の目標", "排液管理の幅",
                                     "留置期間と抜去基準"]),
        ("誰が・何を残す", "amber", ["担当と連絡先", "MEP 変化時の初動",
                                     "記録する項目と時刻"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13.5, style=st,
                          title=ttl, title_size=16, min_h=250))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "脊髄ドレナージの有無、ゼロ点の高さ、設定圧",
        "術中の排液量と性状、MEP の推移",
        "最後に下肢運動を確認した時刻と所見",
        "血圧の目標と、抜去の予定日時",
    ], 13.5, style="navy", title="手術室から ICU へ伝えること", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "事故が起きるのは手技の最中ではなく、移動と交代のときである",
    ], 14.5, style="red", min_h=110)
    cv.save(path("f18_protocol.png"))


if __name__ == "__main__":
    for fn in (f01, f02, f03, f04, f05, f06, f08, f09, f11, f12, f13, f14,
               f15, f16, f17, f18):
        fn()
        print("ok:", fn.__name__)
