# -*- coding: utf-8 -*-
"""周術期アナフィラキシー統合ガイド docx 生成"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx.enum.text import WD_ALIGN_PARAGRAPH

from bookkit import (new_document, set_footer, para, page_break, heading,
                     toc_field, figure, boxed, column, table, bullets, lead,
                     NAVY, GREY, TEAL, GREEN, BLUE, RED)

import ana_p1, ana_p2, ana_p3, ana_p4

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(os.path.dirname(HERE), "図版")
OUT = sys.argv[1] if len(sys.argv) > 1 else "周術期アナフィラキシー統合ガイド.docx"

# 図版の差し込み位置（見出しテキスト → 直後に入れる図版）
FIGMAP = {
    "第2章　診断基準 ── 3項目から2項目へ":
        ("f01_criteria.png", "図1　診断基準の新旧対照（2022年改訂）"),
    "第3章　重症度分類 ── 3つの物差しを使い分ける":
        ("f02_grades.png", "図2　2系統の重症度分類"),
    "第4章　機序 ── 何が起きているのか":
        ("f03_mechanism.png", "図3　アナフィラキシーに至る4本の道"),
    "第6章　疫学② ── 周術期":
        ("f04_causes.png", "図4　周術期アナフィラキシーの原因物質は国によって違う"),
    "第9章　いつ起きるか ── 導入時90%の理由":
        ("f05_timeline.png", "図5　発症時刻と被疑物質"),
    "第11章　鑑別診断 ── 2本のルートで考える":
        ("f06_diffdx.png", "図6　鑑別の2ルート"),
    "第15章　アドレナリン① ── 筋注か静注か":
        ("f07_adrenaline.png", "図7　アドレナリン：筋注と静注の使い分け"),
    "第23章　トリプターゼ":
        ("f08_tryptase.png", "図8　発症時の採血 ── 何を、いつ"),
    "第26章　なぜ麻酔科医が主体になるのか":
        ("f09_workup.png", "図9　術後診断のタイムライン"),
    "第38章　リスク患者の同定":
        ("f10_preop.png", "図10　術前 ── 検査する人と、しない人"),
}

BLOCKS = ana_p1.BLOCKS + ana_p2.BLOCKS + ana_p3.BLOCKS + ana_p4.BLOCKS

doc = new_document()
set_footer(doc, "周術期アナフィラキシー統合ガイド　　")

# ---------------- 表紙 ----------------
for _ in range(2):
    para(doc)
para(doc, "麻酔科 統合資料", size=12, bold=True, color=TEAL,
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "5資料の統合＋2025年までのガイドライン改訂を反映", size=11, color=GREY,
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "周術期", size=25, bold=True, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=0)
para(doc, "アナフィラキシー統合ガイド", size=25, bold=True, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
para(doc, "── 診断・治療・原因検索のすべて ──",
     size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc)
para(doc)
para(doc, "全 7 部・44 章／付録 A〜G", align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "図版 10 点・表 50 点以上", align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc)
para(doc, "診断基準の2022年改訂　　重症度分類の2系統　　国別の原因物質",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "アドレナリンは筋注か静注か　　トリプターゼの読み方",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "皮膚テストの手技と最高濃度　　「アレルギーです」の分解",
     align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(2):
    para(doc)
para(doc, "作成日　2026年9月8日", color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
para(doc, "静岡市立静岡病院　麻酔科　玉里順子", size=11.5, bold=True,
     color=NAVY, align=WD_ALIGN_PARAGRAPH.CENTER)
page_break(doc)

# ---------------- 目次 ----------------
para(doc, "目　次", size=16, bold=True, color=NAVY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
toc_field(doc)
page_break(doc)

# ---------------- 本文 ----------------
FIGCOUNT = 0
TBLCOUNT = 0
pending_fig = None
for blk in BLOCKS:
    kind = blk[0]
    if kind == "h1":
        heading(doc, blk[1], 1)
    elif kind == "h2":
        heading(doc, blk[1], 2)
        if blk[1] in FIGMAP:
            pending_fig = FIGMAP[blk[1]]
    elif kind == "h3":
        heading(doc, blk[1], 3)
    elif kind == "p":
        para(doc, blk[1], space_after=6)
    elif kind == "lead":
        lead(doc, blk[1])
        if pending_fig:
            path = os.path.join(FIGDIR, pending_fig[0])
            if not os.path.exists(path):
                raise SystemExit("図版が見つかりません: " + path)
            figure(doc, path, pending_fig[1])
            FIGCOUNT += 1
            pending_fig = None
    elif kind == "ul":
        bullets(doc, blk[1])
    elif kind == "fig":
        path = os.path.join(FIGDIR, blk[1])
        figure(doc, path, blk[2])
        FIGCOUNT += 1
    elif kind == "tbl":
        _, header, rows, note = blk
        table(doc, None, header, rows)
        if note:
            para(doc, note, size=9.0, color=GREY, space_after=8)
        TBLCOUNT += 1
    elif kind == "th":
        boxed(doc, "Take Home", blk[1], blk[2], GREEN, "EAF3F0", "005F4F")
    elif kind == "pf":
        boxed(doc, "Pitfall", blk[1], blk[2], RED, "FBEEEC", "9C2B26")
    elif kind == "ev":
        boxed(doc, "Evidence", blk[1], blk[2], BLUE, "EDF2F9", "174682")
    elif kind == "col":
        column(doc, blk[1], blk[2], blk[3])
    elif kind == "pb":
        page_break(doc)
    else:
        raise SystemExit("不明なブロック: " + kind)

if pending_fig:
    raise SystemExit("図版が挿入されませんでした: " + pending_fig[0])

doc.save(OUT)

import fix_blank
n = fix_blank.to_page_break_before(OUT)
print("改ページを pageBreakBefore に置換:", n)
print("saved", OUT, "／図版", FIGCOUNT, "点・表", TBLCOUNT, "点")
