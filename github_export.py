#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 GitHub Export Tool - Eksport projektu na GitHub z VS Code
Autor: GitHub Copilot
Data: 21 września 2025
"""

import os
import subprocess
import sys
from datetime import datetime
import json

def print_header():
    """Wyświetl nagłówek narzędzia"""
    print("\n" + "="*60)
    print("🚀 GITHUB EXPORT TOOL - Eksport z VS Code")
    print("="*60)
    print(f"📁 Projekt: Kółko i Krzyżyk 3D - Multi-Game Mouse Edition")
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💻 Lokalizacja: {os.getcwd()}")
    print("="*60)

def run_git_command(command, description=""):
    """Uruchom komendę git i zwróć wynik"""
    try:
        if description:
            print(f"🔄 {description}...")
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            if description:
                print(f"✅ {description} - SUKCES")
            return True, result.stdout.strip()
        else:
            print(f"❌ Błąd: {result.stderr.strip()}")
            return False, result.stderr.strip()
    except Exception as e:
        print(f"❌ Wyjątek: {str(e)}")
        return False, str(e)

def check_git_status():
    """Sprawdź status Git repository"""
    print("\n📊 SPRAWDZANIE STATUS PROJEKTU")
    print("-" * 40)
    
    # Sprawdź czy to repozytorium Git
    if not os.path.exists('.git'):
        print("⚠️  To nie jest repozytorium Git!")
        return False
    
    # Status plików
    success, output = run_git_command("git status --porcelain", "Sprawdzanie zmian")
    if success:
        if output:
            print("📝 Znalezione zmiany:")
            for line in output.split('\n'):
                if line.strip():
                    print(f"   {line}")
        else:
            print("✅ Brak zmian do commitowania")
    
    # Aktualny branch
    success, branch = run_git_command("git branch --show-current", "Sprawdzanie gałęzi")
    if success:
        print(f"🌿 Aktualny branch: {branch}")
    
    # Ostatni commit
    success, last_commit = run_git_command("git log -1 --oneline", "Sprawdzanie ostatniego commit")
    if success:
        print(f"📝 Ostatni commit: {last_commit}")
    
    return True

def get_commit_details():
    """Pobierz szczegóły commit od użytkownika"""
    print("\n💾 SZCZEGÓŁY COMMIT")
    print("-" * 40)
    
    # Sugerowane tytuły na podstawie kontekstu
    suggested_titles = [
        "🎮 Update: Mouse-only control system improvements",
        "🔧 Fix: Cube rotation and ESC confirmation",
        "🖥️ Add: Fullscreen mode with F11 toggle", 
        "📊 Update: Layout improvements for better visibility",
        "🛠️ Add: Complete GitHub tools suite",
        "📚 Update: Documentation and README",
        "🎯 Custom: Własny tytuł..."
    ]
    
    print("🎯 SUGEROWANE TYTUŁY:")
    for i, title in enumerate(suggested_titles, 1):
        print(f"   {i}. {title}")
    
    while True:
        try:
            choice = input(f"\n🏷️  Wybierz tytuł (1-{len(suggested_titles)}) lub Enter dla własnego: ")
            
            if not choice:
                title = input("💬 Wprowadź własny tytuł commit: ")
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(suggested_titles):
                selected = suggested_titles[int(choice) - 1]
                if "Custom:" in selected:
                    title = input("💬 Wprowadź własny tytuł commit: ")
                else:
                    title = selected
                break
            else:
                print("❌ Nieprawidłowy wybór!")
        except KeyboardInterrupt:
            print("\n❌ Przerwano przez użytkownika")
            return None, None
    
    # Opcjonalny opis
    description = input("📄 Opis szczegółowy (opcjonalny, Enter = pomiń): ")
    
    return title, description if description else None

def show_diff_summary():
    """Pokaż podsumowanie zmian"""
    print("\n📊 PODSUMOWANIE ZMIAN")
    print("-" * 40)
    
    # Pokaż krótkie diff
    success, diff_stat = run_git_command("git diff --stat", "Pobieranie statystyk zmian")
    if success and diff_stat:
        print("📈 Statystyki zmian:")
        for line in diff_stat.split('\n'):
            if line.strip():
                print(f"   {line}")
    
    # Pokaż staged files
    success, staged = run_git_command("git diff --cached --name-only", "Sprawdzanie staged files")
    if success and staged:
        print("📋 Pliki w staging area:")
        for file in staged.split('\n'):
            if file.strip():
                print(f"   ✓ {file}")

def export_to_github():
    """Główna funkcja eksportu na GitHub"""
    print_header()
    
    # Sprawdź status
    if not check_git_status():
        print("❌ Nie można kontynuować bez repozytorium Git")
        return False
    
    # Pokaż zmiany
    show_diff_summary()
    
    # Potwierdź czy kontynuować
    print("\n🤔 POTWIERDZENIE EKSPORTU")
    print("-" * 40)
    proceed = input("🚀 Czy kontynuować eksport na GitHub? (y/n): ").lower()
    
    if proceed not in ['y', 'yes', 'tak', 't']:
        print("❌ Eksport anulowany przez użytkownika")
        return False
    
    # Dodaj wszystkie pliki
    success, _ = run_git_command("git add .", "Dodawanie wszystkich plików")
    if not success:
        return False
    
    # Pobierz szczegóły commit
    title, description = get_commit_details()
    if not title:
        return False
    
    # Utwórz commit
    if description:
        commit_cmd = f'git commit -m "{title}" -m "{description}"'
    else:
        commit_cmd = f'git commit -m "{title}"'
    
    success, _ = run_git_command(commit_cmd, "Tworzenie commit")
    if not success:
        return False
    
    # Push na GitHub
    success, _ = run_git_command("git push origin main", "Wysyłanie na GitHub")
    if not success:
        print("⚠️  Push może wymagać autoryzacji GitHub")
        return False
    
    # Sukces!
    print("\n🎉 EKSPORT ZAKOŃCZONY SUKCESEM!")
    print("-" * 40)
    print("✅ Wszystkie pliki zostały wysłane na GitHub")
    print("🌐 Repository: https://github.com/koradus4/tic-tac-toe-3d")
    print("📝 Commit:", title)
    if description:
        print("📄 Opis:", description)
    
    return True

def show_post_export_options():
    """Pokaż opcje po eksporcie"""
    print("\n🎯 OPCJE PO EKSPORCIE:")
    print("1. 🌐 Otwórz repozytorium GitHub w przeglądarce")
    print("2. 📊 Pokaż status projektu")
    print("3. 🎮 Uruchom grę")
    print("4. ❌ Zakończ")
    
    choice = input("\nWybór (1-4): ")
    
    if choice == "1":
        import webbrowser
        webbrowser.open("https://github.com/koradus4/tic-tac-toe-3d")
        print("🌐 Otwarto GitHub w przeglądarce")
    elif choice == "2":
        run_git_command("git log --oneline -5", "Ostatnie 5 commitów")
        run_git_command("git status", "Status projektu")
    elif choice == "3":
        print("🎮 Uruchamianie gry...")
        os.system("python main.py --mouse-games")
    elif choice == "4":
        print("👋 Do zobaczenia!")
    else:
        print("❌ Nieprawidłowy wybór")

def main():
    """Główna funkcja programu"""
    try:
        # Sprawdź czy jesteśmy w odpowiednim folderze
        if not os.path.exists("main.py"):
            print("❌ Błąd: Nie znaleziono main.py")
            print("💡 Upewnij się, że uruchamiasz skrypt z folderu projektu")
            return
        
        # Wykonaj eksport
        success = export_to_github()
        
        if success:
            show_post_export_options()
        else:
            print("\n❌ Eksport nie został ukończony")
            print("💡 Sprawdź błędy powyżej i spróbuj ponownie")
    
    except KeyboardInterrupt:
        print("\n\n❌ Przerwano przez użytkownika (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Nieoczekiwany błąd: {str(e)}")
        print("💡 Sprawdź czy Git jest zainstalowany i skonfigurowany")
    finally:
        input("\n📝 Naciśnij Enter aby zamknąć...")

if __name__ == "__main__":
    main()