"""empty message

Revision ID: e35e0443310a
Revises: 2d2337da2d99
Create Date: 2020-07-14 02:01:29.826115

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e35e0443310a'
down_revision = '2d2337da2d99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assigned_assignments', 'submittable',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assigned_assignments', 'submittable',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    # ### end Alembic commands ###
