"""empty message

Revision ID: f5401ae5033f
Revises: 6e56f04fd589
Create Date: 2020-07-04 22:43:43.516501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5401ae5033f'
down_revision = '6e56f04fd589'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assigned_assigments', sa.Column('note', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assigned_assigments', 'note')
    # ### end Alembic commands ###
