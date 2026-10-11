---
name: project-icls-post-cardiac-surgery-als
description: ICLSインストラクター向け「心臓手術後の心停止（CALS）」配布資料A4 4〜6頁の準備。文献検索キットと神尾2016総説
metadata:
  type: project
---

2026-09-27開始。置き場は `教育ファイル集\ICLS_開心術後ALS配布資料`。
- `開心術後ALS_文献検索プロンプト.html`：Genspark用①本番（ジョブA国際GL／B国内動向／C数字／D教え方／E神尾2016の更新確認）②続き③2巡目照合④Perplexity・Gemini用。
- `_参考資料と検証神尾2016_INTENSIVIST_胸骨正中切開術後の心肺蘇生.pdf`：神尾直・松永渉・大塚祐史. INTENSIVIST 2016;8(1):49-59。デスクトップ直下から移動。院内契約で閲覧したPDFなので、本文は他AIに貼らない（書誌と論点だけ渡す）。図表は許可転載なので再利用しない。
- 骨格は既刊㉖第IV部（EACTS2009→STS2017→AHA2025）。当院HCUのA4チャートは `_教材化待ち\…\01_蘇生・急変対応`。

**次にやること:** Gensparkの回答が来たら、PubMedで照合してから配布資料に組む（[[reference-source-audit-2026-09]]の3段手順）。
関連 [[project-resuscitation-textbook-26]] [[feedback-genspark-max-work-per-reply]]

## 2026-09-27 3つのAI回答を照合
`開心術後ALS_照合結果と検証プロンプト.html` に結果と検証プロンプト（Genspark 16項目／Perplexity 12項目）。
- **AHA 2025 Part 10 の Cardiac Surgery は cpr.heart.org で原文が読める**（WebFetchは403、ブラウザペインの textContent で取れる）。成人6勧告：1/B-NR 圧迫、1/C-EO 3連続・1分、1/C-EO ペーシング・1分、2a/B-NR 再開胸、2a/B-NR 内部マッサージ、2a/C-EO ECLS。**アドレナリンの勧告も「5分」もない。**
- **ERC 2025 は resuscitationjournal.com の PII S0300-9572(25)00265-5 で全文**。筆頭 Lott C。3連続<1分、DDD 80-100、再開胸<5分、少なくとも10日、アドレナリン1 mgは controversial・peri-arrestで50-100 μg「考慮」、MICS・10日超はECPR。
- AI回答の誤り：Whitlock 2023 の PMID 36477544 は無関係論文、Ley は 2026;38(2)、ERC著者 Deakin は誤り、Dunning 2006 は 451→228秒。

## 2026-09-27 3点セット完成
`心臓手術後の心停止_詳細版`（25頁・全10章＋付録A/B・引用28件）／`_専攻医用`（9頁・確認問題5問・引用13件）／`_要点10枚.pptx`（＋各PDF）。
生成は `_生成スクリプト`：`build.py [detail|resident]`（bookkit＋自前の refs.py、ID は PMID か 90000xx）→ `to_pdf.ps1 -name <名前>`、`build_slides.py`（pptxlib）、図は `figs.py`（3点）。
- 検証で確定：Whitlock 2023 は PMID **36413642**（AI が出した 36477544・36695879 はどちらも無関係）。高木のCALS解説は **LiSA 2025;32(6):631-639**（胸部外科ではない）。JSAプラクティカルガイドは2022-01-06「訂正」（改訂ではない）。
- **Gali 2021（SWJPCC 23(2):54-61）は本文でも分子分母が割合と合わない**（12/38≠29%、32/33≠84%）→ 割合とP値だけ引用。
- 未確認のまま：JRC 2025 本文の心臓手術後の記載、虎の門 2026-10-25 のコース。
- ポータル登録済み（2026-09-27）。検索・検証キットHTMLと神尾PDFは `_参考資料と検証` に移動。
- 2026-09-27 改訂：スライドは「枠に収まる最大サイズ」を自動探索（build_slides.py の fit_and_draw、本文14〜18pt・全文太字）。pptxlib のランに lang=ja-JP を付けたら行頭の「）」「。」が消えた。専攻医用は冒頭に略語一覧（ABBR_RES）＋本文の初出に日本語注釈（ユーザー指示「研修医版に略語だらけ」）。

