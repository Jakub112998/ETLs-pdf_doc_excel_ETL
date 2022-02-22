from task.helpers.resources import db_helper
import argparse
import asyncio
import logging

from sqlalchemy import TIMESTAMP, Boolean, Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Sequence

from src.services.universal_scraper.helpers import sql_queries
from src.services.universal_scraper.helpers import db_helper

LOG = logging.getLogger(__name__)

Base = declarative_base()


async def load(zip_file_path=""):
    """ data quality and load to model """
    engine = db_helper.make_engine(section="docker")

    db_helper.set_session(engine)
    # drop_views(args)
    # drop_tables(args)

    LOG.warning("CREATING DEFINED TABLES")
    # recreate tables
    # Base.metadata.create_all(engine)
    # create_views(args)


