---
name: project-jats79-perioperative-ici
description: 第79回日本胸部外科学会(2026-10-21)の玉里茂之先生発表「周術期ICI」。文献台帳68本を作成、発表と論文化を予定
metadata:
  type: project
---

スライド `OneDrive\_旧デスクトップ\JATS79_Tamari.pdf`（12枚・英語）。演者は Shigeyuki Tamari・Toshiya Toyazaki（静岡病院 呼吸器外科）。発表日 2026-10-21。
内容：cN0肺葉切除のアップステージ RATS 98例 vs VATS 45例（pN+ 18.4% vs 6.7%、差はpN1のみ、cStage I→pII–IIIA 14.3% vs 2.2% p=0.037）＋術後アテゾリズマブ35例（RFS 12か月74.5%/24か月55.2%、irAE 25.7%・Grade4–5なし）＋術前ペムブロリズマブ7例。
文献台帳：`呼外プレゼン資料作成\4_論文と総説\JATS79_周術期ICI_文献台帳_20261012.xlsx`（68本、全PMIDをPubMed esummaryで照合済み、区分A〜K＋スライド対応表）。デスクトップ直下にもコピー。
最も直接の比較相手は Nakamura 2026 J Thorac Dis（本邦実臨床の術後アテゾ、PMID 41988310）と IMpower010 日本人5年（Okada 2026 Cancer Sci、PMID 41416818）。

関連: [[project-rats-research-plan]] [[project-elderly-rats-lobectomy-paper]]

**PDF収集（2026-10-12）**: `4_論文と総説\JATS79_文献PDF` に20本（出版社PDF 9＋著者原稿の本文から組んだPDF 11、図なし）。台帳M列から開ける。残り5本（Lu 2024 JAMA、Hennon 2020、Wang 2018、Barroso-Sousa 2018、Haratani 2018）はPMCで閲覧のみ。
**PMCのPDF一括取得の教訓**: pmc.ncbi.nlm.nih.gov/…/pdf/ は reCAPTCHA、Europe PMC の ?pdf=render は Cloudflare で弾かれる（突破しない）。使えるのは AWS の公開バケット `pmc-oa-opendata.s3.amazonaws.com/?list-type=2&prefix=PMCxxxx.` で、OA論文はPDFがあり、NIH著者原稿はxml/txtだけなので、xml→HTML→Chrome headless で PDF にする。

**論文骨子（2026-10-12）**: `4_論文と総説\論文骨子_JATS79_周術期ICI_20261012.docx/.pdf`（9頁・引用51本）。推奨は1本化（主要評価項目＝cStage I→pStage II–IIIAの病期移動と補助療法の実施、RATS/VATSは非同時期の記述比較にとどめる）。
**投稿前の最大の穴**: 「14/98」の分母98にcStage II（cT3 6例ほか）が含まれる→cStage Iだけを分母にし直す必要。ほかに第7版/第8版の対応、2コホートの重複、41→35の6例、RFSの起点（手術日 vs 無作為化）。スライドのp値6つは再計算で一致（感度分析pN1はp=0.027）。
