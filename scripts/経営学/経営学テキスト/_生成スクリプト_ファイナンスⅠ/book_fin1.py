# -*- coding: utf-8 -*-
"""急性期病院で学ぶ MBA ファイナンスⅠ（中級）

本文は fin_p1〜p3.py、数字は calc.py。
    python engine.py fin1
"""
from calc import *  # noqa: F401,F403
import fin_p1
import fin_p2
import fin_p3

META = {
    "series": "ファイナンスⅠ",
    "title": "投資判断・資本コスト・企業価値",
    "sub": "基礎編の一歩先で、病院の大きな決定を数字で説明する",
    "compose": "増分キャッシュフロー、投資の物差し、感度分析とリアルオプション、CAPM と WACC、DCF とマルチプル、資本構成と内部留保",
    "extra": "全 12 章／図版 9 点／例の病院と数字はすべて架空",
    "date": "2026 年 10 月 15 日",
    "file": "急性期病院で学ぶ_MBAファイナンスⅠ_投資判断・資本コスト・企業価値",
}

REFS = {
    "bma": "リチャード・A・ブリーリー, スチュワート・C・マイヤーズ, フランクリン・アレン（藤井眞理子, 國枝繁樹 監訳）. コーポレートファイナンス 第10版 上・下. 日経BP社; 2014. ISBN 978-4-8222-4860-4（上）, 978-4-8222-4861-1（下）",
    "globis": "グロービス経営大学院 編著. 新版 グロービスMBAファイナンス. ダイヤモンド社; 2009. ISBN 978-4-478-00876-8",
    "sunagawa": "砂川伸幸. コーポレートファイナンス入門 第2版（日経文庫）. 日本経済新聞出版社; 2017. ISBN 978-4-532-11368-1",
    "koller": "マッキンゼー・アンド・カンパニー, ティム・コラー, マーク・フーカート, デイビッド・ウェッセルズ（マッキンゼー・コーポレート・ファイナンス・グループ 訳）. 企業価値評価 ── バリュエーションの理論と実践 第7版 上・下. ダイヤモンド社; 2022. ISBN 978-4-478-11287-8（上）, 978-4-478-11288-5（下）",
    "graham01": "Graham JR, Harvey CR. The theory and practice of corporate finance: evidence from the field. J Financ Econ. 2001;60(2-3):187-243. doi:10.1016/S0304-405X(01)00044-7",
    "teraishi26": "Teraishi F, Hasegawa Y, Takahashi K, Kato Y, Takahashi R, Okabayashi H, et al. Establishing a sustainable and high-utilization robot-assisted surgery platform in a regional cancer center: insights from a multidisciplinary, break-even-guided operational strategy. J Robot Surg. 2026;20(1):864. doi:10.1007/s11701-026-03841-4. PMID 42627549",
    "kojo26": "Kojo M, Morishita S, Takemoto K, Nagata T, Naito K, Nakano K. Economic outcomes of robot-assisted surgery for gastric and colorectal cancer at a general hospital: a real-world analysis of the volume-cost dilemma. Surg Today. 2026 Aug 18. Online ahead of print. doi:10.1007/s00595-026-03467-x. PMID 42611262",
    "lovallo03": "Lovallo D, Kahneman D. Delusions of success. How optimism undermines executives' decisions. Harv Bus Rev. 2003;81(7):56-63, 117. PMID 12858711",
    "myers77": "Myers SC. Determinants of corporate borrowing. J Financ Econ. 1977;5(2):147-75. doi:10.1016/0304-405X(77)90015-0",
    "mcdonald86": "McDonald R, Siegel D. The value of waiting to invest. Q J Econ. 1986;101(4):707-27. doi:10.2307/1884175",
    "markowitz52": "Markowitz H. Portfolio selection. J Finance. 1952;7(1):77-91. doi:10.1111/j.1540-6261.1952.tb01525.x",
    "sharpe64": "Sharpe WF. Capital asset prices: a theory of market equilibrium under conditions of risk. J Finance. 1964;19(3):425-42. doi:10.1111/j.1540-6261.1964.tb02865.x",
    "mofjgb": "財務省. 国債金利情報（ヒストリカルデータ jgbcm.csv、2026年10月14日の10年債 3.015%）. https://www.mof.go.jp/jgbs/reference/interest_rate/index.htm（2026年10月15日閲覧）",
    "fama04": "Fama EF, French KR. The capital asset pricing model: theory and evidence. J Econ Perspect. 2004;18(3):25-46. doi:10.1257/0895330042162430",
    "huang18": "Huang SS, Yang J, Carroll N. Taxes, bankruptcy costs, and capital structure in for-profit and not-for-profit hospitals. Health Serv Manage Res. 2018;31(1):21-32. doi:10.1177/0951484817726780. PMID 28876139",
    "wedig88": "Wedig G, Sloan FA, Hassan M, Morrisey MA. Capital structure, ownership, and capital payment policy: the case of hospitals. J Finance. 1988;43(1):21-40. doi:10.1111/j.1540-6261.1988.tb02586.x",
    "gordon59": "Gordon MJ. Dividends, earnings, and stock prices. Rev Econ Stat. 1959;41(2):99-105. doi:10.2307/1927792",
    "kaplan95": "Kaplan SN, Ruback RS. The valuation of cash flow forecasts: an empirical analysis. J Finance. 1995;50(4):1059-93. doi:10.1111/j.1540-6261.1995.tb04050.x",
    "mm58": "Modigliani F, Miller MH. The cost of capital, corporation finance and the theory of investment. Am Econ Rev. 1958;48(3):261-97",
    "mm63": "Modigliani F, Miller MH. Corporate income taxes and the cost of capital: a correction. Am Econ Rev. 1963;53(3):433-43",
    "myers84": "Myers SC. The capital structure puzzle. J Finance. 1984;39(3):574-92. doi:10.1111/j.1540-6261.1984.tb03646.x",
    "myersmajluf84": "Myers SC, Majluf NS. Corporate financing and investment decisions when firms have information that investors do not have. J Financ Econ. 1984;13(2):187-221. doi:10.1016/0304-405X(84)90023-0",
    "iryouhou": "医療法（昭和23年法律第205号）第54条, 第54条の2. e-Gov 法令検索. https://laws.e-gov.go.jp/law/323AC0000000205（2026年10月15日閲覧）",
    "soumugl": "総務省. 持続可能な地域医療提供体制を確保するための公立病院経営強化ガイドライン. 2022年3月. https://www.soumu.go.jp/main_content/000803322.pdf",
    "jensen76": "Jensen MC, Meckling WH. Theory of the firm: managerial behavior, agency costs and ownership structure. J Financ Econ. 1976;3(4):305-60. doi:10.1016/0304-405X(76)90026-X",
    "jensen86": "Jensen MC. Agency costs of free cash flow, corporate finance, and takeovers. Am Econ Rev. 1986;76(2):323-9",
    "mm61": "Miller MH, Modigliani F. Dividend policy, growth, and the valuation of shares. J Bus. 1961;34(4):411-33. doi:10.1086/294442",
    "lintner56": "Lintner J. Distribution of incomes of corporations among dividends, retained earnings, and taxes. Am Econ Rev. 1956;46(2):97-113",
    "mhlwmochibun": "厚生労働省医政局. 「持分なし医療法人」への移行に関する手引書 ── 移行促進税制を中心として（令和8年3月改訂）. p.3. https://www.mhlw.go.jp/content/10800000/000940229.pdf",
    "mhlwqa": "厚生労働省医政局. 持分の定めのない医療法人への移行計画認定制度 Q&A（令和8年8月改訂）. Q1-1. https://www.mhlw.go.jp/content/10800000/000951888.pdf",
}

