from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.user import User
from app.models.company_profile import CompanyProfile
from app.core.security import verify_password, create_access_token, hash_password
from datetime import datetime


def login(email: str, password: str, session: Session) -> dict:
    user = session.exec(select(User).where(User.email == email)).first()

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

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )

    token = create_access_token(user_id=user.id, role_id=user.role_id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "full_name": f"{user.first_name or ''} {user.last_name or ''}".strip() or user.email,
        "role_id": user.role_id,
        "must_change_password": user.must_change_password,
        "profile_completed": user.profile_completed,
        "account_type": user.account_type.value,
    }


def change_password(user: User, old_password: str, new_password: str, session: Session) -> dict:
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    user.password_hash = hash_password(new_password)
    user.must_change_password = False
    session.add(user)
    session.commit()

    return {"message": "Password changed successfully"}


def save_personal_details(user: User, data: dict, session: Session) -> dict:
    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")
    user.phone = data.get("phone") or None
    user.national_id_number = data.get("national_id_number") or None
    user.address = data.get("address") or None
    user.updated_at = datetime.utcnow()

    if user.account_type.value == "individual":
        user.profile_completed = True

    session.add(user)
    session.commit()

    return {
        "message": "Personal details saved",
        "profile_completed": user.profile_completed,
        "account_type": user.account_type.value,
    }


def save_company_profile(user: User, data: dict, session: Session) -> dict:
    existing = session.exec(
        select(CompanyProfile).where(CompanyProfile.user_id == user.id)
    ).first()

    if existing:
        existing.company_name = data.get("company_name") or None
        existing.company_registered_date = data.get("company_registered_date") or None
        existing.rdb_certificate = data.get("rdb_certificate") or None
        existing.status = data.get("status") or "limited_company"
        existing.address = data.get("address") or None
        existing.phone = data.get("phone") or None
        existing.updated_at = datetime.utcnow()
        session.add(existing)
    else:
        profile = CompanyProfile(
            user_id=user.id,
            company_name=data.get("company_name") or None,
            company_registered_date=data.get("company_registered_date") or None,
            rdb_certificate=data.get("rdb_certificate") or None,
            status=data.get("status") or "limited_company",
            address=data.get("address") or None,
            phone=data.get("phone") or None,
        )
        session.add(profile)

    user.profile_completed = True
    user.updated_at = datetime.utcnow()
    session.add(user)
    session.commit()

    return {"message": "Company profile saved"}