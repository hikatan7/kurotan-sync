# -*- coding: utf-8 -*-
"""参考文献台帳と、番号引用（バンクーバー方式）の解決器。

本文には {{12}} のように「台帳のID」を書く。出現順に 1) 2) 3) と番号を振り直し、
巻末に番号順の一覧を出す。台帳にないIDは使えない（＝出典未確認のものは書けない）。

すべての書誌は 2026-09-22 に以下で実在を確認した。
  - PubMed E-utilities（PMIDのあるもの）
  - Crossref API（DOIのあるもの）
  - 版元・書誌データベース（和書）
"""

# id: (著者, タイトル, 出典, 年, 識別子)
REFS = {
    # ---- 思考技術の古典 ----
    1: ("バーバラ・ミント（山崎康司 訳）",
        "新版 考える技術・書く技術：問題解決力を伸ばすピラミッド原則",
        "ダイヤモンド社", "1999", "ISBN 978-4-478-49027-3"),
    2: ("安宅和人",
        "イシューからはじめよ［改訂版］──知的生産の「シンプルな本質」",
        "英治出版（初版 2010 年）", "2024", "ISBN 978-4-86276-356-3"),
    3: ("Toulmin SE",
        "The Uses of Argument. Updated edition",
        "Cambridge University Press（初版 1958 年）", "2003",
        "ISBN 978-0-521-53483-3"),
    4: ("Simon HA",
        "Rational choice and the structure of the environment",
        "Psychological Review 63(2):129-138", "1956",
        "doi:10.1037/h0042769"),

    # ---- 認知バイアスと判断 ----
    5: ("Tversky A, Kahneman D",
        "Judgment under uncertainty: heuristics and biases",
        "Science 185(4157):1124-1131", "1974",
        "doi:10.1126/science.185.4157.1124"),
    6: ("Kahneman D",
        "Thinking, Fast and Slow",
        "Farrar, Straus and Giroux（邦訳『ファスト＆スロー』早川書房 2012 年）",
        "2011", "ISBN 978-0-374-27563-1"),
    7: ("Wason PC",
        "Reasoning about a rule",
        "Quarterly Journal of Experimental Psychology 20(3):273-281", "1968",
        "doi:10.1080/14640746808400161"),
    8: ("Kruger J, Dunning D",
        "Unskilled and unaware of it: how difficulties in recognizing one's own "
        "incompetence lead to inflated self-assessments",
        "Journal of Personality and Social Psychology 77(6):1121-1134", "1999",
        "doi:10.1037/0022-3514.77.6.1121"),
    9: ("Arkes HR, Blumer C",
        "The psychology of sunk cost",
        "Organizational Behavior and Human Decision Processes 35(1):124-140",
        "1985", "doi:10.1016/0749-5978(85)90049-4"),
    10: ("Gigerenzer G, Brighton H",
         "Homo heuristicus: why biased minds make better inferences",
         "Topics in Cognitive Science 1(1):107-143", "2009",
         "doi:10.1111/j.1756-8765.2008.01006.x"),
    11: ("Kahneman D, Sibony O, Sunstein CR",
         "Noise: A Flaw in Human Judgment",
         "Little, Brown Spark（邦訳『NOISE』早川書房 2021 年）", "2021",
         "ISBN 978-0-316-45140-6"),

    # ---- 組織と学習 ----
    12: ("Argyris C",
         "Double loop learning in organizations",
         "Harvard Business Review 55(5):115-125", "1977", ""),
    13: ("Edmondson AC",
         "Psychological safety and learning behavior in work teams",
         "Administrative Science Quarterly 44(2):350-383", "1999",
         "doi:10.2307/2666999"),
    14: ("Janis IL",
         "Groupthink: Psychological Studies of Policy Decisions and Fiascoes. 2nd ed",
         "Houghton Mifflin", "1982", "ISBN 978-0-395-31704-8"),

    # ---- 因果と安全 ----
    15: ("Hill AB",
         "The environment and disease: association or causation?",
         "Proceedings of the Royal Society of Medicine 58(5):295-300", "1965",
         "PMID 14283879"),
    16: ("Reason J",
         "Human error: models and management",
         "BMJ 320(7237):768-770", "2000", "PMID 10720363"),

    # ---- 臨床推論・診断エラー ----
    17: ("Croskerry P",
         "The importance of cognitive errors in diagnosis and strategies to "
         "minimize them",
         "Academic Medicine 78(8):775-780", "2003", "PMID 12915363"),
    18: ("Graber ML, Franklin N, Gordon R",
         "Diagnostic error in internal medicine",
         "Archives of Internal Medicine 165(13):1493-1499", "2005",
         "PMID 16009864"),
    19: ("Norman GR, Monteiro SD, Sherbino J, Ilgen JS, Schmidt HG, Mamede S",
         "The causes of errors in clinical reasoning: cognitive biases, "
         "knowledge deficits, and dual process thinking",
         "Academic Medicine 92(1):23-30", "2017", "PMID 27782919"),
    20: ("Mamede S, van Gog T, van den Berge K, et al",
         "Effect of availability bias and reflective reasoning on diagnostic "
         "accuracy among internal medicine residents",
         "JAMA 304(11):1198-1203", "2010", "doi:10.1001/jama.2010.1276"),
    21: ("Mamede S, van Gog T, Moura AS, et al",
         "Reflection as a strategy to foster medical students' acquisition of "
         "diagnostic competence",
         "Medical Education 46(5):464-472", "2012",
         "doi:10.1111/j.1365-2923.2012.04217.x"),

    # ---- 読解と言葉 ----
    22: ("新井紀子",
         "シン読解力──学力と人生を決めるもうひとつの読み方",
         "東洋経済新報社", "2025", "ISBN 978-4-492-76267-7"),
}

_ORDER = []


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
