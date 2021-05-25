"""Movies table

Revision ID: f478b6cd02c8
Revises: ffb0ad5ebd19
Create Date: 2021-05-24 15:05:40.335331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f478b6cd02c8'
down_revision = 'ffb0ad5ebd19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('m_count', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'm_count')
    # ### end Alembic commands ###
