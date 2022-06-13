"""update forum model add catalog

Revision ID: 8309f69d42b7
Revises: 0a01a4ebc0b4
Create Date: 2022-06-13 11:37:09.912335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8309f69d42b7'
down_revision = '0a01a4ebc0b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('forum', 'catalog_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('forum', 'catalog_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
