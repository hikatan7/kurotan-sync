$ErrorActionPreference = "Stop"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open("C:\Users\junch\AppData\Local\Temp\claude\C--Users-junch-OneDrive---------\b1b32ccc-9630-41e9-b3f7-0c43af361005\scratchpad\v51\脳神経外科の麻酔と脳保護.docx", $false, $false)
    foreach ($t in $doc.TablesOfContents) { $t.Update() }
    $doc.Repaginate()
    $doc.ExportAsFixedFormat("C:\Users\junch\AppData\Local\Temp\claude\C--Users-junch-OneDrive---------\b1b32ccc-9630-41e9-b3f7-0c43af361005\scratchpad\v51\脳神経外科の麻酔と脳保護.pdf", 17)
    $doc.Close(-1)
} finally { $word.Quit() }
