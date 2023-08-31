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
FINANCIAL_MODELING_PREP = os.getenv("FINANCIAL_MODELING_PREP", None)


class YFData:
    @staticmethod
    def _get_stock_price(
        symbols: Union[str, list] = "MSFT",
        start: Optional[str] = None,
        end: Optional[str] = None,
        interval: str = "1m",
        data_source: str = "yahoo finance",
    ):
        valid_intervals = ["1m", "5m", "15m", "30m", "1h", "1d"]
        if interval not in valid_intervals:
            raise ValueError(f"Invalid interval. Must be one of {valid_intervals}")
        symbols = symbols if isinstance(symbols, list) else [symbols]
        if data_source == "yahoo finance":
            for symbol in symbols:
                price = yfinance.download(
                    symbol, start=start, end=end, interval=interval
                )
                price["symbol"] = symbol
                price = standardize_dataframe_column(price, {"Datetime": "date"})
                price["date"] = pandas.to_datetime(price["date"])
                price["vendor_name"] = data_source
                yield price


class FMPData:
    symbols: Union[str, list] = ("MSFT",)
    start: Optional[str] = (None,)
    end: Optional[str] = (None,)
    interval: str = ("1m",)
    data_source: str = "financial modeling prep"

    @classmethod
    def _get_stock_price(
        cls,
        symbols: Union[str, list] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        interval: str = None,
        data_source: str = None,
    ):
        valid_intervals = ["1m", "5m", "15m", "30m", "1h", "1d"]
        valid_intervals_for_fmp = [
            "1min",
            "5min",
            "15min",
            "30min",
            "1hour",
            "1day",
        ]
        valid_intervals_dict = dict(zip(valid_intervals, valid_intervals_for_fmp))
        interval = valid_intervals_dict[interval]
        base_url = "https://financialmodelingprep.com/api/v3/"
        params = {"apikey": FINANCIAL_MODELING_PREP}

        if symbols is None:
            symbols = cls.symbols
        elif isinstance(symbols, str):
            symbols = [symbols]

        start = cls.start if start is None else start
        end = cls.start if end is None else end
        interval = cls.interval if interval is None else interval
        data_source = cls.data_source if data_source is None else data_source

        symbols = symbols if isinstance(symbols, list) else [symbols]
        for symbol in symbols:
            if interval != "1day":
                url = urljoin(base_url, quote(f"historical-chart/{interval}/{symbol}"))
                try:
                    response = requests.get(url=url, params=params)
                    response.raise_for_status()
                    price = pandas.json_normalize(response.json())
                    price["symbol"] = symbol
                except requests.exceptions.HTTPError as error:
                    raise Exception(error)

            else:
                # different endpoint for daily stock price
                url = urljoin(base_url, quote(f"historical-price-full/{symbol}"))
                try:
                    response = requests.get(url=url, params=params)
                    response.raise_for_status()
                    price_json_data = response.json()
                except requests.exceptions.HTTPError as error:
                    raise Exception(error)

                    # grouped_symbols_in_3 = [symbols[i:i+3] for i in range(0, len(symbols), 3)]
                    # prices_v1 = pandas.json_normalize(
                    #    price_json_data["historicalStockList"]
                    # )
                    # prices_v2 = prices_v1.explode("historical")
                    # prices_v3 = pandas.json_normalize(prices_v2["historical"])
                    # prices = pandas.merge(
                    #    prices_v2["symbol"].reset_index(),
                    #    prices_v3.reset_index(),
                    #    on="index",
                    # )

                price = pandas.json_normalize(price_json_data["historical"])
                price["symbol"] = symbol
                # prices = standardize_dataframe_column(
                #    prices, {"adjclose": "adj_close"}, drop_columns=["level_0"]
                # )
            price = standardize_dataframe_column(
                price, {"adjclose": "adj_close"}, drop_columns=["level_0"]
            )
            yield price
