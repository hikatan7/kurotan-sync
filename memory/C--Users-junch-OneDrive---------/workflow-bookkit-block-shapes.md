---
name: workflow-bookkit-block-shapes
description: bookkit のブロックは col/sum/note が「行のリスト」。文字列を渡すと1文字1段落になる
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b1b32ccc-9630-41e9-b3f7-0c43af361005
  modified: 2026-09-22T11:35:44.062Z
---

ミニ教科書のビルド（`bookkit.py` + `cNN_pN.py`）で毎回ひっかかる形の話。

**`col` の本文は「段落のリスト」である。** `column(doc, no, title, paras)` は
`paras` を for で回すので、**文字列を渡すと1文字ずつが段落になる**。
㊸で7つのコラムをそうしてしまい、docx の段落が 381 → 2022 に膨らみ、
PDF が 41 頁のはずが **103 頁**になった。`sum` `note` `ul` も同じくリスト。
`p` と `lead` だけが文字列。

**Why:** 見た目のエラーが出ず、PDF の頁数で初めて気づく。頁数を数える前に
`docx.Document(f).paragraphs` の数を既刊と比べると早い（既刊は 350〜550 程度）。

**How to apply:**
- ビルド直後に段落数を見る。桁が違ったら `col`/`sum`/`note` に文字列を渡していないか疑う。
- 丸数字（巻番号）は `volno.py` を使う。本文には `##18` と書き、
  `volno.fix()` で ⑱ に変換する。符号位置を手で書くと取り違える
  （①=U+2460…⑳=U+2473／㉑=U+3251…㉟=U+325F／㊱=U+32B1…）。
  ビルド後に丸数字を正規表現で一覧して符号位置ごと確認する。
- `qa*.py` の `for name in ("figNNa")` は**文字列を1文字ずつ回していて何も検査していない**。
  タプル `("figNNa",)` にする。㊷まではこれで図版検査が空振りしていた。
- `mkledger.py` は出力名（`refsNN.py` と SourceLedger の xlsx 名）が直書き。
  巻をコピーしたら真っ先に直す。引数は見ていない。
- `build_toc.py` は**カレントディレクトリに保存する**ので、実行後にシリーズ直下へ移す。

**`col` のタプルの形が本編と専攻医版で違う。** 本編の build は `("col", "", 題, [段落])`（4要素・column(b[2], b[3])）、
⑦⑱〔52〕の専攻医版 build（v7s 系）は `("col", 題, [段落])`（3要素）。本編の書き方を専攻医版に写すと
題の文字列が段落として1文字ずつ縦に並ぶ（〔52〕専攻医版で発生、20頁→実際は17頁相当）。build_short52.py に assert を入れた。

**Word COM は一度開けなかったファイル名を記憶して、以後 Open が黙って null を返す**（例外も出ない・Documents.Count=0）。
読み取り専用なら開けることもある。**ファイル名を変えてコピーすれば開ける**（総目次で発生、2026-09-24）。

関連: [[workflow-figure-text-fit]] [[workflow-docx-exact-page-count]]
[[project-anesthesia-minitextbook-series]] [[feedback-vancouver-citation-style]]
