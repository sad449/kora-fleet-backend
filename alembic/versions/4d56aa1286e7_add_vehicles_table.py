"""add vehicles table

Revision ID: 4d56aa1286e7
Revises: 4572e340ddc7
Create Date: 2026-08-31 12:16:29.362421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel




                                        
revision: str = '4d56aa1286e7'
down_revision: Union[str, None] = '4572e340ddc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
                                                                 
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plate_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('make', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('model', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('mileage', sa.Integer(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('available', 'in_use', 'maintenance', 'inactive', name='vehiclestatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('plate_number')
    )
                                  


def downgrade() -> None:
                                                                 
    op.drop_table('vehicles')
                                  
