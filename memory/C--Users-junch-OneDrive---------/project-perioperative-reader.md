---
name: project-perioperative-reader
description: 『周術期のはじめかた』研修医読本。2026-10-08に流し組み56頁へ作り直し（症例枠なし・図の文字拡大）。生成スクリプトは資料フォルダの_生成スクリプトに保存
metadata:
  type: project
---
置き場：教育ファイル集\総論・基礎\麻酔管理の基礎\研修医のための麻酔科入門\周術期のはじめかた_初期研修医のための麻酔科読本.pdf（旧「_50頁」版はごみ箱へ）。
生成スクリプト：同フォルダの `_生成スクリプト`（engine.py／svglib.py／front.py／ch1〜8.py）。**ビルドは `python build2.py`**（1回目で章の開始頁を測って目次に入れ、2回目を組み、PyMuPDF で柱とノンブルを後入れ）。
- 元は「8章×6頁」の1頁ユニット固定組み。2026-10-08 に Book.page() を章単位の流し組み（.flow、@page 余白 17mm、表紙・目次だけ named page `fixed`）に変え、本文 10.6→11pt、表 9.4/8.6→10/9.6pt、枠 9.8→10.4pt。
- 〈症例〉6か所は患者設定を外した解説枠（pit/mech/pearl）に書き換え。〈計算してみる〉は「計算のしくみ」へ改名。
- 図（インライン SVG 26点）は `figscale.py` が Chrome で文字の外へのはみ出し・重なり・枠超えを実測し、崩れない最大倍率（1.0〜1.3）を figscale.json に書く。svglib.svg() がそれを読む。
- `_flow.py` `_nocase.py` `_topup.py` `_fixbr.py` は適用済みの記録。**再実行しない**（_topup は二重挿入になる）。
- 生成スクリプトは一度 Temp ごと消えていた。会話記録 279dc8db の Write/Edit とシェルでの書き換えを時系列で再生して復元した（改行 CRLF の正規化と、os.chdir の Windows パス置換が必要だった）。
- 番号引用（2026-10-08）：106本・82か所。`_cite_plan.py`（目印文字列→文献キー）を `_cite_apply.py` が適用し、初出順に番号、巻末に参考文献（_refs_html.py）。文献はシリーズ本編の文献一覧（scratchpad の corpus.py で抽出）から引き、シリーズにない7本は PubMed で確認（記憶の PMID は3本とも別論文だった）。LAST「約0.27/1,000」「約1/5」は出典で裏付けられず、⑯の「1万例に1例〜500例に1例」と Di Gregorio 2010 の記述に改めた。62頁。[[feedback-vancouver-citation-style]]
関連：[[feedback-no-page-limits-short-versions]] [[feedback-no-cases-or-quizzes]]
