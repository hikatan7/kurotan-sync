param([string]$list)
$files = Get-Content -LiteralPath $list -Encoding UTF8 | Where-Object { $_.Trim() -ne "" }
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
  foreach ($f in $files) {
    $p = [System.IO.Path]::ChangeExtension($f, ".pdf")
    $d = $w.Documents.Open($f, $false, $true)
    $d.ExportAsFixedFormat($p, 17)
    $d.Close($false)
  }
} finally { $w.Quit() }
