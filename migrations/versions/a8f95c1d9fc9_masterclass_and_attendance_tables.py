"""Masterclass and attendance tables

Revision ID: a8f95c1d9fc9
Revises: f913baa07969
Create Date: 2024-02-26 14:28:45.338870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8f95c1d9fc9'
down_revision = 'f913baa07969'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('masterclasses',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('context', sa.Text(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    with op.batch_alter_table('masterclasses', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_masterclasses_createdAt'), ['createdAt'], unique=False)
        batch_op.create_index(batch_op.f('ix_masterclasses_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_masterclasses_updatedAt'), ['updatedAt'], unique=False)

    op.create_table('attendance',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['masterclasses.uid'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    with op.batch_alter_table('masterclasses', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_masterclasses_updatedAt'))
        batch_op.drop_index(batch_op.f('ix_masterclasses_name'))
        batch_op.drop_index(batch_op.f('ix_masterclasses_createdAt'))

    op.drop_table('masterclasses')
    # ### end Alembic commands ###
