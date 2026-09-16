from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class CompanyStatus(str, Enum):
    sole_proprietorship = "sole_proprietorship"
    limited_company = "limited_company"
    partnership = "partnership"


class CompanyProfile(SQLModel, table=True):
    __tablename__ = "company_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, nullable=False)

    company_name: Optional[str] = None
    company_registered_date: Optional[str] = None
    rdb_certificate: Optional[str] = None
    status: CompanyStatus = Field(default=CompanyStatus.limited_company, nullable=False)
    address: Optional[str] = None
    phone: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = None
    is_deleted: bool = Field(default=False, nullable=False)
    deleted_at: Optional[datetime] = None