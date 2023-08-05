"""empty message

Revision ID: 63fcda26eefe
Revises: 024d9269b054
Create Date: 2023-08-05 15:08:18.053433

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import logging
from app.decorators import log_start_end


# revision identifiers, used by Alembic.
revision = '63fcda26eefe'
down_revision = '024d9269b054'
branch_labels = None
depends_on = None

logger = logging.getLogger(__name__)

@log_start_end(log=logger)
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fact_one_min_price',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('vendor_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('adj_close', sa.Float(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['symbol'], ['dim_companies.symbol'], ),
    sa.ForeignKeyConstraint(['vendor_name'], ['dim_data_vendor.vendor_name'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='Daily stock price of public listed companies'
    )
    # ### end Alembic commands ###

@log_start_end(log=logger)
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fact_one_min_price')
    # ### end Alembic commands ###