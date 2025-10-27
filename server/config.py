from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET: str
    ALGORITHM: str
    MONGO_URL: str
    DB_NAME: str
    class Config:
        env_file = "server/.env"


settings = Settings()