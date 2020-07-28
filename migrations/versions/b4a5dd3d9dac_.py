"""empty message

Revision ID: b4a5dd3d9dac
Revises: 1fdea8e876a0
Create Date: 2020-07-27 23:48:16.562143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4a5dd3d9dac'
down_revision = '1fdea8e876a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('key', sa.String(), nullable=True))
    op.add_column('accounts', sa.Column('salt', sa.String(), nullable=True))
    op.drop_column('accounts', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('accounts', 'salt')
    op.drop_column('accounts', 'key')
    # ### end Alembic commands ###
