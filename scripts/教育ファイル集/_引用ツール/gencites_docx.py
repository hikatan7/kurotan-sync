# -*- coding: utf-8 -*-
"""docx から取り出した文と台帳を突き合わせ、引用位置の下書きを作る。

    python gencites_docx.py <sents.tsv> <台帳 xlsx> <シート名> <出力 json>

  1. 数字が二つ以上一致した文は、それで決める
  2. 残った文献は、台帳の「教科書での用途」に書いた章番号で節を絞り、
     その中でいちばん語の重なる文へ置く
  3. どちらにも掛からなかったものは「未配置」として並べる
"""
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import citematch

JOURNALS = (r"(Circulation|Resuscitation|Ann Thorac Surg|Anesthesiology|Lancet|JAMA|"
            r"N Engl J Med|Br J Anaesth|Anesth Analg|Obstet Gynecol|BJOG|Crit Care|"
            r"J Thromb Haemost|Anaesthesia|Br J Surg)\.?\s*;?\s*\d{4}")
WORD_MIN = 4.0


def load_rows(ledger, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(ledger, read_only=True, data_only=True)
    ws = wb[sheet]
    head = None
    out = []
    for row in ws.iter_rows(values_only=True):
        if head is None:
            head = [str(c or "") for c in row]
            idx = {h: i for i, h in enumerate(head)}
            continue
        if not row or not row[0]:
            continue
        def g(k):
            i = idx.get(k)
            v = row[i] if i is not None and i < len(row) else None
            return "" if v is None else str(v).strip()
        m = re.search(r"(\d{7,9})", g("PMID（リンク）"))
        key = m.group(1) if m else g("S-ID")
        if not key:
            continue
        blob = " ".join([g("対象・症例数"), g("主要結果・メッセージ"), g("タイトル")])
        use = g("教科書での用途")
        out.append({"pmid": key, "sid": g("S-ID"), "blob": blob,
                    "use": use, "toks": citematch.toks(blob),
                    "words": citematch.words(blob + " " + use),
                    "desc": "%s %s %s" % (g("年"), g("筆頭著者/学会"), g("タイトル")[:60])})
    wb.close()
    return out


def score(w, rw, df, n):
    hit = w & rw
    if not hit:
        return 0.0
    return sum(math.log(1.0 + n / (1.0 + df.get(x, 1))) for x in hit)


def run(tsv, ledger, sheet, out):
    sents = []
    for l in io.open(tsv, encoding="utf-8"):
        p = l.rstrip("\n").split("\t")
        if len(p) < 3:
            continue
        if re.search(JOURNALS, p[2]) or re.search(r"[A-Z][a-z]+ [A-Z]{1,3}, .*et al\.", p[2]):
            continue
        sents.append((p[0], p[1], p[2]))
    rows = load_rows(ledger, sheet)
    cites = {}

    # 1) 数字
    for h, sec, s in sents:
        pt = citematch.toks(s)
        if not pt:
            continue
        cand = []
        for r in rows:
            hit = pt & r["toks"]
            if len(hit) >= 2:
                cand.append((len(hit), r))
        cand.sort(key=lambda x: -x[0])
        if cand and (len(cand) == 1 or cand[0][0] > cand[1][0]):
            cites.setdefault(h, [])
            if cand[0][1]["pmid"] not in cites[h]:
                cites[h].append(cand[0][1]["pmid"])
    used = {p for v in cites.values() for p in v}

    # 2) 語の重なり（章で絞る）
    df = {}
    sw = []
    for h, sec, s in sents:
        w = citematch.words(s)
        sw.append((h, sec, s, w))
        for x in w:
            df[x] = df.get(x, 0) + 1
    n = max(1, len(sw))
    weak = []
    for r in rows:
        if r["pmid"] in used:
            continue
        nos = [int(x) for x in re.findall(r"第\s*(\d+)\s*章", r["use"] or "")]
        pool = [t for t in sw
                if any(re.search(r"第\s*%d\s*章" % no, t[1] or "") for no in nos)] if nos else []
        cands = [(score(t[3], r["words"], df, n), t) for t in (pool or sw)]
        cands.sort(key=lambda x: -x[0])
        thr = 0.0 if pool else WORD_MIN
        if cands and cands[0][0] >= thr and cands[0][0] > 0:
            h = cands[0][1][0]
            cites.setdefault(h, [])
            if r["pmid"] not in cites[h]:
                cites[h].append(r["pmid"])
        else:
            weak.append(r)
    txt = {h: s for h, sec, s in sents}
    print("文 %d / 引用を置いた文 %d / 文献 %d（台帳 %d）/ 未配置 %d"
          % (len(sents), len(cites), len({p for v in cites.values() for p in v}),
             len(rows), len(weak)))
    for r in weak:
        print("   未配置 %-8s %s" % (r["sid"], r["desc"][:66]))
    json.dump({"cites": cites, "text": txt}, io.open(out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)
    print("→", out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
