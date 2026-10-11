# -*- coding: utf-8 -*-
"""㊸ 麻酔導入と覚醒・抜管　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr46
import refs46_extra
import refs46
import c46_p1
import c46_p2
import c46_p3
import volno

bookkit.REFS = dict(refs46.REFS)
bookkit.REFS.update(refs46_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "麻酔導入と覚醒・抜管.docx")

META = {
    "no": volno.circled(46),
    "vol": "46",
    "audience": "麻酔科専攻医・麻酔科医・手術室看護師",
    "title": "麻酔導入と覚醒・抜管",
    "sub": "入口と出口は、対称ではない",
    "compose": "導入の前に・導入・維持から覚醒へ・抜管・まとめ",
    "extra": "全19章／図版7点／コラム2本／参考文献14件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c46_p1.BLOCKS + c46_p2.BLOCKS + c46_p3.BLOCKS)


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
    para(doc, "麻酔導入と", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "覚醒・抜管", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、麻酔の入口と出口 ── 導入と、覚醒・抜管である。")
    para(doc, "この二つは、しばしば一組にして語られる。"
              "眠らせて、起こす。入口と出口。"
              "だから同じくらいの注意を払えばよい、という感覚になりやすい。"
              "しかし二つは対称ではない。")
    para(doc, "導入のとき、患者は最も条件の整った状態にある ── "
              "絶食し、前酸素化を受け、手術はまだ始まっておらず、"
              "部屋には人がいて、器材は手元に並んでいる。"
              "抜管のときは、そのどれもが崩れている。"
              "数時間の手術で浮腫み、体温が下がり、"
              "気道には血液や分泌物があり、人は減り、次の患者が待っている。"
              "そして患者は、導入前と同じ気道を持っていない。"
              "本書の主張は、つまるところ一つである ── "
              "抜管に、導入と同じだけの準備を与えること。")
    para(doc, "本書には、もう一つ繰り返し現れる形がある。"
              "この二つの時間帯には、あとからでは間に合わないことが集まっている、"
              "ということである。"
              "前酸素化で作る酸素の貯金も、体温の再分布も、無気肺の形成も、"
              "気づいたときにはもう終わっている。"
              "だから「起きてから対応する」ではなく"
              "「起きる前提で準備する」が基本の姿勢になる。"
              "そして決めておいたことは、その場の判断より強い ── "
              "何回試したら方法を変えるか、何が揃ったら抜管するか。"
              "その場で考えると、たいてい楽なほうへ流れる。")
    para(doc, "本書は手技を扱わない。"
              "気道確保そのものは⑬『気道管理』が、"
              "抜管の指針と段階的な方策は㉙『声門上器具と周術期気道トラブル』が"
              "それぞれ一冊を使って書いている。"
              "本書が扱うのは、その前後 ── 準備、判断の順序、条件の立て方である。"
              "薬剤名・用量・時間・判定の数値も書いていない。"
              "何を書かなかったかは付録Cに、"
              "施設で決めておきたい事柄は付録Dにまとめた。")
    para(doc, "図版7点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した14件は、"
              "PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr46.ABBREV[0], abbr46.ABBREV[1])

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
