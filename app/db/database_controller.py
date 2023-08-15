import os
import numpy
import pandas
import logging
from dotenv import load_dotenv, find_dotenv
import sqlalchemy
import polars
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.future.engine import Engine
from typing import Optional
from tqdm import tqdm

from app.decorators import log_start_end
from app.db.stocks.stock_model import (
    get_company_info,
    get_price,
    get_news,
)


from app.db.macro.macro_model import (
    get_economic_calendar,
    get_countries,
    get_macro_parameters,
    get_macro_indicators_data,
)

from app.db.models import (
    CountriesDB,
    CompaniesDB,
    DailyPriceDB,
    OneMinPriceDB,
    NewsDB,
    DataVendorDB,
    NullDB,
)

_ = load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

DATABASE_URI = os.getenv("DATABASE_URI", None)
# set echo=True to view output


######################### CREATE DATABASE #################################
@log_start_end(log=logger)
def create_db_and_tables(engine=None):
    if engine is None:
        engine = create_engine(DATABASE_URI, echo=True)
    SQLModel.metadata.create_all(engine)


############################# INSERT DATA #################################
# Reference: https://sqlmodel.tiangolo.com/tutorial/insert/
"""
@log_start_end(log=logger)
def insert_db(
    sql_model: SQLModel = NullDB,
    data_frame: pandas.DataFrame = pandas.DataFrame(),
    engine: Optional[Engine]=None,
):
    if engine is None:
        engine = create_engine(DATABASE_URI, echo=True)
    # remove null values in the dictionary
    if isinstance(data_frame, pandas.DataFrame):
        result_list = [
            {k: v for k, v in row.items() if v is not None or not numpy.NaN()}
            for row in tqdm(data_frame.reset_index().to_dict("records"))
        ]
        # Convert a pandas DataFrame into a a list of SQLModel objects.
        sql_model_objs = [sql_model(**row) for row in tqdm(result_list)]
        
        if len(sql_model_objs) > 1:
            with Session(engine) as session:
                for obj in sql_model_objs:
                    session.add(obj)
                    try:
                        session.commit()
                    except sqlalchemy.exc.IntegrityError as error:
                        session.rollback()
    else:
        raise ValueError("=============== The data type is wrong===========")
"""

@log_start_end(log=logger)
def insert_db(
    data_frame: pandas.DataFrame = pandas.DataFrame(),
    table_name: str = SQLModel.__tablename__,
    #sql_model: SQLModel = NullDB,
    connection: str = DATABASE_URI,
    if_exists: str = "append",
    #engine: str ="sqlalchemy",
):
    polars.from_pandas(data_frame).write_database(
                      table_name=table_name, 
                      conectionn=connection,
                      if_exists=if_exists)


def run_db_operation(engine=None):
    if engine is None:
        engine = create_engine(DATABASE_URI, echo=True)

    create_db_and_tables(engine=engine)

    #companies_info = get_company_info(exchange="NYQ")
    #insert_db(CountriesDB, get_countries(), engine=engine)
    #insert_db(CompaniesDB, companies_info, engine=engine)

    #data_vendor_df = pandas.read_csv("app/db/input/data_vendor.csv")
    #print(data_vendor_df)
    #insert_db(DataVendorDB,data_vendor_df,engine=engine)

    daily_stock_price_df = get_price("AAPL MSFT GOOGL PLTR", 
                                     data_source="yahoo finance")
    print(daily_stock_price_df)
    insert_db(daily_stock_price_df, table_name=DailyPriceDB.__tablename__)

    # get stock price
    """
    tickers = " ".join(companies_info["symbol"].tolist())
    daily_stock_price_df = get_price(tickers, data_source="yahoo finance")
    insert_db(DailyPriceDB, daily_stock_price_df, engine=engine)
    
    intraday_stock_price_df = get_price(tickers, interval="1m", data_source="yahoo finance")
    insert_db(OneMinPriceDB, intraday_stock_price_df, engine=engine)
    
    daily_stock_price_df_fmp = get_price(tickers, data_source="financial modeling prep")
    insert_db(DailyPriceDB, daily_stock_price_df_fmp, engine=engine)
    
    intraday_stock_price_df_fmp = get_price(tickers, interval="1m", data_source="financial modeling prep")
    insert_db(OneMinPriceDB, intraday_stock_price_df_fmp, engine=engine)

    # get news
    # news_df = pandas.read_csv("./tests/csv_sample_output/newsdb.csv")
    # news_df = get_news("TSLA") # question: why set to PLTR, it breaks?
    # insert_db(NewsDB, news_df)
    """

if __name__ == "__main__":
    from app.loggers import setup_logging
    engine = create_engine(DATABASE_URI, echo=True)
    setup_logging()
    run_db_operation(engine=engine)
