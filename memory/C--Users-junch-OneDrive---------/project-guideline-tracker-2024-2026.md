---
name: project-guideline-tracker-2024-2026
description: ガイドライン改訂トラッカー2024-2026のxlsx（98件・既刊点検18点）。2026 ACC/AHA周術期GLの出現、JRC公式はjrc-cpr.org
metadata:
  node_type: memory
  type: project
  originSessionId: 346c851d-a03c-49ad-9f1c-71b361fdf16d
  modified: 2026-10-15T15:20:00.048Z
---

2026-10-15作成。Genspark横断検索キット39番（A国内・B海外麻酔・C蘇生と周術期循環）の回答をPubMed・学会原本で照合。`教育ファイル集\_制作用（素材・プロンプト・調査メモ）\調査メモ\ガイドライン改訂トラッカー_2024-2026_文献点検表.xlsx`（デスクトップにも写し）。シートは①改訂一覧、②2024年より前が現行、③既刊の点検、④Genspark回答の誤り、⑤作成中・予定。

**要点：**
- 2026 AHA/ACC 周術期GL（Circulation 2026;154:e413、PMID 42804570、2026-09-28公開）は**2024年版と同一内容の再確認版**（本文冒頭に「推奨・本文・図表・文献は2024年版と同一」と明記）。2024年版を引く既刊5点は内容上そのままで可、引用の差し替えは任意
- 2026-10-16に5点を修正済み：周術期のはじめかた（文献23→DAS 2025、build2.pyで再ビルド）、SGA研修医版スライド13枚目、周術期VPCテキスト（文献2→AHA 2025 Part 9。不安定WCTの同期CVはPart 9でCOR1/B-NR）、BIS 2本（モニター指針第5回2025.8）。旧版は各フォルダの `_…差替前_20261016`
- BIS の現行docxは `教育ファイル集\…\12_BISモニター`（`_編集用原本` 側は古い控え）。VPC「4頁テキスト」は旧版で、現行は「テキスト」版
- Word COM の PDF 書き出しがこのツールの前景で固まるときは `Start-Job` で別プロセスにすると通る
- 内蔵ブラウザのPerplexityはサインインなしで使える（Chrome拡張が未接続でも他AIに投げられる）。Gensparkは内蔵ブラウザでは未サインイン
- JRC公式は **jrc-cpr.org**（japanresuscitationcouncil.org は売りに出ている別ドメイン）。JRC2025の書籍版は2026-07-13発刊
- JSAの声明ページ・GL一覧は curl で取れる（一覧の一部はJS描画→ブラウザで取得）。CVC PG2026は「早期掲載版」
- Genspark の誤り：AHA Ethics を Part 13 と誤記（正しくは Part 3）、プロポフォール声明の日付、JSA声明4件とJCS2026（感染性心内膜炎・大型血管炎）の抜け

関連 [[reference-source-audit-2026-09]] [[feedback-verify-ai-supplied-urls]] [[workflow-textbook-master-prompt]]
