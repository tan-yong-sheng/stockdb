"""Historical Module"""
__docformat__ = "numpy"

import os
from typing import Union, Optional
import pandas
import yfinance
from dotenv import load_dotenv, find_dotenv
import requests
from requests.compat import urljoin, quote
from app.helpers import standardize_dataframe_column

_ = load_dotenv(find_dotenv())
FINANCIAL_MODELING_PREP = os.getenv("FINANCIAL_MODELING_PREP",None)

class PriceFetcher:
    @staticmethod
    def _get_price(
        symbols: Union[str, list] = "MSFT",
        start: Optional[str] = None,
        end: Optional[str] = None,
        interval: str="1m",
        data_source: str="yahoo finance",
    ):
        prices = pandas.DataFrame()
        valid_intervals = ["1m", "5m", "15m", "30m", "1h","1d"]
        if interval not in valid_intervals:
            raise ValueError(f"Invalid interval. Must be one of {valid_intervals}")
        symbols = " ".join(symbols) if isinstance(symbols, list) else symbols
        if data_source == "yahoo finance":
            prices = yfinance.download(
                symbols, start=start, end=end, interval=interval
            )
            if len(symbols.split(" ")) == 1:
                prices["symbol"] = symbols
            else:
                prices = prices.stack()
            prices = standardize_dataframe_column(prices, 
                                {"level_1": "symbol", "Datetime":"date"})
        
        elif data_source == "financial modeling prep":
            valid_intervals_for_fmp = ["1min","5min","15min","30min","1hour","1day"]
            valid_intervals = dict(zip(valid_intervals, valid_intervals_for_fmp))
            interval = valid_intervals[interval]
            base_url = "https://financialmodelingprep.com/api/v3/"
            params = {"apikey": FINANCIAL_MODELING_PREP}
            
            if interval != "1day":
                prices = pandas.DataFrame()
                for symbol in symbols.split(" "):
                    url = urljoin(base_url, quote(f"historical-chart/{interval}/{symbol}"))
                    try:
                        response = requests.get(url=url, params=params)
                        response.raise_for_status()
                        price = pandas.json_normalize(response.json())
                        price["symbol"] = symbol
                    except requests.exceptions.HTTPError as error:
                        raise Exception(error)
                    prices = pandas.concat([prices, price])
                prices = standardize_dataframe_column(prices)
            else:
                symbols = symbols.strip().replace(" ",",")
                url = urljoin(base_url, quote(f"historical-price-full/{symbols}"))
                try:
                    response = requests.get(url=url, params=params)
                    response.raise_for_status()
                    price_json_data = response.json()
                except requests.exceptions.HTTPError as error:
                    raise Exception(error)
                if len(symbols.split(",")) > 1:
                    prices_v1 = pandas.json_normalize(price_json_data["historicalStockList"])
                    prices_v2 = prices_v1.explode("historical")
                    prices_v3 = pandas.json_normalize(prices_v2["historical"])
                    prices = pandas.merge(prices_v2["symbol"].reset_index(),prices_v3.reset_index(),on="index")
                else:
                    print(price_json_data["historical"])
                    prices = pandas.json_normalize(price_json_data["historical"])
                    prices["symbol"] = symbols
                prices = standardize_dataframe_column(prices, {"adjclose":"adj_close"}, drop_columns=["level_0"])
        return prices