- **2026-09-27 要点10枚に用語欄**：略語が多いとの指摘で、全10枚の下（出典行の上）に「用語」欄（10.5pt、ベージュ地）を追加。build_slides.py の `GLOSS` 辞書と `gloss()`。表紙は y=6.70 に固定配置。用語欄の分だけ本文は自動で縮む（最小は9枚目の対照表 11.5pt）。旧版の pptx/pdf と `_before_*.py` の控え4つはユーザー指示でごみ箱へ（控えを残さない）。
- **2026-09-28 Genspark 追加調査を照合して詳細版に追記**（28頁・文献31件）：STS 2017 本文（ahajournals でなく annalsthoracicsurgery.org を内蔵ブラウザで閲覧可）で AED・機械的胸骨圧迫装置 III harm・C、持続投与停止 IIA・C、圧迫保留1分 IIA・B、40万例/0.7–8%/半数生存/VF 25–50%、訓練で再開胸時間50%短縮を確認。Weber 2025 JTCVS（CSU-ALS 認定施設で救命失敗 OR 0.30）、CALS Japan 沿革・「二階部分」、ハンドブック序文、湊谷 書評（胸部外科79巻2号）を追加。CALS-ANZ（PMID 38046213）は本文が ScienceDirect の CAPTCHA 先で未確認→数字（0.7–5.2%、75% vs 39%、20 J、挿管は開胸後）は不採用。Genspark は作成者名を「淳子」と誤記。
- **2026-09-28 Genspark 査読（ジョブA/B/C/Z）を詳細版に反映**（29頁）：略語表に ACLS・CSU-ALS・DC・DDD/VVI・HCU・ICLS・LVAD、COR/LOE の読み方の囲み、胸骨ワイヤ・心外膜ペーシングワイヤの説明、「内胸心マッサージ」に統一（図1も）、1分は認識時から、3連続ショックの適用条件（術後ICU・モニタ下目撃）と合間の手順、ペーシング最長1分、PEAは圧迫を始めてからペーシングを数秒止める、持続投与停止の鎮静例外、IABP作動中の動脈圧の注意、72時間の理由（Mackay抄録で確認）、Peek 2023 の結論を原典どおりに修正（教室訓練43%・VR0%、誤りはVR11対15）、付録A「幅が広がった」誤り修正、付録BのCALS-ANZ数値を削除。build.py の DATE は「9月27日（9月28日改訂）」— 専攻医用を作り直すときは戻すこと。スライド・専攻医用はまだ「内胸マッサージ」表記。
- **2026-09-28 Perplexity 検証プロンプト**：`自作ファイル集\プロンプト集\27_CALS未解決点_Perplexity検証.html`。確認済み事実（AHA/ERC/STS/Richardson/Mackay/Weber ほか）を照合用に渡し、未解決の Q1〜Q12（CALS-ANZ 本文、体内パドル J、3連続ショックの直接比較、圧迫損傷の頻度、少量アドレナリン、ペーシング設定、PEA 停止時間、MICS/10日超の ECPR、挿管の時期、日本の報告と JRC 2025、訓練の転帰研究、反対意見）を調べさせる。結果が来たら原文照合して詳細版へ。
- **2026-09-28 Perplexity 検証を照合して反映**（詳細版32頁・文献32件）：CALS-ANZ は PMC10692601 で全文可（Europe PMC の inPMC=N は古い情報、PMC idconv で確認できる）。0.7–5.2%、最初の3時間に最大50%、75% vs 39%、圧迫保留60秒、DOO ペーシング、体内パドル20 J、消毒なし一体型ドレープ、挿管は再開胸後かROSC後、アドレナリン50–100 μg、役割（再開胸チーム・トロリーを含む6役）を 1-1・新2-5・3-3・3-5・5-3・7-1・第10章に反映。Brand 2018 BJA Educ（PMID 33456790, PMC7807979）を追加（20 J、DDD 80–100、緊急ボタンの非同期ペーシング）。付録C「まだ決着していない点」を新設。Perplexity の誤り：VR試験の筆頭を Bakhuis とした（正しくは Peek JJ）、AHA Part 10 の PMID を疑った。JRC 公式ドメイン japanresuscitationcouncil.org は無関係サイトへ転送→JRC 2025 の中身は未確認のまま。
