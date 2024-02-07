import os
import subprocess
import sys
import platform

if platform.system() != 'Darwin':
    raise SystemError('Ten skrypt musi być uruchomiony na systemie MacOS')

def zainstaluj_biblioteki():
    # Ścieżka do pliku requirements.txt
    requirements_txt = "program_files/requirements.txt"

    # Sprawdź, czy plik requirements.txt istnieje
    if os.path.exists(requirements_txt):
        # Wykonaj komendę pip install
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_txt])
    else:
        print(f"Plik {requirements_txt} nie istnieje.")

if __name__ == "__main__":
    zainstaluj_biblioteki()

    # Importuj moduł main
    import main
    main


