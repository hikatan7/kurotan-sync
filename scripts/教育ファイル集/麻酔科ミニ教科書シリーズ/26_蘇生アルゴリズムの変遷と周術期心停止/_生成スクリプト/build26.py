# -*- coding: utf-8 -*-
"""㉖ 蘇生アルゴリズムの変遷と周術期心停止　docx を組む。"""
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
import cites26
import abbr26
import c26_p1
import c26_p2
import c26_p3
import c26_p4

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "蘇生アルゴリズムの変遷と周術期心停止.docx")

META = {
    "no": "㉖",
    "vol": "26",
    "audience": "麻酔科医・集中治療医・看護師・臨床工学技士",
    "title": "蘇生アルゴリズムの変遷と周術期心停止",
    "sub": "ACLS の 60 年、院内迅速対応システム、開心術後の心停止",
    "compose": "ガイドラインの改訂史と、手術室・病棟・心臓外科 ICU の三つの現場",
    "extra": "AHA 2025／ERC 2025／JRC 2025・EACTS 2009・STS 2017 準拠",
    "date": "2026 年 9 月 17 日",
}

_RAW = (list(c26_p1.BLOCKS) + list(c26_p2.BLOCKS)
        + list(c26_p3.BLOCKS) + list(c26_p4.BLOCKS))
BLOCKS, _UNUSED = citeapply.apply_blocks(_RAW, cites26.CITES)
if _UNUSED:
    print("!! 引用の対応が外れた文がある:", sorted(_UNUSED))


def build():
    cites = citekit.Cites()
    bookkit.set_cite_resolver(cites.mark)
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
    para(doc, META["title"], size=24, bold=True, color=NAVY,
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

    # ---- 前置き
    h = para(doc, "本書の立場と限界", size=14, bold=True, color=NAVY,
             space_after=6)
    h.paragraph_format.page_break_before = True
    para(doc, "扱う内容は、施設の規模・体制・使用している機器や薬剤によって"
              "実際の手順が異なる。本書が示すのは一つの筋道であり、"
              "そのまま当てはまらない場面がある。"
              "自施設の手順書と読み合わせて使ってほしい。")
    para(doc, "本書に出てくる発生率・生存率は、"
              "原著によって分子と分母の定義が違う。"
              "比較するときは、必ず定義から読むこと。"
              "薬剤の用量は、最新の添付文書と施設の基準に従うこと。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr26.ABBREV[0], abbr26.ABBREV[1])

    n = {"fig": 0, "tbl": 0, "sum": 0, "note": 0, "p": 0, "ch": 0}
    prev = None
    for b in BLOCKS:
        k = b[0]
        if k == "h1":
            hh = heading(doc, b[1], 1)
            hh.paragraph_format.page_break_before = True
        elif k == "h2":
            hh = heading(doc, b[1], 2)
            n["ch"] += 1
            # 「付録」の見出し直後に来る付録Aで改ページすると、
            # 部扉だけのページができる。直前が h1 のときは入れない。
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
        else:
            print("!! unknown block:", k)
        prev = k

    h = heading(doc, "参考文献", 2)
    h.paragraph_format.page_break_before = True
    para(doc, "本文の肩付き番号は、この一覧の番号に対応する。"
              "すべて PubMed 識別子（PMID）と DOI を確認した。"
              "台帳は同じフォルダの"
              "『蘇生アルゴリズム_SourceLedger.xlsx』にある。")
    para(doc, "1974 年・1980 年・1986 年版の本文、"
              "日本麻酔科学会『術中心停止に対するプラクティカルガイド』、"
              "日本集中治療医学会の RRS 運用指針、"
              "JRC 蘇生ガイドライン 2025 の書籍版、"
              "および院内資料については、"
              "PubMed 上で一次情報を確認できていない。"
              "本文では、確認できた資料に基づく範囲で記述している"
              "（付録 C-3）。")
    reflist(doc, cites.rows())
    n["ref"] = cites.count()

    drop_orphan_blanks(doc)
    doc.save(OUT)
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(build())
    print("saved:", os.path.abspath(OUT))
