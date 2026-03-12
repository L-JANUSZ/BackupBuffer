import os
import sys
import ctypes
from pathlib import Path
import logging
import shutil

def wczytaj_konfiguracje(plik_cfg="copy_cfg.txt"):
    """
    Wczytuje konfigurację z pliku copy_cfg.txt.
    
    Returns:
        tuple: (liczba_plikow_do_skopiowania, sciezka_zrodlowa, sciezka_docelowa)
    """
    liczba_plikow = None
    sciezka_origin = None
    sciezka_destination = None
    
    # Określ katalog, w którym znajduje się plik wykonywalny
    if getattr(sys, 'frozen', False):
        # Jeśli program jest skompilowany do .exe (PyInstaller)
        katalog_programu = os.path.dirname(sys.executable)
    else:
        # Jeśli uruchamiany jest jako skrypt Python
        katalog_programu = os.path.dirname(os.path.abspath(__file__))
    
    # Utwórz pełną ścieżkę do pliku copy_cfg.txt
    sciezka_cfg = os.path.join(katalog_programu, plik_cfg)
    
    try:
        with open(sciezka_cfg, 'r', encoding='utf-8') as f:
            for linia in f:
                linia = linia.strip()
                
                if linia.startswith("Number of files"):
                    # Wydobądź liczbę z linii "Number of files = 2" lub "Number of files = "2""
                    liczba_plikow = int(linia.split("=")[1].strip().strip('"'))
                
                elif linia.startswith("Origin path"):
                    # Wydobądź ścieżkę z linii 'Origin path: "C:\..."'
                    sciezka_origin = linia.split(":", 1)[1].strip().strip('"')
                
                elif linia.startswith("Destination path"):
                    # Wydobądź ścieżkę z linii 'Destination path: "C:\..."'
                    sciezka_destination = linia.split(":", 1)[1].strip().strip('"')
        
        if liczba_plikow is None or sciezka_origin is None or sciezka_destination is None:
            raise ValueError("Brak wymaganych danych w pliku konfiguracyjnym.")
        
        return liczba_plikow, sciezka_origin, sciezka_destination
    
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {sciezka_cfg}")
        print(f"Katalog programu: {katalog_programu}")
        return None, None, None
    except Exception as e:
        print(f"Błąd podczas wczytywania konfiguracji: {e}")
        return None, None, None


def kopiuj_najnowsze_pliki(sciezka_zrodlowa, sciezka_docelowa, liczba_plikow_do_skopiowania):
    """
    Kopiuje X najnowszych plików z folderu źródłowego do folderu docelowego.
    
    Args:
        sciezka_zrodlowa: Ścieżka do folderu źródłowego
        sciezka_docelowa: Ścieżka do folderu docelowego
        liczba_plikow_do_skopiowania: Liczba plików do skopiowania
    """
    try:
        folder_zrodlo = Path(sciezka_zrodlowa)
        folder_cel = Path(sciezka_docelowa)
        
        if not folder_zrodlo.exists() or not folder_zrodlo.is_dir():
            print(f"Folder źródłowy {sciezka_zrodlowa} nie istnieje lub nie jest folderem.")
            return
        
        # Utwórz folder docelowy, jeśli nie istnieje
        if not folder_cel.exists():
            print(f"Folder docelowy {sciezka_docelowa} nie istnieje. Tworzę...")
            folder_cel.mkdir(parents=True, exist_ok=True)
            logging.info(f"Utworzono folder docelowy: {sciezka_docelowa}")
        
        # Pobierz wszystkie pliki (pomijając podfoldery)
        pliki = [f for f in folder_zrodlo.iterdir() if f.is_file()]
        
        if len(pliki) == 0:
            print("Folder źródłowy jest pusty.")
            return
        
        print(f"Znaleziono {len(pliki)} plików w folderze źródłowym.")
        print(f"Ma zostać skopiowanych {liczba_plikow_do_skopiowania} plików.")
        
        # Posortuj pliki według czasu modyfikacji (najnowsze najpierw)
        pliki_posortowane = sorted(pliki, key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Wybierz X najnowszych plików
        liczba_do_skopiowania = min(liczba_plikow_do_skopiowania, len(pliki))
        pliki_do_skopiowania = pliki_posortowane[:liczba_do_skopiowania]
        
        print(f"\nKopiowanie {len(pliki_do_skopiowania)} najnowszych plików:")
        
        for plik in pliki_do_skopiowania:
            sciezka_docelowa_plik = folder_cel / plik.name
            print(f"  - {plik.name}")
            shutil.copy2(plik, sciezka_docelowa_plik)
        
        print(f"\nSkopiowano {len(pliki_do_skopiowania)} plików do folderu {sciezka_docelowa}.")
        
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        logging.error(f"Błąd podczas kopiowania: {e}", exc_info=True)


def pokaz_konsole():
    """Pokaż okno konsoli (jeśli jest ukryte w exe)."""
    if sys.platform == "win32":
        try:
            # Pokaż istniejące okno konsoli
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd:
                ctypes.windll.user32.ShowWindow(whnd, 5)  # 5 = SW_SHOW
        except:
            pass


if __name__ == "__main__":
    try:
        # Konfiguruj logging
        if getattr(sys, 'frozen', False):
            katalog_programu = os.path.dirname(sys.executable)
        else:
            katalog_programu = os.path.dirname(os.path.abspath(__file__))
        
        plik_logu = os.path.join(katalog_programu, "copy_maker.log")
        logging.basicConfig(
            filename=plik_logu,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Program uruchomiony")
        
        # Wczytaj konfigurację z pliku copy_cfg.txt
        liczba_plikow, sciezka_zrodlowa, sciezka_docelowa = wczytaj_konfiguracje()
        
        if liczba_plikow is not None and sciezka_zrodlowa is not None and sciezka_docelowa is not None:
            print(f"Konfiguracja wczytana:")
            print(f"  - Liczba plików do skopiowania: {liczba_plikow}")
            print(f"  - Folder źródłowy: {sciezka_zrodlowa}")
            print(f"  - Folder docelowy: {sciezka_docelowa}\n")
            logging.info(f"Konfiguracja zaladowana: {liczba_plikow} plikow, zrodlo: {sciezka_zrodlowa}, cel: {sciezka_docelowa}")
            
            kopiuj_najnowsze_pliki(sciezka_zrodlowa, sciezka_docelowa, liczba_plikow)
            logging.info("Program zakonczyl sie pomyslnie")
        else:
            # Pokaż konsolę tylko gdy załadowanie konfiguracji się nie powiodło
            pokaz_konsole()
            komunikat = "Nie udalo sie wczytac konfiguracji."
            print(komunikat)
            logging.error(komunikat)
            input("\nNaciśnij Enter, aby zamknąć...")
    
    except Exception as e:
        pokaz_konsole()
        print(f"BŁĄD: {e}")
        logging.error(f"Nieoczekiwany błąd: {e}", exc_info=True)
        input("\nNaciśnij Enter, aby zamknąć...")
