# -*- coding: utf-8 -*-
"""㊳ 産科麻酔　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr38
import refs38_extra
import refs38
import c38_p1
import c38_p2
import c38_p3

bookkit.REFS = dict(refs38.REFS)
bookkit.REFS.update(refs38_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "産科麻酔.docx")

META = {
    "no": "㊳",
    "vol": "38",
    "audience": "麻酔科専攻医・麻酔科医・産科医・助産師・手術室看護師",
    "title": "産科麻酔",
    "sub": "無痛分娩と帝王切開 ── 手技ではなく、体制で決まる",
    "compose": "妊婦という患者・無痛分娩・帝王切開・難しい妊婦・体制をつくる",
    "extra": "全22章／図版8点／コラム7本／参考文献35件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c38_p1.BLOCKS + c38_p2.BLOCKS + c38_p3.BLOCKS)


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
    para(doc, "産科", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、無痛分娩と帝王切開の麻酔である。"
              "産科麻酔には、ほかの領域にない前提がある ── "
              "患者が二人いて、その二人の利害がときどき食い違うこと。"
              "そして、麻酔科が単独で決められることが少ないことである。")
    para(doc, "手技そのものは硬膜外麻酔と脊髄くも膜下麻酔であり、"
              "麻酔科にとって特別に難しいものではない。"
              "しかし、いつ呼ばれるか、どこで導入するか、"
              "誰が見張るか、帝王切開へどう移るか、"
              "そして産科・助産師と同じ前提で話せているか ── "
              "この部分が揃っていなければ、手技は役に立たない。"
              "本書で段取りと体制の話が多くなるのは、そのためである。")
    para(doc, "本書は局所麻酔薬の種類・濃度・量、オピオイドの用量、"
              "昇圧薬の投与量、子宮収縮薬の用量と投与速度、"
              "血小板数の基準値、抗凝固薬の中断期間を本文に書いていない。"
              "薬剤・施設・症例で変わり、数字だけが一人歩きしやすいためである。"
              "何を書かなかったかは付録C-6に、"
              "施設で決めておくべき項目は付録Dにまとめた。")
    para(doc, "産科の大量出血そのものは㉒『常位胎盤早期剝離と産科危機的出血』が"
              "一冊で扱っており、本書では重複を避けた。"
              "脊髄幹麻酔の手技の基本は⑰『区域麻酔と脊髄幹麻酔』、"
              "局所麻酔薬中毒とアナフィラキシーは⑯、"
              "母体の心停止と蘇生は㉖、"
              "そして心疾患を合併した妊娠の生理は"
              "㊱『成人先天性心疾患の麻酔』が土台になる。")
    para(doc, "図版8点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録E）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr38.ABBREV[0], abbr38.ABBREV[1])

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
