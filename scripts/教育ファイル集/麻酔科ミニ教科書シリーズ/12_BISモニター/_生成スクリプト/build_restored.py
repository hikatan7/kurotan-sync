# -*- coding: utf-8 -*-
"""PDF から戻した本文を、㉒と同じ体裁の docx に組む。

  ・表紙と目次は㉒と同じ書式で作り直す
  ・Take Home → 章末の「この章のまとめ」
  ・Pitfall ほかの小枠 → 本文中の「◆ 注意書き」
  ・Column / History → コラム（出現順に採番し、目次に載せる）
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = (r"C:\Users\junch\OneDrive\_旧デスクトップ\教育ファイル集"
       r"\麻酔科ミニ教科書シリーズ\22_常位胎盤早期剝離と産科危機的出血\_生成スクリプト")
sys.path.insert(0, KIT)
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     page_break, heading, toc_field, figure, boxed, column,
                     table, bullets, lead, summary, note,
                     NAVY, GREY, TEAL, BLUE)
import pdf2blocks

# コラムとして目次に載せる枠
AS_COLUMN = {"Column", "History", "コラム"}
# 枠のまま残すもの
AS_EV = {"Evidence"}


def rebuild(blocks, summaries):
    """章末まとめ・注意書き・コラム番号を整える。"""
    out = []
    col_no = 0
    buf = []
    cur = None

    def flush():
        nonlocal buf
        if cur and (buf or cur in summaries):
            lines = summaries.get(cur) or buf
            out.append(("sum", "この章のまとめ", list(lines)))
        buf = []

    for b in blocks:
        k = b[0]
        if k in ("h1", "h2"):
            flush()
            if k == "h2":
                cur = re.sub(r"\s+", "", b[1])
            out.append(b)
            continue
        if k == "th":
            buf.extend(b[2])
            continue
        if k == "pf":
            out.append(("note", b[1], b[2]))
            continue
        if k == "ev":
            out.append(("ev", b[1], b[2]))
            continue
        if k == "colx":
            tag, title, lines = b[1], b[2], b[3]
            if tag in AS_COLUMN:
                col_no += 1
                out.append(("col", col_no, title or tag, lines))
            elif tag in AS_EV:
                out.append(("ev", title or tag, lines))
            else:
                out.append(("note", title or tag, lines))
            continue
        out.append(b)
    flush()
    return out


def build(meta, blocks, figdir, out_path):
    doc = new_document()
    set_footer(doc, "麻酔科ミニ教科書シリーズ %s　%s　　"
               % (meta["no"], meta["title"]))

    # ---- 表紙
    for _ in range(2):
        para(doc)
    para(doc, "麻酔科ミニ教科書シリーズ　%s" % meta["no"], size=12, bold=True,
         color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "第 %s 巻" % meta["vol"], size=11, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, meta["audience"], size=13, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, meta["title"], size=24, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
    para(doc, "── %s ──" % meta["sub"], size=12.5,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc)
    para(doc, meta["compose"], align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, meta["extra"], align=WD_ALIGN_PARAGRAPH.CENTER)
    for _ in range(4):
        para(doc)
    para(doc, "作成日　%s" % meta["date"], color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "静岡市立静岡病院　麻酔科　玉里順子", size=11.5, bold=True,
         color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

    # ---- 目次
    para(doc, "目　次", size=16, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    toc_field(doc)

    # ---- 前置き
    _h = para(doc, "本書の立場と限界", size=14, bold=True, color=NAVY,
              space_after=6)
    _h.paragraph_format.page_break_before = True
    para(doc, "扱う内容は、施設の規模・体制・使用している機器や製剤によって"
              "実際の手順が異なる。本書が示すのは一つの筋道であり、"
              "そのまま当てはまらない場面がある。"
              "自施設の手順書と読み合わせて使ってほしい。")
    para(doc, "数値は「スイッチ」ではなく「境界」として読む。"
              "薬剤の用量や機器の設定値は、最新の添付文書と施設の基準に従うこと。")

    n = {"fig": 0, "tbl": 0, "col": 0, "sum": 0}
    prev = None
    for b in blocks:
        k = b[0]
        if k == "h1":
            h = heading(doc, b[1], 1)
            h.paragraph_format.page_break_before = True
        elif k == "h2":
            h = heading(doc, b[1], 2)
            if str(b[1]).startswith("付録") and prev != "h1":
                h.paragraph_format.page_break_before = True
        elif k == "h3":
            heading(doc, b[1], 3)
        elif k == "p":
            para(doc, b[1])
        elif k == "ul":
            bullets(doc, b[1])
        elif k == "fig":
            p = os.path.join(figdir, b[1])
            if os.path.exists(p):
                figure(doc, p, b[2]); n["fig"] += 1
        elif k == "tbl":
            table(doc, None, b[1], b[2]); n["tbl"] += 1
        elif k == "sum":
            summary(doc, b[1], b[2]); n["sum"] += 1
        elif k == "note":
            note(doc, b[1], b[2])
        elif k == "ev":
            boxed(doc, "Evidence", b[1], b[2], BLUE, "EDF2F9", "174682")
        elif k == "col":
            column(doc, b[1], b[2], b[3]); n["col"] += 1
        prev = k

    drop_orphan_blanks(doc)
    doc.save(out_path)
    return n
