"""create alert_info table

Revision ID: d4a931748386
Revises: 
Create Date: 2022-05-18 20:46:42.554608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4a931748386'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'travel_info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('country_name', sa.String(255), nullable=False),
        sa.Column('travel_alerts', sa.String(200)),
        sa.Column('status_date', sa.String(50), nullable=False),
        sa.Column('link', sa.String(255), nullable=False),
        sa.Column('information', sa.Text, nullable=False),
        sa.Column('key_encode', sa.String(100))
    ),
    op.create_unique_constraint("uq_travel_info", "travel_info", ["key_encode"])


def downgrade():
     op.drop_table('travel_info')

