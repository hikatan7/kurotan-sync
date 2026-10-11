# -*- coding: utf-8 -*-
"""参考文献台帳と番号引用（バンクーバー方式）の解決器。

本文には {{12}} のように台帳IDを書く。出現順に番号を振り直し、巻末に番号順の一覧を出す。
台帳にないIDは使えない。すべての書誌は 2026-09-25 に以下で実在を確認した。
  - Crossref API（DOI）／PubMed E-utilities（PMID）
  - 国立国会図書館サーチ・openBD（書籍の ISBN）
"""

REFS = {
    1: ("高田貴久, 岩澤智之",
        "問題解決 ── あらゆる課題を突破する ビジネスパーソン必須の仕事術",
        "英治出版", "2014", "ISBN 978-4-86276-124-8"),
    2: ("Davenport TH", "Competing on analytics",
        "Harvard Business Review 84(1):98-107", "2006", "PMID 16447373"),
    3: ("トーマス・H・ダベンポート, ジェーン・G・ハリス（村井章子 訳）",
        "分析力を武器とする企業 ── 強さを支える新しい戦略の科学",
        "日経BP社（原著 Competing on Analytics, Harvard Business School Press, 2007）",
        "2008", "ISBN 978-4-8222-4684-6"),
    4: ("Tukey JW", "Exploratory Data Analysis",
        "Addison-Wesley", "1977", "ISBN 978-0-201-07616-5"),
    5: ("Anscombe FJ", "Graphs in statistical analysis",
        "The American Statistician 27(1):17-21", "1973",
        "doi:10.1080/00031305.1973.10478966"),
    6: ("Simpson EH", "The interpretation of interaction in contingency tables",
        "Journal of the Royal Statistical Society Series B 13(2):238-241", "1951",
        "doi:10.1111/j.2517-6161.1951.tb00088.x"),
    7: ("Bickel PJ, Hammel EA, O'Connell JW",
        "Sex bias in graduate admissions: data from Berkeley",
        "Science 187(4175):398-404", "1975", "doi:10.1126/science.187.4175.398"),
    8: ("Cleveland WS, McGill R",
        "Graphical perception: theory, experimentation, and application to the "
        "development of graphical methods",
        "Journal of the American Statistical Association 79(387):531-554", "1984",
        "doi:10.1080/01621459.1984.10478080"),
    9: ("Tufte ER", "The Visual Display of Quantitative Information. 2nd ed",
        "Graphics Press", "2001", "ISBN 978-0-9613921-4-7"),
    10: ("Little JDC", "A proof for the queuing formula: L = λW",
         "Operations Research 9(3):383-387", "1961", "doi:10.1287/opre.9.3.383"),
    11: ("Kingman JFC", "The single server queue in heavy traffic",
         "Mathematical Proceedings of the Cambridge Philosophical Society 57(4):902-904",
         "1961", "doi:10.1017/S0305004100036094"),
    12: ("McManus ML, Long MC, Cooper A, Mandell J, Berwick DM, Pagano M, Litvak E",
         "Variability in surgical caseload and access to intensive care services",
         "Anesthesiology 98(6):1491-1496", "2003",
         "doi:10.1097/00000542-200306000-00029"),
    13: ("Litvak E, Long MC",
         "Cost and quality under managed care: irreconcilable differences?",
         "American Journal of Managed Care 6(3):305-312", "2000", "PMID 10977431"),
    14: ("Green LV", "How many hospital beds?",
         "Inquiry 39(4):400-412", "2002", "doi:10.5034/inquiryjrnl_39.4.400"),
    15: ("Huff D", "How to Lie with Statistics",
         "W. W. Norton（初版 1954 年）", "1993", "ISBN 978-0-393-31072-6"),
    16: ("ハンス・ロスリング, オーラ・ロスリング, アンナ・ロスリング・ロンランド（上杉周作, 関美和 訳）",
         "FACTFULNESS ── 10の思い込みを乗り越え、データを基に世界を正しく見る習慣",
         "日経BP社", "2019", "ISBN 978-4-8222-8960-7"),
    17: ("バーバラ・ミント（山崎康司 訳）",
         "新版 考える技術・書く技術 ── 問題解決力を伸ばすピラミッド原則",
         "ダイヤモンド社", "1999", "ISBN 978-4-478-49027-3"),
}


class Cites(object):
    """出現順に番号を振る。bookkit.set_cite_resolver に渡す。"""

    def __init__(self):
        self.order = []

    def mark(self, ids):
        nums = []
        for s in ids:
            k = int(s)
            if k not in REFS:
                raise KeyError("台帳にない文献ID: %s" % s)
            if k not in self.order:
                self.order.append(k)
            nums.append(self.order.index(k) + 1)
        return _fmt(nums)

    def count(self):
        return len(self.order)

    def rows(self):
        out = []
        for i, k in enumerate(self.order, 1):
            au, ttl, src, yr, ident = REFS[k]
            desc = "%s. %s. %s; %s." % (au, ttl, src, yr)
            if ident:
                desc += "　" + ident
            out.append([str(i), desc, "", ""])
        return out


def _fmt(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j - i >= 2:
            out.append("%d-%d" % (nums[i], nums[j]))
        else:
            out.extend(str(n) for n in nums[i:j + 1])
        i = j + 1
    return ",".join(out)
