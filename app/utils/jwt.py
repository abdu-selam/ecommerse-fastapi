import jwt
from datetime import datetime, timezone, timedelta
from app.utils.env import settings

ALGORITHM = "HS256"

def sign_access(user_id: str):
    payload = {
        "sub": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }

    token = jwt.encode(
        payload,
        settings.JWT_ACCESS,
        algorithm=ALGORITHM
    )

    return token

def verify_access(token: str):
    try:
        payload = jwt.decode(
                token,
                settings.JWT_ACCESS,
                algorithms=[ALGORITHM]
            )
        
        return payload
    except:
        return None

def sign_refresh(user_id: str, refresh_id: str):
    payload = {
        "id": refresh_id,
        "sub": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=15)
    }

    token = jwt.encode(
        payload,
        settings.JWT_REFRESH,
        algorithm=ALGORITHM
    )

    return token

def verify_refresh(token: str):
    try:
        payload = jwt.decode(
                token,
                settings.JWT_REFRESH,
                algorithms=[ALGORITHM]
            )
        
        return payload
    except:
        return None