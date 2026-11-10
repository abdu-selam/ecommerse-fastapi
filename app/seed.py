from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from sqlalchemy import select

from app.models.admin import Admin
from app.utils.env import settings
from app.utils import password

async def create_admin(db: AsyncSession):
    result = await db.execute(
        select(Admin).where(Admin.email == settings.ADMIN_EMAIL)
    )
    admin = result.scalar_one_or_none()
    if admin:
        return

    hashed = password.hash(settings.ADMIN_PASS)

    admin = Admin(
        id=str(uuid4()),
        email=settings.ADMIN_EMAIL,
        name=settings.ADMIN_NAME,
        password=hashed
    )

    db.add(admin)
    await db.commit()

async def seed(db: AsyncSession):
    await create_admin(db)