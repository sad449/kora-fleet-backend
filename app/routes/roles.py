from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.role import Role
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/")
def list_roles(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return session.exec(select(Role)).all()