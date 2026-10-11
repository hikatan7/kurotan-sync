# -*- coding: utf-8 -*-
"""㊸ 周術期生理学　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr45
import refs45_extra
import refs45
import c45_p1
import c45_p2
import c45_p2b
import c45_p3
import volno

bookkit.REFS = dict(refs45.REFS)
bookkit.REFS.update(refs45_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "周術期生理学.docx")

META = {
    "no": volno.circled(45),
    "vol": "45",
    "audience": "麻酔科専攻医・麻酔科医・臨床工学技士",
    "title": "周術期生理学",
    "sub": "麻酔がかかった体で、何がずれるのか",
    "compose": "麻酔がかかった体・循環・呼吸・腎と脳と体温と臓器の事情・まとめ",
    "extra": "全23章／図版8点／コラム6本／参考文献18件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c45_p1.BLOCKS + c45_p2.BLOCKS + c45_p2b.BLOCKS + c45_p3.BLOCKS)


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
    para(doc, "周術期", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "生理学", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、麻酔がかかった体で何がずれるのか、である。")
    para(doc, "麻酔の教科書は、たいてい薬から始まる。"
              "その順番で学ぶと、麻酔が「体の働きを止めるもの」のように見えてくる。"
              "しかし実際には、止まるものはほとんどない。"
              "心臓は拍ち続け、腎は濾過を続け、血管は収縮と拡張を続けている。"
              "変わるのは、それらを調節している仕組みの利き具合と作動点である ── "
              "止まるのではなく、ずれる。")
    para(doc, "この見方が実務で効くのは、"
              "「いま目の前で起きていることは、どの調節が外れた結果か」"
              "という問いを立てられるからである。"
              "血圧が下がったのは血管が開いたからなのか、反射が働かないからなのか。"
              "体温が下がったのは熱が逃げているからなのか、"
              "体の中で熱が移っただけなのか。"
              "原因の場所が違えば、打つ手も違う。")
    para(doc, "本書には、繰り返し現れる形がいくつかある ── "
              "圧と流れは別のものであること、"
              "決めているのはしばしば末梢であること、"
              "供給と需要で見ること、"
              "測っている場所と起きている場所は違うこと、"
              "そして時間には向きがあること。"
              "これらは知識というより読み方であり、"
              "読み方であるからこそ、指針が改訂されても薬が入れ替わっても古びない。"
              "本書が半世紀前の文献を臆せず引いたのは、そのためである。")
    para(doc, "本書は数値を書かない ── 正常値も、目標値も、閾値も。"
              "生理の教科書に載っている数値の多くは、"
              "健康な若年成人を覚醒した状態で安静仰臥位で測ったものであり、"
              "麻酔がかかり陽圧換気がかかり体位が変わり侵襲が加わっている体は、"
              "その条件をどれ一つ満たしていない。"
              "覚えるべきなのは値ではなく、どちらへ、なぜ動くかである。")
    para(doc, "各論は既刊に置いた。"
              "循環は⑲と㉝が、輸液は①②が、呼吸は⑱と㉚が、"
              "腎は㉓と㉘が、脳は㉜が、体温は㊸と㊷が扱っている。"
              "対応は付録Bの表にまとめた。"
              "本書は㊹『麻酔科医の臨床推論』と対になっている ── "
              "あちらが「どう考えるか」、本書が「なぜそうなるか」である。")
    para(doc, "図版8点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した18件は、"
              "PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr45.ABBREV[0], abbr45.ABBREV[1])

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
