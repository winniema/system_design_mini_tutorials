from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Field, SQLModel, Session
from database import create_db_and_tables, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_session)]

# Schema
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str



@app.get("/")
async def get():
    return {"message": "Hello World Winnie"}

@app.post("/heroes/")
def create_hero(name: str, session: SessionDep) -> Hero:
    hero = Hero(name=name, secret_name=f"secrete_{name}")
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero