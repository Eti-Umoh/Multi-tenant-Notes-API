from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET: str
    ALGORITHM: str

    class Config:
        env_file = "server/.env"


settings = Settings()