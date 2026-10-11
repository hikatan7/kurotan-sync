# -*- coding: utf-8 -*-
"""シリーズ全巻に略語対応を適用する。

  python master_abbr.py [巻番号 ...]     引数なしで全巻
元ファイルは各巻の `_略語対応前` に退避してから上書きする。
"""
import glob
import os
import re
import shutil
import sys

from docx import Document
from docx.oxml.ns import qn

import abbr_dict
import concept_blocks
from apply_abbr import ptext, pstyle, make_para, is_body_para, TOC_STYLES
import run_abbr

BASE = (r"C:\Users\junch\OneDrive\デスクトップ\教育ファイル集"
        r"\麻酔科ミニ教科書シリーズ")


def insert_concepts(path, vol):
    blocks = [b for b in concept_blocks.BLOCKS if b[0] == vol]
    if not blocks:
        return 0
    doc = Document(path)
    body = doc.element.body
    tops = [e for e in body if e.tag == qn("w:p")]
    sample = next((e for e in body
                   if e.tag == qn("w:p") and is_body_para(e)), None)
    if sample is None:
        return 0
    n = 0
    for b in blocks:
        _, anchor_re, lead, items, tail = b[:5]
        fkw = b[5] if len(b) > 5 else None
        if fkw and fkw not in os.path.basename(path):
            continue
        rx = re.compile(anchor_re)
        target = None
        for k, e in enumerate(tops):
            if pstyle(e) in TOC_STYLES:
                continue
            t = ptext(e).strip()
            if len(t) > 60 or not t:
                continue
            if not rx.search(t):
                continue
            # 直後に本文らしい長い段落が続くものだけを採用する
            # （部の中扉に並ぶ章名の一覧を拾わないため）
            nxt = ""
            for e2 in tops[k + 1:k + 9]:
                s2 = ptext(e2).strip()
                # 空行・図表キャプション・節見出しは飛ばす
                if (not s2 or re.match(r"^(図|表)\s*[0-9]", s2)
                        or re.match(r"^[0-9]+[.\-][0-9]+[\s　]", s2)):
                    continue
                nxt = s2
                break
            if len(nxt) < 40:
                continue
            target = e
            break
        if target is None:
            print("    [注意] 挿入位置が見つからない:", anchor_re)
            continue
        # すでに入っていれば飛ばす
        nxt = target.getnext()
        if nxt is not None and lead[:16] in ptext(nxt):
            continue
        els = [make_para(sample, lead)]
        els += [make_para(sample, s, indent=0.8) for s in items]
        els.append(make_para(sample, tail))
        prev = target
        for x in els:
            prev.addnext(x)
            prev = x
        n += 1
    if n:
        doc.save(path)
    return n


def main(vols=None):
    dirs = sorted(glob.glob(os.path.join(BASE, "[01]*")))
    total = []
    for d in dirs:
        vol = os.path.basename(d)[:2]
        if vols and vol not in vols:
            continue
        docs = [f for f in sorted(glob.glob(os.path.join(d, "*.docx")))
                if "_略語対応前" not in f]
        if not docs:
            continue
        bak = os.path.join(d, "_略語対応前")
        os.makedirs(bak, exist_ok=True)
        print("=== 第%s巻 %s" % (vol, os.path.basename(d)))
        for f in docs:
            b = os.path.join(bak, os.path.basename(f))
            if not os.path.exists(b):
                shutil.copy2(f, b)
            nc = insert_concepts(f, vol)
            r = run_abbr.process(f, vol)
            if r is None:
                print("    %-52s スキップ" % os.path.basename(f)[:50])
                continue
            print("    %-52s 展開 %3d 件／一覧 %3d 語／概念ブロック %d"
                  % (os.path.basename(f)[:50], r[0], r[1], nc))
            total.append((vol, os.path.basename(f), r[0], r[1], nc))
    print("\n合計：ファイル %d／展開 %d 件／概念ブロック %d"
          % (len(total), sum(t[2] for t in total), sum(t[4] for t in total)))
    return total


if __name__ == "__main__":
    main(sys.argv[1:] or None)
