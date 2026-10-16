---
name: project-servier-material-library
description: 教育ファイル集\_制作用（素材・プロンプト・調査メモ）\素材 にServier医学イラスト515点＋台帳。麻酔器具だけは無料素材に存在しない
metadata: 
  node_type: memory
  type: project
  originSessionId: a14ce877-77ee-49ce-a9c4-9354101f0a80
  modified: 2026-09-21T12:54:57.347Z
---

`デスクトップ\教育ファイル集\_制作用（素材・プロンプト・調査メモ）\素材\` に医学イラストの素材ライブラリ（2026-09-21構築）。**ポータルには登録していない**——ユーザーの意向で「くろたんが把握しているから、必要時に頼むだけでよい」。図が要る依頼が来たら、まずここを見る。

- `Servier\` … 公式配布の元pptx 49本（181MB）。`ServierMedicalArt-all-kits.zip`（165MB）も同梱
- `Servier_抽出\` … **抽出済み透過PNG 515点**、麻酔関連25カテゴリ別フォルダ
- `Servier素材台帳.xlsx` … 515点の一覧。ファイル名がハイパーリンク、オートフィルタ付き、「使えそうな巻」の列でミニ教科書の巻番号と対応づけ済み

**ライセンス**：CC BY 4.0。資料に1行入れれば足りる（画像ごとの表記は不要）。
`Servier Medical Art by Servier, licensed under CC BY 4.0 (https://smart.servier.com)`

**Why:** 元pptxは「完成したスライド」で、背景の装飾・Servierロゴ・ライセンス表記・英語ラベルが乗っており、そのままでは素材にならない。PowerPoint COMでテキストと引き出し線を除いた図形だけを透過PNGで書き出す方式で515点を抽出した。抽出スクリプトの要点は `06_AI別のクセと注意.md` に記載。

**How to apply:** 解剖・臓器・病態の図が要るときは台帳を引く。**ただし麻酔科の器具（喉頭鏡・気管チューブ・声門上器具・ビデオ喉頭鏡）は、Servier・NIH BioArt・Bioiconsのいずれにも存在しない**（3サイトを実査して確認済み。探し直さないこと）。器具の図が要るときは ①実物を撮ってもらう（形が100%正確、著作権は撮影者、後処理はClaudeが担当）②figlibで模式図を作る ③Geminiに描かせて位置関係を検証する、の順で検討する。Gensparkには描かせない（→[[project-genspark-capability-ledger]]）。関連: [[project-education-file-collection]] [[project-anesthesia-minitextbook-series]] [[workflow-figure-text-fit]]

**2026-10-12 移動**：素材はポータルから外し、`教育ファイル集\_制作用（素材・プロンプト・調査メモ）\素材\` に移した（Servier・Servier_抽出・台帳・zip）。
