"""empty message

Revision ID: 1cec5e4d48ba
Revises: 87f3d2fc47c4
Create Date: 2020-07-23 13:27:58.108419

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1cec5e4d48ba'
down_revision = '87f3d2fc47c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submited_assignments', 'submitedDate',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submited_assignments', 'submitedDate',
               existing_type=mysql.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###
