from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class PersonalDetailsRequest(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    national_id_number: Optional[str] = None
    address: Optional[str] = None


class CompanyProfileRequest(BaseModel):
    company_name: str
    company_registered_date: Optional[str] = None
    rdb_certificate: Optional[str] = None
    status: str = "limited_company"
    address: Optional[str] = None
    phone: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    role_id: int
    must_change_password: bool
    profile_completed: bool
    account_type: str