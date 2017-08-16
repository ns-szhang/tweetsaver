"""create_tweets

Revision ID: ac5fbcf9013c
Revises:
Create Date: 2017-08-15 13:46:02.510614

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ac5fbcf9013c'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('tweets',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True, unique=True),
        sa.Column('tweet_id', sa.BigInteger, nullable=False, unique=True),
        sa.Column('text', sa.String(200), nullable=False),
        sa.Column('screenshot_url', sa.String(25)),
        sa.Column('deleted', sa.Boolean(), default=False),
        sa.Column('added_on', sa.DateTime(), nullable=False)
    )

def downgrade():
    op.drop_table('tweets')
