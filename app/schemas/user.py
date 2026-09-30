from pydantic import BaseModel
from typing import Optional


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
    national_id_number: Optional[str] = None
    address: Optional[str] = None
    role_id: int
    is_active: bool
    profile_completed: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    national_id_number: Optional[str] = None
    address: Optional[str] = None
    role_id: Optional[int] = None