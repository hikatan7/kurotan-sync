# -*- coding: utf-8 -*-
"""略語の巻頭一覧を PDF から取り出し、本文に「章ごとの初出で展開」を掛け直す。

⑤と⑪は docx の控えが「略語対応前」しか残っていない。本文そのものは
PDF と一致しているが、初出の展開（例：RCRI → RCRI（Revised Cardiac Risk
Index：改訂心リスク指数））だけが入っていない。
構造の正確な docx を使いつつ、その展開をやり直すためのモジュール。
"""
import re

import pdfplumber

HEAD = re.compile(r"略\s*語")


# 略語らしさの判定。数字だけの見出し（表の通し番号）を略語と取り違えると、
# 本文中の「1」「2」に長い注記が差し込まれて本が壊れる。実際に⑤で起きた。
ABBR = re.compile(r"^[A-Za-z0-9][A-Za-z0-9\-/‐ ]{0,14}$")


def looks_like_abbr(a, en, ja):
    """略語の行かどうか。数字だけ・1文字・説明文のように長い訳語は弾く。"""
    if not ABBR.match(a) or HEAD.search(a):
        return False
    if len(a) < 2 or not re.search(r"[A-Za-z]", a):
        return False            # 「1」「2」のような表の通し番号
    if not re.search(r"[A-Za-z]", en):
        return False
    if len(en) > 70 or len(ja) > 40:
        return False            # 略語の対訳ではなく注記
    return True


def from_pdf(path, max_pages=8):
    """巻頭の略語一覧（略語／英語／日本語）を返す。

    表がページをまたぐと列数がぶれる（結合セルのぶんだけ空欄が増える）ので、
    空欄を落としてから「略語・英語・日本語」の3つに揃った行だけを拾う。
    """
    rows, seen = [], set()
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages[:max_pages]:
            for t in page.find_tables():
                for r in t.extract():
                    cells = [(c or "").replace("\n", " ").strip() for c in r]
                    cells = [c for c in cells if c]
                    if len(cells) != 3:
                        continue
                    a, en, ja = cells
                    if not looks_like_abbr(a, en, ja):
                        continue
                    if a in seen:
                        continue
                    seen.add(a)
                    rows.append([a, en, ja])
    return rows


def _pattern(a):
    """略語そのものを拾う正規表現。前後が英数字なら別語とみなす。"""
    if re.match(r"^[A-Za-z0-9][A-Za-z0-9\-/‐]*$", a):
        return re.compile(r"(?<![A-Za-z0-9\-])" + re.escape(a) + r"(?![A-Za-z0-9\-])")
    return re.compile(re.escape(a))


def expand(blocks, rows):
    """章ごとに、各略語の初出を1回だけ展開する。

    すでに直後が「（」になっているものは、元から展開済みとみなして触らない。
    """
    items = []
    for a, en, ja in rows:
        full = "%s（%s：%s）" % (a, en, ja) if en and ja else None
        if full:
            items.append((a, _pattern(a), full))
    items.sort(key=lambda x: -len(x[0]))     # ACCP を ACC より先に見る

    out = []
    seen = set()

    def fix(s):
        if not isinstance(s, str) or not s:
            return s
        for a, pat, full in items:
            if a in seen:
                continue
            m = pat.search(s)
            if not m:
                continue
            if s[m.end():m.end() + 1] in ("（", "("):
                seen.add(a)
                continue
            s = s[:m.start()] + full + s[m.end():]
            seen.add(a)
        return s

    for b in blocks:
        k = b[0]
        if k == "h2":
            seen = set()                     # 章が変わったら初出をやり直す
            out.append(b)
            continue
        if k in ("h1", "h3"):
            out.append(b)                    # 見出しは展開しない（長くなる）
            continue
        if k == "p":
            out.append(("p", fix(b[1])))
        elif k == "ul":
            out.append(("ul", [fix(x) for x in b[1]]))
        elif k == "tbl":
            out.append(("tbl", b[1], [[fix(c) for c in r] for r in b[2]], b[3]))
        elif k in ("th", "pf", "ev", "note"):
            out.append((k, b[1], [fix(x) for x in b[2]]))
        elif k == "colx":
            out.append(("colx", b[1], b[2], [fix(x) for x in b[3]]))
        else:
            out.append(b)
    return out
