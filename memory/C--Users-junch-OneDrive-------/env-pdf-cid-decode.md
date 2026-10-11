---
name: env-pdf-cid-decode
description: 官公庁・国立大学法人PDFはCID埋込でテキスト抽出が文字化け→グリフ輪郭照合で復号するスクリプトを自作ファイル集に保存済み
metadata: 
  node_type: memory
  type: reference
  originSessionId: 292747d4-72f9-4ff4-a8b8-957155f55b20
  modified: 2026-08-29T14:12:56.775Z
---

国立大学法人の財務諸表PDF（富山大学など）は Identity-H＋MS明朝サブセット埋込で **cmapもToUnicodeも無い**。PyMuPDFは別字に化け、pdfplumberは `(cid:1234)` を返す。OCRは不要で、グリフの輪郭を照合すれば完全に復号できる。

方法: 埋込フォントをfitzで抽出→fontToolsの`DecomposingRecordingPen`で各GIDの輪郭を署名化→`C:\Windows\Fonts\msmincho.ttc` / `msgothic.ttc` の同じ署名の文字に逆引き。サブセットは元フォントから切り出されているので輪郭は完全一致する。空輪郭のGIDは空白として扱う。数字はArial/Times等の単純フォントなのでpdfplumberがそのまま返す。

スクリプト: `デスクトップ\自作ファイル集\PDF文字化け復号\`
- `decode.py` … 参照テーブル（ref.pkl）を作る。先に1回だけ実行
- `decode_cid_pdf.py <in.pdf> <out.txt>` … 座標で行を再構成し、列はタブ区切りで出力（表がそのまま読める）

[[workflow-financial-pdf-protocol]] のPDF読み取りが文字化けしたら、まずこれを試す。
