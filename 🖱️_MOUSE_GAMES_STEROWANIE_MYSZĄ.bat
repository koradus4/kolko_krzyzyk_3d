@echo off
title 🖱️ MOUSE GAMES - Sterowanie tylko myszą (PEŁNY EKRAN)
echo.
echo =====================================================
echo 🖱️ MOUSE GAMES: 3 GRY - STEROWANIE TYLKO MYSZĄ
echo =====================================================
echo.
echo 🖥️ PEŁNY EKRAN NA STARCIE!
echo    - Automatyczny pełny ekran dla najlepszego doświadczenia
echo    - F11 - przełącz pełny ekran/okno
echo    - ESC - wyjście z gry
echo    - Większe gry, lepsza widoczność
echo.
echo 🖱️ INTUICYJNA OBSŁUGA:
echo    - KLIKNIJ w grę w tle -> aktywuje ją na pierwszym planie
echo    - KLIKNIJ w aktywnej grze -> wykonasz ruch
echo    - JEDNA MYSZ do wszystkiego - bez klawiszy!
echo    - Żółte ramki = KLIKALNE gry w tle
echo    - Zielona ramka = AKTYWNA gra (graj tutaj)
echo.
echo 🎮 FUNKCJE:
echo    - 3 gry Human vs AI równocześnie
echo    - AI co 10 sekund w każdej grze
echo    - Płynne przełączanie między grami
echo    - Obracanie kostki prawym przyciskiem myszy
echo.
echo 🖱️ STEROWANIE:
echo    🔲 LPM w tle -> aktywuj tę grę
echo    🔲 LPM w aktywnej -> wykonaj ruch
echo    🔲 PPM -> obracaj kostką (w aktywnej grze)
echo    🔲 STRZAŁKI -> obracaj kostką (⬅️➡️⬆️⬇️)
echo    🔲 F11 -> przełącz pełny ekran/okno
echo    🔲 ESC -> wyjście (z potwierdzeniem)
echo.
echo 🎯 GAMEPLAY:
echo    - Żółte gry w tle: kliknij aby przenieść na przód
echo    - Zielona gra aktywna: kliknij pole aby zagrać
echo    - AI działa automatycznie w każdej grze
echo    - Bez kombinacji klawiszy - tylko mysz!
echo.
echo ⏰ Uruchamianie Mouse Games (PEŁNY EKRAN)...
echo =====================================================
timeout /t 3 >nul

python main.py --mouse-games

echo.
echo 🖱️ Mouse Games zakończone. Naciśnij dowolny klawisz aby wyjść...
pause >nul