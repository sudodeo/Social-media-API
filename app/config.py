from pydantic import BaseSettings


class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_host: str
    database_name: str
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    class Config:
         env_file = ".env"

settings = Settings()
