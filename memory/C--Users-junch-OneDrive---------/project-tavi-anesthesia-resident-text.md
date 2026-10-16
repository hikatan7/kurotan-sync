---
name: project-tavi-anesthesia-resident-text
description: TAVIの麻酔 研修医向け14頁・番号引用24件（2026-10-15）。略語は章ごとの初出で英語正式名称＋日本語を自動展開
metadata:
  node_type: memory
  type: project
  originSessionId: 3dbde3bf-690b-4e6b-a349-80d0d0fb91b1
  modified: 2026-10-15T03:40:03.357Z
---

教育ファイル集\2_各論\01_循環器の麻酔\TAVIの麻酔\ に `TAVIの麻酔_研修医のためのテキスト.html/.pdf`（A4・14頁、図3・表7、引用24件）。デスクトップにもコピー済み。2026-10-15 ポータル登録（循環器の麻酔＞Structural Heart、既存の book_toc 規則「tavi」で自動判定。控え _ポータル生成\_更新前_20261015_TAVI）。

Junko の指示「略語は全て日本語英語の正式名称付き」「20枚以内」。作り方は NG チューブ版と同じ（HTML→Chrome headless→PyMuPDFでノンブル）。make.py は本文中の既知略語を**章（h2）ごとの初出で自動展開**し、見出し・図・表見出しは除外、巻頭に略語一覧を自動生成。スクリプトは scratchpad 限り。改訂は HTML を直接直す。

構成：TAVIの経緯 → AS病態生理（悪循環図・管理目標表）→ 術前評価 → 手技の流れと麻酔科の仕事 → 麻酔法選択 → 鎮静の実際 → モニタリング → 高頻度ペーシング → 弁展開後の変化（suicide LV）→ 合併症（血圧が戻らないときの図）→ 術後。

確かめた数値：SOLVE-TAVI 447例 30日複合 27.2% vs 26.4%、昇圧薬 62.8% vs 97.3%、5年全死亡 41.5% vs 54.3%（主要項目は有意差なし）／冠閉塞 0.66%・30日死亡40.9%（Ribeiro 2013）／VARC-3メタ PMI 13%（Giacobbe 2026 JAHA）／非麻酔科医鎮静2,000例 切替1.2%（Maznyczka 2026）／左室ワイヤーペーシング EASY TAVI 48.4 vs 55.6分。既刊第Ⅴ章の参考文献番号は本文と対応がずれている箇所がある（例：2番が中隔焼灼の論文）。

関連 [[project-intraop-ng-tube-bleeding-text]] [[feedback-vancouver-citation-style]] [[project-advanced-cv-anesthesia-ledger]]
