import argparse
import os
import sys

import h5py
import ingest
import transform
import persist
import logging
import logging.config  # i teraz nie stusujemy już

from pathlib import Path

# DATA_DIR = Path(__file__).parent / "data/in"  # stores directory of our data files
DATA_DIR = "D:/PyCharm_projects/DataEngineering/WEB_DEVELOPMENT/PROJEKTY_WEJŚCIOWE_DO_PRACY/HTA-consulting/task/data/in"

class Pipeline:
    logging.config.fileConfig("resources/configs/logging.conf")
    count = 1

    def run_pipeline(self):
        try:
            logging.info('run_pipeline')  # dobrą praktyką jest drukowanie początku i końca każdej metody
            ingest_process = ingest.Ingest(self.input_file, self.output_file)
            df = ingest_process.ingest_data()
            tranform_process = transform.Transform(self.output_file)
            transformed_df = tranform_process.transform_data(df)
            persist_process = persist.Persist(self.output_file)
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
        # print(DATA_DIR)
        # self.gen_data = DATA_DIR.glob(pattern)
        # print(os.listdir(DATA_DIR))
        self.gen_data = (n for n in os.listdir(DATA_DIR))
        # print(self.gen_data)

    def file_format_standarization(self, output_file):
        """
        Funkcja działa na pliku xxx.xlsx
        Wrzucam tutaj całą informację spoza tabel z tego konkretnego pliku.
        todo: przypadki gdy nie ma nagłówków (przykład plik yyy.xlsx)
        todo: przypadki gdy tabele w różnych arkuszach (przykład w plik zzz.xlsx)
        todo: przypadki gdy ... można pewnie tego sporo wymieniać, bo każdy plik ma swoje "ale"
        """
        print("file_format_standarization")
        mapping_names = {
            output_file: "h5_"+str(self.count),
        }
        print(mapping_names)
        with h5py.File(output_file.split("/")[0]+"/h5_"+str(self.count)+".hdf5", "a") as f:
            self.count += 1
            self.output_file = f
            self.input_file = DATA_DIR+"/"+output_file.split("/")[1]


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
            print("***************************")
            file = next(pipeline.gen_data)
            # file = str(file).split("\\")[-1]
            assert type(file) == str
            assert "\\" not in file
            pipeline.file_format_standarization(args.outbox+f"/{file}")
            logging.info(f'Common format created for {file}')
            pipeline.run_pipeline()
            break
        except StopIteration:
            break
    logging.info('Pipeline executed')
