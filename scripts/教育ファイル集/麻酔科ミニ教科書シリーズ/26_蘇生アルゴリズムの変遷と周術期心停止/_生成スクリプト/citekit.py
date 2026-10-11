# -*- coding: utf-8 -*-
"""本文中の {{PMID}} を出現順の番号に置き換え、章末の参考文献一覧を作る。

書誌は文献台帳（高度心臓血管麻酔_SourceLedger_v1.xlsx）から読む。
台帳にない PMID は本文で使えない（＝出典を確認していない、ということ）。
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "..", "蘇生アルゴリズム_SourceLedger.xlsx")

_META = None


def _load():
    """PMID -> 書誌。台帳の全シートから集める。"""
    global _META
    if _META is not None:
        return _META
    import openpyxl
    wb = openpyxl.load_workbook(LEDGER, read_only=True, data_only=True)
    meta = {}
    for name in wb.sheetnames:
        if not name.startswith("㉖"):
            continue
        ws = wb[name]
        head = None
        for row in ws.iter_rows(values_only=True):
            if head is None:
                head = [str(c or "") for c in row]
                idx = {h: i for i, h in enumerate(head)}
                continue
            if not row or not row[0]:
                continue
            def g(k):
                i = idx.get(k)
                v = row[i] if i is not None and i < len(row) else None
                return "" if v is None else str(v).strip()
            # Ⅰ〜Ⅶ は「PMID 39316661」、Ⅷ は数字のみ。どちらも数字部分を取る。
            mm = re.search(r"(\d{7,9})", g("PMID（リンク）"))
            if not mm:
                continue
            pmid = mm.group(1)
            meta[pmid] = {
                "sid": g("S-ID"), "year": g("年"), "first": g("筆頭著者/学会"),
                "title": g("タイトル"), "journal": g("雑誌"),
                "doi": re.sub(r"^\s*(doi:?|DOI:?)\s*", "", g("DOI（リンク）")), "sheet": name,
            }
    wb.close()
    _META = meta
    return meta


def _fmt_range(nums):
    """[1,2,3,7] -> '1-3,7'"""
    nums = sorted(set(nums))
    out = []
    i = 0
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


class Cites(object):
    def __init__(self, strict=True):
        self.meta = _load()
        self.order = []          # PMID の出現順
        self.missing = []        # 台帳にない PMID
        self.strict = strict

    def mark(self, pmids):
        nums = []
        for p in pmids:
            if p not in self.meta:
                if p not in self.missing:
                    self.missing.append(p)
                if self.strict:
                    raise KeyError("台帳にない PMID: %s" % p)
                continue
            if p not in self.order:
                self.order.append(p)
            nums.append(self.order.index(p) + 1)
        return _fmt_range(nums) if nums else ""

    def count(self):
        return len(self.order)

    def rows(self):
        """参考文献一覧の行（番号, 記述, PMID, DOI）"""
        out = []
        for i, p in enumerate(self.order, 1):
            m = self.meta[p]
            au = m["first"]
            if au and not au.endswith(("会", "学会", "機構", "委員会")):
                au = au + ", et al."
            ttl = m["title"].rstrip(".")
            desc = "%s %s. %s. %s." % (au, ttl, m["journal"], m["year"])
            out.append([str(i), desc.strip(), p, m["doi"]])
        return out


def scan_text(blocks):
    """ブロック列に出てくる PMID を、本文の並び順で返す（検査用）"""
    import bookkit
    found = []
    def walk(x):
        if isinstance(x, str):
            for m in bookkit.CITE_RE.finditer(x):
                for p in m.group(1).split(","):
                    found.append(p.strip())
        elif isinstance(x, (list, tuple)):
            for y in x:
                walk(y)
    walk(blocks)
    return found
