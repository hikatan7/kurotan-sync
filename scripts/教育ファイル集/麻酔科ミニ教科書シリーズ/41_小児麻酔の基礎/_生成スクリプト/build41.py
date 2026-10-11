# -*- coding: utf-8 -*-
"""㊶ 小児麻酔の基礎　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr41
import refs41_extra
import refs41
import c41_p1
import c41_p2
import c41_p3

bookkit.REFS = dict(refs41.REFS)
bookkit.REFS.update(refs41_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "小児麻酔の基礎.docx")

META = {
    "no": "㊶",
    "vol": "41",
    "audience": "麻酔科専攻医・麻酔科医・手術室看護師・小児にかかわる医師",
    "title": "小児麻酔の基礎",
    "sub": "小児は小さな大人ではない ── その中身",
    "compose": "何が違うのか・気道と呼吸・循環と輸液・麻酔の実際・難しい場面と体制",
    "extra": "全24章／図版9点／コラム6本／参考文献32件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c41_p1.BLOCKS + c41_p2.BLOCKS + c41_p3.BLOCKS)


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
    para(doc, "小児麻酔の", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "基礎", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、小児の麻酔の基礎である。"
              "「小児は小さな大人ではない」という言葉は古くからあるが、"
              "本書はその中身を具体的に書くことを目的にした。")
    para(doc, "違いは体の大きさではない。"
              "解剖・生理・薬物動態の三つが、それぞれ別の方向に違っている。"
              "気道の形が違うから体位と器具が変わり、"
              "呼吸の予備能が小さいから無呼吸に耐えられる時間が短く、"
              "一回拍出量を変えられないから徐脈がそのまま心拍出量の低下になる。"
              "そして体組成と臓器機能が違うから、"
              "体重で割った量がそのまま当てはまらない。")
    para(doc, "難しいのは、これらが同時に、"
              "しかも年齢によって違う重みで効いてくることである。"
              "だから「何歳の子か」は、"
              "麻酔計画を立てるうえで診断名と同じくらい重要な情報になる。"
              "施設ごとに体制は違う。自施設の取り決めと読み合わせて使ってほしい。")
    para(doc, "本書は薬剤の投与量、気管チューブのサイズと深さ、"
              "年齢ごとの血圧・心拍数の基準値、絶飲食の具体的な時間、"
              "輸液量、そして局所麻酔薬の上限量を本文に書いていない。"
              "年齢・体重・臓器機能・薬剤のどれか一つでも違えば変わる数字であり、"
              "数字だけが残ると危険だからである。"
              "何を書かなかったかは付録C-6に、"
              "施設で決めておくべき項目は付録Dにまとめた。"
              "自施設の基準と最新の指針を必ず確認すること。")
    para(doc, "気道管理の基本は⑬『気道管理』と"
              "㉙『声門上器具と周術期気道トラブル』が、"
              "手術室の外での鎮静の枠組みは㊵『手術室の外の鎮静』が、"
              "成人先天性心疾患は㊱が、"
              "そして悪性高熱症は㉗が扱っている。"
              "先天性心疾患の小児手術の麻酔、小児集中治療、新生児蘇生、"
              "そして症候群ごとの管理は本書の対象外である。")
    para(doc, "図版9点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録E）。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr41.ABBREV[0], abbr41.ABBREV[1])

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
