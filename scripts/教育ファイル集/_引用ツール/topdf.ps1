# docx を PDF にする（どの本でも使える）。
#   powershell -File topdf.ps1 -Dir "<フォルダ>" -Name "<拡張子なしのファイル名>"
# OneDrive 直下だと Word が開けずに固まることがあるので、
# ローカルの作業フォルダへ写してから処理し、結果を書き戻す。
param(
  [Parameter(Mandatory=$true)][string]$Dir,
  [Parameter(Mandatory=$true)][string]$Name
)
$ErrorActionPreference = "Stop"
$work = "$env:LOCALAPPDATA/Temp/claude_word"
New-Item -ItemType Directory -Force -Path $work | Out-Null
$tmpDocx = "$work/w.docx"; $tmpPdf = "$work/w.pdf"

Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 1200
foreach ($v in @("16.0", "15.0")) {
  $r = "HKCU:\Software\Microsoft\Office\$v\Word\Resiliency"
  if (Test-Path $r) { Remove-Item -Path $r -Recurse -Force -ErrorAction SilentlyContinue }
}
Copy-Item -LiteralPath "$Dir/$Name.docx" -Destination $tmpDocx -Force
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

Copy-Item -LiteralPath $tmpPdf -Destination "$Dir/$Name.pdf" -Force
Copy-Item -LiteralPath $tmpDocx -Destination "$Dir/$Name.docx" -Force
Write-Output "done"
