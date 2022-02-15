import pyspark
from pyspark.sql import SparkSession

import logging
import logging.config

import argparse
import pathlib


def process_document(document_path: pathlib.Path) -> None:
    print(type(document_path))
    print(document_path)


def get_absolute_path(path: str) -> pathlib.Path:
    return pathlib.Path(path).absolute()


def get_parser() -> argparse.ArgumentParser:
    _parser = argparse.ArgumentParser(description="Simple Argument Parser")
    _parser.add_argument(
        "document_path",
        type=get_absolute_path,
    )

    return _parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    process_document(args.document_path)


class Transform:
    logging.config.fileConfig("resources/configs/logging.conf")

    def __init__(self, spark):
        self.spark = spark

    def transform_data(self, df):
        logger = logging.getLogger("Transform")
        logger.info("Transforming")
        logger.warning("Warning in Transforming")

        # drop all the rows having null values
        df1 = df.na.drop()
        return df1
