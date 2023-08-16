from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import UniqueConstraint
from sqlmodel import Column
from sqlalchemy.dialects.mysql import BIGINT, LONGTEXT, TEXT, VARCHAR
from typing import List


class MasterSQLModel(SQLModel):
    created_at: datetime = Field(
                        default=datetime.utcnow(),
                        nullable=False)
    updated_at: datetime = Field(
                        default=datetime.utcnow, 
                        nullable=False)


class PriceDB(MasterSQLModel):
    vendor_name: str = Field(foreign_key="dim_data_vendor.vendor_name")
    date: datetime = Field(nullable=False)
    symbol: Optional[str] = Field(
        foreign_key="dim_companies.symbol", 
        nullable=False)
    open: float = Field(nullable=False)
    high: float = Field(nullable=False)
    low: float = Field(nullable=False)
    close: float = Field(nullable=False)
    volume: int = Field(sa_column=Column(BIGINT), nullable=False)


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
    companies: List["CompaniesDB"] = Relationship(back_populates="data_vendor")
    daily_prices: List["DailyPriceDB"] = Relationship(back_populates="data_vendor")
    one_min_prices: List["OneMinPriceDB"] = Relationship(back_populates="data_vendor")


class CountriesDB(MasterSQLModel, table=True):
    __tablename__ = "dim_countries"
    country_id: Optional[int] = Field(default=None, primary_key=True)
    country: Optional[str] = Field(index=True)
    code: Optional[str]
    currency: Optional[str]
    companies: List["CompaniesDB"] = Relationship(back_populates="countries")


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
    company: CompaniesDB = Relationship(back_populates="daily_prices")
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
