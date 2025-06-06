from sqlmodel import SQLModel, Field


class Hero(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    country: str | None = None


class Heroes(SQLModel):
    data: list[Hero]
    count: int
