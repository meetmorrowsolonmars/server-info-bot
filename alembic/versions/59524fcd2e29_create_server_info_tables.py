"""create server info tables

Revision ID: 59524fcd2e29
Revises: 
Create Date: 2022-02-27 15:16:08.559015

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '59524fcd2e29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cpu_info',
        sa.Column('timestamp', sa.DateTime, primary_key=True),
        sa.Column('percent', sa.Float, index=True),
        sa.Column('user', sa.Float),
        sa.Column('nice', sa.Float),
        sa.Column('system', sa.Float),
        sa.Column('idle', sa.Float),
    )

    op.create_table(
        'ram_info',
        sa.Column('timestamp', sa.DateTime, primary_key=True),
        sa.Column('percent', sa.Float, index=True),
        sa.Column('total', sa.Float),
        sa.Column('available', sa.Float),
        sa.Column('used', sa.Float),
    )

    op.create_table(
        'disk_info',
        sa.Column('timestamp', sa.DateTime, primary_key=True),
        sa.Column('mountpoint', sa.String(length=128), primary_key=True),
        sa.Column('device', sa.String(length=128)),
        sa.Column('percent', sa.Float, index=True),
        sa.Column('total', sa.BigInteger),
        sa.Column('used', sa.BigInteger),
        sa.Column('free', sa.BigInteger),
    )


def downgrade():
    op.drop_table('cpu_info')
    op.drop_table('ram_info')
    op.drop_table('disk_info')
