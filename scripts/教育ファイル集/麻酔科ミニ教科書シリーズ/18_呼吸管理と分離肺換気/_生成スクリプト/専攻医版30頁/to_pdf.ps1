$ErrorActionPreference = "Stop"
$d = "C:\Users\junch\AppData\Local\Temp\claude\C--Users-junch-OneDrive---------\83b04e79-2de1-44b3-b1ed-48b63a9b67f7\scratchpad\v18s"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $doc = $word.Documents.Open("$d\呼吸管理と分離肺換気_専攻医版30頁.docx", $false, $false)
  $doc.Repaginate()
  "pages=" + $doc.ComputeStatistics(2)
  $doc.Save()
  $doc.ExportAsFixedFormat("$d\呼吸管理と分離肺換気_専攻医版30頁.pdf", 17)
  $doc.Close(0)
} finally { $word.Quit() }
