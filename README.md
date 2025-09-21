# 🎮 Kółko i Krzyżyk 3D - Pseudo 3D z AI vs AI

Zaawansowana gra w kółko i krzyżyk na kostce 3x3x3 w przestrzeni 3D z wykorzystaniem pygame.

## ✨ Funkcje

### 🎯 **Tryby gry:**
- **👤 vs 🤖 Human vs AI** - Klasyczna rozgrywka przeciwko AI
- **🤖 vs 🤖 AI vs AI** - Obserwuj walkę dwóch różnych strategii AI
- **🎬 Auto-Demo** - Automatyczna demonstracja AI vs AI z 10-sekundowymi opóźnieniami
- **🚀 Multi-Instance** - 3 gry jednocześnie z przełączaniem klawiszy 1,2,3

### 🎨 **Grafika:**
- Pseudo-3D rendering z perspektywą
- Kolorowe kwadraty zamiast X/O (🟧 Human, 🟦 AI)
- Gradientowe tła i efekty świetlne
- Płynne obracanie kostki 3D
- Interaktywne podświetlanie pól

### 🤖 **Inteligentne AI:**
- **AI Agresywne** (🔴) - atakuje pierwszą okazją
- **AI Defensywne** (🔵) - broni się, potem atakuje
- Strategiczne myślenie: centrum → narożniki → krawędzie

## 🚀 Launchers

### 1. **🎮 Podstawowy launcher**
```
🎮_KÓŁKO_I_KRZYŻYK_3D.bat
```

### 2. **🎬 Auto-Demo AI vs AI**
```
🎬_AUTO_DEMO_AI_VS_AI.bat
```

### 3. **🎯 Multi-Games (3 gry w 1 oknie)**
```
🎯_MULTI_GAMES_1_OKNO.bat
```
- **JEDNO OKNO** z 3 grami wewnątrz
- **1 gra aktywna** (duża, na dole) - w niej grasz
- **2 gry w tle** (małe, u góry) - widzisz postęp
- **Cyfry 1, 2** zamieniają aktywną grę z wybraną z tła
- **AI co 10 sekund** w każdej grze

### 4. **🖱️ Mouse Games (Sterowanie tylko myszą + PEŁNY EKRAN)**
```
🖱️_MOUSE_GAMES_STEROWANIE_MYSZĄ.bat
```
- **🖥️ PEŁNY EKRAN NA STARCIE** - najlepsze doświadczenie
- **TYLKO MYSZ** - zero kombinacji klawiszy!
- **F11** - przełącz pełny ekran/okno
- **KLIKNIJ w grę w tle** -> aktywuje ją na pierwszym planie
- **KLIKNIJ w aktywnej grze** -> wykonasz ruch
- **Żółte ramki** = gry klikalne w tle
- **Zielona ramka** = aktywna gra
- **Intuicyjne przełączanie** jednym kliknięciem

## ⌨️ Sterowanie

### **Podstawowe:**
- **LPM** - wykonaj ruch (kliknij pole)
- **PPM** - przeciągnij aby obracać kostką
- **Strzałki** - obracaj kostką klawiaturą
- **ESC/Q** - wyjście

### **Tryby:**
- **A** - włącz AI vs AI
- **P** - powrót do trybu gracza
- **R** - restart gry

### **Multi-Games + Mouse-Only:**
- **🖱️ LPM w tle** - aktywuj tę grę (swap)
- **🖱️ LPM w aktywnej** - wykonaj ruch
- **🖱️ PPM** - obracaj kostką (tylko w aktywnej grze)
- **⌨️ STRZAŁKI** - obracaj kostką (⬅️➡️⬆️⬇️)
- **F11** - przełącz pełny ekran/okno
- **ESC** - wyjście (z potwierdzeniem bezpieczeństwa)
- **Żółte ramki** = gry klikalne w tle
- **Zielona ramka** = aktywna gra

### **Multi-Games:**
- **1, 2** - przełącz aktywną grę (swap z tłem)

## 🎯 Cel gry

Ułóż **3 kwadraty w linii** w przestrzeni 3D:
- Poziomo, pionowo, ukośnie
- W dowolnej płaszczyźnie kostki 3x3x3
- Możliwe linie 3D przez centrum kostki

## 🔧 Wymagania

- Python 3.7+
- pygame-ce 2.5+
- numpy

```bash
pip install pygame-ce numpy
```

## 📱 Uruchamianie

### Najprostsze - kliknij plik .bat:
```
🖱️_MOUSE_GAMES_STEROWANIE_MYSZĄ.bat  # Mouse-only + PEŁNY EKRAN! (NAJNOWSZE)
🎯_MULTI_GAMES_1_OKNO.bat            # 3 gry w jednym oknie!
```

### Z terminala:
```bash
# Mouse-only games (pełny ekran)
python main.py --mouse-games

# Pojedyncza gra
python main.py

# Auto-demo AI vs AI
python main.py --auto-demo

# Multi-games (3 w 1 oknie)
python main.py --multi-games

# Multi-instance (3 osobne okna)
python main.py --instance=1
python main.py --instance=2  
python main.py --instance=3
```

## 🎯 Multi-Games Mode (NAJNOWSZE!)

**REWOLUCYJNA FUNKCJA!** 3 gry w jednym oknie:

### 📱 **Układ:**
```
┌─────────────────────────────────────┐
│ [Gra A-małe]     [Gra B-małe]      │
│                                     │  
│         GRA C - AKTYWNA             │
│        (duża, z przodu)             │
│                                     │
└─────────────────────────────────────┘
```

### 🔄 **System SWAP:**
1. **Stan początkowy**: A(tło-lewa), B(tło-prawa), **C(aktywna-przód)**
2. **Naciśnij 1**: **A(aktywna-przód)**, C(tło-lewa), B(tło-prawa) 
3. **Naciśnij 2**: A(tło-lewa), **B(aktywna-przód)**, C(tło-prawa)

### ✨ **Funkcje:**
- **JEDNO OKNO** pygame z 3 kostkami 3D
- **1 gra aktywna** (duża, klikalna)
- **2 gry w tle** (małe, obserwowalne)
- **Cyfry 1,2** zamieniają aktywną z wybraną z tła
- **AI co 10 sekund** w każdej grze równolegle
- **Human vs AI** we wszystkich 3 grach

### 🎮 **Gameplay:**
- Grasz **tylko w aktywnej grze** (duża na dole)
- **Widzisz postęp** w grach w tle (małe u góry)
- **Przełączasz się** cyframi gdy chcesz
- **AI działa niezależnie** w każdej grze

**Uruchom**: `🎯_MULTI_GAMES_1_OKNO.bat`

---

## 🏆 Strategia

- **Centrum (1,1,1)** - najważniejsze pole
- **Narożniki** - druga najlepsza opcja
- **Krawędzie** - uzupełniające ruchy
- **Myśl w 3D** - linie mogą przebiegać przez całą kostkę!