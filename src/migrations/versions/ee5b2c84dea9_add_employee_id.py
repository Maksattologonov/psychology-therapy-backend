"""add employee_id

Revision ID: ee5b2c84dea9
Revises: e7d7b1bf4c9c
Create Date: 2022-06-24 22:45:38.742572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee5b2c84dea9'
down_revision = 'e7d7b1bf4c9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appointment', sa.Column('employee_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'appointment', 'users', ['employee_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'appointment', type_='foreignkey')
    op.drop_column('appointment', 'employee_id')
    # ### end Alembic commands ###
