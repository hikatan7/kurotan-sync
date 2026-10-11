# くろたん同期 sync.ps1
# 2台のパソコンで、くろたんの記憶・設定・自作スクリプトを GitHub 経由でそろえる。
#   記憶と設定 … 双方向。新しいほうのファイルが勝つ（削除は伝わらない）
#   自作スクリプト … 作業フォルダ → 保管場所の一方向（配布は OneDrive が担う）
# 作業の始めと終わりに「くろたん同期.bat」をダブルクリックして使う。

$ErrorActionPreference = 'Continue'
$Repo   = Join-Path $env:USERPROFILE 'kurotan-sync'
$Claude = Join-Path $env:USERPROFILE '.claude'
$Work   = Join-Path $env:USERPROFILE 'OneDrive\_旧デスクトップ'
$ScriptExt = '*.py','*.ps1','*.bas','*.vbs','*.bat','*.cmd','*.cls','*.psm1'

function Step($msg) { Write-Host "`n== $msg" -ForegroundColor Cyan }
function Robo { param($src, $dst, [string[]]$files = @('*'), [string[]]$extra = @())
    # /XO: 相手側のほうが新しいファイルは上書きしない  /E: 下位フォルダも
    robocopy $src $dst $files /E /XO /R:1 /W:1 /NFL /NDL /NJH /NJS /NP @extra | Out-Null
    if ($LASTEXITCODE -ge 8) { Write-Host "  コピーに失敗: $src -> $dst" -ForegroundColor Red }
    $global:LASTEXITCODE = 0
}

Set-Location $Repo

Step '1/4 GitHub から最新を受け取る'
git pull --rebase --autostash 2>&1 | Write-Host

Step '2/4 記憶をそろえる（新しいほうが勝つ）'
$repoMem = Join-Path $Repo 'memory'
New-Item -ItemType Directory -Force $repoMem | Out-Null
# 保管場所 → このパソコン
Get-ChildItem $repoMem -Directory | ForEach-Object {
    Robo $_.FullName (Join-Path $Claude "projects\$($_.Name)\memory")
}
# このパソコン → 保管場所
Get-ChildItem (Join-Path $Claude 'projects') -Directory -EA SilentlyContinue | ForEach-Object {
    $m = Join-Path $_.FullName 'memory'
    if (Test-Path $m) { Robo $m (Join-Path $repoMem $_.Name) }
}
# 設定ファイル
if (Test-Path (Join-Path $Repo 'claude\settings.json')) {
    Robo (Join-Path $Repo 'claude') $Claude @('settings.json') @('/LEV:1')
}
Robo $Claude (Join-Path $Repo 'claude') @('settings.json') @('/LEV:1')

Step '3/4 自作スクリプトの控えを取る'
if (Test-Path $Work) {
    Robo $Work (Join-Path $Repo 'scripts') $ScriptExt @('/XD', '__pycache__', '.git')
} else {
    Write-Host "  作業フォルダが見つかりません: $Work" -ForegroundColor Yellow
}

Step '4/4 GitHub へ送る'
git add -A
$changes = git status --porcelain
if ($changes) {
    $n = @($changes).Count
    git commit -q -m "sync $env:COMPUTERNAME $(Get-Date -Format 'yyyy-MM-dd HH:mm') ($n files)"
    if ($LASTEXITCODE -ne 0) { Write-Host '  記録に失敗しました。' -ForegroundColor Red; exit 1 }
    git push 2>&1 | Write-Host
    if ($LASTEXITCODE -eq 0) { Write-Host "  $n 件の変更を送りました。" -ForegroundColor Green }
    else { Write-Host '  GitHub へ送れませんでした。ネット接続とログインを確認してください。' -ForegroundColor Red }
} else {
    git push 2>&1 | Out-Null
    Write-Host '  変更はありません。' -ForegroundColor Green
}
