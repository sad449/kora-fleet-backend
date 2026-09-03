# this defines what the login request looks like, and what the response returns
# pydantic validates these automatically — bad input is rejected before the controller runs

from pydantic import BaseModel

class LoginRequest(BaseModel):
    # what the frontend sends
    email: str
    password: str


class TokenResponse(BaseModel):
    # what we send back on a successful login
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    role_id: int