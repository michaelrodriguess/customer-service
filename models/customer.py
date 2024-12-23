from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import ulid


class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()))
    name: str
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default=None)


class Customer_update(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.now)
