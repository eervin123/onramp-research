"""baseline

Revision ID: e83ac4c81959
Revises: 
Create Date: 2021-06-08 20:14:22.906269

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e83ac4c81959'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "cryptocurrency_pairs",
        sa.Column('asset_1', sa.String),
        sa.Column('asset_2', sa.String),
        sa.Column('price_close', sa.Float),
        sa.Column('price_high', sa.Float),
        sa.Column('price_low', sa.Float),
        sa.Column('price_open', sa.Float),
        sa.Column('volume', sa.Float),
        sa.Column('datetime', sa.DateTime)
    )


def downgrade():
    op.drop_table("cryptocurrency_pairs")
