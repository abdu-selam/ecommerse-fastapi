from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: str
    PG_KEY: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()