from typing import Generator, Annotated
import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlmodel import select, func
from sqlmodel import Session
from models import Hero, Heroes

DATABASE_URL_DIALECT = (
    "postgresql+psycopg://postgres:mysecretpassword@127.0.0.1:5433/postgres"
)


app = FastAPI(
    title="Test FASTAPI SQLALCHEMY SQLMODEL",
    description="TBD",
    version="0.1.0",
)


engine = create_engine(
    DATABASE_URL_DIALECT,
)


def get_session() -> Generator[Session, None, None]:
    session = sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False,
    )
    with session() as sess:
        yield sess


SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep):
    session.add(hero)
    try:
        session.commit()
        return hero
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Hero already exists")


@app.get("/heroes/{hero_id}/")
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.get("/heroes/")
def read_heroes(session: SessionDep):
    count = session.exec(select(func.count()).select_from(Hero))
    res = session.exec(select(Hero))
    return Heroes(data=res.all(), count=count.one())


@app.get("/pool-status/")
def pool_status():
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
    }


@app.post("/heroes/minimal/")
def create_hero_minimal():
    return {"id": 1, "name": "test", "country": "test"}


@app.get("/asyncio-stats/")
def asyncio_stats():
    loop = asyncio.get_event_loop()
    tasks = asyncio.all_tasks(loop)

    return {
        "total_tasks": len(tasks),
        "loop_running": loop.is_running(),
        "loop_debug": loop.get_debug(),
    }
