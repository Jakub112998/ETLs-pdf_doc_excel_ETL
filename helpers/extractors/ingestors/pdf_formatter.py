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