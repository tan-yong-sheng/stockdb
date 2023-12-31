(Remark: Currently, this is a Work in progress)

# Objective:
I wish to create a stock database that scrape the price and finanncial statement data to the MySQL database.

# Metadata
Below is the ER Diagram of this database project: 

![image](img/er-diagram.svg)

# Prerequisite:
- python + mysql database

# steps to run: 
1. rename .sample_env to .env, and then rep
2. open terminal, and then type `python -m app.database.db_controller`
3. check back your mysql gui to see if the database is created

# Plans
0. CSV file for FinancialStatementLineSequenceDB: https://github.com/leosmigel/analyzingalpha/tree/master/2020-02-28-financial-statement-database 
1. use intrinio as a baseline for database design of macro economics data: 
https://docs.intrinio.com/documentation/web_api/get_all_economic_indices_v2
2. use schedule + threading to repeat scraping process at any interval: https://www.geeksforgeeks.org/python-schedule-library/ & https://schedule.readthedocs.io/en/stable/parallel-execution.html
3. use numba + numpy to replace pandas for faster iteration
4. learn pytest for unit testing and Integration testing: 
- (i) Unit testing: https://github.com/OpenBB-finance/OpenBBTerminal/blob/develop/tests/README.md
- (ii) Integration testing: https://github.com/OpenBB-finance/OpenBBTerminal/blob/develop/openbb_terminal/miscellaneous/integration_tests_scripts/README.MD

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