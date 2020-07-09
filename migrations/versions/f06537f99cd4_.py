"""empty message

Revision ID: f06537f99cd4
Revises: a9ab650a82af
Create Date: 2020-07-09 13:11:29.417229

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f06537f99cd4'
down_revision = 'a9ab650a82af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submited_assigments', sa.Column('assignmentName', sa.String(length=100), nullable=False))
    op.create_unique_constraint(None, 'submited_assigments', ['studentId', 'subject', 'assignmentName'])
    op.drop_column('submited_assigments', 'assigmentName')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submited_assigments', sa.Column('assigmentName', mysql.VARCHAR(length=100), nullable=False))
    op.drop_constraint(None, 'submited_assigments', type_='unique')
    op.drop_column('submited_assigments', 'assignmentName')
    # ### end Alembic commands ###