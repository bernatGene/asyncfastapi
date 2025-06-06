### Minimal FASTAPI async + Pooled psycopg DEMO

Simple demo using:
* FastAPI
* SQLModel
* SqlAlchemy
* Psycopg

To demonstarte concurrency/pooling/performance. 

## Installation/Setup

### Postgres

It requires to have a local postgres instance, you can spin up one with docker like so:
```bash
docker run -it --rm  -p 5433:5432 --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword postgres
```

### FastAPI

Through `uv`, just run:
```bash
uv sync
source .venv/bin/activate
```

Next, do the alembic migration
```
alembic upgrade head
```

Then run uvicorn
```bash
uvicorn main_asyncpg:app --host 0.0.0.0 --port 8001 --reload
```

### Testing

I added a notebook, `testendpoints.ipynb` with a little example, expand it as you see fit. 

