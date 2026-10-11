# -*- coding: utf-8 -*-
"""候補PMIDの実物タイトルを PubMed esummary で確認する。"""
import json, sys, time, urllib.request

CAND = sys.argv[1]
ids = []
intent = {}
for ln in open(CAND, encoding="utf-8"):
    ln = ln.strip()
    if not ln or ln.startswith("#"):
        continue
    pmid, memo = ln.split("\t", 1)
    ids.append(pmid.strip())
    intent[pmid.strip()] = memo.strip()

URL = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
       "?db=pubmed&retmode=json&id=%s")
out = []
for i in range(0, len(ids), 40):
    chunk = ids[i:i + 40]
    with urllib.request.urlopen(URL % ",".join(chunk), timeout=60) as r:
        d = json.load(r)["result"]
    for u in chunk:
        rec = d.get(u)
        if not rec or "error" in rec:
            out.append("%s\tNOT_FOUND\t\t\t%s" % (u, intent[u]))
            continue
        au = rec["authors"][0]["name"] if rec.get("authors") else ""
        out.append("%s\t%s\t%s\t%s\t%s\t%s" % (
            u, au, rec.get("source", ""), rec.get("pubdate", "")[:4],
            rec.get("title", "").replace("\t", " "), intent[u]))
    time.sleep(0.4)
sys.stdout.reconfigure(encoding="utf-8")
print("\n".join(out))
