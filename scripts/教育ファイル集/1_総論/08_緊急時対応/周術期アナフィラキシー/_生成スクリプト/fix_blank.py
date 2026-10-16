# -*- coding: utf-8 -*-
"""docx の余分な改ページを取り除く。

・改ページだけの空段落が2つ以上続いていたら、1つだけ残す
・改ページだけの空段落の直前にある「完全に空の段落」を落とす
  （本文が下端ぴったりで終わったとき、この空段落だけが次頁に落ちて白紙になる）
戻り値は (連続改ページの削除数, 直前空段落の削除数)
"""
import sys
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def _text(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def _has_page_br(el):
    return any(b.get(qn("w:type")) == "page" for b in el.iter(qn("w:br")))


def _is_pure_break(el):
    return (el.tag == qn("w:p") and _has_page_br(el)
            and _text(el).strip() == ""
            and not el.findall(".//" + qn("w:drawing")))


def _is_empty(el):
    return (el.tag == qn("w:p") and not _has_page_br(el)
            and _text(el).strip() == ""
            and not el.findall(".//" + qn("w:drawing")))


def fix(path, out=None):
    out = out or path
    doc = Document(path)
    body = doc.element.body
    kids = [e for e in body if e.tag in (qn("w:p"), qn("w:tbl"))]

    dup = 0
    prev_break = False
    for el in kids:
        if _is_pure_break(el):
            if prev_break:
                body.remove(el)
                dup += 1
                continue
            prev_break = True
        else:
            prev_break = False

    kids = [e for e in body if e.tag in (qn("w:p"), qn("w:tbl"))]
    orphan = 0
    for i, el in enumerate(kids[:-1]):
        if _is_empty(el) and _is_pure_break(kids[i + 1]):
            body.remove(el)
            orphan += 1

    doc.save(out)
    return dup, orphan


def to_page_break_before(path, out=None):
    """改ページだけの空段落を、次の段落の pageBreakBefore に置き換える。

    空段落は1行ぶんの高さを占めるので、直前のページが本文で埋まっていると
    その空段落だけが次ページへ落ちて白紙になる。pageBreakBefore なら
    高さを持たないので、この白紙が構造的に発生しない。
    次が表のときは置き換えられないので、そのまま残す。
    """
    doc = Document(path)
    body = doc.element.body
    kids = [e for e in body if e.tag in (qn("w:p"), qn("w:tbl"))]
    n = 0
    for i, el in enumerate(kids[:-1]):
        if not _is_pure_break(el):
            continue
        nxt = kids[i + 1]
        if nxt.tag != qn("w:p"):
            continue
        pPr = nxt.find(qn("w:pPr"))
        if pPr is None:
            pPr = OxmlElement("w:pPr")
            nxt.insert(0, pPr)
        if pPr.find(qn("w:pageBreakBefore")) is None:
            pbb = OxmlElement("w:pageBreakBefore")
            # pPr の先頭付近（pStyle の直後）に置く
            st = pPr.find(qn("w:pStyle"))
            if st is not None:
                st.addnext(pbb)
            else:
                pPr.insert(0, pbb)
        body.remove(el)
        n += 1
    doc.save(out or path)
    return n


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(fix(p), p)
