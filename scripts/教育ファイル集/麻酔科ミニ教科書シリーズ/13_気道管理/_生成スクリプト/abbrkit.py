# -*- coding: utf-8 -*-
"""既刊 docx に「略語の初出定義」と「総称の概念説明」を差し込むための道具。

本文ソースが残っていない巻でも使えるよう、
既存の本文段落を deepcopy して書式を引き継ぐ方式にしてある。
"""
import copy
import re
from docx.shared import Cm
from docx.oxml.ns import qn


def para_text(el):
    return "".join(el.itertext())


def style_of(el):
    m = re.search(r'w:pStyle w:val="([^"]+)"', el.xml)
    return m.group(1) if m else None


def find_body_para(doc, pred, skip_styles=("2f2", "3e", "18")):
    """目次を除いた本文から、条件に合う段落の (index, element) を返す。"""
    els = list(doc.element.body)
    for i, e in enumerate(els):
        if e.tag != qn("w:p"):
            continue
        if style_of(e) in skip_styles:
            continue
        if pred(para_text(e)):
            return i, e
    return None, None


def clone_para(src_el, text, indent_cm=None):
    """src_el の書式を引き継いだ新しい段落要素を作る。"""
    new = copy.deepcopy(src_el)
    # 既存のランと段落内容を消す（pPr は残す）
    for child in list(new):
        if child.tag != qn("w:pPr"):
            new.remove(child)
    # 元の最初のランの rPr を拾う
    rpr = None
    for r in src_el.findall(qn("w:r")):
        found = r.find(qn("w:rPr"))
        if found is not None:
            rpr = copy.deepcopy(found)
        break
    r = new.makeelement(qn("w:r"), {})
    if rpr is not None:
        r.append(rpr)
    t = new.makeelement(qn("w:t"), {})
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    new.append(r)
    if indent_cm is not None:
        pPr = new.find(qn("w:pPr"))
        if pPr is None:
            pPr = new.makeelement(qn("w:pPr"), {})
            new.insert(0, pPr)
        for old in pPr.findall(qn("w:ind")):
            pPr.remove(old)
        ind = new.makeelement(qn("w:ind"), {})
        ind.set(qn("w:left"), str(int(Cm(indent_cm).twips)))
        pPr.append(ind)
    return new


def insert_after(anchor_el, new_els):
    """anchor_el の直後に new_els を順に差し込む。"""
    prev = anchor_el
    for e in new_els:
        prev.addnext(e)
        prev = e


def replace_in_paragraphs(doc, old, new, limit=None):
    """本文・表の中のテキストを置換する（ラン境界をまたぐ場合も処理）。"""
    n = 0

    def fix(p):
        nonlocal n
        if limit is not None and n >= limit:
            return
        runs = p.findall(qn("w:r"))
        texts = []
        for r in runs:
            ts = r.findall(qn("w:t"))
            texts.append("".join(t.text or "" for t in ts))
        whole = "".join(texts)
        if old not in whole:
            return
        whole = whole.replace(old, new, 1 if limit else -1)
        n += 1
        # 先頭ランに全文を入れ、残りのランのテキストを空にする
        first = True
        for r in runs:
            ts = r.findall(qn("w:t"))
            if not ts:
                continue
            for k, t in enumerate(ts):
                if first:
                    t.text = whole
                    t.set(qn("xml:space"), "preserve")
                    first = False
                else:
                    t.text = ""

    for p in doc.element.body.iter(qn("w:p")):
        fix(p)
    return n
