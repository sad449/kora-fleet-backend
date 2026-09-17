"""add must_change_password and profile_completed to users

Revision ID: 7d99e487fbe9
Revises: 1c02cceca21e
Create Date: 2026-09-10 10:39:36.492751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = '7d99e487fbe9'
down_revision: Union[str, None] = '1c02cceca21e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('must_change_password', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('users', sa.Column('profile_completed', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    op.drop_column('users', 'profile_completed')
    op.drop_column('users', 'must_change_password')