"""Fixes

Revision ID: e7ee40bec423
Revises: a8f95c1d9fc9
Create Date: 2024-02-26 14:34:06.487731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7ee40bec423'
down_revision = 'a8f95c1d9fc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('masterclass_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('attendance_class_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'masterclasses', ['masterclass_id'], ['uid'])
        batch_op.drop_column('class_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('class_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('attendance_class_id_fkey', 'masterclasses', ['class_id'], ['uid'])
        batch_op.drop_column('masterclass_id')

    # ### end Alembic commands ###