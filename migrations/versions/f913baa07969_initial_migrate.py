"""Initial migrate

Revision ID: f913baa07969
Revises: 
Create Date: 2024-02-25 18:47:05.113956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f913baa07969'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('father_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('school_name', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_father_name'), ['father_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_last_name'), ['last_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_login'), ['login'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_school_name'), ['school_name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_school_name'))
        batch_op.drop_index(batch_op.f('ix_users_login'))
        batch_op.drop_index(batch_op.f('ix_users_last_name'))
        batch_op.drop_index(batch_op.f('ix_users_first_name'))
        batch_op.drop_index(batch_op.f('ix_users_father_name'))

    op.drop_table('users')
    # ### end Alembic commands ###
