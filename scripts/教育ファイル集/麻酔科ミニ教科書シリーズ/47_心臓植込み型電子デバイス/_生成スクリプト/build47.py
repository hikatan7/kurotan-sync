# -*- coding: utf-8 -*-
"""㊸ 心臓植込み型電子デバイス　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr47
import refs47_extra
import refs47
import c47_p1
import c47_p2
import c47_p3
import volno

bookkit.REFS = dict(refs47.REFS)
bookkit.REFS.update(refs47_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "心臓植込み型電子デバイス.docx")

META = {
    "no": volno.circled(47),
    "vol": "47",
    "audience": "麻酔科専攻医・麻酔科医・臨床工学技士・手術室看護師",
    "title": "心臓植込み型電子デバイス",
    "sub": "ペースメーカー・ICD・CRT と周術期管理",
    "compose": "デバイスを知る・ICDとCRT・周術期の管理・植込み手術の麻酔・まとめ",
    "extra": "全19章／図版7点／コラム2本／参考文献19件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c47_p1.BLOCKS + c47_p2.BLOCKS + c47_p3.BLOCKS)


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
    para(doc, "心臓植込み型", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "電子デバイス", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、心臓植込み型電子デバイス ── "
              "ペースメーカー、植込み型除細動器、心臓再同期療法の機器 ── を"
              "持つ患者の周術期管理と、デバイス植込み手術そのものの麻酔である。")
    para(doc, "デバイスの設定を決めるのは麻酔科の仕事ではない。"
              "しかし設定が変わったあとの患者を管理するのは麻酔科であり、"
              "術中にデバイスが予期しない動きをしたとき、"
              "最初に気づくのも麻酔科である。"
              "本書は、その役割に必要な最小限を扱う ── "
              "何を尋ねればよいのか、返ってきた答えが何を意味するのか、"
              "そして目の前で起きていることをどう読むのか。")
    para(doc, "この巻には、一つの軸がある。"
              "ペースメーカーがしていることは二つしかない ── "
              "刺激することと、感知すること。"
              "そして感知は「刺激しないための仕組み」である。"
              "自分の心臓が拍ったと判断すれば、予定していた刺激をやめる。"
              "この一点を押さえると、周術期にデバイスで起きる問題の"
              "ほとんどが説明できる ── "
              "電気メスの雑音を「拍った」と誤認すれば刺激が止まり、"
              "「頻脈だ」と誤認すれば必要のない治療が加わる。")
    para(doc, "もう一つ、繰り返し述べることがある ── "
              "必要のない変更にも不利益がある、ということである。"
              "非同期にすれば自分の拍と競合し、"
              "頻脈治療を止めればその間は守られていない。"
              "「念のため変更しておく」が常に安全側とは限らない。"
              "そして変更したなら、戻すところまでが一組である ── "
              "周術期管理で最も抜けやすいのが、この「戻すこと」である。")
    para(doc, "本書は機種名・数値・設定の内容を書かない。"
              "この領域は変化が速く ── "
              "リードレスも皮下植込み型も刺激伝導系ペーシングも"
              "この十年のあいだに実用化されたものである ── "
              "書いた時点で古くなることが分かっているからである。"
              "何を書かなかったかは付録Cに、"
              "施設で決めておきたい事柄は付録Dにまとめた。")
    para(doc, "心臓血管麻酔におけるデバイス患者の管理は"
              "『高度心臓血管麻酔』第Ⅰ章が別に扱っている。"
              "本書はデバイスそのものの理解と、植込み手術の麻酔に重心を置いた。"
              "低心機能患者の導入は㊻が、"
              "カテーテル検査室での鎮静は㊵が扱っている。"
              "対応は付録Bの表にまとめた。")
    para(doc, "図版7点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した19件は、"
              "PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr47.ABBREV[0], abbr47.ABBREV[1])

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
