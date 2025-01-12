"""
This module deals with models, specifying what each model needs and uses.
"""
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime
from typing import Optional
import ulid


class Customer(BaseModel):
    """
    Represents a customer with information such as name, email and status.
    """
    id: str = Field(
        default_factory=lambda: str(ulid.new()),
        description="Unique customer identifier in ULID format.",
    )
    name: str = Field(..., description="Customer name")
    email: EmailStr = Field(..., description="Valid customer email adress")
    active: bool = Field(
        default=True, description="Customer status (active or inactive)."
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Customer creation date."
    )
    updated_at: datetime | None = Field(
        default=None, description="Customer update date."
    )


class CustomerUpdate(BaseModel):
    """
    Represents the partial update of a customer. At least one field must be provided.
    """
    id: str = Field(..., description="Unique customer identifier in ULID format.")
    name: Optional[str] = Field(None, description="Customer name (optional).")
    email: Optional[EmailStr] = Field(
        None, description="Valid customer email address (optional)."
    )
    active: Optional[bool] = Field(None, description="Customer status (optional).")
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Customer update date (optional).",
    )

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        """
        Validates that at least one field, in addition to ‘id’, is provided for updating.
        """
        required_keys = [
            key for key, value in values.items() if key != "id" and value is not None
        ]

        if not required_keys:
            raise ValueError("At least one field other than 'id' must be provided.")

        return values
