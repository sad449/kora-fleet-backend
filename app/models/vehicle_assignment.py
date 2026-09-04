
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
class VehicleAssignment(SQLModel, table=True):
    __tablename__ = "vehicle_assignments"

    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_id: int = Field(foreign_key="vehicles.id", nullable=False)
    driver_id: int = Field(foreign_key="drivers.id", nullable=False)

    assigned_from: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    assigned_to: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = Field(default=None, foreign_key="users.id")