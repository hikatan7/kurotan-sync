# docx を Word で開き、目次とフィールドを更新して PDF を書き出す（一時フォルダ経由・SaveAs2）
param([string]$name)
$ErrorActionPreference = "Stop"
$dir  = Join-Path $PSScriptRoot ".."
$work = Join-Path $env:TEMP "ivroute_word"
New-Item -ItemType Directory -Force -Path $work | Out-Null
$stamp = Get-Date -Format "HHmmss"
$tmpDocx = Join-Path $work "w_$stamp.docx"; $tmpPdf = Join-Path $work "w_$stamp.pdf"
Copy-Item -LiteralPath (Join-Path $dir "$name.docx") -Destination $tmpDocx -Force
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($tmpDocx, $false, $false, $false)
$doc.Fields.Update() | Out-Null
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
$doc.Repaginate()
Write-Output ("pages=" + $doc.ComputeStatistics(2))
$doc.SaveAs2([string]$tmpDocx, 16)
$doc.SaveAs2([string]$tmpPdf, 17)
$doc.Close(0)
$word.Quit()
Start-Sleep -Milliseconds 600
Copy-Item -LiteralPath $tmpPdf -Destination (Join-Path $dir "$name.pdf") -Force
Copy-Item -LiteralPath $tmpDocx -Destination (Join-Path $dir "$name.docx") -Force
Write-Output "done"
