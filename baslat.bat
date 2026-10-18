@echo off
chcp 65001 >nul
title Fırat Öğrenci Asistanı

echo ===================================================
echo     Fırat Üniversitesi Öğrenci Asistanı
echo ===================================================
echo.

cd /d "%~dp0backend"
if not exist "venv\Scripts\activate.bat" (
  echo [HATA] venv klasoru bulunamadi!
  echo Lutfen backend klasorunde sanal ortamin kurulu oldugundan emin olun.
  pause
  exit /b
)

echo [*] Sanal ortam aktif ediliyor...
call venv\Scripts\activate.bat

echo [*] Tarayici baslatiliyor (http://localhost:8000)...
start "" cmd /c "timeout /t 3 >nul & start http://localhost:8000"

echo [*] Sunucu baslatiliyor (Uvicorn)...
echo [*] Kapatmak icin bu pencerede CTRL+C tuslarina basin.
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
