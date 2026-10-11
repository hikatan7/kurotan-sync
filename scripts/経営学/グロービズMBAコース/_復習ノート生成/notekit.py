"""復習ノート生成エンジン（Day5 THE YES 版の体裁を全科目に展開）

使い方: 各ノートの中身を notes/<id>.py に NOTE = dict(...) で書き、
    python build.py <id> [...]   または   python build.py all
出力: 各 Day フォルダに <file>.docx と <file>.pdf、_復習ノート生成/index/<id>.json（ポータル用）

NOTE の形
    id, course, day, file(拡張子なし), dir(コース内の相対フォルダ)
    title, lecturer, sources(元資料の説明1行), made(作成日)
    lead: ひとことまとめ
    sections: [(見出し, [ブロック, ...]), ...]
        ブロック: ("b", [文字列 or (太字, 本文)])  箇条書き
                  ("t", 見出し行, 行リスト, 列幅mm)  表
                  ("box", "1行目が太字の見出し\n本文...")
                  ("p", 小さい注記)
    closing: [box文字列, ...]  まとめ・持ち帰りの問い
    glossary: [(分野見出し, [(語句, よみ, 解説, 頁), ...]), ...]
"""
import json
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # グロービズMBAコース
HERE = os.path.dirname(os.path.abspath(__file__))
NAVY = "1F3A5F"
PALE = "E8EEF5"
FONT = "Meiryo UI"


