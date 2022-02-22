import os
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent / "results"

class BasePathManager:
    """
    Wszystkie pliki związane z ekstrachowanym plikiem .xslx znajdują się w jednym folderze o nazwie:
    - dzien-miesiac-rok-godzina-minuta-sekunda

    todo: add logs
    """

    def __init__(self, destination=""):
        self.destination = DATA_DIR
        if destination != "":
            self.destination = destination
        base_destination = destination.split("\\")
        base_destination = "".join(map(str, base_destination[:-1]))

        self._folder_name = time.strftime("%Y%m%d-%H%M%S")
        self.base_path = "../data/output/" + self._folder_name
        self._build_folder_structure()

    def _build_folder_structure(self) -> None:
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

