"""empty message

Revision ID: 18cf36b5c13d
Revises: bfeea52e9270
Create Date: 2023-08-12 01:08:33.106054

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import logging
from app.decorators import log_start_end
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "18cf36b5c13d"
down_revision = "bfeea52e9270"
branch_labels = None
depends_on = None

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index('ix_dim_companies_symbol', table_name='dim_companies')
    op.create_index(
        op.f("ix_dim_companies_symbol"), "dim_companies", ["symbol"], unique=True
    )
    op.alter_column(
        "dim_countries", "created_at", existing_type=mysql.DATETIME(), nullable=True
    )
    op.alter_column(
        "dim_countries", "updated_at", existing_type=mysql.DATETIME(), nullable=True
    )
    op.alter_column(
        "dim_data_vendor", "created_at", existing_type=mysql.DATETIME(), nullable=True
    )
    op.alter_column(
        "dim_data_vendor", "updated_at", existing_type=mysql.DATETIME(), nullable=True
    )
    op.drop_index("vendor_name", table_name="dim_data_vendor")
    op.drop_index("ix_dim_data_vendor_vendor_name", table_name="dim_data_vendor")
    op.create_index(
        op.f("ix_dim_data_vendor_vendor_name"),
        "dim_data_vendor",
        ["vendor_name"],
        unique=True,
    )
    op.alter_column(
        "dim_macro_parameters",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "dim_macro_parameters",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.add_column("fact_daily_price", sa.Column("dividend", sa.Float(), nullable=True))
    op.add_column(
        "fact_daily_price",
        sa.Column("split_ratio_numerator", sa.Integer(), nullable=True),
    )
    op.add_column(
        "fact_daily_price",
        sa.Column("split_ratio_denominator", sa.Integer(), nullable=True),
    )
    op.alter_column(
        "fact_daily_price", "created_at", existing_type=mysql.DATETIME(), nullable=True
    )
    op.alter_column(
        "fact_daily_price", "updated_at", existing_type=mysql.DATETIME(), nullable=True
    )
    op.create_foreign_key(
        None, "fact_daily_price", "dim_companies", ["symbol"], ["symbol"]
    )
    op.alter_column(
        "fact_economic_calendar",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "fact_economic_calendar",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "fact_income_statement",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "fact_income_statement",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "fact_macro_indicators",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "fact_macro_indicators",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "fact_news", "created_at", existing_type=mysql.DATETIME(), nullable=True
    )
    op.alter_column(
        "fact_news", "updated_at", existing_type=mysql.DATETIME(), nullable=True
    )
    op.alter_column(
        "fact_one_min_price",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "fact_one_min_price",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=True,
    )
    op.drop_column("fact_one_min_price", "adj_close")
    op.alter_column("test", "created_at", existing_type=mysql.DATETIME(), nullable=True)
    op.alter_column("test", "updated_at", existing_type=mysql.DATETIME(), nullable=True)
    # ### end Alembic commands ###


@log_start_end(log=logger)
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "test", "updated_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.alter_column(
        "test", "created_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.add_column(
        "fact_one_min_price", sa.Column("adj_close", mysql.FLOAT(), nullable=True)
    )
    op.alter_column(
        "fact_one_min_price",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "fact_one_min_price",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "fact_news", "updated_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.alter_column(
        "fact_news", "created_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.alter_column(
        "fact_macro_indicators",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "fact_macro_indicators",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "fact_income_statement",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "fact_income_statement",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "fact_economic_calendar",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "fact_economic_calendar",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.drop_constraint(None, "fact_daily_price", type_="foreignkey")
    op.alter_column(
        "fact_daily_price", "updated_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.alter_column(
        "fact_daily_price", "created_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.drop_column("fact_daily_price", "split_ratio_denominator")
    op.drop_column("fact_daily_price", "split_ratio_numerator")
    op.drop_column("fact_daily_price", "dividend")
    op.alter_column(
        "dim_macro_parameters",
        "updated_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "dim_macro_parameters",
        "created_at",
        existing_type=mysql.DATETIME(),
        nullable=False,
    )
    op.drop_index(op.f("ix_dim_data_vendor_vendor_name"), table_name="dim_data_vendor")
    op.create_index(
        "ix_dim_data_vendor_vendor_name",
        "dim_data_vendor",
        ["vendor_name"],
        unique=False,
    )
    op.create_index("vendor_name", "dim_data_vendor", ["vendor_name"], unique=False)
    op.alter_column(
        "dim_data_vendor", "updated_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.alter_column(
        "dim_data_vendor", "created_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.alter_column(
        "dim_countries", "updated_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.alter_column(
        "dim_countries", "created_at", existing_type=mysql.DATETIME(), nullable=False
    )
    op.drop_index(op.f("ix_dim_companies_symbol"), table_name="dim_companies")
    op.create_index(
        "ix_dim_companies_symbol", "dim_companies", ["symbol"], unique=False
    )
    # ### end Alembic commands ###
