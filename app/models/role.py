#the roles table.one row per access level
#valuses:admin,manager,managment,driver(seeded on first run)

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = None
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = None