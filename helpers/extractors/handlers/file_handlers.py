from abc import ABC, abstractmethod
import pandas as pd

# pdf
import pytesseract
import shutil
import tabula
# https://geekyhumans.com/de/how-to-extract-text-and-images-from-pdf-using-python/

# xlsx
import xlrd


class PDFExtractor():
    def __init__(self, destination):
        self._destination = destination
        pass

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
        # self._extract_text()


#                     for COL_IDX in range(len(row)):
#                         c = first_sheet.cell(row, COL_IDX)
#                         print(c)
#                         xf = book.xf_list[c.xf_index]
#                         print(xf)
#
# text_cell = first_sheet.cell_value(row_idx, COL_IDX)
# text_cell_xf = book.xf_list[first_sheet.cell_xf_index(row_idx, COL_IDX)]
# print(text_cell)
# if not text_cell:
#     continue
# text_cell_runlist = first_sheet.rich_text_runlist_map.get((row_idx, COL_IDX))
# if text_cell_runlist:
#     print('(cell multi style) SEGMENTS:')
# segments = []
# for segment_idx in range(len(text_cell_runlist)):
#     start = text_cell_runlist[segment_idx][0]
#     the last segment starts at given 'start' and ends at the end of the string
# end = None
# if segment_idx != len(text_cell_runlist) - 1:
#     end = text_cell_runlist[segment_idx + 1][0]
# segment_text = text_cell[start:end]
# segments.append({
#     'text': segment_text,
#     'font': book.font_list[text_cell_runlist[segment_idx][1]]
# })
# segments did not start at beginning, assume cell starts with text styled as the cell
# if text_cell_runlist[0][0] != 0:
#     segments.insert(0, {
#         'text': text_cell[:text_cell_runlist[0][0]],
#         'font': book.font_list[text_cell_xf.font_index]
#     })
# for segment in segments:
#     print(segment['text'])
#     print('italic:', segment['font'].italic)
#     print('size:', segment['font'].size)
#     print('bold:', segment['font'].bold)
# else:
#     print('(cell single style)')
#     print('italic:', book.font_list[text_cell_xf.font_index].italic)
#     print('size:', book.font_list[text_cell_xf.font_index].size)
#     print('bold:', book.font_list[text_cell_xf.font_index].bold)
# """

class XLSXExtractor():
    def __init__(self, destination):
        self._destination = destination
        pass

    def _extract_text(self):
        pass

    def _extract_tables(self) -> bool:
        # rozpoznanie początku tabeli, zwykle jako:
        # wiersz z tabelą zaczyna się liczbą 1.0, zwykle powyżej jest "Lp." - wiersz gdzie jest Lp,
        # wypełniony jest danymi dekstowymi w komórkach
        pass

    def _extract_images(self):
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


if __name__ == '__main__':
    # ext = PDFExtractor("")
    # ext.process()
    ext = XLSXExtractor(
        "D:/PyCharm_projects/DataEngineering/WEB_DEVELOPMENT/PROJEKTY_WEJŚCIOWE_DO_PRACY/HTA-consulting/task/data/in/"
        # "0070-19%20zmienione%203%2c%205%2c%208%2c%209%20i%20nowy%20p.%2012%20formularz%20cenowy_e467b2d3c6d0a01f0a7a7d81aee8c11c5690c4547b7304dfaafb1cabdaa2df4e.xlsx"
        # "04. załącznik nr 1a do swz - formularz cenowy_.xlsx"
        "03_formularz cenowy_647d60f3d047864138da4377746cd23f7c2013276a80eabfe715a847fc3f5099.xls"
    )
    ext.process()
    print(__package__)
