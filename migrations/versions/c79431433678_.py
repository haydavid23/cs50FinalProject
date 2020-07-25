"""empty message

Revision ID: c79431433678
Revises: aa6f8719e837
Create Date: 2020-07-25 22:43:40.452828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c79431433678'
down_revision = 'aa6f8719e837'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submited_assignments', 'submitedDate',
               existing_type=mysql.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submited_assignments', 'submitedDate',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###
