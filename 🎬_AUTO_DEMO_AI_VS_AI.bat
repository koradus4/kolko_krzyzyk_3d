@echo off
title 🎬 AUTO-DEMO: AI vs AI - Kolko i Krzyzyk 3D
echo.
echo =====================================================
echo 🎬 AUTO-DEMO: AI vs AI - KOLKO I KRZYZYK 3D
echo =====================================================
echo.
echo 🎯 AUTOMATYCZNA DEMONSTRACJA:
echo    - AI vs AI wlacza sie automatycznie
echo    - Ruchy co 10 sekund dla lepszej obserwacji
echo    - Pokaz strategii dwoch roznych AI
echo.
echo 🤖 AI STRATEGIE:
echo    🔴 AI AGRESYWNE (X) - atakuje pierwsza okazja
echo    🔵 AI DEFENSYWNE (O) - broni sie, potem atakuje
echo.
echo ⏰ Czekaj na rozpoczecie demo...
echo.
echo =====================================================
timeout /t 3 >nul

python main.py --auto-demo

echo.
echo 🎬 Demo zakonczone. Nacisnij dowolny klawisz aby wyjsc...
pause >nul