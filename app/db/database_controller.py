import os
import numpy
import pandas
import logging
from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlmodel import SQLModel, create_engine, Session

from app.decorators import log_start_end
from app.db.stocks.stock_model import (
    get_company_info,
    get_daily_price,
    get_fundamentals_data,
    get_news,
)

from app.db.macro.macro_model import (
    get_economic_calendar,
    get_countries,
    get_macro_parameters,
    get_macro_indicators_data
)

from app.db.models import (
    CountriesDB,    
    CompaniesDB,
    DailyPriceDB,
    FundamentalsDB,
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

@log_start_end(log=logger)
def insert_db(sql_model: SQLModel = NullDB, 
              data_frame: pandas.DataFrame=pandas.DataFrame(), engine=None):
    if engine is None:
        engine = create_engine(DATABASE_URI, echo=True)
    # remove null values in the dictionary
    if isinstance(data_frame, pandas.DataFrame):
        result_list = [{k: v for k, v in row.items() if v is not None or not numpy.nan} for row in \
            data_frame.reset_index().to_dict("records")]
        #Convert a pandas DataFrame into a a list of SQLModel objects.
        sql_model_objs = [sql_model(**row) for row in result_list]

        with Session(engine) as session:
            for obj in sql_model_objs:
                session.add(obj)
                try:
                    session.commit()
                except sqlalchemy.exc.IntegrityError as error:
                    session.rollback()
    else:
        print(data_frame)
        raise ValueError("=============== The data type is wrong===========")     

def run_db_operation(engine=None):
    if engine is None:
        engine = create_engine(DATABASE_URI, echo=True)
    create_db_and_tables(engine=engine)
    
    #insert_db(CountriesDB, get_countries(), engine=engine)
    
    #insert_db(CompaniesDB, get_company_info(exchange="NYQ"), engine=engine)

    data_vendor_df = pandas.read_csv("app/db/input/data_vendor.csv")
    # print(data_vendor_df)
    print(data_vendor_df)
    insert_db(DataVendorDB,data_vendor_df,engine=engine)

    #get stock price
    #tickers = " ".join(get_company_info()["symbol"].tolist())
    stock_price_df = get_daily_price("AAPL AAIC AAC")
    print(stock_price_df)
    insert_db(DailyPriceDB, stock_price_df, engine=engine)


    # get news
    # news_df = pandas.read_csv("./tests/csv_sample_output/newsdb.csv")
    # news_df = get_news("TSLA") # question: why set to PLTR, it breaks?
    # insert_db(NewsDB, news_df)

    # get fundamentals data
    # fundamentals_data_df=get_fundamentals_data("MSFT AAPL GOOGL NVDA TSLA")
    # fundamentals_data_df.to_csv("./tests/csv_sample_output/fundamentalsdatadb.csv")
    # insert_db(FundamentalsDB, fundamentals_data_df)

if __name__ == "__main__":
    from app.loggers import setup_logging
    engine = create_engine(DATABASE_URI, echo=True)

    setup_logging()
    run_db_operation(engine=engine)
