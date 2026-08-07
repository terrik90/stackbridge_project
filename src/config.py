from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_debug: bool = True
    app_name: str = "stackbridge"
    host_app: str = "127.0.0.1"
    port_app: int = 8000
    prefix: str = "/api"

    username_db: str = "postgres"
    password_db: str = "fvbl2006"
    name_db: str = "stackbridge"
    host_db: str = "localhost"
    port_db: int = 5432

    jwt_key: str = "iqOvIiyPm3wDcaIVC61olu8P+CL17KvLofEHU/AAXHw="
    algoritm: str = "HS256"

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.username_db}:{self.password_db}@{self.host_db}:{self.port_db}/{self.name_db}"


settings = Settings()
