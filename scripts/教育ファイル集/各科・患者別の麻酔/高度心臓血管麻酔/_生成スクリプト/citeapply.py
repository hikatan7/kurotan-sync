# -*- coding: utf-8 -*-
"""引用番号を本文へ差し込む。

本文（cN_pX.py）は書いたまま触らない。どの文にどの文献を付けるかは
citesN.py に「文のハッシュ → [PMID]」で持ち、組版のときに差し込む。
ハッシュで持つので、段落を足しても順序を変えても対応が崩れない。
逆に、引用の付いた文を書き換えると対応が外れる。外れたら組版時に警告が出る。
"""
import hashlib
import re

SENT = re.compile(r"[^。]*。|[^。]+$")


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


def apply_text(text, cites, used):
    ss = split_sents(text)
    for i, s in enumerate(ss):
        k = h(s)
        if k in cites:
            ss[i] = _mark(s, cites[k])
            used.add(k)
    return "".join(ss)


def apply_blocks(blocks, cites):
    """本文・箇条書き・まとめ・注記のすべてに差し込む。返り値は (新ブロック, 未使用キー)"""
    used = set()
    out = []
    for b in blocks:
        k = b[0]
        if k == "p":
            out.append((k, apply_text(b[1], cites, used)))
        elif k == "ul":
            out.append((k, [apply_text(x, cites, used) for x in b[1]]))
        elif k in ("summary", "note"):
            out.append((k, b[1], [apply_text(x, cites, used) for x in b[2]]))
        else:
            out.append(b)
    return out, set(cites) - used


def dump_keys(blocks):
    """文とハッシュの一覧（引用を付ける場所を選ぶときに使う）"""
    rows = []
    for i, b in enumerate(blocks):
        if b[0] == "p":
            src = [b[1]]
        elif b[0] == "ul":
            src = list(b[1])
        elif b[0] in ("summary", "note"):
            src = list(b[2])
        else:
            continue
        for t in src:
            for s in split_sents(t):
                rows.append((h(s), b[0], i, s))
    return rows
