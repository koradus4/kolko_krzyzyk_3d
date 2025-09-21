@echo off
chcp 65001 >nul
title 🚀 GitHub Manager - Kompletne zarządzanie projektem
color 0A

echo.
echo ============================================================
echo 🚀 GITHUB MANAGER - Kompletne zarządzanie projektem
echo ============================================================
echo.
echo 📁 Projekt: Kółko i Krzyżyk 3D - Multi-Game Mouse Edition
echo 🌐 Repository: tic-tac-toe-3d
echo 👤 Owner: koradus4
echo.
echo ============================================================

:MENU
echo.
echo 🎯 WYBIERZ AKCJĘ:
echo.
echo 1️⃣  - 📊 PRZEGLĄD RÓŻNIC (git status + diff)
echo 2️⃣  - ➕ DODAJ PLIKI (git add)
echo 3️⃣  - 💾 COMMIT z tytułem (git commit)
echo 4️⃣  - 🚀 PUSH na GitHub (git push)
echo 5️⃣  - 🔄 PEŁNY WORKFLOW (add + commit + push)
echo 6️⃣  - 📜 HISTORIA COMMITÓW (git log)
echo 7️⃣  - 🌿 ZARZĄDZANIE BRANCH (przełączanie gałęzi)
echo 8️⃣  - 🔍 STATUS SZCZEGÓŁOWY (git status -v)
echo 9️⃣  - ❌ WYJŚCIE
echo.
set /p choice="🎯 Wybór (1-9): "

if "%choice%"=="1" goto DIFF
if "%choice%"=="2" goto ADD
if "%choice%"=="3" goto COMMIT
if "%choice%"=="4" goto PUSH
if "%choice%"=="5" goto FULL_WORKFLOW
if "%choice%"=="6" goto LOG
if "%choice%"=="7" goto BRANCH
if "%choice%"=="8" goto STATUS
if "%choice%"=="9" goto EXIT

echo ❌ Nieprawidłowy wybór!
goto MENU

:DIFF
echo.
echo ============================================================
echo 📊 PRZEGLĄD RÓŻNIC I ZMIAN
echo ============================================================
echo.
echo 📁 STATUS PLIKÓW:
git status
echo.
echo ============================================================
echo 📝 SZCZEGÓŁOWE RÓŻNICE:
git diff
echo.
echo ============================================================
echo 📋 PLIKI W STAGING AREA:
git diff --cached
echo.
echo ============================================================
pause
goto MENU

:ADD
echo.
echo ============================================================
echo ➕ DODAWANIE PLIKÓW DO COMMIT
echo ============================================================
echo.
echo 📁 Aktualne pliki do dodania:
git status --porcelain
echo.
echo 🎯 OPCJE:
echo   a - Dodaj WSZYSTKIE zmiany (git add .)
echo   s - Dodaj WYBRANE pliki
echo   m - Powrót do MENU
echo.
set /p add_choice="Wybór: "

if "%add_choice%"=="a" (
    echo.
    echo ➕ Dodawanie wszystkich plików...
    git add .
    echo ✅ Wszystkie pliki dodane!
) else if "%add_choice%"=="s" (
    echo.
    echo 📝 Podaj nazwę pliku do dodania:
    set /p filename="Plik: "
    git add "%filename%"
    echo ✅ Plik dodany: %filename%
) else if "%add_choice%"=="m" (
    goto MENU
) else (
    echo ❌ Nieprawidłowy wybór!
)

echo.
echo 📋 Status po dodaniu:
git status
pause
goto MENU

:COMMIT
echo.
echo ============================================================
echo 💾 TWORZENIE COMMIT Z TYTUŁEM
echo ============================================================
echo.
echo 📁 Pliki w staging area:
git status --cached
echo.
echo 📝 WPROWADŹ SZCZEGÓŁY COMMIT:
echo.
set /p commit_title="🏷️  Tytuł commit (krótki): "
echo.
echo 📋 Opis szczegółowy (opcjonalny, Enter = pomiń):
set /p commit_desc="📄 Opis: "

if "%commit_desc%"=="" (
    echo.
    echo 💾 Tworzenie commit tylko z tytułem...
    git commit -m "%commit_title%"
) else (
    echo.
    echo 💾 Tworzenie commit z tytułem i opisem...
    git commit -m "%commit_title%" -m "%commit_desc%"
)

if %errorlevel%==0 (
    echo ✅ Commit utworzony pomyślnie!
    echo.
    echo 📊 Ostatni commit:
    git log -1 --oneline
) else (
    echo ❌ Błąd podczas tworzenia commit!
)

pause
goto MENU

:PUSH
echo.
echo ============================================================
echo 🚀 WYSYŁANIE NA GITHUB
echo ============================================================
echo.
echo 📡 Sprawdzanie połączenia z remote...
git remote -v
echo.
echo 🌿 Aktualny branch:
git branch --show-current
echo.
echo 📊 Commit do wypchnięcia:
git log --oneline origin/main..HEAD
echo.
set /p push_confirm="🚀 Czy wypchnąć zmiany na GitHub? (y/n): "

