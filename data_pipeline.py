import sys
import ingest
import transform
import persist
import logging
import logging.config  # i teraz nie stusujemy już

class Pipeline:
    logging.config.fileConfig("resources/configs/logging.conf")

    def run_pipeline(self):
        try:
            logging.info('run_pipeline')  # dobrą praktyką jest drukowanie początku i końca każdej metody
            ingest_process = ingest.Ingest(self.spark)
            df = ingest_process.ingest_data()
            df.show()
            tranform_process = transform.Transform(self.spark)
            transformed_df = tranform_process.transform_data(df)
            transformed_df.show()
            persist_process = persist.Persist(self.spark)
            persist_process.persist_data(transformed_df)
            logging.info('run_pipeline method ended')
        except Exception as e: # whatever error is raised inside methods
            # it is called here
            logging.error("An error occured while running the pipeline > " + str(e))
            # to wydrukowało An error occured while running the pipeline > HDFS directory already exists,
            # czyli wygrukowało przy raise Error w persist.py
            # send email
            # log error to database
            sys.exit(1)
        return

    def create_common_format(self):
        """
        Funkcja działa na pliku xxx.xlsx
        todo: przypadki gdy nie ma nagłówków (przykład plik yyy.xlsx)
        todo: przypadki gdy tabele w różnych arkuszach (przykład w plik zzz.xlsx)
        todo: przypadki gdy ... można pewnie tego sporo wymieniać, bo każdy plik ma swoje "ale"
        """


if __name__ == "__main__":
    logging.debug('Debugging the Application ')
    pipeline = Pipeline()
    pipeline.create_common_format()
    logging.info('Common format created')
    pipeline.run_pipeline()
    logging.info('Pipeline executed')
