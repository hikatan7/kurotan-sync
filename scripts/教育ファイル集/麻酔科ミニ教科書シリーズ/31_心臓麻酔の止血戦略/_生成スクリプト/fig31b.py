# -*- coding: utf-8 -*-
"""㉛ 図版 第III部〜第V部（図10-1 〜 図23-1）"""
from fig31common import (W, Canvas, Panel, LH, head, path, legend, decay,
                         textbox, NAVY, INK, GREY, RED, BLUE, GREEN,
                         ORANGE, PURPLE, C_NOTE)


def f09():
    """2026年3月の適応追加と四つの条件"""
    cv = Canvas(W, 1300)
    y = head(cv, "図10-1　2026年3月に加わった適応と、その四つの条件",
             "四つが揃ってはじめて適応内になる。一つでも欠ければ、適応外の投与である。")
    h0 = textbox(cv, 56, y, W - 112, [
        "産科危機的出血、心臓血管外科手術における出血に伴う",
        "後天性低フィブリノゲン血症に対するフィブリノゲンの補充",
    ], 15, style="navy", title="効能・効果（2026年3月23日 一部変更承認）",
        title_size=16)
    y2 = y + h0 + 50
    bw = (W - 112 - 3 * 24) / 4
    conds = (
        ("① 人工心肺", "blue", ["人工心肺を用いた手術に限る",
                                "OPCAB は対象外"]),
        ("② 出血がある", "amber", ["「出血に伴う」低フィブリノゲン血症",
                                   "予防投与は承認されていない"]),
        ("③ 投与直前の測定", "green", ["投与直前の血中フィブリノゲン値を",
                                       "必ず測定する"]),
        ("④ 150 mg/dL 未満", "red", ["後天性低フィブリノゲン血症の定義",
                                     "測定値で確認する"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(conds):
        hs.append(textbox(cv, 56 + i * (bw + 24), y2, bw, lines, 13, style=st,
                          title=ttl, title_size=15.5, min_h=200))
    y3 = y2 + max(hs) + 50
    h3 = textbox(cv, 56, y3, W - 112, [
        "1回 3 g を静脈内投与。改善しなければ同量を追加投与する",
        "追加投与の適否は、フィブリノゲン以外の因子の関与も考慮して慎重に判断し、"
        "漫然と投与しない",
    ], 14, style="grey", title="用法・用量", title_size=15)
    y4 = y3 + h3 + 44
    textbox(cv, 56, y4, W - 112, [
        "「出血傾向の改善」ではなく「フィブリノゲンの補充」という言葉が選ばれている",
        "検討会議は、前者は予防的投与を想起させるため適切でないと明記した",
        "つまりこの薬は、予防的に入れる薬としては承認されていない",
    ], 14, style="amber", title="言葉の選び方に意味がある", title_size=15)
    cv.save(path("f09_fc_indication2026.png"))


def f10():
    """FC のエビデンス地図"""
    cv = Canvas(W, 1240)
    y = head(cv, "図11-1　主要試験の投与前フィブリノゲン値",
             "主要評価項目を達成しなかった試験は、いずれも投与前の値が 150 mg/dL を上回っていた。")
    x = 300
    w = W - x - 140
    p = Panel(cv, x, y, w, 330, "", color=INK)
    cv.text(x - 14, y + 165, "投与前 Fib", size=13, color=INK, ha="right",
            va="center", weight="bold")
    # 150 のライン
    p.hline(.34, color=RED, t0=0, t1=1.0)
    cv.text(x - 14, p.py(.34), "150 mg/dL", size=12, color=RED, ha="right",
            va="center", weight="bold")
    trials = (
        (.12, .78, "Rahe-Meyer 2013", GREEN),
        (.33, .74, "REPLACE 2016", C_NOTE),
        (.54, .48, "Bilecen 2017", C_NOTE),
        (.78, .42, "FIBRES 2019", BLUE),
    )
    for t, v, name, col in trials:
        cv.ax.plot([p.px(t)], [p.py(v)], marker="o", markersize=13,
                   color=col, zorder=6)
        cv.text(p.px(t), p.py(v) - 44, name, size=11.5,
                color=col, weight="bold")
    p.note(.33, .20, "主要評価項目 未達成", color=C_NOTE, size=12.5)
    p.note(.78, .20, "非劣性を達成", color=BLUE, size=12.5)

    y2 = y + 330 + 70
    h2 = textbox(cv, 56, y2, W - 112, [
        "「これらの論文の投与前の血中フィブリノゲン値は、いずれも投与基準として設定している",
        "150 mg/dL を超えていることを踏まえると、これらの結果は 150 mg/dL 未満の患者における",
        "有用性を否定するものではない」── 公知申請報告書",
    ], 13.5, style="navy", title="承認を支えた論理", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "「150 未満で有効だと証明された」のではない",
        "「150 未満を対象にした試験がないので、否定もされていない」のである",
        "報告書自身が「予後改善への寄与を示す情報はない」と書いている",
    ], 14, style="red", title="ここは誤解されやすい", title_size=15)
    cv.save(path("f10_fc_evidence.png"))


def f11():
    """クリオと FC"""
    cv = Canvas(W, 1200)
    y = head(cv, "図12-1　クリオプレシピテートとフィブリノゲン濃縮製剤",
             "FIBRES が示したのは「止血効果は同等」。選択の理由は運用側にある。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "含有因子：フィブリノゲン、第 VIII・XIII 因子、vWF ほか",
        "調製：院内で FFP から作製（融解・遠心）",
        "含量：ロットにより変動",
        "保存：凍結。融解に時間がかかる",
        "病原体不活化：なし",
        "保険：K924-3 作製術 600点＋原料 FFP（施設基準あり）",
    ], 13, style="blue", title="クリオプレシピテート", title_size=16, min_h=330)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "含有因子：フィブリノゲンのみ",
        "調製：注射用水で溶解するだけ",
        "含量：1 瓶 1 g と既知",
        "保存：室温可",
        "病原体不活化：加熱・ウイルス除去工程あり",
        "保険：薬剤として算定（心臓血管外科は2026年3月から）",
    ], 13, style="green", title="フィブリノゲン濃縮製剤", title_size=16, min_h=330)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "FIBRES（n=827）：FC 4 g はクリオ 10 単位に非劣性（輸血比 0.96）",
        "血栓塞栓症は FC 群 7.0％、クリオ群 9.6％",
    ], 14, style="navy", title="効果は同等である", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "国内 GL の初期用量：クリオ 3〜4 mL/kg ／ FC 50 mg/kg（ともに 2C）",
        "適応追加を受けて、「クリオ体制を維持するか、FC に寄せるか」を施設で決める時期にある",
    ], 14, style="amber", title="選ぶ理由は運用にある", title_size=15)
    cv.save(path("f11_cryo_vs_fc.png"))


