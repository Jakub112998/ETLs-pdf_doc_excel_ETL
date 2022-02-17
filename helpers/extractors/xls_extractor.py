import logging
import os
import datetime
from .. import factory
import xlrd


class XLSXExtractor():
    def __init__(self, destination):
        self._destination = destination
        pass

    def process(self):
        book = xlrd.open_workbook(self._destination, formatting_info=True)
        # for el in book.font_list:
        #     print(el)
        for idx in range(len(book.sheets())):
            first_sheet = book.sheet_by_index(idx)
            df_building = False
            df = pd.DataFrame
            columns = []
            file_object = open(f"{first_sheet.name}_{idx}.txt", 'a')
            for row_idx in range(first_sheet.nrows):
                row = first_sheet.row(row_idx)
                if 'text' or 'number' in str(row):
                    # print(str(row))
                    if all(x in 'text' for x in str(row)) or \
                            ('Lp.' in str(
                                row)) and not df_building:  # jeśli tekst jest we wszystkich komórkach w wierszu
                        columns = [x.value for x in row]
                        df = df(columns=columns)
                        print(df)
                        df_building = True
                        continue
                    if df_building and ('number' in str(row)):
                        data = {name: x.value for name, x in zip(columns, row)}
                        df = df.append(data, ignore_index=True)
                        continue
                    if df_building:
                        df.to_csv(f"{first_sheet.name}_{idx}_{row_idx}.csv", index=False, encoding="utf-8")
                        df_building = False
                    for el in row:
                        if str(el.value) is not None or str(el.value) is not '':
                            print(str(el.value))
                            file_object.write(str(el.value))
                            file_object.write("\n")
                df_building = False
            file_object.close()


def main(logger, target_path):
    industry = target_path.split("/")
    industry = industry[len(industry) - 2]
    data_source = industry[len(industry) - 1]

    with XLSXExtractor(destination=target_path) as handler:
        handler.process()


class XLSXBot:  # ten obiekt jest tworzony przy ładowaniu pluginów
    name: str = ''  # parametr z jsona
    url: str = ''  # parametr z jsona

    def scrape(self, industry="automation", start_page=1, end_page=2) -> None:
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
    factory.register("xlsx", XLSXBot)


if __name__ == "__main__":
    ext = XLSXExtractor(
        "D:/PyCharm_projects/DataEngineering/WEB_DEVELOPMENT/PROJEKTY_WEJŚCIOWE_DO_PRACY/HTA-consulting/task/data/in/"
        # "0070-19%20zmienione%203%2c%205%2c%208%2c%209%20i%20nowy%20p.%2012%20formularz%20cenowy_e467b2d3c6d0a01f0a7a7d81aee8c11c5690c4547b7304dfaafb1cabdaa2df4e.xlsx"
        # "04. załącznik nr 1a do swz - formularz cenowy_.xlsx"
        "03_formularz cenowy_647d60f3d047864138da4377746cd23f7c2013276a80eabfe715a847fc3f5099.xls"
    )
    ext.process()
