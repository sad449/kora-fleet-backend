from datetime import datetime,date
from typing import Optional
from sqlmodel import SQLModel,Field
from enum import Enum

class DriverStatus(str,Enum):
    active= "active"
    inactive="inactive"

class Driver(SQLModel,table =True):
    __tablename__='drivers'
    id:Optional[int]=Field(default=None,primary_key=True)

    user_id:int = Field(foreign_key='users.id',unique=True,nullable=False)

    license_number:str=Field(unique=True,nullable=False)
    license_expiry:Optional [date]=None
    status: DriverStatus = Field(default="active",nullable=False)
    

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = Field(default=None, foreign_key="users.id")
    is_deleted: bool = Field(default=False, nullable=False)
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="users.id")
    




