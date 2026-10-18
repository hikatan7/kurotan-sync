@echo off
chcp 65001 >nul
cd /d C:\
title デスクトップ名前戻し
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0デスクトップ名前戻し.ps1"
echo.
pause
