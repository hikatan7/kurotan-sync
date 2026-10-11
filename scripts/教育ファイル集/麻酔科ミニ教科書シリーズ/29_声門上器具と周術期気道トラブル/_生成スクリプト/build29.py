# -*- coding: utf-8 -*-
"""㉙ 声門上器具と周術期気道トラブル　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     page_break, heading, toc_field, figure, table, bullets,
                     summary, note, column, NAVY, GREY, TEAL)

import abbr29
import c29_p1
import c29_p2
import c29_p3

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "声門上器具と周術期気道トラブル.docx")

META = {
    "no": "㉙",
    "vol": "29",
    "audience": "麻酔科医・研修医・手術室看護師",
    "title": "声門上器具と周術期気道トラブル",
    "sub": "声門の外側にとどまる器具を、どこまで信じるか",
    "compose": "解剖と病態生理から、喉頭痙攣とトラブルシューティングまで",
    "extra": "2025-JSA 抜管ガイドライン・DAS 2025・ASA 2022 を反映",
    "date": "2026 年 9 月 17 日",
}

BLOCKS = (c29_p1.BLOCKS + c29_p2.BLOCKS + c29_p3.BLOCKS)


def build():
    doc = new_document()
    set_footer(doc, "麻酔科ミニ教科書シリーズ %s　%s　　"
               % (META["no"], META["title"]))

    # ---- 表紙
    for _ in range(2):
        para(doc)
    para(doc, "麻酔科ミニ教科書シリーズ　%s" % META["no"], size=12, bold=True,
         color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "第 %s 巻" % META["vol"], size=11, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, META["audience"], size=13, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    # 大タイトルが 14 字を超えるので 2 行に分けて 30pt にする
    para(doc, "声門上器具と", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "周術期気道トラブル", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
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

    # ---- 前置き
    h = para(doc, "本書の立場と限界", size=14, bold=True, color=NAVY,
             space_after=6)
    h.paragraph_format.page_break_before = True
    para(doc, "声門上器具の選び方、サイズ、留置の確認法、抜去のタイミング ── "
              "このあたりは施設と麻酔科の方針によって実際が異なる。"
              "本書が示すのは一つの筋道であって、標準手順ではない。"
              "自施設の手順書と読み合わせて使ってほしい。")
    para(doc, "本書は製品名を書かない。世代交代が早く、数年で古くなるからである。"
              "咽頭リーク圧の具体的な数値と、喉頭痙攣に用いる薬剤の用量も書いていない。"
              "前者は器具と患者で大きく変わり、後者は施設の手順書と添付文書に"
              "従うべきものだからである。"
              "何を載せ、何を載せなかったかは付録Bに記録した。")
    para(doc, "土台にしたのは、院内教材『声門上器具と周術期気道トラブル』と、"
              "それを読み物にした10頁テキスト版である。"
              "図版四点はそこから引用し、残る二十二点は本書のために新しく作図した。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr29.ABBREV[0], abbr29.ABBREV[1])

    n = {"fig": 0, "tbl": 0, "sum": 0, "note": 0, "col": 0, "p": 0, "ch": 0}
    prev = None
    for b in BLOCKS:
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
                figure(doc, p, b[2])
                n["fig"] += 1
            else:
                print("!! missing figure:", b[1])
        elif k == "tbl":
            table(doc, None, b[1], b[2])
            n["tbl"] += 1
        elif k == "sum":
            summary(doc, b[1], b[2])
            n["sum"] += 1
        elif k == "note":
            note(doc, b[1], b[2])
            n["note"] += 1
        elif k == "col":
            column(doc, b[1], b[2], b[3])
            n["col"] += 1
        else:
            print("!! unknown block:", k)
        prev = k

    drop_orphan_blanks(doc)
    doc.save(OUT)
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(build())
    print("saved:", os.path.abspath(OUT))
