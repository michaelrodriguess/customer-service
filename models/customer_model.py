from pydantic import BaseModel, EmailStr, Field, root_validator
from datetime import datetime
from typing import Optional
import ulid


class Customer(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ulid.new()),
        description="Identificador único do cliente no formato ULID.",
    )
    name: str = Field(..., description="Nome do cliente.")
    email: EmailStr = Field(..., description="Endereço de email válido do cliente.")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Data de criação do cliente."
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Data de atualização do cliente."
    )
    active: bool = Field(
        default=True, description="Status do cliente (ativo ou inativo)."
    )


from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class Customer_update(BaseModel):
    id: str = Field(..., description="Identificador único do cliente no formato ULID.")
    name: Optional[str] = Field(None, description="Nome do cliente (opcional).")
    email: Optional[EmailStr] = Field(
        None, description="Endereço de email válido do cliente (opcional)."
    )
    active: Optional[bool] = Field(None, description="Status do cliente (opcional).")
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Data de atualização do cliente."
    )

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        required_keys = [
            key for key, value in values.items() if key != "id" and value is not None
        ]

        if not required_keys:
            raise ValueError("At least one field other than 'id' must be provided.")

        return values
