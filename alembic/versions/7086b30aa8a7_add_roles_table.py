"""add roles table

Revision ID: 7086b30aa8a7
Revises: 
Create Date: 2026-08-31 10:05:58.243553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

                                        
revision: str = '7086b30aa8a7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
                                                                 
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
                                  


def downgrade() -> None:
                                                                 
    op.drop_table('roles')
                                  
