# settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str = (
        "db"
    )
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "mydb"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"

    @property
    def DATABASE_URL(self) -> str:
        """Cria a URL de conexão com o banco de dados."""
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


settings = Settings()
