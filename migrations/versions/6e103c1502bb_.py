"""empty message

Revision ID: 6e103c1502bb
Revises: db2b1f6271e5
Create Date: 2020-07-28 00:42:22.526067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e103c1502bb'
down_revision = 'db2b1f6271e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('password', sa.String(length=255), nullable=False))
    op.drop_column('accounts', 'salt')
    op.drop_column('accounts', 'key')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('key', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('accounts', sa.Column('salt', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('accounts', 'password')
    # ### end Alembic commands ###
