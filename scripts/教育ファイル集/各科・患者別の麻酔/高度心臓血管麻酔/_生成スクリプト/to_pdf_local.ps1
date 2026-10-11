# OneDrive 同期下のファイルは Word が開けずに固まることがある。
# いったんローカルの作業フォルダへ写してから Word にかけ、結果を書き戻す。
param([Parameter(Mandatory=$true)][string]$Name)
$ErrorActionPreference = "Stop"
$base = "C:/Users/junch/OneDrive/_旧デスクトップ/教育ファイル集/高度心臓血管麻酔"
$work = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive---------/585edbaa-4ad2-4d47-b0c9-dc8724e340b8/scratchpad/word"
New-Item -ItemType Directory -Force -Path $work | Out-Null

$srcDocx = "$base/$Name.docx"
$dstPdf  = "$base/$Name.pdf"
$tmpDocx = "$work/w.docx"
$tmpPdf  = "$work/w.pdf"

Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 1000
foreach ($v in @("16.0", "15.0")) {
  $r = "HKCU:\Software\Microsoft\Office\$v\Word\Resiliency"
  if (Test-Path $r) { Remove-Item -Path $r -Recurse -Force -ErrorAction SilentlyContinue }
}
Copy-Item -LiteralPath $srcDocx -Destination $tmpDocx -Force
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

Copy-Item -LiteralPath $tmpPdf -Destination $dstPdf -Force
Copy-Item -LiteralPath $tmpDocx -Destination $srcDocx -Force
Write-Output "done"
