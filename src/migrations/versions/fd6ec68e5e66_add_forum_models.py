"""add forum models

Revision ID: fd6ec68e5e66
Revises: 1e108fc73a16
Create Date: 2022-02-03 21:09:05.627585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd6ec68e5e66'
down_revision = '1e108fc73a16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('images', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=True)
    op.create_table('forum',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('images_id', sa.Integer(), nullable=True),
    sa.Column('is_anonymous', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['images_id'], ['images.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forum_id'), 'forum', ['id'], unique=True)
    op.create_table('forum_discussion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('forum_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('is_anonymous', sa.Boolean(), nullable=True),
    sa.Column('images_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['forum_id'], ['forum.id'], ),
    sa.ForeignKeyConstraint(['images_id'], ['images.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forum_discussion_id'), 'forum_discussion', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_forum_discussion_id'), table_name='forum_discussion')
    op.drop_table('forum_discussion')
    op.drop_index(op.f('ix_forum_id'), table_name='forum')
    op.drop_table('forum')
    op.drop_index(op.f('ix_images_id'), table_name='images')
    op.drop_table('images')
    # ### end Alembic commands ###