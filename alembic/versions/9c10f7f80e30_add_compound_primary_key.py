"""Add compound primary key

Revision ID: 9c10f7f80e30
Revises: e83ac4c81959
Create Date: 2021-06-08 22:25:31.657224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c10f7f80e30'
down_revision = 'e83ac4c81959'
branch_labels = None
depends_on = None


def upgrade():
    op.create_primary_key(
                "pk_cryptocurrency_pairs", "cryptocurrency_pairs",
                ["asset_1", "asset_2", "datetime"]
            )


def downgrade():
    op.drop_constraint("pk_cryptocurrency_pairs", "cryptocurrency_pairs")
