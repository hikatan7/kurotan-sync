---
name: workflow-docx-exact-page-count
description: 「◯ページちょうど」のWord資料を作るときの詰め方と、余分な空白ページの正体
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c7a2f6f3-3622-4fc4-be06-b73729ec6941
  modified: 2026-08-17T05:40:08.526Z
---

python-docx で「10ページちょうど」を要求されたときの手順。

1. まず内容を書き切り、Word COM で PDF 化して `ComputeStatistics(2)` でページ数を測る。
2. 溢れている場所は PyMuPDF の `page.get_text('blocks')` の **maxY** で特定する。
   A4・下余白10mm なら本文下端は約 y=814pt。行数だけ数えても当たらない。
3. 削るより先に**版面を詰める**ほうが効く。本文 9pt→8.5pt、行間 1.06→1.02、
   表 8pt→7.5pt、余白 14mm→13mm で約15%圧縮できた（14頁→11頁）。
4. `Document.add_page_break()` は**空段落を1つ挿入する**ので、直前ページが埋まっていると
   空白ページが1枚生まれる。見出し段落に `w:pageBreakBefore` を直接付ければ起きない。

**既存 docx の空白ページを一括で潰す**（2026-09-04にミニ教科書シリーズ全巻で実施）。
scratchpad の `fix_blank.py`：
- `fix()` … ①改ページだけの空段落が連続していたら1つ残す ②改ページ段落の直前の空段落を落とす
- `to_page_break_before()` … **改ページだけの空段落を、次の段落の `w:pageBreakBefore` に置き換える。**
  これが本命。空段落は1行分の高さを持つので、直前ページが埋まっていると空段落だけが
  次頁に落ちて白紙になる。pageBreakBefore は高さを持たないので構造的に起きない。
  次が表のときは置換できないのでそのまま残す。
- 順番に注意：`fix()` の空段落削除で**新しく改ページが隣接する**ことがあるので、
  `fix()` → `to_page_break_before()` の順に両方かけること。
- 点検は `scan_blank.py`（PDFの全ページで `get_text()` が空かつ画像0を空白と判定）。
  略語一覧の挿入（[[workflow-abbreviation-expansion]]）で表紙直後に空白が入っていた巻が4つあった。

**Why:** 段落単位で削る作業を延々と繰り返しても収束しない。密度を先に上げてから局所を削るほうが速く、
最後の1ページは改ページの実装で決まることが多い。
**How to apply:** 教科書・サマリ資料でページ数指定があるときはこの順で。環境は [[env-word-com-doc-generation]]。
