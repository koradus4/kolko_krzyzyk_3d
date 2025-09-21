@echo off
chcp 65001 >nul
title 🛠️ GitHub Tools Suite - Kompletne narzędzia Git/GitHub
color 0C

echo.
echo ============================================================
echo 🛠️ GITHUB TOOLS SUITE - Zarządzanie projektem
echo ============================================================
echo.
echo 📁 Projekt: Kółko i Krzyżyk 3D - Multi-Game Mouse Edition
echo 🌐 Repository: https://github.com/koradus4/tic-tac-toe-3d
echo 📍 Lokalizacja: %cd%
echo.
echo ============================================================

:MAIN_MENU
echo.
echo 🎯 WYBIERZ NARZĘDZIE:
echo.
echo 1️⃣  - 🚀 GITHUB MANAGER (pełne zarządzanie)
echo 2️⃣  - ⚡ QUICK GIT (szybkie operacje)
echo 3️⃣  - 💾 AUTO BACKUP (kopie zapasowe)
echo 4️⃣  - 📊 PROJECT STATUS (status projektu)
echo 5️⃣  - 🔧 GIT CONFIG (konfiguracja Git)
echo 6️⃣  - 📁 OPEN REPO (otwórz repozytorium w przeglądarce)
echo 7️⃣  - 📋 HELP (pomoc i dokumentacja)
echo 8️⃣  - ❌ WYJŚCIE
echo.
set /p main_choice="🎯 Wybór (1-8): "

if "%main_choice%"=="1" goto GITHUB_MANAGER
if "%main_choice%"=="2" goto QUICK_GIT
if "%main_choice%"=="3" goto AUTO_BACKUP
if "%main_choice%"=="4" goto PROJECT_STATUS
if "%main_choice%"=="5" goto GIT_CONFIG
if "%main_choice%"=="6" goto OPEN_REPO
if "%main_choice%"=="7" goto HELP
if "%main_choice%"=="8" goto EXIT

echo ❌ Nieprawidłowy wybór!
goto MAIN_MENU

:GITHUB_MANAGER
echo.
echo 🚀 Uruchamianie GitHub Manager...
start "" "🚀_GITHUB_MANAGER.bat"
goto MAIN_MENU

:QUICK_GIT
echo.
echo ⚡ Uruchamianie Quick Git...
start "" "⚡_QUICK_GIT.bat"
goto MAIN_MENU

:AUTO_BACKUP
echo.
echo 💾 Uruchamianie Auto Backup...
start "" "💾_AUTO_BACKUP.bat"
goto MAIN_MENU

:PROJECT_STATUS
echo.
echo ============================================================
echo 📊 STATUS PROJEKTU
echo ============================================================
echo.
echo 📁 Lokalizacja projektu:
cd
echo.
echo 🌿 Aktualny branch i commit:
git log -1 --oneline
echo.
echo 📊 Status plików:
git status --short
echo.
echo 📈 Statystyki:
echo 📄 Pliki Python:
dir *.py /B | find /c "."
echo 🦇 Pliki BAT:
dir *.bat /B | find /c "."
echo 📝 Pliki dokumentacji:
dir *.md /B | find /c "."
echo.
echo 🔗 Remote repository:
git remote get-url origin
echo.
echo 📅 Ostatnia aktywność:
git log -1 --pretty=format:"Data: %%cd%%nAutor: %%an%%nWiadomość: %%s" --date=local
echo.
echo.
pause
goto MAIN_MENU

:GIT_CONFIG
echo.
echo ============================================================
echo 🔧 KONFIGURACJA GIT
echo ============================================================
echo.
echo 📋 Aktualna konfiguracja:
git config --list | findstr user
echo.
echo 🎯 OPCJE:
echo   1 - Ustaw nazwę użytkownika
echo   2 - Ustaw email
echo   3 - Pokaż całą konfigurację
echo   4 - Powrót do menu
echo.
set /p config_choice="Wybór: "

if "%config_choice%"=="1" (
    echo.
    set /p username="👤 Nowa nazwa użytkownika: "
    git config --global user.name "%username%"
    echo ✅ Nazwa użytkownika ustawiona: %username%
) else if "%config_choice%"=="2" (
    echo.
    set /p useremail="📧 Nowy email: "
    git config --global user.email "%useremail%"
    echo ✅ Email ustawiony: %useremail%
) else if "%config_choice%"=="3" (
    echo.
    echo 📋 Pełna konfiguracja Git:
    git config --list
) else if "%config_choice%"=="4" (
    goto MAIN_MENU
) else (
    echo ❌ Nieprawidłowy wybór!
)

pause
goto MAIN_MENU

:OPEN_REPO
echo.
echo 🌐 Otwieranie repozytorium GitHub w przeglądarce...
start "" https://github.com/koradus4/tic-tac-toe-3d
echo ✅ Repozytorium otwarte w przeglądarce!
timeout /t 2 >nul
goto MAIN_MENU

:HELP
echo.
echo ============================================================
echo 📋 POMOC I DOKUMENTACJA
echo ============================================================
echo.
echo 🛠️ DOSTĘPNE NARZĘDZIA:
echo.
echo 🚀 GITHUB MANAGER:
echo    - Pełne zarządzanie Git/GitHub
echo    - Przegląd różnic, commit, push
echo    - Zarządzanie gałęziami
echo    - Historia commitów
echo.
echo ⚡ QUICK GIT:
echo    - Szybkie operacje w jednej linii
echo    - Quick push (add+commit+push)
echo    - Szybki status i synchronizacja
echo.
echo 💾 AUTO BACKUP:
echo    - Automatyczne kopie zapasowe
echo    - GitHub backup z datą
echo    - Lokalne kopie projektu
echo    - Pełny backup (GitHub+lokalny)
echo.
echo 🎯 PODSTAWOWE KOMENDY GIT:
echo    git status       - sprawdź status
echo    git add .        - dodaj wszystkie pliki  
echo    git commit -m    - utwórz commit
echo    git push         - wyślij na GitHub
echo    git pull         - pobierz zmiany
echo    git log          - historia commitów
echo.
echo 🌐 REPOZYTORIUM:
echo    https://github.com/koradus4/tic-tac-toe-3d
echo.
pause
goto MAIN_MENU

:EXIT
echo.
echo ============================================================
echo ❌ WYJŚCIE Z GITHUB TOOLS SUITE
echo ============================================================
echo.
echo 👋 Dziękujemy za korzystanie z GitHub Tools!
echo 🌐 Repository: https://github.com/koradus4/tic-tac-toe-3d
echo 🛠️ Wszystkie narzędzia dostępne w folderze github-tools
echo.
echo 💡 TIP: Dodaj ten folder do ulubionych dla łatwego dostępu!
echo.
timeout /t 3 >nul
exit