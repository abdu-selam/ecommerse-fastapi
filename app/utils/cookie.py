from fastapi import Response
from app.utils.env import settings

def send_cookie(response: Response, key: str, value: str, type="access"): 
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=settings.PY_ENV == "production",
        samesite="none" if settings.PY_ENV == "production" else "lax",
        max_age= 900 if type == "access" else 15 * 24 * 3600,
        path="/" if type == "access" else "/api/auth/refresh"
    )
    