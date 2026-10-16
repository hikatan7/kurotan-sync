---
name: project-mba-accounting1-textbook
description: MBAアカウンティングⅠ（中級）は2026-10-15に2版できた。22頁・9章・引用12件版と33頁・12章・引用27件版。どちらを残すか未決
metadata:
  node_type: memory
  type: project
  originSessionId: 1c030d10-a51a-4ed9-91bf-3937c795aa8f
  modified: 2026-10-15T10:21:47.184Z
---

2026-10-15、経営学\経営学テキスト とデスクトップ直下に、アカウンティングⅠが2版ある。

- 『…_MBAアカウンティングⅠ_財務諸表分析と管理会計』22頁・全9章・引用12件。財務諸表分析＋管理会計。架空A病院は calc.py で貸借一致を検算（起動元セッション作）
- 『…_MBAアカウンティングⅠ_財務分析・キャッシュフロー・管理会計』33頁・全12章・図9・引用27件。第Ⅰ部 財務分析（デュポン分解まで）、第Ⅱ部 CF計算書（病院会計準則の「業務活動」区分、ディキンソンの符号分類）、第Ⅲ部 管理会計（CVP・配賦・TDABC・関連原価・予算差異）。生成は _生成スクリプト_アカウンティングⅠ（`python engine.py acc1` → readable_docx.reprocess）（サイドセッション作）

経営学ポータルの acc テーマに2冊並んでいる。

**Why:** 起動元セッションとサイドセッションが同じ課題を並行で仕上げ、重複した。
**How to apply:** アカウンティングⅠに触れる前に、Junko にどちらを正本にするか確認する。残さない方は _旧版 へ退避してから build_portal.py で再生成する。関連：[[project-mba-finance1-textbook]]、[[feedback-globis-materials-no-ai-input]]、[[feedback-vancouver-citation-style]]
