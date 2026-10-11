$ErrorActionPreference = "Stop"
$docx = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive-------/d9b26fe0-bebf-4669-aeec-3acfee1a3350/scratchpad/toc.docx"
$pdf  = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive-------/d9b26fe0-bebf-4669-aeec-3acfee1a3350/scratchpad/toc.pdf"
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 600
Get-ChildItem -LiteralPath "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive-------/d9b26fe0-bebf-4669-aeec-3acfee1a3350/scratchpad" -Force -File | Where-Object { $_.Name -like "~`$*" } | Remove-Item -Force
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
