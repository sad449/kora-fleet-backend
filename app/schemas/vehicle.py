from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class VehicleBase(BaseModel):
    """Base schema for Vehicle"""
    registration_number: str = Field(..., description="Vehicle registration number")
    make: str = Field(..., description="Vehicle make/brand")
    model: str = Field(..., description="Vehicle model")
    year: int = Field(..., description="Manufacturing year", ge=1900, le=datetime.now().year + 1)
    color: Optional[str] = None
    capacity: Optional[int] = Field(None, description="Passenger or load capacity")
    license_plate: str = Field(..., description="License plate number")
    insurance_number: Optional[str] = None
    insurance_expiry: Optional[datetime] = None
    inspection_due_date: Optional[datetime] = None
    status: Optional[str] = Field("available", description="Status: available, assigned, maintenance, retired")
    notes: Optional[str] = None


class VehicleCreate(VehicleBase):
    """Schema for creating a new vehicle"""
    pass


class VehicleUpdate(BaseModel):
    """Schema for updating a vehicle"""
    registration_number: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=datetime.now().year + 1)
    color: Optional[str] = None
    capacity: Optional[int] = None
    license_plate: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_expiry: Optional[datetime] = None
    inspection_due_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class VehicleResponse(VehicleBase):
    """Schema for vehicle response"""
    id: int
    is_active: bool
    created_at: datetime
    created_by: Optional[int]
    updated_at: Optional[datetime]
    updated_by: Optional[int]
    deleted_at: Optional[datetime]
    deleted_by: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class VehicleListResponse(BaseModel):
    """Schema for paginated vehicle list response"""
    items: list[VehicleResponse]
    total: int
    page: int
    size: int
    pages: int


class VehicleStatusUpdate(BaseModel):
    """Schema for updating vehicle status only"""
    status: str = Field(..., description="Status: available, assigned, maintenance, retired")
    notes: Optional[str] = None