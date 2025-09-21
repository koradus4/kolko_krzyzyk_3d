#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Quick GitHub Export - Szybki eksport w 1 linii
"""

import os
import subprocess
from datetime import datetime

def quick_export():
    """Szybki eksport na GitHub"""
    print("⚡ QUICK GITHUB EXPORT")
    print("=" * 30)
    
    # Sprawdź czy to repo Git
    if not os.path.exists('.git'):
        print("❌ Nie ma repozytorium Git!")
        return
    
    # Pokaż status
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 Zmiany do commitowania:")
        for line in result.stdout.strip().split('\n'):
            print(f"   {line}")
    else:
        print("✅ Brak zmian")
        return
    
    # Szybki commit
    message = input("💬 Wiadomość commit (lub Enter dla auto): ")
    if not message:
        message = f"🔄 Quick update {datetime.now().strftime('%H:%M')}"
    
    # Wykonaj operacje
    print("⚡ Eksport...")
    
    commands = [
        "git add .",
        f'git commit -m "{message}"',
        "git push origin main"
    ]
    
    for cmd in commands:
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f"❌ Błąd w: {cmd}")
            return
    
    print("🎉 SUKCES! Projekt wysłany na GitHub!")
    print("🌐 https://github.com/koradus4/tic-tac-toe-3d")

if __name__ == "__main__":
    try:
        quick_export()
    except KeyboardInterrupt:
        print("\n❌ Przerwano")
    except Exception as e:
        print(f"❌ Błąd: {e}")
    finally:
        input("📝 Enter aby zamknąć...")