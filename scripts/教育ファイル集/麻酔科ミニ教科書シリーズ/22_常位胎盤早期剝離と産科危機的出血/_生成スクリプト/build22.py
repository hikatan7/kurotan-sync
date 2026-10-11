# -*- coding: utf-8 -*-
"""麻酔科ミニ教科書シリーズ ㉒「常位胎盤早期剝離と産科危機的出血」docx 生成"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, summary, note, set_footer, para, page_break, heading,
                     toc_field, figure, boxed, column, table, bullets, lead,
                     reflist, NAVY, GREY, TEAL, GREEN, BLUE, RED)

import citeapply
import citekit
import cites22
import c22_p1
import c22_p2
import c22_p3
import c22_p4
import c22_sum

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "..", "図版")
OUT = sys.argv[1] if len(sys.argv) > 1 else "常位胎盤早期剝離と産科危機的出血.docx"

BLOCKS = c22_p1.BLOCKS + c22_p2.BLOCKS + c22_p3.BLOCKS + c22_p4.BLOCKS


def _rebuild(blocks):
    """枠の廃止・章末まとめの挿入・コラム番号の振り直しをまとめて行う。"""
    # --- コラムは本文に現れる順に 1 から振り直す
    col_no = 0
    tmp = []
    for b in blocks:
        if b[0] == "col":
            col_no += 1
            tmp.append(("col", col_no, b[2], b[3]))
        else:
            tmp.append(b)
    blocks = tmp

    # --- 章末まとめを差し込む位置を決める
    #     章（h2）の中身が終わる直前＝次の h1／h2／pb の手前。
    out = []
    cur_ch = None          # いま開いている章の見出し
    pending = None         # まだ出していないまとめ

    def flush():
        nonlocal pending
        if pending:
            out.append(("sum", "この章のまとめ", pending))
            pending = None

    for i, b in enumerate(blocks):
        kind = b[0]
        if kind in ("h1", "h2", "pb"):
            flush()
            if kind == "h2":
                cur_ch = b[1]
                pending = c22_sum.SUMMARIES.get(cur_ch)
            out.append(b)
            continue
        # Take Home / Pitfall の枠をやめる
        if kind == "th":
            title = b[1]
            if title.endswith("部の要点"):
                out.append(("sum", title.replace("の要点", "のまとめ"), b[2]))
            elif title.endswith("章の要点"):
                pass                      # 章末まとめに統合済み
            else:
                out.append(("note", title, b[2]))
            continue
        if kind == "pf":
            out.append(("note", b[1], b[2]))
            continue
        out.append(b)
    flush()
    return out


BLOCKS = _rebuild(BLOCKS)

# 明示的な改頁の直後が部見出し・付録見出しなら、改頁を落として見出し側に
# page_break_before を付ける。改頁とみなしページが重なって空白ページが生まれるのを防ぐ。
_clean = []
for i, b in enumerate(BLOCKS):
    if b[0] == "pb" and i + 1 < len(BLOCKS) and BLOCKS[i + 1][0] in ("h1", "h2"):
        continue
    _clean.append(b)
BLOCKS = _clean

# ---- 引用（肩付き番号）を差し込む
BLOCKS, _UNUSED = citeapply.apply_blocks(BLOCKS, cites22.CITES)
if _UNUSED:
    print("!! 引用の対応が外れた文がある:", sorted(_UNUSED))
CITES = citekit.Cites()
bookkit.set_cite_resolver(CITES.mark)

doc = new_document()
set_footer(doc, "麻酔科ミニ教科書シリーズ ㉒　常位胎盤早期剝離と産科危機的出血　　")

# ---------------- 表紙 ----------------
for _ in range(2):
    para(doc)
para(doc, "麻酔科ミニ教科書シリーズ　㉒", size=12, bold=True, color=TEAL,
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "第 22 巻", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "専門医のための", size=13, color=GREY,
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "常位胎盤早期剝離と産科危機的出血", size=24, bold=True, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
para(doc, "── 児を娩出しながら、母体のDICを同時に治療する ──",
     size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc)
para(doc)
para(doc, "全 7 部・39 章／コラム 8 本／付録 A〜E",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "図版 22 点・表 23 点", align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc)
para(doc, "見えない出血　フィブリノゲン　産科DIC　粘弾性検査",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "麻酔法の選択　大量輸血　止血のエスカレーション　術後管理",
     align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(4):
    para(doc)
para(doc, "作成日　2026年9月14日", color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "静岡市立静岡病院　麻酔科　玉里順子", size=11.5, bold=True,
     color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
page_break(doc)

# ---------------- 目次 ----------------
para(doc, "目　次", size=16, bold=True, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
toc_field(doc)

# ---------------- 略語（巻頭） ----------------
# 目次の直後に手で改頁を入れると、目次がページ境界で終わったときに白紙が1枚出る。
# 見出し側の pageBreakBefore で改頁する。
_abbr = para(doc, "本書で使う主な略語", size=14, bold=True, color=NAVY,
             space_after=8)
_abbr.paragraph_format.page_break_before = True
para(doc, "初出時には本文中でも展開している。全一覧は付録Cを参照。",
     size=10, color=GREY, space_after=8)
table(doc, None, ["略語", "意味"],
      [["DIC", "播種性血管内凝固"],
       ["Fbg", "フィブリノゲン"],
       ["FDP", "フィブリン分解産物"],
       ["FFP", "新鮮凍結血漿"],
       ["FIBTEM", "血小板を遮断してフィブリン形成能を測る粘弾性検査項目"],
       ["A5", "凝固開始 5 分後の血餅強度"],
       ["MTP", "大量輸血プロトコル"],
       ["IUFD", "子宮内胎児死亡"],
       ["HDP", "妊娠高血圧症候群"],
       ["VTE", "静脈血栓塞栓症"]])
page_break(doc)

# ---------------- 本文 ----------------
FIGCOUNT = 0
TBLCOUNT = 0
COLCOUNT = 0
SUMCOUNT = 0
_prev_kind = None
for blk in BLOCKS:
    kind = blk[0]
    if kind == "h1":
        h = heading(doc, blk[1], 1)
        h.paragraph_format.page_break_before = True
    elif kind == "h2":
        h = heading(doc, blk[1], 2)
        # 直前が部見出しなら改頁しない（「付　録」だけのページを作らない）
        if str(blk[1]).startswith("付録") and _prev_kind != "h1":
            h.paragraph_format.page_break_before = True
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
        _, header, rows, tnote = blk
        table(doc, None, header, rows)
        if tnote:
            para(doc, tnote, size=9.0, color=GREY, space_after=8)
        TBLCOUNT += 1
    elif kind == "sum":
        summary(doc, blk[1], blk[2])
        SUMCOUNT += 1
    elif kind == "note":
        note(doc, blk[1], blk[2])
    elif kind == "ev":
        boxed(doc, "Evidence", blk[1], blk[2], BLUE, "EDF2F9", "174682")
    elif kind == "col":
        column(doc, blk[1], blk[2], blk[3])
        COLCOUNT += 1
    elif kind == "pb":
        page_break(doc)
    else:
        raise SystemExit("不明なブロック: " + kind)
    _prev_kind = kind

# ---------------- 参考文献 ----------------
_h = heading(doc, "参考文献", 2)
_h.paragraph_format.page_break_before = True
para(doc, "本文の肩付き番号は、この一覧の番号に対応する。"
          "すべて PubMed 識別子（PMID）と DOI を確認した。"
          "台帳は同じフォルダの"
          "『常位胎盤早期剝離_SourceLedger.xlsx』にある。")
para(doc, "日本産科婦人科学会ほかの『産科危機的出血への対応指針』と"
          "『産科DIC診断基準』は、学会の公開文書であり PubMed 上の"
          "識別子を持たない。本文では図の脇に出典を示した。")
reflist(doc, CITES.rows())
print("参考文献", CITES.count(), "件")

n_drop = drop_orphan_blanks(doc)
doc.save(OUT)
print("空段落を除去:", n_drop, "件")
print("saved", OUT, "／図版", FIGCOUNT, "点・表", TBLCOUNT,
      "点・コラム", COLCOUNT, "本・まとめ", SUMCOUNT, "本")
