from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class UserPermission(SQLModel, table=True):
    __tablename__ = "user_permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    permission_id: int = Field(foreign_key="permissions.id", nullable=False)
    granted_by: int = Field(foreign_key="users.id", nullable=False)
    granted_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(default=True, nullable=False)