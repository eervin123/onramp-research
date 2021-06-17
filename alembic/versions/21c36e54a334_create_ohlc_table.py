"""Create OHLC table

Revision ID: 21c36e54a334
Revises: 9c10f7f80e30
Create Date: 2021-06-08 23:18:58.607308

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '21c36e54a335'
down_revision = '9c10f7f80e30'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "close_data",
        sa.Column("symbol", sa.String, primary_key=True),
        sa.Column("close", sa.Float),
        sa.Column("date", sa.Date)
    )


def downgrade():
    op.drop_table("close_data")
