from typing import AsyncGenerator, Annotated
import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from models import Hero, Heroes

DATABASE_URL_DIALECT = (
    "postgresql+psycopg://postgres:mysecretpassword@127.0.0.1:5433/postgres"
)


app = FastAPI(
    title="Test FASTAPI SQLALCHEMY SQLMODEL",
    description="TBD",
    version="0.1.0",
)


engine = create_async_engine(
    DATABASE_URL_DIALECT,
    pool_size=100,
    max_overflow=100,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post("/heroes/")
async def create_hero(hero: Hero, session: SessionDep):
    session.add(hero)
    try:
        await session.commit()
        return hero
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Hero already exists")


@app.get("/heroes/{hero_id}/")
async def read_hero(hero_id: int, session: SessionDep):
    hero = await session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.get("/heroes/")
async def read_heroes(session: SessionDep):
    count = await session.exec(select(func.count()).select_from(Hero))
    res = await session.exec(select(Hero))
    return Heroes(data=res.all(), count=count.one())


@app.get("/pool-status/")
async def pool_status():
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
    }


@app.post("/heroes/minimal/")
async def create_hero_minimal():
    return {"id": 1, "name": "test", "country": "test"}


@app.get("/asyncio-stats/")
async def asyncio_stats():
    loop = asyncio.get_event_loop()
    tasks = asyncio.all_tasks(loop)

    return {
        "total_tasks": len(tasks),
        "loop_running": loop.is_running(),
        "loop_debug": loop.get_debug(),
    }
