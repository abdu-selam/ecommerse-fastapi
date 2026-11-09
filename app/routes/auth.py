from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.admin import AdminLogin, AdminLoginResponse
from app.utils import password, jwt, cookie
from app.configs.db import get_db
from app.models.admin import Admin
from app.models.refresh_token import RefreshToken
from app.dependencies.auth import protected_route

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
    refresh_id = str(uuid4())
    access_token = jwt.sign_access(admin.id)
    refresh_token = jwt.sign_refresh(admin.id, refresh_id)

    refresh = RefreshToken(
        id=refresh_id,
        token=refresh_token,
        admin_id=admin.id
    )
    
    # save user
    db.add(refresh)
    await db.commit()

    # send cookie
    cookie.send_cookie(response, "access", access_token)
    cookie.send_cookie(response, "refresh", refresh_token)

    # send response
    admin_response = AdminLoginResponse.model_validate(admin)
    return admin_response


@router.delete("/logout")
async def logout(request: Request, response: Response,db: DBSession, protect = Depends(protected_route)):
    await db.delete(protect.get("refresh"))

    response.delete_cookie("access", path="/")
    response.delete_cookie("refresh", path="/api/auth/refresh")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
