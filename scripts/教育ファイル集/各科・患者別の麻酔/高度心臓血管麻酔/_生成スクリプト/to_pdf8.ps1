$ErrorActionPreference = "Stop"
$base = "C:/Users/junch/OneDrive/_旧デスクトップ/教育ファイル集/高度心臓血管麻酔"
$name = "第Ⅷ章_心臓麻酔と神経モニタリング"
$docx = "$base/$name.docx"
$pdf  = "$base/$name.pdf"

Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 1200

# 強制終了のあとは Word が「ドキュメントの回復」作業ウィンドウを出して自動化を止める。
# 回復エントリと無効化項目を消してから起動する。
foreach ($v in @("16.0", "15.0")) {
  $r = "HKCU:\Software\Microsoft\Office\$v\Word\Resiliency"
  if (Test-Path $r) { Remove-Item -Path $r -Recurse -Force -ErrorAction SilentlyContinue }
}
if (Test-Path $pdf) { Remove-Item -LiteralPath $pdf -Force }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$word.Options.SaveInterval = 0
$doc = $word.Documents.Open($docx, $false, $false, $false)
$doc.Fields.Update() | Out-Null
foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
$doc.Repaginate()
Write-Output ("pages=" + $doc.ComputeStatistics(2))
$doc.Save()
$doc.ExportAsFixedFormat($pdf, 17)
$doc.Close(0)
$word.Quit()
Write-Output "done"
