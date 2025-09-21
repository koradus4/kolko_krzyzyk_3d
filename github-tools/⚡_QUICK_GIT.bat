@echo off
chcp 65001 >nul
title ⚡ Quick Git - Szybkie operacje
color 0B

echo.
echo ====================================
echo ⚡ QUICK GIT - Szybkie operacje
echo ====================================
echo.

:QUICK_MENU
echo 🚀 SZYBKIE AKCJE:
echo.
echo 1 - ⚡ Quick Push (add + commit + push w 1 linii)
echo 2 - 📊 Quick Status (status + diff summary)
echo 3 - 🔄 Quick Sync (pull + status)
echo 4 - 💾 Quick Commit (tylko commit z tytułem)
echo 5 - 🏠 Powrót do głównego managera
echo 6 - ❌ Wyjście
echo.
set /p quick="Wybór: "

if "%quick%"=="1" goto QUICK_PUSH
if "%quick%"=="2" goto QUICK_STATUS
if "%quick%"=="3" goto QUICK_SYNC
if "%quick%"=="4" goto QUICK_COMMIT
if "%quick%"=="5" goto MAIN_MANAGER
if "%quick%"=="6" goto EXIT

echo ❌ Nieprawidłowy wybór!
goto QUICK_MENU

:QUICK_PUSH
echo.
echo ⚡ QUICK PUSH - wszystko w jednej linii
echo =====================================
echo.
set /p quick_msg="💬 Wiadomość commit (np: 'Update features'): "

if "%quick_msg%"=="" (
    set quick_msg=Quick update
)

echo.
echo ⚡ Wykonuję: add + commit + push...
git add .
git commit -m "%quick_msg%"
git push origin main

if %errorlevel%==0 (
    echo.
    echo 🎉 SUKCES! Wszystko wysłane na GitHub!
    echo 🌐 https://github.com/koradus4/tic-tac-toe-3d
) else (
    echo ❌ Wystąpił błąd podczas operacji!
)

pause
goto QUICK_MENU

:QUICK_STATUS
echo.
echo 📊 QUICK STATUS - szybki przegląd
echo =================================
echo.
echo 📁 Status plików:
git status --short
echo.
echo 📊 Podsumowanie zmian:
git diff --stat
echo.
echo 🌿 Aktualny branch:
git branch --show-current
echo.
pause
goto QUICK_MENU

:QUICK_SYNC
echo.
echo 🔄 QUICK SYNC - synchronizacja z GitHub
echo =======================================
echo.
echo 📥 Pobieranie zmian z GitHub...
git pull origin main
echo.
echo 📊 Status po synchronizacji:
git status
echo.
pause
goto QUICK_MENU

:QUICK_COMMIT
echo.
echo 💾 QUICK COMMIT - szybki commit
echo ===============================
echo.
echo 📁 Pliki w staging:
git status --cached
echo.
set /p commit_msg="💬 Tytuł commit: "

if "%commit_msg%"=="" (
    echo ❌ Tytuł commit jest wymagany!
    pause
    goto QUICK_MENU
)

git commit -m "%commit_msg%"

if %errorlevel%==0 (
    echo ✅ Commit utworzony!
    echo 💡 Użyj opcji 3 żeby wypchnąć na GitHub
) else (
    echo ❌ Błąd podczas commit!
)

pause
goto QUICK_MENU

:MAIN_MANAGER
echo.
echo 🔄 Uruchamianie głównego GitHub Managera...
start "" "🚀_GITHUB_MANAGER.bat"
goto EXIT

:EXIT
echo.
echo 👋 Do zobaczenia!
timeout /t 1 >nul
exit