$ErrorActionPreference = "Stop"
$d = Split-Path -Parent $PSScriptRoot
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $doc = $word.Documents.Open("$d\$($args[0])", $false, $false)
  foreach ($t in $doc.TablesOfContents) { $t.Update() }
  $doc.Repaginate()
  foreach ($t in $doc.TablesOfContents) { $t.Update() }
  "pages=" + $doc.ComputeStatistics(2)
  $doc.Save()
  $doc.ExportAsFixedFormat("$d\" + [IO.Path]::GetFileNameWithoutExtension($args[0]) + ".pdf", 17)
  $doc.Close(0)
} finally { $word.Quit() }
