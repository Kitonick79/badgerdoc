"""Add Categories tree

Revision ID: 66cd6054c2d0
Revises: f44cabeef963
Create Date: 2022-11-08 18:08:51.419245

"""
import sqlalchemy as sa
import sqlalchemy_utils

from alembic import op

# revision identifiers, used by Alembic.
revision = '66cd6054c2d0'
down_revision = 'f44cabeef963'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('tree', sqlalchemy_utils.types.ltree.LtreeType(), nullable=True))
    op.create_index('index_tree', 'categories', ['tree'], unique=False, postgresql_using='gist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('index_tree', table_name='categories', postgresql_using='gist')
    op.drop_column('categories', 'tree')
    # ### end Alembic commands ###
