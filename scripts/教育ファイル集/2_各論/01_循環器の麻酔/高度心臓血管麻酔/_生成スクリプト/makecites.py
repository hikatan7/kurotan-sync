# -*- coding: utf-8 -*-
"""各章の引用位置（citesN.py）を作る。

手順は二段階。
  1) 数字の一致で決まるものを採る（もっとも確かで、数値の出典はここで決まる）
  2) 残った文献を、語の重なりでいちばん近い文に置く
どちらにも掛からなかった文献は「未配置」として報告する。
提案はあくまで提案で、citesN.py を直接手で直してよい。
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import citeapply
import citematch

# 引用を置かない文（付録の一覧や、確認できなかった資料の記述）
NG_WORDS = ("確認できなかった", "S-ID", "PMID", "この章で引用した文献",
            "台帳", "本文では使っていない", "実在を確認できない")

WORD_MIN = 4.0        # 語の重なりでの採用しきい値


def sections(ch):
    """文のハッシュ -> その文が属する節（h2 見出し）と、その節にある図表番号"""
    import re as _re
    blocks = []
    for part in ("p1", "p2"):
        blocks += list(importlib.import_module("c%d_%s" % (ch, part)).BLOCKS)
    cur = ""
    figs = {}
    smap = {}
    order = []
    for b in blocks:
        if b[0] == "h2":
            cur = b[1]
            order.append(cur)
            figs.setdefault(cur, set())
        elif b[0] == "fig":
            m = _re.search(r"図\s*(\d+)-(\d+)", b[2])
            if m:
                figs.setdefault(cur, set()).add(int(m.group(2)))
        if b[0] == "p":
            src = [b[1]]
        elif b[0] == "ul":
            src = list(b[1])
        elif b[0] in ("summary", "note"):
            src = list(b[2])
        else:
            continue
        for t in src:
            for x in citeapply.split_sents(t):
                smap[citeapply.h(x)] = cur
    return smap, figs, order


def targets(use):
    """用途の文字列から、狙う節番号と図表番号を読む"""
    import re as _re
    chs = [int(x) for x in _re.findall(r"第\s*\d+\s*章\s*-\s*(\d+)", use or "")]
    figs = [int(m.group(2)) for m in _re.finditer(r"(?:Fig|図)\s*(\d+)-(\d+)", use or "")]
    tbls = [int(m.group(2)) for m in _re.finditer(r"(?:Tbl|表)\s*(\d+)-(\d+)", use or "")]
    return chs, figs, tbls


def collect(ch):
    blocks = []
    for part in ("p1", "p2"):
        blocks += list(importlib.import_module("c%d_%s" % (ch, part)).BLOCKS)
    rows = citeapply.dump_keys(blocks)
    ok = [(h, s) for h, k, i, s in rows
          if not any(w in s for w in NG_WORDS)]
    return blocks, rows, ok


def build(ch, verbose=True):
    blocks, rows, ok = collect(ch)
    keys = {h: s for h, _, _, s in rows}
    cites = {}

    # --- 1) 数字で決まるもの
    num = citematch.suggest(ch, ok, min_hits=2)
    for key, text, cand in num:
        if not cand:
            continue
        if len(cand) == 1 or cand[0][0] > cand[1][0]:
            cites.setdefault(key, [])
            if cand[0][1]["pmid"] not in cites[key]:
                cites[key].append(cand[0][1]["pmid"])

    used = {p for v in cites.values() for p in v}

    # --- 2) 残りを置く。台帳の「用途」が節や図表を指していれば、その節に絞る
    smap, figs, order = sections(ch)
    import re as _re
    left = [r for r in citematch.rows_for(ch) if r["pmid"] not in used]
    weak = []
    for r in left:
        chs, fg, tb = targets(r.get("use", ""))
        want = set()
        for no in chs:
            for sec in order:
                if _re.search(r"第\s*%d\s*章" % no, sec):
                    want.add(sec)
        for no in fg:
            for sec, ff in figs.items():
                if no in ff:
                    want.add(sec)
        pool = [(h, s_) for h, s_ in ok if smap.get(h) in want] if want else []
        best = citematch.best_sentence_for(ch, pool, r["pmid"], top=1) if pool else []
        thr = 0.0
        if not best:
            # 節が分からない、または節の中に近い文がない。章全体から探す。
            best = citematch.best_sentence_for(ch, ok, r["pmid"], top=1)
            thr = WORD_MIN
        if best and best[0][0] >= thr:
            sc, k, s, hit = best[0]
            cites.setdefault(k, [])
            if r["pmid"] not in cites[k]:
                cites[k].append(r["pmid"])
            if verbose:
                print("  語 %5.1f %-9s %s" % (sc, r["sid"], s[:70]))
        else:
            weak.append(r)
            if verbose:
                sc = best[0][0] if best else 0.0
                print("  ** %5.1f %-9s %s" % (sc, r["sid"], r["desc"][:66]))
    return cites, keys, weak


def write(ch, cites, keys):
    src = ['# -*- coding: utf-8 -*-',
           '"""第%s章の引用位置。文のハッシュ → その文で引く PMID。' % "ⅠⅡⅢⅣⅤⅥⅦⅧ"[ch - 1],
           '',
           '本文（c%d_p1.py / c%d_p2.py）は触らず、ここだけで引用を管理する。' % (ch, ch),
           'コメントに文の頭を残してあるので、どの文に付けたかが読める。',
           '"""',
           '',
           'CITES = {']
    for h in sorted(cites, key=lambda x: keys.get(x, "")):
        src.append('    # %s' % keys.get(h, "?").replace('"', "'")[:52])
        src.append('    "%s": [%s],' % (h, ", ".join('"%s"' % p for p in cites[h])))
    src.append('}')
    io.open(os.path.join(HERE, "cites%d.py" % ch), "w",
            encoding="utf-8").write("\n".join(src) + "\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for ch in [int(x) for x in sys.argv[1:]] or list(range(1, 8)):
        print("=== 第%d章" % ch)
        cites, keys, weak = build(ch)
        write(ch, cites, keys)
        n = len({p for v in cites.values() for p in v})
        print("  → %d 文に引用、文献 %d 件、未配置 %d 件" % (len(cites), n, len(weak)))
        for r in weak:
            print("     未配置 %-9s %s" % (r["sid"], r["desc"][:70]))
