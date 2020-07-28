"""empty message

Revision ID: db2b1f6271e5
Revises: aab43e821e31
Create Date: 2020-07-28 00:35:07.538771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db2b1f6271e5'
down_revision = 'aab43e821e31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'key',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('accounts', 'salt',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'salt',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('accounts', 'key',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
