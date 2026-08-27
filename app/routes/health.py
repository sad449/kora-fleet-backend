# this file is about 'the /api/health endpoint.it confirms the API is up and the database responds'.

from fastapi import APIRouter, Depends
from sqlmodel import Session, text
from app.database import get_session

router = APIRouter()

@router.get("/health")
def health(session: Session = Depends(get_session)):
    try:
        session.exec(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {"status": "ok", "database": db_status}