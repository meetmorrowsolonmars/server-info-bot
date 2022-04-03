"""drop schemas ram_info cpu_info disk_info

Revision ID: 4a26ad1e679f
Revises: 9f756cf4e3f3
Create Date: 2022-04-03 22:16:12.020091

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '4a26ad1e679f'
down_revision = '9f756cf4e3f3'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('cpu_info')
    op.drop_table('ram_info')
    op.drop_table('disk_info')


def downgrade():
    pass
