---
name: env-word-com-doc-generation
description: Office文書生成の環境事情 — Python 3.12+openpyxlは使用可(2026-07-17確認)、LibreOffice無し、Word文書はPowerShell+Word COMで生成(手順・注意点)
metadata: 
  node_type: memory
  type: project
  originSessionId: fdbdc720-d3c4-4943-a77c-c858d93ee9b0
  modified: 2026-08-14T02:56:59.200Z
---

ユーザーのPC(Windows 11)の実行環境(2026-07-17更新):
- **Python 3.12.10 + openpyxl 3.1.5 が使用可能になった**(2026-07-04時点では無かった)。xlsx生成はopenpyxlでOK。
- Node.js は未確認(以前は無し)。LibreOffice(soffice)は無い → xlsxスキルのrecalc.pyは使えない。**再計算はExcel COMで行う**(`$excel.CalculateFullRebuild()` → Save → openpyxl data_only=Trueで検証)。
- MS Office はインストール済み。Excel COMの注意: Power Query接続付きブックはopenpyxlで再保存すると接続が壊れる → 新シートはopenpyxlで別ブックに作り、Excel COMの `Sheets.Copy(Before)` で合体し、外部参照 `[ファイル名]` を `Cells.Replace` で除去する方式が実績あり([[project-receipt-tool-workbook]]で使用)。

**Why:** Word/Excel/PowerPoint ファイル生成のたびにランタイム探しで失敗しないため。

**How to apply:** Word文書は PowerShell + Word COM (`New-Object -ComObject Word.Application`) で生成する。実績ある手順(2026-07-05、[[workflow-chrome-search-two-modes]]の簡易検索Word出力で使用):
1. .ps1 をスクラッチパッドに Write → **UTF-8 BOM に再エンコードしてから実行**(PS5.1はBOM無しUTF-8の日本語を文字化けさせる): `[IO.File]::WriteAllText($p, [IO.File]::ReadAllText($p), [Text.UTF8Encoding]::new($true))`
2. `$word.Visible=$false; $word.DisplayAlerts=0`、try/finally で `$word.Quit()`
3. A4は `PageSetup.PaperSize=7`、標準スタイルは `$doc.Styles.Item(-1)` でメイリオ+`DisableLineHeightGrid=$true`(行グリッド無効化が1枚収めに必須)
4. ハイパーリンクは `$doc.Hyperlinks.Add($sel.Range, $url, [Type]::Missing, [Type]::Missing, $text)`
5. ページ数確認は `$doc.ComputeStatistics(2)`、保存は `SaveAs2($path, 16)`
6. 保存先はデスクトップ = `C:\Users\junch\OneDrive\デスクトップ`

実績スクリプトの雛形: スクラッチパッドの build_doc.ps1(セッション限りなので、構造はこのメモの手順を再現する)

**PDF化の可否(2026-08-14 確認)**
- **PowerPoint COM は正常に動く**。pptx→PDF は `$app.Presentations.Open($in,$true,$false,$false)` →
  `$pres.SaveAs($out, 32)`。`ExportAsFixedFormat` は PS5.1 から引数型エラーになるので **SaveAs(…,32) を使う**。
  → スライドの見た目検証は「PDFに出す→PyMuPDFで画像化して読む」が唯一確実な方法。pptx の座標計算だけでは判断を誤る。
- **Word COM も正常に動く（2026-08-21 訂正）**。docx→PDF は
  `$doc.ExportAsFixedFormat($dst, 17)`。TOC は先に
  `foreach ($toc in $doc.TablesOfContents) { $toc.Update() }` → `$doc.Repaginate()`、
  ページ数は `$doc.ComputeStatistics(2)`、`$doc.Close(-1)` にすると docx 側も
  保存され目次にページ番号が入る（Ctrl+A→F9 が不要になる）。
  **「Word COM がハングする」という以前の記述は誤りだった。真因は ps1 の BOM 欠落**で、
  bash のヒアドキュメントで ps1 を書くと BOM が付かず日本語パスが化けて
  `Documents.Open` が「コマンドは正常終了できませんでした」で落ちるか無反応になる。
  → ps1 は必ず Python から `open(p,'wb').write(u'﻿'.encode('utf-8') + ps.encode('utf-8'))`
  で BOM 付き UTF-8 として書き出すこと。
