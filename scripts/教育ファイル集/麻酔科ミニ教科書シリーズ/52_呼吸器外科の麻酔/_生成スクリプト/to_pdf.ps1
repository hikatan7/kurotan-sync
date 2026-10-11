$ErrorActionPreference = "Stop"
$d = "C:\Users\junch\AppData\Local\Temp\claude\C--Users-junch-OneDrive---------\83b04e79-2de1-44b3-b1ed-48b63a9b67f7\scratchpad\v52"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $doc = $word.Documents.Open("$d\$args", $false, $false)
  foreach ($t in $doc.TablesOfContents) { $t.Update() }
  $doc.Repaginate()
  foreach ($t in $doc.TablesOfContents) { $t.Update() }
  "pages=" + $doc.ComputeStatistics(2)
  $doc.Save()
  $doc.ExportAsFixedFormat("$d\" + [IO.Path]::GetFileNameWithoutExtension($args[0]) + ".pdf", 17)
  $doc.Close(0)
} finally { $word.Quit() }
