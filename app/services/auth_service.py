# the business logic for authentication
# the controller calls this ,it never touches HTTP directly

from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import verify_password, create_access_token


def login(email: str, password: str, session: Session) -> dict:
    # 1. find the user by email
    user = session.exec(select(User).where(User.email == email)).first()

    # 2. If no user found, or password wrong, return the same error
    #  never reveal which one failed ,that can lead to informationleaks 
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 3. if account is deactivated, block login
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )

    # 4. all checks passed ,create and return a token
    token = create_access_token(user_id=user.id, role_id=user.role_id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "full_name": f"{user.first_name} {user.last_name}",
        "role_id": user.role_id,
    }