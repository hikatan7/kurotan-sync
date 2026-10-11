---
name: project-anesthesia-pharm-handbook
description: 専攻医・研修医向け「麻酔薬理ハンドブック」全15章100頁のdocx+PDF+図版26点の所在と再ビルド手順
metadata: 
  node_type: memory
  type: project
  originSessionId: ad9b6eb5-a15f-449d-978b-430112ff2a8e
  modified: 2026-08-04T10:27:50.904Z
---

デスクトップ「学習ファイル\医学\08_麻酔・気道管理\麻酔薬理ハンドブック」に、
麻酔薬理ハンドブック.docx / .pdf（A4・100頁・全15章＋付録A〜D）と「図版」フォルダ（PNG 26点）を作成（2026-08-04）。

構成：1 麻酔とは／2 4本柱／3 吸入麻酔薬／4 静脈麻酔薬の薬物動態／5 プロポフォール／6 レミマゾラム／
7 ケタミン他／8 デクスメデトミジン／9 オピオイド／10 筋弛緩薬・拮抗薬／11 モニタリング／
12 症例20例／13 ICU鎮静／14 医療経済と環境負荷／15 まとめ。
コラム枠は Clinical Pearl / Pitfall / Mechanism / Column / History / Evidence Update / Q&A / Case / Take Home Message の9種。

第14章の薬価は「相対比＋計算式」で書いてあり金額は入れていない（改定で変わるため）。自施設の薬価で再計算する前提。
第14章末に令和8年度改定の3軸再編とプレセデックス適応の注意を参考として収載 → [[reference-r8-anesthesia-sedation-rules]]

再ビルド：ビルドスクリプト一式はセッション用スクラッチにのみ存在（figs_a/b/c.py で図生成 → main.py で docx →
export.ps1 で Word COM が目次更新＋PDF書き出し）。作り直す場合は matplotlib/scipy/python-docx/pymupdf が必要。
関連 [[env-word-com-doc-generation]] [[project-teaching-file-folder]]

**2026-09-17 に番号引用へ改訂。** PDF 96頁。`麻酔薬理ハンドブック_SourceLedger.xlsx`（44件）を新規作成。Eleveld モデル・Doi のレミマゾラム第III相・SEDCOM・SPICE III・MENDS2・ASA 2023 筋弛緩モニタリング・JSA 悪性高熱症2025 などを原典で確認。

**2026-09-24 専攻医版30頁（コラム入り）を作成。** 同フォルダに `麻酔薬理ハンドブック_専攻医版30頁.docx/.pdf` と台帳xlsx（引用50件）。
全14節・コラム8本・症例8例・図5点（本編の図版を流用）。生成物は `_生成スクリプト\専攻医版30頁\build7s.py`（c7s_p1/p2 が本文）。
本編の記述から直した点：ダントロレンは JSA2025 の「上限を設けない」に合わせた（本編の症例1は旧記載）／
スガマデクス承認は欧州2008・日本2010・米国2015／真珠湾のチオペンタール死亡は Bennetts 1995 で誇張と判明、と書いた。
30頁に収めるには図を26→5点に絞る必要があった（本文約2.6万字＋文献3頁で30頁ちょうど）。
