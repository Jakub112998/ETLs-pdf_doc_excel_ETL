import os
import time
from pathlib import Path
from abc import abstractmethod, ABC
import os

DATA_DIR = Path(__file__).parent


class OutputManager(ABC):
    """
    Wszystkie pliki związane z ekstrachowanym plikiem .xslx znajdują się w jednym folderze o nazwie:
    - dzien-miesiac-rok-godzina-minuta-sekunda

    todo: add logs
    """

    def __init__(self, input_file=""):
        os.path.abspath(os.curdir)
        os.chdir("..")
        self.input = os.path.abspath(os.curdir) + input_file

        self._destination = os.path.abspath(os.curdir) + "/data/output/"
        self._destination = self._destination.replace("\\", "/")
        self._build_folder_structure()

    @abstractmethod
    def _build_folder_structure(self) -> None:
        pass


class BaseOutputManager(OutputManager):
    def __init__(self, input_file: str):
        super().__init__(input_file=input_file)

    def _build_folder_structure(self) -> None:
        self._folder_name = time.strftime("%Y%m%d-%H%M%S")
        self.base_path = self._destination + self._folder_name
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)


class CustomOutputManager(OutputManager):
    """
    Different path managers to store data in local / remote or on Hadoop cluster.
    """
    def __init__(self, input_file: str):
        super().__init__(input_file=input_file)

    def _build_folder_structure(self) -> None:
        pass
