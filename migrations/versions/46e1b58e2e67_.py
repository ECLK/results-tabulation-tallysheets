"""empty message

Revision ID: 46e1b58e2e67
Revises: 0844f6026b55
Create Date: 2019-10-28 14:42:45.327266

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '46e1b58e2e67'
down_revision = '0844f6026b55'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'numberOfACoversRejected',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'numberOfAPacketsFound',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'numberOfBCoversRejected',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'numberOfValidBallotPapers',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'situation',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'timeOfCommencementOfCount',
               existing_type=mysql.DATETIME(),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'timeOfCommencementOfCount',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'situation',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'numberOfValidBallotPapers',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'numberOfBCoversRejected',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'numberOfAPacketsFound',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('tallySheetVersionRow_CE_201_PV_CC', 'numberOfACoversRejected',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    ### end Alembic commands ###
