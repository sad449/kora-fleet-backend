from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class CompanyType(str, Enum):
    solo = "solo"
    company = "company"


class CompanyProfile(SQLModel, table=True):
    __tablename__ = "company_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, nullable=False)

    company_name: Optional[str] = None
    company_type: CompanyType = Field(default=CompanyType.solo, nullable=False)
    company_registered_date: Optional[date] = None
    rdb_certificate: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = None
    is_deleted: bool = Field(default=False, nullable=False)
    deleted_at: Optional[datetime] = None