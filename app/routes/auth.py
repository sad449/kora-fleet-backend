# auth routes: login and get current user
# /api/auth/login , public, no token needed
# /api/auth/me   ,protected, token required

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from app.database import get_session
from app.schemas.auth import LoginRequest, TokenResponse
from app.controllers.auth_controller import login_controller
from app.core.security import decode_access_token
from app.models.user import User

router = APIRouter()
bearer = HTTPBearer()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    return login_controller(request, session)


@router.get("/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    session: Session = Depends(get_session)
):
    # this decodes the token from the authorization header
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # this loads the user from the database
    user = session.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role_id": user.role_id,
    }