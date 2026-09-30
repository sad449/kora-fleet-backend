"""remove updated_by, remove trip distances, add permissions tables

Revision ID: 882015bcbe20
Revises: 33ab7c4ca920
Create Date: 2026-09-28 15:39:22.550839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = '882015bcbe20'
down_revision: Union[str, None] = '33ab7c4ca920'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.Column('granted_by', sa.Integer(), nullable=False),
    sa.Column('granted_at', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
    sa.ForeignKeyConstraint(['granted_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('drivers_updated_by_fkey', 'drivers', type_='foreignkey')
    op.drop_column('drivers', 'updated_by')
    op.drop_constraint('trips_updated_by_fkey', 'trips', type_='foreignkey')
    op.drop_column('trips', 'updated_by')
    op.drop_column('trips', 'est_distance')
    op.drop_column('trips', 'actual_distance')
    op.drop_constraint('users_updated_by_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'updated_by')
    op.drop_constraint('vehicle_assignments_updated_by_fkey', 'vehicle_assignments', type_='foreignkey')
    op.drop_column('vehicle_assignments', 'updated_by')
    op.add_column('vehicles', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'))
    op.drop_constraint('vehicles_updated_by_fkey', 'vehicles', type_='foreignkey')
    op.drop_column('vehicles', 'updated_by')


def downgrade() -> None:
    op.add_column('vehicles', sa.Column('updated_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('vehicles_updated_by_fkey', 'vehicles', 'users', ['updated_by'], ['id'])
    op.drop_column('vehicles', 'is_deleted')
    op.add_column('vehicle_assignments', sa.Column('updated_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('vehicle_assignments_updated_by_fkey', 'vehicle_assignments', 'users', ['updated_by'], ['id'])
    op.add_column('users', sa.Column('updated_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_updated_by_fkey', 'users', 'users', ['updated_by'], ['id'])
    op.add_column('trips', sa.Column('actual_distance', sa.NUMERIC(precision=8, scale=2), autoincrement=False, nullable=True))
    op.add_column('trips', sa.Column('est_distance', sa.NUMERIC(precision=8, scale=2), autoincrement=False, nullable=True))
    op.add_column('trips', sa.Column('updated_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('trips_updated_by_fkey', 'trips', 'users', ['updated_by'], ['id'])
    op.add_column('drivers', sa.Column('updated_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('drivers_updated_by_fkey', 'drivers', 'users', ['updated_by'], ['id'])
    op.drop_table('user_permissions')
    op.drop_table('permissions')