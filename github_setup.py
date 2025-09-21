#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 GitHub Repository Setup - Tworzenie repozytorium na GitHub
"""

import webbrowser
import time
import subprocess

def create_github_repo_guide():
    """Przewodnik tworzenia repozytorium GitHub"""
    print("\n" + "="*60)
    print("🔧 GITHUB REPOSITORY SETUP")
    print("="*60)
    print("📋 Przewodnik tworzenia nowego repozytorium na GitHub")
    print("="*60)
    
    print("""
🎯 KROK 1: Utwórz repozytorium na GitHub.com
==========================================

1. 🌐 Otworzę GitHub w przeglądarce...
2. 🔑 Zaloguj się do swojego konta GitHub
3. ➕ Kliknij "New repository" (zielony przycisk)
4. 📝 Ustaw parametry:
   
   Repository name: tic-tac-toe-3d
   Description: 🎮 Kółko i Krzyżyk 3D - Multi-Game Mouse Edition
   ✅ Public (zalecane)
   ❌ NIE dodawaj README.md (już masz)
   ❌ NIE dodawaj .gitignore (niepotrzebne)
   ❌ NIE dodawaj license (na razie)

5. 🚀 Kliknij "Create repository"
""")
    
    input("📝 Naciśnij Enter gdy będziesz gotowy otworzyć GitHub...")
    
    print("🌐 Otwieranie GitHub...")
    webbrowser.open("https://github.com/new")
    time.sleep(2)
    
    print("""
🎯 KROK 2: Skopiuj dane repozytorium
==================================

Po utworzeniu repozytorium GitHub pokaże Ci stronę z instrukcjami.
SKOPIUJ link HTTPS do repozytorium, przykład:

https://github.com/TWOJA_NAZWA/tic-tac-toe-3d.git

""")
    
    repo_url = input("📋 Wklej tutaj URL repozytorium (HTTPS): ").strip()
    
    if not repo_url:
        print("❌ Brak URL repozytorium!")
        return False
    
    if not repo_url.startswith("https://github.com/"):
        print("❌ URL powinien zaczynać się od https://github.com/")
        return False
    
    print(f"✅ URL repozytorium: {repo_url}")
    
    print("""
🎯 KROK 3: Konfiguracja lokalnego Git
===================================
""")
    
    # Sprawdź konfigurację Git
    try:
        result = subprocess.run("git config user.name", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git user.name: {result.stdout.strip()}")
        else:
            name = input("👤 Podaj swoją nazwę dla Git: ")
            subprocess.run(f'git config --global user.name "{name}"', shell=True)
            print(f"✅ Ustawiono nazwę: {name}")
        
        result = subprocess.run("git config user.email", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git user.email: {result.stdout.strip()}")
        else:
            email = input("📧 Podaj swój email dla Git: ")
            subprocess.run(f'git config --global user.email "{email}"', shell=True)
            print(f"✅ Ustawiono email: {email}")
            
    except Exception as e:
        print(f"⚠️ Błąd konfiguracji Git: {e}")
    
    print("""
🎯 KROK 4: Połączenie z GitHub
=============================
""")
    
    # Sprawdź czy już jest remote
    try:
        result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
        if "origin" in result.stdout:
            print("📡 Remote 'origin' już istnieje:")
            print(result.stdout)
            
            update = input("🔄 Zaktualizować URL remote na nowy? (y/n): ").lower()
            if update in ['y', 'yes', 'tak']:
                subprocess.run(f'git remote set-url origin "{repo_url}"', shell=True)
                print("✅ URL remote zaktualizowany!")
        else:
            print("➕ Dodawanie remote origin...")
            subprocess.run(f'git remote add origin "{repo_url}"', shell=True)
            print("✅ Remote origin dodany!")
            
    except Exception as e:
        print(f"❌ Błąd z remote: {e}")
        return False
    
    print("""
🎯 KROK 5: Pierwszy push na GitHub
=================================
""")
    
    try:
        print("🚀 Wysyłanie na GitHub...")
        result = subprocess.run("git push -u origin main", shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("🎉 SUKCES! Projekt wysłany na GitHub!")
            print(f"🌐 Dostępny na: {repo_url.replace('.git', '')}")
            
            # Otwórz repozytorium
            open_repo = input("🌐 Otworzyć repozytorium w przeglądarce? (y/n): ").lower()
            if open_repo in ['y', 'yes', 'tak']:
                webbrowser.open(repo_url.replace('.git', ''))
            
            return True
        else:
            print("❌ Błąd podczas push:")
            print(result.stderr)
            print("""
💡 MOŻLIWE ROZWIĄZANIA:
- Sprawdź czy jesteś zalogowany do GitHub
- Może potrzebujesz Personal Access Token
- Spróbuj użyć GitHub Desktop
- Lub skonfiguruj SSH keys
""")
            return False
            
    except Exception as e:
        print(f"❌ Błąd push: {e}")
        return False

def main():
    """Główna funkcja"""
    try:
        success = create_github_repo_guide()
        
        if success:
            print("""
🎉 SETUP ZAKOŃCZONY SUKCESEM!
============================

✅ Repozytorium GitHub utworzone
✅ Projekt wysłany na GitHub  
✅ Git skonfigurowany

🚀 NASTĘPNE KROKI:
- Użyj 'python github_export.py' do przyszłych commitów
- Lub 'python quick_github.py' do szybkich aktualizacji
- Wszystko gotowe do pracy!

""")
        else:
            print("""
⚠️ Setup nie został ukończony
============================

💡 Możesz:
- Spróbować ponownie później
- Użyć GitHub Desktop (prostsze)
- Skonfigurować SSH keys
- Poprosić o pomoc

""")
    
    except KeyboardInterrupt:
        print("\n❌ Przerwano przez użytkownika")
    except Exception as e:
        print(f"❌ Błąd: {e}")
    finally:
        input("📝 Naciśnij Enter aby zamknąć...")

if __name__ == "__main__":
    main()