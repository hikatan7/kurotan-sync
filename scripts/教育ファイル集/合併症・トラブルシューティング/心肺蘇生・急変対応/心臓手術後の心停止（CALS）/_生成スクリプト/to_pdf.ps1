# docx を Word で開き、目次とフィールドを更新して PDF を書き出す（ローカル作業フォルダ経由）
param([string]$name)
$ErrorActionPreference = "Stop"
$dir  = "C:/Users/junch/OneDrive/_旧デスクトップ/教育ファイル集/ICLS_開心術後ALS配布資料"
$work = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive---------/c3009d8a-0cff-4970-913e-1e17d2a4990d/scratchpad/word"
New-Item -ItemType Directory -Force -Path $work | Out-Null
$stamp = Get-Date -Format "HHmmss"
$tmpDocx = "$work/w_$stamp.docx"; $tmpPdf = "$work/w_$stamp.pdf"
Copy-Item -LiteralPath "$dir/$name.docx" -Destination $tmpDocx -Force
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDocx, $false, $false, $false)
$doc.Fields.Update() | Out-Null
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
$doc.Repaginate()
Write-Output ("pages=" + $doc.ComputeStatistics(2))
$doc.Save()
$doc.ExportAsFixedFormat($tmpPdf, 17)
$doc.Close(0)
$word.Quit()
Start-Sleep -Milliseconds 600
Copy-Item -LiteralPath $tmpPdf -Destination "$dir/$name.pdf" -Force
Copy-Item -LiteralPath $tmpDocx -Destination "$dir/$name.docx" -Force
Write-Output "done"
