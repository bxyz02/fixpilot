@echo off
setlocal
cd /d "%~dp0"
title Problem Detective - Diagnostic Hub
set "PORT=5007"

python --version >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Install Python from python.org and select "Add Python to PATH" during setup.
  pause
  exit /b 1
)

python -c "import flask, flask_cors, pandas, openpyxl, sklearn" >nul 2>&1
if errorlevel 1 (
  echo Installing the diagnostic app's Python packages. This only needs to finish once.
  python -m pip install -r requirements.txt
  if errorlevel 1 (
    echo Package installation failed. Check your internet connection and try again.
    pause
    exit /b 1
  )
)

rem Do not open a stale server that was started from an older FixPilot build.
powershell.exe -NoProfile -Command "try{$r=Invoke-WebRequest 'http://127.0.0.1:5007/understanding' -TimeoutSec 2 -UseBasicParsing;if($r.StatusCode -eq 200){exit 0}}catch{};exit 1"
if not errorlevel 1 (
  start "" "http://127.0.0.1:5007"
  exit /b 0
)

powershell.exe -NoProfile -Command "try{$r=Invoke-WebRequest 'http://127.0.0.1:5007/health' -TimeoutSec 2 -UseBasicParsing;if($r.StatusCode -eq 200){exit 0}}catch{};exit 1"
if not errorlevel 1 (
  echo Another FixPilot server is already using port 5007.
  echo Close its Diagnostic Hub or Python window, then run this file again.
  pause
  exit /b 1
)

start "" powershell.exe -NoProfile -WindowStyle Hidden -Command "$deadline=(Get-Date).AddMinutes(2); while((Get-Date) -lt $deadline){try{$r=Invoke-WebRequest 'http://127.0.0.1:5007/health' -TimeoutSec 2; if($r.StatusCode -eq 200){Start-Process 'http://127.0.0.1:5007'; exit}}catch{}; Start-Sleep -Seconds 1}"
echo Starting the diagnostic service. Keep this window open while using the app.
python backend\main.py
pause
