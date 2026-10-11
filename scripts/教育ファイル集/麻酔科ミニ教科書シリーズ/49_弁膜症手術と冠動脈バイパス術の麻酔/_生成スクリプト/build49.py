# -*- coding: utf-8 -*-
"""㊸ 弁膜症手術と冠動脈バイパス術の麻酔　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr49
import refs49_extra
import refs49
import c49_p1
import c49_p2
import volno

bookkit.REFS = dict(refs49.REFS)
bookkit.REFS.update(refs49_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "弁膜症手術と冠動脈バイパス術の麻酔.docx")

META = {
    "no": volno.circled(49),
    "vol": "49",
    "audience": "麻酔科専攻医・麻酔科医・臨床工学技士",
    "title": "弁膜症手術と冠動脈バイパス術の麻酔",
    "sub": "病名ではなく、負荷の向きで読む",
    "compose": "この巻の位置・弁膜症・冠動脈バイパス術・共通する管理",
    "extra": "全18章／図版6点／コラム1本／参考文献14件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c49_p1.BLOCKS + c49_p2.BLOCKS)


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
    para(doc, "弁膜症手術と", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "冠動脈バイパス術", size=30, bold=True, color=NAVY,
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
    para(doc, "本書が扱うのは、心臓手術のうち最も件数の多い二つ ── "
              "弁膜症手術と冠動脈バイパス術である。")
    para(doc, "心臓手術の麻酔について、このシリーズはすでに何冊かを持っている ── "
              "基礎㉝、止血㉛、緊急と補助循環㉞、低侵襲・ロボット㉟、"
              "先天性㊱、移植㊲、そして大血管㉜。"
              "しかしこの二つの術式そのものを扱った巻が無かった。本書はそこを埋める。")
    para(doc, "弁膜症の章は、病名ごとに覚える形をとっていない。"
              "四つの病態は二つの軸で整理できるからである ── "
              "どちらの心室に、圧負荷と容量負荷のどちらがかかっているか。"
              "圧負荷の病態では充満する時間と圧が命であり、"
              "容量負荷の病態では前へ出しやすくすることが効く。"
              "「脈は速めに／遅めに」「後負荷は下げる／保つ」という指示は、"
              "すべてこの二軸から出ている。")
    para(doc, "そして弁膜症手術には、ほかの手術に無い特徴がある ── "
              "手術そのものが患者の生理を変える、ということである。"
              "狭窄を取り除けば後負荷が急に減り、"
              "逆流を止めれば逃げ場が無くなる。"
              "だから離脱後の管理は、術前とは別の設計になる。"
              "術前の方針をそのまま持ち込まない ── これが第II部を貫く原則である。")
    para(doc, "冠動脈バイパス術のほうは、煎じ詰めれば"
              "「虚血を起こさずに手術が終わるまで持たせる」ことに尽きる。"
              "虚血の生理は供給と需要の差でしかなく、"
              "心拍数が供給と需要の両側に現れることが、"
              "頻脈を避けるという原則の根拠になっている。")
    para(doc, "血行動態の目標は、方向（上げる・下げる・保つ）だけを書いた。"
              "数値は患者と術式で変わり、"
              "「この病態ならこの値」という普遍の答えが無いためである（㊺第2章）。"
              "人工心肺の運転そのもの、経食道心エコーの断面、"
              "弁膜症の重症度の診断基準と手術適応も書いていない ── "
              "何を書かなかったかは付録Cに、"
              "施設で決めておきたい事柄は付録Dにまとめた。")
    para(doc, "図版6点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた。"
              "引用した14件は、"
              "PubMed の書誌情報と題名を一件ずつ照合して確定している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文は原則として日本語表記で書いてある。"
              "以下は、同じ事柄を英語の文献で探すときの手がかりである。")
    table(doc, None, abbr49.ABBREV[0], abbr49.ABBREV[1])

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
