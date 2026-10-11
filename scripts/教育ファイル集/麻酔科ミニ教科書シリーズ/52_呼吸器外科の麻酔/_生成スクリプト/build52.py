# -*- coding: utf-8 -*-
"""〔52〕呼吸器外科の麻酔　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr52
import refs52
import c52_p1
import c52_p2
import c52_p3
import volno

bookkit.REFS = dict(refs52.REFS)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "呼吸器外科の麻酔.docx")

META = {
    "no": volno.circled(52),
    "vol": "52",
    "audience": "麻酔科専攻医・麻酔科医・呼吸器外科医・手術室看護師",
    "title": "呼吸器外科の麻酔",
    "sub": "切る前に、残る肺を見積もる",
    "compose": "術前評価・肺分離・片肺換気・術式・鎮痛と回復・合併症と危機",
    "extra": "全6部25章／図版15点／コラム7本／参考文献55件",
    "date": "2026 年 9 月 24 日",
}

BLOCKS = (c52_p1.BLOCKS + c52_p2.BLOCKS + c52_p3.BLOCKS)


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
    para(doc, "呼吸器外科の", size=26, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、肺切除を中心とする呼吸器外科手術の麻酔である ── "
              "術前評価、肺分離、片肺換気、術式ごとの管理、術後鎮痛と早期回復、そして周術期の合併症と危機。")
    para(doc, "全体を一本の筋でつないだ。"
              "術前に「切ったあとに残る肺と心臓で、術後を乗り切れるか」を見積もり（第I部）、"
              "肺を確実に分け（第II部）、分けた肺をなるべく傷めずに換気し（第III部）、"
              "術式ごとに変わる重心に備え（第IV部）、咳と深呼吸を支える鎮痛で回復させ（第V部）、"
              "起きうる危機に順番を持って対応する（第VI部）。")
    para(doc, "この巻では数値を多く書いた。"
              "呼吸機能の区分、運動試験の参考値、片肺換気の一回換気量、禁煙の期間 ── "
              "いずれもガイドラインと一次研究から出典を付けて示している。"
              "ただし、ほとんどの数値はエビデンスの確実性が低く、"
              "2025 年の欧州の指針自身が「特定の閾値を推奨することはできない」と書いている。"
              "本書の数値は「線」ではなく「分かれ道」として読んでほしい。"
              "とくに片肺換気の設定は、2026 年の大規模試験（PROTHOR）を受けて、"
              "固定の処方箋ではなく、患者ごとに決める手順として書いた（第9章）。")
    para(doc, "本書は、ユーザーが用意した原案（生成 AI による項目立てと本文案）を土台にしている。"
              "原案の文献と数値はすべて原典と照合し、確認できなかったもの・誤っていたものは修正した。"
              "その記録を付録Bに残した。")
    para(doc, "片肺換気の生理と人工呼吸の基礎は⑱『呼吸管理と分離肺換気』に、"
              "区域麻酔の手技は⑰と㊽に、危機的出血と輸血は㉑・㉛・③に置いた。"
              "本書はそれらを呼吸器外科の手術室で使う形にまとめ直したものである。"
              "施設で決めておきたい事柄は付録Cにまとめた。")
    para(doc, "図版 15 点のうち 13 点は本書のために作図し、2 点は⑱から再掲した。"
              "本文の記述には出現順の肩付き番号を付し、巻末に番号順の参考文献一覧を置いた。"
              "引用した 55 件は、PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr52.ABBREV[0], abbr52.ABBREV[1])

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
