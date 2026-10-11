$ErrorActionPreference = "Stop"
$base = "C:/Users/junch/OneDrive/_旧デスクトップ/教育ファイル集/麻酔科ミニ教科書シリーズ/29_声門上器具と周術期気道トラブル"
$docx = "$base/声門上器具と周術期気道トラブル.docx"
$pdf  = "$base/声門上器具と周術期気道トラブル.pdf"
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 800
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
