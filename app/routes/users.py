from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.controllers.user_controller import (
    create_user_controller, list_users_controller,
    get_user_controller, update_user_controller,
    delete_user_controller
)
from app.core.deps import get_current_user, require_admin
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=list[UserOut])
def list_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return list_users_controller(session)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return get_user_controller(user_id, session)


@router.post("/", response_model=UserOut, status_code=201)
def create_user(
    data: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    return create_user_controller(data, current_user, session)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    return update_user_controller(user_id, data, current_user, session)


@router.delete("/{user_id}", response_model=UserOut)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    return delete_user_controller(user_id, current_user, session)