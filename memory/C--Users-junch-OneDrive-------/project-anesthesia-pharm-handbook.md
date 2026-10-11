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
