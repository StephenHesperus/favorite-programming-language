"""empty message

Revision ID: c05c4e65edac
Revises: None
Create Date: 2016-04-17 19:41:24.612802

"""

# revision identifiers, used by Alembic.
revision = 'c05c4e65edac'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('languagetests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=200), nullable=False),
    sa.Column('answer', sa.Boolean(), nullable=False),
    sa.Column('language', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('languagetests')
    ### end Alembic commands ###
