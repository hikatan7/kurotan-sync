---
name: feedback-links-must-be-excel
description: URLリンクを含む一覧・資料はMarkdownやテキストではなく必ずExcelで作る
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 154caa56-6f5d-4ed1-b4d2-6fbd3e3b2911
  modified: 2026-08-25T09:25:43.409Z
---

URL（ハイパーリンク）を含む一覧や資料は、**必ずExcel（.xlsx）で作成する**。Markdown（.md）やテキストで納品しない。

**Why:** ユーザーは .md をメモ帳で開くため、リンクがただの文字列になりクリックで飛べない。2026-08-25に「リンクがあるファイルはメモ帳だと飛べないので必ずエクセルで作って」と明示的な指示があった。

**How to apply:**
- openpyxl で `cell.hyperlink = url` を設定し、あわせて `Font(color='0563C1', underline='single')` を付けて見た目もリンクにする
- リンクが1つでも含まれるなら、資料全体をExcelブックとして構成する（シート分けで章立て）
- 既に .md で作ってしまった場合は .xlsx に作り直し、**古い .md は削除**して二重管理を避ける
- 参照している索引ファイル（例：[[workflow-textbook-master-prompt]] の 00_早見表）の拡張子表記も同時に更新する
- リンク先URLは推測で書かず、WebFetch等で到達を確認するか「要確認」と明記する

例：`自作ファイル集\プロンプト集\11_検索AI・データベース一覧.xlsx`（6シート・36リンク）
