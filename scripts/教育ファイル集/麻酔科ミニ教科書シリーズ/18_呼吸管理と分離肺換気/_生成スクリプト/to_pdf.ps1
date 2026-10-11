$ErrorActionPreference = "Stop"
$docx = "C:/Users/junch/OneDrive/デスクトップ/教育ファイル集/麻酔科ミニ教科書シリーズ/18_呼吸管理と分離肺換気/呼吸管理と分離肺換気.docx"
$tmp  = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive-------/d9b26fe0-bebf-4669-aeec-3acfee1a3350/scratchpad/vol18.pdf"
$pdf  = "C:/Users/junch/OneDrive/デスクトップ/教育ファイル集/麻酔科ミニ教科書シリーズ/18_呼吸管理と分離肺換気/呼吸管理と分離肺換気.pdf"
Write-Output "open"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($docx)
Write-Output "opened"
$doc.Fields.Update() | Out-Null
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
$doc.Repaginate()
$pages = $doc.ComputeStatistics(2)
Write-Output ("pages=" + $pages)
$doc.Save()
Write-Output "saved"
$doc.ExportAsFixedFormat($tmp, 17)
Write-Output "exported"
$doc.Close(0)
$word.Quit()
Copy-Item -LiteralPath $tmp -Destination $pdf -Force
Write-Output "done"
