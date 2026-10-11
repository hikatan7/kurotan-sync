# -*- coding: utf-8 -*-
"""意図した文献をタイトル検索で PubMed から引き当てる。
入力 TSV: key <TAB> 検索語（タイトルの一部＋著者・雑誌でも可）
出力: key / PMID / 第一著者 / 誌名 / 年 / 実物タイトル  を上位3件。
"""
import json, sys, time, urllib.parse, urllib.request

E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def get(url):
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            err = e
            time.sleep(1.5)
    raise err

def search(q, n=3):
    u = E + "esearch.fcgi?db=pubmed&retmode=json&retmax=%d&sort=relevance&term=%s" % (
        n, urllib.parse.quote(q))
    return get(u)["esearchresult"].get("idlist", [])

def summ(ids):
    if not ids:
        return {}
    u = E + "esummary.fcgi?db=pubmed&retmode=json&id=" + ",".join(ids)
    return get(u)["result"]

sys.stdout.reconfigure(encoding="utf-8")
rows = [l.rstrip("\n") for l in open(sys.argv[1], encoding="utf-8")
        if l.strip() and not l.startswith("#")]
for ln in rows:
    key, q = ln.split("\t", 1)
    try:
        ids = search(q)
    except Exception as e:
        print("%s\tERROR\t%s" % (key, e)); continue
    d = summ(ids)
    if not ids:
        print("%s\tNONE\t%s" % (key, q)); continue
    for u in ids:
        r = d.get(u, {})
        au = r["authors"][0]["name"] if r.get("authors") else ""
        print("%s\t%s\t%s\t%s\t%s\t%s" % (
            key, u, au, r.get("source", ""), str(r.get("pubdate", ""))[:4],
            r.get("title", "").replace("\t", " ")))
    print("-")
    time.sleep(0.4)
