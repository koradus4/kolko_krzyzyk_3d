@echo off
title KÓŁKO I KRZYŻYK 3D - LAUNCHER
echo.
echo ========================================
echo    🎮 KÓŁKO I KRZYŻYK 3D - LAUNCHER 🎮
echo ========================================
echo.
echo 🎮 TRYBY GRY:
echo 👤 vs 🤖 - Normalny     🤖 vs 🤖 - Naciśnij A w grze
echo.
echo Uruchamianie gry...
echo.

cd /d "%~dp0"
python main.py

echo.
echo Gra zakończona. Naciśnij dowolny klawisz aby zamknąć...
pause >nul