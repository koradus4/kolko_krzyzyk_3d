"""
🎮 KÓŁKO I KRZYŻYK 3D - PSEUDO 3D VERSION Z AI 🎮
Wizualnie wygląda jak 3D ale używa tylko Pygame!
Graj przeciwko inteligentnemu AI!
"""

import pygame
import numpy as np
import math
import random
import time
import ctypes
from ctypes import wintypes

# Windows API dla bring-to-front
try:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    
    def bring_window_to_front(window_title):
        """Przenosi okno o danym tytule na pierwszy plan"""
        def enum_windows_proc(hwnd, lParam):
            title = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(hwnd, title, 256)
            if window_title in title.value:
                user32.SetForegroundWindow(hwnd)
                user32.BringWindowToTop(hwnd)
                return False  # Stop enumeration
            return True  # Continue enumeration
        
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        user32.EnumWindows(EnumWindowsProc(enum_windows_proc), 0)
        
except Exception:
    def bring_window_to_front(window_title):
        pass  # Fallback - nic nie rób na innych systemach

# Kolory - ULEPSZONE DLA LEPSZEJ WIDOCZNOŚCI
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 50, 50)  # Jaśniejszy czerwony
NIEBIESKI = (50, 150, 255)  # Jaśniejszy niebieski
ZIELONY = (50, 255, 50)  # Jaśniejszy zielony
SZARY = (128, 128, 128)
ZLOTY = (255, 220, 0)  # Jaśniejszy złoty
CIEMNY_SZARY = (32, 32, 40)  # Ciemniejsze tło
JASNY_SZARY = (220, 220, 220)
FIOLETOWY = (180, 50, 255)  # Nowy kolor
POMARANCZOWY = (255, 150, 0)  # Nowy kolor
TURKUSOWY = (0, 200, 200)  # Nowy kolor


