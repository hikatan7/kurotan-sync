# 新しいパソコンの一括セットアップ setup.ps1
# 「新PCセットアップ.bat」から1回だけ実行する。途中で止まっても、もう一度実行すれば続きから進む。

$ErrorActionPreference = 'Continue'
$GitHubUser = 'hikatan7'
$RepoName   = 'kurotan-sync'
$Repo   = Join-Path $env:USERPROFILE $RepoName
$Work   = Join-Path $env:USERPROFILE 'OneDrive\_旧デスクトップ'
$Kit    = $PSScriptRoot
$PyPackages = @(
    'openpyxl==3.1.5', 'python-docx==1.2.0', 'python-pptx==1.0.2', 'pywin32==312',
    'pymupdf==1.28.0', 'pypdf==6.14.2', 'pdfplumber==0.11.10', 'matplotlib==3.11.1',
    'scipy==1.18.0', 'opencv-python-headless==5.0.0.93', 'xlrd==2.0.2',
    'pyzipper==0.4.0', 'defusedxml==0.7.1'
)
$Apps = [ordered]@{
    'Git.Git'             = 'Git'
    'Python.Python.3.12'  = 'Python 3.12'
    'Google.Chrome'       = 'Google Chrome'
    'Anthropic.Claude'    = 'Claude デスクトップアプリ'
}

function Step($msg) { Write-Host "`n== $msg" -ForegroundColor Cyan }
function Ok($msg)   { Write-Host "  OK  $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "  注意 $msg" -ForegroundColor Yellow }
function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
                [Environment]::GetEnvironmentVariable('Path', 'User')
}

Write-Host '新しいパソコンのセットアップを始めます。' -ForegroundColor White

Step '1/7 前提の確認'
if ($env:USERNAME -ne 'junch') {
    Warn "ユーザー名が junch ではありません（今は $env:USERNAME）。記憶やスクリプトの場所がずれます。"
    $ans = Read-Host '  このまま続けますか？ (y/n)'
    if ($ans -ne 'y') { exit 1 }
} else { Ok 'ユーザー名は junch' }
if (Test-Path $Work) { Ok "作業フォルダあり: $Work" }
else { Warn "作業フォルダがまだ見えません: $Work （OneDrive の同期が終わってから再実行してください）" }

Step '2/7 ソフトを入れる（入っていれば飛ばす）'
foreach ($id in $Apps.Keys) {
    $null = winget list --id $id --exact --accept-source-agreements 2>$null
    if ($LASTEXITCODE -eq 0) { Ok "$($Apps[$id]) は入っています"; continue }
    Write-Host "  $($Apps[$id]) を入れています…"
    winget install --id $id --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -eq 0) { Ok "$($Apps[$id]) を入れました" } else { Warn "$($Apps[$id]) を入れられませんでした（手順書の手作業欄を参照）" }
}
Refresh-Path

Step '3/7 Python のライブラリを入れる'
py -3.12 -m pip install --upgrade pip --quiet
py -3.12 -m pip install @PyPackages --quiet
if ($LASTEXITCODE -eq 0) { Ok "$($PyPackages.Count) 個のライブラリを入れました" } else { Warn 'ライブラリの一部が入りませんでした' }

Step '4/7 フォント（Noto Sans/Serif JP）を入れる'
$fontSrc = Join-Path $Kit 'fonts'
$fontDst = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts'
$regKey  = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'
New-Item -ItemType Directory -Force $fontDst | Out-Null
Get-ChildItem $fontSrc -Filter *.ttf -EA SilentlyContinue | ForEach-Object {
    $dst = Join-Path $fontDst $_.Name
    if (-not (Test-Path $dst)) { Copy-Item $_.FullName $dst }
    New-ItemProperty -Path $regKey -Name "$($_.BaseName) (TrueType)" -Value $dst -PropertyType String -Force | Out-Null
    Ok $_.Name
}

Step '5/7 Git の基本設定'
git config --global user.name 'Junko'
git config --global user.email "$GitHubUser@users.noreply.github.com"
git config --global core.quotepath false
git config --global core.longpaths true
git config --global init.defaultBranch main
Ok 'Git の設定をしました'

Step '6/7 GitHub の保管場所を取ってくる'
if (Test-Path (Join-Path $Repo '.git')) {
    Ok '保管場所はすでにあります'
} else {
    Write-Host '  ブラウザが開いたら GitHub にログインして「Authorize」を押してください。'
    git clone "https://github.com/$GitHubUser/$RepoName.git" $Repo
    if ($LASTEXITCODE -eq 0) { Ok "保管場所を取ってきました: $Repo" } else { Warn '取ってこられませんでした。ログインを確認して再実行してください'; exit 1 }
}
git -C $Repo config core.autocrlf false

Step '7/7 くろたんの記憶と設定を戻す'
& (Join-Path $Repo 'sync.ps1')

Write-Host "`nセットアップが終わりました。手順書の「手作業で入れるもの」に進んでください。" -ForegroundColor Green
