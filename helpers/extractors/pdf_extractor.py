class PDFHandler(FileHandler):
    def __init__(self, destination):
        self._destination = destination

    def process(self, input):
        # read PDF file
        # uncomment if you want to pass pdf file from command line arguments
        tables = tabula.read_pdf(input.split("/")[1], pages="all")
        print(tables)
        # save them in a folder
        folder_name = self._destination.split("/")[1]
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        # iterate over extracted tables and export as excel individually
        for i, table in enumerate(tables, start=1):
            table.to_excel(os.path.join(folder_name, f"table_{i}.xlsx"), index=False)

        # convert all tables of a PDF file into a single CSV file
        # supported output_formats are "csv", "json" or "tsv"
        tabula.convert_into(input.split("/")[1], "output.csv", output_format="csv", pages="all")
        # convert all PDFs in a folder into CSV format
        # `pdfs` folder should exist in the current directory
        tabula.convert_into_by_batch("pdfs", output_format="csv", pages="all")


class BizfindBot:  # ten obiekt jest tworzony przy ładowaniu pluginów
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
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        main(logger=myLogger, target_path=target_path, base_url=self.url, start_page=start_page, end_page=end_page)

        logging.shutdown()
        # -------------------------------------------------------------------------
        # login = driver.find_element_by_name('UserName').send_keys("name")
        # pwd = driver.find_element_by_name('Password').send_keys("password")
        # submit = driver.find_element_by_class_name('button').click()

        # myLogger.setLevel(logging.INFO)
        # myLogger.debug("debug")
        # myLogger.info("informuje")
        # myLogger.warning("ostrzeżenie")
        # myLogger.error("error")
        # myLogger.critical("critical")


# def register() -> None:
#     factory.register("bizfind", BizfindBot)


if __name__ == "__main__":
    ob = BizfindBot()
    ob.scrape()