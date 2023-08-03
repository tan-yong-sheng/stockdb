"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import logging
from app.decorators import log_start_end
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

logger = logging.getLogger(__name__)

@log_start_end(log=logger)
def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

@log_start_end(log=logger)
def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
