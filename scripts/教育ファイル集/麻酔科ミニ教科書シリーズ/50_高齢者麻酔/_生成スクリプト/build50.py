# -*- coding: utf-8 -*-
"""㊸ 高齢者麻酔　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr50
import refs50_extra
import refs50
import c50_p1
import c50_p2
import volno

bookkit.REFS = dict(refs50.REFS)
bookkit.REFS.update(refs50_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "高齢者麻酔.docx")

META = {
    "no": volno.circled(50),
    "vol": "50",
    "audience": "麻酔科専攻医・麻酔科医・病棟/手術室看護師",
    "title": "高齢者麻酔",
    "sub": "年齢ではなく、予備能で評価する",
    "compose": "高齢という状態・脳を守る・術中管理・前後をつなぐ",
    "extra": "全18章／図版6点／コラム2本／参考文献15件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c50_p1.BLOCKS + c50_p2.BLOCKS)


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
    para(doc, "高齢者", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、高齢者の周術期管理である。")
    para(doc, "最初に断っておくべきことがある ── "
              "年齢そのものは、ほとんど何も教えてくれない。"
              "同じ年齢の二人が、まったく違う予備能を持っている。"
              "一方は自分で歩いて外来に来て、もう一方は施設から車椅子で来る。"
              "この差を年齢は説明しない。"
              "だから高齢者の麻酔の第一歩は、"
              "年齢を評価の代わりに使うのをやめることである。")
    para(doc, "加齢による変化は「全体に弱くなる」という一様なものでもない。"
              "臓器ごとに減り方が違い、どこが先に破綻するかが人によって違う。"
              "循環が先に破綻する患者と、呼吸が先に破綻する患者では、"
              "準備する手が違う ── "
              "本書が第2章に表を置いたのは、"
              "「どの列が最も細いか」を患者ごとに見積もるためである。")
    para(doc, "第II部は術後せん妄に充てた。"
              "高齢者の周術期で最も頻度が高く、最も予防の余地がある問題だからである。"
              "そして予防について現在最も確かな結論は、"
              "多因子の非薬物的な介入が効く、というものである ── "
              "眼鏡と補聴器、昼夜のリズム、早期離床、脱水と痛みを取ること。"
              "内容は地味で、しかもその多くは手術室の外で行われる。"
              "「麻酔深度を浅くすれば防げる」「区域麻酔にすれば防げる」という"
              "自然な期待は、いずれも大規模な無作為化試験で"
              "明快な支持を得ていない（第8・9章）。")
    para(doc, "本書は薬剤名・用量・目標値を書かない。"
              "フレイルとせん妄の評価尺度の具体も書いていない ── "
              "尺度は数多くあり、どれを使うかで結果が変わるためである。"
              "何を書かなかったかは付録Cに、"
              "施設で決めておきたい事柄は付録Dにまとめた。")
    para(doc, "最後の第18章には「手術をしないという選択肢」を置いた。"
              "ここまでの十七章が、すべて「手術をする」という前提の上に立っているからである。"
              "その前提を一度疑う場所を、本の中に置いておきたかった。"
              "麻酔科がこの判断を下すわけではないが、"
              "手術に耐えられるかを評価する立場にあり、"
              "術前外来は患者本人が何を望んでいるかを聞ける数少ない場でもある。")
    para(doc, "図版6点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した15件は、"
              "PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr50.ABBREV[0], abbr50.ABBREV[1])

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
