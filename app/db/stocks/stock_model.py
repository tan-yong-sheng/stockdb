""" stock_controller.py

This module provides functions for CRUD application, which includes 
extracting stock data, fundamentals data, and news data, as well as 
storing data into a MySQL database.

Functions:
- get_company_info
- get_daily_price
- get_news
- get_financial_statement
- get_financial_ratio
"""

__doc__ = "numpy"

import os
import logging
from typing import Union
from datetime import datetime
import pandas
import requests
from requests.compat import urljoin, quote
from typing import Optional
from dotenv import load_dotenv, find_dotenv

from dateutil.relativedelta import relativedelta
import yfinance
import newsapi
from newsapi import NewsApiClient
import financedatabase as fd
from financetoolkit import Toolkit

from app.decorators import log_start_end, check_api_key
from app.helpers import standardize_dataframe_column


logger = logging.getLogger(__name__)

_ = load_dotenv(find_dotenv())
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY", None)
DATABASE_URI = os.getenv("DATABASE_URI", None)
FINANCIAL_MODELLING_PREP = os.getenv("FINANCIAL_MODELING_PREP", None)

############################# CREATE (OR FETCH) DATA #################################

## stock price query date
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - relativedelta(years=20)).strftime(
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
    sector: str = "",
    industry_group: str = "",
    industry: str = "",
    exchange: str = "NYQ",
    data_source: str = "yahoo finance",
) -> pandas.DataFrame:
    eq = fd.Equities()

    equities_info: pandas.DataFrame = eq.search(
        country=country,
        sector=sector,
        industry_group=industry_group,
        industry=industry,
        exchange=exchange,
    )
    equities_info = standardize_dataframe_column(equities_info)
    equities_info["vendor_name"] = data_source
    return equities_info


@log_start_end(log=logger)
def get_daily_price(
    symbols: Union[str, list] = "MSFT",
    start: Optional[str] = start_date,
    end: Optional[str] = end_date,
    interval="1d",
    data_source="yahoo finance",
) -> pandas.DataFrame:
    """Extracts daily stock price data for the given stock symbols.

    Parameters
    ----------
        symbols: Union[str, list], optional:
            A list of stock symbols or a single symbol as a string,
            by default "MSFT"
        start: Optional[str], optional:
            The start date in the format "YYYY-MM-DD", by default 10
            years ago from the current date.
        Optional[str], optional:
            The end date in the format "YYYY-MM-DD", by default the
            current date.
        data_source : str, optional:
            The data source, such as "yahoo finance", "financial modeling prep",
            by default yahoo finance

    Returns
    -------
        pandas.DataFrame: A DataFrame containing daily stock price data
        with columns: ['date', 'symbol', 'open', 'high', 'low', 'close',
                    'adj_close', 'volume'].
    """
    daily_prices = pandas.DataFrame()
    if data_source == "yahoo finance":
        symbols = " ".join(symbols) if isinstance(symbols, list) else symbols
        daily_prices = yfinance.download(
            symbols, start=start, end=end, interval=interval
        )
        if len(symbols.split(" ")) == 1:
            daily_prices["symbol"] = symbols
        else:
            daily_prices = daily_prices.stack()
            print(daily_prices)
        daily_prices = standardize_dataframe_column(daily_prices, {"level_1": "symbol"})
    elif data_source == "financial modeling prep":
        symbols = symbols.split(" ") if isinstance(symbols, str) else symbols
        companies = Toolkit(
            symbols, api_key=FINANCIAL_MODELLING_PREP, start_date=start, end_date=end
        )
        daily_prices = companies.get_historical_data()
        if len(symbols) == 1:
            daily_prices["symbol"] = symbols
        else:
            daily_prices = daily_prices.stack()
        daily_prices = standardize_dataframe_column(
            daily_prices, {"level_1": "symbol", "adjClose": "adj_close"}
        )
    daily_prices["date"] = pandas.to_datetime(daily_prices["date"])
    daily_prices["vendor_name"] = data_source
    return daily_prices


