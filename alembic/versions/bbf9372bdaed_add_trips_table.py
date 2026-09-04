"""add trips table

Revision ID: bbf9372bdaed
Revises: e1dd69074a91
Create Date: 2026-08-31 12:21:48.173362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel




                                        
revision: str = 'bbf9372bdaed'
down_revision: Union[str, None] = 'e1dd69074a91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
                                                                 
    op.create_table('trips',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=False),
    sa.Column('origin', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('destination', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('trip_date', sa.Date(), nullable=False),
    sa.Column('status', sa.Enum('planned', 'assigned', 'in_progress', 'completed', 'cancelled', name='tripstatus'), nullable=False),
    sa.Column('est_distance', sa.Numeric(precision=8, scale=2), nullable=True),
    sa.Column('actual_distance', sa.Numeric(precision=8, scale=2), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['deleted_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['drivers.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
                                  


def downgrade() -> None:
                                                                 
    op.drop_table('trips')
                                  
