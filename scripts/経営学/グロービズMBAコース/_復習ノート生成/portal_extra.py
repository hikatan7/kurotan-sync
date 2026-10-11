"""経営学ポータルに統合する追加データ（2026-09-24）
- 経営学テキスト：本文の見出しと柱（「第N 章 …｜」）から章を、しおり／見出しの文字サイズから節を取り出す
  （しおりは本によって章が抜けているので、章はしおりに頼らない）
- MBA用語・フレームワーク事典.html：埋め込みデータ（DATA／CATS）をそのまま取り込む"""
import json, os, re
from collections import Counter
import fitz

CH = re.compile(r"^(序章|終章(?!要点)|第\s*[0-9０-９]+\s*章|第\s*[ⅠⅡⅢⅣⅤⅥ]+\s*部|第\s*[IV]+\s*部|付録[A-ZＡ-Ｚ]|巻末資料)")
HEAD = re.compile(r"^(序章|終章|巻末資料|付録\S)|^第\s*\S+\s*[章部](\s|$)")
SUBLIKE = re.compile(r"補強モジュール|補助モジュール|実践ワークブック")
GENERIC = re.compile(r"^(章の要点|次章への橋渡し|学習目標|要点|まとめ|用語の解説|概念の説明|フレームワークの説明|歴史と変遷|企業・組織の例|目\s*次|本書の凡例|凡例|改訂版について|全体構成|本書の使い方|手本に近づける|章末要点|確認問題|実践ワークブック|\d+\.\s)")


def _clean_book(name):
    t = re.sub(r"\.(pdf|docx)$", "", name)
    t = t.replace("急性期病院で学ぶ_", "").replace("_YuGothic_A4_目次・統一スタイル", "").replace("_本文12pt版", "")
    return t.replace("_", " ")


def _lines(doc):
    out = []
    for pn, p in enumerate(doc):
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = "".join(s["text"] for s in l["spans"]).strip()
                if t:
                    out.append((round(max(s["size"] for s in l["spans"]), 1), t, pn + 1))
    return out


def _key(t):
    t = re.sub(r"\s+", "", t)
    m = re.match(r"(序章|終章|巻末資料|第[0-9０-９]+章|第[ⅠⅡⅢⅣⅤⅥIV]+部|付録[A-ZＡ-Ｚ])", t)
    return m.group(1) if m else t[:20]


def _chapters(L):
    # 目次の頁（章見出しが3つ以上並ぶ頁、リーダー点のある行）を除く
    per = Counter(p for s, t, p in L if CH.match(t) and "｜" not in t)
    last = max(p for s, t, p in L)
    # 目次＝「目次」の見出しがある頁と、そこから続く章見出しの多い頁
    toc_pages = set()
    starts = sorted({p for s, t, p in L if re.match(r"^目\s*次$", t)})
    for st in starts:
        q = st
        toc_pages.add(q)
        while per.get(q + 1, 0) >= 2:
            q += 1; toc_pages.add(q)
    # 「目次」の見出しがない一覧頁（全体構成など）：前半にあって章見出しが4つ以上並ぶ頁
    toc_pages |= {p for p, n in per.items() if n >= 4 and p <= max(12, last * 0.12)}
    big = {}
    for s, t, p in L:
        if p in toc_pages or "…" in t or "...." in t or "｜" in t or SUBLIKE.search(t):
            continue
        if CH.match(t) and HEAD.match(t) and len(re.sub(r"\s", "", t)) >= 4:
            k = _key(t)
            if k not in big or s > big[k][0]:
                big[k] = (s, t, p)
    # 見出しの文字サイズが本文より小さい誤検出を落とす：その本の章見出しで最多のサイズ以上
    if big:
        top = Counter(v[0] for v in big.values()).most_common(1)[0][0]
        low = {k: v for k, v in big.items() if v[0] < min(top, 14.0)}
        big = {k: v for k, v in big.items() if v[0] >= min(top, 14.0)}
        # 見出しが小さい字で組まれた章（例：ファイナンス第2・3・11章）を補う。巻末の索引頁は除く
        for k, v in low.items():
            if k not in big and v[2] < last - 3 and v[0] >= 12:
                big[k] = v
    ch = {k: {"t": v[1], "p": v[2], "l": 1} for k, v in big.items()}
    # 柱「第N 章 タイトル ｜ 読み物 …」の初出頁（見出しのない章を補う）
    for s, t, p in L:
        m = re.match(r"(第\s*\d+\s*章\s*[^｜]+?)\s*｜", t)
        if m and p not in toc_pages:
            k = _key(m.group(1))
            if k not in ch:
                ch[k] = {"t": m.group(1).strip(), "p": max(p - 1, 1), "l": 1}
    return sorted(ch.values(), key=lambda c: c["p"])


def _sections(doc, L, chs):
    toc = [(lv, t.strip(), pg) for lv, t, pg in doc.get_toc() if lv >= 2 and pg > 0]
    toc = [(t, pg) for lv, t, pg in toc if lv == 2 and not GENERIC.match(t)]
    if len(toc) >= max(10, 3 * len(chs)):
        return [{"t": t, "p": pg, "l": 2} for t, pg in toc]
    ch_sizes = {s for s, t, p in L if CH.match(t)}
    body = Counter(s for s, t, p in L).most_common(1)[0][0]
    cand = Counter(s for s, t, p in L if s > body + 2 and s not in ch_sizes)
    for s, n in sorted(cand.items(), key=lambda x: -x[1]):
        if 10 <= n <= 400:
            return [{"t": t, "p": p, "l": 2} for sz, t, p in L if sz == s and not GENERIC.match(t)
                    and p >= (chs[0]["p"] if chs else 1)]
    return []


def text_books(tx_dir, href):
    books = []
    files = sorted(os.listdir(tx_dir))
    for f in files:
        if not f.lower().endswith(".pdf"):
            continue
        p = os.path.join(tx_dir, f)
        d = fitz.open(p)
        L = _lines(d)
        chs = _chapters(L)
        secs = _sections(d, L, chs)
        allc = sorted(chs + secs, key=lambda c: (c["p"], c["l"]))
        docx = f[:-4] + ".docx"
        books.append({"n": _clean_book(f), "h": href(p), "pages": len(d), "ch": allc,
                      "docx": href(os.path.join(tx_dir, docx)) if docx in files else ""})
    return books


def dictionary(path):
    s = open(path, encoding="utf-8").read()
    data = json.loads(re.search(r"const DATA = (\[.*?\]);\s*\n", s, re.S).group(1))
    cats = json.loads(re.search(r"CATS = (\[.*?\]);", s, re.S).group(1))
    keep = ("id", "cat", "name", "en", "oneline", "purpose", "parts", "steps", "pitfall", "who", "src", "etym", "tags")
    return {"cats": cats, "items": [{k: x.get(k) for k in keep} for x in data]}
