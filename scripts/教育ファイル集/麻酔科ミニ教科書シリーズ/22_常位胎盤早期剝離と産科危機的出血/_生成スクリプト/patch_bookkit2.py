# -*- coding: utf-8 -*-
r"""目次を部・章・コラムだけにし、まとめ／注意書きの組版を足す。"""
import io

p = "bookkit.py"
s = io.open(p, encoding="utf-8").read()

# --- 目次の深さ 1-3 → 1-2（8-1 などの小見出しを載せない）
old_toc = r'instr.text = r' + "'" + r' TOC \o "1-3" \h \z \u ' + "'"
new_toc = r'instr.text = r' + "'" + r' TOC \o "1-2" \h \z \u ' + "'"
assert old_toc in s, old_toc
s = s.replace(old_toc, new_toc, 1)

# --- まとめ・注意書き・アウトラインレベル
NEW = '''def outline(p, level):
    """段落にアウトラインレベルを与える。
    見出しスタイルを使わずに目次へ載せたいとき（コラム）に使う。"""
    ol = OxmlElement("w:outlineLvl")
    ol.set(qn("w:val"), str(level))
    p._p.get_or_add_pPr().append(ol)


def summary(doc, title, lines):
    """章や部の最後に置くまとめ。左に縦線を引くだけで、枠では囲まない。
    目次には載せない。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(13)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    left_bar(p, "0A1830", size=20)
    _run(p, title, size=12, bold=True, color=NAVY)
    for i, ln in enumerate(lines):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.line_spacing = 1.35
        q.paragraph_format.left_indent = Cm(0.55)
        q.paragraph_format.first_line_indent = Cm(-0.45)
        q.paragraph_format.keep_with_next = (i < len(lines) - 1)
        left_bar(q, "0A1830", size=20)
        _run(q, "・" + ln, size=10.5, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def note(doc, title, lines):
    """本文中の注意書き。枠で囲まず、太字の導入＋箇条書きにする。"""
    if title:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        _run(p, "◆　" + title, size=11, bold=True, color=RED)
    for i, ln in enumerate(lines):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.line_spacing = 1.35
        q.paragraph_format.left_indent = Cm(0.55)
        q.paragraph_format.first_line_indent = Cm(-0.45)
        q.paragraph_format.keep_with_next = (i < len(lines) - 1)
        _run(q, "・" + ln, size=10.5, color=INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def column(doc, no, title, paras):'''
assert "def column(doc, no, title, paras):" in s
s = s.replace("def column(doc, no, title, paras):", NEW, 1)

# --- コラム見出しを目次に出す
old_col = '    _run(p, "コラム%d　%s" % (no, title), bold=True, color=PURPLE)'
assert old_col in s
s = s.replace(old_col, old_col + "\n    outline(p, 1)", 1)

io.open(p, "w", encoding="utf-8").write(s)
print("bookkit patched")
