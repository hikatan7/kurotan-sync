@echo off
chcp 65001 > nul
cd /d "%~dp0"
start "" pythonw "ファイル整理ツール.py"
if errorlevel 1 (
  start "" python "ファイル整理ツール.py"
)
