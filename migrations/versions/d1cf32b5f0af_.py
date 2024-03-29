"""empty message

Revision ID: d1cf32b5f0af
Revises: f436db3360b2
Create Date: 2020-08-11 03:17:32.387001

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd1cf32b5f0af'
down_revision = 'f436db3360b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assigned_assignments', sa.Column('assignmentName', sa.String(length=30), nullable=False))
    op.drop_index('name', table_name='assigned_assignments')
    op.create_unique_constraint(None, 'assigned_assignments', ['assignmentName', 'schoolTermId'])
    op.drop_column('assigned_assignments', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assigned_assignments', sa.Column('name', mysql.VARCHAR(length=30), nullable=False))
    op.drop_constraint(None, 'assigned_assignments', type_='unique')
    op.create_index('name', 'assigned_assignments', ['name', 'schoolTermId'], unique=True)
    op.drop_column('assigned_assignments', 'assignmentName')
    # ### end Alembic commands ###
