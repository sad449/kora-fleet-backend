"""add personal and company fields to users

Revision ID: 6f4382fb4af6
Revises: 1c7febc0710a
Create Date: 2026-09-07 09:52:58.888324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = '6f4382fb4af6'
down_revision: Union[str, None] = '1c7febc0710a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('date_of_birth', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('national_id_number', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('users', sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    account_type_enum = sa.Enum('individual', 'company', name='accounttype')
    account_type_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('users', sa.Column('account_type', account_type_enum, nullable=False, server_default='individual'))
    op.add_column('users', sa.Column('company_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('users', sa.Column('position', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('users', sa.Column('certificate_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'certificate_url')
    op.drop_column('users', 'position')
    op.drop_column('users', 'company_name')
    op.drop_column('users', 'account_type')
    sa.Enum(name='accounttype').drop(op.get_bind(), checkfirst=True)
    op.drop_column('users', 'address')
    op.drop_column('users', 'national_id_number')
    op.drop_column('users', 'date_of_birth')