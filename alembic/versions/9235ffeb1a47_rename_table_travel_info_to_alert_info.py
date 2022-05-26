"""rename table travel_info to alert_info

Revision ID: 9235ffeb1a47
Revises: d4a931748386
Create Date: 2022-05-18 20:48:21.260456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9235ffeb1a47'
down_revision = 'd4a931748386'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('travel_info', 'alert_info')
    pass


def downgrade():
    op.rename_table('alert_info', 'travel_info')
    pass
