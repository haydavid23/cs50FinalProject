"""empty message

Revision ID: 87f3d2fc47c4
Revises: 3489dbf21e2f
Create Date: 2020-07-23 03:17:12.536900

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '87f3d2fc47c4'
down_revision = '3489dbf21e2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students_grades', sa.Column('gradeAvg', sa.Integer(), nullable=False))
    op.add_column('students_grades', sa.Column('gradeLetter', sa.String(length=5), nullable=False))
    op.alter_column('students_grades', 'gradeLevel',
               existing_type=mysql.VARCHAR(length=80),
               nullable=True)
    op.drop_column('students_grades', 'grade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students_grades', sa.Column('grade', mysql.VARCHAR(length=80), nullable=False))
    op.alter_column('students_grades', 'gradeLevel',
               existing_type=mysql.VARCHAR(length=80),
               nullable=False)
    op.drop_column('students_grades', 'gradeLetter')
    op.drop_column('students_grades', 'gradeAvg')
    # ### end Alembic commands ###
