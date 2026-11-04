from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int
    PG_KEY: str
    JWT_ACCESS: str
    JWT_REFRESH: str
    PY_ENV: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()