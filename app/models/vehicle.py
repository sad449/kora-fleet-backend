# the vehicles table. a vehicle has no direct driver reference —
# that lives in vehicle_assignments so we can keep history.

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class VehicleStatus(str, Enum):
    available = "available"
    in_use = "in_use"
    maintenance = "maintenance"
    inactive = "inactive"


class Vehicle(SQLModel, table=True):
    __tablename__ = "vehicles"

    id: Optional[int] = Field(default=None, primary_key=True)
#vehicle --info
    plate_number: str = Field(unique=True, nullable=False)
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    mileage: int = Field(default=0, nullable=False)
    capacity: Optional[int] = None
    status: VehicleStatus = Field(default=VehicleStatus.available, nullable=False)
#audit
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = Field(default=None, foreign_key="users.id")
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="users.id")