$ErrorActionPreference = "Stop"
$base = "C:/Users/junch/OneDrive/_旧デスクトップ/経営学/経営学テキスト/急性期病院で学ぶ_MBAビジネスアナリティクス別冊_定量分析の入口"
$docx = "$base.docx"
$pdf  = "$base.pdf"
if (Test-Path $pdf) { Remove-Item -LiteralPath $pdf -Force }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($docx)
$doc.Fields.Update() | Out-Null
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
$doc.Repaginate()
Write-Output ("pages=" + $doc.ComputeStatistics(2))
Write-Output ("chars=" + $doc.ComputeStatistics(3))
$doc.Save()
$doc.ExportAsFixedFormat($pdf, 17)
$doc.Close(0)
$word.Quit()
Write-Output "done"
