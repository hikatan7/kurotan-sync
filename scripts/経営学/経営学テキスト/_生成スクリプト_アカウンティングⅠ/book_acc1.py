# -*- coding: utf-8 -*-
"""急性期病院で学ぶ MBA アカウンティングⅠ（中級）

本文は acc_p1〜p3.py、数字は calc.py。
    python engine.py acc1
"""
from calc import *  # noqa: F401,F403
import acc_p1
import acc_p2
import acc_p3

META = {
    "series": "アカウンティングⅠ",
    "title": "財務分析・キャッシュフロー・管理会計",
    "sub": "決算書から病院の状態を読み、院内の数字で判断する",
    "compose": "収益性・効率性・安全性の指標、ROA と ROE のデュポン分解、キャッシュフロー計算書の読み方、CVP 分析、診療科別原価計算と配賦、関連原価、予算と業績評価",
    "extra": "全 12 章／図版 9 点／例の病院と数字はすべて架空",
    "date": "2026 年 10 月 15 日",
    "file": "急性期病院で学ぶ_MBAアカウンティングⅠ_財務分析・キャッシュフロー・管理会計",
}

REFS = {
    "globis": "グロービス経営大学院 編著. グロービスMBAアカウンティング 改訂4版. ダイヤモンド社; 2022. ISBN 978-4-478-11672-2",
    "sakurai": "桜井久勝. 財務諸表分析 第8版. 中央経済社; 2020. ISBN 978-4-502-34241-7",
    "ito": "伊藤邦雄. 新・現代会計入門 第7版. 日経BP日本経済新聞出版; 2026. ISBN 978-4-296-12672-9",
    "sakuraim": "櫻井通晴. 管理会計 第7版. 同文舘出版; 2019. ISBN 978-4-495-16147-7",
    "arai": "荒井耕. 病院原価計算 ── 医療制度適応への経営改革. 中央経済社; 2009. ISBN 978-4-502-29060-2",
    "junsoku": "厚生労働省医政局長. 病院会計準則の改正について（平成16年8月19日 医政発第0819001号）別添 病院会計準則［改正版］. https://www.mhlw.go.jp/topics/bukyoku/isei/igyou/igyoukeiei/tuchi/jyunsoku/jyunsoku01.pdf（2026年10月15日閲覧）",
    "kijun": "医療法人会計基準（平成28年厚生労働省令第95号）第1条. e-Gov 法令検索. https://laws.e-gov.go.jp/law/428M60000100095（2026年10月15日閲覧）",
    "kouei": "地方公営企業法施行規則（昭和27年総理府令第73号）第21条, 別表第1号. e-Gov 法令検索. https://laws.e-gov.go.jp/law/327M50000002073（2026年10月15日閲覧）",
    "iryouhou": "医療法（昭和23年法律第205号）第54条. e-Gov 法令検索. https://laws.e-gov.go.jp/law/323AC0000000205（2026年10月15日閲覧）",
    "nissim01": "Nissim D, Penman SH. Ratio analysis and equity valuation: from research to practice. Rev Account Stud. 2001;6(1):109-54. doi:10.1023/A:1011338221623",
    "soliman08": "Soliman MT. The use of DuPont analysis by market participants. Account Rev. 2008;83(3):823-53. doi:10.2308/accr.2008.83.3.823",
    "beaver66": "Beaver WH. Financial ratios as predictors of failure. J Account Res. 1966;4:71-111. doi:10.2307/2490171",
    "altman68": "Altman EI. Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. J Finance. 1968;23(4):589-609. doi:10.1111/j.1540-6261.1968.tb00843.x",
    "dickinson11": "Dickinson V. Cash flow patterns as a proxy for firm life cycle. Account Rev. 2011;86(6):1969-94. doi:10.2308/accr-10130",
    "roberts99": "Roberts RR, Frutos PW, Ciavarella GG, Gussow LM, Mensah EK, Kampe LM, et al. Distribution of variable vs fixed costs of hospital care. JAMA. 1999;281(7):644-9. doi:10.1001/jama.281.7.644. PMID 10029127",
    "taheri00": "Taheri PA, Butz DA, Greenfield LJ. Length of stay has minimal impact on the cost of hospital admission. J Am Coll Surg. 2000;191(2):123-30. doi:10.1016/S1072-7515(00)00352-5. PMID 10945354",
    "kaplan04": "Kaplan RS, Anderson SR. Time-driven activity-based costing. Harv Bus Rev. 2004;82(11):131-8, 150. PMID 15559451",
    "kaplan11": "Kaplan RS, Porter ME. How to solve the cost crisis in health care. Harv Bus Rev. 2011;89(9):46-52, 54, 56-61 passim. PMID 21939127",
    "keel17": "Keel G, Savage C, Rafiq M, Mazzocato P. Time-driven activity-based costing in health care: a systematic review of the literature. Health Policy. 2017;121(7):755-63. doi:10.1016/j.healthpol.2017.04.013. PMID 28535996",
    "macario10": "Macario A. What does one minute of operating room time cost? J Clin Anesth. 2010;22(4):233-6. doi:10.1016/j.jclinane.2010.02.003. PMID 20522350",
    "pizzini06": "Pizzini MJ. The relation between cost-system design, managers' evaluations of the relevance and usefulness of cost data, and financial performance: an empirical study of US hospitals. Account Organ Soc. 2006;31(2):179-210. doi:10.1016/j.aos.2004.11.001",
    "eldenburg17": "Eldenburg LG, Krishnan HA, Krishnan R. Management accounting and control in the hospital industry: a review. J Gov Nonprofit Account. 2017;6(1):52-91. doi:10.2308/ogna-51922",
    "arkes85": "Arkes HR, Blumer C. The psychology of sunk cost. Organ Behav Hum Decis Process. 1985;35(1):124-40. doi:10.1016/0749-5978(85)90049-4",
    "kaplan92": "Kaplan RS, Norton DP. The balanced scorecard: measures that drive performance. Harv Bus Rev. 1992;70(1):71-9. PMID 10119714",
    "kerr75": "Kerr S. On the folly of rewarding A, while hoping for B. Acad Manage J. 1975;18(4):769-83. doi:10.2307/255378",
    "graham05": "Graham JR, Harvey CR, Rajgopal S. The economic implications of corporate financial reporting. J Account Econ. 2005;40(1-3):3-73. doi:10.1016/j.jacceco.2005.01.002",
    "hope03": "Hope J, Fraser R. Who needs budgets? Harv Bus Rev. 2003;81(2):108-15, 126. PMID 12577658",
}

