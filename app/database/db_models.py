# Reference 1: https://analyzingalpha.com/create-an-equities-database
# Reference 2: https://analyzingalpha.com/create-price-database-postgresql-sqlalchemy

from datetime import datetime
from typing import Optional, List
from sqlalchemy.sql.functions import func
from sqlalchemy import ForeignKey
from sqlalchemy.types import (
    Integer,
    BigInteger,
    Float,
    Boolean,
    String,
    TIMESTAMP,
    Date,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Enum, UniqueConstraint
from typing_extensions import Annotated
import enum
from sqlalchemy.event import listens_for


# Creating a base class
class Base(DeclarativeBase):
    pass

# float column with double data type
float_double = Annotated[float, mapped_column(Float)]
# int column with BigInt data type
BigInt = Annotated[int, mapped_column("adj_volume", BigInteger)]


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class PriceFrequency(enum.Enum):
    one_second = "1 second"
    five_seconds = "5 seconds"
    ten_seconds = "10 seconds"
    fifteen_seconds = "15 seconds"
    thirty_seconds = "30 seconds"
    one_minute = "1 minute"
    three_minutes = "3 minutes"
    five_minutes = "5 minutes"
    fifteen_minutes = "15 minutes"
    thirty_minutes = "30 minutes"
    forty_five_minutes = "45 minutes"
    one_hour = "1 hour"
    two_hours = "2 hours"
    three_hours = "3 hours"
    four_hours = "4 hours"
    one_day = "1 day"
    one_week = "1 week"
    one_month = "1 month"
    three_months = "3 months"
    six_months = "6 months"
    twelve_months = "12 months"


class MarketDB(enum.Enum):
    crypto = "crypto"
    stock = "stock"
    forex = "forex"
    futures = "futures"


class DataVendorDB(Base, TimestampMixin):
    __tablename__ = "dim_data_vendor"
    __table_args__ = (
        UniqueConstraint("vendor_name", name="vendor_name"),
        dict(comment="List of data vendor sources"),
    )
    id: Mapped[int] = mapped_column("data_vendor_id", Integer, default=None, primary_key=True)
    vendor_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    website_url: Mapped[str] = mapped_column(String(100))
    support_email: Mapped[str] = mapped_column(String(100))
    securities: Mapped[List["SecurityDB"]] = relationship(back_populates="data_vendor")
    # daily_prices: Mapped[List["DailyPriceDB"]] = relationship(back_populates="data_vendor")
    # one_min_prices: Mapped[List["OneMinPriceDB"]] = relationship(back_populates="data_vendor")


class SecurityDB(Base, TimestampMixin):
    __tablename__ = "dim_security"
    id: Mapped[int] = mapped_column(
        "security_id", Integer, primary_key=True, autoincrement=True
    )
    code: Mapped[str] = mapped_column("code", String(7), nullable=False)
    currency: Mapped[str] = mapped_column("currency", String(3), nullable=False)
    ticker: Mapped[str] = mapped_column("ticker", String(12), nullable=False)
    name: Mapped[str] = mapped_column("name", String(200), nullable=False)
    figi: Mapped[Optional[str]] = mapped_column("figi", String(12))
    composite_figi: Mapped[Optional[str]] = mapped_column("composite_figi", String(12))
    share_class_figi: Mapped[Optional[str]] = mapped_column(
        "share_class_figi", String(12)
    )
    has_invalid_data: Mapped[Optional[str]] = mapped_column("has_invalid_data", Boolean)
    has_missing_company: Mapped[Optional[str]] = mapped_column(
        "has_missing_company", Boolean
    )
    market: Mapped["MarketDB"] = mapped_column("market", Enum(MarketDB), nullable=False)
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dim_exchange.exchange_id", onupdate="CASCADE", ondelete="RESTRICT"),
    )
    exchange: Mapped["ExchangeDB"] = relationship(back_populates="security")
    vendor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dim_data_vendor.data_vendor_id", onupdate="CASCADE", ondelete="RESTRICT"),
    )
    data_vendor: Mapped["DataVendorDB"] = relationship(back_populates="security")
    security_price: Mapped["SecurityPriceDB"] = relationship(back_populates="security")
    company: Mapped["SecurityDB"] = relationship(back_populates="security")
    stock_adjustment: Mapped["StockAdjustmentDB"] = relationship(
        back_populates="security"
    )
    # active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class ExchangeDB(Base, TimestampMixin):
    __tablename__ = "dim_exchange"
    id: Mapped[int] = mapped_column(
        "exchange_id", Integer, primary_key=True, autoincrement=True
    )
    mic: Mapped[str] = mapped_column("mic", String(10), unique=True, nullable=False)
    acronym: Mapped[str] = mapped_column("acronym", String(20))
    name: Mapped[str] = mapped_column("name", String(200), nullable=False)
    security: Mapped[List["SecurityDB"]] = relationship(back_populates="exchange")


