import os
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent / "results"

class BasePathManager:
    """
    Klasa odpowiada za sprowadzenie pliku w formacie XLSX do wspólnego formatu
    składającego się z pliku .csv oraz pliku .txt
    - plik .csv zawierającego 1 tabelę
    - plik .txt zawierającego pozostały tekst spoza tabeli

    Wszystkie pliki związane z ekstrachowanym plikiem .xslx znajdują się w jednym folderze o nazwie:
    - dzien-miesiac-rok-godzina-minuta_nazwa-ekstrachowanego-pliku
    """

    def __init__(self, destination=""):
        self.destination = DATA_DIR
        if destination != "":
            self.destination = destination
        base_destination = destination.split("\\")
        base_destination = "".join(map(str, base_destination[:-1]))

        self._folder_name = time.strftime("%Y%m%d-%H%M%S")
        self.base_path = base_destination + "/" + self._folder_name
        self._build_folder_structure()

    def _build_folder_structure(self) -> None:
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