def _shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), color)
    tcPr.append(sh)


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def _no_split(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    el.set(qn("w:val"), "true")
    trPr.append(el)


class Builder:
    def __init__(self):
        doc = Document()
        s = doc.sections[0]
        s.page_width, s.page_height = Mm(210), Mm(297)
        s.left_margin = s.right_margin = Mm(18)
        s.top_margin = s.bottom_margin = Mm(16)
        st = doc.styles["Normal"]
        st.font.name = FONT
        st.font.size = Pt(10)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        for name in ("Heading 1", "Heading 2", "Heading 3"):
            h = doc.styles[name]
            h.font.name = FONT
            h.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
            h.font.color.rgb = RGBColor.from_string(NAVY)
        doc.styles["Heading 1"].font.size = Pt(15)
        doc.styles["Heading 2"].font.size = Pt(12.5)
        doc.styles["Heading 3"].font.size = Pt(11)
        self.doc = doc

    def para(self, text, bold=False, size=None, color=None, after=3):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.space_before = Pt(0)
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        return p

    def bullets(self, items):
        for it in items:
            p = self.doc.add_paragraph()
            p.paragraph_format.left_indent = Mm(8)
            p.paragraph_format.first_line_indent = Mm(-4)
            p.paragraph_format.space_after = Pt(1.5)
            if isinstance(it, (tuple, list)):
                r = p.add_run("・" + it[0])
                r.bold = True
                p.add_run(it[1])
            else:
                p.add_run("・" + it)

    def box(self, text, fill=PALE):
        t = self.doc.add_table(rows=1, cols=1)
        t.autofit = False
        _no_split(t.rows[0])
        c = t.rows[0].cells[0]
        c.width = Mm(174)
        _shade(c, fill)
        for i, ln in enumerate(text.split("\n")):
            p = c.paragraphs[0] if i == 0 else c.add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(ln)
            if i == 0:
                r.bold = True
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def table(self, header, rows, widths, font=9):
        t = self.doc.add_table(rows=1, cols=len(header))
        t.style = "Table Grid"
        t.autofit = False
        hr = t.rows[0]
        _repeat_header(hr)
        for i, h in enumerate(header):
            c = hr.cells[i]
            c.width = Mm(widths[i])
            _shade(c, NAVY)
            r = c.paragraphs[0].add_run(h)
            r.bold = True
            r.font.size = Pt(font)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        for ri, row in enumerate(rows):
            tr = t.add_row()
            _no_split(tr)
            for i, v in enumerate(row):
                c = tr.cells[i]
                c.width = Mm(widths[i])
                if ri % 2 == 1:
                    _shade(c, "F4F6F9")
                p = c.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(str(v))
                r.font.size = Pt(font)
                if i == 0:
                    r.bold = True
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def footer(self):
        for s in self.doc.sections:
            fp = s.footer.paragraphs[0]
            fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = fp.add_run()
            for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
                if tag:
                    e = OxmlElement("w:fldChar")
                    e.set(qn("w:fldCharType"), tag)
                else:
                    e = OxmlElement("w:instrText")
                    e.set(qn("xml:space"), "preserve")
                    e.text = txt
                r._r.append(e)
            r.font.size = Pt(8)


# ---- 50音ソート ----
_KATA = {chr(c): chr(c - 0x60) for c in range(0x30A1, 0x30F7)}


def sort_key(term, yomi):
    y = (yomi or term).strip()
    if re.match(r"[A-Za-z0-9]", y):
        return (0, y.upper())
    y = "".join(_KATA.get(ch, ch) for ch in y)
    return (1, y)


def build(N, pdf=True):
    B = Builder()
    doc = B.doc
    outdir = os.path.join(ROOT, N["dir"])
    base = os.path.join(outdir, N["file"])

    p = doc.add_paragraph()
    r = p.add_run(f"グロービス経営大学院　{N['course']}　Day{N['day']} 復習ノート")
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    p = doc.add_paragraph()
    r = p.add_run(N["title"])
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = RGBColor.from_string(NAVY)
    B.para(f"講師：{N['lecturer']}　／　元資料：{N['sources']}", size=9, color="555555")
    B.para(f"作成：{N.get('made', '2026-09-24')}　構成：Ⅰ 要点まとめ ／ Ⅱ 語句解説（分野別） ／ Ⅲ 語句リスト（索引）",
           size=9, color="555555", after=8)
    B.box("この回のひとことまとめ\n" + N["lead"])

    doc.add_heading("Ⅰ　要点まとめ", level=1)
    for heading, blocks in N["sections"]:
        doc.add_heading(heading, level=2)
        for b in blocks:
            kind = b[0]
            if kind == "b":
                B.bullets(b[1])
            elif kind == "t":
                B.table(b[1], b[2], b[3])
            elif kind == "box":
                B.box(b[1])
            elif kind == "p":
                B.para("※ " + b[1], size=8.5, color="666666")
            else:
                raise ValueError(kind)
    for c in N.get("closing", []):
        B.box(c)

    doc.add_page_break()
    doc.add_heading("Ⅱ　語句解説（分野別）", level=1)
    B.para("「頁」は講義スライドの頁番号。解説はスライドの定義を基本に、補足を加えています。", size=9, color="666666", after=6)
    allterms = []
    for gi, (gtitle, items) in enumerate(N["glossary"]):
        doc.add_heading(gtitle, level=2)
        B.table(["語句", "解説", "頁"], [(t, e, pg) for t, y, e, pg in items], [38, 118, 18])
        cat = gtitle.split(".", 1)[-1].strip()
        for t, y, e, pg in items:
            allterms.append(dict(term=t, yomi=y, expl=e, pages=pg, cat=cat))

    doc.add_page_break()
    doc.add_heading("Ⅲ　語句リスト（索引）", level=1)
    B.para("Ⅱで解説した語句を、英字→50音順に並べた一覧です。見返しや暗記チェック用に。", size=9, color="666666", after=6)
    srt = sorted(allterms, key=lambda d: sort_key(d["term"], d["yomi"]))
    B.table(["No.", "語句", "分野", "頁"],
            [(str(i + 1), d["term"], d["cat"], d["pages"]) for i, d in enumerate(srt)],
            [12, 96, 44, 22], font=8.5)
    B.para(f"全{len(srt)}語。", size=8.5, color="666666")
    B.footer()

    os.makedirs(outdir, exist_ok=True)
    doc.save(base + ".docx")

    os.makedirs(os.path.join(HERE, "index"), exist_ok=True)
    meta = {k: N[k] for k in ("id", "course", "day", "file", "dir", "title", "lecturer", "sources", "lead")}
    meta["case"] = N.get("case", "")
    meta["terms"] = allterms
    meta["sections"] = [h for h, _ in N["sections"]]
    with open(os.path.join(HERE, "index", N["id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return base + ".docx", len(srt)
