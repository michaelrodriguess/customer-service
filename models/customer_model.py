from pydantic import BaseModel, EmailStr, Field, root_validator
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
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.now)

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        required_keys = [
            key for key, value in values.items() if key != "id" and value is not None
        ]

        if not required_keys:
            raise ValueError("At least one field other than 'id' must be provided.")

        return values
