from sqlmodel import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import login


def login_controller(request: LoginRequest, session: Session) -> TokenResponse:
    result = login(
        email=request.email,
        password=request.password,
        session=session
    )
    return TokenResponse(**result)