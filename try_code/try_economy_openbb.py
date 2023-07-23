from openbb_terminal.sdk import openbb
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())
openbb.keys.fred(key = os.getenv("FRED_API"), persist = True)

print(openbb.economy.country_codes())

#List of Countries Accepted by Macro Function
#print(openbb.economy.overview())

# List of Countries Accepted by Macro Function
#print(openbb.economy.macro_countries())

# Dictionary of Parameters & Descriptions for Macro Function
#print(openbb.economy.macro_parameters())

#Gets Series Data from EconDB


"""
# very slow to run
print(openbb.economy.macro(parameters=openbb.economy.macro_parameters().keys(), 
                           countries=openbb.economy.macro_countries().keys()))

# calendar events
# very slow to run
openbb.economy.events(countries = openbb.economy.macro_countries().keys(), 
                      start_date = '2022-11-18', end_date = '2022-11-18').head(5)

print(openbb.economy.revenue()) # Government Revenues by Country
print(openbb.economy.spending()) # General Government Spending by Year and Country
print(openbb.economy.rgdp()) # Real GDP by Country
print(openbb.economy.trust())
print(openbb.economy.valuation())


# Only US
print(openbb.economy.treasury()) # US Treasuries Data
print(openbb.economy.usbonds())
print(openbb.economy.get_groups())
print(openbb.economy.valuation())

print(openbb.economy.available_indices())

print(openbb.economy.balance())

# The Big Mac Index
print(openbb.economy.bigmac())

# CPI Components Data by Country
print(openbb.economy.ccpi())

# Harmonized CPI Data by Country
print(openbb.economy.cpi())

# Government Debt-to-GDP Ratio
print(openbb.economy.debt())

# Economic Calendar
print(openbb.economy.events())

# Real GDP Forecast by Country
print(openbb.economy.fgdp())

# Current Prices of Commodities and Futures from WSJ
print(openbb.economy.futures())
"""
