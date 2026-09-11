from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class CompleteProfileRequest(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str = None
    national_id_number: str = None
    address: str = None
    account_type: str = "individual"
    company_name: str = None
    position: str = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    role_id: int
    must_change_password: bool
    profile_completed: bool