@log_start_end(log=logger)
@check_api_key(["NEWSAPI_API_KEY", "FINANCIAL_MODELING_PREP"])
def get_news(
    symbols: Union[str, list] = "MSFT",
    start: str = news_start_date,
    end: str = news_end_date,
    data_source: str = "news api",
):
    """
    Extracts news data for the given stock symbols from the news api.

    Parameters:
        symbols (list, optional): A list of stock symbols. Defaults to "MSFT".
        start_date (str, optional): The start date in the format "YYYY-MM-DD".
                                    Defaults to 10 years ago from the current date.
        end_date (str, optional): The end date in the format "YYYY-MM-DD".
                                  Defaults to the current date.
        data_source (str): The data source, such as "news api",
                            by default "news api"
    Returns:
        pandas.DataFrame: A DataFrame containing news data for the given
                        stock symbols with columns: ["title", "author",
                        "publisher", "publishedat", "content", "source_name",
                        "vendor_name", "symbol", "relatedtickers"]
    """
    news_data = pandas.DataFrame()
    symbols = symbols.split(" ") if isinstance(symbols, str) else symbols
    if data_source == "news api":
        news_api: str = NewsApiClient(api_key=NEWSAPI_API_KEY)
        for symbol in symbols:
            try:
                news = news_api.get_everything(
                    q=symbol,
                    language="en",
                    from_param=start,
                    to=end,
                    sort_by="relevancy",
                )
            except newsapi.newsapi_exception.NewsAPIException as error:
                raise error
            news = pandas.json_normalize(news)["articles"]
            news = pandas.json_normalize(news.explode())
            news["symbol"] = symbol
            news_data = pandas.concat([news_data, news], ignore_index=True)
        news_data = news_data.replace(columns={"description": "content"})

    elif data_source == "financial modeling prep":
        page_count: int = -1
        stock_news_url: str = "https://financialmodelingprep.com/api/v3/stock_news"
        # not sure whether could accept mulitple stocks, e.g., above 1000?
        # in documentation, seems like up to 3 only

        # Problem 2: how many pages to scrape?
        symbols = symbols.replace(" ", ",")
        try:
            response = requests.get(
                stock_news_url,
                params={
                    "symbol": symbols,
                    "page": page_count,
                    "apikey": FINANCIAL_MODELLING_PREP,
                },
            )
            response.raise_for_status()
            news_data = pandas.json_normalize(response.json())
        except requests.exceptions.HTTPError as error:
            raise Exception(
                """Special Endpoint : This endpoint is not available
                        under your current subscription please visit our
                        subscription page to upgrade your plan at 
                https://site.financialmodelingprep.com/developer/docs/pricing"""
            )

    news_data["vendor_name"] = data_source
    return standardize_dataframe_column(news_data)


@log_start_end(log=logger)
@check_api_key(["FINANCIAL_MODELING_PREP"])
def get_financial_statement(
    symbols: Union[str, list] = "MSFT",
    start: str = start_date,
    end: str = end_date,
    report: str = "income statement",
    data_source="financial modeling prep",
) -> pandas.DataFrame:
    """
    Extracts financial report data for the given stock symbols.

    Parameters:
        symbols (list, optional): A list of stock symbols. Defaults to "MSFT".a
        start_date (str, optional): The start date in the format "YYYY-MM-DD".
                                    Defaults to 10 years ago from the current date.
        end_date (str, optional): The end date in the format "YYYY-MM-DD".
                                  Defaults to the current date.
        data_source (str): The data source, such as "yahoo finance",
                     "news api"
                        Defaults to yahoo finance
    Returns:
        pandas.DataFrame: A DataFrame containing news data for the given stock symbols,
                            where the columns includes:
                            ["title", "author", "publisher", "content",
                            "providerpublishdate", "url", "urltoimage",
                            "source_name", "vendor_name", "symbol", "relatedtickers"]
    """
    if isinstance(symbols, str):
        symbols = symbols.split(" ")
    companies = Toolkit(
        symbols, api_key=FINANCIAL_MODELLING_PREP, start_date=start, end_date=end
    )
    financial_statement = pandas.DataFrame()
    report = report.replace(" ", "_")
    if report == "income_statement":
        financial_statement = companies.get_income_statement()
    elif report == "balance_sheet":
        financial_statement = companies.get_balance_sheet_statement()
    elif report == "cash_flow":
        financial_statement = companies.get_cash_flow_statement()

    financial_statement = financial_statement.reset_index().rename(
        columns={"level_0": "symbol", "level_1": f"{report}_item"}
    )
    financial_statement = pandas.melt(
        financial_statement,
        id_vars=["symbol", f"{report}_item"],
        var_name=["year"],
        value_name="value",
    )
    financial_statement["vendor_name"] = data_source
    return standardize_dataframe_column(financial_statement)


