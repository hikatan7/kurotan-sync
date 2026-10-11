# -*- coding: utf-8 -*-
"""高度心臓血管麻酔　第Ⅶ章「人工心肺・出血と輸血・循環の目標」docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH
import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     page_break, heading, toc_field, figure, table, bullets,
                     summary, note, reflist, NAVY, GREY, TEAL)

import citeapply
import citekit
import cites7
import figwidths
import figmove
import abbr7
import c7_p1
import c7_p2

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "第Ⅶ章_人工心肺・出血と輸血・循環の目標.docx")

META = {
    "book": "高度心臓血管麻酔",
    "chap": "第 Ⅶ 章",
    "audience": "麻酔科医・臨床工学技士・手術室看護師",
    "title": "人工心肺・出血と輸血・循環の目標",
    "sub": "測れることと、転帰が変わること",
    "compose": "人工心肺、患者血液管理、輸血閾値、低血圧、離脱困難、そして全章の総括",
    "extra": "2024 EACTS/EACTAIC/EBCP 人工心肺・患者血液管理ガイドライン・"
             "TRICS III / ATACAS / PrevAKI 準拠",
    "date": "2026 年 9 月 17 日",
}

_RAW = list(c7_p1.BLOCKS) + list(c7_p2.BLOCKS)
BLOCKS, _UNUSED = citeapply.apply_blocks(_RAW, cites7.CITES)
if _UNUSED:
    print("!! 引用の対応が外れた文がある:", sorted(_UNUSED))


def build():
    cites = citekit.Cites()
    bookkit.set_cite_resolver(cites.mark)
    doc = new_document()
    set_footer(doc, "%s　%s　%s　　" % (META["book"], META["chap"], META["title"]))

    for _ in range(2):
        para(doc)
    para(doc, META["book"], size=12, bold=True, color=TEAL,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, META["chap"], size=11, color=GREY,
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

    para(doc, "目　次", size=16, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    toc_field(doc)

    h = para(doc, "本書の立場と限界", size=14, bold=True, color=NAVY,
             space_after=6)
    h.paragraph_format.page_break_before = True
    para(doc, "人工心肺の運転そのもの（回路構成・充填量・流量計算）は"
              "臨床工学技士の領分である。"
              "本章では、麻酔科が判断に関わる範囲に限って扱う。"
              "薬剤の具体的な投与量は書いていない。"
              "とくにトラネキサム酸は、投与量と腎機能によって"
              "けいれんのリスクが変わる。施設の基準を確認してほしい。")
    para(doc, "本章は本書の最終章であり、"
              "第Ⅰ章から第Ⅵ章で扱った主題を横断してまとめている。"
              "各章の詳細は、それぞれの章に戻って確認してほしい。")
    para(doc, "引用した文献は、著者・雑誌・年・識別子まで確認できたものに限った。"
              "人工心肺と患者血液管理のガイドラインは、"
              "2024 年版として策定され 2025 年に各誌へ同時掲載されている。"
              "引用の年号を書くときは注意が要る。")

    heading(doc, "本章で使う略語", 2)
    para(doc, "本文では、初出で「略語（英語表記：日本語表記）」の形に展開している。"
              "以下はその一覧である。")
    table(doc, None, abbr7.ABBREV[0], abbr7.ABBREV[1])

    n = {"fig": 0, "tbl": 0, "sum": 0, "note": 0, "p": 0, "ch": 0}
    prev = None
    for b in figmove.reorder(BLOCKS):
        k = b[0]
        if k == "h1":
            hh = heading(doc, b[1], 1)
            hh.paragraph_format.page_break_before = True
        elif k == "h2":
            hh = heading(doc, b[1], 2)
            n["ch"] += 1
            if str(b[1]).startswith(("付録", "おわりに")) and prev != "h1":
                hh.paragraph_format.page_break_before = True
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
                figure(doc, p, b[2], width_cm=figwidths.W.get(b[1], 16.0))
                n["fig"] += 1
            else:
                print("!! missing figure:", b[1])
        elif k == "tbl":
            table(doc, None, b[1], b[2])
            n["tbl"] += 1
        elif k in ("sum", "summary"):
            summary(doc, b[1], b[2])
            n["sum"] += 1
        elif k == "note":
            note(doc, b[1], b[2])
            n["note"] += 1
        else:
            print("!! unknown block:", k)
        prev = k

    h = heading(doc, "参考文献", 2)
    h.paragraph_format.page_break_before = True
    para(doc, "本文の肩付き番号は、この一覧の番号に対応する。"
              "すべて PubMed 識別子（PMID）と DOI を確認した。"
              "台帳は『高度心臓血管麻酔_SourceLedger_v1.xlsx』の"
              "「Ⅶ_横断（CPB・PBM・TEE）」シートにある。")
    reflist(doc, cites.rows())
    n["ref"] = cites.count()

    drop_orphan_blanks(doc)
    doc.save(OUT)
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(build())
    print("saved:", os.path.abspath(OUT))
