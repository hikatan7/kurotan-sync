# -*- coding: utf-8 -*-
"""docx に「巻頭の略語一覧」と「章ごとの初出展開」を入れる。

・展開は本文段落（表の中・見出し・図表キャプション・目次を除く）だけで行う
・すでに直後に丸括弧がある場合は触らない
・ランをまたぐ場合は、同じ書式のランに限って連結してから置換する
"""
import copy
import re
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import abbr_dict

NAVY = RGBColor(0x0A, 0x18, 0x30)
INK = RGBColor(0x22, 0x30, 0x3F)

TOC_STYLES = {"2f2", "3e", "18", "1f", "2f", "3f"}
HEAD_RE = re.compile(r"^(第\s*[０-９0-9IVX]+\s*[章部]|付録\s*[A-Z]|はじめに|"
                     r"[0-9]+-[0-9]+[\s　]|■|▸|コラム[0-9]|【|図\s*[0-9]|表\s*[0-9]|"
                     r"目\s*次)")
CHAP_RE = re.compile(r"^(第\s*[０-９0-9]+\s*章|はじめに|付録\s*[A-Z])")
# 文献リストらしい行（展開すると引用文の中身を書き換えてしまう）
REF_RE = re.compile(r"(et al\.|doi:|DOI:|PMID|https?://|[12][0-9]{3};[0-9]|\bJAMA\b|\bLancet\b|N Engl J Med|Anesthesiology|Br J Anaesth|Crit Care|Intensive Care Med)")


def ptext(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t")))


def pstyle(el):
    m = re.search(r'w:pStyle w:val="([^"]+)"', el.xml)
    return m.group(1) if m else None


def is_body_para(el):
    """展開してよい本文段落か"""
    if el.tag != qn("w:p"):
        return False
    if pstyle(el) in TOC_STYLES:
        return False
    t = ptext(el).strip()
    if not t or len(t) < 12:
        return False
    if HEAD_RE.match(t):
        return False
    if "PAGEREF" in t or "HYPERLINK" in t:
        return False
    if REF_RE.search(t) or re.match(r"^(\[[0-9]+\]|[0-9]{1,3}[.)]\s)", t):
        return False
    return True


def _runs(el):
    return [r for r in el.findall(qn("w:r")) if r.findall(qn("w:t"))]


def _rtext(r):
    return "".join(t.text or "" for t in r.findall(qn("w:t")))


def _set_rtext(r, s):
    ts = r.findall(qn("w:t"))
    for i, t in enumerate(ts):
        if i == 0:
            t.text = s
            t.set(qn("xml:space"), "preserve")
        else:
            t.text = ""


def _rpr_key(r):
    rpr = r.find(qn("w:rPr"))
    return str(rpr.xml) if rpr is not None else ""


def _depth_at(whole, i):
    d = 0
    for ch in whole[:i]:
        if ch in "（(":
            d += 1
        elif ch in "）)":
            d = max(0, d - 1)
    return d


def _enclosing(whole, s, e):
    """s..e を囲む丸括弧の (開始, 終了) を返す。囲まれていなければ None。"""
    i, d = s - 1, 0
    while i >= 0:
        if whole[i] in "）)":
            d += 1
        elif whole[i] in "（(":
            if d == 0:
                break
            d -= 1
        i -= 1
    if i < 0:
        return None
    j, d = e, 0
    while j < len(whole):
        if whole[j] in "（(":
            d += 1
        elif whole[j] in "）)":
            if d == 0:
                break
            d -= 1
        j += 1
    if j >= len(whole):
        return None
    return i, j


def expand_in_para(el, abbr, eng, jp):
    """段落内の最初の abbr を展開する。

    ・地の文にあるとき      … ABBR（英語：日本語）
    ・「（ABBR）」の形のとき … （ABBR：英語）に書き換える（二重括弧を避ける）
    ・それ以外の括弧の中     … 触らない
    """
    runs = _runs(el)
    if not runs:
        return False
    texts = [_rtext(r) for r in runs]
    whole = "".join(texts)
    for m in re.finditer(re.escape(abbr), whole):
        s, e = m.start(), m.end()
        if s > 0 and (whole[s - 1].isalnum() or whole[s - 1] in "-‐：:"):
            continue
        if e < len(whole) and (whole[e].isalnum() or whole[e] in "-‐"):
            continue
        if whole[e:e + 1] in ("（", "("):
            return False
        rep, s2, e2 = "%s（%s：%s）" % (abbr, eng, jp), s, e
        if _depth_at(whole, s) > 0:
            enc = _enclosing(whole, s, e)
            if enc is None:
                continue
            i, j = enc
            if whole[i + 1:j].strip() != abbr:
                continue          # 括弧の中に他の語もある → 触らない
            rep, s2, e2 = "（%s：%s）" % (abbr, eng), i, j + 1
        pos, start_i, end_i = 0, None, None
        for i2, t in enumerate(texts):
            if start_i is None and pos + len(t) > s2:
                start_i = i2
            if pos + len(t) >= e2:
                end_i = i2
                break
            pos += len(t)
        if start_i is None or end_i is None:
            return False
        if start_i != end_i and len({_rpr_key(runs[i2])
                                     for i2 in range(start_i, end_i + 1)}) != 1:
            return False
        off = sum(len(x) for x in texts[:start_i])
        merged = "".join(texts[start_i:end_i + 1])
        _set_rtext(runs[start_i], merged[:s2 - off] + rep + merged[e2 - off:])
        for i2 in range(start_i + 1, end_i + 1):
            _set_rtext(runs[i2], "")
        return True
    return False


def make_para(sample, text, size=None, bold=False, color=None, indent=None,
              align=None):
    new = copy.deepcopy(sample)
    for ch in list(new):
        if ch.tag != qn("w:pPr"):
            new.remove(ch)
    pPr = new.find(qn("w:pPr"))
    if pPr is None:
        pPr = new.makeelement(qn("w:pPr"), {})
        new.insert(0, pPr)
    for tag in ("w:ind", "w:jc"):
        for old in pPr.findall(qn(tag)):
            pPr.remove(old)
    if indent is not None:
        ind = new.makeelement(qn("w:ind"), {})
        ind.set(qn("w:left"), str(int(Cm(indent).twips)))
        pPr.append(ind)
    if align is not None:
        jc = new.makeelement(qn("w:jc"), {})
        jc.set(qn("w:val"), align)
        pPr.append(jc)
    r = new.makeelement(qn("w:r"), {})
    rPr = new.makeelement(qn("w:rPr"), {})
    if bold:
        rPr.append(new.makeelement(qn("w:b"), {}))
    if color is not None:
        c = new.makeelement(qn("w:color"), {})
        c.set(qn("w:val"), color)
        rPr.append(c)
    if size:
        sz = new.makeelement(qn("w:sz"), {})
        sz.set(qn("w:val"), str(int(size * 2)))
        rPr.append(sz)
    if len(rPr):
        r.append(rPr)
    t = new.makeelement(qn("w:t"), {})
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    new.append(r)
    return new


def page_break_para(sample):
    new = make_para(sample, "")
    r = new.findall(qn("w:r"))[0]
    br = new.makeelement(qn("w:br"), {})
    br.set(qn("w:type"), "page")
    r.insert(0, br)
    return new
