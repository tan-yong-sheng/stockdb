from openbb_terminal.sdk import openbb
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
from datetime import datetime


countries = ["United States", "China", "Singapore", "Malaysia"]
countries_code = ["USA", "CHN", "SIN", "MYS"]
countries_lower = [country.lower().strip().replace(" ", "_") for country in countries]

_ = load_dotenv(find_dotenv())
openbb.keys.fred(key=os.getenv("FRED_API"), persist=True)


# available_country_code = openbb.economy.country_codes()
# available_country_code.to_csv("dim_countries.csv")
# print(available_country_code)

# List of Countries Accepted by Macro Function
# countries = openbb.economy.macro_countries()
# print(countries)

# Dictionary of Parameters & Descriptions for Macro Function
# macro_parameters = openbb.economy.macro_parameters()
# macro_parameters = pd.DataFrame.from_dict(macro_parameters).T
# macro_parameters.to_csv("dim_macro_parameters.csv")

# Gets Series Data from EconDB
# very slow to run
# print(openbb.economy.macro(parameters=openbb.economy.macro_parameters().keys(),
#                           countries=openbb.economy.macro_countries().keys()))
macro_data, *metadata = openbb.economy.macro(
    parameters=["RGDP", "CPI"],
    countries=["United States", "China"],  # ,"China","Malaysia","Singpore"],
    symbol="USD",
)
# idx = pd.MultiIndex.from_product(metadata)

# [{'United States': {'RGDP': 'USD', 'CPI': 'Index'}, 'China': {'RGDP': 'USD', 'CPI': 'Index'}}, ' [in Trillions]']


print(metadata)

print("---------------------")
macro_data.to_csv(
    "fact_economy.csv"
)  # .unstack().reset_index().rename(columns={"level_1":
#                                      "macroeconomics_indicator"}).\
# to_csv("fact_macro_data.csv")
print(macro_data)

# calendar events
# very slow to run
# openbb.economy.macro_countries().keys()

# -------------------------------------------------------
# print(openbb.economy.macro_countries().keys()) # str.lower() + replace(" ","_")

# too slow # which countries?
# economy_events = openbb.economy.events(countries = ["united_states","china"],
#                                       start_date="2022-01-01",end_date=datetime.now())
# economy_events.to_csv("fact_economy_events.csv")
# print(economy_events)


# ---------------------------
"""

# Aim to put together with openbb.economy.macro
print("=============================")
# Trust in government refers to the share of people who report having confidence in the national government. The data shown reflect the share of respondents answering “yes” (the other response categories being “no”, and “don’t know”) to the survey question: “In this country, do you have confidence in… national government? Due to small sample sizes, country averages for horizontal inequalities (by age, gender and education) are pooled between 2010-18 to improve the accuracy of the estimates. The sample is ex ante designed to be nationally representative of the population aged 15 and over. This indicator is measured as a percentage of all survey respondents. [Source: OECD]
trust = openbb.economy.trust(countries=countries_lower)
trust.to_csv("trust.csv")
print(trust)
print("=============================")

print("=============================")
fgdp = openbb.economy.fgdp(countries=countries_lower) # Real GDP Forecast by Country
fgdp.to_csv("fgdp.csv")
print(fgdp)

print("=============================")
ccpi = openbb.economy.ccpi(countries=countries_lower) # CPI Components Data by Country
ccpi.to_csv("ccpi.csv")
print(ccpi)
print("=============================")


# -------------------------------------------------------------------------


# Only US
#print(openbb.economy.treasury()) # US Treasuries Data
#print(openbb.economy.usbonds())
#print(openbb.economy.available_indices())
#print(openbb.economy.get_groups())
#valuation = openbb.economy.valuation()
# Current Prices of Commodities and Futures from WSJ
#print(openbb.economy.futures())


## got already in openbb.economy.macro
#--------------------------------------
#print(openbb.economy.rgdp()) # Real GDP by Country
#print(openbb.economy.debt()) # Government Debt-to-GDP Ratio 
#print(openbb.economy.balance())
#print(openbb.economy.cpi()) # Harmonized CPI Data by Country

#revenue = openbb.economy.revenue(countries=countries_codes) # Government Revenues by Country
#revenue.to_csv("revenue.csv")
#print(revenue)
#print("=============================")
#spending = openbb.economy.spending(countries=countries_codes) # General Government Spending by Year and Country
#spending.to_csv("spending.csv")
#print(spending)


# Quandl data - data support until 2020 only
bigmac = openbb.economy.bigmac(country_codes=countries_lower) # The Big Mac Index
bigmac.to_csv("bigmac.csv")
print(bigmac)
"""
