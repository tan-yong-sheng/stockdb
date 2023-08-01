from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import UniqueConstraint
from sqlmodel import Column
from sqlalchemy.dialects.mysql import BIGINT, LONGTEXT, TEXT, VARCHAR
from typing import List

class MasterSQLModel(SQLModel):
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class DailyPriceVendorLink(MasterSQLModel,table=True):
    data_vendor_id: Optional[int] = Field(
        default=None,foreign_key="fact_daily_price.id", primary_key=True,
    )
    daily_price_id: Optional[int] = Field(
        default=None, foreign_key="dim_data_vendor.id",primary_key=True
    )


class CountryCompanyLink(MasterSQLModel, table=True):
    # Link Model
    # To link up 2 tables with Many-to-Many relationship
    country_id: Optional[int] = Field(
        default=None, foreign_key="dim_countries.id", primary_key=True,
    )
    company_id: Optional[int] = Field(
        default=None, foreign_key="dim_companies.id", primary_key=True
    )


class DataVendorDB(MasterSQLModel, table=True):
    __tablename__ = "dim_data_vendor"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, nullable=False)
    website_url: Optional[str] = Field(default=None)
    support_email: Optional[str] = Field(default=None)
    daily_prices: List["DailyPriceDB"] = Relationship(back_populates="data_vendors",
                                                     link_model=DailyPriceVendorLink)

class CountriesDB(MasterSQLModel, table=True):
    __tablename__ = "dim_countries"
    id: Optional[int] = Field(default=None, primary_key=True)
    country: Optional[str] = Field(index=True)
    code: Optional[str]
    currency: Optional[str]
    companies: List["CompaniesDB"] = Relationship(back_populates="countries", 
                                                  link_model=CountryCompanyLink)


