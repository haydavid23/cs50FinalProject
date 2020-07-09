"""empty message

Revision ID: c6f43e030700
Revises: ef3c9529920d
Create Date: 2020-07-08 21:19:42.241775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c6f43e030700'
down_revision = 'ef3c9529920d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submited_assigments', 'submitedDate',
               existing_type=mysql.VARCHAR(length=80),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submited_assigments', 'submitedDate',
               existing_type=mysql.VARCHAR(length=80),
               nullable=True)
    # ### end Alembic commands ###