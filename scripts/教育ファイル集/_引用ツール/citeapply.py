# -*- coding: utf-8 -*-
"""引用番号を本文へ差し込む。

本文（cNN_pX.py）は書いたまま触らない。どの文にどの文献を付けるかは
citesNN.py に「文のハッシュ → [PMID]」で持ち、組版のときに差し込む。
ハッシュで持つので、段落を足しても順序を変えても対応が崩れない。
逆に、引用の付いた文を書き換えると対応が外れる。外れたら組版時に警告が出る。

本によってブロックの種類が違う（p / lead / th / pf / col / ev …）ので、
「中の文字列はすべて本文」とみなして走査し、種類ごとの例外だけを表で持つ。
"""
import hashlib
import re

SENT = re.compile(r"[^。]*。|[^。]+$")

# 中身を本文として扱わないブロック
SKIP_KINDS = {"fig", "tbl", "h1", "h2", "h3", "pb", "toc", "ev"}
# 先頭いくつかの要素を見出し等として飛ばすブロック（種類 -> 飛ばす数）
HEAD_SLOTS = {"th": 1, "pf": 1, "summary": 1, "note": 1, "sum": 1, "col": 2}


def split_sents(text):
    return [m.group(0) for m in SENT.finditer(text) if m.group(0)]


def h(sent):
    """文のハッシュ（空白を落としてから取る）"""
    t = re.sub(r"\s+", "", sent)
    return hashlib.md5(t.encode("utf-8")).hexdigest()[:10]


def _mark(s, pmids):
    m = "{{%s}}" % ",".join(pmids)
    if s.endswith("。"):
        return s[:-1] + m + "。"
    return s + m


def _slots(b):
    """ブロックから、本文として扱う (位置, 文字列) を取り出す"""
    kind = b[0]
    if kind in SKIP_KINDS:
        return []
    start = 1 + HEAD_SLOTS.get(kind, 0)
    out = []
    for i in range(start, len(b)):
        v = b[i]
        if isinstance(v, str):
            out.append((i, v))
        elif isinstance(v, list):
            for j, x in enumerate(v):
                if isinstance(x, str):
                    out.append(((i, j), x))
    return out


def _set(b, pos, val):
    b = list(b)
    if isinstance(pos, tuple):
        i, j = pos
        lst = list(b[i])
        lst[j] = val
        b[i] = lst
    else:
        b[pos] = val
    return tuple(b)


def apply_text(text, cites, used):
    ss = split_sents(text)
    for i, s in enumerate(ss):
        k = h(s)
        if k in cites:
            ss[i] = _mark(s, cites[k])
            used.add(k)
    return "".join(ss)


def apply_blocks(blocks, cites):
    """返り値は (新ブロック列, 使われなかったキー)"""
    used = set()
    out = []
    for b in blocks:
        slots = _slots(b)
        if not slots:
            out.append(b)
            continue
        nb = b
        for pos, txt in slots:
            nt = apply_text(txt, cites, used)
            if nt != txt:
                nb = _set(nb, pos, nt)
        out.append(nb)
    return out, set(cites) - used


def dump_keys(blocks):
    """(ハッシュ, 種類, 位置, 文) の一覧"""
    rows = []
    for i, b in enumerate(blocks):
        for pos, txt in _slots(b):
            for s in split_sents(txt):
                rows.append((h(s), b[0], i, s))
    return rows
