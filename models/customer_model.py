"""
Esse módulo lida com as models, especificando o que cada model precisa e utiliza.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator
import ulid


class Customer(BaseModel):
    """
    Representa um cliente com informações como nome, email e status.
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
    Representa a atualização parcial de um cliente. Pelo menos um campo deve ser fornecido.
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
        Valida que pelo menos um campo, além do 'id', seja fornecido para atualização.

        Args:
            values (dict): Dicionário com os valores do modelo.

        Raises:
            ValueError: Se nenhum campo além do 'id' for fornecido.

        Returns:
            dict: Os valores validados.
        """
        # Verificando se algum campo além do 'id' foi fornecido
        required_keys = [
            key for key, value in values.items() if key != "id" and value is not None
        ]
        print(required_keys)

        if not required_keys:
            raise ValueError("At least one field other than 'id' must be provided.")

        return values
