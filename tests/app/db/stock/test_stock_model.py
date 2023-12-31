from unittest.mock import patch
import pytest
import pandas as pd
from app.database.stocks.downloader_model.FDData import (
    get_price,
    get_news,
)


@pytest.fixture
def stock_price():
    result = get_price("MSFT", start="2023-07-12", end="2023-07-15", interval="1d")
    yield result


def test_get_daily_price(stock_price):
    # Test get_daily_price
    assert isinstance(stock_price, pd.DataFrame)
    assert len(stock_price) == 3  # 3 days of data
    assert stock_price.index.names == ["Date", "Symbol"]


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