def f12():
    """PCC のエビデンスと適応のずれ"""
    cv = Canvas(W, 1220)
    y = head(cv, "図14-1　エビデンスと日本の適応のずれ",
             "FARES-II が示した使い方は、日本ではまだ適応外である。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "対象：心臓手術中に凝固因子補充を要する出血（n=420）",
        "止血有効性 77.9％ 対 60.4％（差 17.6％）",
        "輸血 6.6 対 9.3 単位",
        "重篤有害事象 36.2％ 対 47.3％（RR 0.76）",
        "急性腎障害 10.3％ 対 18.8％（RR 0.55）",
    ], 13, style="green", title="FARES-II（JAMA 2025）── PCC は FFP に優越",
        title_size=15, min_h=300)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "「ビタミンK拮抗薬投与中の患者における、",
        "急性重篤出血時、又は重大な出血が予想される",
        "緊急を要する手術・処置の施行時の出血傾向の抑制」",
        "→ 心臓手術の凝固障害性出血は適応外",
    ], 13, style="red", title="日本のケイセントラの効能・効果", title_size=15,
        min_h=300)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "ワルファリン服用患者の緊急心臓手術で急性拮抗が必要 → PCC を強く推奨（1B）",
        "非服用患者の複雑心臓手術で、CPB 離脱後の危機的出血が通常の止血療法に不応 →",
        "20〜30 IU/kg を考慮することを弱く推奨（2C／適応外）",
    ], 13.5, style="navy", title="国内ガイドラインの立場（大量出血GL 2019）",
        title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "五年前のフィブリノゲンも同じ位置にいた ── 推奨されながら適応外だった",
        "溝を埋めたのは公知申請と、国内の地味な使用実態データだった",
    ], 14, style="amber", title="この構造は繰り返す", title_size=15)
    cv.save(path("f12_pcc_gap.png"))


