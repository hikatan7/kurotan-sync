$ErrorActionPreference = "Stop"
$base = "C:/Users/junch/OneDrive/_旧デスクトップ/教育ファイル集/高度心臓血管麻酔"
$docx = "$base/第Ⅷ章_心臓麻酔と神経モニタリング.docx"
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 1000
Write-Output ("step1 起動 " + (Get-Date -Format HH:mm:ss))
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
Write-Output ("step2 開く " + (Get-Date -Format HH:mm:ss))
$doc = $word.Documents.Open($docx, $false, $false, $false)
Write-Output ("step3 開いた " + (Get-Date -Format HH:mm:ss) + " 段落数=" + $doc.Paragraphs.Count)
$doc.Fields.Update() | Out-Null
Write-Output ("step4 フィールド更新 " + (Get-Date -Format HH:mm:ss))
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
Write-Output ("step5 目次更新 " + (Get-Date -Format HH:mm:ss))
$doc.Repaginate()
Write-Output ("step6 改ページ " + (Get-Date -Format HH:mm:ss) + " pages=" + $doc.ComputeStatistics(2))
$doc.Close(0)
$word.Quit()
Write-Output "done"
