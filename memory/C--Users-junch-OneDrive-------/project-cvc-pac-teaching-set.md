---
name: project-cvc-pac-teaching-set
description: CVC/PAC統合教材3点セット（専門医版87頁docx・研修医版31頁docx・58枚pptx）の保管場所と作成方針
metadata: 
  node_type: memory
  type: project
  originSessionId: 56e43c50-08c5-4112-8bfe-aac6f92e0ae6
  modified: 2026-08-14T03:44:03.726Z
---

**2026-08-14に「学習ファイル\医学\00_麻酔科ミニ教科書シリーズ\06_中心静脈カテーテル・肺動脈カテーテル」へ移動**し、
シリーズ第⑥巻になった（旧置き場 02_血管アクセス・カテーテル管理\統合教材_CVC-PAC は空）。
表紙はシリーズ共通仕様に差し替え済み → [[project-anesthesia-minitextbook-series]]。

- 中心静脈カテーテル・肺動脈カテーテル完全マニュアル_専門医版.docx（87頁／約62,000字／表18）
- CVC・PAC実践ハンドブック_研修医専攻医版.docx（31頁）
- CVC・PAC安全講義_研修医専攻医看護師版.pptx（58枚、全スライドにノート）
- **CVC・PAC安全講義_40枚版.pptx ＋ 同.pdf**（2026-08-14。58枚を1枚あたりの密度を上げて40枚へ圧縮。
  章扉スライドを廃し、全スライドに Part 帯とページ番号。[[project-pptxlib-slide-engine]] で生成）

準拠した一次資料：医療事故調査・支援センター提言 第1号／第17号（12提言・CVC死亡55例）／第19号（PAC死亡9例・8提言）、日本心臓血管外科学会＋日本心臓血管麻酔学会 合同ステートメント2020、日本麻酔科学会 プラクティカルガイド2017、CDC 2011／SHEA・IDSA 2022、INS Standards 9th ed. 2024、MAGIC 2015。

引用元10ファイルはデスクトップ「引用済みファイル」へ退避済み（[[env-onedrive-desktop-file-ops]] の手順でハッシュ照合）。結果として「03_肺動脈カテーテル_PAC」フォルダは空になった。

**Why:** 提言17号・19号の提言本文はPDFがテキスト抽出可能なので、改訂時はWebFetchでPDFを落としてfitzで抽出すれば原文どおり引用できる（Zero-Harm_CVC_Protocol.pdfのみ画像PDFでfitz不可→fitzでPNG化してRead）。

**How to apply:** 改訂は scratchpad の book_01〜05.txt／short_01.txt＋build_docx.py、build_pptx.py と同じ自作マークアップ方式で再生成する。この端末にはnode/pptxgenjsもLibreOfficeも無いため、pptxはpython-pptx、視覚QAはPowerPoint COMの `SaveCopyAs(path.png, 18)` でスライド画像を書き出して確認する（[[env-word-com-doc-generation]]）。
