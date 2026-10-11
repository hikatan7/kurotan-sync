# -*- coding: utf-8 -*-
"""改ページだけの空段落を、次の段落の pageBreakBefore に置き換える。

改ページだけの段落は1行ぶんの高さを持つ。直前のページが本文で埋まっていると、
その段落だけが次ページへ落ちて「フッターだけの白紙ページ」になる。
pageBreakBefore は高さを持たないので、この白紙が構造的に発生しない。

w:pPr の子要素には決まった順序があり、順序を守らずに挿入すると
Word がファイルを壊れていると判断する。ここでは
pStyle / keepNext / keepLines の直後、それ以外の要素より前に入れる。
"""
import sys
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# w:pPr の中で pageBreakBefore より前に来る要素（この順序で並ぶ）
BEFORE = ("w:pStyle", "w:keepNext", "w:keepLines")


def _text(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def _has_page_br(el):
    return any(b.get(qn("w:type")) == "page" for b in el.iter(qn("w:br")))


def _is_pure_break(el):
    return (el.tag == qn("w:p") and _has_page_br(el)
            and _text(el).strip() == ""
            and not el.findall(".//" + qn("w:drawing")))


def _insert_pbb(p):
    """段落 p に pageBreakBefore を、スキーマ順を守って入れる。"""
    pPr = p.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        p.insert(0, pPr)
    if pPr.find(qn("w:pageBreakBefore")) is not None:
        return False
    pbb = OxmlElement("w:pageBreakBefore")
    anchor = None
    for name in BEFORE:
        found = pPr.find(qn(name))
        if found is not None:
            anchor = found
    if anchor is not None:
        anchor.addnext(pbb)
    else:
        pPr.insert(0, pbb)
    return True


def convert(path, out=None):
    doc = Document(path)
    body = doc.element.body
    kids = [e for e in body if e.tag in (qn("w:p"), qn("w:tbl"))]
    n, skipped = 0, 0
    for i, el in enumerate(kids[:-1]):
        if not _is_pure_break(el):
            continue
        nxt = kids[i + 1]
        if nxt.tag != qn("w:p"):
            skipped += 1          # 次が表のときは置き換えられない
            continue
        _insert_pbb(nxt)
        body.remove(el)
        n += 1
    doc.save(out or path)
    return n, skipped


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(convert(p), p)