if "%push_confirm%"=="y" (
    echo.
    echo 🚀 Wysyłanie na GitHub...
    git push origin main
    
    if %errorlevel%==0 (
        echo ✅ Zmiany wysłane pomyślnie na GitHub!
        echo 🌐 Sprawdź: https://github.com/koradus4/tic-tac-toe-3d
    ) else (
        echo ❌ Błąd podczas wysyłania!
        echo 💡 Sprawdź połączenie internetowe i uprawnienia
    )
) else (
    echo ❌ Push anulowany
)

pause
goto MENU

:FULL_WORKFLOW
echo.
echo ============================================================
echo 🔄 PEŁNY WORKFLOW: ADD + COMMIT + PUSH
echo ============================================================
echo.
echo 📁 Aktualne zmiany:
git status
echo.
set /p workflow_confirm="🔄 Kontynuować pełny workflow? (y/n): "

if "%workflow_confirm%"=="y" (
    echo.
    echo ➕ KROK 1/3: Dodawanie plików...
    git add .
    echo ✅ Pliki dodane!
    
    echo.
    echo 💾 KROK 2/3: Tworzenie commit...
    set /p commit_title="🏷️  Tytuł commit: "
    set /p commit_desc="📄 Opis (opcjonalny): "
    
    if "%commit_desc%"=="" (
        git commit -m "%commit_title%"
    ) else (
        git commit -m "%commit_title%" -m "%commit_desc%"
    )
    
    if %errorlevel%==0 (
        echo ✅ Commit utworzony!
        
        echo.
        echo 🚀 KROK 3/3: Wysyłanie na GitHub...
        git push origin main
        
        if %errorlevel%==0 (
            echo.
            echo 🎉 SUKCES! Pełny workflow zakończony!
            echo 🌐 Zmiany dostępne na: https://github.com/koradus4/tic-tac-toe-3d
        ) else (
            echo ❌ Błąd podczas push!
        )
    ) else (
        echo ❌ Błąd podczas commit!
    )
) else (
    echo ❌ Workflow anulowany
)

pause
goto MENU

:LOG
echo.
echo ============================================================
echo 📜 HISTORIA COMMITÓW
echo ============================================================
echo.
echo 📊 Ostatnie 10 commitów:
git log --oneline -10
echo.
echo 📈 Graf gałęzi:
git log --graph --oneline -10
echo.
echo 📋 Szczegóły ostatniego commit:
git log -1 --stat
echo.
pause
goto MENU

:BRANCH
echo.
echo ============================================================
echo 🌿 ZARZĄDZANIE GAŁĘZIAMI
echo ============================================================
echo.
echo 🌿 Dostępne gałęzie:
git branch -a
echo.
echo 🎯 Aktualna gałąź:
git branch --show-current
echo.
echo 🎯 OPCJE:
echo   n - Nowa gałąź
echo   s - Przełącz gałąź  
echo   m - Powrót do MENU
echo.
set /p branch_choice="Wybór: "

if "%branch_choice%"=="n" (
    echo.
    set /p new_branch="🆕 Nazwa nowej gałęzi: "
    git checkout -b "%new_branch%"
    echo ✅ Utworzono i przełączono na gałąź: %new_branch%
) else if "%branch_choice%"=="s" (
    echo.
    set /p switch_branch="🔄 Nazwa gałęzi do przełączenia: "
    git checkout "%switch_branch%"
    echo ✅ Przełączono na gałąź: %switch_branch%
) else if "%branch_choice%"=="m" (
    goto MENU
) else (
    echo ❌ Nieprawidłowy wybór!
)

pause
goto MENU

:STATUS
echo.
echo ============================================================
echo 🔍 STATUS SZCZEGÓŁOWY PROJEKTU
echo ============================================================
echo.
echo 📁 Lokalizacja:
cd
echo.
echo 🌿 Branch info:
git branch -vv
echo.
echo 📊 Status plików:
git status -v
echo.
echo 🔗 Remote repositories:
git remote -v
echo.
echo 📈 Różnice z remote:
git log --oneline origin/main..HEAD
echo.
pause
goto MENU

:EXIT
echo.
echo ============================================================
echo ❌ WYJŚCIE Z GITHUB MANAGER
echo ============================================================
echo.
echo 👋 Do zobaczenia! Powodzenia z projektem!
echo 🌐 Repository: https://github.com/koradus4/tic-tac-toe-3d
echo.
timeout /t 2 >nul
exit

:ERROR
echo.
echo ❌ BŁĄD: Nie znaleziono repozytorium Git!
echo 💡 Upewnij się, że jesteś w folderze z projektem Git.
echo.
pause
goto EXIT