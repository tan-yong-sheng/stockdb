import os
from dotenv import load_dotenv, find_dotenv
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from sqlalchemy.sql.functions import func
from sqlalchemy.types import (
    TIMESTAMP,
    BigInteger,
    Float,
)
import pandas
from typing_extensions import Annotated
from datetime import datetime
from app.decorators import log_start_end

_ = load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)
DATABASE_URI = os.getenv("DATABASE_URI", None)
# set echo=True to view output
ENGINE = create_engine(DATABASE_URI, echo=True)
SESSIONMAKER = sessionmaker(ENGINE)
SESSION = SESSIONMAKER()

# Creating a base class
class Base(DeclarativeBase):
    pass

# float column with double data type
float_double = Annotated[float, mapped_column(Float)]
# int column with BigInt data type
BigInt = Annotated[int, mapped_column("adj_volume", BigInteger)]

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

######################### CREATE DATABASE #################################
@log_start_end(log=logger)
def create_db_and_tables(engine=None):
    if engine is None:
        engine = ENGINE
    Base.metadata.create_all(engine)


####################### INSERT OPERATIONS - DATABASE #########################
@log_start_end(log=logger)
def insert_db(data_frame: pandas.DataFrame = pandas.DataFrame(), 
              engine=None):
    if engine is None:
        engine = ENGINE
    