---
name: project-advanced-cv-anesthesia-ledger
description: 高度心臓血管麻酔（CIED／大動脈脳・脊髄保護／Structural Heart／透析）教科書のSource Ledger 210本
metadata: 
  node_type: memory
  type: project
  originSessionId: 585edbaa-4ad2-4d47-b0c9-dc8724e340b8
  modified: 2026-09-17T07:24:39.666Z
---

デスクトップ「教育ファイル集\高度心臓血管麻酔\高度心臓血管麻酔_SourceLedger_v1.xlsx」（2026-09-17作成）。7領域210本（目標150本）、Tier1が119本。全PMID/DOIをPubMed E-utilitiesで著者・年・タイトル照合済み。シート構成は00使い方／Ⅰ〜Ⅶ領域／99検証結果／図表・アルゴリズム設計（130件、うち新規48）／不足領域と補完。

他AIが挙げた資料のうち**実在しなかったもの**: 2024 ASA practice advisory for CIED（正しくは2005 ASA advisory＋2011 HRS/ASA consensus）、2026 ACC/AHA/ASE/HRS/STS tricuspid consensus（代替は2024 AHA tricuspid statement）、2025 STS Aortic Surgery Update（代替は2024 EACTS/STS大動脈オルガンGL）。**誤帰属**: 2026 PLoS MedのSCPP標的RCTは外傷性脊髄損傷が対象で大動脈手術ではない。日本の学会GL（JCS/JHRS不整脈、JSCVA NIRS増補版、JSDT周術期）はPubMed未収載のため学会サイトで要確認のまま。

第Ⅰ章「ペースメーカー・ICDと周術期麻酔」34頁（図版14・表8）、第Ⅱ章「大血管手術の脳保護」30頁（図版13・表4）、第Ⅲ章「脊髄保護と髄液ドレナージ」32頁（図版15・表4）、第Ⅳ章「M-TEERと僧帽弁インターベンション」29頁（図版14・表4）、第Ⅴ章「TAVIと三尖弁インターベンション」28頁（図版15）、第Ⅵ章「透析患者の心大血管手術」28頁（図版14）、第Ⅶ章「人工心肺・出血と輸血・循環の目標」28頁（図版14）を2026-09-17に執筆。さらに同日、第Ⅷ章「心臓麻酔と神経モニタリング」40頁（図版16）を追加し、**全8章263頁・図版115点**。2026-09-17 に全8章を番号引用（バンクーバー方式）へ改訂した。本文に肩付き番号、章末に参考文献一覧（PMID・DOI つき）。台帳284件すべてを本文から引用している。さらに『高度心臓血管麻酔_総目次と図版一覧』21頁（図版3点・全115図の一覧表つき）を作り、各章PDFから見出しと図の実ページを拾う `toc_index.json`／`build_toc.py` で自動生成している。台帳も「Ⅷ_神経モニタリング」74件を追加して**全8シート284件**。第Ⅷ章は「麻酔は足りているか／脳に届いているか／脳は傷んでいないか」の三つの問いを分けるのが軸で、せん妄を減らせたのは自動調節能に基づく血圧の個別化と鎮痛の追加だけ、「モニタを足して外れたら戻す」型（Bottomline-CS・ENGAGES-Canada）は転帰を動かさなかった、が結論。第Ⅶ章は全章を横断し、「測れること/できること≠転帰が変わること」を一覧化（NIRS・塞栓防止デバイス・髄液ドレナージ・AKIバンドル等）。生成スクリプトは同フォルダ_生成スクリプト（bookkit.py/figlib.py＋figcrop.py）。**縦長のアルゴリズム図はCanvas高さを決め打ちすると下端が切れる** → 高さ1900-2000で描いてfigcrop.crop_bottomで余白を実測トリミングする（PNGの高さ＝宣言したCanvas高さなら切れている、が検出法）。

**レイアウト見直しの自動化（2026-09-17）**: `_生成スクリプト` に4つの道具を追加した。`figwidths.py`（図ごとの版面幅）＋`figmove.py`（図を後ろの段落ぶん下げる）を buildN.py が読み、`autofit.py`／`autofit2.py` が PDF を実測して両者を書き戻す。これでページ末の大きな空白が 16箇所4190pt → 6箇所1367pt に減った。`figqa.py` は Canvas.save 直前に matplotlib の get_window_extent で全文字の外接矩形を取り、食い込んでいる組を報告する（目視では見落とす重なりを拾う。比率0.30以上が本物、0.12〜0.24は行間の偽陽性）。`figlib.duo()` は「A 対 B」の二数字を実測幅で並べるヘルパ（決め打ちオフセットは桁数が増えると必ず重なる）。**注意: figNx.py は `OUT = sys.argv[1]` なので、引数なしで import して呼ぶと `fig/` に書き出され本番の図版が更新されない。**

**OneDrive 配下の docx は Word COM が開けずに固まることがある**（Documents.Open が無応答のまま数十分）。`to_pdf_local.ps1 -Name <章名>` がローカル作業フォルダへ写してから Word にかけ、PDF と docx を書き戻す。強制終了のあとは Word の Resiliency キー（HKCU:\Software\Microsoft\Office.0\Word\Resiliency）を消さないと「ドキュメントの回復」で再び止まる。

**Why:** 教科書執筆のPhase 1資料。数値は抄録から採ったため本文で引用してよい。
**How to apply:** 追記時はS-ID連番＋Tier＋図表番号を同時に決める。[[feedback-verify-ai-supplied-urls]] [[feedback-links-must-be-excel]] [[project-education-file-collection]]
