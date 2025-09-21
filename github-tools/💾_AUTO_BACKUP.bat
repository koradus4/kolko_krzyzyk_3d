@echo off
chcp 65001 >nul
title 💾 Auto Backup - Automatyczne kopie zapasowe
color 0E

echo.
echo ================================================
echo 💾 AUTO BACKUP - Automatyczne kopie zapasowe
echo ================================================
echo.

set "PROJECT_NAME=kolkokrzyzyk3d"
set "DATE=%date:~-4%-%date:~3,2%-%date:~0,2%"
set "TIME=%time:~0,2%-%time:~3,2%"
set "TIME=%TIME: =0%"
set "BACKUP_NAME=%PROJECT_NAME%_backup_%DATE%_%TIME%"

echo 📁 Projekt: %PROJECT_NAME%
echo 📅 Data: %DATE%
echo ⏰ Czas: %TIME:~0,5%
echo 📦 Nazwa backup: %BACKUP_NAME%
echo.

:BACKUP_MENU
echo 🎯 OPCJE BACKUP:
echo.
echo 1 - 💾 GitHub Backup (commit + push z datą)
echo 2 - 📁 Lokalny Backup (kopia folderu)
echo 3 - 🔄 Pełny Backup (GitHub + lokalny)
echo 4 - 📊 Status backupów
echo 5 - ❌ Wyjście
echo.
set /p backup_choice="Wybór: "

if "%backup_choice%"=="1" goto GITHUB_BACKUP
if "%backup_choice%"=="2" goto LOCAL_BACKUP
if "%backup_choice%"=="3" goto FULL_BACKUP
if "%backup_choice%"=="4" goto BACKUP_STATUS
if "%backup_choice%"=="5" goto EXIT

echo ❌ Nieprawidłowy wybór!
goto BACKUP_MENU

:GITHUB_BACKUP
echo.
echo 💾 GITHUB BACKUP - Automatyczny commit z datą
echo =============================================
echo.
echo ➕ Dodawanie plików...
git add .

echo 💾 Tworzenie commit z datą...
git commit -m "🔄 Auto backup %DATE% %TIME:~0,5%" -m "Automatyczna kopia zapasowa projektu Kółko i Krzyżyk 3D"

echo 🚀 Wysyłanie na GitHub...
git push origin main

if %errorlevel%==0 (
    echo.
    echo ✅ GitHub backup zakończony pomyślnie!
    echo 🌐 Dostępny na: https://github.com/koradus4/tic-tac-toe-3d
) else (
    echo ❌ Błąd podczas GitHub backup!
)

pause
goto BACKUP_MENU

:LOCAL_BACKUP
echo.
echo 📁 LOKALNY BACKUP - Kopia folderu projektu
echo ==========================================
echo.

cd ..
echo 📂 Tworzenie kopii lokalnej...
xcopy "%PROJECT_NAME%" "%BACKUP_NAME%" /E /I /H /Y

if %errorlevel%==0 (
    echo ✅ Lokalny backup utworzony!
    echo 📁 Lokalizacja: ..\%BACKUP_NAME%
    
    echo.
    echo 📊 Rozmiar backup:
    dir "%BACKUP_NAME%" /s
) else (
    echo ❌ Błąd podczas tworzenia lokalnego backup!
)

cd "%PROJECT_NAME%"
pause
goto BACKUP_MENU

:FULL_BACKUP
echo.
echo 🔄 PEŁNY BACKUP - GitHub + Lokalny
echo ==================================
echo.
echo 🚀 Rozpoczynam pełny backup...

echo.
echo 📁 KROK 1/2: GitHub backup...
git add .
git commit -m "🔄 Full backup %DATE% %TIME:~0,5%" -m "Pełna kopia zapasowa - GitHub + lokalny"
git push origin main

if %errorlevel%==0 (
    echo ✅ GitHub backup OK!
    
    echo.
    echo 📂 KROK 2/2: Lokalny backup...
    cd ..
    xcopy "%PROJECT_NAME%" "%BACKUP_NAME%" /E /I /H /Y
    
    if %errorlevel%==0 (
        echo ✅ Lokalny backup OK!
        echo.
        echo 🎉 PEŁNY BACKUP ZAKOŃCZONY POMYŚLNIE!
        echo 🌐 GitHub: https://github.com/koradus4/tic-tac-toe-3d
        echo 📁 Lokalny: ..\%BACKUP_NAME%
    ) else (
        echo ❌ Błąd lokalnego backup!
    )
    
    cd "%PROJECT_NAME%"
) else (
    echo ❌ Błąd GitHub backup!
)

pause
goto BACKUP_MENU

:BACKUP_STATUS
echo.
echo 📊 STATUS BACKUPÓW
echo ==================
echo.
echo 🌐 GitHub status:
git log --oneline -5
echo.
echo 📁 Lokalne backupy:
cd ..
dir "*backup*" /B
cd "%PROJECT_NAME%"
echo.
echo 📈 Ostatnia aktywność:
git log -1 --pretty=format:"📅 Data: %%cd%%n👤 Autor: %%an%%n💬 Wiadomość: %%s" --date=local
echo.
echo.
pause
goto BACKUP_MENU

:EXIT
echo.
echo 👋 Backup zakończony!
timeout /t 2 >nul
exit