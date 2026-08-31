# trips — one journey by a vehicle and a driver
# separate from assignments: a trip is temporary; an assignment is standing

from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from sqlmodel import SQLModel, Field
from enum import Enum


class TripStatus(str, Enum):
    planned = "planned"
    assigned = "assigned"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Trip(SQLModel, table=True):
    __tablename__ = "trips"

    id: Optional[int] = Field(default=None, primary_key=True)

    vehicle_id: int = Field(foreign_key="vehicles.id", nullable=False)
    driver_id: int = Field(foreign_key="drivers.id", nullable=False)

    origin: str = Field(nullable=False)
    destination: str = Field(nullable=False)
    trip_date: date = Field(nullable=False)
    status: TripStatus = Field(default=TripStatus.planned, nullable=False)

    est_distance: Optional[Decimal] = Field(default=None, max_digits=8, decimal_places=2)
    actual_distance: Optional[Decimal] = Field(default=None, max_digits=8, decimal_places=2)
#audit
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = Field(default=None, foreign_key="users.id")
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="users.id")