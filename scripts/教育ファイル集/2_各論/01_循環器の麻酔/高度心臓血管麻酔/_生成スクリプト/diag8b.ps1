$ErrorActionPreference = "Stop"
$docx = "C:/Users/junch/AppData/Local/Temp/claude/C--Users-junch-OneDrive---------/585edbaa-4ad2-4d47-b0c9-dc8724e340b8/scratchpad/word/ch8.docx"
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 1000
Write-Output ("起動 " + (Get-Date -Format HH:mm:ss))
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($docx, $false, $false, $false)
Write-Output ("開いた " + (Get-Date -Format HH:mm:ss) + " 段落数=" + $doc.Paragraphs.Count)
$doc.Close(0); $word.Quit()
Write-Output "done"
