# -*- coding: utf-8 -*-
"""citesNN.py（文のハッシュ → PMID）の下書きを作る。

使い方（本の _生成スクリプト の中で）:
    python gencites.py <NN> <本文モジュールをカンマ区切り> [出力ファイル]
      例: python gencites.py 22 c22_p1,c22_p2,c22_p3,c22_p4

方針:
  1. 数字が二つ以上一致した文は、それだけで決める（もっとも確か）
  2. 残った文献は、台帳の「教科書での用途」に書いた章番号で節を絞り、
     その中でいちばん語の重なる文に置く
  3. どちらにも掛からなかった文献は「未配置」として並べる（人が決める）
出力はあくまで下書きで、手で直してよい。
"""
import importlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import citeapply
import citematch

# 引用を置かない文（参考文献らしい行、確認できなかった資料の記述）
NG_WORDS = ("確認できなかった", "S-ID", "PMID", "この章で引用した文献", "台帳")
JOURNALS = (r"(Circulation|Resuscitation|Ann Thorac Surg|Anesthesiology|Lancet|JAMA|"
            r"N Engl J Med|Br J Anaesth|Anesth Analg|Obstet Gynecol|BJOG|Crit Care)"
            r"\.?\s*\d{4}")
WORD_MIN = 4.0


def is_ref_like(s):
    return bool(re.search(JOURNALS, s)) or bool(re.search(r"[A-Z][a-z]+ [A-Z]{1,3}\s*ら\.", s))


def collect(mods):
    blocks = []
    for m in mods:
        blocks += list(importlib.import_module(m).BLOCKS)
    rows = citeapply.dump_keys(blocks)
    ok = [(h, s) for h, k, i, s in rows
          if not any(w in s for w in NG_WORDS) and not is_ref_like(s)]
    return blocks, rows, ok


def sections(blocks):
    cur = ""
    smap = {}
    order = []
    for b in blocks:
        if b[0] == "h2":
            cur = b[1]
            order.append(cur)
        if b[0] == "p":
            src = [b[1]]
        elif b[0] == "ul":
            src = list(b[1])
        elif b[0] in ("summary", "note", "sum"):
            src = list(b[2]) if len(b) > 2 else []
        else:
            continue
        for t in src:
            if not isinstance(t, str):
                continue
            for x in citeapply.split_sents(t):
                smap[citeapply.h(x)] = cur
    return smap, order


def run(no, mods, out=None):
    blocks, rows, ok = collect(mods)
    keys = {h: s for h, _, _, s in rows}
    cites = {}
    for key, text, cand in citematch.suggest(None, ok, min_hits=2):
        if not cand:
            continue
        if len(cand) == 1 or cand[0][0] > cand[1][0]:
            cites.setdefault(key, [])
            if cand[0][1]["pmid"] not in cites[key]:
                cites[key].append(cand[0][1]["pmid"])
    used = {p for v in cites.values() for p in v}
    smap, order = sections(blocks)
    weak = []
    for r in citematch.rows_for(None):
        if r["pmid"] in used:
            continue
        nos = [int(x) for x in re.findall(r"第\s*(\d+)\s*章", r.get("use") or "")]
        want = set()
        for n in nos:
            for sec in order:
                if re.search(r"第\s*%d\s*章" % n, sec):
                    want.add(sec)
        pool = [(h, s) for h, s in ok if smap.get(h) in want] if want else []
        best = citematch.best_sentence_for(None, pool, r["pmid"], top=1) if pool else []
        thr = 0.0
        if not best:
            best = citematch.best_sentence_for(None, ok, r["pmid"], top=1)
            thr = WORD_MIN
        if best and best[0][0] >= thr:
            sc, k, s, hit = best[0]
            cites.setdefault(k, [])
            if r["pmid"] not in cites[k]:
                cites[k].append(r["pmid"])
        else:
            weak.append(r)
    total = len(citematch.rows_for(None))
    print("文 %d / 引用を置いた文 %d / 文献 %d（台帳 %d）/ 未配置 %d"
          % (len(rows), len(cites), len({p for v in cites.values() for p in v}),
             total, len(weak)))
    for r in weak:
        print("   未配置 %-8s %s" % (r["sid"], r["desc"][:66]))
    src = ['# -*- coding: utf-8 -*-',
           '"""第%s巻の引用位置。文のハッシュ → その文で引く PMID。' % no,
           '',
           '本文は触らず、ここだけで引用を管理する。',
           '"""', '', 'CITES = {']
    for h in sorted(cites, key=lambda x: keys.get(x, "")):
        src.append('    # %s' % keys.get(h, "?").replace('"', "'")[:52])
        src.append('    "%s": [%s],' % (h, ", ".join('"%s"' % p for p in cites[h])))
    src.append('}')
    path = out or os.path.join(os.getcwd(), "cites%s.py" % no)
    io.open(path, "w", encoding="utf-8").write("\n".join(src) + "\n")
    print("→", path)
    return cites, keys, weak


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, os.getcwd())
    run(sys.argv[1], sys.argv[2].split(","),
        sys.argv[3] if len(sys.argv) > 3 else None)
