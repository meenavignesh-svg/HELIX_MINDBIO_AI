@echo off
title Professor Voice Assistant
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo First run setup needed.
  echo.
  echo Double-click install.bat first, then open Professor.bat again.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" main.py
pause
