# Currently, this is a Work in progress:

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