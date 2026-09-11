from sqlmodel import Session, select
from fastapi import HTTPException, status
from datetime import datetime
from app.models.user import User, AccountType
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


def create_user(data: UserCreate, created_by_id: int, session: Session) -> User:
    existing = session.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role_id=data.role_id,
        is_active=True,
        is_deleted=False,
        must_change_password=True,
        profile_completed=False,
        created_by=created_by_id,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def list_users(session: Session) -> list[User]:
    return session.exec(
        select(User).where(User.is_deleted == False)
    ).all()


def get_user(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(user_id: int, data: UserUpdate, updated_by_id: int, session: Session) -> User:
    user = get_user(user_id, session)

    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.phone is not None:
        user.phone = data.phone
    if data.role_id is not None:
        user.role_id = data.role_id
    if data.date_of_birth is not None:
        user.date_of_birth = data.date_of_birth
    if data.national_id_number is not None:
        user.national_id_number = data.national_id_number
    if data.address is not None:
        user.address = data.address
    if data.account_type is not None:
        user.account_type = data.account_type
    if data.company_name is not None:
        user.company_name = data.company_name
    if data.position is not None:
        user.position = data.position
    if data.certificate_url is not None:
        user.certificate_url = data.certificate_url

    user.updated_at = datetime.utcnow()
    user.updated_by = updated_by_id

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(user_id: int, deleted_by_id: int, session: Session) -> User:
    user = get_user(user_id, session)
    user.is_deleted = True
    user.is_active = False
    user.deleted_at = datetime.utcnow()
    user.deleted_by = deleted_by_id

    session.add(user)
    session.commit()
    session.refresh(user)
    return user