from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class AccountType(str, Enum):
    individual = "individual"
    company = "company"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = Field(default=None, unique=True)
    phone: Optional[str] = None

    date_of_birth: Optional[date] = None
    national_id_number: Optional[str] = None
    address: Optional[str] = None

    account_type: AccountType = Field(default=AccountType.individual, nullable=False)
    company_name: Optional[str] = None
    position: Optional[str] = None
    certificate_url: Optional[str] = None

    password_hash: Optional[str] = None

    role_id: int = Field(foreign_key="roles.id", nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    must_change_password: bool = Field(default=True, nullable=False)
    profile_completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = Field(default=None, foreign_key="users.id")
    is_deleted: bool = Field(default=False, nullable=False)
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="users.id")