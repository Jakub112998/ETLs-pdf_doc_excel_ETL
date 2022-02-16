import logging
import logging.config


class Transform:
    logging.config.fileConfig("resources/configs/logging.conf")

    def __init__(self, file):
        self.file = file

    def transform_data(self, df):
        logger = logging.getLogger("Transform")
        logger.info("Transforming")
        logger.warning("Warning in Transforming")

        # drop all the rows having null values
        return df
