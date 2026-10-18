$ErrorActionPreference='Continue'
try { [Console]::OutputEncoding=[Text.Encoding]::UTF8 } catch {}
Set-Location 'C:\'
[Environment]::CurrentDirectory='C:\'

$old='C:\Users\junch\OneDrive\_旧デスクトップ'
$new='C:\Users\junch\OneDrive\デスクトップ'
$tmp='C:\Users\junch\Desktop'

Add-Type -Namespace KFR -Name Api -MemberDefinition @"
[DllImport("shell32.dll")]
public static extern int SHSetKnownFolderPath(ref System.Guid rfid, uint dwFlags, System.IntPtr hToken, [MarshalAs(UnmanagedType.LPWStr)] string pszPath);
"@
$guid=[Guid]'B4BFCC3A-DB2C-424C-B029-7FE99A87C641'

Write-Host "================================================"
Write-Host " デスクトップのフォルダ名を元に戻します"
Write-Host "================================================"

if (Test-Path -LiteralPath $new) {
  Write-Host "[完了済] すでに デスクトップ が存在します。処理は不要です。" -ForegroundColor Green
  return
}
if (-not (Test-Path -LiteralPath $old)) {
  Write-Host "[中止] _旧デスクトップ が見つかりません。" -ForegroundColor Red
  return
}

Write-Host ""
Write-Host "[1/6] デスクトップ登録を一時退避..."
if (-not (Test-Path -LiteralPath $tmp)) { New-Item -ItemType Directory -Path $tmp -Force | Out-Null }
$null=[KFR.Api]::SHSetKnownFolderPath([ref]$guid,0,[IntPtr]::Zero,$tmp)

Write-Host "[2/6] エクスプローラーを一時停止..."
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 4

Write-Host "[3/6] フォルダ名を変更中..."
$ok=$false
for ($i=1; $i -le 6; $i++) {
  try { Rename-Item -LiteralPath $old -NewName 'デスクトップ' -ErrorAction Stop; $ok=$true; break }
  catch { Write-Host ("    試行{0} 失敗（まだ掴んでいるアプリがあります）" -f $i); Start-Sleep -Seconds 2 }
}

if (-not $ok) {
  $null=[KFR.Api]::SHSetKnownFolderPath([ref]$guid,0,[IntPtr]::Zero,$old)
  if (-not (Get-Process -Name explorer -ErrorAction SilentlyContinue)) { Start-Process explorer.exe }
  Write-Host ""
  Write-Host "[失敗] リネームできませんでした。" -ForegroundColor Red
  Write-Host "Claude・エクスプローラー・エディタなど、デスクトップを開いているアプリを全て閉じてから再実行してください。"
  Write-Host "デスクトップの状態は元に戻してあります。"
  return
}
Write-Host "    成功: _旧デスクトップ → デスクトップ" -ForegroundColor Green

Write-Host "[4/6] デスクトップ登録先を確定..."
$null=[KFR.Api]::SHSetKnownFolderPath([ref]$guid,0,[IntPtr]::Zero,$new)

Write-Host "[5/6] アイコン参照とショートカットのパスを修正..."
$srcP = $old + '\'
$dstP = $new + '\'
$enc = New-Object System.Text.UnicodeEncoding($false,$true)
$fixed=0
foreach ($d in (Get-ChildItem -LiteralPath $new -Directory -Force -ErrorAction SilentlyContinue)) {
  $ini = Join-Path $d.FullName 'desktop.ini'
  if (-not (Test-Path -LiteralPath $ini)) { continue }
  $t = $enc.GetString([IO.File]::ReadAllBytes($ini)).TrimStart([char]0xFEFF)
  if ($t -notlike "*$srcP*") { continue }
  $item = Get-Item -LiteralPath $ini -Force
  $at = $item.Attributes
  $item.Attributes = [IO.FileAttributes]::Normal
  [IO.File]::WriteAllText($ini, $t.Replace($srcP,$dstP), $enc)
  (Get-Item -LiteralPath $ini -Force).Attributes = $at
  $fixed++
  Write-Host ("    アイコン修正: " + $d.Name)
}
$sh = New-Object -ComObject WScript.Shell
foreach ($base in @($new, (Join-Path $new '_重複レビュー'))) {
  if (-not (Test-Path -LiteralPath $base)) { continue }
  foreach ($f in (Get-ChildItem -LiteralPath $base -Filter *.lnk -File -ErrorAction SilentlyContinue)) {
    $l = $sh.CreateShortcut($f.FullName); $ch=$false
    if ($l.TargetPath       -like "*$srcP*") { $l.TargetPath       = $l.TargetPath.Replace($srcP,$dstP);       $ch=$true }
    if ($l.IconLocation     -like "*$srcP*") { $l.IconLocation     = $l.IconLocation.Replace($srcP,$dstP);     $ch=$true }
    if ($l.WorkingDirectory -like "*$srcP*") { $l.WorkingDirectory = $l.WorkingDirectory.Replace($srcP,$dstP); $ch=$true }
    if ($ch) { $l.Save(); Write-Host ("    ショートカット修正: " + $f.Name) }
  }
}

Write-Host "[6/6] アイコンキャッシュを再生成..."
$ex = "$env:LocalAppData\Microsoft\Windows\Explorer"
foreach ($f in (Get-ChildItem -LiteralPath $ex -Force -ErrorAction SilentlyContinue)) {
  if ($f.Name -like 'iconcache*.db') { try { [IO.File]::Delete($f.FullName) } catch {} }
}
if (-not (Get-Process -Name explorer -ErrorAction SilentlyContinue)) { Start-Process explorer.exe }
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host " 完了しました" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ("デスクトップ: " + [Environment]::GetFolderPath('Desktop'))
Write-Host ("アイコン修正: " + $fixed + " フォルダ")
Write-Host ""
Write-Host "Claude を起動すると、71件の会話が開けるようになります。"
