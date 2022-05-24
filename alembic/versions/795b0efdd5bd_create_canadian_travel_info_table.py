"""create canadian travel_info table

Revision ID: 795b0efdd5bd
Revises: 9235ffeb1a47
Create Date: 2022-05-23 20:52:07.849338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '795b0efdd5bd'
down_revision = '9235ffeb1a47'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'canadian_travel_info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('country_name', sa.String(255), nullable=False),
        sa.Column('alert_text', sa.String(200)),
        sa.Column('last_updated', sa.String(50), nullable=False),
        sa.Column('risk_heading', sa.String(255), nullable=False),
        sa.Column('risk_information', sa.Text, nullable=False),
        sa.Column('country_security', sa.Text, nullable=False),
        sa.Column('criteria', sa.Text, nullable=False),
        sa.Column('health', sa.Text, nullable=False),
        sa.Column('laws', sa.Text, nullable=False), 
        sa.Column('natural_disaster', sa.Text, nullable=False),
        sa.Column('canadian_key_encode', sa.String(100))
    ),
    op.create_unique_constraint("uq_canadian_travel_info", "canadian_travel_info", ["canadian_key_encode"])


def downgrade():
    op.drop_table('canadian_travel_info')
