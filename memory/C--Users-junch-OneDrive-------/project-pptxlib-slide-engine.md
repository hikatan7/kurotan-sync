---
name: project-pptxlib-slide-engine
description: 高密度スライドを組むための自作ビルダー pptxlib の設計と、レイアウト崩れを起こした3つの落とし穴
metadata: 
  node_type: memory
  type: project
  originSessionId: dfa56fed-97fb-49e2-913d-191807cdb3d5
  modified: 2026-08-14T02:57:19.386Z
---

教科書シリーズと同じ配色・枠でスライドを組む自作ビルダー `pptxlib.py`(16:9・Meiryo)。
python-pptx にはテキストの実測手段が無いため、**推定モデルで自動フィット**する設計になっている。

構成：`Deck.title_slide / slide(part,title,lead)` ＋ 積み上げ部品
`strip`(最下部の帯・固定) `cards` `kpis` `steps` `table` `two_col`、最後に `audit(path)`。

**踏んだ落とし穴（同じ設計をするなら必ず入れる）**
1. **積み上げカーソル**。`body_rect()` が毎回「本文領域の先頭」を返す実装だと、
   2つ目のブロックが1つ目を**塗りつぶして隠す**。スライドに `_cur_top` を持たせ、
   ブロックを切り出すたびに下へ進める。`reserved=` は「下に空けておく高さ」の意味で使う。
2. **行高の見積り**。PowerPoint の％行間は**フォント固有の行高**に掛かる。Meiryo は約1.30em なので
   `line_spacing 1.22` の実効は約1.59em。この係数を入れないと高さを過小評価して溢れる。
   太字は字幅が約1.06倍になるので幅計算にも係数が要る。
3. **枠が中身より大きいとき**。カードや2カラムは中身の必要高を計算して枠を詰める
   （下限は領域の0.80倍）。詰めた分はカーソルを前倒しし、余白は最下部に一箇所へ集める。

**検証は必ず目視で。** `audit()` は推定なので、他のツールで作った pptx には偽陽性を大量に出す
（本文と小見出しが同じテキストボックスにあると最大サイズで判定してしまう）。
PowerPoint COM で PDF 化 → PyMuPDF で画像化 → 実際に見る、が唯一確実
（手順は [[env-word-com-doc-generation]]）。

用途は [[workflow-textbook-four-deliverables]] の④スライド。
