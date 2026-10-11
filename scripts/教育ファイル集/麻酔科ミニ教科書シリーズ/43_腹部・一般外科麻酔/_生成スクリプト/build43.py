# -*- coding: utf-8 -*-
"""㊸ 腹部・一般外科麻酔　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr43
import refs43_extra
import refs43
import c43_p1
import c43_p2
import c43_p3
import volno

bookkit.REFS = dict(refs43.REFS)
bookkit.REFS.update(refs43_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "腹部・一般外科麻酔.docx")

META = {
    "no": volno.circled(43),
    "vol": "43",
    "audience": "麻酔科専攻医・麻酔科医・手術室看護師",
    "title": "腹部・一般外科麻酔",
    "sub": "腹腔という閉じた空間で起きていること",
    "compose": "腹腔という場所・気腹と体位・予定手術・臓器別・緊急の腹部・まとめ",
    "extra": "全23章／図版8点／コラム7本／参考文献42件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c43_p1.BLOCKS + c43_p2.BLOCKS + c43_p3.BLOCKS)


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
    para(doc, "腹部・一般外科", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、腹部・一般外科の手術に固有の麻酔管理である。")
    para(doc, "腹部の手術の麻酔は、"
              "「基本の全身麻酔ができれば足りる」と扱われがちである。"
              "心臓手術のような山場がなく、"
              "教科書でも臓器別の各論に分散していて、"
              "「腹部の麻酔」という一つのまとまりになっていない。"
              "しかしこの領域には、ほかの部位には無い共通の事情がある ── "
              "外科が仕事をする場所が、腹腔という一つの閉じた空間だということである。"
              "そこを開けるか、ガスで膨らませるか。"
              "どちらにしても腹腔の圧が変わり、"
              "圧が変われば呼吸も循環も腎臓もまとめて動く。")
    para(doc, "本書はこの一点を軸にした。"
              "気腹でも、腸閉塞でも、腹腔内出血でも、"
              "腹腔内圧が上がったときに起きることは同じ順序で並ぶ。"
              "この軸があるおかげで、"
              "腹腔鏡の生理も、緊急開腹も、"
              "腹部コンパートメント症候群も、"
              "ひと続きの話として読めるようになる。")
    para(doc, "もう一つ、本書が繰り返し述べることがある。"
              "予定手術と緊急手術は、別の仕事だということである。"
              "予定の腹部手術は術後回復強化（ERAS）という枠組みのなかにあり、"
              "判断の多くは手術の前に済んでいる。"
              "緊急の腹部手術はそうではない ── "
              "評価の時間がなく、判断は手術室のなかで次々に求められ、"
              "成績を決めているのは個々の手技よりも体制である。"
              "同じ「開腹」という言葉が使われていても、"
              "この二つを同じ引き出しに入れてはいけない。")
    para(doc, "本書は、送気圧の数値、輸液の量、絶飲食の時間、"
              "体温と血糖の目標値、薬剤名と投与量、"
              "腹腔内圧の閾値を本文に書いていない。"
              "手術・薬剤・施設・製品によって変わり、"
              "指針の版でも変わってきた事柄だからである。"
              "何を書かなかったかは付録Cに、"
              "施設で決めておきたい事柄は付録Dにまとめた。"
              "国内の診療報酬上の取り扱いも扱っていない ── "
              "算定や請求の根拠として本書を用いないこと。")
    para(doc, "重複する主題はほかの巻に譲った。"
              "輸液そのものの考え方は①②『麻酔中の輸液管理』が、"
              "気道管理は⑬と㉙が、"
              "体位による神経障害は⑮が、"
              "区域麻酔の手技は⑰が、"
              "抗血栓薬との兼ね合いは㉑が、"
              "腎機能低下例は㉓と㉘が、"
              "感染対策は㊷が扱っている。"
              "対応は付録Bの表にまとめた。")
    para(doc, "図版8点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した42件は、"
              "PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr43.ABBREV[0], abbr43.ABBREV[1])

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
