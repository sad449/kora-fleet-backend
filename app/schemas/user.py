from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.user import AccountType


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    password: str
    role_id: int
    date_of_birth: Optional[date] = None
    national_id_number: Optional[str] = None
    address: Optional[str] = None
    account_type: AccountType = AccountType.individual
    company_name: Optional[str] = None
    position: Optional[str] = None
    certificate_url: Optional[str] = None


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
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