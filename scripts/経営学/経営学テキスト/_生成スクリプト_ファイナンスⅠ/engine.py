# -*- coding: utf-8 -*-
"""ファイナンスⅠの組版（必修4冊の engine.py を複製して図版の置き場と図の型だけ変えた）。

    python engine.py fin1       → ファイナンスⅠ

本の中身は book_<名前>.py に META・REFS・FIGS・BLOCKS として書く。
本文の {{key1,key2}} は REFS のキーで、出現順に番号を振り直す。
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH
import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     page_break, heading, toc_field, figure, table, bullets,
                     summary, note, column, reflist, NAVY, GREY, TEAL)

FIGROOT = os.path.join(HERE, "..", "図版", "ファイナンスⅠ")
OUTDIR = os.path.join(HERE, "..")


class Cites(object):
    def __init__(self, refs):
        self.refs = refs
        self.order = []

    def mark(self, ids):
        nums = []
        for k in ids:
            if k not in self.refs:
                raise KeyError("台帳にない文献: %s" % k)
            if k not in self.order:
                self.order.append(k)
            nums.append(self.order.index(k) + 1)
        nums = sorted(set(nums))
        out, i = [], 0
        while i < len(nums):
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1
            out.append("%d-%d" % (nums[i], nums[j]) if j - i >= 2
                       else ",".join(str(n) for n in nums[i:j + 1]))
            i = j + 1
        return ",".join(out)

    def rows(self):
        return [[str(i), self.refs[k], "", ""] for i, k in enumerate(self.order, 1)]


def build(name):
    bk = importlib.import_module("book_" + name)
    figdir = os.path.join(FIGROOT, name)
    os.makedirs(figdir, exist_ok=True)
    if getattr(bk, "FIGS", None):
        import figkit_fin as figkit
        for fn, kind, kw in bk.FIGS:
            getattr(figkit, kind)(os.path.join(figdir, fn), **kw)

    M = bk.META
    cites = Cites(bk.REFS)
    bookkit.set_cite_resolver(cites.mark)
    doc = new_document()
    set_footer(doc, "急性期病院で学ぶ MBA シリーズ　%s　　" % M["title"])

    for _ in range(2):
        para(doc)
    para(doc, "急性期病院で学ぶ MBA シリーズ", size=12, bold=True, color=TEAL,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, M["series"], size=13, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, M["title"], size=22, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
    para(doc, "── %s ──" % M["sub"], size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc)
    para(doc, M["compose"], align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, M["extra"], align=WD_ALIGN_PARAGRAPH.CENTER)
    for _ in range(4):
        para(doc)
    para(doc, "作成日　%s" % M["date"], color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "静岡市立静岡病院　麻酔科　玉里順子", size=11.5, bold=True,
         color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

    para(doc, "目　次", size=16, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    toc_field(doc)

    n = {"fig": 0, "tbl": 0, "h2": 0}
    prev = None
    for b in bk.BLOCKS:
        k = b[0]
        if k == "h1":
            heading(doc, b[1], 1).paragraph_format.page_break_before = True
        elif k == "h2":
            h = heading(doc, b[1], 2)
            if str(b[1]).startswith("付録") and prev != "h1":
                h.paragraph_format.page_break_before = True
            n["h2"] += 1
        elif k == "h3":
            heading(doc, b[1], 3)
        elif k == "p":
            assert isinstance(b[1], str)
            para(doc, b[1])
        elif k == "ul":
            assert isinstance(b[1], list), b
            bullets(doc, b[1])
        elif k == "fig":
            p = os.path.join(figdir, b[1])
            if os.path.exists(p):
                figure(doc, p, b[2], width_cm=16.0)
                n["fig"] += 1
            else:
                print("!! 図版が無い:", b[1])
        elif k == "tbl":
            table(doc, b[1], b[2], b[3])
            n["tbl"] += 1
        elif k == "sum":
            assert isinstance(b[2], list), b
            summary(doc, b[1], b[2])
        elif k == "note":
            assert isinstance(b[2], list), b
            note(doc, b[1], b[2])
        elif k == "column":
            assert isinstance(b[3], list), b
            column(doc, b[1], b[2], b[3])
        else:
            print("!! 未知のブロック:", k)
        prev = k

    h = heading(doc, "参考文献", 2)
    h.paragraph_format.page_break_before = True
    reflist(doc, cites.rows())
    n["ref"] = len(cites.order)
    unused = sorted(set(bk.REFS) - set(cites.order))
    if unused:
        print("!! 本文で使っていない文献:", unused)

    drop_orphan_blanks(doc)
    out = os.path.join(OUTDIR, M["file"] + ".docx")
    doc.save(out)
    print(n, "->", os.path.abspath(out))
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    build(sys.argv[1])
