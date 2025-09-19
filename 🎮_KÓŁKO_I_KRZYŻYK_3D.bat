@echo off
chcp 65001 >nul 2>&1
title 🎮 KÓŁKO I KRZYŻYK 3D
cls
color 0A

echo.
echo    ╔════════════════════════════════════════╗
echo    ║        🎮 KÓŁKO I KRZYŻYK 3D 🎮        ║
echo    ║                                        ║
echo    ║     Prawdziwa gra 3D z AI vs AI!      ║
echo    ║                                        ║
echo    ║    ✨ Uruchamianie gry... ✨           ║
echo    ╚════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Użyj systemowego Pythona - działa lepiej!
echo 🚀 Uruchamiam grę systemowym Pythonem...
echo.
echo 🎮 TRYBY GRY:
echo 👤 vs 🤖 - Tryb normalny (domyślny)
echo 🤖 vs 🤖 - Naciśnij A w grze aby włączyć AI vs AI!
echo.
echo ⌨️  KLAWISZE W GRZE:
echo A - tryb AI vs AI    P - tryb gracza    R - restart    ESC - wyjście
echo.
timeout /t 2 /nobreak >nul

python main.py

echo.
if errorlevel 1 (
    color 0C
    echo ❌ Gra zakończona z błędem!
) else (
    color 0B  
    echo ✅ Gra zakończona pomyślnie!
)
echo.
echo 👋 Dziękuję za grę!
echo.
echo Naciśnij dowolny klawisz aby zamknąć...
pause >nul