class SecurityPriceDB(Base, TimestampMixin):
    __tablename__ = "dim_security_price"
    id: Mapped[int] = mapped_column("security_price_id", Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column("date", DateTime, nullable=False)
    open: Mapped[float_double]
    high: Mapped[float_double]
    low: Mapped[float_double]
    close: Mapped[float_double]
    volume: Mapped[BigInt]
    adj_open: Mapped[float_double]
    adj_high: Mapped[float_double]
    adj_low: Mapped[float_double]
    adj_close: Mapped[float_double]
    adj_volume: Mapped[BigInt] = mapped_column("adj_volume", BigInteger)
    # intraperiod: Mapped[bool] = mapped_column('intraperiod', Boolean, nullable=False)
    frequency: Mapped["PriceFrequency"] = mapped_column(
        "frequency", Enum(PriceFrequency), nullable=False
    )
    security_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dim_security.security_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    security: Mapped["SecurityDB"] = relationship(back_populates="security_price")
    UniqueConstraint(security_id, date)


class StockAdjustmentDB(Base, TimestampMixin):
    __tablename__ = "fact_stock_adjustment"
    id: Mapped[int] = mapped_column("stock_adjustment_id", Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column("date", Date, nullable=False)
    factor: Mapped[float] = mapped_column("factor", Float, nullable=False)
    dividend: Mapped[float_double]
    split_ratio: Mapped[float_double]
    security_id: Mapped["SecurityDB"] = mapped_column(
        Integer,
        ForeignKey("dim_security.security_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    security: Mapped["SecurityDB"] = relationship(back_populates="stock_adjustment")


class CompanyDB(Base, TimestampMixin):
    __tablename__ = "dim_company"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(100), nullable=False)
    cik: Mapped[str] = mapped_column("cik", String(10))
    description: Mapped[str] = mapped_column("description", String(2000))
    company_url: Mapped[str] = mapped_column("company_url", String(100))
    sic: Mapped[str] = mapped_column("sic", String(4))
    employees: Mapped[int] = mapped_column("employees", Integer)
    sector: Mapped[int] = mapped_column("sector", String(200))
    industry_category: Mapped[str] = mapped_column("industry_category", String(200))
    industry_group: Mapped[str] = mapped_column("industry_group", String(200))
    security_id: Mapped["SecurityDB"] = mapped_column(
        Integer,
        ForeignKey("dim_security.security_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    security: Mapped["SecurityDB"] = relationship(back_populates="company")


class FinancialStatementType(enum.Enum):
    balance_sheet = 'balance sheet'
    income_statement = 'income statement'
    cash_flow_statement = 'cash flow statement'


class FinancialStatementPeriod(enum.Enum):
    fy = 'fy'
    q1 = 'q1'
    q2 = 'q2'
    q3 = 'q3'
    q4 = 'q4'


class FinancialStatementDB(Base):
    __tablename__ = 'dim_financial_statement'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True)
    name: Mapped[int] = mapped_column(
        'name', String(100), nullable=False)


class FinancialStatementLineDB(Base):
    __tablename__ = 'dim_financial_statement_line'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True)
    tag: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(
        'name', String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column('description', String(1000))
    sequences: Mapped["FinancialStatementLineSequenceDB"] = relationship(backref="line")
    facts: Mapped['FinancialStatementFactDB']= relationship(backref='line')


class FinancialStatementLineSequenceDB(Base):
    __tablename__ = 'dim_financial_statement_line_sequence'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sequence: Mapped[int] = mapped_column('sequence', Integer, nullable=False)
    financial_statement_id: Mapped[int] = mapped_column(Integer,
                                    ForeignKey('dim_financial_statement.id',
                                               onupdate='CASCADE',
                                               ondelete='CASCADE'),
                                    nullable=False)
    financial_statement_line_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey('dim_financial_statement_line.id',
                                                    onupdate='CASCADE',
                                                    ondelete='CASCADE'),
                                         nullable=False)
    UniqueConstraint(financial_statement_id,
                     financial_statement_line_id)
    financial_statement: Mapped['FinancialStatementDB'] = relationship(backref="sequence")
    financial_statement_line: Mapped["FinancialStatementLineDB"]= relationship(backref='sequence')


class FinancialStatementLineAliasDB(Base):
    __tablename__ = 'dim_financial_statement_line_alias'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alias: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    financial_statement_line_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey('dim_financial_statement_line.id',
                                                    onupdate='CASCADE',
                                                    ondelete='CASCADE'),
                                         nullable=False)
    financial_statement_line: Mapped['FinancialStatementLineDB'] = relationship(backref="line_alias")


class FinancialStatementFactDB(Base):
    __tablename__ = 'fact_financial_statement_fact'
    __table_args__ = tuple(
        [UniqueConstraint('company_id',
                          'financial_statement_line_id',
                          'fiscal_year',
                          'fiscal_period')])
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    fiscal_period: Mapped[FinancialStatementPeriod] = mapped_column(
                            'fiscal_period',
                           Enum(FinancialStatementPeriod),
                           nullable=False)
    filing_date: Mapped[datetime] = mapped_column('filing_date', Date, nullable=False)
    start_date: Mapped[datetime] = mapped_column('start_date', Date)
    end_date: Mapped[datetime] = mapped_column('end_date', Date, nullable=False)
    amount: Mapped[float] = mapped_column('amount', Float, nullable=False)
    company_id: Mapped[int] = mapped_column(Integer,
                        ForeignKey('dim_company.id',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'),
                        nullable=False)
    financial_statement_line_id: Mapped[int] = mapped_column(
                                    Integer,
                                    ForeignKey('dim_financial_statement_line.id',
                                               onupdate='CASCADE',
                                               ondelete='CASCADE'),
                                    nullable=False)
    company: Mapped["CompanyDB"] = relationship(backref="financial_statement_fact")


"""
class PriceDB(MasterSQLModel):
    vendor_name: str = Field(foreign_key="dim_data_vendor.vendor_name")
    date: datetime = Field(nullable=False)
    symbol: str = Field(
        foreign_key="dim_companies.symbol", 
        nullable=False)
    open: float = Field(nullable=False)
    high: float = Field(nullable=False)
    low: float = Field(nullable=False)
    close: float = Field(nullable=False)
    volume: int = Field(sa_column=Column(BigInteger), nullable=False)


class DataVendorDB(MasterSQLModel, table=True):
    __tablename__ = "dim_data_vendor"
    __table_args__ = (
        UniqueConstraint("vendor_name", name="vendor_name"),
        dict(comment="List of data vendor sources"),
    )
    id: int = Field(default=None, primary_key=True)
    vendor_name: str= Field(index=True, nullable=False)
    website_url: str
    support_email: str
    companies: List["CompanyDB"] = Relationship(back_populates="data_vendor")
    daily_prices: List["DailyPriceDB"] = Relationship(back_populates="data_vendor")
    one_min_prices: List["OneMinPriceDB"] = Relationship(back_populates="data_vendor")


class CountriesDB(MasterSQLModel, table=True):
    __tablename__ = "dim_countries"
    country_id: Optional[int] = Field(default=None, primary_key=True)
    country: Optional[str] = Field(index=True)
    code: Optional[str]
    currency: Optional[str]
    companies: List["CompanyDB"] = Relationship(back_populates="countries")


class CompanyDB(MasterSQLModel, table=True):
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
    countries: Optional["CountriesDB"] = Relationship(back_populates="companies")
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
    one_min_prices: List["OneMinPriceDB"] = Relationship(back_populates="company")
    vendor_name: Optional[str] = Field(foreign_key="dim_data_vendor.vendor_name")
    data_vendor: Optional["DataVendorDB"] = Relationship(back_populates="companies")


class DailyPriceDB(PriceDB, table=True):
    __tablename__ = "fact_daily_price"
    __table_args__ = (dict(comment="Daily stock price of public listed companies"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    data_vendor: Optional["DataVendorDB"] = Relationship(back_populates="daily_prices")
    company: CompanyDB = Relationship(back_populates="daily_prices")
    adj_close: float


class OneMinPriceDB(PriceDB, table=True):
    __tablename__ = "fact_one_min_price"
    __table_args__ = (dict(comment="Daily stock price of public listed companies"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    data_vendor: Optional["DataVendorDB"] = Relationship(
        back_populates="one_min_prices"
    )
    company: Optional[CompaniesDB] = Relationship(back_populates="one_min_prices")
   
 
class IncomeStatement(MasterSQLModel, table=True):
    __tablename__ = "fact_income_statement"
    __table_args__ = (
        dict(comment="Historical income statement of public listed companies"),
    )
    id: Optional[int] = Field(primary_key=True, nullable=False)


class NewsDB(MasterSQLModel, table=True):
    __tablename__ = "fact_news"
    __table_args__ = (
        # UniqueConstraint("title", "author", name="title_author"),
        dict(comment="List of news of public listed companies"),
    )
    id: Optional[int] = Field(primary_key=True, nullable=False)
    symbol: Optional[str]
    title: Optional[str]
    author: Optional[str]
    description: Optional[str] = Field(sa_column=Column(TEXT))
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
    country: Optional[str]
    event: Optional[str]
    actual: Optional[str]
    consensus: Optional[str]
    previous: Optional[str]


class MacroIndicatorsDB(MasterSQLModel, table=True):
    __tablename__ = "fact_macro_indicators"
    id: Optional[int] = Field(primary_key=True, default=None)
    date: Optional[datetime]
    country: Optional[str]
    variable: Optional[str]
    value: Optional[int]
    unit: Optional[str]
    currency_or_measurement: Optional[str]


class NullDB(MasterSQLModel, table=True):
    # an empty database for testing purpose
    __tablename__ = "test"
    id: int = Field(default=None, primary_key=True)
"""
