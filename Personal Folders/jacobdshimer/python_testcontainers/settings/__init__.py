from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_host: str
    pg_port: str
    pg_username: str
    pg_password: str
    pg_database: str
