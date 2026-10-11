# -*- coding: utf-8 -*-
"""詳細版・専攻医用テキストの docx を組む。

  python build.py detail     → 心臓手術後の心停止_詳細版.docx
  python build.py resident   → 心臓手術後の心停止_専攻医用.docx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH
import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para, page_break,
                     heading, toc_field, figure, table, bullets, summary, note, reflist,
                     NAVY, GREY, TEAL)
import refs

OUTDIR = os.path.join(HERE, "..")
FIGDIR = os.path.join(HERE, "..", "図版")
DATE = "2026 年 10 月 8 日"

ABBR = (["略語", "英語", "日本語"],
        [["A-DIVA", "Adult Difficult Intravenous Access scale", "成人の静脈路確保困難を予測するスケール"],
         ["BSI", "bloodstream infection", "血流感染"],
         ["CDC", "Centers for Disease Control and Prevention", "米国疾病予防管理センター"],
         ["CRBSI", "catheter-related bloodstream infection", "カテーテル関連血流感染"],
         ["CRPS", "complex regional pain syndrome", "複合性局所疼痛症候群"],
         ["CVC", "central venous catheter", "中心静脈カテーテル"],
         ["DNTP", "dynamic needle tip positioning", "短軸像で針先を追いながら進める超音波ガイド法"],
         ["ESA", "European Society of Anaesthesiology", "欧州麻酔科学会"],
         ["G", "gauge", "ゲージ（カテーテルの太さ。数が大きいほど細い）"],
         ["ICU", "intensive care unit", "集中治療室"],
         ["INS", "Infusion Nurses Society", "米国輸液看護師協会"],
         ["MAGIC", "Michigan Appropriateness Guide for Intravenous Catheters", "ミシガン静脈カテーテル適正使用ガイド"],
         ["PICC", "peripherally inserted central catheter", "末梢挿入型中心静脈カテーテル"],
         ["PIVC", "peripheral intravenous catheter", "末梢静脈カテーテル"]])

ABBR_RES = (["略語", "英語", "日本語での意味"],
            [["CDC", "Centers for Disease Control and Prevention", "米国疾病予防管理センター（ガイドラインの発行元）"],
             ["PICC", "peripherally inserted central catheter", "末梢挿入型中心静脈カテーテル"],
             ["CVC", "central venous catheter", "中心静脈カテーテル"],
             ["MAGIC", "Michigan Appropriateness Guide for Intravenous Catheters", "ミシガン静脈カテーテル適正使用ガイド"],
             ["DNTP", "dynamic needle tip positioning", "短軸像で針先を追いながら進める超音波ガイド法"],
             ["A-DIVA", "Adult Difficult Intravenous Access scale", "静脈路確保が難しい患者を予測するスケール"],
             ["INS", "Infusion Nurses Society", "米国輸液看護師協会"],
             ["CRPS", "complex regional pain syndrome", "複合性局所疼痛症候群（神経損傷後に続く強い痛み）"],
             ["G", "gauge", "ゲージ（数が大きいほど細い）"],
             ["カテゴリー IA／IB／II", "CDC の推奨区分", "IA・IB＝強く推奨、II＝実施を提案"]])

KINDS = {
    "detail": dict(
        module="text_detail",
        out="静脈・動脈ルート確保_詳細版.docx",
        kicker="専攻医・指導医用資料　詳細版",
        title="静脈・動脈ルート確保",
        sub="── 神経損傷・器材選択・静脈炎・動脈圧ライン ──",
        lines=["CDC 2011・MAGIC・ESA 2020 と主要な臨床研究・判例にもとづく"],
        footer="静脈・動脈ルート確保（詳細版）　　",
        toc=True, abbr=True),
    "resident": dict(
        module="text_resident",
        out="静脈・動脈ルート確保_専攻医版.docx",
        kicker="専攻医用テキスト",
        title="静脈・動脈ルート確保",
        sub="── 刺す前に決めること、刺しながら守ること ──",
        lines=["麻酔科専攻医のための要点"],
        footer="静脈・動脈ルート確保（専攻医版）　　",
        toc=False, abbr=True, abbr_table=ABBR_RES),
}


def build(kind):
    k = KINDS[kind]
    mod = __import__(k["module"])
    res = refs.Resolver()
    bookkit.set_cite_resolver(res)
    doc = new_document()
    set_footer(doc, k["footer"])

    # ---- 表紙（院内文書：表題の下・右寄せに作成者）
    for _ in range(3):
        para(doc)
    para(doc, k["kicker"], size=12, bold=True, color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, k["title"], size=26, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
    para(doc, k["sub"], size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "作成：麻酔科　玉里順子", size=11, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=10)
    para(doc)
    for ln in k["lines"]:
        para(doc, ln, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
    for _ in range(5):
        para(doc)
    para(doc, "作成日　%s" % DATE, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "静岡市立静岡病院　麻酔科", size=11.5, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

    if k["toc"]:
        para(doc, "目　次", size=16, bold=True, color=NAVY,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
        toc_field(doc)
    if k["abbr"]:
        h = heading(doc, "この資料で使う略語", 2)
        if k["toc"]:
            h.paragraph_format.page_break_before = True
        else:
            para(doc, "本文では、初めて出てくる略語に日本語を添えている。図の中の略語はこの表で確かめてほしい。",
                 size=9.5, color=GREY)
        ab = k.get("abbr_table", ABBR)
        table(doc, None, ab[0], ab[1])

    first_h2 = True
    for b in mod.BLOCKS:
        t = b[0]
        if t == "h2":
            hh = heading(doc, b[1], 2)
            if kind == "detail" and b[1].startswith(("はじめに",)):
                hh.paragraph_format.page_break_before = True
            first_h2 = False
        elif t == "h3":
            heading(doc, b[1], 3)
        elif t == "p":
            assert isinstance(b[1], str)
            para(doc, b[1])
        elif t == "ul":
            assert isinstance(b[1], list)
            bullets(doc, b[1])
        elif t == "fig":
            figure(doc, os.path.join(FIGDIR, b[1]), b[2], width_cm=16.0)
        elif t == "tbl":
            table(doc, None, b[1], b[2], size=9.5 if len(b[1]) <= 4 else 9.0)
        elif t == "sum":
            assert isinstance(b[2], list)
            summary(doc, b[1], b[2])
        elif t == "note":
            assert isinstance(b[2], list)
            note(doc, b[1], b[2])
        else:
            raise ValueError(t)

    h = heading(doc, "参考文献", 2)
    if kind == "detail":
        h.paragraph_format.page_break_before = True
    para(doc, "本文の肩付き番号はこの一覧の番号に対応する。", size=9.5, color=GREY)
    reflist(doc, res.rows(), size=9.0)
    if res.missing:
        print("!! 台帳にない ID:", sorted(res.missing))
    drop_orphan_blanks(doc)
    # 末尾の空段落を落とす（白紙の最終頁を防ぐ）
    body = doc.element.body
    while True:
        ps = [e for e in body if e.tag.endswith("}p")]
        last = ps[-1] if ps else None
        if last is None or "".join(last.itertext()).strip() or last.getnext() is None:
            break
        if last.getnext().tag.endswith("}sectPr"):
            body.remove(last)
        else:
            break
    out = os.path.join(OUTDIR, k["out"])
    doc.save(out)
    print(kind, "refs=%d paras=%d" % (len(res.order), len(doc.paragraphs)), out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for kind in (sys.argv[1:] or ["detail", "resident"]):
        build(kind)
