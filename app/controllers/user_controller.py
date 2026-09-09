from sqlmodel import Session
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import (
    create_user, list_users, get_user, update_user, delete_user
)
from app.models.user import User


def create_user_controller(data: UserCreate, current_user: User, session: Session) -> UserOut:
    user = create_user(data, current_user.id, session)
    return UserOut.model_validate(user)

def list_users_controller(session: Session) -> list[UserOut]:
    users = list_users(session)
    return [UserOut.model_validate(u) for u in users]

def get_user_controller(user_id: int, session: Session) -> UserOut:
    user = get_user(user_id, session)
    return UserOut.model_validate(user)

def update_user_controller(user_id: int, data: UserUpdate, current_user: User, session: Session) -> UserOut:
    user = update_user(user_id, data, current_user.id, session)
    return UserOut.model_validate(user)

def delete_user_controller(user_id: int, current_user: User, session: Session) -> UserOut:
    user = delete_user(user_id, current_user.id, session)
    return UserOut.model_validate(user)