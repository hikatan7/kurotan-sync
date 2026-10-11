---
name: feedback-vancouver-citation-style
description: 教科書・テキストは本文に肩付き番号、巻末に番号順の参考文献一覧（バンクーバー方式）を必ず付ける
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 585edbaa-4ad2-4d47-b0c9-dc8724e340b8
  modified: 2026-09-17T14:38:27.090Z
---

**教材はすべて番号引用（バンクーバー方式）で統一する。** 本文の該当箇所に肩付きの番号を打ち、
テキストの最後に番号順の参考文献一覧を並べる。出典のないテキストは作らない。
2026-09-17 に「出典、参考文献を必ず入れて。引用した文中に数字で肩に入れ、テキストの最後に番号で
参考文献一覧を並べる文献スタイルを貫いて」「例えば心肺蘇生のテキストには全く参考文献やガイドラインがない」
「このようなテキストがないかどうかを全てのテキストで確認してやり直して」と指示された。

**Why:** 数字や推奨を書いた以上、読者が原典に戻れなければ教材として使えない。
付録に文献表を置くだけでは、どの記述がどの文献に由来するか分からない。

**How to apply:**
- 仕組みは `高度心臓血管麻酔\_生成スクリプト` にある。本文に `{{PMID}}`（複数は `{{a,b}}`）と書くと、
  `bookkit._run_with_cites` が出現順の番号を肩付きで描き、`citekit.Cites` が章末一覧を作る。
  連番は `1-3,7` のように畳む。書誌は文献台帳 xlsx の全シートから PMID をキーに引く。
- **台帳にない PMID は KeyError で落とす**（strict）。出典を確認していない引用を通さないための仕掛け。
- 台帳のない既刊に付けるときは、まず PubMed E-utilities で文献を確認して台帳を作る。
  抄録の RESULTS/CONCLUSIONS から数値を採り、著者・雑誌・年・PMID・DOI が揃ったものだけ使う。
- 学会ガイドラインなど PMID のない一次資料は、台帳に別 ID で登録し、発行者・年・版・URL を書く。
- **既刊は docx を直接いじる**（生成スクリプトの作りが本ごとに違うため）。道具は
  `教育ファイル集\_引用ツール`（dumpdocx → mkledger → gencites_docx → applycites → topdf.ps1）。
- **台帳を確定する前に、PMID ごとに「意図した内容」と PubMed の実物タイトルを
  一行ずつ突き合わせる。** ㉘では初回の台帳で1件が全く別の論文（喘息の呼吸抵抗解析）
  だった。検索で拾った ID をそのまま載せると気づけない。
- **自動配置は章見出しの行に番号を落とす。** 見出しに付いた分は必ず本文の文へ移す。
- **docx の sectPr を消さないこと。** 消すと Word が既定余白に戻し docGrid に type="lines" を付けるため、
  78頁の本が119頁に膨らむ。番号はそのままで一覧だけ作り直すなら `citedocx.redo_refs`。


関連: [[project-advanced-cv-anesthesia-ledger]] [[feedback-verify-ai-supplied-urls]]
[[project-anesthesia-minitextbook-series]] [[feedback-links-must-be-excel]]
