---
name: workflow-notebooklm-grounded-check
description: NotebookLM（画面名 Gemini Notebook、PRO契約）は検索でなく手元資料の照合係として使う。質問テンプレはデスクトップ直下のHTML
metadata:
  node_type: memory
  type: reference
  originSessionId: bac7f009-ad46-4a5e-848d-937156d85919
  modified: 2026-10-12T14:03:17.923Z
---

Junko は NotebookLM を PRO で契約しており、画面上の名前は「Gemini Notebook」（2026-10-12確認）。1ノートブックのソース上限は300件。
Gemini の検索は話を作るので使わず、NotebookLM は「入れた資料の中だけで答える照合係」として使う方針。

- 質問テンプレ：デスクトップ直下 `NotebookLM_質問テンプレ.html`（コピーボタン付き）。中身は共通ルール、ガイドライン照合、参考文献チェック、巻をまたいだ矛盾探し、周術期アナフィラキシーの例A〜D
- 共通ルールはチャット欄右上のスライダー形アイコン →「会話のスタイル：カスタム」に貼る。右上の歯車はアカウント全体の設定で、別物
- 自分の文書を一次資料と照合するときは、自分の文書のチェックを外す（外さないと自分の文章を根拠として引く）
- 「全部挙げて」は見落とすので、①話題を洗い出す → ②話題ごとに資料を並べる、の2段で聞く
- グロービス配布資料と患者情報は入れない（[[feedback-globis-materials-no-ai-input]]）

関連：[[reference-gemini-search-limits]] [[feedback-verify-ai-supplied-urls]] [[project-periop-anaphylaxis-guide]]
