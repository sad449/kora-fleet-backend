

from datetime import datetime
from typing import Optional, Any
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum


class AuditAction(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    action: AuditAction = Field(nullable=False)
    entity_type: str = Field(nullable=False)   
    entity_id: int = Field(nullable=False)     

    changes: Optional[Any] = Field(default=None, sa_column=Column(JSONB))

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)