_y = ("前期", "当期")

FIGS = [
    ("f01_profit.png", "waterfall", dict(
        title="A病院（当期）の利益の段階：医業収益から当期純利益まで",
        steps=[("医業収益", P2["rev"], "total"), ("給与費", -P2["salary"], "delta"),
               ("材料費", -P2["material"], "delta"), ("委託費", -P2["outsrc"], "delta"),
               ("設備\n関係費", -P2["equip"], "delta"), ("経費ほか", -P2["expense"], "delta"),
               ("医業利益", P2["op"], "total"), ("医業外\nの損益", P2["nonop_in"] - P2["interest"], "delta"),
               ("経常利益", P2["ord"], "total"), ("法人税等", -P2["tax"], "delta"),
               ("当期\n純利益", P2["ni"], "total")],
        note="単位 百万円。数値はすべて架空", h=3.9)),
    ("f02_coststruct.png", "bars", dict(
        title="医業収益に対する費用の割合（%）：前期と当期",
        labels=["給与費", "材料費", "委託費", "設備関係費", "経費ほか", "医業利益"],
        series=[(_y[0], [round(R1[k], 1) for k in ("salary", "material", "outsrc", "equip", "expense", "op_m")], "grey"),
                (_y[1], [round(R2[k], 1) for k in ("salary", "material", "outsrc", "equip", "expense", "op_m")], "blue")],
        ylabel="医業収益に対する %", note="数値はすべて架空")),
    ("f03_dupont.png", "cards", dict(
        title="ROE を三つに分ける：A病院の前期と当期",
        cols=2,
        items=[("ROE（純資産利益率）", ["%.1f%% → %.1f%%" % (R1["roe"], R2["roe"]), "＝ 当期純利益 ÷ 純資産"]),
               ("① 純利益率", ["%.2f%% → %.2f%%" % (R1["ni_m"], R2["ni_m"]), "＝ 当期純利益 ÷ 医業収益", "稼ぐ力"]),
               ("② 総資産回転率", ["%.2f回 → %.2f回" % (R1["at"], R2["at"]), "＝ 医業収益 ÷ 総資産", "資産を使う力"]),
               ("③ 財務レバレッジ", ["%.2f倍 → %.2f倍" % (R1["lev"], R2["lev"]), "＝ 総資産 ÷ 純資産", "借入の使い方"])])),
    ("f04_cfbridge.png", "waterfall", dict(
        title="当期の税引前利益から現金の増減まで（間接法）",
        steps=[("税引前\n利益", CF["pretax"], "total"), ("減価\n償却費", CF["dep"], "delta"),
               ("引当金\nの増加", CF["d_ret"], "delta"), ("未収金\nの増加", CF["d_ar"], "delta"),
               ("棚卸資産\nの増加", CF["d_inv"], "delta"), ("買掛金等\nの増加", CF["d_ap"] + CF["d_ocl"], "delta"),
               ("法人税等\nの支払", CF["taxpaid"], "delta"), ("業務活動\nCF", CF_OP, "total"),
               ("設備投資", CF_INV, "delta"), ("借入\n（純額）", CF_FIN, "delta"), ("現金の\n増減", CF_NET, "total")],
        note="単位 百万円。数値はすべて架空", h=3.9)),
    ("f05_cfpattern.png", "cards", dict(
        title="三つのキャッシュフローの符号で読む組織の段階（ディキンソンの分類）",
        cols=3,
        items=[("導入期（−／−／＋）", ["本業はまだ現金を生まない", "投資を借入や出資で賄う", "新設直後の病院"]),
               ("成長期（＋／−／＋）", ["本業は現金を生む", "それを上回る投資を借入で補う", "増床・建て替えの時期"]),
               ("成熟期（＋／−／−）", ["本業の現金で投資も返済も賄う", "いちばん安定した形"]),
               ("衰退期（−／＋／±）", ["本業が現金を失う", "資産を売って穴を埋める"]),
               ("淘汰期（残りの組み合わせ）", ["−／−／− は手元の現金を取り崩す", "＋／＋／− は資産売却で返済を急ぐ"]),
               ("病院で読むときの注意", ["補助金の入り方と", "建て替えの周期で", "符号は一時的に変わる"])])),
    ("f06_cvp.png", "lines", dict(
        title="A病院（当期）の損益分岐点：固定費が重く、余裕は小さい",
        series=[("医業収益", [0, 6000, 12000, 14000], [0, 6000, 12000, 14000], "blue", "-"),
                ("医業費用（固定費＋変動費）", [0, 6000, 12000, 14000], [FC + VC / P2["rev"] * x for x in (0, 6000, 12000, 14000)], "red", "-"),
                ("固定費", [0, 14000], [FC, FC], "grey", "--")],
        xlabel="医業収益（百万円）", ylabel="百万円", legend_loc="upper left",
        marks=[(BEP, BEP, "損益分岐点 %s" % f0(BEP), -5600, -3000),
               (P2["rev"], P2["rev"], "当期 %s（余裕 %.1f%%）" % (f0(P2["rev"]), MOS), -3000, -6000)],
        xfmt="%.0f", note="変動費＝材料費＋委託費の3割。数値はすべて架空")),
    ("f07_alloc.png", "bars", dict(
        title="共通費の配り方で、診療科の損益の見え方が変わる",
        labels=["配賦前（貢献利益）"] + ["%s で配賦" % n for n, _, _ in ALLOC],
        series=[(d, [D_CM[i]] + [round(a[2][i]) for a in ALLOC], c) for i, (d, c) in enumerate(zip(DEPTS, ("blue", "green", "orange")))],
        ylabel="百万円", note="共通費 %s を三つの基準で配った。数値はすべて架空" % f0(COMMON))),
    ("f08_stepdown.png", "flow", dict(
        title="部門別原価計算の流れ（階梯式配賦）",
        steps=[("費用を部門に集める", ["給与・材料・委託などを", "発生した部門に直課", "直課できない費用は", "共通費としてためる"]),
               ("補助・管理部門", ["事務・施設・医療情報", "→ 面積・職員数などで", "他の部門へ配る"]),
               ("中央診療部門", ["手術室・検査・放射線", "→ 時間・件数などで", "診療科へ配る"]),
               ("診療科", ["直接費＋配賦額", "＝ 診療科の原価", "収益と比べて損益を出す"])],
        note="配る順番と配る基準を変えるたびに、診療科の損益は変わる。判断に使う前に、配賦前の貢献利益を必ず並べる。")),
    ("f09_variance.png", "waterfall", dict(
        title="入院収益：予算と実績の差を、患者数と単価に分ける",
        steps=[("予算", BUD_INPT, "total"), ("患者数\nの差異", VOL_VAR, "delta"),
               ("単価\nの差異", PRICE_VAR, "delta"), ("実績", P2["inpt"], "total")],
        note="予算：病床利用率 %d%%・単価 %s 円。実績：%d%%・%s 円。縦軸は 8,000 から。単位 百万円、数値は架空"
             % (round(BUD_OCC * 100), f0(BUD_UNIT), round(P2["occ"] * 100), f0(P2["unit"])), h=3.4,
        ymin=8000)),
]

BLOCKS = acc_p1.BLOCKS + acc_p2.BLOCKS + acc_p3.BLOCKS
