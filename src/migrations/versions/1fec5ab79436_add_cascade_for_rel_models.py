"""add cascade for rel models

Revision ID: 1fec5ab79436
Revises: 5b741b2fa00b
Create Date: 2022-03-16 16:10:18.026035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fec5ab79436'
down_revision = '5b741b2fa00b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('images_forum_id_fkey', 'images', type_='foreignkey')
    op.create_foreign_key(None, 'images', 'forum', ['forum_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('images_forum_discussion_forum_id_fkey', 'images_forum_discussion', type_='foreignkey')
    op.create_foreign_key(None, 'images_forum_discussion', 'forum_discussion', ['forum_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('verification_code_user_fkey', 'verification_code', type_='foreignkey')
    op.create_foreign_key(None, 'verification_code', 'users', ['user'], ['email'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'verification_code', type_='foreignkey')
    op.create_foreign_key('verification_code_user_fkey', 'verification_code', 'users', ['user'], ['email'])
    op.drop_constraint(None, 'images_forum_discussion', type_='foreignkey')
    op.create_foreign_key('images_forum_discussion_forum_id_fkey', 'images_forum_discussion', 'forum_discussion', ['forum_id'], ['id'])
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.create_foreign_key('images_forum_id_fkey', 'images', 'forum', ['forum_id'], ['id'])
    # ### end Alembic commands ###