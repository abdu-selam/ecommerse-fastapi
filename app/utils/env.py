from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int
    PY_ENV: str

    PG_KEY: str
    CLIENT_URL: str

    JWT_ACCESS: str
    JWT_REFRESH: str

    ADMIN_EMAIL: str
    ADMIN_PASS: str
    ADMIN_NAME: str

    BREVO_EMAIL: str
    BREVO_NAME: str
    BREVO_KEY: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()