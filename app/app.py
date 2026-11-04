from fastapi import FastAPI
from app.configs.db import Base, engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # at startup
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    yield
    # at shutdown
    engine.dispose()

app = FastAPI(lifespan=lifespan)
