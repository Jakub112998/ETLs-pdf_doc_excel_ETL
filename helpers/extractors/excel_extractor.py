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