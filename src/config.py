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

    def DATABASE_URL_psycopg2(self) -> str:
        return f"postgresql+psycopg2://{self.username_db}:{self.password_db}@{self.host_db}:{self.port_db}/{self.name_db}"


settings = Settings()
