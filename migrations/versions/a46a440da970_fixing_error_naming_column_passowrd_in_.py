"""Fixing error (naming column passowrd in stead of password_hash)

Revision ID: a46a440da970
Revises: a2a8e0fe1f76
Create Date: 2022-11-27 17:48:00.562253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a46a440da970'
down_revision = 'a2a8e0fe1f76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=128), nullable=True))
    op.drop_column('user', 'password_hash')
    # ### end Alembic commands ###