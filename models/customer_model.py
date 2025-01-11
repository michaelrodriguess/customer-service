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
        description="Identificador único do cliente no formato ULID.",
    )
    name: str = Field(..., description="Nome do cliente.")
    email: EmailStr = Field(..., description="Endereço de email válido do cliente.")
    active: bool = Field(
        default=True, description="Status do cliente (ativo ou inativo)."
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Data de criação do cliente."
    )
    updated_at: datetime | None = Field(
        default=None, description="Data de atualização do cliente."
    )


class CustomerUpdate(BaseModel):
    """
    Represents the partial update of a customer. At least one field must be provided.
    """
    id: str = Field(..., description="Identificador único do cliente no formato ULID.")
    name: Optional[str] = Field(None, description="Nome do cliente (opcional).")
    email: Optional[EmailStr] = Field(
        None, description="Endereço de email válido do cliente (opcional)."
    )
    active: Optional[bool] = Field(None, description="Status do cliente (opcional).")
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Data de atualização do cliente (opcional).",
    )

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        """
        Validates that at least one field, in addition to ‘id’, is provided for updating.

        Args:
            values (dict): Dictionary with the model's values.

        Raises:
            ValueError: If no field other than ‘id’ is supplied.
            
        Returns:
            dict: The validated values.
        """
        required_keys = [
            key for key, value in values.items() if key != "id" and value is not None
        ]

        if not required_keys:
            raise ValueError("At least one field other than 'id' must be provided.")

        return values
