# -*- coding: utf-8 -*-
"""㉞ 心臓麻酔の緊急と補助循環　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr36
import refs36_extra
import refs36
import c36_p1
import c36_p2
import c36_p3

bookkit.REFS = dict(refs36.REFS)
bookkit.REFS.update(refs36_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "成人先天性心疾患の麻酔.docx")

META = {
    "no": "㊱",
    "vol": "36",
    "audience": "麻酔科専攻医・麻酔科医・集中治療医・手術室看護師",
    "title": "成人先天性心疾患の麻酔",
    "sub": "病名では決まらない ── 生理で分類して、守るものを決める",
    "compose": "考え方の土台・生理を読む・麻酔の実際・場面別・支える",
    "extra": "全23章／図版7点／コラム7本／参考文献32件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c36_p1.BLOCKS + c36_p2.BLOCKS + c36_p3.BLOCKS)


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
    para(doc, META["audience"], size=12, color=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "成人先天性心疾患の", size=28, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "麻酔", size=30, bold=True, color=NAVY,
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

    # ---- 目次
    h = para(doc, "目　次", size=16, bold=True, color=NAVY,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    h.paragraph_format.page_break_before = True
    toc_field(doc)

    # ---- 前置き
    h = para(doc, "本書の立場と限界", size=14, bold=True, color=NAVY,
             space_after=6)
    h.paragraph_format.page_break_before = True
    para(doc, "本書が扱うのは、成人になった先天性心疾患の患者の麻酔である。"
              "そして麻酔科がこの人たちに出会う機会の大半は、"
              "心臓の手術ではない ── "
              "虫垂炎、胆嚢摘出、整形外科の手術、内視鏡、歯科治療、帝王切開。"
              "つまり「この患者でなければ何も考えずに済む手術」である。")
    para(doc, "この領域の難しさは、病名では麻酔が決まらないことにある。"
              "同じ病名でも、手術の時期と術式でいまの循環はまったく違う。"
              "だから本書は、病名ではなく生理で分類する道具を用意した ── "
              "シャント、狭窄、単心室・Fontan、体心室が右室。"
              "この四つで、守るべきものがほぼ決まる。"
              "施設ごとに体制は違う。自施設の取り決めと読み合わせて使ってほしい。")
    para(doc, "本書は目標とする血圧・心拍数・酸素飽和度、換気の設定値、"
              "抗凝固の中断期間、そして薬剤の投与量を本文に書いていない。"
              "病態・患者・施設で変わるためであり、"
              "とくに ACHD では「普段の値」が患者ごとに違うため、"
              "一般化した数値は誤解を招きやすい。"
              "何を書かなかったかは付録D-4に、"
              "施設で決めておくべき項目は付録Eにまとめた。"
              "情報が足りないときにも実行できる原則は、付録Cにまとめた。")
    para(doc, "土台となる心臓麻酔の基礎 ── 弁膜症の血行動態、TEE、"
              "人工心肺の生理 ── は㉝『心臓麻酔の基礎』が、"
              "右心不全と補助循環は㉞『心臓麻酔の緊急と補助循環』が、"
              "止血と輸血は㉛『心臓麻酔の止血戦略』が扱っている。"
              "本書はその隣に「循環そのものが通常と違う患者」を置く巻である。")
    para(doc, "図版7点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録F）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr36.ABBREV[0], abbr36.ABBREV[1])

    n = {"fig": 0, "tbl": 0, "sum": 0, "note": 0, "col": 0, "p": 0,
         "ch": 0, "ul": 0}
    col_no = [0]
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
            n["ul"] += 1
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
            col_no[0] += 1
            column(doc, col_no[0], b[2], b[3])
            n["col"] += 1
        elif k == "refs":
            n["refs"] = references(doc)
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