class CompaniesDB(MasterSQLModel, table=True):
    __tablename__ = "dim_companies"
    __table_args__ = (dict(comment="List of public listed companies"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: Optional[str] = Field(index=True, nullable=False)
    name: Optional[str]
    summary: Optional[str] = Field(sa_column=Column(TEXT))
    currency: Optional[str]
    sector: Optional[str]
    industry_group: Optional[str]
    industry: Optional[str]
    exchange: Optional[str]
    market: Optional[str]
    country: Optional[str] = Field(foreign_key="dim_countries.country")
    countries: List["CountriesDB"] = Relationship(back_populates="companies",
                                                  link_model=CountryCompanyLink)
    state: Optional[str]
    city: Optional[str]
    zipcode: Optional[int]
    website: Optional[str] = Field(sa_column=Column(TEXT))
    market_cap: Optional[str] = Field(sa_column=Column(VARCHAR(255)))
    isin: Optional[str]
    cusip: Optional[str]
    figi: Optional[str]
    composite_figi: Optional[str]
    shareclass_figi: Optional[str]
    daily_prices: List["DailyPriceDB"] = Relationship(back_populates="company")

class DailyPriceDB(MasterSQLModel, table=True):
    __tablename__ = "fact_daily_price"
    __table_args__ = (
        dict(comment="Daily stock price of public listed companies"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    #data_vendor_id: Optional[int] = Field(foreign_key="dim_data_vendor.name")
    data_vendors: List["DataVendorDB"] = Relationship(back_populates="daily_prices",
                                                     link_model=DailyPriceVendorLink)
    date: datetime
    symbol: Optional[str] = Field(foreign_key='dim_companies.symbol', nullable=False)
    company: Optional[CompaniesDB] = Relationship(back_populates="daily_prices")
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    adj_close: Optional[float]
    volume: Optional[int] = Field(sa_column=Field(Column(BIGINT)))
    
    


class NewsDB(MasterSQLModel, table=True):
    __tablename__ = "fact_news"
    __table_args__ = (
        #UniqueConstraint("title", "author", name="title_author"),
        dict(comment="List of news of public listed companies"),
    )
    id: Optional[int] = Field(primary_key=True, nullable=False)
    #symbol_id: Optional[int] = Field(default=None, foreign_key="dim_companies.id")
    symbol: Optional[str] #"CompaniesDB" = Relationship(back_populates="news_links")
    title: Optional[str]
    author: Optional[str]
    description: Optional[str] = Field(sa_column=Column(LONGTEXT))
    url: Optional[str] = Field(sa_column=Column(TEXT))
    urlToImage: Optional[str] = Field(alias="urltoimage")
    publishedAt: Optional[datetime] = Field(alias="publishedat")
    content: Optional[str] = Field(sa_column=Column(LONGTEXT))
    source_id: Optional[str]
    source_name: Optional[str]
    

class MacroParametersDB(MasterSQLModel, table=True):
    __tablename__ = "dim_macro_parameters"
    id: int = Field(primary_key=True, default=None)
    name: str
    period: str
    description: str = Field(sa_column=Column(TEXT))


class EconomicCalendarDB(MasterSQLModel, table=True):
    __tablename__ = "fact_economic_calendar"
    id: Optional[int] = Field(primary_key=True, default=None)
    date: Optional[datetime] = Field(alias="date")
    time: Optional[datetime] = Field(alias="time_(et)")
    #country_id: Optional[int] = Field(default=None, foreign_key="dim_countries.id")
    country: Optional[str] #"CountriesDB" = Relationship(back_populates="economic_calendar_links")
    event: Optional[str]
    actual: Optional[str]
    consensus: Optional[str]
    previous: Optional[str]


class MacroIndicatorsDB(MasterSQLModel, table=True):
    __tablename__ = "fact_macro_indicators"
    id: Optional[int] = Field(primary_key=True, default=None)
    date: Optional[datetime]
    #country_id: Optional[int] = Field(default=None, foreign_key="dim_countries.id")
    country: Optional[str]#[CountriesDB] = Relationship(back_populates="macro_indicators_links")
    variable: Optional[str]
    value: Optional[int]
    unit: Optional[str]
    currency_or_measurement: Optional[str]
    

class NullDB(MasterSQLModel, table=True):
    # an empty database for testing purpose
    __tablename__ = "test"
    id: int = Field(default=None, primary_key=True)

class FundamentalsDB(MasterSQLModel, table=True):
    __tablename__ = "fundamentals"
    __table_args__ = (UniqueConstraint("symbol", name="symbol"),)
    id: Optional[int] = Field(primary_key=True, nullable=False)
    symbol: str
    address1: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str] = Field(alias="zip")
    country: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    industry: Optional[str]
    industryDisp: Optional[str]
    sector: Optional[str]
    longBusinessSummary: Optional[str] = Field(sa_column=Column(LONGTEXT))
    fullTimeEmployees: Optional[int]
    companyOfficers: Optional[str] = Field(sa_column=Column(TEXT))
    auditRisk: Optional[int]
    boardRisk: Optional[int]
    compensationRisk: Optional[int]
    shareHolderRightsRisk: Optional[int]
    overallRisk: Optional[int]
    governanceEpochDate: Optional[str]
    compensationAsOfEpochDate: Optional[str]
    maxAge: Optional[str]
    priceHint: Optional[int]
    previousClose: Optional[float]
    open: Optional[float]
    dayLow: Optional[float]
    dayHigh: Optional[float]
    regularMarketPreviousClose: Optional[float]
    regularMarketOpen: Optional[float]
    regularMarketDayLow: Optional[float]
    regularMarketDayHigh: Optional[float]
    dividendRate: Optional[float]
    dividendYield: Optional[float]
    exDividendDate: Optional[datetime]
    payoutRatio: Optional[float]
    fiveYearAvgDividendYield: Optional[float]
    beta: Optional[float]
    trailingPE: Optional[float]
    forwardPE: Optional[float]
    volume: Optional[int]
    regularMarketVolume: Optional[int]
    averageVolume: Optional[int]
    averageVolume10days: Optional[int]
    averageDailyVolume10Day: Optional[int]
    bid: Optional[float]
    ask: Optional[float]
    bidSize: Optional[int]
    askSize: Optional[int]
    marketCap: Optional[int] = Field(sa_column=Column(BIGINT))
    fiftyTwoWeekLow: Optional[float]
    fiftyTwoWeekHigh: Optional[float]
    priceToSalesTrailing12Months: Optional[float]
    fiftyDayAverage: Optional[float]
    twoHundredDayAverage: Optional[float]
    trailingAnnualDividendRate: Optional[float]
    trailingAnnualDividendYield: Optional[float]
    currency: Optional[str]
    enterpriseValue: Optional[float]
    profitMargins: Optional[float]
    floatShares: Optional[int] = Field(sa_column=Column(BIGINT))
    sharesOutstanding: Optional[int] = Field(sa_column=Column(BIGINT))
    sharesShort: Optional[int]
    sharesShortPriorMonth: Optional[int]
    sharesShortPreviousMonthDate: Optional[int]
    dateShortInterest: Optional[datetime]
    sharesPercentSharesOut: Optional[float]
    heldPercentInsiders: Optional[float]
    heldPercentInstitutions: Optional[float]
    shortRatio: Optional[float]
    shortPercentOfFloat: Optional[float]
    impliedSharesOutstanding: Optional[int] = Field(sa_column=Column(BIGINT))
    bookValue: Optional[float]
    priceToBook: Optional[float]
    lastFiscalYearEnd: Optional[float]
    nextFiscalYearEnd: Optional[float]
    mostRecentQuarter: Optional[float]
    earningsQuarterlyGrowth: Optional[float]
    netIncomeToCommon: Optional[float]
    trailingEps: Optional[float]
    forwardEps: Optional[float]
    pegRatio: Optional[float]
    lastSplitFactor: Optional[str]
    lastSplitDate: Optional[datetime]
    enterpriseToRevenue: Optional[float]
    enterpriseToEbitda: Optional[float]
    FiftyTwoWeekChange: Optional[float] = Field(alias="52WeekChange")
    SandP52WeekChange: Optional[float]
    lastDividendValue: Optional[float]
    lastDividendDate: Optional[datetime]
    exchange: Optional[str]
    quoteType: Optional[str]
    underlyingSymbol: Optional[str]
    shortName: Optional[str]
    longName: Optional[str]
    firstTradeDateEpochUtc: Optional[str]
    timeZoneFullName: str
    timeZoneShortName: Optional[str]
    uuid: Optional[str]
    messageBoardId: Optional[int]
    gmtOffSetMilliseconds: Optional[int]
    currentPrice: Optional[float]
    targetHighPrice: Optional[float]
    targetLowPrice: Optional[float]
    targetMeanPrice: Optional[float]
    targetMedianPrice: Optional[float]
    recommendationMean: Optional[float]
    recommendationKey: Optional[float]
    numberOfAnalystOpinions: Optional[float]
    totalCash: Optional[float]
    totalCashPerShare: Optional[float]
    ebitda: Optional[float]
    totalDebt: Optional[float]
    quickRatio: Optional[float]
    currentRatio: Optional[float]
    totalRevenue: Optional[float]
    debtToEquity: Optional[float]
    revenuePerShare: Optional[float]
    returnOnAssets: Optional[float]
    returnOnEquity: Optional[float]
    grossProfits: Optional[float]
    freeCashflow: Optional[float]
    operatingCashflow: Optional[float]
    earningsGrowth: Optional[float]
    revenueGrowth: Optional[float]
    grossMargins: Optional[float]
    ebitdaMargins: Optional[float]
    operatingMargins: Optional[float]
    financialCurrency: Optional[str]
    trailingPegRatio: Optional[str] = Field(nullable=True)
    fax: Optional[str] = Field(nullable=True)
