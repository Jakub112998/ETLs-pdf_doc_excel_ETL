import logging
import logging.config
import pandas as pd
from datetime import datetime
from enum import Enum
# from PIL import Image
import argparse
import os
# import pytesseract
import shutil
import tabula
import os
from . import loader
from abc import ABC, abstractmethod
import json





class Ingest:
    logging.config.fileConfig("resources/configs/logging.conf")  # by użyć tego pliku w innych

    # logach (z innych klas, deklaruję to jako zmienną klasy
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file  # przekazujemy spark session do ingest.py

    def ingest_data(self):
        logger = logging.getLogger("Ingest")  # definiujemy którego loggera używam w tej klasie
        logger.info("Ingesting from a file")

        with open("helpers/resources/configs/level.json") as file:
            data = json.load(file)
            # industry_data = data[industry]
            # load the plugins
            # loader.load_plugins(industry_data["plugins"])

            # create the characters
            sources = [factory.create(item) for item in industry_data["sources"]]

            # do something with the characters
            for source in sources:
                # source = obiekt
                # scrape = metoda
                source.scrape()

        # df = pd.DataFrame()
        # detect format
        # handler = FileHandler(is_jpg(self.input_file), JPEGHandler(self.output_file))
        # handler = FileHandler(is_pdf, PDFHandler(self.output_file))
        # handler(self.input_file, handler)
        # read file
        # - what you can read easily - put into df
        # - everything else put into .h5 file

        logger.info("DF created")
        logger.warning("DF created with warning")
        # return customer_df
        return df
