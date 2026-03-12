import os
import sys
import ctypes
from pathlib import Path
import logging

def wczytaj_konfiguracje(plik_cfg="cfg.txt"):
    """
    Wczytuje konfigurację z pliku cfg.txt.
    
    Returns:
        tuple: (liczba_plikow_do_pozostawienia, sciezka_folderu)
    """
    liczba_plikow = None
    sciezka = None
    
    # Określ katalog, w którym znajduje się plik wykonywalny
    if getattr(sys, 'frozen', False):
        # Jeśli program jest skompilowany do .exe (PyInstaller)
        katalog_programu = os.path.dirname(sys.executable)
    else:
        # Jeśli uruchamiany jest jako skrypt Python
        katalog_programu = os.path.dirname(os.path.abspath(__file__))
    
    # Utwórz pełną ścieżkę do pliku cfg.txt
    sciezka_cfg = os.path.join(katalog_programu, plik_cfg)
    
    try:
        with open(sciezka_cfg, 'r', encoding='utf-8') as f:
            for linia in f:
                linia = linia.strip()
                
                if linia.startswith("Number of files"):
                    # Wydobądź liczbę z linii "Number of files = 5" lub "Number of files = "5""
                    liczba_plikow = int(linia.split("=")[1].strip().strip('"'))
                
                elif linia.startswith("Path:"):
                    # Wydobądź ścieżkę z linii 'Path: "C:\..."'
                    sciezka = linia.split(":", 1)[1].strip().strip('"')
        
        if liczba_plikow is None or sciezka is None:
            raise ValueError("Brak wymaganych danych w pliku konfiguracyjnym.")
        
        return liczba_plikow, sciezka
    
    except FileNotFoundError:
        print(f"Nie znaleziono pliku {sciezka_cfg}")
        print(f"Katalog programu: {katalog_programu}")
        return None, None
    except Exception as e:
        print(f"Błąd podczas wczytywania konfiguracji: {e}")
        return None, None


def usun_najstarsze_pliki(folder_path, liczba_plikow_do_pozostawienia):
    """
    Usuwa najstarsze pliki z folderu, pozostawiając określoną liczbę.
    
    Args:
        folder_path: Ścieżka do folderu
        liczba_plikow_do_pozostawienia: Liczba plików, która ma pozostać w folderze
    """
    try:
        folder = Path(folder_path)
        
        if not folder.exists() or not folder.is_dir():
            print(f"Folder {folder_path} nie istnieje lub nie jest folderem.")
            return
        
        # Pobierz wszystkie pliki (pomijając podfoldery)
        pliki = [f for f in folder.iterdir() if f.is_file()]
        
        if len(pliki) == 0:
            print("Folder jest pusty.")
            return
        
        print(f"Znaleziono {len(pliki)} plików w folderze.")
        print(f"Ma pozostać {liczba_plikow_do_pozostawienia} plików.")
        
        # Oblicz ile plików należy usunąć
        liczba_do_usuniecia = len(pliki) - liczba_plikow_do_pozostawienia
        
        if liczba_do_usuniecia <= 0:
            print(f"Nie trzeba usuwać plików. W folderze jest {len(pliki)} plików.")
            return
        
        # Posortuj pliki według czasu modyfikacji (najstarsze najpierw)
        pliki_posortowane = sorted(pliki, key=lambda x: x.stat().st_mtime)
        
        # Wybierz najstarsze pliki do usunięcia
        pliki_do_usuniecia = pliki_posortowane[:liczba_do_usuniecia]
        
        print(f"\nUsuwanie {len(pliki_do_usuniecia)} najstarszych plików:")
        
        for plik in pliki_do_usuniecia:
            print(f"  - {plik.name}")
            plik.unlink()  # Usuń plik
        
        print(f"\nUsunięto {len(pliki_do_usuniecia)} plików. W folderze pozostało {len(pliki) - len(pliki_do_usuniecia)} plików.")
        
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


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
        
        plik_logu = os.path.join(katalog_programu, "Memory_saver.log")
        logging.basicConfig(
            filename=plik_logu,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Program uruchomiony")
        
        # Wczytaj konfigurację z pliku cfg.txt
        liczba_plikow, sciezka_folderu = wczytaj_konfiguracje()
        
        if liczba_plikow is not None and sciezka_folderu is not None:
            print(f"Konfiguracja wczytana:")
            print(f"  - Liczba plików do pozostawienia: {liczba_plikow}")
            print(f"  - Ścieżka folderu: {sciezka_folderu}\n")
            logging.info(f"Konfiguracja zaladowana: {liczba_plikow} plikow, folder: {sciezka_folderu}")
            
            usun_najstarsze_pliki(sciezka_folderu, liczba_plikow)
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
