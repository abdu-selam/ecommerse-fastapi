from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.db import Base, engine, get_db
from app.routes import auth
from app.routes import product
from app.seed import seed as seed_start

DBSession = Annotated[AsyncSession, Depends(get_db)]

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # at startup
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    yield
    # at shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(product.router, prefix="/api/product", tags=["product"])

@app.get("/api/seed")
async def seed(db: DBSession):
    await seed_start(db)
    return {"message":"seeded everything!"}
