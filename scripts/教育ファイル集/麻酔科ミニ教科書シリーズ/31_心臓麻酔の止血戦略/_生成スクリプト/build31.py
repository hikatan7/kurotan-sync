# -*- coding: utf-8 -*-
"""㉚ ICU の人工呼吸管理　docx を組む。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docx.enum.text import WD_ALIGN_PARAGRAPH

import bookkit
from bookkit import (drop_orphan_blanks, new_document, set_footer, para,
                     heading, toc_field, figure, table, bullets,
                     summary, note, column, references, NAVY, GREY, TEAL)

import abbr31
import refs31_extra
import refs31
import c31_p1
import c31_p2
import c31_p3
import c31_p4

bookkit.REFS = dict(refs31.REFS)
bookkit.REFS.update(refs31_extra.EXTRA)

FIGDIR = os.path.join(HERE, "..", "図版")
OUT = os.path.join(HERE, "..", "心臓麻酔の止血戦略.docx")

META = {
    "no": "㉛",
    "vol": "31",
    "audience": "麻酔科医・心臓血管外科医・臨床工学技士・輸血部",
    "title": "心臓麻酔の止血戦略",
    "sub": "フィブリノゲンを中心に、測って・補って・記録する",
    "compose": "人工心肺の凝固障害から、2026年の適応追加と保険算定まで",
    "extra": "全24章／コラム7本／図版18点・表20点／参考文献45件",
    "date": "2026 年 9 月 22 日",
}

BLOCKS = (c31_p1.BLOCKS + c31_p2.BLOCKS + c31_p3.BLOCKS + c31_p4.BLOCKS)


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
    para(doc, "心臓麻酔の", size=30, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    para(doc, "止血戦略", size=30, bold=True, color=NAVY,
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
    para(doc, "本書は、人工心肺を用いた心臓血管外科手術の周術期止血を扱う。"
              "施設ごとに手順書があり、機種によって検査の作法も違う。"
              "本書が示すのは一つの筋道であって、標準手順ではない。"
              "自施設の手順書と読み合わせて使ってほしい。")
    para(doc, "本書は具体的な投与量・閾値を本文にほとんど書いていない。"
              "病態と施設で適切な値が変わり、数字だけが一人歩きしやすいためである。"
              "何を書かなかったかは付録D-7に、"
              "施設で決めておくべき項目は付録Eにまとめた。")
    para(doc, "2026年3月23日、フィブリノゲン濃縮製剤に"
              "「心臓血管外科手術における出血に伴う後天性低フィブリノゲン血症に対する"
              "フィブリノゲンの補充」が効能・効果として追加された。"
              "本書はこの変更を中心に置き、その条件・根拠・限界を第III部で詳しく扱う。"
              "保険適応と算定は付録Cに一覧にした。"
              "制度は改定で変わるので、使用時には必ず最新の点数表と通知を確認してほしい。")
    para(doc, "本書の内容は、院内資料『高度心臓血管麻酔』第Ⅶ章"
              "（人工心肺・出血と輸血・循環の目標）の第2部と重なる。"
              "第Ⅶ章は人工心肺と循環の目標を含めて俯瞰する位置づけであり、"
              "本書は止血の各論を、2026年3月の適応追加まで含めて深く扱う。"
              "神経モニタリングは㉜『大血管手術の脳・脊髄保護』を参照されたい。")
    para(doc, "図版18点はすべて本書のために作図した。"
              "本文の記述には出現順の肩付き番号を付し、"
              "巻末に番号順の参考文献一覧を置いた（付録F）。"
              "添付文書・通知・国内ガイドライン・診療報酬点数表など"
              "PubMed に収載されない一次資料も、同じ番号体系で引用している。")

    heading(doc, "本書で使う略語", 2)
    para(doc, "本文では、章ごとの初出で「略語（英語表記：日本語表記）」の形に"
              "展開している。以下はその一覧である。")
    table(doc, None, abbr31.ABBREV[0], abbr31.ABBREV[1])

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
            col_no[0] += 1          # 出現順に振り直す
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
