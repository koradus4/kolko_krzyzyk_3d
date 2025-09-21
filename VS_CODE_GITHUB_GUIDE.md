# 🚀 GitHub Export z VS Code - Instrukcja użycia

## 📁 Utworzone pliki

### **🚀 `github_export.py` - Główne narzędzie eksportu**
- **Pełne zarządzanie** eksportem na GitHub
- **Interaktywne menu** z sugerowanymi tytułami commit
- **Podgląd zmian** przed wysłaniem
- **Status projektu** i podsumowanie
- **Opcje po eksporcie** (otwórz GitHub, uruchom grę)

### **⚡ `quick_github.py` - Szybki eksport**
- **Ultra-szybki** eksport w kilku sekundach
- **Minimal UI** - tylko essentials
- **Auto-tytuły** z czasem
- **Idealny do małych zmian**

### **🔧 `.vscode/launch.json` - Konfiguracja uruchamiania**
- **Gotowe konfiguracje** do uruchamiania w VS Code
- **F5 shortcuts** dla różnych trybów
- **Debug support** dla wszystkich skryptów

### **⚙️ `.vscode/tasks.json` - Zadania VS Code**
- **Ctrl+Shift+P** → "Tasks: Run Task"
- **Szybki dostęp** do wszystkich funkcji
- **Terminale w VS Code**

## 🎯 Jak używać w VS Code

### **Metoda 1: Uruchamianie skryptów (F5)**

1. **Otwórz plik `github_export.py`** w VS Code
2. **Naciśnij F5** lub Ctrl+F5
3. **Wybierz konfigurację** z listy:
   - `🚀 GitHub Export Tool` - pełne narzędzie
   - `⚡ Quick GitHub Export` - szybki eksport

### **Metoda 2: Run & Debug Panel**

1. **Kliknij ikonę "Run and Debug"** (Ctrl+Shift+D)
2. **Wybierz konfigurację** z dropdown:
   - `🚀 GitHub Export Tool`
   - `⚡ Quick GitHub Export`
   - `🎮 Uruchom grę (Mouse Games)`
   - `🎯 Uruchom grę (Multi Games)`
   - `🎬 Auto Demo (AI vs AI)`
3. **Kliknij Play** (▶️)

### **Metoda 3: Command Palette (Najszybsza)**

1. **Naciśnij Ctrl+Shift+P**
2. **Wpisz "Tasks: Run Task"**
3. **Wybierz zadanie:**
   - `🚀 GitHub Export Tool`
   - `⚡ Quick GitHub Export`
   - `🎮 Run Mouse Games`
   - `📊 Git Status`
   - `🌐 Open GitHub Repo`

### **Metoda 4: Terminal w VS Code**

1. **Naciśnij Ctrl+`** (otworzy terminal)
2. **Wpisz komendę:**
   ```bash
   python github_export.py    # Pełne narzędzie
   python quick_github.py     # Szybki eksport
   ```

## 🎮 Workflow dla różnych sytuacji

### **🔥 Szybka poprawka (30 sekund)**
```
Ctrl+Shift+P → "Tasks: Run Task" → "⚡ Quick GitHub Export"
Wpisz opis → Enter → Gotowe!
```

### **🎨 Nowa funkcja (2 minuty)**
```
F5 → "🚀 GitHub Export Tool" → Przejrzyj zmiany → 
Wybierz tytuł → Dodaj opis → Potwierdź eksport
```

### **📊 Sprawdź status przed pracą**
```
Ctrl+Shift+P → "Tasks: Run Task" → "📊 Git Status"
```

### **🎮 Przetestuj grę po zmianach**
```
F5 → "🎮 Uruchom grę (Mouse Games)" → Test → 
F5 → "⚡ Quick GitHub Export" → Wyślij
```

## 💡 Tips & Tricks

### **🔧 Skróty klawiszowe**
- **F5** - Szybkie uruchomienie z bieżącego pliku
- **Ctrl+F5** - Uruchom bez debugowania
- **Ctrl+Shift+D** - Panel Run & Debug
- **Ctrl+Shift+P** - Command Palette (najważniejszy!)
- **Ctrl+`** - Terminal

### **⚡ Superszybki workflow**
1. **Przypisz skrót** do "⚡ Quick GitHub Export":
   - File → Preferences → Keyboard Shortcuts
   - Szukaj "Tasks: Run Task"
   - Dodaj np. **Ctrl+Alt+G**
2. **Teraz**: Ctrl+Alt+G → wybierz Quick Export → 15 sekund do GitHub!

### **📊 Monitoring zmian**
- Włącz **Source Control** panel (Ctrl+Shift+G)
- Widzisz **zmiany na żywo** 
- **Kliknij plik** → zobacz diff
- **+ przycisk** → staging

### **🎯 Integracja z Git**
- VS Code **automatycznie wykrywa** zmiany Git
- **Timeline** pokazuje historię commitów
- **GitLens extension** = super moce Git w VS Code

## 🚀 Przykłady użycia

### **Scenariusz 1: Poprawka buga**
```
1. Napraw bug w kodzie
2. Ctrl+Shift+P → "⚡ Quick GitHub Export"  
3. Wpisz: "Fix: rotation bug with arrows"
4. Enter → gotowe w GitHub!
```

### **Scenariusz 2: Nowa funkcja**
```
1. Dodaj nową funkcję
2. F5 → "🚀 GitHub Export Tool"
3. Przejrzyj zmiany (pokazuje co się zmieniło)
4. Wybierz "🎮 Update: Mouse-only control improvements"
5. Dodaj opis: "Added fullscreen support and ESC confirmation"
6. Potwierdź → na GitHub + opcje post-eksport
```

### **Scenariusz 3: Sesja developerska**
```
1. Rano: Ctrl+Shift+P → "📊 Git Status" (sprawdź stan)
2. Programuj...
3. Test: F5 → "🎮 Uruchom grę" 
4. Commit: Ctrl+Alt+G → Quick Export
5. Więcej pracy...
6. Wieczorem: F5 → "🚀 GitHub Export Tool" (pełny commit)
```

## 🔧 Personalizacja

### **Dodaj własne zadania**
Edytuj `.vscode/tasks.json`:
```json
{
    "label": "🔥 My Custom Task",
    "type": "shell",
    "command": "python",
    "args": ["my_script.py"]
}
```

### **Zmień skróty klawiszowe**
- File → Preferences → Keyboard Shortcuts
- Szukaj nazwy zadania
- Dodaj własny skrót

### **Dostosuj konfiguracje debugowania**
Edytuj `.vscode/launch.json` - dodaj argumenty, zmienne środowiskowe itp.

## 🎉 Gotowe!

**Wszystko skonfigurowane i gotowe do użycia!**

### **Pierwsze kroki:**
1. **Otwórz projekt** w VS Code (File → Open Folder)
2. **Naciśnij F5** - wybierz "🚀 GitHub Export Tool"
3. **Przetestuj** szybki eksport: Ctrl+Shift+P → Quick Export
4. **Ciesz się** professional workflow! 🚀

### **W razie problemów:**
- Sprawdź czy Python jest w PATH
- Sprawdź czy Git jest skonfigurowany
- Uruchom `🔧_GIT_SETUP.bat` z folderu github-tools

**Happy coding! 💻🎮**