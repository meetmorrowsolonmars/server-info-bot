"""send info  message

Revision ID: 9f756cf4e3f3
Revises: 59524fcd2e29
Create Date: 2022-02-27 18:48:38.278595

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9f756cf4e3f3'
down_revision = '59524fcd2e29'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sent_messages',
        sa.Column('type', sa.String(32), primary_key=True),
        sa.Column('timestamp', sa.DateTime, primary_key=True),
    )


def downgrade():
    op.drop_table('sent_messages')
