from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_users():
    return {"items": []}

@router.get("/me")
def get_current_user():
    return {"id": None, "email": None, "name": None}
