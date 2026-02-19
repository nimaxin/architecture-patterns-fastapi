from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_driver: str
    db_name: str
    db_host: str | None = None
    db_port: int | None = None
    db_user: str | None = None
    db_pass: str | None = None

    db_pool_size: int = 10
    db_max_overflow: int = 15
    db_pool_recycle: int = 1800
    db_pool_timeout: int = 0


settings = Settings()  # type: ignore
