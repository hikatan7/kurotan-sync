@echo off
chcp 65001 > nul
cd /d "%~dp0"
start "" pythonw "ファイル保護ツール.py"
if errorlevel 1 (
  start "" python "ファイル保護ツール.py"
)
