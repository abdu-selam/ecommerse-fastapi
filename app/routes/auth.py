from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from datetime import datetime, UTC

from app.schemas.admin import AdminLogin, AdminLoginResponse
from app.utils import password, jwt, cookie
from app.configs.db import get_db
from app.models.admin import Admin

router = APIRouter()

DBSession = Annotated[AsyncSession, Depends(get_db)]

@router.post("/login", response_model=AdminLoginResponse)
async def login(user: AdminLogin, db: DBSession, response: Response):
    # seach for email 
    result = await db.execute(
        select(Admin).where(Admin.email == user.email)
    )
    admin = result.scalar_one_or_none()
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # check for password
    if not password.verify(user.password, admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # gen for jwt
    access_token = jwt.sign_access(admin.id)
    refresh_token = jwt.sign_refresh(admin.id)

    admin.refresh_token = refresh_token
    admin.refresh_created_at = datetime(UTC)
    # save user
    db.add(admin)
    await db.commit()
    await db.refresh(admin)

    # send cookie
    cookie.send_cookie(response, "access", access_token)
    cookie.send_cookie(response, "refresh", refresh_token)

    # send response
    admin_response = AdminLoginResponse.model_validate(admin)
    return admin_response
