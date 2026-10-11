# -*- coding: utf-8 -*-
"""高度心臓血管麻酔　第Ⅷ章「心臓麻酔と神経モニタリング」docx を組む。"""
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
import cites8

import figwidths
import figmove
import abbr8
import c8_p1
import c8_p2

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "第Ⅷ章_心臓麻酔と神経モニタリング.docx")

META = {
    "book": "高度心臓血管麻酔",
    "chap": "第 Ⅷ 章",
    "audience": "麻酔科医・臨床工学技士・手術室看護師",
    "title": "心臓麻酔と神経モニタリング",
    "sub": "脳を見る機械と、そのときの麻酔",
    "compose": "脳波と処理脳波指数、近赤外線脳酸素、経頭蓋ドプラ、自動調節能、術中覚醒、せん妄と認知",
    "extra": "NAP5 / B-Aware / BAG-RECALL / BALANCED / ENGAGES・ENGAGES-Canada・"
             "MYRIAD / DECADE / Bottomline-CS 準拠",
    "date": "2026 年 9 月 17 日",
}

_RAW = list(c8_p1.BLOCKS) + list(c8_p2.BLOCKS)
BLOCKS, _UNUSED = citeapply.apply_blocks(_RAW, cites8.CITES)
if _UNUSED:
    print("!! 引用の対応が外れた文がある（本文を書き換えた？）:", sorted(_UNUSED))


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
    para(doc, "本章は、心臓手術の麻酔で使われる「脳のモニタ」と、"
              "そのときの麻酔の特徴を扱う。"
              "装置ごとの設定手順や、各社製品の仕様は扱わない。"
              "薬剤の具体的な投与量も書いていない。"
              "とくにトラネキサム酸は、投与量と腎機能によって"
              "けいれんのリスクが変わる。施設の基準を確認してほしい。")
    para(doc, "弓部手術に特化した脳保護は第Ⅱ章、"
              "脊髄保護と誘発電位は第Ⅲ章で扱った。"
              "本章はそれらと重なる数字を意図的に再掲している。"
              "重なっていること自体が、この主題の要点だからである。")
    para(doc, "引用した文献は、著者・雑誌・年・識別子まで確認できたものに限った。"
              "確認できなかった資料は付録 E に記録し、本文では使っていない。"
              "米国麻酔科学会の術中覚醒に関する practice advisory は"
              "2006 年版までしか確認できていない。")

    heading(doc, "本章で使う略語", 2)
    para(doc, "本文では、初出で「略語（英語表記：日本語表記）」の形に展開している。"
              "以下はその一覧である。")
    table(doc, None, abbr8.ABBREV[0], abbr8.ABBREV[1])

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
              "「Ⅷ_神経モニタリング」シートにある。")
    reflist(doc, cites.rows())
    n["ref"] = cites.count()

    drop_orphan_blanks(doc)
    doc.save(OUT)
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(build())
    print("saved:", os.path.abspath(OUT))
