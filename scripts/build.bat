@echo off
title NexusSave — Build System
echo ============================================
echo   NexusSave Build System
echo ============================================
echo.

cd /d "%~dp0.."

echo [1/3] Gerando background do desktop...
python scripts\generate_bg.py
echo.

echo [2/3] Compilando NexusSave (Web)...
.venv\Scripts\pyinstaller config\nexussave.spec --clean -y
echo.

echo [3/3] Compilando NexusTube Downloader (Desktop)...
.venv\Scripts\pyinstaller config\nexustube_downloader.spec --clean -y
echo.

echo ============================================
echo   Build concluido! Verifique a pasta dist/
echo ============================================
pause
