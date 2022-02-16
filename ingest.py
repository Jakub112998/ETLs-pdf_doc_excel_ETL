import logging
import logging.config

from datetime import datetime
from enum import Enum
from PIL import Image
import argparse
import inotify.adapters
import os
import pytesseract
import shutil


class FileState(Enum):
    CREATED = 1
    MODIFIED = 2
    CLOSED = 3


class FileHandler:
    """
	Event handler which maintains a state machine for each path
	seen. When a file goes through the create, write, close sequence,
	notifies the created handler.
	"""

    def __init__(self, filter, created_handler):
        self._files = {}
        self._filter = filter
        self._created_handler = created_handler

    def __call__(self, event, path):
        if ('IN_CREATE' in event or 'IN_OPEN' in event) and self._filter(path):
            self._files[path] = FileState.CREATED
        elif 'IN_MODIFY' in event and self._files.get(path) == FileState.CREATED:
            self._files[path] = FileState.MODIFIED
        elif 'IN_CLOSE_WRITE' in event or 'IN_CLOSE_NOWRITE' in event:
            if self._files.get(path) == FileState.MODIFIED:
                self._created_handler(path)
            if path in self._files:
                del self._files[path]


class JPEGHandler:
    """Handler for the creation of a new JPEG"""

    def __init__(self, destination):
        self._destination = destination

    def _add_suffix(self, path, suffix):
        name = path + "" if not suffix else f"_{suffix}"
        return os.path.join(self._destination, name)

    def _unique_dest(self):
        base = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        suffix = 0
        while os.path.exists(self._add_suffix(base, suffix)):
            suffix += 1
        return self._add_suffix(base, suffix)

    def __call__(self, path):
        print(f"Processing {path}")
        try:
            dest = self._unique_dest()
            pdf = pytesseract.image_to_pdf_or_hocr(Image.open(path), extension='pdf')
            with open(f"{dest}.pdf", 'wb') as f:
                f.write(pdf)
            shutil.move(path, f"{dest}.jpg")
        except Exception as e:
            print(e)


def is_jpg(path):
    """Determine if a file path is a JPEG"""
    ext = os.path.splitext(path)[1]
    return ext.lower() in [".jpg", ".jpeg"]


class Ingest:
    logging.config.fileConfig("resources/configs/logging.conf")  # by użyć tego pliku w innych

    # logach (z innych klas, deklaruję to jako zmienną klasy
    def __init__(self, file):
        self.file = file  # przekazujemy spark session do ingest.py

    def ingest_data(self):
        logger = logging.getLogger("Ingest")  # definiujemy którego loggera używam w tej klasie
        logger.info("Ingesting from csv")
        # detect format
        handler = FileHandler(is_jpg, JPEGHandler(args.outbox))
        # read file
        # - what you can read easily - put into df
        # - everything else put into .h5 file
        logger.info("DF created")
        logger.warning("DF created with warning")
        # return customer_df
        return course_df
