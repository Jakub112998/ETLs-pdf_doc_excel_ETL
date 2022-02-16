import argparse
import sys

import h5py
import ingest
import transform
import persist
import logging
import logging.config  # i teraz nie stusujemy już

from pathlib import Path

DATA_DIR = Path(__file__).parent / "../data/in/"  # stores directory of our data files


class Pipeline:
    logging.config.fileConfig("resources/configs/logging.conf")

    def run_pipeline(self):
        try:
            logging.info('run_pipeline')  # dobrą praktyką jest drukowanie początku i końca każdej metody
            ingest_process = ingest.Ingest(self.file)
            df = ingest_process.ingest_data()
            df.show()
            tranform_process = transform.Transform(self.file)
            transformed_df = tranform_process.transform_data(df)
            transformed_df.show()
            persist_process = persist.Persist(self.file)
            persist_process.persist_data(transformed_df)
            logging.info('run_pipeline method ended')
        except Exception as e:  # whatever error is raised inside methods
            # it is called here
            logging.error("An error occured while running the pipeline > " + str(e))
            # to wydrukowało An error occured while running the pipeline > HDFS directory already exists,
            # czyli wygrukowało przy raise Error w persist.py
            # send email
            # log error to database
            sys.exit(1)
        return

    def collect_files(self, pattern):  # string pattern we want to search for
        """
        W zależności czy podany został plik w formacie:
         - xxx.xlsx czy, -> procesowany jest tylko ten plik
         - .xlsx  -> procesowane są wszystkie pliki w ścieżce danych
        """
        # DATA_DIR.glob(pattern)  # search for this pattern in data directory
        # glob() returns generator
        self.list_files = list(DATA_DIR.glob(pattern))
        return self.list_files

    def file_format_standarization(self, output_file):
        """
        Funkcja działa na pliku xxx.xlsx
        Wrzucam tutaj całą informację spoza tabel z tego konkretnego pliku.
        todo: przypadki gdy nie ma nagłówków (przykład plik yyy.xlsx)
        todo: przypadki gdy tabele w różnych arkuszach (przykład w plik zzz.xlsx)
        todo: przypadki gdy ... można pewnie tego sporo wymieniać, bo każdy plik ma swoje "ale"
        """
        with h5py.File(output_file, "a") as f:
            self.file = f


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inbox", help="Folder to watch for new images")
    parser.add_argument("outbox", help="Folder for processed images")
    args = parser.parse_args()

    print(f"Processing {args.inbox} for file; sending results to {args.outbox}")

    logging.debug('Debugging the Application ')
    pipeline = Pipeline()
    pipeline.collect_files(args.inbox)

    while True:
        try:
            file = next(pipeline.list_files)
            pipeline.file_format_standarization(args.outbox+f"/{file}")
            logging.info(f'Common format created for {file}')
            pipeline.run_pipeline()
        except StopIteration:
            break
    logging.info('Pipeline executed')
