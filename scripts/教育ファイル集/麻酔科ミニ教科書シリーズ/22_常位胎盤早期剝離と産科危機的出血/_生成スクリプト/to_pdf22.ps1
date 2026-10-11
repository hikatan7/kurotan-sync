$ErrorActionPreference = "Stop"
$dir  = "C:/Users/junch/OneDrive/_旧デスクトップ/教育ファイル集/麻酔科ミニ教科書シリーズ/22_常位胎盤早期剝離と産科危機的出血"
$name = "常位胎盤早期剝離と産科危機的出血"
$work = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive---------/585edbaa-4ad2-4d47-b0c9-dc8724e340b8/scratchpad/word"
New-Item -ItemType Directory -Force -Path $work | Out-Null
$tmpDocx = "$work/w22.docx"; $tmpPdf = "$work/w22.pdf"
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 1200
foreach ($v in @("16.0", "15.0")) {
  $r = "HKCU:\Software\Microsoft\Office\$v\Word\Resiliency"
  if (Test-Path $r) { Remove-Item -Path $r -Recurse -Force -ErrorAction SilentlyContinue }
}
Copy-Item -LiteralPath "$dir/$name.docx" -Destination $tmpDocx -Force
if (Test-Path $tmpPdf) { Remove-Item -LiteralPath $tmpPdf -Force }
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
