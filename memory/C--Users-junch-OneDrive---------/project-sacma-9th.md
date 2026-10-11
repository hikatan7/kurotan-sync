---
name: project-sacma-9th
description: 第9回SACMA研究会(2026-08-08)の会場・座席・グループ資料一式の構成と再生成手順
metadata: 
  node_type: memory
  type: project
  originSessionId: 76fcb6e9-0735-4911-be19-89ceab3724bf
  modified: 2026-07-31T08:22:42.966Z
---

第9回 静岡心臓血管周術期管理研究会（SACMA）／開催日 2026-08-08。デスクトップ「第9回SACMA研究会」に成果物、直下に入力Excel。

**成果物**
- `第9回SACMA研究会\研究会 座席配置表_改訂版.pptx`（15枚・7.5×10in縦）
- `第9回SACMA研究会\名札_有料受講生.pptx`（39枚／2列×4段・5ページ）
- `ハンズオングループ名簿_チェック済.xlsx`（グループ表＋チェック結果）
- `参加者別スケジュール.xlsx`

**入力**：`グループ分け作成.xlsx`（受講者リスト・希望順1〜4）／`講義椅子配置.xlsx`（No.33〜39が見学者、41以降はインストラクター陣）／`座席表作成リスト.xlsx`

**午後ハンズオンの構成**：全6ブース各定員6名 — ①-A/①-B フィリップスTEE（C会議室・藤田 信子／永井 美玲）、②日本ライトTEEシム（B会議室・川本 英智）、③人工心肺CPB（多目的室・土井 健司）、④-A ECMO（講師なし）、④-B IABP（小嶋）。15時の④は整備で休止。**④-B IABPの14:00-14:45だけは確定枠12名**（心臓血管外科4名・見学2名・循環器内科6名）で、この枠は変更しないこと。定員6名にした結果12コマ分不足し、12名に1コマずつ自由時間がある。

**再生成スクリプト**（セッションscratchpadに `build_seating.py` `build_layouts.py` `build_howto.py` `build_exhibit.py` `merge_grouptable.py` `build_itinerary.py` `build_badges.py` `restore_iabp.py`）。11〜13枚目の会議室レイアウトはユーザーが手で配置するので**丸ごと再生成しない**。

**必ず守る**：スライド特定は本文の部分一致ではなく**タイトル文字列の完全一致**で行う（部分一致で別スライドを破壊した事故あり）。編集前に必ずpptxをバックアップ。関連 [[env-word-com-doc-generation]] [[env-onedrive-desktop-file-ops]]
