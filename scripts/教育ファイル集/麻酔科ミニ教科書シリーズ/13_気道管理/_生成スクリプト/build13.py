# -*- coding: utf-8 -*-
"""麻酔科ミニ教科書シリーズ ⑬「気道管理」docx 生成"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

import bookkit as bk
from bookkit import (drop_orphan_blanks, summary, note,
                     new_document, set_footer, para, page_break, heading, toc_field,
                     figure, boxed, column, table, bullets, lead,
                     NAVY, GREY, TEAL, GREEN, BLUE, PURPLE, RED, INK)

import c13_p1, c13_p2, c13_p3, c13_p4, c13_p5

FIGDIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "図版")
OUT = sys.argv[1] if len(sys.argv) > 1 else "気道管理.docx"

BLOCKS = (c13_p1.BLOCKS + c13_p2.BLOCKS + c13_p3.BLOCKS
          + c13_p4.BLOCKS + c13_p5.BLOCKS)


def _rebuild(blocks):
    """枠の廃止・章末まとめ・コラム番号の振り直しをまとめて行う。

    既刊の Take Home は章の途中に置かれているが、中身はその章の要点である。
    章ごとに拾い集め、章の最後に「この章のまとめ」としてまとめ直す。
    """
    n = 0
    tmp = []
    for b in blocks:
        if b[0] == "col":
            n += 1
            tmp.append(("col", n, b[2], b[3]))
        else:
            tmp.append(b)
    blocks = tmp

    out = []
    buf = []

    def flush():
        if buf:
            out.append(("sum", "この章のまとめ", list(buf)))
            del buf[:]

    for b in blocks:
        k = b[0]
        if k in ("h1", "h2", "pb"):
            flush()
            out.append(b)
            continue
        if k == "th":
            title = str(b[1])
            if title.endswith("部の要点"):
                flush()
                out.append(("sum", title.replace("の要点", "のまとめ"), b[2]))
            else:
                buf.extend(b[2])          # 章の最後まで持ち越す
            continue
        if k == "pf":
            out.append(("note", b[1], b[2]))
            continue
        out.append(b)
    flush()
    return out


BLOCKS = _rebuild(BLOCKS)
BLOCKS = [b for i, b in enumerate(BLOCKS)
          if not (b[0] == "pb" and i + 1 < len(BLOCKS)
                  and BLOCKS[i + 1][0] in ("h1", "h2"))]
BLOCKS = [b for i, b in enumerate(BLOCKS)
          if not (b[0] == "pb" and i + 1 < len(BLOCKS)
                  and BLOCKS[i + 1][0] in ("h1", "h2"))]

doc = new_document()
set_footer(doc, "麻酔科ミニ教科書シリーズ ⑬　気道管理　　")

# ---------------- 表紙 ----------------
for _ in range(2):
    para(doc)
para(doc, "麻酔科ミニ教科書シリーズ　⑬", size=12, bold=True, color=TEAL,
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "第 13 巻", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "専門医・専攻医のための", size=13, color=GREY,
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "気道管理", size=30, bold=True, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
para(doc, "── 見えるかどうかではなく、酸素化を続けられるか ──", size=13,
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc)
para(doc)
para(doc, "全 5 部・16 章／コラム 8 本／付録 A〜E",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "図版 20 点・表 9 点", align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc)
para(doc, "上気道の閉塞　無呼吸耐用時間　Mallampati　マスク換気　声門上器具",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "ビデオ喉頭鏡　覚醒下挿管　Plan A〜D　CICO と前頸部気道　抜管の設計",
     align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(4):
    para(doc)
para(doc, "作成日　2026年9月3日", color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "静岡市立静岡病院　麻酔科　玉里順子", size=11.5, bold=True,
     color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
page_break(doc)

# ---------------- 目次 ----------------
para(doc, "目　次", size=16, bold=True, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
toc_field(doc)
_TOC_BREAK = True

# ---------------- 本文 ----------------
FIGCOUNT = 0
TBLCOUNT = 0
_prev_kind = None
for blk in BLOCKS:
    kind = blk[0]
    if kind == "h1":
        _h = heading(doc, blk[1], 1)
        _h.paragraph_format.page_break_before = True
    elif kind == "h2":
        _h = heading(doc, blk[1], 2)
        if str(blk[1]).startswith("付録") and _prev_kind != "h1":
            _h.paragraph_format.page_break_before = True
    elif kind == "h3":
        heading(doc, blk[1], 3)
    elif kind == "p":
        para(doc, blk[1], space_after=6)
    elif kind == "lead":
        lead(doc, blk[1])
    elif kind == "ul":
        bullets(doc, blk[1])
    elif kind == "fig":
        path = os.path.join(FIGDIR, blk[1])
        if not os.path.exists(path):
            raise SystemExit("図版が見つかりません: " + path)
        figure(doc, path, blk[2])
        FIGCOUNT += 1
    elif kind == "tbl":
        _, cap, header, rows, widths = blk
        table(doc, cap, header, rows, widths)
        TBLCOUNT += 1
    elif kind == "sum":
        summary(doc, blk[1], blk[2])
    elif kind == "note":
        note(doc, blk[1], blk[2])
    elif kind == "ev":
        boxed(doc, "Evidence", blk[1], blk[2], BLUE, "EDF2F9", "174682")
    elif kind == "col":
        column(doc, blk[1], blk[2], blk[3])
    elif kind == "pb":
        page_break(doc)
    else:
        raise SystemExit("不明なブロック: " + kind)
    _prev_kind = kind

drop_orphan_blanks(doc)
doc.save(OUT)
print("saved", OUT, "／図版", FIGCOUNT, "点・表", TBLCOUNT, "点")
