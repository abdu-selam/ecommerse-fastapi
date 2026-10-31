from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int
    PG_KEY: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()