import logging
import logging.config


class Persist:
    logging.config.fileConfig("resources/configs/logging.conf")

    def __init__(self, spark):
        self.spark = spark

    def persist_data(self, df):
        try:
            logger = logging.getLogger("Persist")
            logger.info('Persisting')
            logger.error("dummy error in Persisting")
            df.coalesce(1).write.option("header", "true").csv("transformed_retailstore")  # data is stored in Hive table
        except Exception as e:
            logger.error("An error occured while persisting data > " + str(e))
            raise Exception(
                "HDFS directory already exists")  # if occurs it is raised here and executed in data_pipeline.py
