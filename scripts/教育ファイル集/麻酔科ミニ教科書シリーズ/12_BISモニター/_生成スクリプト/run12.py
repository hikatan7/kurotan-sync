# -*- coding: utf-8 -*-
import os, sys, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pdf2blocks, build_restored
from sum12 import SUMMARIES

VOL = ("C:/Users/junch/OneDrive/_\u65e7\u30c7\u30b9\u30af\u30c8\u30c3\u30d7"
       "/\u6559\u80b2\u30d5\u30a1\u30a4\u30eb\u96c6"
       "/\u9ebb\u9154\u79d1\u30df\u30cb\u6559\u79d1\u66f8\u30b7\u30ea\u30fc\u30ba"
       "/12_BIS\u30e2\u30cb\u30bf\u30fc")
PDF = os.path.join(VOL, "_旧レイアウト",
                   "BISモニター完全ガイド"
                   "_専門医版_旧.pdf")
FIG = os.path.join(VOL, "\u56f3\u7248")

META = {
    "no": "\u246b",
    "vol": "12",
    "audience": "\u5c02\u9580\u533b\u5411\u3051",
    "title": "BIS \u30e2\u30cb\u30bf\u30fc\u5b8c\u5168\u30ac\u30a4\u30c9",
    "sub": "\u6570\u5b57\u3092\u8aad\u3080\u306e\u3067\u306f\u306a\u304f\u3001\u8133\u3092\u8aad\u3080",
    "compose": "\u5168 10 \u7ae0\u30fb\u4ed8\u9332 A\u301cD",
    "extra": "\u56f3\u7248 12 \u70b9\u30fb\u30b3\u30e9\u30e0 8 \u672c",
    "date": "2026\u5e749\u670814\u65e5",
}

blocks, prof = pdf2blocks.convert(PDF, FIG)
print("body %.1fpt" % prof["body"])
keys = set(re.sub(r"\s+", "", b[1]) for b in blocks if b[0] == "h2")
print("MISS:", [k for k in SUMMARIES if k not in keys])
blocks = build_restored.rebuild(blocks, SUMMARIES)
print(collections.Counter(b[0] for b in blocks))
print(build_restored.build(META, blocks, FIG, os.path.join(HERE, "v12.docx")))
