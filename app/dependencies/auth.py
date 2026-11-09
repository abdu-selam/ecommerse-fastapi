from fastapi import Request, Response, HTTPException, status, Depends
from app.utils.jwt import verify_access, verify_refresh
from app.configs.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from app.models.admin import Admin
from app.models.refresh_token import RefreshToken

DBSession = Annotated[AsyncSession, Depends(get_db)]

async def protected_route(request: Request, db: DBSession):
    access_token = request.cookies.get("access")
    refresh_token = request.cookies.get("refresh")

    print(access_token)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Missed")

    payload = verify_access(access_token)
    print(payload)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    payloadRefresh = verify_refresh(refresh_token)
    user = await db.execute(
        select(Admin).where(Admin.id == payload.get("sub"))
    )

    refresh = await db.execute(
        select(RefreshToken).where(RefreshToken.id == payloadRefresh.get("id"))
    )

    return {
        "user": user.scalar_one_or_none(),
        "refresh": refresh.scalar_one_or_none()
    }