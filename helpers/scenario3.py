import logging
import os
import datetime
from task.helpers import factory
import xlrd
from dataclasses import dataclass
from plugins import load_to_postgres
from task.helpers.base import SourceManager


def main(logger, target_path):
    load_to_postgres.load()


@dataclass
class Scenario3(SourceManager):  # ten obiekt jest tworzony przy ładowaniu pluginów
    name: str = ''  # parametr z jsona

    def transform(self, industry="automation", start_page=1, end_page=2) -> None:
        now = datetime.datetime.now()
        scrape_date = f"{now.year}-{now.month}-{now.day}"

        # z env variables:
        self.name = "biznesfinder"
        parent_dir = "D:/PyCharm_projects/DataEngineering/PROJEKTY/ProjektDlaTaty_v_final/data/"

        directory = f"{scrape_date}/{industry}/{self.name}/"
        target_path = parent_dir + directory

        logging.config.fileConfig(parent_dir + "logging.conf")
        myLogger = logging.getLogger('simpleExample')
        fh = logging.FileHandler(parent_dir + 'scraping_history.logs')
        myLogger.addHandler(fh)

        # check_if_page_range_was_already_scraped(logger=myLogger, start_page=start_page, end_page=end_page)

        if not os.path.exists(target_path):
            os.makedirs(target_path)
        main(logger=myLogger, target_path=target_path)

        logging.shutdown()


def register() -> None:
    factory.register("3", Scenario3)