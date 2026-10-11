---
name: env-word-export-saveas2
description: Word COM の PDF 出力は ExportAsFixedFormat ではなく SaveAs2(…, 17) を使い、一時フォルダ経由で書き出してから上書きコピーする
metadata:
  type: reference
---
2026-10-07、教育ファイル集の docx を Word COM で PDF にするとき、ExportAsFixedFormat が表示されないダイアログで止まった（CPU が止まったまま戻らない）。
SaveAs2([string]$path, 17) なら速く確実に通った。PowerShell では [ref] を付けると型変換のエラーになるので、[string] で渡す。

フォルダによってはファイル保護ツールの削除禁止 ACL が付いている（[[project-file-protect-tool]]）。Word は保存時に「削除して置き換える」ので、上書きできず「読み取り専用」のエラーになる。
そこで次の順にする：docx を %TEMP% へコピー → Word で開いて目次を更新 → SaveAs2(docx, 16) と SaveAs2(pdf, 17) → Copy-Item -Force で元の場所へ上書き。コピーで上書きするだけなら削除権限は要らない。
手順は scratchpad の topdf_tmp.ps1 と exp.py（セッション限り。必要なら作り直す）。止まった WINWORD は、ウィンドウ名が空の自動化インスタンスだけを Stop-Process する。関連：[[env-word-com-doc-generation]]
