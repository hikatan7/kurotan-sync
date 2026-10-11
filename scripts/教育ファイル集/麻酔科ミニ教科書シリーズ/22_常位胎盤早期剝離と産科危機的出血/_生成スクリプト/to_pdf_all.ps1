$ErrorActionPreference = "Stop"
$base = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive---------/0a01b107-1760-4b4d-a5de-e53cfa73f6fc/scratchpad/vol22"
Get-Process WINWORD, POWERPNT -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 900
Get-ChildItem -LiteralPath $base -Force -File | Where-Object { $_.Name -like "~`$*" } | Remove-Item -Force

$word = New-Object -ComObject Word.Application
$word.Visible = $false
foreach ($n in @("vol22", "short22")) {
    $docx = "$base/$n.docx"
    $pdf = "$base/$n.pdf"
    if (Test-Path $pdf) { Remove-Item -LiteralPath $pdf -Force }
    $doc = $word.Documents.Open($docx)
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Repaginate()
    Write-Output ($n + " pages=" + $doc.ComputeStatistics(2))
    $doc.Save()
    $doc.ExportAsFixedFormat($pdf, 17)
    $doc.Close(0)
}
$word.Quit()

$ppt = New-Object -ComObject PowerPoint.Application
$pptx = (Resolve-Path "$base/slides22.pptx").Path
$pdf = ($base + "/slides22.pdf") -replace "/", "\\"
if (Test-Path $pdf) { Remove-Item -LiteralPath $pdf -Force }
$pres = $ppt.Presentations.Open($pptx, $false, $false, $true)
$pres.SaveAs($pdf, 32)
Write-Output ("slides22 slides=" + $pres.Slides.Count)
$pres.Close()
$ppt.Quit()
Write-Output "done"
