"""update forum model

Revision ID: 0a01a4ebc0b4
Revises: 
Create Date: 2022-06-12 21:08:09.224361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a01a4ebc0b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('catalog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_catalog_id'), 'catalog', ['id'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('anonymous_name', sa.String(length=50), nullable=True),
    sa.Column('hashed_password', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_student', sa.Boolean(), nullable=True),
    sa.Column('is_employee', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_blocked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('anonymous_name')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    op.create_index(op.f('ix_appointment_id'), 'appointment', ['id'], unique=True)
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('image', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_article_id'), 'article', ['id'], unique=True)
    op.create_table('forum',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('catalog_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['catalog_id'], ['catalog.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_forum_id'), 'forum', ['id'], unique=True)
    op.create_table('verification_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(), nullable=True),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.email'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_verification_code_id'), 'verification_code', ['id'], unique=True)
    op.create_table('forum_discussion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('forum_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['forum_id'], ['forum.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forum_discussion_id'), 'forum_discussion', ['id'], unique=True)
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('forum_id', sa.Integer(), nullable=True),
    sa.Column('images', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['forum_id'], ['forum.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_id'), 'image', ['id'], unique=True)
    op.create_table('image_discussion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('forum_id', sa.Integer(), nullable=True),
    sa.Column('images', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['forum_id'], ['forum_discussion.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_discussion_id'), 'image_discussion', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_image_discussion_id'), table_name='image_discussion')
    op.drop_table('image_discussion')
    op.drop_index(op.f('ix_image_id'), table_name='image')
    op.drop_table('image')
    op.drop_index(op.f('ix_forum_discussion_id'), table_name='forum_discussion')
    op.drop_table('forum_discussion')
    op.drop_index(op.f('ix_verification_code_id'), table_name='verification_code')
    op.drop_table('verification_code')
    op.drop_index(op.f('ix_forum_id'), table_name='forum')
    op.drop_table('forum')
    op.drop_index(op.f('ix_article_id'), table_name='article')
    op.drop_table('article')
    op.drop_index(op.f('ix_appointment_id'), table_name='appointment')
    op.drop_table('appointment')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_catalog_id'), table_name='catalog')
    op.drop_table('catalog')
    # ### end Alembic commands ###
