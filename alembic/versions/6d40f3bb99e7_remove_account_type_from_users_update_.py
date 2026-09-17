"""remove account_type from users, update company_profiles

Revision ID: 33ab7c4ca920
Revises: 6c1803731e4b
Create Date: 2026-09-17 09:55:20.384322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from sqlalchemy.dialects import postgresql


revision: str = '33ab7c4ca920'
down_revision: Union[str, None] = '6c1803731e4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    company_type_enum = sa.Enum('solo', 'company', name='companytype')
    company_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('company_profiles', sa.Column(
        'company_type', company_type_enum,
        nullable=False, server_default='solo'
    ))

    op.alter_column('company_profiles', 'company_registered_date',
        existing_type=sa.VARCHAR(),
        type_=sa.Date(),
        existing_nullable=True,
        postgresql_using='company_registered_date::date'
    )

    op.drop_column('company_profiles', 'status')
    op.drop_column('users', 'account_type')


def downgrade() -> None:
    op.add_column('users', sa.Column('account_type', sa.VARCHAR(), nullable=True))
    op.add_column('company_profiles', sa.Column('status', sa.VARCHAR(), nullable=True))
    op.drop_column('company_profiles', 'company_type')
    sa.Enum(name='companytype').drop(op.get_bind(), checkfirst=True)
    op.alter_column('company_profiles', 'company_registered_date',
        existing_type=sa.Date(),
        type_=sa.VARCHAR(),
        existing_nullable=True
    )