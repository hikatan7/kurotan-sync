@echo off
chcp 65001 >nul
cd /d "%~dp0"
start "" pythonw "貼り付けツール.pyw"
if errorlevel 1 start "" python "貼り付けツール.pyw"
