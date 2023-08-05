from financetoolkit import Toolkit
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

FMP_API = os.getenv("FINANCIAL_MODELING_PREP")

companies = Toolkit(["AAPL", "MSFT"], api_key=FMP_API)  # quarterly=True)


"""
efficiency_ratios = companies.ratios.collect_efficiency_ratios().unstack().stack(level=0).\
                        reset_index().rename(columns={'level_0':"Symbol"})
efficiency_ratios.to_csv("efficiency_ratios.csv")
print(efficiency_ratios.columns)
print(efficiency_ratios)


profitability_ratios = companies.ratios.collect_profitability_ratios().unstack().stack(level=0).\
                        reset_index().rename(columns={'level_0':"Symbol"})
profitability_ratios.to_csv("profitability_ratios.csv")
print(profitability_ratios.columns)
print(profitability_ratios)


liquidity_ratios = companies.ratios.collect_liquidity_ratios().unstack().stack(level=0).\
                        reset_index().rename(columns={'level_0':"Symbol"})
liquidity_ratios.to_csv("liquidity_ratios.csv")
print(liquidity_ratios.columns)
print(liquidity_ratios)



solvency_ratios = companies.ratios.collect_solvency_ratios().unstack().stack(level=0).\
                        reset_index().rename(columns={'level_0':"Symbol"})
solvency_ratios.to_csv("solvency_ratios.csv")
print(solvency_ratios.columns)
print(solvency_ratios)


print(help(companies.ratios.collect_valuation_ratios))

valuation_ratios = companies.ratios.collect_valuation_ratios().unstack().stack(level=0).\
                        reset_index().rename(columns={'level_0':"Symbol", "level_1":"date"})
valuation_ratios.to_csv("valuation_ratios.csv")
print(valuation_ratios.columns)
print(valuation_ratios)


"""
print(help(companies.get_income_statement))
income_statement = (
    companies.get_income_statement()
    .unstack()
    .stack(level=0)
    .reset_index()
    .rename(columns={"level_0": "Symbol"})
)
# income_statement.to_csv("income_statement.csv")
print(income_statement.columns)
print(income_statement)

"""
print(help(companies.get_balance_sheet_statement))
balance_sheet_statement = companies.get_balance_sheet_statement(quarter=True).unstack().stack(level=0).\
                        reset_index().rename(columns={'level_0':"Symbol"})
                        

balance_sheet_statement.to_csv("balance_sheet.csv")
print(balance_sheet_statement)


cash_flow_statement = companies.get_cash_flow_statement().unstack().stack(level=0).\
                        reset_index().rename(columns={'level_0':"Symbol"})
cash_flow_statement.to_csv("cash_flow_statement.csv")
print(cash_flow_statement)

"""
