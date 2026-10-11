---
name: project-mba-critical-thinking-textbook
description: 急性期病院で学ぶMBAクリティカル・シンキング（61頁・全31章）。経営学テキストの7冊目、グロービス受講記録からの再構成
metadata: 
  node_type: memory
  type: project
  originSessionId: 3e0596e4-0b8b-40e2-b23d-72acda33abcc
  modified: 2026-09-21T16:34:00.279Z
---

デスクトップ `経営学\経営学テキスト\急性期病院で学ぶ_MBAクリティカル・シンキング.docx / .pdf`（2026-09-22、61頁・全31章・図版8点・演習5題・番号引用22件）。既刊6冊（アカウンティング／ファイナンス／マーケティング／組織行動／ビジネスアナリティクス／テクノベート）に続く7冊目。

**中身の作り：** 第Ⅰ〜Ⅳ部がグロービス講義6日間（Day1〜6、資料641頁）の再構成、**第Ⅴ部が補講**（システム1/2、トゥールミン、誤謬カタログ、因果、ダブルループ、診断エラー）、第Ⅵ部が復習・演習。題材はすべて手術室・病院管理に置き換え、講義資料の文言は引き写していない。

**Why:** 「手元資料のまとめ＋補足すべき知識を1冊に」という依頼。講義は思考の型までしか扱わないので、その背景（なぜ即答するのか、因果をどう言うのか）を一次文献で補うと独習用に完結する。

**How to apply:**
- 生成物は `経営学テキスト\_生成スクリプト`（bookkit.py／figlib.py は麻酔ミニ教科書シリーズから複製、p1〜p6.py が本文、refs.py が文献台帳、figs.py が作図、build.py、to_pdf.ps1）
- **章は流して組む**。h2 ごとに改ページすると章末まとめだけの頁が17枚でき79頁に膨らんだ。部（h1）と付録だけ改ページで61頁
- 引用は PMID/DOI/ISBN まで実在確認したものだけ（PubMed E-utilities と Crossref API を curl で叩く方式が速い）
- 図版は figlib の textbox が返す高さを使って次の要素を置く。固定オフセットで置くと下端が切れる（f02・f05・f06 で再発）
- 日本語の本文に別言語の単語が紛れる事故が3回起きた（четыре／диагностика／signal）。書き上げたら `[Ѐ-ӿ]` 等で全ファイルを走査する

残りの必修4冊は 2026-10-07 に作成済み → [[project-mba-required-four-books]]

関連: [[project-globis-mba-folder]] [[project-anesthesia-minitextbook-series]] [[feedback-vancouver-citation-style]] [[workflow-figure-text-fit]]
