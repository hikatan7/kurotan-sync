@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo テーマ別（蘇生・急変対応）の目録を作り直しています...
python "..\麻酔科ミニ教科書シリーズ\26_蘇生アルゴリズムの変遷と周術期心停止\_生成スクリプト\portal26.py"
if errorlevel 1 goto err
echo 目録を作り直しています...
python "1_目録を作る.py"
if errorlevel 1 goto err
echo ポータルを組み直しています...
python "2_ポータルを作る.py"
if errorlevel 1 goto err
echo.
echo 完了しました。1つ上のフォルダの 麻酔資料ポータル.html を開いてください。
pause
exit /b 0
:err
echo.
echo エラーが出ました。上の表示をそのままClaudeに見せてください。
pause
