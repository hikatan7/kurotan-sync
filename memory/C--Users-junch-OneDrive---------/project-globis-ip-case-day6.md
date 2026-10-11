---
name: project-globis-ip-case-day6
description: GLOBISファイナンス基礎Day6「IP社の新市場参入」のDCF分析ブック。デスクトップ「IP社_新市場参入分析」に10シート
metadata: 
  node_type: memory
  type: project
  originSessionId: 137cd429-7693-409d-ac80-dd01e59ddeaa
  modified: 2026-09-16T17:59:39.720Z
---

デスクトップ「IP社_新市場参入分析\IP社_新市場参入_CF分析.xlsx」（2026-09-17作成）。
①結論サマリー ②用語解説 ③前提条件 ④P/L ⑤FCF計算 ⑥WACC ⑦NPV・IRR ⑧感度分析 ⑨よくある誤り ⑩提言 の10シート。
③の黄色セルを変えると⑤⑦⑧が連動する生きたモデル。

主要な数値：WACC 13.8%（rE15%×90% + rD5%×(1−40%)×10%、D/(D+E)は時価50,000/500,000）、
NPV +13,678百万円（継続価値込み）／+4,404（Yr8打切）、IRR 28.3%／23.1%、
損益分岐は3年後シェア12.8%・キャッシュコスト率65%。

この種の課題の作り方：計算は必ずopenpyxlで数式として埋め、Excel COMで再計算→PDF書き出し→
fitzでPNG化して目視QA（文字の切れは行高不足が原因なので、列幅から折返し行数を計算して行高を入れ直す）。
関連: [[project-globis-mba-folder]] [[project-financial-analysis-sheet]] [[env-desktop-localized]]
