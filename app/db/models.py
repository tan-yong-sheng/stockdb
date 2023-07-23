from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, LONGTEXT, TEXT

class MasterSQLModel(SQLModel):
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    

class CompanyDB(MasterSQLModel,table=True):
    __tablename__ = "Company"
    __table_args__ = (
        dict(comment="List of public listed companies"),
    )
    id: Optional[int] = Field(primary_key=True, nullable=False)
    symbol: Optional[str]
    name: Optional[str]
    summary: Optional[str] = Field(sa_column=Column(TEXT))
    currency: Optional[str]
    sector: Optional[str]
    industry_group: Optional[str]
    industry: Optional[str]
    exchange: Optional[str]
    market: Optional[str]
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    zipcode: Optional[int]
    website: Optional[str] = Field(sa_column=Column(TEXT))
    market_cap: Optional[int] = Field(sa_column=Column(BIGINT))
    isin: Optional[str]
    cusip: Optional[str]
    figi: Optional[str]
    composite_figi: Optional[str]
    shareclass_figi: Optional[str]

    
class PriceDB(MasterSQLModel, table=True):
    __tablename__ = "Price"
    __table_args__ = (
        UniqueConstraint("Date", "Symbol", name="date_symbol"),
        dict(comment="Historical stock price of public listed companies")
    )
    id: Optional[int] = Field(primary_key=True, nullable=False) 
    Date: datetime
    Symbol: str = Field(alias="Symbol",foreign_key="CompanyDB.id")
    Open: Optional[float]
    High: Optional[float]
    Low: Optional[float]
    Close: Optional[float]
    Adj_Close: Optional[float] = Field(alias="Adj Close")
    Volume: Optional[int]


class NewsDB(MasterSQLModel, table=True):
    __tablename__ = "News"
    __table_args__ = (
        UniqueConstraint("title","author", name="title_author_date"),
        dict(comment="List of news of public listed companies"),
    )
    id: Optional[int] = Field(primary_key=True, nullable=False)
    Symbol: Optional[str] 
    title: Optional[str]
    author: Optional[str]
    description: Optional[str] = Field(sa_column=Column(LONGTEXT))
    url: Optional[str] = Field(sa_column=Column(TEXT))
    urlToImage: Optional[str]
    publishedAt: Optional[datetime]
    content: Optional[str] = Field(sa_column=Column(LONGTEXT))
    source_id: Optional[str]
    source_name: Optional[str]


class FundamentalsDB(MasterSQLModel, table=True):
    __tablename__ = "Fundamentals"
    __table_args__ = (
        UniqueConstraint("Symbol", name="symbol"),
    )
    id: Optional[int] = Field(primary_key=True, nullable=False)
    Symbol: str = Field(alias="symbol")
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


class NullDB(MasterSQLModel, table=True):
    # an empty database for testing purpose
    __tablename__ = "test"
    id: int = Field(default=None, primary_key=True)
