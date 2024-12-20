# settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str = (
        "db"  # O host do banco de dados (por exemplo, "db" para o container Docker)
    )
    DATABASE_PORT: str = "5432"  # A porta padrão do PostgreSQL
    DATABASE_NAME: str = "mydb"  # O nome do banco de dados
    DATABASE_USER: str = "postgres"  # Nome do usuário do PostgreSQL
    DATABASE_PASSWORD: str = "password"  # Senha do usuário

    @property
    def DATABASE_URL(self) -> str:
        """Cria a URL de conexão com o banco de dados."""
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


settings = Settings()
