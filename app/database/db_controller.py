import os
import numpy
import pandas
import logging
import sqlalchemy
from app.database.setup_db_environment import ENGINE

# from sqlmodel import SQLModel, create_engine, Session
from typing import Optional
from tqdm import tqdm
from datetime import datetime
from app.decorators import log_start_end
from app.database.stocks.downloader_model.FDData import (
    get_company_info,
    get_price,
    get_news,
)
#from app.database.macro.macro_model import (
#    get_economic_calendar,
#    get_countries,
#    get_macro_parameters,
#    get_macro_indicators_data,
#) # don't want use openbb
from app.database.stocks.db_model.security_model import (
    SecurityPriceDB,
    CompanyDB,
    DataVendorDB,
)
from app.database.stocks.db_model.security_model import Base
from app.database.setup_db_environment import (create_db_and_tables, 
                                               insert_db, 
                                               ENGINE)


logger = logging.getLogger(__name__)

############################# INSERT DATA #################################
# Reference: https://sqlmodel.tiangolo.com/tutorial/insert/
"""
@log_start_end(log=logger)
def insert_db(
    data_frame: pandas.DataFrame = pandas.DataFrame(),
    engine: Optional[ENGINE]=None,
):
    if engine is None:
        engine = ENGINE
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

@log_start_end(log=logger)
def insert_db(
    data_frame: pandas.DataFrame = pandas.DataFrame(),
    sql_model: str = None,
    if_exists: str = "append",
    chunksize: str = 1000,
    index=False,
    method="multi",
):
    if sql_model == None:
        raise Exception(
            "Please choose any sql class model to\
            input your data"
        )
    
    data_frame["created_at"] = datetime.utcnow()
    data_frame["updated_at"] = datetime.utcnow()
    data_frame.to_sql(
        name=sql_model.__tablename__,
        con=ENGINE,
        if_exists=if_exists,
        index=index,
        chunksize=chunksize,
        method=method,
    )
"""



def run_db_operation(engine=None):
    create_db_and_tables(engine=ENGINE)

    companies_info = get_company_info(exchange="NYQ")[:10]
    # insert_db(CountriesDB, get_countries(), engine=engine)
    # insert_db(CompanyDB, companies_info, engine=engine)

    # data_vendor_df = pandas.read_csv("app/db/input/data_vendor.csv")
    # print(data_vendor_df)
    # insert_db(DataVendorDB,data_vendor_df,engine=engine)

    daily_stock_price_df = get_price(companies_info["symbol"].tolist(),
                                     data_source="yahoo finance")
    for daily_price in daily_stock_price_df:
        insert_db(daily_price, sql_model=SecurityPriceDB)

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
    setup_logging()
    run_db_operation(engine=ENGINE)
