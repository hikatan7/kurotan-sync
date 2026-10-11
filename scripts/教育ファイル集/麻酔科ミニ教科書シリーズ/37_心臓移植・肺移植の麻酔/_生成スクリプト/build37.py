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

import abbr37
import refs37_extra
import refs37
import c37_p1
import c37_p2
import c37_p3

bookkit.REFS = dict(refs37.REFS)
bookkit.REFS.update(refs37_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "心臓移植・肺移植の麻酔.docx")

META = {
    "no": "㊲",
    "vol": "37",
    "audience": "麻酔科専攻医・麻酔科医・集中治療医・臨床工学技士・手術室看護師",
    "title": "心臓移植・肺移植の麻酔",
    "sub": "臓器が働き始めるところまでが、麻酔の仕事である",
    "compose": "移植という枠組み・心臓移植・肺移植・共通の問題・移植のあと",
    "extra": "全21章／図版7点／コラム6本／参考文献37件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c37_p1.BLOCKS + c37_p2.BLOCKS + c37_p3.BLOCKS)


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
    para(doc, "心臓移植・肺移植の", size=27, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、心臓移植と肺移植の麻酔である。"
              "この麻酔には、ほかの手術にない三つの特徴がある ── "
              "患者が二人いること、"
              "時間が外から決められていること、"
              "そして臓器が働き始めるところまでが麻酔の仕事であること。")
    para(doc, "臓器は違っても、"
              "「重症の患者に、他人の臓器を入れて、働かせる」という構造は同じである。"
              "だから心臓移植と肺移植を一冊にまとめた。"
              "施設ごとに体制は違う。自施設の取り決めと読み合わせて使ってほしい。")
    para(doc, "そして、実際に移植を行う施設は限られている。"
              "本書の読者の多くが関わるのは、"
              "むしろ「移植を受けた患者が、何年か経って別の手術を受けにくる」場面だろう。"
              "第18章がその場面を扱っている。"
              "その人の心臓が神経とつながっていないこと、"
              "肺が咳をできないこと、"
              "免疫抑制を止められないことを知っているかどうかで、"
              "麻酔の設計は変わる。")
    para(doc, "本書は目標とする血圧・心拍数・肺動脈圧、換気の設定値、"
              "阻血時間の許容範囲、免疫抑制薬の用量と目標血中濃度、"
              "そして薬剤の投与量を本文に書いていない。"
              "臓器・施設・症例で変わり、数字だけが一人歩きしやすいためである。"
              "何を書かなかったかは付録C-6に、"
              "施設で決めておくべき項目は付録Dにまとめた。")
    para(doc, "本書は心臓麻酔の巻立ての最後に置かれている。"
              "土台は㉝『心臓麻酔の基礎』、止血は㉛『心臓麻酔の止血戦略』、"
              "補助循環は㉞『心臓麻酔の緊急と補助循環』、"
              "分離肺換気は㉟『低侵襲・ロボット心臓手術の麻酔』、"
              "そして重症心不全に至る手前は㊱『成人先天性心疾患の麻酔』が扱っている。"
              "各巻との関係は第21章にまとめた。")
    para(doc, "図版7点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録E）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr37.ABBREV[0], abbr37.ABBREV[1])

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
