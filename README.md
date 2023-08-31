# Currently, this is a Work in progress:
- please resume working on : app\db\financial_statement_model.py - half done, haven't yet finished

# Plans:
- use intrinio as a baseline for database design of macro economics data: 
https://docs.intrinio.com/documentation/web_api/get_all_economic_indices_v2

# Objective:
Build a MySQL database which scrape historical stock price data, news data, and macroeconomics data.

# Challenges:
1. Makefile to automate the mysql db creation... (+Github actions)

2. Use financedatabase to get data: https://pypi.org/project/financedatabase/


# Reminder
database migrations tool: `alembic`

- Step 1: Type `alembic init alembic` at your working directory. It will create an folder named `alembic`. Skip this if `alembic` folder exists
- Step 2: Type `alembic revision --autogenerate`
- Step 3: Type `alembic upgrade head`