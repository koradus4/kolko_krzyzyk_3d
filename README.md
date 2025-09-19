# Kółko i Krzyżyk 3D

Prosta gra w kółko i krzyżyk na planszy 3x3x3.

## Uruchomienie

```
python main.py
```

## Jak grać

1. **Cel**: Ułóż 3 znaki w linii (poziomo, pionowo lub po przekątnej w 3D)

2. **Współrzędne**: Podawaj w formacie `poziom,wiersz,kolumna`
   - Poziom: 0, 1, 2 (od dołu do góry)
   - Wiersz: 0, 1, 2 (od góry do dołu)
   - Kolumna: 0, 1, 2 (od lewej do prawej)

3. **Przykłady ruchów**:
   - `0,0,0` - lewy górny róg poziomu 1
   - `1,1,1` - centrum planszy (najlepsza pozycja!)
   - `2,2,2` - prawy dolny róg poziomu 3

4. **Komendy**:
   - `help` - pokaż pomoc
   - `q` - zakończ grę

## Sposoby wygranej w 3D

- **Tradycyjne linie** w każdym poziomie (wiersze, kolumny, przekątne)
- **Linie pionowe** przez wszystkie poziomy
- **Przekątne 3D** przez różne poziomy (np. 0,0,0 → 1,1,1 → 2,2,2)

## Wymagania

- Python 3.6+
- numpy (`pip install numpy`)