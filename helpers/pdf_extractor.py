import logging
import datetime
import os
from task.helpers import factory
import pytesseract
import shutil
import tabula
from task.helpers.base import BasePathManager

class PDFExtractor():
    def __init__(self, destination):
        super().__init__(destination)

    def _extract_text(self):
        # open the PDF file - extract text
        PDFfile = open(
            '/task/data/in/3_formularz_cenowy_pak16_8d2731ef55bad25ee24cb9add1eaf148c20bf0f6062db40652b50f8ce8d6c331.pdf',
            'rb')
        PDFfilereader = PyPDF2.PdfFileReader(PDFfile)
        # print(PDFfilereader.getDocumentInfo())
        f = PDFfilereader.getFields()
        # print(f.values())
        for value in f.values():
            print(type(value))
            for v in value.values():
                try:
                    print(v['/Contents'].rstrip('\x00'))
                    # print(v['/Contents'].decode('utf-8'))
                except Exception as e:
                    print(e)
                # print(v['/Contents'])
                # for z in v.values():
                #     print(z)
                # for y in z.values():
                #     print(y)
                # print(z['/Contents'])
        # print(PDFfilereader.getXmpMetadata())
        # print the number of pages
        # print(PDFfilereader.numPages)
        # provide the page number
        pages = PDFfilereader.getPage(1)
        # extracting the text in PDF file
        # print(pages.extractText())
        # close the PDF file
        PDFfile.close()

    def _extract_tables(self):
        # reading both table as an independent table
        tables = tabula.read_pdf(file, pages=1, multiple_tables=True)
        print(tables[0])
        print(tables[1])
        # iterate over extracted tables and export as excel individually
        for i, table in enumerate(tables, start=1):
            table.to_excel(os.path.join(folder_name, f"table_{i}.xlsx"), index=False)

    def _extract_images(self):
        # open the fitz file
        pdf = fitz.open(file)
        # select the page number
        image_list = pdf.getPageImageList(0)
        # applying the loop
        for image in image_list:
            xref = image[0]
            pix = fitz.Pixmap(pdf, xref)
            if pix.n < 5:
                pix.writePNG(f'{xref}.png')
            else:
                pix1 = fitz.open(fitz.csRGB, pix)
                pix1.writePNG(f'{xref}.png')
                pix1 = None
            pix = None
        # print the images
        print(len(image_list), 'detected')

    def process(self):
        print("PDF processing")


def main(logger, target_path, base_url, start_page, end_page):
    industry = target_path.split("/")
    industry = industry[len(industry) - 2]
    data_source = industry[len(industry) - 1]

    # https://selenium-python.readthedocs.io/locating-elements.html

    with PDFExtractor(destination=target_path) as handler:
        handler.process()
        # driver = handler.get_driver()
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # for page_number in range(start_page, end_page):  # zaczynać od 1
        #     try:
        #         logger.debug(f"{page_number} page of {industry} industry from {data_source} was scraped")
        #     except Exception as e:
        #         print(e)


if __name__ == "__main__":
    now = datetime.datetime.now()
    scrape_date = f"{now.year}-{now.month}-{now.day}"

    # z env variables:
    parent_dir = "D:/PyCharm_projects/DataEngineering/PROJEKTY/ProjektDlaTaty_v_final/data/"

    directory = f"{scrape_date}/{industry}/{self.name}/"
    target_path = parent_dir + directory

    logging.config.fileConfig(parent_dir + "logging.conf")
    myLogger = logging.getLogger('simpleExample')
    fh = logging.FileHandler(parent_dir + 'scraping_history.logs')
    myLogger.addHandler(fh)

    target_path = "/task/data/in/04. załącznik nr 1a do swz - formularz cenowy_.xlsx"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    main(logger=myLogger, target_path=target_path)
