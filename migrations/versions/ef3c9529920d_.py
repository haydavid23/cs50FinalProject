"""empty message

Revision ID: ef3c9529920d
Revises: bcd28c74d56f
Create Date: 2020-07-08 21:12:59.488581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef3c9529920d'
down_revision = 'bcd28c74d56f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submited_assigments', sa.Column('assigmentFile', sa.String(length=80), nullable=True))
    op.add_column('submited_assigments', sa.Column('submitedDate', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('submited_assigments', 'submitedDate')
    op.drop_column('submited_assigments', 'assigmentFile')
    # ### end Alembic commands ###