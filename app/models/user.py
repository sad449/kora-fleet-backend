# The users table. every person in the system is a user, whether or not they log in.
# personal details live here; driver-specific data lives in drivers with a link back.


from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id:Optional[int] =Field(default=None,primary_key=True)
        # personal-info

    first_name :str =Field(nullable=False)    
    last_name :str =Field(nullable=False)
    email: Optional[str]=Field(default=None,unique=True)
    phone:Optional[str]=None
    # login (optional — a driver who never logs in has these empty)

    password_hash: Optional[str]=None
    # access level (FK to roles.id, always set)

    role_id: int=Field(foreign_key='roles.id',nullable=False)

    is_active:bool=Field(default=True,nullable=False)
    # audit columns — same shape on every operational table

    created_at:datetime=Field(default_factory=datetime.utcnow,nullable=False)

    created_by:Optional[int]=Field(default=None,foreign_key='users.id')
    updated_at:Optional[datetime]=None
    updated_by:Optional[int]=Field(default=None,foreign_key='users.id')
    deleted_at:Optional[datetime]=None
    deleted_by:Optional[int]=Field(default=None,foreign_key='users.id')

        