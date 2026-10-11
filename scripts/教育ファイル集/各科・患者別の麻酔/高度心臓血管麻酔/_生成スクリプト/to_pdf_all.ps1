# 全章をまとめて PDF にする。OneDrive 直下だと Word が固まることがあるので、
# 章ごとにローカルの作業フォルダへ写してから処理し、結果を書き戻す。
$ErrorActionPreference = "Stop"
$base = "C:/Users/junch/OneDrive/_旧デスクトップ/教育ファイル集/高度心臓血管麻酔"
$work = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive---------/585edbaa-4ad2-4d47-b0c9-dc8724e340b8/scratchpad/word"
New-Item -ItemType Directory -Force -Path $work | Out-Null
$names = @(
 "第Ⅰ章_ペースメーカー・ICDと周術期麻酔",
 "第Ⅱ章_大血管手術の脳保護",
 "第Ⅲ章_脊髄保護と髄液ドレナージ",
 "第Ⅳ章_M-TEERと僧帽弁インターベンション",
 "第Ⅴ章_TAVIと三尖弁インターベンション",
 "第Ⅵ章_透析患者の心大血管手術",
 "第Ⅶ章_人工心肺・出血と輸血・循環の目標",
 "第Ⅷ章_心臓麻酔と神経モニタリング")

Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 1200
foreach ($v in @("16.0", "15.0")) {
  $r = "HKCU:\Software\Microsoft\Office\$v\Word\Resiliency"
  if (Test-Path $r) { Remove-Item -Path $r -Recurse -Force -ErrorAction SilentlyContinue }
}
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
foreach ($n in $names) {
  $tmpDocx = "$work/w.docx"; $tmpPdf = "$work/w.pdf"
  Copy-Item -LiteralPath "$base/$n.docx" -Destination $tmpDocx -Force
  if (Test-Path $tmpPdf) { Remove-Item -LiteralPath $tmpPdf -Force }
  $doc = $word.Documents.Open($tmpDocx, $false, $false, $false)
  $doc.Fields.Update() | Out-Null
  foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
  $doc.Repaginate()
  Write-Output ($n.Substring(0,3) + " pages=" + $doc.ComputeStatistics(2))
  $doc.Save()
  $doc.ExportAsFixedFormat($tmpPdf, 17)
  $doc.Close(0)
  Copy-Item -LiteralPath $tmpPdf -Destination "$base/$n.pdf" -Force
  Copy-Item -LiteralPath $tmpDocx -Destination "$base/$n.docx" -Force
}
$word.Quit()
Write-Output "done"
