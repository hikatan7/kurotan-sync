# -*- coding: utf-8 -*-
"""docx の本文を文単位で取り出す（引用位置を決めるための下ごしらえ）。

    python dumpdocx.py <docx> [出力 tsv]

出力は「ハッシュ<TAB>見出し<TAB>文」。見出しは、その文が属する直前の章見出し。
"""
import io
import re
import sys

from docx import Document

import citedocx

HEAD = re.compile(r"^(第\s*[0-9IVX]+\s*[章部]|付\s*録|はじめに|おわりに|参考文献)")


def dump(path):
    doc = Document(path)
    rows = []
    cur = ""
    for par in doc.paragraphs:
        t = par.text.strip()
        if not t:
            continue
        # 章（第N章・第N部・付録・はじめに・おわりに）だけを覚える。
        # 小見出し（1-1 など）で上書きすると、章での絞り込みができなくなる。
        if HEAD.match(t):
            cur = t[:40]
        for s in citedocx.split_sents(t):
            s = s.strip()
            if len(s) < 6:
                continue
            rows.append((citedocx.h(s), cur, s))
    return rows


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rows = dump(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else None
    if out:
        with io.open(out, "w", encoding="utf-8") as f:
            for r in rows:
                f.write("\t".join(r) + "\n")
        print("%d 文 -> %s" % (len(rows), out))
    else:
        for r in rows[:50]:
            print("\t".join(r)[:160])
        print("... 合計 %d 文" % len(rows))
