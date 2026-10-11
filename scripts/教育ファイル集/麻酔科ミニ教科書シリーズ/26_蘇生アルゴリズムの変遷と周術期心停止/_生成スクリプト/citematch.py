# -*- coding: utf-8 -*-
"""本文の段落と文献台帳を、数字の一致で突き合わせて引用位置を提案する。

数値は捏造できないので、段落に出てくる特徴的な数字が台帳の「主要結果」に
あるかどうかで対応づける。提案は必ず目で確かめてから採用する。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SHEET_OF_CH = {26: "㉖_蘇生と周術期心停止"}

# 「3.42 倍」「95%CI 0.31〜0.97」「1:8,200」「7,635 例」などを拾う
NUM = re.compile(r"\d[\d,]*\.\d+|\d[\d,]{2,}|\d+\.\d+|\b\d{2,}\b")
# ありふれた数字は照合に使わない
STOP = {"95", "100", "0", "1", "2", "3", "4", "5", "10", "20", "30", "50",
        "2024", "2025", "2026", "2023", "2022", "2021", "2020", "2019",
        "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011",
        "2010", "24", "12", "48", "60", "65", "70", "75", "80", "90"}


def toks(s):
    out = set()
    for m in NUM.finditer(s or ""):
        t = m.group(0).replace(",", "")
        if t in STOP or len(t) < 2:
            continue
        out.add(t)
    return out


def rows_for(ch):
    """台帳の該当シートから（PMID, S-ID, 照合用テキスト, 短い説明）"""
    import openpyxl
    wb = openpyxl.load_workbook(
        os.path.join(HERE, "..", "蘇生アルゴリズム_SourceLedger.xlsx"),
        read_only=True, data_only=True)
    ws = wb[SHEET_OF_CH[ch]]
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
        if not m:
            continue
        blob = " ".join([g("対象・症例数"), g("介入／比較"),
                         g("主要結果・メッセージ"), g("タイトル")])
        out.append({"pmid": m.group(1), "sid": g("S-ID"), "blob": blob,
                    "toks": toks(blob),
                    "desc": "%s %s %s" % (g("年"), g("筆頭著者/学会"),
                                          g("タイトル")[:60]),
                    "use": g("教科書での用途") or g("教科書での用途（章／図／表／アルゴリズム）")})
    wb.close()
    return out


def suggest(ch, paragraphs, min_hits=2):
    """paragraphs: [(識別子, 本文)] -> [(識別子, 本文, [(スコア, row, 一致した数字)])]"""
    lg = rows_for(ch)
    res = []
    for key, text in paragraphs:
        pt = toks(text)
        if not pt:
            res.append((key, text, []))
            continue
        cand = []
        for r in lg:
            hit = pt & r["toks"]
            if len(hit) >= min_hits:
                cand.append((len(hit), r, sorted(hit)))
        cand.sort(key=lambda x: -x[0])
        res.append((key, text, cand[:3]))
    return res


# ---------------- 語の重なりで合わせる（数字の少ない章むけ） ----------------
KATA = re.compile(r"[ァ-ヴー]{3,}")
LATIN = re.compile(r"[A-Za-z][A-Za-z0-9\-]{2,}")
KANJI = re.compile(r"[一-龥]{2,4}")


def words(s):
    s = s or ""
    out = set()
    out |= {m.group(0) for m in KATA.finditer(s)}
    out |= {m.group(0).lower() for m in LATIN.finditer(s)}
    out |= {m.group(0) for m in KANJI.finditer(s)}
    out |= toks(s)
    return out


def suggest_by_words(ch, sentences, top=3):
    """sentences: [(キー, 文)]。語の重なり（希少語を重く）で台帳行を推す。"""
    import math
    lg = rows_for(ch)
    for r in lg:
        r["words"] = words(r["blob"] + " " + r.get("use", ""))
    # 文の側で何回出る語かを数え、ありふれた語を軽くする
    df = {}
    sw = []
    for k, s in sentences:
        w = words(s)
        sw.append((k, s, w))
        for x in w:
            df[x] = df.get(x, 0) + 1
    n = max(1, len(sentences))
    res = []
    for k, s, w in sw:
        cand = []
        for r in lg:
            hit = w & r["words"]
            if not hit:
                continue
            sc = sum(math.log(1.0 + n / (1.0 + df.get(x, 1))) for x in hit)
            if sc > 0:
                cand.append((sc, r, sorted(hit, key=lambda x: -df.get(x, 1))[:8]))
        cand.sort(key=lambda x: -x[0])
        res.append((k, s, cand[:top]))
    return res


def best_sentence_for(ch, sentences, pmid, top=5):
    """ある文献に最も近い文を探す（引用位置を決めるとき用）"""
    import math
    lg = {r["pmid"]: r for r in rows_for(ch)}
    r = lg[pmid]
    rw = words(r["blob"] + " " + r.get("use", ""))
    df = {}
    sw = []
    for k, s in sentences:
        w = words(s)
        sw.append((k, s, w))
        for x in w:
            df[x] = df.get(x, 0) + 1
    n = max(1, len(sentences))
    out = []
    for k, s, w in sw:
        hit = w & rw
        if not hit:
            continue
        sc = sum(math.log(1.0 + n / (1.0 + df.get(x, 1))) for x in hit)
        out.append((sc, k, s, sorted(hit, key=lambda x: -df.get(x, 1))[:8]))
    out.sort(key=lambda x: -x[0])
    return out[:top]
