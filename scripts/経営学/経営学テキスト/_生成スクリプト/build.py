# -*- coding: utf-8 -*-
"""『急性期病院で学ぶ MBAクリティカル・シンキング』docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH
import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     page_break, heading, toc_field, figure, table, bullets,
                     summary, note, column, reflist, NAVY, GREY, TEAL)

import refs
import p1, p2, p3, p4, p5, p6

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "急性期病院で学ぶ_MBAクリティカル・シンキング.docx")

META = {
    "book": "急性期病院で学ぶ MBA シリーズ",
    "audience": "病院の管理職・医療従事者",
    "title": "クリティカル・シンキング",
    "sub": "イシューから始めて、相手に届くまで",
    "compose": "グロービス経営大学院 6 日間の再構成と、独習のための補講",
    "extra": "全 31 章／図版 8 点／演習 5 題",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (list(p1.BLOCKS) + list(p2.BLOCKS) + list(p3.BLOCKS) +
          list(p4.BLOCKS) + list(p5.BLOCKS) + list(p6.BLOCKS))


def build():
    cites = refs.Cites()
    bookkit.set_cite_resolver(cites.mark)
    doc = new_document()
    set_footer(doc, "%s　%s　　" % (META["book"], META["title"]))

    # ---- 表紙
    for _ in range(2):
        para(doc)
    para(doc, META["book"], size=12, bold=True, color=TEAL,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, META["audience"], size=13, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, META["title"], size=22, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
    para(doc, "── %s ──" % META["sub"], size=12.5,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc)
    para(doc, META["compose"], align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, META["extra"], align=WD_ALIGN_PARAGRAPH.CENTER)
    for _ in range(4):
        para(doc)
    para(doc, "作成日　%s" % META["date"], color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "静岡市立静岡病院　麻酔科　玉里順子", size=11.5, bold=True,
         color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

    # ---- 目次
    para(doc, "目　次", size=16, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    toc_field(doc)

    # ---- 本文
    n = {"fig": 0, "tbl": 0, "sum": 0, "note": 0, "col": 0, "p": 0,
         "h1": 0, "h2": 0}
    prev = None
    for b in BLOCKS:
        k = b[0]
        if k == "h1":
            h = heading(doc, b[1], 1)
            h.paragraph_format.page_break_before = True
            n["h1"] += 1
        elif k == "h2":
            h = heading(doc, b[1], 2)
            # 章は流して組む。部の扉（h1）と付録だけ改ページする。
            if str(b[1]).startswith("付録") and prev != "h1":
                h.paragraph_format.page_break_before = True
            n["h2"] += 1
        elif k == "h3":
            heading(doc, b[1], 3)
        elif k == "p":
            para(doc, b[1])
            n["p"] += 1
        elif k == "ul":
            bullets(doc, b[1])
        elif k == "fig":
            p = os.path.join(FIGDIR, b[1])
            if os.path.exists(p):
                figure(doc, p, b[2], width_cm=16.0)
                n["fig"] += 1
            else:
                print("!! 図版が無い:", b[1])
        elif k == "tbl":
            table(doc, None, b[1], b[2])
            n["tbl"] += 1
        elif k in ("sum", "summary"):
            summary(doc, b[1], b[2])
            n["sum"] += 1
        elif k == "note":
            note(doc, b[1], b[2])
            n["note"] += 1
        elif k == "column":
            column(doc, b[1], b[2], b[3])
            n["col"] += 1
        else:
            print("!! 未知のブロック:", k)
        prev = k

    # ---- 参考文献
    h = heading(doc, "参考文献", 2)
    h.paragraph_format.page_break_before = True
    para(doc, "本文の肩付き番号は、この一覧の番号に対応する。"
              "掲載したものはすべて、2026 年 9 月 22 日に "
              "PubMed・Crossref・版元の書誌データベースで実在を確認した。"
              "確認できなかった資料は本文から外した。")
    reflist(doc, cites.rows())
    n["ref"] = cites.count()

    drop_orphan_blanks(doc)
    doc.save(OUT)
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(build())
    print("saved:", os.path.abspath(OUT))
