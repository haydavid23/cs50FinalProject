"""empty message

Revision ID: 06a0dae9a605
Revises: 5072ee613b92
Create Date: 2020-07-13 13:21:45.481972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06a0dae9a605'
down_revision = '5072ee613b92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assigned_assignments', sa.Column('assignedDate', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assigned_assignments', 'assignedDate')
    # ### end Alembic commands ###
