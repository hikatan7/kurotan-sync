@echo off
chcp 65001 >nul
if "%~1"=="" (
    echo Excelファイルをこのバッチファイルにドラッグ＆ドロップしてください。
    pause
    exit /b
)
python "%~dp0患者データ匿名化.py" %*
pause
