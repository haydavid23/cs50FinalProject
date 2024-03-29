"""empty message

Revision ID: 21fe9def6352
Revises: 0ccf8b6e186b
Create Date: 2020-07-23 01:36:57.312641

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '21fe9def6352'
down_revision = '0ccf8b6e186b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students_grades', sa.Column('schoolTermId', sa.Integer(), nullable=False))
    op.drop_index('studentId', table_name='students_grades')
    op.create_unique_constraint(None, 'students_grades', ['studentId', 'subjectId', 'schoolTermId'])
    op.drop_column('students_grades', 'semesterId')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students_grades', sa.Column('semesterId', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'students_grades', type_='unique')
    op.create_index('studentId', 'students_grades', ['studentId', 'subjectId', 'semesterId'], unique=True)
    op.drop_column('students_grades', 'schoolTermId')
    # ### end Alembic commands ###
