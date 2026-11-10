from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from uuid import uuid4
from datetime import datetime, timezone

from app.schemas.admin import (
    AdminLogin, 
    AdminLoginResponse, 
    AdminChangePassword, 
    AdminForgotPassword
)
from app.utils import password, jwt, cookie
from app.configs.db import get_db
from app.models.admin import Admin
from app.models.refresh_token import RefreshToken
from app.dependencies.auth import protected_route, ProtectedReturn
from app.utils import password
from app.utils.jinja_email import forgot_password_html
from app.configs.email import send_email

router = APIRouter()

DBSession = Annotated[AsyncSession, Depends(get_db)]
ProtectedRoute =  Annotated[ProtectedReturn, Depends(protected_route)]

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
async def logout(request: Request, response: Response,db: DBSession, protect: ProtectedRoute):
    await db.delete(protect.refresh)

    response.delete_cookie("access", path="/")
    response.delete_cookie("refresh", path="/api/auth/refresh")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/change-password")
async def change_password(passwords: AdminChangePassword, protect: ProtectedRoute, db: DBSession):
    is_correct = password.verify(passwords.oldpassword, protect.user.password)
    if not is_correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")

    hashed = password.hash(passwords.newpassword)
    protect.user.password = hashed

    db.add(protect.user)
    await db.commit()

    return {"message": "Pasword changed"}

@router.post("/forgot")
async def forgot_password(user: AdminForgotPassword, db: DBSession):
    email = user.email
    result = await db.execute(
        select(Admin).where(Admin.email == email)
    )

    admin = result.scalar_one_or_none()

    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    token = password.gen_token()
    admin.forgot_token = token
    admin.forgot_created_at = datetime.now(timezone.utc)

    db.add(admin)
    await db.commit()

    html = forgot_password_html(token)
    await send_email("Reset Password Email", html)

    return {"message": "forgot password email has been sent"}