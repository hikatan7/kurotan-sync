$ErrorActionPreference = "Stop"
$docx = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive-------/d9b26fe0-bebf-4669-aeec-3acfee1a3350/scratchpad/vol18.docx"
$pdf  = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive-------/d9b26fe0-bebf-4669-aeec-3acfee1a3350/scratchpad/vol18.pdf"
Write-Output "start"
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
$doc.ExportAsFixedFormat($pdf, 17)
$doc.Close(0)
$word.Quit()
Write-Output "done"
