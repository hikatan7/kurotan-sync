# -*- coding: utf-8 -*-
"""〔53〕ステロイドホルモン　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr53
import refs53
import c53_p1
import c53_p2
import c53_p3
import c53_p4
import volno

bookkit.REFS = dict(refs53.REFS)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "ステロイドホルモン.docx")

META = {
    "no": volno.circled(53),
    "vol": "53",
    "audience": "麻酔科専攻医・麻酔科医・集中治療医・手術室看護師",
    "title": "ステロイドホルモン",
    "sub": "補う量、抑える量、叩く量",
    "compose": "基礎・補充・周術期の使い方・集中治療とパルス療法・アレルギーとアナフィラキシー",
    "extra": "全5部21章／図版8点／コラム4本／参考文献99件",
    "date": "2026 年 10 月 7 日",
}

_END = next(i for i, b in enumerate(c53_p3.BLOCKS)
            if b[0] == "h2" and b[1].startswith("おわりに"))
BLOCKS = (c53_p1.BLOCKS + c53_p2.BLOCKS + c53_p3.BLOCKS[:_END]
          + c53_p4.BLOCKS + c53_p3.BLOCKS[_END:])


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
    para(doc, "ステロイド", size=26, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "ホルモン", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、副腎皮質ステロイド（糖質コルチコイド）である ── "
              "体が作るコルチゾールの生理、薬としてのステロイドの効き方、副腎不全の補充療法、"
              "周術期のステロイドカバーとデキサメタゾンの使い方、集中治療での低用量療法、そしてパルス療法。")
    para(doc, "全体を「量」の一本の筋でつないだ。"
              "ステロイドは、副腎が作れない分を足す「補う量」、炎症と免疫を抑える「抑える量」、"
              "臓器を脅かす炎症を数日で抑え込む「叩く量」とで、目的も危険もまったく違う。"
              "第I部で体の中のステロイドと薬の性質を押さえ（基礎）、第II部で補う量を（補充とやめ方）、"
              "第III部で周術期に麻酔科医が決める量を、第IV部で集中治療とパルス療法の量を扱う。"
              "第V部では、アナフィラキシーとアレルギーの場面でのステロイドを、できることとできないことに分けて整理した。")
    para(doc, "この巻では用量を具体的に書いた。"
              "周術期のカバーやクリーゼの初期治療は、迷う時間そのものが危険になる場面だからである。"
              "ただし、ガイドラインの多くは観察研究と専門家の合意に基づいており、"
              "同じ問いに国や学会で違う答えがあるところは、その違いをそのまま示した。"
              "実際の投与量は、患者の状態と施設の取り決めに合わせて決めてほしい。")
    para(doc, "副腎不全の内分泌学的な診断と長期管理は本書の範囲を超えるので、要点だけにとどめた。"
              "アナフィラキシーの診断と初期対応の全体は⑯と周術期アナフィラキシー統合ガイドに、"
              "敗血症の循環管理は⑲に、気道浮腫と抜管は㊻に置いた。")
    para(doc, "図版 8 点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、巻末に番号順の参考文献一覧を置いた。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr53.ABBREV[0], abbr53.ABBREV[1])

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
