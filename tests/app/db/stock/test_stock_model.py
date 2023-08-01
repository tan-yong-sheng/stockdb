from unittest.mock import patch
import pytest
import pandas as pd
from app.db.stocks.stock_model import (
    get_daily_price,
    get_fundamentals_data,
    get_news,
)


@pytest.fixture
def stock_price():
    result = get_daily_price(
        "MSFT", start="2023-07-12", end="2023-07-15", interval="1d"
    )
    yield result


@pytest.fixture
def fundamentals_data():
    result = get_fundamentals_data("MSFT")
    yield result


def test_get_daily_price(stock_price):
    # Test get_daily_price
    assert isinstance(stock_price, pd.DataFrame)
    assert len(stock_price) == 3  # 3 days of data
    assert stock_price.index.names == ["Date", "Symbol"]


@pytest.mark.skip("Haven't done yet")
def test_get_fundamentals_data():
    # Mocking yf.Ticker
    with patch("stock_database.stocks.stock_model.yf.Ticker") as mock_ticker:
        mock_ticker.return_value.info = {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "sector": "Technology",
            # Add more fields here as needed for testing
        }
        result = get_fundamentals_data(["AAPL"])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.loc[0, "symbol"] == "AAPL"
        assert result.loc[0, "name"] == "Apple Inc."
        assert result.loc[0, "sector"] == "Technology"


@pytest.mark.skip("Haven't done yet")
def test_get_news():
    # Mocking NewsApiClient
    with patch("db.stocks.stock_controller.NewsApiClient") as mock_news_api:
        mock_news_api.return_value.get_everything.return_value = {
            "articles": [
                {
                    "title": "Apple stock news",
                    "description": "Apple Inc. announced...",
                    # Add more fields here as needed for testing
                },
                {
                    "title": "Google stock news",
                    "description": "Alphabet Inc. released...",
                    # Add more fields here as needed for testing
                },
            ]
        }
        result = get_news(["AAPL", "GOOGL"])
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.loc[0, "title"] == "Apple stock news"
        assert result.loc[0, "description"] == "Apple Inc. announced..."
        assert result.loc[1, "title"] == "Google stock news"
        assert result.loc[1, "description"] == "Alphabet Inc. released..."
