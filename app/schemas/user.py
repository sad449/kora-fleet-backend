from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.user import AccountType


class UserCreate(BaseModel):
    email: str
    password: str
    role_id: int


class UserOut(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role_id: int
    is_active: bool
    date_of_birth: Optional[date] = None
    national_id_number: Optional[str] = None
    address: Optional[str] = None
    account_type: AccountType
    company_name: Optional[str] = None
    position: Optional[str] = None
    certificate_url: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[int] = None
    date_of_birth: Optional[date] = None
    national_id_number: Optional[str] = None
    address: Optional[str] = None
    account_type: Optional[AccountType] = None
    company_name: Optional[str] = None
    position: Optional[str] = None
    certificate_url: Optional[str] = None