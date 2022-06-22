"""change models 5

Revision ID: e7d7b1bf4c9c
Revises: 90ab7df9215c
Create Date: 2022-06-22 12:14:28.835121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7d7b1bf4c9c'
down_revision = '90ab7df9215c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('date_time', sa.String(length=50), nullable=True))
    op.drop_constraint('appointment_date_key', 'appointment', type_='unique')
    op.create_unique_constraint(None, 'appointment', ['date_time'])
    op.drop_column('appointment', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('date', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'appointment', type_='unique')
    op.create_unique_constraint('appointment_date_key', 'appointment', ['date'])
    op.drop_column('appointment', 'date_time')
    # ### end Alembic commands ###
