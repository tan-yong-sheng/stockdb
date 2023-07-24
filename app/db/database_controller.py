import os
import logging
from dotenv import load_dotenv, find_dotenv
import sqlalchemy
from sqlmodel import SQLModel, create_engine, Session
import pandas as pd
import numpy as np
from app.decorators import log_start_end
from app.db.stocks.stock_model import (get_company_info, 
                                        get_stock_price,
                                        get_fundamentals_data,
                                        get_news
                                        )
from .models import (MasterSQLModel,
                     CompanyDB,
                     PriceDB,
                     FundamentalsDB,
                     NewsDB,
                     NullDB)


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
def insert_db(sql_model: MasterSQLModel = NullDB, 
              data_frame: pd.DataFrame=pd.DataFrame(), engine=None):
    if engine is None:
        engine = create_engine(DATABASE_URI, echo=True)
    # remove null values in the dictionary
    result_list = [{k: v for k, v in row.items() if v is not None} for row in \
        data_frame.replace(np.nan, None).reset_index().to_dict("records")]
    #Convert a pandas DataFrame into a a list of SQLModel objects.
    sql_model_objs = [sql_model(**row) for row in result_list]

    with Session(engine) as session:
        for obj in sql_model_objs:
            session.add(obj)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError as error:
                # logging here
                session.rollback()

def main():
    create_db_and_tables()
    
    insert_db(CompanyDB, get_company_info())

    stock_price_df = get_stock_price("MSFT GOOGL")
    insert_db(PriceDB, stock_price_df)
    
    #news_df = pd.read_csv("./tests/csv_sample_output/newsdb.csv")
    news_df = get_news("TSLA") # question: why set to PLTR, it breaks?
    insert_db(NewsDB, news_df)

    
    fundamentals_data_df=get_fundamentals_data("MSFT AAPL GOOGL NVDA TSLA")
    #fundamentals_data_df.to_csv("./tests/csv_sample_output/fundamentalsdatadb.csv")
    insert_db(FundamentalsDB, fundamentals_data_df)


if __name__ == "__main__":
    from app.loggers import setup_logging
    setup_logging()
    main()
