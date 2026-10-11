
$ErrorActionPreference = "Stop"
$src = "C:\Users\junch\AppData\Local\Temp\claude\C--Users-junch-OneDrive---------\b1b32ccc-9630-41e9-b3f7-0c43af361005\scratchpad\v30\ICUの人工呼吸管理.docx"
$dst = "C:\Users\junch\AppData\Local\Temp\claude\C--Users-junch-OneDrive---------\b1b32ccc-9630-41e9-b3f7-0c43af361005\scratchpad\v30\ICUの人工呼吸管理.pdf"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($src, $false, $false)
    foreach ($t in $doc.TablesOfContents) { $t.Update() }
    $doc.Repaginate()
    $pages = $doc.ComputeStatistics(2)
    Write-Output ("pages=" + $pages)
    $doc.ExportAsFixedFormat($dst, 17)
    $doc.Close(-1)
} finally {
    $word.Quit()
}
