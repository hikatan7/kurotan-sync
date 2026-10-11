---
name: project-intraop-vpc-lidocaine-atropine
description: 術中に散発するVPC 詳細版9頁・文献29件＋専攻医版5頁・文献25件（2026-10-09）。他AI原案の誤りと一次資料で確かめた数値
metadata:
  node_type: memory
  type: project
  originSessionId: 21f7376f-261b-49c3-b2f8-403e0580fa2d
  modified: 2026-10-09T04:12:52.122Z
---

教育ファイル集\総論・基礎\麻酔管理の基礎\周術期の心室性不整脈\ に
`術中に散発するVPC_詳細版.html/.pdf`（9頁・29件）と `…_専攻医のためのテキスト.html/.pdf`（5頁・25件）。
HTML→Chrome headless印刷＋PyMuPDFでノンブル。ソースは scratchpad の vpc\（refs.py 台帳・figs.py 心電図SVG・build.py）。改訂は HTML を直接直す。
ポータル登録済：Ⅰ-5 循環管理、詳細版／研修医テキストのボタン（控え `_ポータル生成\_更新前_20261009_VPC`）。

確かめた要点：
- キシロカイン静注用2%：50〜100mg（1〜2mg/kg）を1〜2分、5分後同量、1時間300mgまで。効能に「手術に伴う心室性不整脈の予防」あり／完全房室ブロックは禁忌（2023-09改訂）
- Cochrane予防的リドカイン（MI）：死亡・VF減らず、心静止1.03% vs 0.41%（RR 2.32）。ALPS：退院生存 アミオ24.4／リド23.7／プラセボ21.0
- AHA 2025徐脈：アトロピン1mg q3–5分、総量3mg。国内添付文書は0.5mg皮下・筋注（場合により静注）
- ガイドワイヤー15/17.5/20cmで不整脈26/35/65%（Lee 2017）。PAC挿入で進行性心室性不整脈63%、予防リドカインで有意減少せず（Sprung 1983）
- 慢性低K（2.6–3.4）は術中不整脈を増やさない（Vitez 1985）／CABGでK<3.5は術中不整脈OR2.0（Wahr 1999）

他AI原案の誤り：「JCS/JCC/JACR/JATS 2024 周術期GL」は存在しない（国内は2022年改訂版）。そこに付けた「無症候性VPCは治療不要＝クラスI」も根拠なし。アトロピン「0.5mgから開始」はAHA旧版。ACLSでの「アミオダロン第一選択」は誤り（2025もアミオダロンかリドカイン）。PMC3167157はBecker & Haas 2011（歯科の鎮静）で、リドカイン0.5〜1mg/kg。
関連 [[project-perioperative-va-text]] [[feedback-verify-ai-supplied-urls]]

2026-10-09追記：段階Bの解説（第5節）と薬剤17種＋ジゴキシンの適否表（第6節）を追加 → 詳細版11頁・31件／専攻医版6頁・27件。ジゴキシンはAndrews 2023コンセンサス（PMC全文）とLevine 2011（中毒時のCa静注で致死的不整脈・死亡増なし）で確認した範囲だけ載せた。
ジゴキシンのPerplexity回答（プロンプト集33）の書誌誤り：ESC AF 2024の筆頭はVan Gelder（Hindricksではない, PMID 39210723）／RATE-AFはJAMA 2020;324:2497（PMID 33351042）／DECISION本論文はNat Med 2026（ehag385は中止後の副研究）／SPAQIの筆頭はSahai SK（PMID 36058586、Wiermanではない。ジゴキシン継続の文言は全文未確認）／Andrews 2023は30:395-401、DOI …1065／ACC/AHA AF 2023のCirculation版はPMID 38033089。DIGIT-HF（NEJM 2025;393:1155, PMID 40879434）の数値は正しかった。
