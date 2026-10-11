---
name: project-resuscitation-history-deck
description: 蘇生の歴史12枚（Slidesアーティファクト）。アルゴリズム変遷9枚＋2025年版と見通し＋蘇生教育史2枚、通し番号引用44件
metadata:
  node_type: memory
  type: project
  originSessionId: b515f003-9740-4636-8202-026b589a1df8
  modified: 2026-09-27T05:42:30.207Z
---

2026-09-27 作成。claude.ai の Slides アーティファクト「蘇生の60年 ― アルゴリズムの変遷と蘇生教育」
https://claude.ai/artifact/M2RkCVuUFShqNQ8uxNVkrE （pptx/PDF はページの書き出しから）。

- 構成：表紙／1960年の合流／1966–97（市民に教えない→救命の連鎖・ILCOR）／2000（削除理由3つ・Class/LOE）／
  2005–15（30:2・C-A-B・上限）／薬の引き算＋PARAMEDIC2／2020（回復・6/491）／2025の数字（760・LOE A 11）／
  2025の変更点／見通し3つ（随時改訂・予防の鎖・装置は証拠待ち）／教育史①1960–2002／教育史②2005–2025。
- 材料は㉖ [[project-resuscitation-textbook-26]] の本文と SourceLedger。教育史用に11本を Europe PMC で確認して追加
  （Sim One 1969、Harvey 1974、Gaba 1988、ACRM 1992、ICLS Okudera 2011、Issenberg 2005、Wayne 2006/2008、
  Andreatta 2011、McGaghie 2011、Sutton 2011、Hunt 2014、Cheng 2018、Donoghue 2025）。
- ㉖は C-A-B の出典に Link 2010（電気治療の部）を当てていたが、スライドでは Berg 2010 Part 5 に差し替えた。
- 2026-09-27 時点で PubMed E-utilities が 500 を返した。書誌確認は Europe PMC REST（`EXT_ID:<pmid> AND SRC:MED`）で代替できる。
- **PDF版**：`教育ファイル集\テーマ別スライド集\11_蘇生の60年_アルゴリズムの変遷と蘇生教育_講義スライド12枚.pdf`（2026-09-27）。
  ポータルでは「心肺蘇生・急変対応」テーマの要点解説プレゼン。作り方は、slides/*.html を1枚のHTMLにまとめ
  （aside除去、p/h のmargin・tableの罫線をCSSで補う）、Chrome headless の --print-to-pdf（@page 1920×1080px）で書き出す。
  アーティファクトを直したら、PDFも同じ手順で作り直す。
- **2026-09-27 改訂**：教育史の2枚をインストラクター向けに作り直した。①「代表格として育った」＝広める→標準化→成果で問う＋代表格の4条件（くろたんの整理）＋Cook 2011（609研究）/Mundell 2013（蘇生182研究・16,636人）。②T1→T2→T3（McGaghie 2010）の実例＋教える五原則（Cheng 2018・AHA 2025 Part 12）＋生存の公式（Søreide 2013）。引用は45件に。
- 「蘇生教育が最もデータが大きい」は比較文献が未確認。検証用の横断検索プロンプトを `自作ファイル集\プロンプト集\26_蘇生教育はシミュレーション教育の代表格か_横断検索.html` に作成。比較相手は CVC のマスタリー・ラーニング、産科急変訓練など。結果が来たら照合してスライドの言い方を決める。
- **2026-09-27 14枚化**：ユーザーの依頼で、教育史2枚の後ろに15枚版（[[project-resus-education-lab-deck]]）の11枚目（AHA 2025 Part 12 推奨表）と15枚目（経験を教育に変える8つの手順）を移植し、全14枚に。文献は通しで48件（Bhanji 2010/2015・Cheng 2020 を46–48に追加）。PDFは `テーマ別スライド集\11_蘇生の60年_…_講義スライド14枚.pdf`（12枚版は削除）。
- **用語欄**（2026-09-27）：2〜14枚目の下の空白に「用語」欄（略語の日本語解説、24px・薄いベージュ地、`data-gloss="1"`）。生成は scratchpad の gloss.py。8・10・12・13・4枚目は間隔を詰めて収めた。