def f13():
    """赤血球輸血の閾値"""
    cv = Canvas(W, 1100)
    y = head(cv, "図16-1　赤血球輸血の閾値をめぐる考え方",
             "貧血の害と、輸血の害の両方がある。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "酸素運搬能の低下",
        "心筋虚血",
        "創傷治癒の遅延",
    ], 14, style="amber", title="貧血の害", title_size=16, min_h=210)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "免疫調節・感染",
        "循環過負荷・肺障害",
        "コストと供給の制約",
    ], 14, style="red", title="輸血の害", title_size=16, min_h=210)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "TRICS III（n=5,243）：制限的輸血戦略は非制限的戦略に非劣性",
        "6か月後の転帰でも差はなかった",
        "「もっと輸血すれば安全」という仮定は支持されない",
    ], 14, style="navy", title="心臓手術での答え", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "出血への対応と、貧血への対応は分けて考える",
        "輸血を減らす努力は、安全性の犠牲ではない",
    ], 14, style="green", min_h=120)
    cv.save(path("f13_rbc_threshold.png"))


def f14():
    """トラネキサム酸"""
    cv = Canvas(W, 1140)
    y = head(cv, "図17-1　トラネキサム酸の効果と代償",
             "輸血量と再開胸は減り、痙攣は増える。そして痙攣は用量に依存する。")
    bw = (W - 112 - 60) / 2
    h1 = textbox(cv, 56, y, bw, [
        "血液製剤の総単位数 4,331 対 7,994（P<0.001）",
        "再開胸を要する大出血・タンポナーデ 1.4％ 対 2.8％",
        "主要複合転帰は 16.7％ 対 18.1％（有意差なし）",
    ], 13.5, style="green", title="ATACAS（n=4,631）で得られたもの",
        title_size=15.5, min_h=250)
    h2 = textbox(cv, 56 + bw + 60, y, bw, [
        "術後痙攣 0.7％ 対 0.1％（P=0.002）",
        "OPTIMAL：高用量で輸血は減るが有害事象が増える",
        "腎機能低下例では蓄積する",
    ], 13.5, style="red", title="払う代償", title_size=15.5, min_h=250)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "早期から始める ── 出血してからでは効果が落ちる",
        "高用量に寄せない ── 痙攣が増える",
        "痙攣が起きたとき「トラネキサム酸かもしれない」と想起できるようにしておく",
    ], 14, style="navy", title="実務の三点", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "この薬は日本で生まれた ── 岡本彰祐・歌子が1950〜60年代に見いだした",
    ], 14.5, style="amber", min_h=110)
    cv.save(path("f14_txa.png"))


def f15():
    """PBM の三本柱"""
    cv = Canvas(W, 1160)
    y = head(cv, "図20-1　患者血液管理（PBM）の三本柱",
             "止血戦略は二本目の柱の中心にある。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("① 貧血を是正する", "blue", ["術前貧血の診断と治療",
                                      "鉄欠乏の是正", "採血量そのものを減らす"]),
        ("② 出血を最小化する", "green", ["抗線溶薬", "粘弾性検査とアルゴリズム",
                                        "自己血回収・希釈式自己血", "外科的止血"]),
        ("③ 耐容能を最適化する", "amber", ["制限的輸血閾値", "酸素需給の管理",
                                          "貧血に耐えられる状態を作る"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 13.5, style=st,
                          title=ttl, title_size=15.5, min_h=260))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "EACTS／EACTA 2017、STS／SCA／AmSECT／SABM 2021、ESAIC 2023",
        "いずれも粘弾性検査アルゴリズム・抗線溶薬・自己血回収・制限的輸血閾値を推奨",
    ], 14, style="navy", title="国際的な枠組み", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "国内は大量出血GL 2019。心臓血管外科では POC モニタリングが唯一 1B（強い推奨）",
    ], 14, style="green", min_h=110)
    cv.save(path("f15_pbm_pillars.png"))


def f16():
    """アルゴリズムの骨組み"""
    cv = Canvas(W, 1560)
    y = head(cv, "図21-1　アルゴリズムの骨組み",
             "この順に見て、対応する手を一つずつ当てる。")
    steps = (
        ("① 外科的出血か", "grey", "局所・拍動性なら術者に戻す"),
        ("② ヘパリンは残っていないか", "blue", "HEPTEM と INTEM を比べる → プロタミン"),
        ("③ 線溶は亢進していないか", "red", "APTEM で確認 → 抗線溶薬"),
        ("④ フィブリンは足りているか", "green", "FIBTEM → フィブリノゲン濃縮製剤／クリオ"),
        ("⑤ 血小板は働いているか", "purple", "EXTEM − FIBTEM の差 → 血小板濃厚液"),
    )
    yy = y
    for i, (ttl, st, memo) in enumerate(steps):
        h = textbox(cv, 56 + i * 40, yy, W - 112 - i * 80, [memo], 13.5,
                    style=st, title=ttl, title_size=15, min_h=120)
        yy += h + 18
    y2 = yy + 34
    h2 = textbox(cv, 56, y2, W - 112, [
        "誰が検査を実施し、誰が結果を読み、誰が製剤をオーダーするか",
        "検査を出すタイミング（復温開始時・プロタミン投与後・閉胸前）",
        "夜間・休日にフィブリノゲン製剤が何分で届くか",
        "適応外使用（PCC・rFVIIa）になる場面の院内ルール",
    ], 13.5, style="navy", title="アルゴリズムを作るときに決めておくこと",
        title_size=15)
    cv.save(path("f16_algorithm.png"))


