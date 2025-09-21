@echo off
title 🎯 MULTI-GAMES - 3 Gry w Jednym Oknie
echo.
echo =====================================================
echo 🎯 MULTI-GAMES: 3 GRY W JEDNYM OKNIE
echo =====================================================
echo.
echo 🎮 REWOLUCYJNA FUNKCJA:
echo    - JEDNO OKNO pygame z 3 kostkami 3D
echo    - 1 gra AKTYWNA (duża, klikalna, na dole)  
echo    - 2 gry w TLE (małe, obserwowalne, u góry)
echo    - Cyfry 1,2 zamieniają aktywną z wybraną z tła
echo    - AI co 10 sekund w każdej grze równolegle
echo    - Human vs AI we wszystkich 3 grach
echo.
echo 🔄 SYSTEM SWAP:
echo    Stan początkowy: A(tło-lewa), B(tło-prawa), C(aktywna-przód)
echo    Naciśnij 1: A(aktywna-przód), C(tło-lewa), B(tło-prawa)
echo    Naciśnij 2: A(tło-lewa), B(aktywna-przód), C(tło-prawa)
echo.
echo ⌨️  STEROWANIE:
echo    🔲 CYFRA 1 - zamień aktywną z lewą grą z tła
echo    🔲 CYFRA 2 - zamień aktywną z prawą grą z tła
echo    🔲 LPM - graj w aktywnej grze (duża na dole)
echo    🔲 PPM - obracaj kostką w aktywnej grze
echo    🔲 ESC - wyjście
echo.
echo 🎯 GAMEPLAY:
echo    - Grasz TYLKO w aktywnej grze (duża na dole)
echo    - WIDZISZ postęp w grach w tle (małe u góry)
echo    - PRZEŁĄCZASZ się cyframi gdy chcesz
echo    - AI działa niezależnie w każdej grze
echo.
echo ⏰ Uruchamianie Multi-Games...
echo =====================================================
timeout /t 3 >nul

python main.py --multi-games

echo.
echo 🎮 Multi-Games zakończony. Naciśnij dowolny klawisz aby wyjść...
pause >nul