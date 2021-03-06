"""empty message

Revision ID: 22d57adbc78d
Revises: b5e17459ff10
Create Date: 2016-12-19 22:50:39.326650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22d57adbc78d'
down_revision = 'b5e17459ff10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pickup_record',
    sa.Column('pickupRecordId', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('emailAddress', sa.String(length=120), nullable=True),
    sa.Column('streetNumber', sa.String(length=45), nullable=False),
    sa.Column('streetName', sa.String(length=120), nullable=False),
    sa.Column('neighbourhood', sa.String(length=80), nullable=True),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('pickupDate', sa.String(length=40), nullable=False),
    sa.Column('moneyLocation', sa.String(length=120), nullable=False),
    sa.Column('otherInstructions', sa.String(length=120), nullable=True),
    sa.Column('dateSubmitted', sa.DateTime(), nullable=False),
    sa.Column('source', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('pickupRecordId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pickup_record')
    # ### end Alembic commands ###