- ハングした Word を kill すると次回起動時に「前回開いた時に重大なエラーが発生しました。
  開きますか？」という NUIDialog が出て `Documents.Open` ごとブロックする。
  同じファイル名で再試行せず、別名にするか Word プロセスを整理してから開き直す。
- docx を HTML で二重に組んで headless Chrome `--print-to-pdf` で出す方法も有効
  （[[project-preop-assessment-textbook]] の dox.py / htmldoc.py 二系統）。
  ただし Word とは行送りが違うので頁数は一致しない。配布用は Word 出力を正とする。
- `pdftoppm` は未インストール。PDFの画像化は **PyMuPDF**(`page.get_pixmap(dpi=…).save(png)`)。

**OneDrive 同期フォルダ上の docx を Word COM で開くとハングする**（2026-09-09）。
python-docx で保存した直後の 4〜5 MB の docx を `Documents.Open` しようとすると、
ダイアログも出ないまま何分でも返らない（Visible=$false）。強制終了すると
`~$xxx.docx` が残り、次回は「読み取り専用なので上書き保存できません」で失敗する。

**How to apply:** 教科書のような大きい docx は
(1) ビルドから PDF 変換までスクラッチパッド（`%LOCALAPPDATA%\Temp\claude\...`）で完結させ、
(2) 完成した docx / PDF だけをデスクトップへコピーする。
失敗したら WINWORD プロセスを止め、`~$` ロックファイルを消してから再実行する。

**`$doc.Fields.Update()` を全文書に掛けるとハングすることがある**（2026-09-14）。
⑥（89頁・フィールド71個）で、`Fields.Update()` を呼ぶと CPU を食い続けたまま
1時間以上返らなかった。同じ docx が、その行を外すと **開く0.4秒／組版1秒／PDF出力10秒**
で終わる。目次のページ番号を入れたいだけなら
`foreach ($t in $doc.TablesOfContents) { $t.Update() }`（0.75秒）だけで足り、
`Fields.Update()` は使わないこと。
`Repaginate()` と `Save()` も、ハングしたときの容疑者として外して試す価値がある。

**PowerPoint COM でスライドを編集するときの落とし穴**（2026-09-17）
- `TextRange.Paragraphs(n).Text = "…`r"` で段落を差し替えると、末尾の CR が
  **空段落を1つ増やし、以降の段落番号がずれる**。結果、直したはずの行が残り
  古い行と二重に並ぶ。段落単位の置換はやめて、
  `TextFrame.DeleteText()` → `TextRange.Text = [string]::Join("`r", $lines)`
  と**本文をまるごと入れ替える**。書式は流し込み後に Paragraphs をループして設定する。
- **前のセッションの POWERPNT プロセスが残っていると、`Presentations.Open(…, ReadOnly=$false)`
  したあとの `Save()` が例外も出さずに効かない**。`$d.ReadOnly` は 0 を返すのに
  保存されない。編集前に `Get-Process POWERPNT | Stop-Process -Force`、
  編集後は**別セッションで開き直して内容を読み直す**まで成功と見なさない。
- 既存デッキに体裁を揃えたスライドを足すなら、**同じレイアウトの既存スライドを
  `Slides.Item(n).Duplicate()` して `MoveTo()`** し、プレースホルダの文字だけ差し替えるのが速い。
  枠・ロゴのグループごと複製されるのでデザインが確実に一致する。
  挿入は**後ろのスライドから順に**行うと、元の番号のまま位置を指定できる。
- 240MB級（動画入り）の pptx でも COM 経由の編集・保存で media は保持される。
  python-pptx で開き直す必要はない。

**2026-10-09：SaveAs2 に PowerShell の変数（Join-Path の戻り値）をそのまま渡すと、PDF 保存の段で無言で固まる。** `$doc.SaveAs2([string]$wp, [int]17)` と型を明示したら1本5秒で通った（106本を3回に分けて前面実行）。強制終了した Word は作業フォルダに隠しファイル `~$xx.docx` を残し、次に同じファイルを開くと見えない確認で止まる → 作業フォルダを変えるか `Documents.Open(path,$false,$true,$false)`（読み取り専用）で開く。python-docx で編集した docx に `$doc.Save()` をかけるのも止まる原因になった（保存せず PDF だけ書き出す）。