def f17():
    """保険適応の地図"""
    cv = Canvas(W, 1240)
    y = head(cv, "図23-1　止血戦略に関わる保険上の位置づけ（2026年時点）",
             "適応内・施設基準つき・適応外を分けて把握しておく。")
    bw = (W - 112 - 2 * 30) / 3
    cols = (
        ("適応内で使える", "green",
         ["フィブリノゲン濃縮製剤",
          "（人工心肺・出血・投与直前の測定・150 未満）",
          "トラネキサム酸",
          "PCC（ビタミンK拮抗薬の拮抗に限る）"]),
        ("算定に要件がある", "blue",
         ["血液粘弾性検査 D006-21 600点",
          "（人工心肺使用の心臓手術／術前・中・後 各1回）",
          "同種クリオプレシピテート作製 K924-3 600点",
          "（施設基準の届出）"]),
        ("適応外になる", "red",
         ["PCC を心臓手術の凝固障害性出血に使う",
          "（FARES-II の使い方）",
          "rFVIIa を心臓外科で使う",
          "→ 院内手続きを踏む"]),
    )
    hs = []
    for i, (ttl, st, lines) in enumerate(cols):
        hs.append(textbox(cv, 56 + i * (bw + 30), y, bw, lines, 12.5, style=st,
                          title=ttl, title_size=15.5, min_h=300))
    y2 = y + max(hs) + 50
    h2 = textbox(cv, 56, y2, W - 112, [
        "自己血回収 K923：濃縮及び洗浄 5,500点／濾過 3,500点",
        "希釈式自己血輸血 K920：1,000点／200 mL（6歳以上）",
    ], 14, style="amber", title="自己血の算定", title_size=15)
    y3 = y2 + h2 + 44
    textbox(cv, 56, y3, W - 112, [
        "点数と要件は改定で変わる。使用時に最新の点数表と通知を確認すること",
        "本書は2026年9月時点で確認できた情報に基づく",
    ], 14, style="grey", min_h=120)
    cv.save(path("f17_insurance_map.png"))


def f18():
    """危機的出血の順番"""
    cv = Canvas(W, 1200)
    y = head(cv, "図22-1　危機的出血のときの順番",
             "並行して走らせるものと、順に確かめるものを分ける。")
    bw = (W - 112 - 50) / 2
    h1 = textbox(cv, 56, y, bw, [
        "応援を呼ぶ",
        "輸血部に連絡する（必要量を伝える）",
        "加温を止めない",
        "カルシウムを測って補正する",
        "pH とヘマトクリットを追う",
    ], 13.5, style="red", title="並行して走らせる", title_size=16, min_h=290)
    h2 = textbox(cv, 56 + bw + 50, y, bw, [
        "① 外科的出血ではないか",
        "② ヘパリンは残っていないか",
        "③ 線溶は亢進していないか",
        "④ フィブリノゲンは足りているか",
        "⑤ 血小板は働いているか",
    ], 13.5, style="blue", title="順に確かめる", title_size=16, min_h=290)
    y2 = y + max(h1, h2) + 50
    h3 = textbox(cv, 56, y2, W - 112, [
        "MTP を用いることを弱く推奨（2C）",
        "FFP：血小板：赤血球＝1：1：1 を目標に、少なくとも FFP：赤血球は 1：1 より高く（1C）",
    ], 14, style="navy", title="大量輸血プロトコル（大量出血GL 2019）", title_size=15)
    y3 = y2 + h3 + 44
    textbox(cv, 56, y3, W - 112, [
        "体温・pH・イオン化カルシウムが崩れていると、どの製剤も効かない",
        "大量輸血ではクエン酸による低カルシウムが必発 ── 測って補正する",
    ], 14, style="amber", title="土台を忘れない", title_size=15)
    cv.save(path("f18_crisis_order.png"))


if __name__ == "__main__":
    for fn in (f09, f10, f11, f12, f13, f14, f15, f16, f17, f18):
        fn()
        print("ok:", fn.__name__)
