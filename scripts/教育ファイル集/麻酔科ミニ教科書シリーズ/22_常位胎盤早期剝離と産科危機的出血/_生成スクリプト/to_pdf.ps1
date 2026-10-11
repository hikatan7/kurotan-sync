$ErrorActionPreference = "Stop"
$base = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive---------/0a01b107-1760-4b4d-a5de-e53cfa73f6fc/scratchpad/vol22"
$name = $args[0]
$docx = "$base/$name.docx"
$pdf  = "$base/$name.pdf"
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 800
Get-ChildItem -LiteralPath $base -Force -File | Where-Object { $_.Name -like "~`$*" } | Remove-Item -Force
if (Test-Path $pdf) { Remove-Item -LiteralPath $pdf -Force }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($docx)
$doc.Fields.Update() | Out-Null
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
$doc.Repaginate()
Write-Output ("pages=" + $doc.ComputeStatistics(2))
$doc.Save()
$doc.ExportAsFixedFormat($pdf, 17)
$doc.Close(0)
$word.Quit()
Write-Output "done"
