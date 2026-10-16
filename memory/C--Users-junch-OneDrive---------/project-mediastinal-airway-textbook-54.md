---
name: project-mediastinal-airway-textbook-54
description: 〔54〕『縦隔腫瘍と中枢気道の麻酔・集中治療』本編48頁＋専攻医版16頁。写真14点はCC BY／BY-SA（Commons・PMC）、自作図12点、引用62件
metadata:
  node_type: memory
  type: project
  originSessionId: 99a0cc2d-bf8f-48aa-b742-74a1b8cf0599
  modified: 2026-10-13T01:22:30.317Z
---

2026-10-13 作成。`教育ファイル集\麻酔科ミニ教科書シリーズ\54_縦隔腫瘍と中枢気道の麻酔・集中治療`（デスクトップにも docx/PDF をコピー）。
Junko が Gemini＋ChatGPT（画像入り）の回答と、検索による補足を貼って「画像入りで詳細版と専攻医用簡易版を」と依頼。
全5部13章：区画と画像／縦隔腫瘍症候群と術前評価／生検・導入・危機と ECMO・摘出術／硬性鏡・ステント・熱焼灼／ICU・重症筋無力症。

- **ChatGPT の画像は UWorld・Radiology Assistant・CTisus など転載不可のものだった** → 同じ内容の写真を Wikimedia Commons（API で作者・ライセンスを取得）と PMC の CC BY 症例報告から集めた。図の説明文に出典とライセンスを明記。
- PMC の図は Europe PMC の bin/ は 403、PMC の OA サービス oa.fcgi は 404。**pmc-oa-opendata の S3（https://pmc-oa-opendata.s3.amazonaws.com/?list-type=2&prefix=PMCxxxx.）で画像が取れる**。
- 原典で確認できた主な数値：Béchard 2004（心嚢液 OR19.8、気管圧迫>50% OR7.4）、Hartigan 2022（17例、陽圧換気・筋弛緩で気道は広がる）、APSF 2025（ICU 基準）、Choudhury 2026 J Card Crit Care TSS（ドレーン200mL/h×4h・1000mL/1h、正のバランス1.5L、乳び胸2〜4週）、AABIP 2023（FiO2/FeO2≦0.40）、Akan 2026（ステント移動中央値 良性17日・悪性25.5日）、SALTY STENT。
- 原案の「片側横隔神経麻痺で肺活量20〜30%低下」「スガマデクス後の再クラーレ化」は根拠が見つからず不採用。
- 生成：`_生成スクリプト\build54.py`／`build_short54.py`（`SHORT=1 python qa54.py` で図番号なしの専攻医版図を `図版\_専攻医版` に出す）。写真は高さ11cm上限で幅を自動決定。最後に readable_docx の reprocess を通した。
- ポータル：「縦隔腫瘍」が「気道」の規則に取られたので book_toc.py に P[9] の規則を追加し、Junko の指示で呼吸器外科の麻酔に**小項目「縦隔腫瘍・中枢気道」（旧章番号40）**を新設（PARTS と NEW_PARTS の両方に登録、キーワード 縦隔／中枢気道／気道ステント／硬性気管支鏡）。フォルダはシリーズ内のまま。158資料・54巻。控えは `_ポータル生成\_更新前_20261013_縦隔`。

関連: [[project-thoracic-anesthesia-textbook-52]] [[feedback-verify-ai-supplied-urls]] [[project-anesthesia-material-portal]] [[feedback-vancouver-citation-style]]
