"""
🎮 KÓŁKO I KRZZLOTY = (255, 220, 0)  # Jaśniejszy złoty
CIEMNY_SZARY = (32, 32, 40)  # Ciemniejsze tło
JASNY_SZARY = (220, 220, 220)
FIOLETOWY = (180, 50, 255)  # Nowy kolor
POMARANCZOWY = (255, 150, 0)  # Nowy kolor
TURKUSOWY = (0, 200, 200)  # Nowy kolor


class Kostka3D:2D VERSION Z AI 🎮
Wizualnie wygląda jak 3D ale używa tylko Pygame!
Graj przeciwko inteligentnemu AI!
"""

import pygame
import numpy as np
import math
import random
import time

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
        """Sprawdza czy aktualny gracz wygrał"""
        gracz = self.aktualny_gracz
        
        # Linie w poziomach
        for z in range(3):
            # Wiersze i kolumny
            for i in range(3):
                if (all(self.plansza[z, i, j] == gracz for j in range(3)) or
                    all(self.plansza[z, j, i] == gracz for j in range(3))):
                    return True
            # Przekątne w poziomie
            if (all(self.plansza[z, i, i] == gracz for i in range(3)) or
                all(self.plansza[z, i, 2-i] == gracz for i in range(3))):
                return True
        
        # Linie pionowe przez poziomy
        for x in range(3):
            for y in range(3):
                if all(self.plansza[z, y, x] == gracz for z in range(3)):
                    return True
        
        # Główne przekątne 3D
        if (all(self.plansza[i, i, i] == gracz for i in range(3)) or
            all(self.plansza[i, i, 2-i] == gracz for i in range(3)) or
            all(self.plansza[i, 2-i, i] == gracz for i in range(3)) or
            all(self.plansza[i, 2-i, 2-i] == gracz for i in range(3))):
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


def main(auto_demo=False):
    """Główna funkcja gry"""
    pygame.init()
    
    # Większe okno dla większej kostki
    szeroksc, wysoksc = 1000, 700  # Powiększone okno
    screen = pygame.display.set_mode((szeroksc, wysoksc))
    pygame.display.set_caption("🎮 Kółko i Krzyżyk 3D - Pseudo 3D")
    
    kostka = Kostka3D(szeroksc, wysoksc)
    
    # Auto-demo mode - natychmiast uruchom AI vs AI z dłuższym delay
    if auto_demo:
        kostka.ai_delay = 10000  # 10 sekund zamiast 1.2
        kostka.wlacz_tryb_ai_vs_ai(auto_start=True)
    
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
            # Dynamiczne opóźnienie - krótkie w trybie normalnym, długie w auto-demo
            delay = kostka.ai_delay if kostka.auto_ai_vs_ai else 1200
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


if __name__ == "__main__":
    import sys
    # Sprawdź czy uruchomiono z parametrem --auto-demo
    auto_demo = "--auto-demo" in sys.argv
    main(auto_demo=auto_demo)