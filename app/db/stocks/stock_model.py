""" stock_controller.py

This module provides functions for CRUD application, which includes 
extracting stock data, fundamentals data, and news data, as well as 
storing data into a MySQL database.

Functions:
- get_stock_price
- get_fundamentals_data
- get_news
- store_data_in_mysql
"""
import os
import logging
from typing import Union
from datetime import datetime
import yfinance as yf
import pandas as pd
from dateutil.relativedelta import relativedelta
import newsapi
from newsapi import NewsApiClient
import financedatabase as fd
from dotenv import load_dotenv, find_dotenv
from app.decorators import log_start_end, check_api_key

logger = logging.getLogger(__name__)

_ = load_dotenv(find_dotenv())
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY", None)
DATABASE_URI = os.getenv("DATABASE_URI", None)

############################# CREATE (OR FETCH) DATA #################################

## stock price query date
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - relativedelta(years=10)).strftime(
    "%Y-%m-%d"
)  # 10 years ago
# news query date
news_end_date = end_date
news_start_date = (datetime.now() - relativedelta(months=1)).strftime(
    "%Y-%m-%d"
)  # 1 month ago

@log_start_end(log=logger)
def get_company_info(
    country: str = "United States",
    sector: str="",
    industry_group: str = "",
    industry: str = "",
    exchange: str = "NYQ"

) -> pd.DataFrame: 
    eq = fd.Equities()
    equities_info: pd.DataFrame = eq.search(country=country,
                              sector=sector,
                              industry_group=industry_group,
                              industry=industry,
                              exchange=exchange
                              )
    return equities_info

@log_start_end(log=logger)
def get_stock_price(
    symbols: Union[str, list] = "MSFT",
    start: str = start_date,
    end: str = end_date,
    interval="1d",
) -> pd.DataFrame:
    """
    Extracts historical stock price data for the given stock symbols.

    Parameters:
        symbols (Union[list, str], optional): A list of stock symbols or
                                            a single symbol as a string.
                                            Defaults to "MSFT".
        start_date (str, optional): The start date in the format "YYYY-MM-DD".
                                    Defaults to 10 years ago from the current date.
        end_date (str, optional): The end date in the format "YYYY-MM-DD".
                                    Defaults to the current date.

    Returns:
        pd.DataFrame: A DataFrame containing historical stock price data with columns:
                       ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume'].
    """
    if isinstance(symbols, list):
        symbols = " ".join(symbols)
    stock_price = yf.download(symbols, start=start, end=end, interval="1d")
    if isinstance(symbols, str):
        if len(symbols.split(" ")) == 1:
            stock_price = stock_price.reset_index()
            stock_price["Symbol"] = symbols
            stock_price.set_index(["Date", "Symbol"], inplace=True)
            return stock_price
    stock_price = stock_price.stack()
    stock_price.index.names = ["Date", "Symbol"]
    return stock_price

@log_start_end(log=logger)
def get_fundamentals_data(symbols: Union[str, list] = "MSFT") -> pd.DataFrame:
    """
    Extracts fundamental data for the given stock symbols.

    Parameters:
        symbols (Union[list, str], optional): A list of stock symbols or
                                            a single symbol as a string.
                                            Defaults to "MSFT".
    Returns:
        pd.DataFrame: A DataFrame containing fundamental data for the
        given stock symbols.
    """
    fundamentals_data = pd.DataFrame()
    if isinstance(symbols, str):
        symbols = symbols.split(" ")
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        # normalize JSON / dict data into a flat table / dataframe
        info = pd.json_normalize(stock.info)
        fundamentals_data = pd.concat([fundamentals_data, info], ignore_index=True)
    #fundamentals_data = fundamentals_data.replace(np.nan, "empty")
    return fundamentals_data


@log_start_end(log=logger)
@check_api_key(["NEWSAPI_API_KEY"])
def get_news(
    symbols: Union[str, list] = "MSFT",
    api_key: str = NEWSAPI_API_KEY,
    start: str = news_start_date,
    end: str = news_end_date,
):
    """
    Extracts news data for the given stock symbols from the News API.

    Parameters:
        symbols (list, optional): A list of stock symbols. Defaults to "MSFT".
        api_key (str, optional): The API key for accessing the News API. Defaults to
                                  the value from the environment variable
                                  "NEWSAPI_API_KEY".
        start_date (str, optional): The start date in the format "YYYY-MM-DD".
                                    Defaults to 10 years ago from the current date.
        end_date (str, optional): The end date in the format "YYYY-MM-DD".
                                  Defaults to the current date.
    Returns:
        pd.DataFrame: A DataFrame containing news data for the given stock symbols.
    """
    news_api: str = NewsApiClient(api_key=api_key)
    if isinstance(symbols, str):
        symbols = symbols.split(" ")
    news_data = pd.DataFrame()
    for symbol in symbols:
        try:
            news = news_api.get_everything(
                q=symbol, language="en", from_param=start, to=end, sort_by="relevancy"
            )
        except newsapi.newsapi_exception.NewsAPIException as error:
            raise error
        news = pd.json_normalize(news)["articles"]
        news = pd.json_normalize(news.explode())
        news["Symbol"] = symbol
        news_data = pd.concat([news_data, news], ignore_index=True)
    return news_data
