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

---

## 🌐 Wersja Web - multi_kostka.html

**Aktualnie dostępna wersja webowa z pełną funkcjonalnością desktop:**
- ✅ **3D rendering** w przeglądarce (HTML5 Canvas)
- ✅ **3 równoczesne gry** z przełączaniem myszą
- ✅ **Zaawansowane AI** z algorytmem Minimax + Alpha-Beta Pruning
- ✅ **Obsługa myszy** - klik w gry tła przenosi na pierwszy plan
- ✅ **49 linii wygrywających** w przestrzeni 3D
- ✅ **Strategiczne myślenie AI** - 2-3 ruchy naprzód

---

## 🚀 Plan Rozwoju / Roadmap

### 📱 **KIERUNEK 1: Progressive Web App (PWA) + Mobile**
*Priorytet: ⭐⭐⭐ (Łatwy start - 1-2 godziny)*

**Co to oznacza:**
- 📲 **Instalowalna aplikacja** na telefonie (jak natywna app)
- 🔄 **Działa offline** dzięki Service Worker
- 👆 **Touch controls** zamiast myszy
- 📐 **Responsive design** dla różnych ekranów
- 🏠 **"Add to Home Screen"** - ikona na pulpicie

**Potrzebne zmiany:**
```html
<!-- Podstawowe meta tagi dla mobile -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="manifest" href="manifest.json">

<!-- Service Worker dla cache -->
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
</script>

<!-- Touch events zamiast mouse -->
canvas.addEventListener('touchstart', handleTouch);
canvas.addEventListener('touchmove', handleTouch);
```

**Deploy na Render.com:**
- ☁️ **Static Site** (darmowy hosting)
- 🔗 **Custom domain** opcjonalnie  
- 🔒 **HTTPS** automatycznie
- 🌍 **Globalny dostęp** z telefonu

---

### 🌐 **KIERUNEK 2: Multiplayer Online**
*Priorytet: ⭐⭐ (Średni projekt - 3-5 dni)*

**Wizja systemu:**
```
┌─────────────────────────────────────┐
│  GLOBAL GAME STATE (3 kostki)      │
│  ┌─────┐  ┌─────┐  ┌─────┐        │
│  │Game1│  │Game2│  │Game3│         │
│  │H+AI │  │AI+AI│  │H+H+A│         │
│  └─────┘  └─────┘  └─────┘        │
└─────────────────────────────────────┘
    ↕️ WebSocket sync ↕️
┌─────────────────────────────────────┐
│  PLAYER PANEL (klif123)            │
│  Score: 1240  Rank: #15            │
│  ┌─────┐  ┌─────┐  ┌─────┐        │
│  │  ●  │  │     │  │  ●  │        │ (● = aktywny)
│  └─────┘  └─────┘  └─────┘        │
└─────────────────────────────────────┘
```

**Mechanika gry:**
- 🎮 **3 kostki zawsze aktywne** - AI gra non-stop w tle
- 👤 **Gracz loguje się** → dostaje swój panel z 3 grami  
- ⏱️ **30 sekund na ruch** - timer + auto-skip
- 🌍 **Globalna pula graczy** - każdy human może wejść w dowolną kostkę
- 🤝 **Hybrydowe mecze:** Human vs AI lub Human vs Human vs AI
- 🏆 **System punktowy** + ranking globalny

**Architektura techniczna:**
- **Backend:** Node.js + Express + Socket.IO (Render.com)
- **Frontend:** Obecny `multi_kostka.html` + WebSocket API
- **Baza danych:** PostgreSQL (darmowa na Render) dla kont/statystyk
- **Real-time:** Socket.IO dla synchronizacji gier między graczami

**Funkcje społecznościowe:**
- 👥 **Lobby z listą aktywnych gier**
- 💬 **Chat w grach** (opcjonalny)
- 🏅 **Achievements/osiągnięcia**
- 📊 **Szczegółowe statystyki**

---

### 🎯 **Rekomendacja implementacji:**

**FAZA 1 (Start):** 📱 PWA + Mobile + Render Deploy
- ✅ **Szybki efekt** - gra na telefonie w weekend
- ✅ **Nauka technologii** PWA/Service Workers  
- ✅ **Test hostingu** na Render.com

**FAZA 2 (Przyszłość):** 🌐 Multiplayer Online
- ✅ **Zaawansowany projekt** na dłuższy czas
- ✅ **Uczenie się** WebSocket/backend development
- ✅ **Skalowalna architektura** dla wielu graczy

---

**Pytania do rozważenia:**
- 🤔 Zacząć od jakiej fazy?
- 🎨 Jakieś dodatkowe funkcje graficzne?
- 🏆 System rankingowy - jak skomplikowany?
- 💰 Monetyzacja w przyszłości? (reklamy/premium features)