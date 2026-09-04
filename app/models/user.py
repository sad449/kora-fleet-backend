


from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id:Optional[int] =Field(default=None,primary_key=True)

    first_name :str =Field(nullable=False)    
    last_name :str =Field(nullable=False)
    email: Optional[str]=Field(default=None,unique=True)
    phone:Optional[str]=None

    password_hash: Optional[str]=None

    role_id: int=Field(foreign_key='roles.id',nullable=False)

    is_active:bool=Field(default=True,nullable=False)

    created_at:datetime=Field(default_factory=datetime.utcnow,nullable=False)

    created_by:Optional[int]=Field(default=None,foreign_key='users.id')
    updated_at:Optional[datetime]=None
    updated_by:Optional[int]=Field(default=None,foreign_key='users.id')
    deleted_at:Optional[datetime]=None
    deleted_by:Optional[int]=Field(default=None,foreign_key='users.id')

        