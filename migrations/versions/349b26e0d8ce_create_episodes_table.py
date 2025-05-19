"""Create episodes table

Revision ID: 349b26e0d8ce
Revises: 
Create Date: 2025-05-09 14:37:57.320168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '349b26e0d8ce'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'episodes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('season', sa.Integer(), nullable=False),
        sa.Column('episode_num', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('characters', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        # This ensures you can't have duplicate episode numbers within the same season
        sa.UniqueConstraint('season', 'episode_num', name='unique_episode_in_season')
    )

def downgrade() -> None:
    op.drop_table('episodes')
