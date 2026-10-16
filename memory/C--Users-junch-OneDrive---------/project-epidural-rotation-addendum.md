---
name: project-epidural-rotation-addendum
description: 硬膜外穿刺テキストに第9章（回旋・側弯・圧迫骨折）と第10章（異所留置）を追記、CC BY画像6点、文献18–50（2026-10-16）
metadata:
  node_type: memory
  type: project
  originSessionId: f257e9dc-2e8e-44d0-b211-3b2cb56757a6
  modified: 2026-10-16T04:29:33.390Z
---

2026-10-16、教育ファイル集\1_総論\05_区域麻酔・鎮痛\脊髄幹麻酔と硬膜外穿刺\硬膜外穿刺とカテーテル挿入のためのテキスト.html／.pdf（30→46頁）に追記。
控えは同フォルダ `_旧版\…_回旋追記前`。HTML は自己完結（画像は base64 埋込）、PDF は headless Chrome の --print-to-pdf で作る。

- 第9章：腰椎回旋 46.7%（側弯除外・平均52歳、Zhao 2024）、L3–5 は回旋が少ない。変性側弯 60歳超 36%（メタ解析）、椎体骨折 女性80歳以上 53%（ROAD）。凸側へ向ける/凸側から傍正中。年齢と胸部硬膜外不成功 aOR 4.16（75歳以上）
- 第10章：術後CTで12.7%が黄色靱帯手前（Matsuo 2025）、硬膜下 5.3/1000（Sidash 2021）、血管内迷入の予防OR（Mhyre 2009）
- 図17–22 は CC BY 4.0 の原著図（Crowe 2024 BJA Educ Fig3/4、Huang 2023、Diwan 2023、Matsuo 2025、Khan 2023）。PMC の画像は `pmc.ncbi.nlm.nih.gov/articles/instance/<数字>/bin/<file>` なら取れる（europepmc は403）
- 4AI 横断検索の照合表は `_制作用（素材・プロンプト・調査メモ）\硬膜外_椎体回旋_横断検索と照合_20261016.xlsx`。Gemini は PMC 番号を捏造、Perplexity・ChatGPT は Ko & Leffert の誌名を誤った（正：Anesth Analg）

**同日午後：第1〜8章にも「数字（と画像）で見る」小節を追加**（64頁・文献85件・図33）。build18.py で図番号・文献番号を出現順に振り直した（参考文献欄の「原著の図番号」は振り直し対象から外すこと）。控え `_旧版\…_第1-8章追記前`。Copilot は3回とも無回答、Gemini は PMID 34521453（犬の寄生虫）を捏造。素材は `_制作用…\硬膜外_第1-8章追記素材_20261016`。

**研修医版『硬膜外麻酔の基本』**：1_総論\05_区域麻酔・鎮痛\硬膜外麻酔の基本\ に HTML/PDF（本文10頁＋文献2頁、引用42、図7、表2）。脊麻の基本の CSS を流用、略語は章ごと初出で自動展開、ノンブルは PyMuPDF。ポータル登録済（区域麻酔・鎮痛、170資料）、控え `_ポータル生成\_更新前_20261016_硬膜外`。

関連 [[feedback-verify-ai-supplied-urls]] [[workflow-chrome-search-two-modes]]
