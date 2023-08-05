"""empty message

Revision ID: 29ca995cdc8f
Revises: 2720618578ea
Create Date: 2023-08-02 21:36:09.218896

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import logging
from app.decorators import log_start_end


# revision identifiers, used by Alembic.
revision = "29ca995cdc8f"
down_revision = "2720618578ea"
branch_labels = None
depends_on = None

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_dim_data_vendor_name", table_name="dim_data_vendor")
    op.create_index(
        op.f("ix_dim_data_vendor_vendor_name"),
        "dim_data_vendor",
        ["vendor_name"],
        unique=False,
    )
    # ### end Alembic commands ###


@log_start_end(log=logger)
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_dim_data_vendor_vendor_name"), table_name="dim_data_vendor")
    op.create_index(
        "ix_dim_data_vendor_name", "dim_data_vendor", ["vendor_name"], unique=False
    )
    # ### end Alembic commands ###