@log_start_end(log=logger)
@check_api_key(["FINANCIAL_MODELING_PREP"])
def get_financial_ratio(
    symbols: Union[str, list] = "MSFT",
    start: str = start_date,
    end: str = end_date,
    include_dividends: bool = False,
    diluted: bool = True,
    days: int = 365,
    data_source="financial modeling prep",
) -> pandas.DataFrame:
    if isinstance(symbols, str):
        symbols = symbols.split(" ")
    companies = Toolkit(
        symbols, api_key=FINANCIAL_MODELLING_PREP, start_date=start, end_date=end
    )
    efficiency_ratios = companies.ratios.collect_efficiency_ratios(days=days)
    efficiency_ratios["category"] = "efficiency"
    liquidity_ratios = companies.ratios.collect_liquidity_ratios()
    liquidity_ratios["category"] = "liquidity"
    profitability_ratios = companies.ratios.collect_profitability_ratios()
    profitability_ratios["category"] = "profitability"
    solvency_ratios = companies.ratios.collect_solvency_ratios()
    solvency_ratios["category"] = "solvency"
    valuation_ratios = companies.ratios.collect_valuation_ratios(
        include_dividends=include_dividends, diluted=diluted
    )
    valuation_ratios["category"] = "valution"
    all_ratios = pandas.concat(
        [
            efficiency_ratios,
            liquidity_ratios,
            profitability_ratios,
            solvency_ratios,
            valuation_ratios,
        ]
    )
    all_ratios = all_ratios.reset_index()
    if len(symbols) == 1:
        all_ratios["symbol"] = symbols[0]
        all_ratios = all_ratios.rename(columns={"index": "financial ratio"})
    else:
        all_ratios = all_ratios.rename(
            columns={"level_0": "symbol", "level_1": "financial ratio"}
        )
    all_ratios["vendor_name"] = data_source
    all_ratios = pandas.melt(
        all_ratios,
        id_vars=["symbol", "financial ratio", "category", "vendor_name"],
        var_name=["date"],
        value_name="value",
    )
    return standardize_dataframe_column(all_ratios)


@log_start_end(log=logger)
@check_api_key(["FINANCIAL_MODELING_PREP"])
def get_intraday_data(
    symbols: Union[str, list] = "MSFT",
    start: str = start_date,
    end: str = end_date,
    interval="1min",
    data_source="financial modeling prep",
):
    pass


if __name__ == "__main__":
    # all_ratios = get_financial_ratio(symbols="AAPL MSFT")
    # all_ratios.to_csv("all_ratios.csv")
    # print(all_ratios)

    df = get_daily_price("AAPL MSFT", data_source="financial modeling prep")
    print(df)

    # news = get_news("MSFT AAPL", data_source="financial modeling prep")
    # news.to_csv("news_api.csv")
    # print(news)

# ,index,uuid,title,publisher,link,providerpublishtime,type,relatedtickers,thumbnail.resolutions,symbol
# ,index,author,title,description,url,urltoimage,publishedat,content,source.id,source.name,symbol
