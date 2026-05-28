@echo off
title JANET - Bioinformatics Desktop Assistant
color F0
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo First run setup is needed.
  echo Double-click install_helixmind_bio_ai.bat first.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" janet_chat.py
