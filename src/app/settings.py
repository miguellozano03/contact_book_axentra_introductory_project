from pathlib import Path
from typing import ClassVar
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent

class CommonSettings(BaseSettings):
    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"

class AppSettings(CommonSettings):
    api_version: str = "1.0.0"
    project_name: str = "Contact Book Demo"
    project_domain: str = "AxentraOs Induction"

class CORSSettings(CommonSettings):
    allowed_origins: list[str] = ["*"]
    allowed_methods: list[str] = ["*"]
    allowed_headers: list[str] = ["*"]

class DatabaseSettings(CommonSettings):
    db_user: str = ""
    db_password: str = ""
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = ""
    SQLITE_FILE: ClassVar[Path] = BASE_DIR.parent / "db.sqlite3"
    sqlite_path: str = f"sqlite+aiosqlite:///{SQLITE_FILE}"

    @property
    def db_url(self) -> str:
        if self.db_user and self.db_name:
            return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return self.sqlite_path

    @property
    def db_url_sync(self) -> str:
        if self.db_user and self.db_name:
            return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return self.sqlite_path.replace("aiosqlite", "sqlite")

class Settings(CommonSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)

@lru_cache
def get_settings() -> Settings:
    return Settings()