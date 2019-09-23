"""empty message

Revision ID: 92414d7435e4
Revises: 7b90e0131061
Create Date: 2019-09-18 19:29:41.205536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92414d7435e4'
down_revision = '7b90e0131061'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('party', sa.Column('partyAbbreviation', sa.String(length=50), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('party', 'partyAbbreviation')
    ### end Alembic commands ###
