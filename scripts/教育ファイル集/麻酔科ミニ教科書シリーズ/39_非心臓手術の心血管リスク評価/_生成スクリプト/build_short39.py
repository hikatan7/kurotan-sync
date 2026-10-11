# -*- coding: utf-8 -*-
"""㊴ 専攻医向け要約テキスト（10頁）を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import shortfix
import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, figure, table, bullets, summary, note, lead,
                     references, NAVY, GREY, TEAL)

import refs39
import refs39_extra
import c39_short

bookkit.REFS = dict(refs39.REFS)
bookkit.REFS.update(refs39_extra.EXTRA)
bookkit.CITES = bookkit._Cites()          # 本編とは別に採番する

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "非心臓手術の心血管リスク評価_専攻医版.docx")

TITLE = "非心臓手術の心血管リスク評価　専攻医版"


def build():
    doc = new_document()
    set_footer(doc, "麻酔科ミニ教科書シリーズ ㊴　別冊　%s　　" % TITLE)

    para(doc, "麻酔科ミニ教科書シリーズ ㊴　別冊", size=11, bold=True,
         color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    para(doc, "非心臓手術の心血管リスク評価　── 専攻医版 ──", size=15, bold=True,
         color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    para(doc, "その検査・その薬で、何が変わるのか",
         size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "2026 年 9 月 22 日　静岡市立静岡病院　麻酔科　玉里順子",
         size=10, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    n = {"fig": 0, "tbl": 0, "p": 0, "sec": 0}
    for b in shortfix.prepare(c39_short.BLOCKS, HERE):
        k = b[0]
        if k == "h2":
            heading(doc, b[1], 2)
            n["sec"] += 1
        elif k == "h3":
            heading(doc, b[1], 3)
        elif k == "p":
            para(doc, b[1])
            n["p"] += 1
        elif k == "lead":
            lead(doc, b[1])
        elif k == "ul":
            bullets(doc, b[1])
        elif k == "fig":
            p = shortfix.figpath(FIGDIR, b[1])
            if os.path.exists(p):
                figure(doc, p, b[2], width_cm=16.0)
                n["fig"] += 1
            else:
                print("!! missing figure:", b[1])
        elif k == "tbl":
            table(doc, None, b[1], b[2], size=(9.5 if len(b[1]) <= 4 else 9.0))
            n["tbl"] += 1
        elif k == "sum":
            summary(doc, b[1], b[2])
        elif k == "note":
            note(doc, b[1], b[2])
        elif k == "refs":
            n["refs"] = references(doc, size=9.0)
        else:
            print("!! unknown block:", k)

    drop_orphan_blanks(doc)
    doc.save(OUT)
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(build())
    print("saved:", os.path.abspath(OUT))
