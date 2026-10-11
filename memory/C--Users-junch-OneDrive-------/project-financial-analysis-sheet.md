---
name: project-financial-analysis-sheet
description: デスクトップ「財務分析シート.xlsx」— PL/BS/CFを入力すると財務指標を自動計算する2シート構成のExcel
metadata: 
  node_type: memory
  type: project
  originSessionId: 472d0651-052a-4194-b29c-d7e332b44cde
---

2026-07-10、デスクトップに「財務分析シート.xlsx」を作成(Excel COMで生成、[[env-word-com-doc-generation]]と同じ方式でps1はUTF-8 BOM必須)。

- 「入力」シート: PL・BS・CFを3期分(前々期/前期/当期)入力。青字=入力セル、黒字=自動計算。B42:D42にバランスチェック式あり。
- 「分析」シート: 成長性・収益性・効率性・安全性・CFの約25指標を自動計算(行番号固定で入力シートを参照)。E列=目安、F列=当期の判定(◎○△)。
- 拡張時の注意: 入力シートの行を挿入/削除すると分析シートの参照がずれるため、行構成は変えず末尾に追加するのが安全。