class Kostka3D:
    """Kostka 3D renderowana w 2D z efektem perspektywy"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Plansza gry - 3x3x3
        self.plansza = np.full((3, 3, 3), ' ', dtype=str)
        self.aktualny_gracz = 'X'  # Gracz zawsze zaczyna jako X
        self.gracz_ai = 'O'  # AI gra jako O
        self.koniec_gry = False
        self.zwyciezca = None
        self.czy_ruch_ai = False  # Czy teraz kolej AI
        
        # Tryb AI vs AI
        self.tryb_ai_vs_ai = False
        self.ai1_nazwa = "AI Czerwony 🔴"
        self.ai2_nazwa = "AI Niebieski 🔵"
        self.auto_ai_vs_ai = False  # Automatyczne uruchomienie AI vs AI po starcie
        self.ai_delay = 10000  # 10 sekund opóźnienia między ruchami AI
        
        # Parametry renderowania - POWIĘKSZONE
        self.centrum_x = screen_width // 2
        self.centrum_y = screen_height // 2
        self.rozmiar_kostki = 250  # Powiększone z 150 do 250
        self.rot_x = 20  # Rotacja dla perspektywy
        self.rot_y = 30
        
        # Pozycje pól w 3D (będą konwertowane na 2D)
        self.pola_3d = []
        self.pola_2d = []  # Pozycje po konwersji
        self.highlighted_pole = None  # Podświetlone pole
        self._wygeneruj_pola()
        
        # Tryb AI vs AI
        self.tryb_ai_vs_ai = False
        self.ai1_nazwa = "AI Czerwony 🔴"
        self.ai2_nazwa = "AI Niebieski 🔵"
        self.auto_ai_vs_ai = False  # Automatyczne uruchomienie AI vs AI po starcie
        self.ai_delay = 10000  # 10 sekund opóźnienia między ruchami AI
        
        # Parametry renderowania - POWIĘKSZONE
        self.centrum_x = screen_width // 2
        self.centrum_y = screen_height // 2
        self.rozmiar_kostki = 250  # Powiększone z 150 do 250
        self.rot_x = 20  # Rotacja dla perspektywy
        self.rot_y = 30
        
        # Pozycje pól w 3D (będą konwertowane na 2D)
        self.pola_3d = []
        self.pola_2d = []  # Pozycje po konwersji
        self.highlighted_pole = None  # Podświetlone pole
        self._wygeneruj_pola()
    
    def _wygeneruj_pola(self):
        """Generuje pozycje wszystkich pól kostki"""
        self.pola_3d = []
        odstep = self.rozmiar_kostki / 3
        
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    # Pozycja 3D względem centrum kostki
                    pos_x = (x - 1) * odstep
                    pos_y = (y - 1) * odstep  
                    pos_z = (z - 1) * odstep
                    self.pola_3d.append((pos_x, pos_y, pos_z, x, y, z))
        
        self._konwertuj_3d_na_2d()
    
    def _konwertuj_3d_na_2d(self):
        """Konwertuje pozycje 3D na 2D z perspektywą"""
        self.pola_2d = []
        
        # Macierze rotacji
        cos_x = math.cos(math.radians(self.rot_x))
        sin_x = math.sin(math.radians(self.rot_x))
        cos_y = math.cos(math.radians(self.rot_y))
        sin_y = math.sin(math.radians(self.rot_y))
        
        for pos_x, pos_y, pos_z, x, y, z in self.pola_3d:
            # Rotacja Y
            temp_x = pos_x * cos_y - pos_z * sin_y
            temp_z = pos_x * sin_y + pos_z * cos_y
            
            # Rotacja X
            temp_y = pos_y * cos_x - temp_z * sin_x
            final_z = pos_y * sin_x + temp_z * cos_x
            
            # Projekcja perspektywiczna (uproszczona)
            distance = 400
            scale = distance / (distance + final_z)
            
            screen_x = int(self.centrum_x + temp_x * scale)
            screen_y = int(self.centrum_y - temp_y * scale)  # Minus bo Y w pygame jest odwrócony
            
            self.pola_2d.append((screen_x, screen_y, scale, x, y, z))
    
    def narysuj_kostke(self, screen):
        """Rysuje całą kostke na ekranie"""
        # Gradient tło dla lepszej głębi
        for y in range(screen.get_height()):
            blend = y / screen.get_height()
            color = (
                int(CIEMNY_SZARY[0] * (1 - blend) + (CIEMNY_SZARY[0] + 20) * blend),
                int(CIEMNY_SZARY[1] * (1 - blend) + (CIEMNY_SZARY[1] + 30) * blend),
                int(CIEMNY_SZARY[2] * (1 - blend) + (CIEMNY_SZARY[2] + 50) * blend)
            )
            pygame.draw.line(screen, color, (0, y), (screen.get_width(), y))
        
        # Konwertuj pozycje 3D na 2D
        self._konwertuj_3d_na_2d()
        
        # Sortuj pola według głębokości (z-buffer)
        sorted_pola = sorted(self.pola_2d, key=lambda p: p[2])  # Sortuj po scale (głębokość)
        
        # Rysuj linie kostki z świecącym efektem
        self._narysuj_linie_kostki(screen)
        
        # Rysuj wszystkie pola
        for screen_x, screen_y, scale, x, y, z in sorted_pola:
            self._narysuj_pole(screen, screen_x, screen_y, scale, x, y, z)
    
    def _narysuj_linie_kostki(self, screen):
        """Rysuje linie pokazujące strukturę kostki z efektem świecenia"""
        # Rysowanie uproszczone - kostka szkieletowa
        odstep = self.rozmiar_kostki / 3
        
        # Główne linie kostki - grubsze i jaśniejsze
        # Linie poziome
        for z in range(3):
            for y in range(3):
                start_3d = ((-1) * odstep, (y-1) * odstep, (z-1) * odstep)
                end_3d = ((1) * odstep, (y-1) * odstep, (z-1) * odstep)
                
                start_2d = self._projekt_punkt(start_3d)
                end_2d = self._projekt_punkt(end_3d)
                
                # Efekt świecenia - potrójne linie
                pygame.draw.line(screen, ZLOTY, start_2d, end_2d, 3)
                pygame.draw.line(screen, (255, 255, 150), start_2d, end_2d, 1)
        
        # Linie pionowe
        for z in range(3):
            for x in range(3):
                start_3d = ((x-1) * odstep, (-1) * odstep, (z-1) * odstep)
                end_3d = ((x-1) * odstep, (1) * odstep, (z-1) * odstep)
                
                start_2d = self._projekt_punkt(start_3d)
                end_2d = self._projekt_punkt(end_3d)
                
                pygame.draw.line(screen, ZLOTY, start_2d, end_2d, 3)
                pygame.draw.line(screen, (255, 255, 150), start_2d, end_2d, 1)
        
        # Linie przez głębokość
        for y in range(3):
            for x in range(3):
                start_3d = ((x-1) * odstep, (y-1) * odstep, (-1) * odstep)
                end_3d = ((x-1) * odstep, (y-1) * odstep, (1) * odstep)
                
                start_2d = self._projekt_punkt(start_3d)
                end_2d = self._projekt_punkt(end_3d)
                
                pygame.draw.line(screen, ZLOTY, start_2d, end_2d, 3)
                pygame.draw.line(screen, (255, 255, 150), start_2d, end_2d, 1)
    
    def _projekt_punkt(self, punkt_3d):
        """Projektuje punkt 3D na 2D"""
        pos_x, pos_y, pos_z = punkt_3d
        
        # Rotacje
        cos_x = math.cos(math.radians(self.rot_x))
        sin_x = math.sin(math.radians(self.rot_x))
        cos_y = math.cos(math.radians(self.rot_y))
        sin_y = math.sin(math.radians(self.rot_y))
        
        # Rotacja Y
        temp_x = pos_x * cos_y - pos_z * sin_y
        temp_z = pos_x * sin_y + pos_z * cos_y
        
        # Rotacja X
        temp_y = pos_y * cos_x - temp_z * sin_x
        final_z = pos_y * sin_x + temp_z * cos_x
        
        # Projekcja
        distance = 400
        scale = distance / (distance + final_z)
        
        screen_x = int(self.centrum_x + temp_x * scale)
        screen_y = int(self.centrum_y - temp_y * scale)
        
        return (screen_x, screen_y)
    
    def _narysuj_pole(self, screen, screen_x, screen_y, scale, x, y, z):
        """Rysuje pojedyncze pole z efektami wizualnymi"""
        znak = self.plansza[z, y, x]
        rozmiar = int(35 * scale)  # Powiększone z 20 do 35
        
        if znak == 'X':
            # Kolorowy kwadrat dla gracza
            self._narysuj_kwadrat_gracza(screen, screen_x, screen_y, rozmiar)
        elif znak == 'O':
            # Kolorowy kwadrat dla AI  
            self._narysuj_kwadrat_ai(screen, screen_x, screen_y, rozmiar)
        else:
            # Puste pole - z lepszą widocznością
            rozmiar_pola = int(rozmiar * 0.6)
            
            # Sprawdź czy to pole jest podświetlone
            is_highlighted = (self.highlighted_pole == (x, y, z))
            
            if is_highlighted:
                # Podświetlenie - jaśniejsze kolory
                pygame.draw.rect(screen, (120, 120, 150), 
                               (screen_x - rozmiar_pola, screen_y - rozmiar_pola, 
                                rozmiar_pola*2, rozmiar_pola*2))
                pygame.draw.rect(screen, ZLOTY, 
                               (screen_x - rozmiar_pola, screen_y - rozmiar_pola, 
                                rozmiar_pola*2, rozmiar_pola*2), 3)
                # Pulsujący środek
                pulse_size = int(rozmiar_pola * 0.3 + 5 * math.sin(pygame.time.get_ticks() * 0.01))
                pygame.draw.circle(screen, ZLOTY, 
                                 (screen_x, screen_y), pulse_size)
            else:
                # Normalne pole
                pygame.draw.rect(screen, (80, 80, 100), 
                               (screen_x - rozmiar_pola, screen_y - rozmiar_pola, 
                                rozmiar_pola*2, rozmiar_pola*2))
                pygame.draw.rect(screen, JASNY_SZARY, 
                               (screen_x - rozmiar_pola, screen_y - rozmiar_pola, 
                                rozmiar_pola*2, rozmiar_pola*2), 2)
                # Kropka w środku dla lepszej widoczności
                pygame.draw.circle(screen, (150, 150, 170), 
                                 (screen_x, screen_y), max(2, int(rozmiar_pola * 0.1)))
    
    def _narysuj_kwadrat_gracza(self, screen, x, y, rozmiar):
        """Rysuje kolorowy kwadrat dla gracza (X) z efektem gradientu"""
        # Gradient od pomarańczowego do czerwonego
        for i in range(rozmiar, 0, -4):
            # Oblicz kolor gradientu
            progress = (rozmiar - i) / rozmiar
            r = int(255 - progress * 50)  # Od 255 do 205
            g = int(150 - progress * 100)  # Od 150 do 50  
            b = int(50 + progress * 30)   # Od 50 do 80
            
            color = (r, g, b)
            
            # Narysuj prostokąt
            rect = pygame.Rect(x - i//2, y - i//2, i, i)
            pygame.draw.rect(screen, color, rect)
        
        # Obramowanie
        border_rect = pygame.Rect(x - rozmiar//2, y - rozmiar//2, rozmiar, rozmiar)
        pygame.draw.rect(screen, BIALY, border_rect, 3)
        
        # Połysk w lewym górnym rogu
        highlight_size = rozmiar // 4
        highlight_rect = pygame.Rect(x - rozmiar//2 + 5, y - rozmiar//2 + 5, 
                                   highlight_size, highlight_size)
        pygame.draw.rect(screen, (255, 255, 200), highlight_rect)
    
    def _narysuj_kwadrat_ai(self, screen, x, y, rozmiar):
        """Rysuje kolorowy kwadrat dla AI (O) z efektem gradientu"""
        # Gradient od niebieskiego do fioletowego
        for i in range(rozmiar, 0, -4):
            # Oblicz kolor gradientu
            progress = (rozmiar - i) / rozmiar
            r = int(100 + progress * 80)   # Od 100 do 180
            g = int(150 - progress * 50)   # Od 150 do 100
            b = int(255 - progress * 50)   # Od 255 do 205
            
            color = (r, g, b)
            
            # Narysuj prostokąt
            rect = pygame.Rect(x - i//2, y - i//2, i, i)
            pygame.draw.rect(screen, color, rect)
        
        # Obramowanie
        border_rect = pygame.Rect(x - rozmiar//2, y - rozmiar//2, rozmiar, rozmiar)
        pygame.draw.rect(screen, BIALY, border_rect, 3)
        
        # Połysk w lewym górnym rogu
        highlight_size = rozmiar // 4
        highlight_rect = pygame.Rect(x - rozmiar//2 + 5, y - rozmiar//2 + 5, 
                                   highlight_size, highlight_size)
        pygame.draw.rect(screen, (200, 200, 255), highlight_rect)
    
    def znajdz_klikniete_pole(self, mouse_pos):
        """Znajduje pole na które kliknięto - zwiększona tolerancja"""
        mouse_x, mouse_y = mouse_pos
        min_odleglosc = float('inf')
        najblizsze_pole = None
        
        for screen_x, screen_y, scale, x, y, z in self.pola_2d:
            odleglosc = math.sqrt((mouse_x - screen_x)**2 + (mouse_y - screen_y)**2)
            tolerancja = 50 * scale  # Zwiększona tolerancja zależna od odległości
            if odleglosc < min_odleglosc and odleglosc < tolerancja:
                min_odleglosc = odleglosc
                najblizsze_pole = (x, y, z)
        
        return najblizsze_pole
    
    def aktualizuj_podswietlenie(self, mouse_pos):
        """Aktualizuje podświetlenie pola pod kursorem"""
        if not self.czy_ruch_ai and not self.tryb_ai_vs_ai:  # Tylko gdy gracz może grać
            pole = self.znajdz_klikniete_pole(mouse_pos)
            if pole and self.plansza[pole[2], pole[1], pole[0]] == ' ':
                self.highlighted_pole = pole
            else:
                self.highlighted_pole = None
        else:
            self.highlighted_pole = None
    
    def wykonaj_ruch(self, x, y, z):
        """Wykonuje ruch gracza"""
        if self.koniec_gry or self.plansza[z, y, x] != ' ':
            return False
        
        self.plansza[z, y, x] = self.aktualny_gracz
        
        if self.sprawdz_zwyciezce():
            self.koniec_gry = True
            self.zwyciezca = self.aktualny_gracz
        elif self.czy_plansza_pelna():
            self.koniec_gry = True
            self.zwyciezca = 'Remis'
        else:
            # Zmień gracza
            self.aktualny_gracz = 'O' if self.aktualny_gracz == 'X' else 'X'
            if self.tryb_ai_vs_ai:
                self.czy_ruch_ai = True  # W trybie AI vs AI zawsze kolej AI
            else:
                self.czy_ruch_ai = (self.aktualny_gracz == self.gracz_ai)
        
        return True
    
    def wlacz_tryb_ai_vs_ai(self, auto_start=False):
        """Włącza tryb AI vs AI"""
        self.tryb_ai_vs_ai = True
        self.czy_ruch_ai = True  # AI zawsze ma ruch
        self.auto_ai_vs_ai = auto_start
        
        if auto_start:
            print(f"🎬 AUTO-DEMO: AI vs AI WŁĄCZONY!")
            print(f"⏰ Ruchy co {self.ai_delay//1000} sekund dla lepszej obserwacji")
        else:
            print(f"🤖⚔️🤖 TRYB AI vs AI WŁĄCZONY!")
            
        print(f"🔴 {self.ai1_nazwa} (X) vs 🔵 {self.ai2_nazwa} (O)")
        print("🎯 Obserwuj strategie dwóch różnych AI!")
        print("="*60)
    
    def ruch_ai_vs_ai(self):
        """AI wykonuje ruch w trybie AI vs AI z różnymi strategiami"""
        if self.koniec_gry or not self.czy_ruch_ai:
            return
        
        # AI1 (X) - agresywna strategia
        if self.aktualny_gracz == 'X':
            self._ai_agresywny()
        # AI2 (O) - defensywna strategia  
        else:
            self._ai_defensywny()
    
    def _ai_agresywny(self):
        """AI agresywny - priorytet na atak"""
        # 1. Spróbuj wygrać
        ruch = self._znajdz_ruch_wygrywajacy('X')
        if ruch:
            x, y, z = ruch
            if self.wykonaj_ruch(x, y, z):
                print(f"🔴 {self.ai1_nazwa} zagrał WYGRYWAJĄCO na ({z},{y},{x})")
                return
        
        # 2. Zajmij centrum (priorytet ataku)
        if self.plansza[1, 1, 1] == ' ':
            if self.wykonaj_ruch(1, 1, 1):
                print(f"🔴 {self.ai1_nazwa} zajął CENTRUM (1,1,1)")
                return
        
        # 3. Zablokuj przeciwnika
        ruch = self._znajdz_ruch_wygrywajacy('O')
        if ruch:
            x, y, z = ruch
            if self.wykonaj_ruch(x, y, z):
                print(f"🔴 {self.ai1_nazwa} zablokowało przeciwnika na ({z},{y},{x})")
                return
        
        # 4. Narożniki
        self._zajmij_naroznik_lub_losowy('X')
    
    def _ai_defensywny(self):
        """AI defensywny - priorytet na obronę"""
        # 1. Zablokuj przeciwnika NAJPIERW
        ruch = self._znajdz_ruch_wygrywajacy('X')
        if ruch:
            x, y, z = ruch
            if self.wykonaj_ruch(x, y, z):
                print(f"🔵 {self.ai2_nazwa} zablokowało przeciwnika na ({z},{y},{x})")
                return
        
        # 2. Spróbuj wygrać
        ruch = self._znajdz_ruch_wygrywajacy('O')
        if ruch:
            x, y, z = ruch
            if self.wykonaj_ruch(x, y, z):
                print(f"🔵 {self.ai2_nazwa} zagrał WYGRYWAJĄCO na ({z},{y},{x})")
                return
        
        # 3. Centrum
        if self.plansza[1, 1, 1] == ' ':
            if self.wykonaj_ruch(1, 1, 1):
                print(f"🔵 {self.ai2_nazwa} zajął CENTRUM (1,1,1)")
                return
        
        # 4. Krawędzie (defensywne)
        krawedzie = [(1,0,1), (1,2,1), (0,1,1), (2,1,1), (1,1,0), (1,1,2)]
        dostepne_krawedzie = [(x,y,z) for x,y,z in krawedzie if self.plansza[z,y,x] == ' ']
        if dostepne_krawedzie:
            x, y, z = random.choice(dostepne_krawedzie)
            if self.wykonaj_ruch(x, y, z):
                print(f"🔵 {self.ai2_nazwa} zajął KRAWĘDŹ ({z},{y},{x})")
                return
        
        # 5. Narożniki
        self._zajmij_naroznik_lub_losowy('O')
    
    def _zajmij_naroznik_lub_losowy(self, gracz):
        """Zajmuje narożnik lub gra losowo"""
        narozniki = [(0,0,0), (0,0,2), (0,2,0), (0,2,2), 
                     (2,0,0), (2,0,2), (2,2,0), (2,2,2)]
        dostepne_narozniki = [(x,y,z) for x,y,z in narozniki if self.plansza[z,y,x] == ' ']
        
        if dostepne_narozniki:
            x, y, z = random.choice(dostepne_narozniki)
            if self.wykonaj_ruch(x, y, z):
                symbol = "🔴" if gracz == 'X' else "🔵"
                nazwa = self.ai1_nazwa if gracz == 'X' else self.ai2_nazwa
                print(f"{symbol} {nazwa} zajął NAROŻNIK ({z},{y},{x})")
                return
        
        # Losowy ruch
        dostepne_pola = []
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if self.plansza[z, y, x] == ' ':
                        dostepne_pola.append((x, y, z))
        
        if dostepne_pola:
            x, y, z = random.choice(dostepne_pola)
            if self.wykonaj_ruch(x, y, z):
                symbol = "🔴" if gracz == 'X' else "🔵"
                nazwa = self.ai1_nazwa if gracz == 'X' else self.ai2_nazwa
                print(f"{symbol} {nazwa} zagrał losowo na ({z},{y},{x})")
    
    def ruch_ai(self):
        """AI wykonuje inteligentny ruch"""
        if self.koniec_gry or not self.czy_ruch_ai:
            return
        
        ruch_wykonany = None
        
        # Strategia AI:
        # 1. Spróbuj wygrać
        ruch = self._znajdz_ruch_wygrywajacy(self.gracz_ai)
        if ruch:
            x, y, z = ruch
            if self.wykonaj_ruch(x, y, z):
                print(f"🤖 AI zagrało WYGRYWAJĄCO na ({z},{y},{x})")
                return
        
        # 2. Zablokuj gracza przed wygraną
        ruch = self._znajdz_ruch_wygrywajacy('X')
        if ruch:
            x, y, z = ruch
            if self.wykonaj_ruch(x, y, z):
                print(f"🤖 AI zablokowało na ({z},{y},{x})")
                return
        
        # 3. Zajmij centrum kostki (najlepsze pole strategiczne)
        if self.plansza[1, 1, 1] == ' ':
            if self.wykonaj_ruch(1, 1, 1):
                print(f"🤖 AI zajęło CENTRUM (1,1,1)")
                return
        
        # 4. Zajmij narożniki
        narozniki = [(0,0,0), (0,0,2), (0,2,0), (0,2,2), 
                     (2,0,0), (2,0,2), (2,2,0), (2,2,2)]
        dostepne_narozniki = [(x,y,z) for x,y,z in narozniki if self.plansza[z,y,x] == ' ']
        if dostepne_narozniki:
            x, y, z = random.choice(dostepne_narozniki)
            if self.wykonaj_ruch(x, y, z):
                print(f"🤖 AI zajęło NAROŻNIK ({z},{y},{x})")
                return
        
        # 5. Zajmij środki krawędzi głównych płaszczyzn
        krawedzie = [(1,0,1), (1,2,1), (0,1,1), (2,1,1), (1,1,0), (1,1,2)]
        dostepne_krawedzie = [(x,y,z) for x,y,z in krawedzie if self.plansza[z,y,x] == ' ']
        if dostepne_krawedzie:
            x, y, z = random.choice(dostepne_krawedzie)
            if self.wykonaj_ruch(x, y, z):
                print(f"🤖 AI zajęło KRAWĘDŹ ({z},{y},{x})")
                return
        
        # 6. Losowy ruch z dostępnych pól
        dostepne_pola = []
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if self.plansza[z, y, x] == ' ':
                        dostepne_pola.append((x, y, z))
        
        if dostepne_pola:
            x, y, z = random.choice(dostepne_pola)
            if self.wykonaj_ruch(x, y, z):
                print(f"🤖 AI zagrało losowo na ({z},{y},{x})")
    
    def _znajdz_ruch_wygrywajacy(self, gracz):
        """Znajduje ruch który pozwoli wygrać graczowi"""
        # Sprawdź wszystkie puste pola
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if self.plansza[z, y, x] == ' ':
                        # Symuluj ruch
                        self.plansza[z, y, x] = gracz
                        
                        # Sprawdź czy to wygrywa
                        temp_gracz = self.aktualny_gracz
                        self.aktualny_gracz = gracz
                        wygrywa = self.sprawdz_zwyciezce()
                        self.aktualny_gracz = temp_gracz
                        
                        # Cofnij ruch
                        self.plansza[z, y, x] = ' '
                        
                        if wygrywa:
                            return (x, y, z)
        return None
    
    def sprawdz_zwyciezce(self):
        """Sprawdza czy aktualny gracz wygrał - KOMPLETNA WALIDACJA 3D"""
        gracz = self.aktualny_gracz
        
        # 1. LINIE POZIOME W KAŻDYM POZIOMIE (9 linii)
        for z in range(3):
            # Wiersze (3 linie)
            for y in range(3):
                if all(self.plansza[z, y, x] == gracz for x in range(3)):
                    return True
            # Kolumny (3 linie)  
            for x in range(3):
                if all(self.plansza[z, y, x] == gracz for y in range(3)):
                    return True
        
        # 2. PRZEKĄTNE W KAŻDYM POZIOMIE (6 linii)
        for z in range(3):
            # Główna przekątna w poziomie
            if all(self.plansza[z, i, i] == gracz for i in range(3)):
                return True
            # Druga przekątna w poziomie
            if all(self.plansza[z, i, 2-i] == gracz for i in range(3)):
                return True
        
        # 3. LINIE PIONOWE PRZEZ POZIOMY (9 linii)
        for x in range(3):
            for y in range(3):
                if all(self.plansza[z, y, x] == gracz for z in range(3)):
                    return True
        
        # 4. PRZEKĄTNE PIONOWE PRZEZ POZIOMY (18 linii)
        # Przekątne w płaszczyźnie XZ (6 linii)
        for y in range(3):
            # Główna przekątna XZ
            if all(self.plansza[z, y, z] == gracz for z in range(3)):
                return True
            # Druga przekątna XZ
            if all(self.plansza[z, y, 2-z] == gracz for z in range(3)):
                return True
        
        # Przekątne w płaszczyźnie YZ (6 linii) 
        for x in range(3):
            # Główna przekątna YZ
            if all(self.plansza[z, z, x] == gracz for z in range(3)):
                return True
            # Druga przekątna YZ
            if all(self.plansza[z, 2-z, x] == gracz for z in range(3)):
                return True
        
        # Przekątne w płaszczyźnie XY (6 linii)
        for z in range(3):
            # Główna przekątna XY (już sprawdzona wyżej w punkcie 2)
            # Druga przekątna XY (już sprawdzona wyżej w punkcie 2)
            pass
        
        # 5. GŁÓWNE PRZEKĄTNE 3D PRZEZ CAŁĄ KOSTKĘ (4 linie)
        # Przekątna (0,0,0) -> (1,1,1) -> (2,2,2)
        if all(self.plansza[i, i, i] == gracz for i in range(3)):
            return True
        # Przekątna (0,0,2) -> (1,1,1) -> (2,2,0) 
        if all(self.plansza[i, i, 2-i] == gracz for i in range(3)):
            return True
        # Przekątna (0,2,0) -> (1,1,1) -> (2,0,2)
        if all(self.plansza[i, 2-i, i] == gracz for i in range(3)):
            return True
        # Przekątna (0,2,2) -> (1,1,1) -> (2,0,0)
        if all(self.plansza[i, 2-i, 2-i] == gracz for i in range(3)):
            return True
        
        return False
    
    def czy_plansza_pelna(self):
        """Sprawdza czy plansza jest pełna"""
        return not np.any(self.plansza == ' ')
    
    def obrot(self, delta_x, delta_y):
        """Obraca kostką - płynniej"""
        self.rot_y += delta_x * 0.8  # Zwiększona czułość
        self.rot_x += delta_y * 0.8  # Zwiększona czułość
        
        # Ograniczenia rotacji X dla lepszego widoku
        self.rot_x = max(-80, min(80, self.rot_x))


def narysuj_ui(screen, kostka, font):
    """Rysuje interfejs użytkownika z lepszą widocznością"""
    # Półprzezroczyste tło dla UI
    ui_width = 500 if kostka.tryb_ai_vs_ai else 400
    ui_surface = pygame.Surface((ui_width, 120))
    ui_surface.set_alpha(200)
    ui_surface.fill((20, 20, 30))
    screen.blit(ui_surface, (5, 5))
    
    if kostka.koniec_gry:
        if kostka.zwyciezca == 'Remis':
            tekst = font.render("🤝 REMIS!", True, ZLOTY)
        elif kostka.zwyciezca == 'X':
            if kostka.tryb_ai_vs_ai:
                tekst = font.render(f"🔴 {kostka.ai1_nazwa} WYGRAŁ! 🟧", True, ZIELONY)
            else:
                tekst = font.render("🎉 WYGRAŁEŚ! 🟧", True, ZIELONY)
        else:
            if kostka.tryb_ai_vs_ai:
                tekst = font.render(f"🔵 {kostka.ai2_nazwa} WYGRAŁ! 🟦", True, FIOLETOWY)
            else:
                tekst = font.render("🤖 AI WYGRAŁO! 🟦", True, FIOLETOWY)
        screen.blit(tekst, (15, 15))
        
        restart_tekst = font.render("R - nowa gra | A - tryb AI vs AI | P - tryb gracza", True, JASNY_SZARY)
        screen.blit(restart_tekst, (15, 55))
    else:
        if kostka.tryb_ai_vs_ai:
            if kostka.aktualny_gracz == 'X':
                tekst = font.render(f"🔴 Ruch: {kostka.ai1_nazwa} 🟧", True, POMARANCZOWY)
            else:
                tekst = font.render(f"🔵 Ruch: {kostka.ai2_nazwa} 🟦", True, TURKUSOWY)
        else:
            if kostka.czy_ruch_ai:
                tekst = font.render("🤖 Ruch AI... 🟦", True, TURKUSOWY)
            else:
                tekst = font.render("👤 Twój ruch 🟧", True, POMARANCZOWY)
        screen.blit(tekst, (15, 15))
    
    # Instrukcje z lepszą widocznością
    instrukcje = [
        "🎮 KÓŁKO I KRZYŻYK 3D",
        "",
        "TRYBY GRY:",
        "👤 vs 🤖: Ty vs AI",
        "🤖 vs 🤖: AI vs AI (automatyczna gra!)",
        "",
        "STEROWANIE:",
        "LPM - wykonaj ruch (tylko tryb gracza)",
        "PPM - obracaj kostką (przeciągnij)", 
        "STRZAŁKI - obracaj kostką",
        "",
        "KLAWISZE:",
        "R - nowa gra (obecny tryb)",
        "A - przełącz na AI vs AI",
        "P - przełącz na tryb gracza", 
        "ESC - wyjście",
        "",
        "Ułóż 3 kwadraty w linii w przestrzeni 3D!",
    ]
    
    # Półprzezroczyste tło dla instrukcji
    ui_height = len(instrukcje) * 22 + 10
    ui_surface = pygame.Surface((450, ui_height))
    ui_surface.set_alpha(180)
    ui_surface.fill((20, 20, 30))
    screen.blit(ui_surface, (5, 550))
    
    font_maly = pygame.font.Font(None, 24)
    for i, instrukcja in enumerate(instrukcje):
        if i == 0:
            kolor = ZLOTY  # Tytuł
        elif "TY:" in instrukcja or "AI:" in instrukcja:
            kolor = TURKUSOWY  # Opis graczy
        else:
            kolor = JASNY_SZARY  # Instrukcje
        tekst = font_maly.render(instrukcja, True, kolor)
        screen.blit(tekst, (15, 560 + i * 22))  # Przesunięte niżej bo większe okno


def main(auto_demo=False, instance=1):
    """Główna funkcja gry"""
    pygame.init()
    
    # Pozycjonowanie okien dla różnych instancji
    window_positions = {
        1: (200, 100),   # Główne okno - centrum
        2: (800, 400),   # Drugie okno - prawy dół  
        3: (50, 400)     # Trzecie okno - lewy dół
    }
    
    # Rozmiary okien - główne większe, pozostałe mniejsze
    window_sizes = {
        1: (1000, 700),  # Główne okno - duże
        2: (600, 400),   # Drugie okno - mniejsze
        3: (600, 400)    # Trzecie okno - mniejsze
    }
    
    # Ustawienie pozycji okna
    if instance in window_positions:
        x, y = window_positions[instance]
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
    
    # Rozmiar okna zależny od instancji
    if instance in window_sizes:
        szeroksc, wysoksc = window_sizes[instance]
    else:
        szeroksc, wysoksc = 900, 600
        
    screen = pygame.display.set_mode((szeroksc, wysoksc))
    
    # Tytuł okna z oznaczeniem aktywności
    if instance == 1:
        pygame.display.set_caption(f"🎮 Kółko i Krzyżyk 3D - Gra #{instance} [GŁÓWNA]")
    else:
        pygame.display.set_caption(f"🎮 Kółko i Krzyżyk 3D - Gra #{instance}")
    
    kostka = Kostka3D(szeroksc, wysoksc)
    
    # Auto-demo mode - natychmiast uruchom AI vs AI z dłuższym delay
    if auto_demo:
        kostka.ai_delay = 10000  # 10 sekund zamiast 1.2
        kostka.wlacz_tryb_ai_vs_ai(auto_start=True)
    
    # Multi-instance mode - Human vs AI z 10s delay dla AI
    if instance > 0 and not auto_demo:
        kostka.ai_delay = 10000  # 10 sekund dla AI w trybie human vs AI
        kostka.czy_ruch_ai = False  # Gracz zaczyna
        print(f"🎮 INSTANCJA #{instance} - HUMAN vs AI")
        print(f"👤 TY: 🟧 (pomarańczowe kwadraty)  🤖 AI: 🟦 (niebieskie kwadraty)")
        print(f"⏰ AI wykona ruch co 10 sekund")
        if instance == 1:
            print(f"🎯 GŁÓWNA GRA - na pierwszym planie")
        else:
            print(f"📱 Gra w tle - naciśnij {instance} aby przybliżyć")
    
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    
    mouse_pressed = False
    last_mouse_pos = None
    ai_timer = 0  # Timer dla ruchu AI
    
    print("🎮 KÓŁKO I KRZYŻYK 3D vs AI!")
    print("============================")
    print("👤 TY: 🟧 (pomarańczowe kwadraty)  🤖 AI: 🟦 (niebieskie kwadraty)")
    print()
    print("🎮 TRYBY GRY:")
    print("👤 vs 🤖 - Tryb normalny (domyślny)")
    print("🤖 vs 🤖 - Naciśnij A aby włączyć tryb AI vs AI!")
    print()
    print("⌨️  STEROWANIE:")
    print("LPM - kliknij w pole aby wykonać ruch")
    print("PPM - przeciągnij aby obracać kostką")
    print("STRZAŁKI - obracaj kostką")
    print()
    print("🔧 KLAWISZE:")
    print("A - włącz tryb AI vs AI (obserwuj walkę AI!)")
    print("P - powrót do trybu gracza")
    print("R - restart gry")
    print("ESC - wyjście")
    print()
    print("🎯 CEL: Ułóż 3 kwadraty w linii w przestrzeni 3D!")
    print("="*50)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # Globalne przełączanie między instancjami - bring to front
                if event.key == pygame.K_1:
                    print(f"🎮 AKTYWACJA: Gra #1 - GŁÓWNA")
                    bring_window_to_front("Gra #1")
                    pygame.display.set_caption(f"🎮 Kółko i Krzyżyk 3D - Gra #1 [GŁÓWNA - AKTYWNA]")
                elif event.key == pygame.K_2:
                    print(f"🎮 AKTYWACJA: Gra #2")
                    bring_window_to_front("Gra #2") 
                    pygame.display.set_caption(f"🎮 Kółko i Krzyżyk 3D - Gra #2 [AKTYWNA]")
                elif event.key == pygame.K_3:
                    print(f"🎮 AKTYWACJA: Gra #3")
                    bring_window_to_front("Gra #3")
                    pygame.display.set_caption(f"🎮 Kółko i Krzyżyk 3D - Gra #3 [AKTYWNA]")
                
                # Reszta obsługi klawiszy
                if event.key == pygame.K_r:
                    kostka = Kostka3D(szeroksc, wysoksc)  # Restart gry
                    ai_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_a:  # Włącz AI vs AI
                    kostka = Kostka3D(szeroksc, wysoksc)
                    kostka.wlacz_tryb_ai_vs_ai(auto_start=False)
                    ai_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_p:  # Włącz tryb gracza
                    kostka = Kostka3D(szeroksc, wysoksc)
                    print("👤 TRYB GRACZA WŁĄCZONY!")
                    print("👤 TY: 🟧 (pomarańczowe kwadraty)  🤖 AI: 🟦 (niebieskie kwadraty)")
                    ai_timer = pygame.time.get_ticks()
                # Obracanie klawiszami strzałek
                elif event.key == pygame.K_LEFT:
                    kostka.obrot(-10, 0)
                elif event.key == pygame.K_RIGHT:
                    kostka.obrot(10, 0)
                elif event.key == pygame.K_UP:
                    kostka.obrot(0, -10)
                elif event.key == pygame.K_DOWN:
                    kostka.obrot(0, 10)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # LPM - wykonaj ruch
                    if not kostka.czy_ruch_ai:  # Tylko gdy nie kolej AI
                        pole = kostka.znajdz_klikniete_pole(event.pos)
                        if pole and not kostka.koniec_gry:
                            x, y, z = pole
                            if kostka.wykonaj_ruch(x, y, z):
                                print(f"👤 Gracz zagrał na pozycji ({z},{y},{x})")
                                ai_timer = pygame.time.get_ticks()  # Rozpocznij timer AI
                
                elif event.button == 3:  # PPM - rozpocznij rotację
                    mouse_pressed = True
                    last_mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # PPM - zakończ rotację  
                    mouse_pressed = False
            
            elif event.type == pygame.MOUSEMOTION:
                if not kostka.tryb_ai_vs_ai:  # Podświetlanie tylko w trybie gracza
                    kostka.aktualizuj_podswietlenie(event.pos)
                if mouse_pressed:
                    if last_mouse_pos:
                        dx = event.pos[0] - last_mouse_pos[0]
                        dy = event.pos[1] - last_mouse_pos[1]
                        kostka.obrot(dx, dy)
                        last_mouse_pos = event.pos
        
        # AI wykonuje ruch po krótkiej przerwie
        if kostka.czy_ruch_ai and not kostka.koniec_gry:
            current_time = pygame.time.get_ticks()
            # Dynamiczne opóźnienie - długie w multi-instance lub auto-demo
            if auto_demo:
                delay = kostka.ai_delay if kostka.auto_ai_vs_ai else 1200
            elif instance > 0:
                delay = kostka.ai_delay  # 10 sekund w trybie multi-instance
            else:
                delay = 1200  # Normalny tryb
                
            if current_time - ai_timer > delay:
                if kostka.tryb_ai_vs_ai:
                    kostka.ruch_ai_vs_ai()
                else:
                    kostka.ruch_ai()
                ai_timer = current_time
        
        # Renderowanie
        kostka.narysuj_kostke(screen)
        narysuj_ui(screen, kostka, font)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


class MouseControlledMultiGameManager:
    """Manager obsługujący 3 gry z aktywacją przez kliknięcie myszą"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 3 instancje gier
        self.games = [
            Kostka3D(screen_width, screen_height),  # Gra 0 - lewa w tle
            Kostka3D(screen_width, screen_height),  # Gra 1 - prawa w tle  
            Kostka3D(screen_width, screen_height)   # Gra 2 - aktywna z przodu
        ]
        
        # Indeksy gier: [lewa_tło, prawa_tło, aktywna]
        self.game_positions = [0, 1, 2]  # które gry są na których pozycjach
        
        # 📊 SYSTEM PUNKTOWY
        self.total_score = 0  # Globalny wynik gracza
        self.game_end_timers = [0, 0, 0]  # Timer dla każdej gry (10 sekund)
        self.game_end_messages = [None, None, None]  # Komunikaty końca gry
        self.games_in_end_state = [False, False, False]  # Które gry są w stanie końcowym
        
        # Ustawienia każdej gry na Human vs AI z 10s delay
        for i, game in enumerate(self.games):
            game.ai_delay = 10000
            game.czy_ruch_ai = False
            print(f"🎮 Gra #{i+1} - HUMAN vs AI gotowa (sterowanie myszą)")
        
        # Timery AI dla każdej gry
        self.ai_timers = [0, 0, 0]
        
        # Layout pozycji w oknie
        self.setup_layout()
    
    def setup_layout(self):
        """Ustawia pozycje i rozmiary gier w oknie"""
        # Gra aktywna (duża, na dole)
        self.active_rect = pygame.Rect(100, 200, 800, 400)
        
        # Gry w tle (małe, u góry) - KLIKALNE
        self.background_left_rect = pygame.Rect(50, 20, 350, 160)   # Lewa góra
        self.background_right_rect = pygame.Rect(500, 20, 350, 160) # Prawa góra
    
    def setup_fullscreen_layout(self):
        """Ustawia pozycje dla pełnego ekranu - większe i lepiej rozłożone"""
        # Oblicz rozmiary na podstawie rozdzielczości ekranu
        margin = 40
        background_width = (self.screen_width - 4 * margin) // 2.5  # Większe gry w tle
        background_height = int(background_width * 0.6)  # Proporcje 5:3
        
        # Aktywna gra - mniejsza, żeby lepiej było widać gry w tle
        active_width = int(self.screen_width * 0.5)  # 50% szerokości ekranu (było 70%)
        active_height = int(active_width * 0.6)  # Proporcje 5:3
        active_x = (self.screen_width - active_width) // 2
        active_y = self.screen_height - active_height - margin * 2  # Więcej miejsca z góry
        
        self.active_rect = pygame.Rect(active_x, active_y, active_width, active_height)
        
        # Gry w tle - równomiernie rozłożone u góry
        top_y = margin
        left_x = margin
        right_x = self.screen_width - background_width - margin
        
        self.background_left_rect = pygame.Rect(left_x, top_y, background_width, background_height)
        self.background_right_rect = pygame.Rect(right_x, top_y, background_width, background_height)
    
    def handle_mouse_click(self, mouse_pos):
        """Obsługuje kliknięcia myszą - zarówno gameplay jak i aktywacja"""
        mx, my = mouse_pos
        
        # Sprawdź czy kliknięto w grę w tle (aktywacja)
        if self.background_left_rect.collidepoint(mx, my):
            # Kliknięto w lewą grę w tle - aktywuj ją
            self.activate_background_game(0)  # lewa pozycja tła
            return
        
        if self.background_right_rect.collidepoint(mx, my):
            # Kliknięto w prawą grę w tle - aktywuj ją
            self.activate_background_game(1)  # prawa pozycja tła
            return
        
        # Sprawdź czy kliknięto w aktywną grę (gameplay)
        if self.active_rect.collidepoint(mx, my):
            self.handle_active_game_click(mouse_pos)
    
    def activate_background_game(self, background_position):
        """Aktywuje grę z tła (pozycja 0=lewa, 1=prawa)"""
        # Zamiana: aktywna <-> wybrana z tła
        active_game_idx = self.game_positions[2]  # aktualna aktywna
        background_game_idx = self.game_positions[background_position]  # wybrana z tła
        
        # Swap
        self.game_positions[2] = background_game_idx      # tło -> aktywna
        self.game_positions[background_position] = active_game_idx  # aktywna -> tło
        
        pos_name = "lewą" if background_position == 0 else "prawą"
        print(f"🖱️ KLIKNIĘTO: {pos_name} grę -> Gra #{background_game_idx+1} teraz AKTYWNA")
    
    def handle_active_game_click(self, mouse_pos):
        """Obsługuje gameplay w aktywnej grze"""
        active_game = self.games[self.game_positions[2]]
        
        # Przeskaluj pozycję myszy dla aktywnej gry
        scaled_pos = self.scale_mouse_pos(mouse_pos, self.active_rect)
        if scaled_pos:
            pole = active_game.znajdz_klikniete_pole(scaled_pos)
            if pole and not active_game.koniec_gry and not active_game.czy_ruch_ai:
                x, y, z = pole
                if active_game.wykonaj_ruch(x, y, z):
                    active_idx = self.game_positions[2]
                    print(f"👤 Gracz zagrał w grze #{active_idx+1} na pozycji ({z},{y},{x})")
                    self.ai_timers[active_idx] = pygame.time.get_ticks()
    
    def update_ai(self):
        """Aktualizuje AI we wszystkich grach"""
        current_time = pygame.time.get_ticks()
        
        for i, game in enumerate(self.games):
            if game.czy_ruch_ai and not game.koniec_gry:
                if current_time - self.ai_timers[i] > game.ai_delay:
                    game.ruch_ai()
                    self.ai_timers[i] = current_time
                    print(f"🤖 AI w grze #{i+1} wykonało ruch")
    
    def check_game_endings(self):
        """Sprawdza końce gier i obsługuje system punktowy"""
        current_time = pygame.time.get_ticks()
        
        for i, game in enumerate(self.games):
            # Sprawdź czy gra się właśnie zakończyła
            if game.koniec_gry and not self.games_in_end_state[i]:
                print(f"🏆 Gra #{i+1} ZAKOŃCZONA!")
                self.games_in_end_state[i] = True
                self.game_end_timers[i] = current_time
                
                # Ustal wynik i komunikat
                if game.zwyciezca == 'X':  # Gracz wygrał
                    self.total_score += 1
                    self.game_end_messages[i] = "🎉 WYGRAŁEŚ TĘ PARTIĘ!"
                    print(f"👤 Gracz wygrał grę #{i+1}! Punkty: +{self.total_score}")
                elif game.zwyciezca == 'O':  # AI wygrało
                    self.total_score -= 1
                    self.game_end_messages[i] = "🤖 AI WYGRAŁO TĘ PARTIĘ!"
                    print(f"🤖 AI wygrało grę #{i+1}! Punkty: {self.total_score}")
                else:  # Remis
                    # Remis = bez zmiany punktów
                    self.game_end_messages[i] = "🤝 REMIS W TEJ PARTII!"
                    print(f"🤝 Remis w grze #{i+1}! Punkty: {self.total_score}")
            
            # Sprawdź czy minęło 10 sekund i restart grę
            if self.games_in_end_state[i]:
                if current_time - self.game_end_timers[i] > 10000:  # 10 sekund
                    print(f"🔄 Restartowanie gry #{i+1}...")
                    self.games[i] = Kostka3D(self.screen_width, self.screen_height)
                    self.games[i].ai_delay = 10000
                    self.games[i].czy_ruch_ai = False
                    self.ai_timers[i] = 0
                    
                    # Reset stanu końcowego
                    self.games_in_end_state[i] = False
                    self.game_end_timers[i] = 0
                    self.game_end_messages[i] = None
                    print(f"✅ Gra #{i+1} zrestartowana! Punkty zachowane: {self.total_score}")
    
    def scale_mouse_pos(self, mouse_pos, target_rect):
        """Przeskalowuje pozycję myszy do docelowego prostokąta"""
        mx, my = mouse_pos
        if target_rect.collidepoint(mx, my):
            # Przeskaluj do rozmiaru gry
            rel_x = (mx - target_rect.x) * self.screen_width // target_rect.width
            rel_y = (my - target_rect.y) * self.screen_height // target_rect.height
            return (rel_x, rel_y)
        return None
    
    def draw(self, screen):
        """Rysuje wszystkie 3 gry z wizualną wskazówką o klikalności"""
        # Wypełnij tło
        screen.fill((20, 25, 35))
        
        # Pobierz gry według pozycji
        left_game = self.games[self.game_positions[0]]
        right_game = self.games[self.game_positions[1]]
        active_game = self.games[self.game_positions[2]]
        
        # Tymczasowe powierzchnie
        left_surface = pygame.Surface((self.screen_width, self.screen_height))
        right_surface = pygame.Surface((self.screen_width, self.screen_height))
        active_surface = pygame.Surface((self.screen_width, self.screen_height))
        
        # Narysuj gry na powierzchniach
        left_game.narysuj_kostke(left_surface)
        right_game.narysuj_kostke(right_surface)
        active_game.narysuj_kostke(active_surface)
        
        # Przeskaluj
        left_scaled = pygame.transform.scale(left_surface, self.background_left_rect.size)
        right_scaled = pygame.transform.scale(right_surface, self.background_right_rect.size)
        active_scaled = pygame.transform.scale(active_surface, self.active_rect.size)
        
        # Dodaj ramki - KLIKALNE gry mają żółte ramki
        pygame.draw.rect(screen, (255, 255, 0), self.background_left_rect, 3)   # Żółta - klikalna
        pygame.draw.rect(screen, (255, 255, 0), self.background_right_rect, 3)  # Żółta - klikalna  
        pygame.draw.rect(screen, (0, 255, 0), self.active_rect, 3)  # Zielona - aktywna do gry
        
        # Narysuj gry
        screen.blit(left_scaled, self.background_left_rect)
        screen.blit(right_scaled, self.background_right_rect)
        screen.blit(active_scaled, self.active_rect)
        
        # Etykiety z instrukcjami
        font = pygame.font.Font(None, 24)
        left_idx = self.game_positions[0]
        right_idx = self.game_positions[1] 
        active_idx = self.game_positions[2]
        
        left_text = font.render(f"Gra #{left_idx+1} - KLIKNIJ aby aktywować", True, (255, 255, 0))
        right_text = font.render(f"Gra #{right_idx+1} - KLIKNIJ aby aktywować", True, (255, 255, 0))
        active_text = font.render(f"Gra #{active_idx+1} - AKTYWNA (graj tutaj)", True, (0, 255, 0))
        
        screen.blit(left_text, (self.background_left_rect.x, self.background_left_rect.y - 25))
        screen.blit(right_text, (self.background_right_rect.x, self.background_right_rect.y - 25))
        screen.blit(active_text, (self.active_rect.x + 250, self.active_rect.y - 25))
        
        # 📊 WYNIK GLOBALNY NA GÓRZE EKRANU
        score_font = pygame.font.Font(None, 48)
        score_color = (0, 255, 0) if self.total_score >= 0 else (255, 50, 50)
        score_text = score_font.render(f"TWÓJ WYNIK TO: {self.total_score:+d}", True, score_color)
        score_rect = score_text.get_rect(center=(screen.get_width() // 2, 50))
        
        # Tło dla wyniku
        score_bg = pygame.Surface((score_rect.width + 40, score_rect.height + 20))
        score_bg.set_alpha(180)
        score_bg.fill((20, 20, 40))
        screen.blit(score_bg, (score_rect.x - 20, score_rect.y - 10))
        screen.blit(score_text, score_rect)
        
        # 🏆 KOMUNIKATY KOŃCA GRY (na środku każdej gry)
        self.draw_game_end_messages(screen, left_game, self.background_left_rect, self.game_positions[0])
        self.draw_game_end_messages(screen, right_game, self.background_right_rect, self.game_positions[1])
        self.draw_game_end_messages(screen, active_game, self.active_rect, self.game_positions[2])
    
    def draw_game_end_messages(self, screen, game, game_rect, game_index):
        """Rysuje komunikaty końca gry dla konkretnej gry"""
        if self.games_in_end_state[game_index] and self.game_end_messages[game_index]:
            # Semi-transparentne tło
            overlay = pygame.Surface(game_rect.size)
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, game_rect)
            
            # Główny komunikat (duży)
            big_font = pygame.font.Font(None, 36 if game_rect.width < 400 else 64)
            message = self.game_end_messages[game_index]
            
            # Kolor komunikatu
            if "WYGRAŁEŚ" in message:
                color = (0, 255, 0)  # Zielony
            elif "AI WYGRAŁO" in message:
                color = (255, 100, 100)  # Czerwony  
            else:
                color = (255, 255, 100)  # Żółty (remis)
            
            message_text = big_font.render(message, True, color)
            message_rect = message_text.get_rect(center=(game_rect.centerx, game_rect.centery - 40))
            screen.blit(message_text, message_rect)
            
            # Wynik (mniejszy, pod spodem)
            score_font = pygame.font.Font(None, 28 if game_rect.width < 400 else 48)
            score_color = (0, 255, 0) if self.total_score >= 0 else (255, 100, 100)
            score_text = score_font.render(f"TWÓJ WYNIK TO: {self.total_score:+d}", True, score_color)
            score_rect = score_text.get_rect(center=(game_rect.centerx, game_rect.centery + 20))
            screen.blit(score_text, score_rect)
            
            # Countdown timer
            current_time = pygame.time.get_ticks()
            remaining_time = 10 - (current_time - self.game_end_timers[game_index]) // 1000
            if remaining_time > 0:
                timer_font = pygame.font.Font(None, 24 if game_rect.width < 400 else 36)
                timer_text = timer_font.render(f"Nowa gra za: {remaining_time}s", True, (200, 200, 200))
                timer_rect = timer_text.get_rect(center=(game_rect.centerx, game_rect.centery + 60))
                screen.blit(timer_text, timer_rect)


def main_mouse_controlled_games():
    """Główna funkcja dla 3 gier sterowanych myszą"""
    pygame.init()
    
    # Pełny ekran na starcie
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    pygame.display.set_caption("🖱️ Kółko i Krzyżyk 3D - STEROWANIE MYSZĄ (PEŁNY EKRAN)")
    
    # Manager 3 gier sterowanych myszą - dostosowany do pełnego ekranu
    mouse_manager = MouseControlledMultiGameManager(screen_width, screen_height)
    
    # Dostosuj layout do pełnego ekranu
    mouse_manager.setup_fullscreen_layout()
    clock = pygame.time.Clock()
    
    print("🖱️ MOUSE-CONTROLLED MULTI-GAME MODE!")
    print("="*50)
    print("🎯 3 gry sterowane myszą (PEŁNY EKRAN):")
    print("   - 1 aktywna gra (zielona ramka) - graj tutaj")
    print("   - 2 gry w tle (żółte ramki) - KLIKNIJ aby aktywować")
    print("🖱️ STEROWANIE:")
    print("   - KLIKNIJ w grę w tle -> aktywuje ją")
    print("   - KLIKNIJ w aktywnej grze -> wykonaj ruch")
    print("   - PPM -> obracaj kostką")
    print("   - F11 -> przełącz pełny ekran/okno")
    print("   - ESC -> wyjście")
    print("🤖 AI wykonuje ruch co 10 sekund w każdej grze")
    print("="*50)
    
    mouse_pressed = False
    last_mouse_pos = None
    fullscreen = True
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Potwierdzenie wyjścia
                    print("❓ ESC naciśnięty - naciśnij ponownie ESC aby wyjść lub dowolny inny klawisz aby kontynuować...")
                    confirm_exit = False
                    waiting_for_confirm = True
                    
                    # Pętla potwierdzenia
                    while waiting_for_confirm:
                        for confirm_event in pygame.event.get():
                            if confirm_event.type == pygame.KEYDOWN:
                                if confirm_event.key == pygame.K_ESCAPE:
                                    confirm_exit = True
                                waiting_for_confirm = False
                            elif confirm_event.type == pygame.QUIT:
                                confirm_exit = True
                                waiting_for_confirm = False
                        
                        # Rysuj ekran podczas oczekiwania na potwierdzenie
                        mouse_manager.draw(screen)
                        
                        # Dodaj tekst potwierdzenia
                        font = pygame.font.Font(None, 48)
                        text = font.render("ESC ponownie = WYJŚCIE, inny klawisz = KONTYNUUJ", True, (255, 255, 0))
                        text_rect = text.get_rect(center=(screen.get_width()//2, 50))
                        screen.blit(text, text_rect)
                        
                        pygame.display.flip()
                        pygame.time.wait(50)
                    
                    if confirm_exit:
                        running = False
                
                elif event.key == pygame.K_F11:
                    # Przełącz tryb pełny ekran
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        pygame.display.set_caption("🖱️ Kółko i Krzyżyk 3D - PEŁNY EKRAN")
                    else:
                        screen = pygame.display.set_mode((1400, 900))
                        pygame.display.set_caption("🖱️ Kółko i Krzyżyk 3D - OKNO")
                    
                    # Zaktualizuj rozmiary i layout
                    screen_width = screen.get_width()
                    screen_height = screen.get_height()
                    mouse_manager.screen_width = screen_width
                    mouse_manager.screen_height = screen_height
                    
                    if fullscreen:
                        mouse_manager.setup_fullscreen_layout()
                    else:
                        mouse_manager.setup_layout()
                    
                    print(f"🖥️ Przełączono na: {'Pełny ekran' if fullscreen else 'Okno'} ({screen_width}x{screen_height})")
                
                # Obsługa strzałek - obracanie aktywnej kostki
                elif event.key == pygame.K_LEFT:
                    active_game = mouse_manager.games[mouse_manager.game_positions[2]]
                    active_game.obrot(-10, 0)
                    print("⬅️ Obracanie w lewo")
                elif event.key == pygame.K_RIGHT:
                    active_game = mouse_manager.games[mouse_manager.game_positions[2]]
                    active_game.obrot(10, 0)
                    print("➡️ Obracanie w prawo")
                elif event.key == pygame.K_UP:
                    active_game = mouse_manager.games[mouse_manager.game_positions[2]]
                    active_game.obrot(0, -10)
                    print("⬆️ Obracanie w górę")
                elif event.key == pygame.K_DOWN:
                    active_game = mouse_manager.games[mouse_manager.game_positions[2]]
                    active_game.obrot(0, 10)
                    print("⬇️ Obracanie w dół")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # LPM - gameplay lub aktywacja
                    mouse_manager.handle_mouse_click(event.pos)
                elif event.button == 3:  # PPM - obracanie kostki (tylko aktywna gra)
                    mouse_pressed = True
                    last_mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # PPM - zakończ obracanie
                    mouse_pressed = False
            
            elif event.type == pygame.MOUSEMOTION:
                # Obracanie kostki w aktywnej grze
                if mouse_pressed:
                    active_game = mouse_manager.games[mouse_manager.game_positions[2]]
                    if last_mouse_pos:
                        dx = event.pos[0] - last_mouse_pos[0]
                        dy = event.pos[1] - last_mouse_pos[1]
                        # Sprawdź czy mysz jest w obszarze aktywnej gry
                        if mouse_manager.active_rect.collidepoint(event.pos):
                            active_game.obrot(dx, dy)
                        last_mouse_pos = event.pos
        
        # Update AI w wszystkich grach
        mouse_manager.update_ai()
        
        # 🎯 Sprawdź końce gier i system punktowy
        mouse_manager.check_game_endings()
        
        # Renderowanie
        mouse_manager.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


class MultiGameManager:
    """Manager do obsługi 3 gier w jednym oknie"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 3 instancje gier
        self.games = [
            Kostka3D(screen_width, screen_height),  # Gra 0 - lewa w tle
            Kostka3D(screen_width, screen_height),  # Gra 1 - prawa w tle  
            Kostka3D(screen_width, screen_height)   # Gra 2 - aktywna z przodu
        ]
        
        # Indeksy gier: [lewa_tło, prawa_tło, aktywna]
        self.game_positions = [0, 1, 2]  # które gry są na których pozycjach
        self.active_game_index = 2  # indeks aktywnej gry (zawsze 2)
        
        # Ustawienia każdej gry na Human vs AI z 10s delay
        for i, game in enumerate(self.games):
            game.ai_delay = 10000
            game.czy_ruch_ai = False
            print(f"🎮 Gra #{i+1} - HUMAN vs AI gotowa")
        
        # Timery AI dla każdej gry
        self.ai_timers = [0, 0, 0]
        
        # Layout pozycji w oknie
        self.setup_layout()
    
    def setup_layout(self):
        """Ustawia pozycje i rozmiary gier w oknie"""
        # Gra aktywna (duża, na dole)
        self.active_rect = pygame.Rect(100, 200, 800, 400)
        
        # Gry w tle (małe, u góry)
        self.background_left_rect = pygame.Rect(50, 20, 350, 160)   # Lewa góra
        self.background_right_rect = pygame.Rect(500, 20, 350, 160) # Prawa góra
    
    def swap_games(self, direction):
        """Zamienia aktywną grę z grą z tła"""
        if direction == 1:  # Cyfra 1 - lewa gra na pierwszy plan
            # Swap: aktywna <-> lewa_tło
            active_idx = self.game_positions[2]  # aktualna aktywna
            left_idx = self.game_positions[0]    # lewa w tle
            
            self.game_positions[2] = left_idx    # lewa staje się aktywna
            self.game_positions[0] = active_idx  # aktywna idzie na lewe tło
            
            print(f"🔄 SWAP: Gra #{left_idx+1} na pierwszy plan, Gra #{active_idx+1} na lewe tło")
            
        elif direction == 2:  # Cyfra 2 - prawa gra na pierwszy plan  
            # Swap: aktywna <-> prawa_tło
            active_idx = self.game_positions[2]  # aktualna aktywna
            right_idx = self.game_positions[1]   # prawa w tle
            
            self.game_positions[2] = right_idx   # prawa staje się aktywna
            self.game_positions[1] = active_idx  # aktywna idzie na prawe tło
            
            print(f"🔄 SWAP: Gra #{right_idx+1} na pierwszy plan, Gra #{active_idx+1} na prawe tło")
    
    def update_ai(self):
        """Aktualizuje AI we wszystkich grach"""
        current_time = pygame.time.get_ticks()
        
        for i, game in enumerate(self.games):
            if game.czy_ruch_ai and not game.koniec_gry:
                if current_time - self.ai_timers[i] > game.ai_delay:
                    game.ruch_ai()
                    self.ai_timers[i] = current_time
                    print(f"🤖 AI w grze #{i+1} wykonało ruch")
    
    def handle_click(self, mouse_pos):
        """Obsługuje kliknięcia tylko w aktywnej grze"""
        active_game = self.games[self.game_positions[2]]
        
        # Przeskaluj pozycję myszy dla aktywnej gry
        scaled_pos = self.scale_mouse_pos(mouse_pos, self.active_rect)
        if scaled_pos:
            pole = active_game.znajdz_klikniete_pole(scaled_pos)
            if pole and not active_game.koniec_gry and not active_game.czy_ruch_ai:
                x, y, z = pole
                if active_game.wykonaj_ruch(x, y, z):
                    active_idx = self.game_positions[2]
                    print(f"👤 Gracz zagrał w grze #{active_idx+1} na pozycji ({z},{y},{x})")
                    self.ai_timers[active_idx] = pygame.time.get_ticks()
    
    def scale_mouse_pos(self, mouse_pos, target_rect):
        """Przeskalowuje pozycję myszy do docelowego prostokąta"""
        mx, my = mouse_pos
        if target_rect.collidepoint(mx, my):
            # Przeskaluj do rozmiaru gry
            rel_x = (mx - target_rect.x) * self.screen_width // target_rect.width
            rel_y = (my - target_rect.y) * self.screen_height // target_rect.height
            return (rel_x, rel_y)
        return None
    
    def draw(self, screen):
        """Rysuje wszystkie 3 gry"""
        # Wypełnij tło
        screen.fill((20, 25, 35))
        
        # Narysuj gry w tle (małe)
        left_game = self.games[self.game_positions[0]]
        right_game = self.games[self.game_positions[1]]
        active_game = self.games[self.game_positions[2]]
        
        # Tymczasowe powierzchnie dla gier w tle
        left_surface = pygame.Surface((self.screen_width, self.screen_height))
        right_surface = pygame.Surface((self.screen_width, self.screen_height))
        active_surface = pygame.Surface((self.screen_width, self.screen_height))
        
        # Narysuj gry na tymczasowych powierzchniach
        left_game.narysuj_kostke(left_surface)
        right_game.narysuj_kostke(right_surface)
        active_game.narysuj_kostke(active_surface)
        
        # Przeskaluj i narysuj na ekranie
        left_scaled = pygame.transform.scale(left_surface, self.background_left_rect.size)
        right_scaled = pygame.transform.scale(right_surface, self.background_right_rect.size)
        active_scaled = pygame.transform.scale(active_surface, self.active_rect.size)
        
        # Dodaj ramki
        pygame.draw.rect(screen, (100, 100, 100), self.background_left_rect, 2)
        pygame.draw.rect(screen, (100, 100, 100), self.background_right_rect, 2) 
        pygame.draw.rect(screen, (255, 255, 255), self.active_rect, 3)  # Aktywna - biała ramka
        
        screen.blit(left_scaled, self.background_left_rect)
        screen.blit(right_scaled, self.background_right_rect)
        screen.blit(active_scaled, self.active_rect)
        
        # Etykiety
        font = pygame.font.Font(None, 24)
        left_idx = self.game_positions[0]
        right_idx = self.game_positions[1] 
        active_idx = self.game_positions[2]
        
        left_text = font.render(f"Gra #{left_idx+1} (naciśnij 1)", True, (200, 200, 200))
        right_text = font.render(f"Gra #{right_idx+1} (naciśnij 2)", True, (200, 200, 200))
        active_text = font.render(f"Gra #{active_idx+1} - AKTYWNA", True, (255, 255, 255))
        
        screen.blit(left_text, (self.background_left_rect.x, self.background_left_rect.y - 25))
        screen.blit(right_text, (self.background_right_rect.x, self.background_right_rect.y - 25))
        screen.blit(active_text, (self.active_rect.x + 300, self.active_rect.y - 25))


def main_multi_games():
    """Główna funkcja dla 3 gier w jednym oknie"""
    pygame.init()
    
    # Duże okno dla 3 gier
    screen_width, screen_height = 1200, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("🎮 Kółko i Krzyżyk 3D - 3 GRY W JEDNYM OKNIE")
    
    # Manager 3 gier
    multi_manager = MultiGameManager(screen_width, screen_height)
    clock = pygame.time.Clock()
    
    print("🎮 MULTI-GAME MODE STARTED!")
    print("="*50)
    print("🎯 3 gry w jednym oknie:")
    print("   - 1 aktywna gra (duża, na dole)")
    print("   - 2 gry w tle (małe, u góry)")
    print("📱 STEROWANIE:")
    print("   - CYFRA 1: przełącz na lewą grę")
    print("   - CYFRA 2: przełącz na prawą grę") 
    print("   - LPM: graj w aktywnej grze")
    print("   - ESC: wyjście")
    print("🤖 AI wykonuje ruch co 10 sekund w każdej grze")
    print("="*50)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    multi_manager.swap_games(1)
                elif event.key == pygame.K_2:
                    multi_manager.swap_games(2)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # LPM
                    multi_manager.handle_click(event.pos)
        
        # Update AI w wszystkich grach
        multi_manager.update_ai()
        
        # Renderowanie
        multi_manager.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    import sys
    # Sprawdź parametry uruchomienia
    auto_demo = "--auto-demo" in sys.argv
    multi_games = "--multi-games" in sys.argv
    mouse_games = "--mouse-games" in sys.argv
    
    if mouse_games:
        main_mouse_controlled_games()
    elif multi_games:
        main_multi_games()
    else:
        # Sprawdź numer instancji dla starego trybu
        instance = 0
        for arg in sys.argv:
            if arg.startswith("--instance="):
                try:
                    instance = int(arg.split("=")[1])
                except ValueError:
                    instance = 1
        
        main(auto_demo=auto_demo, instance=instance)