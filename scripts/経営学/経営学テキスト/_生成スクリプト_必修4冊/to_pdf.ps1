param([string]$Name)
$ErrorActionPreference = "Stop"
$base = Join-Path (Split-Path $PSScriptRoot -Parent) $Name
$docx = "$base.docx"; $pdf = "$base.pdf"
if (Test-Path -LiteralPath $pdf) { Remove-Item -LiteralPath $pdf -Force }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
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
