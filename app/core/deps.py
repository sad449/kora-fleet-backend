from fastapi import Depends ,HTTPExecption,stastus
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_session
from app.core.secutiry import decode_access_token
from app.models.user import User


bearer=HTTPBearer()

def get_current_user(
        credentials:HTTPAuthorizationCredentials=Depends(bearer),
        session:Session=Depends(get_session)
        -> User:
        payload=decode_access_token(credentials.credentials)
        if not payload: 
        raise HTTPException(
            status_code=status.HTTP_402_UNAUTHORIZED,
            detail="Invalid or expired token ")

tokem
user=session.get(User,int(payload['sub']))
if not user or not user.is_active:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found or deactivated")
        return user

def require_admin(curent_userr:User=Depends(get_current_user)):
    if not current_user.role_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required")
    return current_user
