from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import verify_password, create_access_token, hash_password


def login(email: str, password: str, session: Session) -> dict:
    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not user.password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account is deactivated")

    token = create_access_token(user_id=user.id, role_id=user.role_id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "full_name": f"{user.first_name} {user.last_name}",
        "role_id": user.role_id,
        "must_change_password": user.must_change_password,
        "profile_completed": user.profile_completed,
    }


def change_password(user: User, old_password: str, new_password: str, session: Session) -> dict:
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    user.password_hash = hash_password(new_password)
    user.must_change_password = False

    session.add(user)
    session.commit()

    return {"message": "Password changed successfully"}


def complete_profile(user: User, data: dict, session: Session) -> dict:
    user.first_name = data.get("first_name") or None
    user.last_name = data.get("last_name") or None
    user.date_of_birth = data.get("date_of_birth") or None
    user.national_id_number = data.get("national_id_number") or None
    user.address = data.get("address") or None
    user.account_type = data.get("account_type") or "individual"
    user.company_name = data.get("company_name") or None
    user.position = data.get("position") or None
    user.profile_completed = True

    session.add(user)
    session.commit()

    return {"message": "Profile completed"}