"""empty message

Revision ID: 5072ee613b92
Revises: 25f675d00526
Create Date: 2020-07-09 19:02:25.860048

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5072ee613b92'
down_revision = '25f675d00526'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assigned_assignments', 'name',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)
    op.alter_column('assigned_assignments', 'semesterId',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('assigned_assignments', 'subjectId',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assigned_assignments', 'subjectId',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('assigned_assignments', 'semesterId',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('assigned_assignments', 'name',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
    # ### end Alembic commands ###
