"""create common info table

Revision ID: a23d4196b276
Revises: 4a26ad1e679f
Create Date: 2022-04-03 22:19:09.212187

"""
import sqlalchemy as sa
from alembic import op

from src.models.system_load_type import SystemLoadType

# revision identifiers, used by Alembic.
revision = 'a23d4196b276'
down_revision = '4a26ad1e679f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'system_load_statistics',
        sa.Column('type', sa.Enum(SystemLoadType), primary_key=True),
        sa.Column('timestamp', sa.DateTime, primary_key=True),
        sa.Column('percent', sa.Float),
    )

    op.create_table(
        'disk_space_statistics',
        sa.Column('mount_point', sa.String(length=128), primary_key=True),
        sa.Column('timestamp', sa.DateTime, primary_key=True),
        sa.Column('percent', sa.Float),
        sa.Column('total', sa.BigInteger),
        sa.Column('used', sa.BigInteger),
        sa.Column('available', sa.BigInteger),
        sa.Column('device', sa.String(length=128)),
    )


def downgrade():
    op.drop_table('system_load_statistics')
    op.drop_table('disk_space_statistics')
