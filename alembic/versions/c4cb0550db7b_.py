"""empty message

Revision ID: c4cb0550db7b
Revises: 99dc8fe6ac5f
Create Date: 2023-08-11 23:04:53.496291

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import logging
from app.decorators import log_start_end
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "c4cb0550db7b"
down_revision = "99dc8fe6ac5f"
branch_labels = None
depends_on = None

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_dim_companies_symbol", table_name="dim_companies")
    op.create_index(
        op.f("ix_dim_companies_symbol"), "dim_companies", ["symbol"], unique=True
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
        "fact_daily_price",
        "symbol",
        existing_type=mysql.VARCHAR(length=255),
        nullable=True,
    )
    op.drop_constraint(
        "fact_daily_price_ibfk_3", "fact_daily_price", type_="foreignkey"
    )
    op.drop_constraint(
        "fact_daily_price_ibfk_2", "fact_daily_price", type_="foreignkey"
    )
    op.alter_column(
        "fact_one_min_price",
        "symbol",
        existing_type=mysql.VARCHAR(length=255),
        nullable=True,
    )
    op.drop_constraint(
        "fact_one_min_price_ibfk_1", "fact_one_min_price", type_="foreignkey"
    )
    op.drop_constraint(
        "fact_one_min_price_ibfk_2", "fact_one_min_price", type_="foreignkey"
    )
    op.drop_column("fact_one_min_price", "adj_close")
    # ### end Alembic commands ###


@log_start_end(log=logger)
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "fact_one_min_price", sa.Column("adj_close", mysql.FLOAT(), nullable=True)
    )
    op.create_foreign_key(
        "fact_one_min_price_ibfk_2",
        "fact_one_min_price",
        "dim_data_vendor",
        ["vendor_name"],
        ["vendor_name"],
    )
    op.create_foreign_key(
        "fact_one_min_price_ibfk_1",
        "fact_one_min_price",
        "dim_companies",
        ["symbol"],
        ["symbol"],
    )
    op.alter_column(
        "fact_one_min_price",
        "symbol",
        existing_type=mysql.VARCHAR(length=255),
        nullable=False,
    )
    op.create_foreign_key(
        "fact_daily_price_ibfk_2",
        "fact_daily_price",
        "dim_companies",
        ["symbol"],
        ["symbol"],
    )
    op.create_foreign_key(
        "fact_daily_price_ibfk_3",
        "fact_daily_price",
        "dim_data_vendor",
        ["vendor_name"],
        ["vendor_name"],
    )
    op.alter_column(
        "fact_daily_price",
        "symbol",
        existing_type=mysql.VARCHAR(length=255),
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
    op.drop_index(op.f("ix_dim_companies_symbol"), table_name="dim_companies")
    op.create_index(
        "ix_dim_companies_symbol", "dim_companies", ["symbol"], unique=False
    )
    # ### end Alembic commands ###
