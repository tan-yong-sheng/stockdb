# Reference 1: https://analyzingalpha.com/financial-statement-database
# still on the way

from datetime import datetime
import enum
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer,\
                       Date, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.event import listens_for
from app.db.security_model import Base, CompanyDB


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
    sequences: Mapped["FinancialStatementLineSequenceDB"] = relationship(back_ref="line")
    facts: Mapped['FinancialStatementFactDB'] = relationship(backref='line')


class FinancialStatementLineSequenceDB(Base):
    __tablename__ = 'dim_financial_statement_line_sequence'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sequence: Mapped[int] = mapped_column('sequence', Integer, nullable=False)
    financial_statement_id: Mapped[int] = mapped_column(Integer,
                                    ForeignKey('financial_statement.id',
                                               onupdate='CASCADE',
                                               ondelete='CASCADE'),
                                    nullable=False)
    financial_statement_line_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey('financial_statement_line.id',
                                                    onupdate='CASCADE',
                                                    ondelete='CASCADE'),
                                         nullable=False)
    UniqueConstraint('financial_statement_id',
                     'financial_statement_line_id')
    financial_statement: Mapped['FinancialStatementDB'] = relationship(backref="sequence")
    financial_statement_line: Mapped["FinancialStatementLineDB"]= relationship(backref='sequence')


class FinancialStatementLineAliasDB(Base):
    __tablename__ = 'financial_statement_line_alias'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alias: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    financial_statement_line_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey('financial_statement_line.id',
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
    company_id = Column(Integer,
                        ForeignKey('company.id',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'),
                        nullable=False)
    financial_statement_line_id = Column(
                                    Integer,
                                    ForeignKey('financial_statement_line.id',
                                               onupdate='CASCADE',
                                               ondelete='CASCADE'),
                                    nullable=False)

    company: Mapped["CompanyDB"] = relationship(backref="financial_statement_fact")