_npv_rates = [i / 1000 for i in range(0, 161, 2)]
_A_curve = [npv(A["cfs"], r) for r in _npv_rates]
_B_curve = [npv(B_CFS, r) for r in _npv_rates]
_cross_npv = npv(A["cfs"], CROSS)

_dv = [i / 100 for i in range(0, 61, 2)]


def _mm(dv):
    # V＝VU＋tD、D＝dv×V → V＝VU／(1−t·dv)
    v = VU / (1 - TAX * dv)
    d, e = dv * v, (1 - dv) * v
    re_ = MM_RU + (MM_RU - MM_RD) * (1 - TAX) * (d / e)
    w = (d * MM_RD * (1 - TAX) + e * re_) / v
    return re_, w


FIGS = [
    ("f01_incremental.png", "cards", dict(
        title="増分キャッシュフローに入れるもの・入れないもの",
        cols=2,
        items=[("入れる", ["機会費用（使えなくなる倉庫の代わりの賃料）",
                         "副次効果（腹腔鏡からの置き換えによる差額）",
                         "運転資本の増加（未収金）と最後の回収",
                         "減価償却による税の減少（お金は動かないが税は減る）"]),
               ("入れない", ["埋没費用（昨年の調査費。やめても戻らない）",
                           "配賦される共通費（導入しても増えない）",
                           "借入の利息（割引率の側で扱う。二重に数えない）",
                           "置き換え症例の収益の全額（増えるのは差額だけ）"])])),
    ("f02_npvprofile.png", "lines", dict(
        title="NPV プロファイル：割引率で順位が入れ替わる",
        series=[("A案（ロボット2台目）", [r * 100 for r in _npv_rates], _A_curve, "blue", "-"),
                ("B案（腹腔鏡更新）", [r * 100 for r in _npv_rates], _B_curve, "orange", "-")],
        xlabel="割引率（%）", ylabel="NPV（百万円）", hline=0,
        marks=[(CROSS * 100, _cross_npv, "交点 %.1f%%" % (CROSS * 100), 1.2, 40),
               (A_IRR * 100, 0, "A案の IRR %.1f%%" % (A_IRR * 100), -4.4, -40),
               (B_IRR * 100, 0, "B案の IRR %.1f%%" % (B_IRR * 100), 0.8, 45),
               (WACC, A["npv"], "A案 %.1f%%で %s" % (WACC, f1(A["npv"])), 1.0, 55)],
        note="数値はすべて架空")),
    ("f03_tornado.png", "tornado", dict(
        title="どの前提が外れると NPV が大きく動くか（基準 NPV %s）" % f1(A["npv"]),
        rows=SENS, base=A["npv"], xlabel="NPV（百万円）　赤＝悪い側、青＝良い側、点線＝NPV ゼロ",
        note="数値はすべて架空")),
    ("f04_tree.png", "tree", dict(
        title="いま投資するか、1年待つか",
        root=("いま投資する", ["期待 NPV %s" % f1(NOW_E)]),
        branches=[("確率 50%", "近隣の外科縮小が決まる（新規 %d 件/年）" % GOOD_N, "NPV %s" % f1(NOW_GOOD), "green"),
                  ("確率 50%", "決まらない（新規 %d 件/年）" % BAD_N, "NPV %s" % f1(NOW_BAD), "red")],
        wait=(("1年待つ", ["期待 NPV %s" % f1(WAIT_E), "（1年分割り引いた値）"]),
              [("確率 50%", "決まったら投資する", "NPV %s ÷ %.3f ＝ %s" % (f1(NOW_GOOD), 1 + R, f1(NOW_GOOD / (1 + R))), "green"),
               ("確率 50%", "決まらなければ投資しない", "NPV 0", "grey")]),
        note="待つことの価値 ＝ %s − %s ＝ %s（百万円、数値はすべて架空）" % (f1(WAIT_E), f1(NOW_E), f1(OPT_VALUE)))),
    ("f05_sml.png", "lines", dict(
        title="証券市場線：β が大きいほど求められる利回りが高い",
        series=[("求められる利回り", [0, 0.5, 1.0, 1.5], [RF + b * MRP for b in (0, 0.5, 1.0, 1.5)], "navy", "-")],
        xlabel="β（市場全体と一緒に動く度合い）", ylabel="求められる利回り（%）",
        marks=[(0, RF, "無リスク利子率 %.1f%%" % RF, 0.04, 3.4),
               (1.0, RF + MRP, "市場全体 %.1f%%" % (RF + MRP), -0.42, 1.4),
               (BETA_L, RE, "A病院 β %.2f → %.2f%%" % (BETA_L, RE), 0.1, -2.6)],
        xfmt="%.1f", note="無リスク利子率と市場リスクプレミアムは本書の仮定")),
    ("f06_dcf.png", "stack", dict(
        title="C病院の事業価値 %s の内訳（現在価値、百万円）" % f0(C["ev"]),
        labels=["1年目", "2年目", "3年目", "4年目", "5年目", "継続価値"],
        vals=[f / (1 + C_WACC / 100) ** (t + 1) for t, f in enumerate(C_FCF)] + [C["pv_tv"]],
        colors=["blue"] * 5 + ["orange"], ylabel="百万円", total_label="事業価値",
        note="継続価値が全体の %d%%。数値はすべて架空" % round(C_TV_SHARE * 100))),
    ("f07_mm.png", "lines", dict(
        title="借入を増やすと株主資本コストは上がり、WACC は節税の分だけ下がる",
        series=[("株主資本コスト", [d * 100 for d in _dv], [_mm(d)[0] for d in _dv], "red", "-"),
                ("WACC", [d * 100 for d in _dv], [_mm(d)[1] for d in _dv], "navy", "-"),
                ("借入金利（税引後）", [d * 100 for d in _dv], [MM_RD * (1 - TAX)] * len(_dv), "grey", "--")],
        xlabel="負債の割合 D／V（%）", ylabel="資本コスト（%）", legend_loc="upper left",
        note="倒産の費用を入れていない。入れると、ある水準から先で WACC は上がりに転じる（トレードオフ理論）。数値は架空")),
    ("f08_pecking.png", "flow", dict(
        title="医療法人の資金調達の順番（ペッキングオーダー）",
        steps=[("内部の資金", ["過去の利益の蓄積", "（配当できないので", "すべて内部に残る）"]),
               ("借入", ["銀行", "公的な融資機関", "リース"]),
               ("債券", ["社会医療法人債", "（社会医療法人のみ）"]),
               ("株式", ["発行できない", "（医療法人には", "株式がない）"])],
        note="公立病院は、病院事業債（企業債）と設置自治体の一般会計からの繰り出しが主な財源になる。")),
    ("f09_limits.png", "cards", dict(
        title="病院でファイナンスの道具が届きにくい四つの領域",
        cols=2,
        items=[("お金で測れない価値", ["救急・不採算の診療科・教育", "→ 引き受ける持ち出しの額として示す"]),
               ("制度で決まる価格", ["2年ごとの診療報酬改定", "→ シナリオと待つオプションで扱う"]),
               ("公立病院の立場", ["繰り出しは病院の収入、住民の負担", "→ 誰の立場の NPV かを先に決める"]),
               ("見込みの楽観", ["計画者の楽観と組織の圧力", "→ 類似案件の実績と事後の振り返り"])])),
]

BLOCKS = fin_p1.BLOCKS + fin_p2.BLOCKS + fin_p3.BLOCKS
