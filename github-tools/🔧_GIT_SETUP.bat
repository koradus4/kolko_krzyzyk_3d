@echo off
chcp 65001 >nul
title 🔧 Git Setup - Inicjalizacja projektu
color 0D

echo.
echo ============================================================
echo 🔧 GIT SETUP - Inicjalizacja projektu na GitHub
echo ============================================================
echo.

# Sprawdź czy Git jest zainstalowany
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git nie jest zainstalowany!
    echo 💡 Pobierz Git z: https://git-scm.com/downloads
    pause
    exit
)

echo ✅ Git jest zainstalowany
git --version

# Sprawdź czy to już jest repozytorium Git
if exist ".git" (
    echo ✅ To już jest repozytorium Git
    goto CHECK_CONFIG
) else (
    echo ⚠️  To nie jest jeszcze repozytorium Git
    goto INIT_REPO
)

:INIT_REPO
echo.
echo 🔧 INICJALIZACJA REPOZYTORIUM
echo =============================
echo.
set /p init_confirm="🤔 Zainicjalizować nowe repozytorium Git? (y/n): "

if "%init_confirm%"=="y" (
    echo.
    echo 🔧 Inicjalizacja Git repository...
    git init
    
    echo ➕ Dodawanie wszystkich plików...
    git add .
    
    echo 💾 Pierwszy commit...
    git commit -m "🎮 Initial commit: Kółko i Krzyżyk 3D - Multi-Game Mouse Edition"
    
    echo ✅ Lokalne repozytorium utworzone!
    goto ADD_REMOTE
) else (
    echo ❌ Inicjalizacja anulowana
    pause
    exit
)

:ADD_REMOTE
echo.
echo 🌐 DODAWANIE REMOTE REPOSITORY
echo ==============================
echo.
echo 🔗 Dodawanie połączenia z GitHub...
git remote add origin https://github.com/koradus4/tic-tac-toe-3d.git

echo 🚀 Pierwszy push na GitHub...
git branch -M main
git push -u origin main

if %errorlevel%==0 (
    echo.
    echo 🎉 SUKCES! Projekt został połączony z GitHub!
    echo 🌐 Dostępny na: https://github.com/koradus4/tic-tac-toe-3d
) else (
    echo.
    echo ⚠️  Pierwszy push może wymagać autoryzacji
    echo 💡 Sprawdź ustawienia GitHub lub użyj GitHub Desktop
)

goto CHECK_CONFIG

:CHECK_CONFIG
echo.
echo 🔧 SPRAWDZANIE KONFIGURACJI
echo ===========================
echo.

# Sprawdź konfigurację użytkownika
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Brak nazwy użytkownika Git
    set /p git_name="👤 Podaj nazwę użytkownika Git: "
    git config --global user.name "%git_name%"
    echo ✅ Nazwa użytkownika ustawiona: %git_name%
) else (
    echo ✅ Nazwa użytkownika Git: 
    git config user.name
)

git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Brak emaila użytkownika Git
    set /p git_email="📧 Podaj email Git: "
    git config --global user.email "%git_email%"
    echo ✅ Email ustawiony: %git_email%
) else (
    echo ✅ Email użytkownika Git: 
    git config user.email
)

echo.
echo ✅ KONFIGURACJA KOMPLETNA!

:SUMMARY
echo.
echo ============================================================
echo 📊 PODSUMOWANIE SETUP
echo ============================================================
echo.
echo ✅ Git zainstalowany i skonfigurowany
echo ✅ Repository zainicjalizowane
echo ✅ Połączenie z GitHub skonfigurowane
echo ✅ Użytkownik Git skonfigurowany
echo.
echo 🌐 Repository: https://github.com/koradus4/tic-tac-toe-3d
echo 📁 Lokalna ścieżka: %cd%
echo.
echo 🎯 NASTĘPNE KROKI:
echo   1. Użyj 🛠️_GITHUB_TOOLS_SUITE.bat do zarządzania
echo   2. Lub ⚡_QUICK_GIT.bat do szybkich operacji
echo   3. Lub 🚀_GITHUB_MANAGER.bat do pełnego zarządzania
echo.
echo 📚 Dokumentacja dostępna w README.md
echo.

set /p open_tools="🚀 Otworzyć GitHub Tools Suite teraz? (y/n): "

if "%open_tools%"=="y" (
    echo.
    echo 🚀 Uruchamianie GitHub Tools Suite...
    start "" "🛠️_GITHUB_TOOLS_SUITE.bat"
)

echo.
echo 🎉 Setup zakończony! Powodzenia z projektem!
pause
exit