"""fix fs_uniquifier in user model

Revision ID: f4161b623ee2
Revises: 523d565fc0fa
Create Date: 2025-02-02 19:09:39.659867

"""
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision = 'f4161b623ee2'
down_revision = '523d565fc0fa'
branch_labels = None
depends_on = None



def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fs_uniquifier', sa.String(length=255), nullable=False))
        batch_op.create_unique_constraint('uq_user_fs_uniquifier', ['fs_uniquifier'])

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_fs_uniquifier', type_='unique')
        batch_op.drop_column('fs_uniquifier')


    # ### end Alembic commands ###
