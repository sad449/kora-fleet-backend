from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_roles():
    return {"items": []}

@router.get("/{role_id}")
def get_role(role_id: int):
    return {"id": role_id, "name": "role"}
