from datetime import datetime
from typing import Dict
import pandas
from openbb_terminal.sdk import openbb
from app.helpers import standardize_dataframe_column


def get_macro_parameters() -> Dict[str, Dict[str, str]]:
    return openbb.economy.macro_parameters()


def get_countries_with_currencies() -> Dict[str, str]:
    """_summary_
    This function returns the available countries and respective currencies.

    Returns
    Dict[str, str]
        A dictionary with the available countries and respective currencies.
    """
    return openbb.economy.macro_countries()


def get_countries_code() -> pandas.DataFrame:
    """_summary_
    Get available country codes for Bigmac index

    Returns
    List[str]
        List of ISO-3 letter country codes.
    """
    return standardize_dataframe_column(openbb.economy.country_codes())

def get_countries() -> pandas.DataFrame:
    countries_with_currencies = pandas.DataFrame.from_dict(
                                    get_countries_with_currencies(),
                                    orient="index").reset_index()
    countries_with_currencies.columns = ["country", "currency"]
    countries_code = get_countries_code()
    countries = pandas.merge(countries_code, countries_with_currencies, 
                             on="country", how="outer")
    test_df = standardize_dataframe_column(countries,
                                        drop_columns=["level_0","index"])
    print(test_df.columns)
    return test_df
    

def get_macro_indicators_data(
    parameters: list = ["RGDP","HOU", "CORE"],
    countries: list = ["United States", "China"],
    start_date="2022-01-01",
    end_date=datetime.now(),
    symbol: str = "USD",
) -> pandas.DataFrame:
    """_summary_

    Parameters
    ----------
    parameters : list
        The type of data you wish to download. Available parameters can be
        accessed through economy.macro_parameters().
    countries : list
        The selected country or countries. Available countries can be accessed
        through economy.macro_countries().
    start_date : str
        The starting date, format "YEAR-MONTH-DAY", i.e. 2022-01-01.
    end_date : str
        The ending date, format "YEAR-MONTH-DAY", i.e. 2023-01-01.

    Returns
    -------
    _type_
        _description_
    """
    macro_data, *metadata = openbb.economy.macro(
        parameters=parameters,
        countries=countries,
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )
    macro_df = pandas.melt(
        macro_data.reset_index(),
        id_vars=["date"],
        var_name=["countries", "variable"],
        value_name="value",
    )
    macro_df["unit"] = metadata[1].replace("[", "").replace("]", "").replace("in ", "")
    # add currency & measurement column
    data_type_dict = {}
    for data_type in metadata[0].values():
        data_type_dict.update(**data_type)
    macro_df["currency_or_measurement"] = macro_df["variable"].replace(data_type_dict)
    return standardize_dataframe_column(macro_df)


def get_economic_calendar(
    countries=["united_states", "china"],
    start_date="2022-01-01",
    end_date=datetime.now(),
):
    """_summary_

    Parameters
    ----------
    countries : list, optional
        List of countries to include in calendar. Empty returns all
    start_date : str, optional
        Start date for calendar, by default "2022-01-01"
    end_date : _type_, optional
        End date for calendar, by default datetime.now()

    Returns
    -------
    pandas.DataFrame
        Economic calendar
    """
    calendar = openbb.economy.events(
        countries=countries, start_date=start_date, end_date=end_date
    )
    return standardize_dataframe_column(calendar)


if __name__ == "__main__":
    # df = get_macro_indicators_data()
    df = get_countries()
    print(df)
